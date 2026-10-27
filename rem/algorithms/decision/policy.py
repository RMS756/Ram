"""Policy predicates D1/D2 and the feasible verdict set (Chapter 3 Sec. 3.7.4–3.7.5).

Status: CHAPTER 3 SPECIFICATION, PENDING SUPERVISOR APPROVAL (SD-4). The
prohibited set Pi, the minimum tier k_D2, the evidence required per tier and the
restricted-tool set T_R are declared policy supplied by the caller.

D1 (prohibited action): if a_t in Pi, the verdict is Block irrespective of p_t.
D2 (missing required evidence): if evidence required for tier k_t cannot be
    computed and k_t >= k_D2, the verdict is Escalate.
Feasible set V(a_t): Allow, Escalate and Block always; Modify only if the tool
    of a_t belongs to T_R (the tools to which the Modify mechanism applies).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Mapping, Optional, Sequence, Tuple

from rem.core.results import Verdict

__all__ = ["PredicatePolicy", "PredicateOutcome", "STATUS"]

STATUS = "CHAPTER 3 SEC. 3.7.4 — PENDING SUPERVISOR APPROVAL (SD-4)"


@dataclass(frozen=True)
class PredicateOutcome:
    """Result of evaluating D1/D2 for one step."""

    verdict: Optional[Verdict]
    source: Optional[str]          # "D1", "D2" or None
    missing_evidence: Tuple[str, ...] = ()


@dataclass(frozen=True)
class PredicatePolicy:
    """Declared predicate policy.

    Attributes:
        prohibited: Pi — tool names whose calls are categorically prohibited.
        k_D2: Minimum tier at which missing evidence forces escalation.
        required_evidence: Feature names required at tiers >= k_D2.
        restricted_tools: T_R.
        enabled: False only in the "predicates disabled" ablation.
    """

    prohibited: FrozenSet[str]
    k_D2: int
    required_evidence: Tuple[str, ...]
    restricted_tools: FrozenSet[str]
    enabled: bool = True

    def evaluate(self, tool: str, tier: int, available: Mapping[str, bool]) -> PredicateOutcome:
        """Apply D1 then D2; return the forced verdict, if any."""
        if not self.enabled:
            return PredicateOutcome(None, None)
        if tool in self.prohibited:
            return PredicateOutcome(Verdict.BLOCK, "D1")
        if tier >= self.k_D2:
            missing = tuple(f for f in self.required_evidence if not available.get(f, False))
            if missing:
                return PredicateOutcome(Verdict.ESCALATE, "D2", missing)
        return PredicateOutcome(None, None)

    def feasible(self, tool: str) -> Tuple[Verdict, ...]:
        """V(a_t)."""
        base = [Verdict.ALLOW, Verdict.ESCALATE, Verdict.BLOCK]
        if tool in self.restricted_tools:
            base.insert(1, Verdict.MODIFY)
        return tuple(base)
