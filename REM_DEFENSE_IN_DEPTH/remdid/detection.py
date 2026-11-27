"""L2: complementary detection signals over UNTRUSTED segments. Detection supplies evidence; it never authorizes.

Sub-detectors (declared before any REM-DiD scoring; word lists are generic and listed in 43_DETECTION_SPEC.md):
  D_pattern   : REM v1.0 instruction-pattern detector (x_ctx2 baseline, unchanged, imported from rem/)
  D_role      : role / delimiter manipulation (pseudo-markup tags, chat-role prefixes, special tokens)
  D_override  : attempts to override the user's intent or escalate privileges
  D_fin       : financial directive = imperative payment/credential verb AND an account identifier, amount or
                password in the same untrusted segment (expected to fire on legitimate bills too: measured)
Honesty note: the designer knew AgentDojo's templates. Detection figures on those templates are therefore
optimistic; paraphrased and obfuscated variants are evaluated separately (SIG-2).

Failure semantics: a detector that raises, exceeds its time budget, or returns a non-boolean is UNAVAILABLE for
that segment. Unavailable is never treated as "not fired" (fail-safe; consumed by the decision layer).
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Mapping, Optional, Sequence, Tuple

ROLE_RE = re.compile(
    r"(<\s*/?\s*[A-Z][A-Z_ ]{2,}\s*>)|(^|\n)\s*(system|assistant|developer)\s*:|<\|[^|]{1,20}\|>|\[/?INST\]|"
    r"(^|\n)\s*#{2,}\s*(instruction|system|new task)", re.IGNORECASE)
OVERRIDE_RE = re.compile(
    r"\b(ignore|disregard|forget)\b[^.\n]{0,40}\b(instruction|instructions|above|previous|prior|earlier|task)\b|"
    r"\bbefore you (can )?(solve|complete|do|finish|continue)\b|\bnew instructions?\b|\binstead of\b|"
    r"\bdo not (tell|inform|mention|notify)\b|\byour (new |real |actual )?task is\b|\boverride\b|"
    r"\b(important|urgent) (message|instruction|notice) (from|for)\b|\byou (must|have to) (first|now)\b",
    re.IGNORECASE)
FIN_VERB_RE = re.compile(r"\b(send|transfer|pay|wire|move|redirect|change|update|modify|set)\b", re.IGNORECASE)
FIN_OBJ_RE = re.compile(r"\b[A-Z]{2}\d{2}(?:[\s\-]?[A-Z0-9]){10,30}\b|\bpassword\b|[$€£]\s?\d|\b\d+(?:\.\d+)?\s?(?:usd|eur|gbp|dollars|euros)\b",
                        re.IGNORECASE)


@dataclass(frozen=True)
class DetectorResult:
    name: str
    available: bool
    fired: bool
    latency_ms: float
    error: Optional[str] = None


def _role(text: str) -> bool:
    return bool(ROLE_RE.search(text))


def _override(text: str) -> bool:
    return bool(OVERRIDE_RE.search(text))


def _fin(text: str) -> bool:
    return bool(FIN_VERB_RE.search(text)) and bool(FIN_OBJ_RE.search(text))


class DetectorSuite:
    """Runs every sub-detector on a text; isolates failures; optional per-detector failure injection."""

    def __init__(self, pattern_detector=None, budget_ms: float = 50.0,
                 disabled: Sequence[str] = (), failing: Sequence[str] = ()) -> None:
        self.detectors: Dict[str, Callable[[str], bool]] = {}
        if pattern_detector is not None:
            self.detectors["D_pattern"] = lambda t: bool(pattern_detector.fired(t))
        self.detectors.update({"D_role": _role, "D_override": _override, "D_fin": _fin})
        self.budget_ms = budget_ms
        self.disabled = set(disabled)      # bypass modelling: detector evaded (reports not fired)
        self.failing = set(failing)        # failure injection: detector unavailable

    def run(self, text: str) -> List[DetectorResult]:
        out = []
        for name, fn in self.detectors.items():
            t0 = time.perf_counter()
            if name in self.failing:
                out.append(DetectorResult(name, False, False, 0.0, "injected_failure"))
                continue
            try:
                v = fn(text)
                ms = (time.perf_counter() - t0) * 1e3
                if not isinstance(v, bool):
                    out.append(DetectorResult(name, False, False, ms, "invalid_output"))
                elif ms > self.budget_ms:
                    out.append(DetectorResult(name, False, False, ms, "timeout"))
                else:
                    out.append(DetectorResult(name, True, False if name in self.disabled else v, ms))
            except Exception as exc:  # isolated: one detector's failure does not affect the others
                out.append(DetectorResult(name, False, False, (time.perf_counter() - t0) * 1e3, repr(exc)[:80]))
        return out


@dataclass
class SegmentDetection:
    seg_index: int
    results: Tuple[DetectorResult, ...]

    @property
    def fired(self) -> bool:
        return any(r.fired for r in self.results)

    @property
    def any_unavailable(self) -> bool:
        return any(not r.available for r in self.results)

    def fired_names(self) -> Tuple[str, ...]:
        return tuple(r.name for r in self.results if r.fired)


def call_linked(lineages: Mapping[str, "object"], detections: Mapping[int, SegmentDetection],
                kinds=("iban", "text", "id")) -> Tuple[Optional[bool], Tuple[str, ...]]:
    """Call-linked injection evidence: a sensitive identity value of THIS call occurs in an untrusted segment on
    which a detector fired. Returns (True|False|None, reasons); None = cannot tell (a relevant segment had an
    unavailable detector and none fired) -> the decision layer treats None as missing evidence (fail-safe)."""
    unknown, reasons = False, []
    for f, lin in lineages.items():
        if lin.kind not in kinds:
            continue
        for i in lin.segments:
            d = detections.get(i)
            if d is None:
                continue
            if d.fired:
                reasons.append(f"{f}<-seg{i}:{'+'.join(d.fired_names())}")
            elif d.any_unavailable:
                unknown = True
    if reasons:
        return True, tuple(reasons)
    return (None if unknown else False), ()
