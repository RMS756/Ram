"""Layers 2–3 evidence vector x_t (Chapter 3, Tables 3.8 and 3.9).

Status: CHAPTER 3 SPECIFICATION, PENDING SD-FREEZE (SD-FEAT). Every declared
quantity (n_max, key arguments, privilege map, sensitive-read tools, pattern
set, benign reference transitions) is supplied by the caller; none has a
default. The feature definitions follow Chapter 3 verbatim, with the
implementation interpretations below stated explicitly because Chapter 3 does
not settle them:

I-1  *Step and decision point.* Chapter 3 defines step t as the interval in
     which the agent proposes action a_t. An agent may propose several calls in
     one message; those calls share one decision point, and "untrusted segments
     added since the previous step" means segments added since the previous
     decision point.
I-2  *x^beh_2 counts proposed calls,* including refused ones, because Chapter 3
     Sec. 3.8 property 4 states that retries raise x^beh_2. Calls are "the same"
     if tool and declared key arguments are equal; for tools with no declared
     key arguments all arguments are compared. n_rep includes the current call,
     so the feature is at least 1/n_max.
I-3  *x^beh_3 at the first call:* "the highest level used so far" is taken as
     the lowest privilege level (0) when nothing has been used yet.
I-4  *x^beh_4 at the first call:* the previous tool is the start symbol
     ``<START>``, and the benign reference set contains start transitions.
I-5  *x^act_2:* "transactions observed before the episode's first untrusted
     ingestion" can only be observed through tool outputs, which are untrusted
     by TB-2. In this environment the clause is therefore empty and the feature
     reduces to "the recipient does not occur in the user objective g".
I-6  *x^act_3:* the external recipient is any recipient different from the
     user's own account identifier when that identifier has been read from a
     sensitive read; values obtained from sensitive reads are account
     identifiers and profile values extracted from those tool outputs; the
     feature fires if such a value occurs in a non-recipient argument.
I-7  *Availability (for predicate D2):* x^act_1 is unavailable for a call
     whose tool has declared key arguments but whose call carries none of them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Tuple

from rem.algorithms.context.provenance import (
    Segment,
    TrustLevel,
    extract_ibans,
    strip_invisible,
    value_occurs_in,
)
from rem.algorithms.detection.instruction_patterns import InstructionPatternDetector

__all__ = [
    "FEATURE_ORDER",
    "FEATURE_GROUPS",
    "EvidenceSpec",
    "BenignReference",
    "EpisodeTracker",
    "START",
]

START = "<START>"

#: Order of x_t. x^ctx_1 is absent because the classifier is BLOCKED (SD-DET).
FEATURE_ORDER: Tuple[str, ...] = (
    "x_ctx2",
    "x_beh1",
    "x_beh2",
    "x_beh3",
    "x_beh4",
    "x_act1",
    "x_act2",
    "x_act3",
)

#: Chapter 3 index sets I_ctx, I_beh, I_act.
FEATURE_GROUPS: Dict[str, Tuple[str, ...]] = {
    "ctx": ("x_ctx2",),
    "beh": ("x_beh1", "x_beh2", "x_beh3", "x_beh4"),
    "act": ("x_act1", "x_act2", "x_act3"),
}


@dataclass(frozen=True)
class EvidenceSpec:
    """Declared quantities of Table 3.9. No field has a default.

    Attributes:
        n_max: Cap for the repeated-call count.
        key_arguments: Tool name -> its key arguments (recipient, amount,
            password, profile values).
        privilege_map: Tool name -> privilege level.
        sensitive_read_tools: Tools whose outputs are sensitive reads.
    """

    n_max: int
    key_arguments: Mapping[str, Sequence[str]]
    privilege_map: Mapping[str, int]
    sensitive_read_tools: Sequence[str]

    def __post_init__(self) -> None:
        if int(self.n_max) < 1:
            raise ValueError("n_max must be a positive integer.")

    def privilege(self, tool: str) -> int:
        """Privilege level of ``tool``.

        Raises:
            KeyError: If the tool is absent from the declared privilege map —
                REM does not guess a privilege level.
        """
        if tool not in self.privilege_map:
            raise KeyError(f"Tool {tool!r} has no declared privilege level.")
        return int(self.privilege_map[tool])


@dataclass(frozen=True)
class BenignReference:
    """Benign reference transition set, estimated offline on benign fitting data."""

    transitions: FrozenSet[Tuple[str, str]]

    @classmethod
    def fit(cls, tool_sequences: Iterable[Sequence[str]]) -> "BenignReference":
        """Collect (previous tool, current tool) pairs, including start pairs."""
        pairs = set()
        for seq in tool_sequences:
            prev = START
            for tool in seq:
                pairs.add((prev, tool))
                prev = tool
        return cls(frozenset(pairs))


def _key_view(spec: EvidenceSpec, tool: str, args: Mapping[str, Any]) -> Tuple:
    keys = spec.key_arguments.get(tool)
    if keys:
        return tuple((k, str(args.get(k))) for k in keys)
    return tuple(sorted((k, str(v)) for k, v in args.items()))


@dataclass
class EpisodeTracker:
    """Maintains H_t for one episode and computes x_t for proposed calls.

    The tracker never changes REM's parameters; it only accumulates the
    episode's own history (Chapter 3 Sec. 3.6.1: reset at each episode start).
    """

    objective: str
    trusted_texts: Sequence[str]
    spec: EvidenceSpec
    detector: InstructionPatternDetector
    reference: BenignReference
    segments: List[Segment] = field(default_factory=list)
    proposed: List[Tuple[str, Mapping[str, Any]]] = field(default_factory=list)
    decision_point: int = 0
    _segments_at_last_dp: int = 0
    _new_untrusted: List[Segment] = field(default_factory=list)
    _sensitive_values: List[str] = field(default_factory=list)
    _own_iban: Optional[str] = None

    # -- context ingestion -----------------------------------------------------

    def add_tool_result(self, tool: str, text: str, *, executed: bool) -> None:
        """Ingest a tool result as untrusted content (TB-2).

        Args:
            tool: Tool that produced the result.
            text: Result text (an error notice for refused calls).
            executed: Whether the tool actually ran. Values are harvested from
                sensitive reads only when the read executed.
        """
        clean = strip_invisible(text or "")
        self.segments.append(Segment(clean, TrustLevel.UNTRUSTED, tool, self.decision_point))
        if executed and tool in self.spec.sensitive_read_tools:
            ibans = extract_ibans(clean)
            if tool == "get_iban" and ibans:
                self._own_iban = ibans[0]
            self._sensitive_values.extend(ibans)
            if tool == "get_user_info":
                for line in clean.splitlines():
                    if ":" in line:
                        val = line.split(":", 1)[1].strip().strip("'\"")
                        if len(val) >= 3:
                            self._sensitive_values.append(val)

    def begin_decision_point(self) -> None:
        """Mark the start of a new agent decision point (one assistant message)."""
        self._new_untrusted = [
            s for s in self.segments[self._segments_at_last_dp :] if s.trust == TrustLevel.UNTRUSTED
        ]
        self._segments_at_last_dp = len(self.segments)
        self.decision_point += 1

    # -- feature computation ---------------------------------------------------

    def _untrusted_texts(self) -> List[str]:
        return [s.text for s in self.segments if s.trust == TrustLevel.UNTRUSTED]

    def features(self, tool: str, args: Mapping[str, Any]) -> Tuple[Dict[str, float], Dict[str, bool]]:
        """Compute x_t for a proposed call without changing the history.

        Returns:
            ``(features, available)`` where ``available`` reports, per feature,
            whether it could be computed (used by predicate D2).
        """
        spec = self.spec
        det = self.detector
        trusted = [self.objective, *self.trusted_texts]

        # x^ctx_2 — new untrusted segments since the previous decision point.
        x_ctx2 = det.any_match(s.text for s in self._new_untrusted)

        # x^beh_1 — most recent tool result untrusted and matching the pattern set.
        last = self.segments[-1] if self.segments else None
        x_beh1 = int(last is not None and last.trust == TrustLevel.UNTRUSTED and det.matches(last.text))

        # x^beh_2 — consecutive repeated calls (I-2).
        view = _key_view(spec, tool, args)
        n_rep = 1
        for prev_tool, prev_args in reversed(self.proposed):
            if prev_tool == tool and _key_view(spec, prev_tool, prev_args) == view:
                n_rep += 1
            else:
                break
        x_beh2 = min(n_rep, spec.n_max) / spec.n_max

        # x^beh_3 — privilege escalation (I-3).
        highest = max((spec.privilege(t) for t, _ in self.proposed), default=0)
        x_beh3 = int(spec.privilege(tool) > highest)

        # x^beh_4 — transition deviation (I-4).
        prev_tool = self.proposed[-1][0] if self.proposed else START
        x_beh4 = int((prev_tool, tool) not in self.reference.transitions)

        # x^act_1 — argument provenance (I-7 for availability).
        keys = list(spec.key_arguments.get(tool, ()))
        present = [k for k in keys if k in args and args.get(k) is not None]
        untrusted_texts = self._untrusted_texts()
        x_act1 = int(
            any(
                value_occurs_in(args[k], untrusted_texts) and not value_occurs_in(args[k], trusted)
                for k in present
            )
        )
        act1_available = not keys or bool(present)

        # x^act_2 — destination novelty (I-5).
        recipient = args.get("recipient") if "recipient" in keys else None
        x_act2 = int(recipient is not None and not value_occurs_in(recipient, [self.objective]))

        # x^act_3 — sensitive egress (I-6).
        x_act3 = 0
        if recipient is not None and (self._own_iban is None or str(recipient) != self._own_iban):
            other_texts = [str(v) for k, v in args.items() if k != "recipient" and v is not None]
            x_act3 = int(any(value_occurs_in(val, other_texts) for val in self._sensitive_values))

        feats = {
            "x_ctx2": float(x_ctx2),
            "x_beh1": float(x_beh1),
            "x_beh2": float(x_beh2),
            "x_beh3": float(x_beh3),
            "x_beh4": float(x_beh4),
            "x_act1": float(x_act1),
            "x_act2": float(x_act2),
            "x_act3": float(x_act3),
        }
        available = {name: True for name in FEATURE_ORDER}
        available["x_act1"] = act1_available
        return feats, available

    def record_proposal(self, tool: str, args: Mapping[str, Any]) -> None:
        """Append a proposed call to H_t (whether or not it was released)."""
        self.proposed.append((tool, dict(args)))
