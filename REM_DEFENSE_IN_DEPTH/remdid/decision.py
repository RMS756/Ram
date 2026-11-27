"""L4: Decision Engine = 4A deterministic, non-compensatory authorization + 4B frozen REM v1.0 expected-loss verdict.

Precedence (declared in 44_DECISION_SPEC.md; the most restrictive outcome wins, so no rule can loosen another):
  P1  4A VIOLATION or NO_ENTRY on a state-changing call ............................ BLOCK
  P2  4A UNSPECIFIED / UNVERIFIABLE, or a MANDATORY input unavailable .............. ESCALATE
  P3  deterministic evidence on a sensitive value NOT pinned by a verified TAE entry:
        untrusted-only or missing lineage of an identity field (PROV),
        call-linked detection (DET), a behavioral rule (BEH) ......................... ESCALATE
  P4  4B: REM v1.0 verdict from calibrated p, consequence tier and expected loss ..... as computed (may tighten)
  final verdict = max severity over the active rules; ALLOW < MODIFY < ESCALATE < BLOCK.
A learned probability can never compensate a P1/P2/P3 outcome (non-compensatory). REM-DiD itself never emits
MODIFY: no Modify mechanism is declared (CLAUDE.md MITIGATION LOCK); a MODIFY from 4B keeps v1.0 semantics
(withhold the current call).
'pinned_release' variant: when 4A AUTHORIZED pins every sensitive field of the call, P4 is not consulted
(authorization-first). Both variants are evaluated; neither is adopted.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from rem.core.results import Verdict

SEVERITY = {Verdict.ALLOW: 0, Verdict.MODIFY: 1, Verdict.ESCALATE: 2, Verdict.BLOCK: 3}


@dataclass
class Rule:
    code: str
    verdict: Verdict
    layer: str


@dataclass
class Decision:
    verdict: Verdict
    rules: List[Rule] = field(default_factory=list)

    @property
    def sources(self) -> Tuple[str, ...]:
        return tuple(r.code for r in self.rules if SEVERITY[r.verdict] == SEVERITY[self.verdict])


def combine(rules: List[Rule]) -> Decision:
    if not rules:
        return Decision(Verdict.ALLOW, [])
    v = max((r.verdict for r in rules), key=lambda x: SEVERITY[x])
    return Decision(v, rules)
