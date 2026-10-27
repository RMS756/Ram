"""A3 — cost-sensitive decision-theoretic REM verdict (primary method).

Master-prompt name A3 = the frozen REM decision layer of ``CLAUDE.md``
(expected-loss Bayes verdict on the calibrated probability) completed with the
Chapter 3 feasible set and policy predicates:

    1. predicates D1, D2 (Sec. 3.7.4) — if one fires it fixes the verdict;
    2. otherwise R_t(v) = (1 - p_t) L(v,0,k_t) + p_t L(v,1,k_t) for v in V(a_t)
       (Eq. 3.6, computed by the frozen ``ExpectedLossDecisionEngine``);
    3. v_t = argmin R_t(v) (Eq. 3.7).

Ties (SC-2, UNRESOLVED): the frozen implementation raises ``VerdictTieError``;
Chapter 3 resolves ties toward Block > Escalate > Modify > Allow. This module
supports both behaviours explicitly through ``tie_mode`` and never chooses one
silently:

    * ``"raise"`` (frozen behaviour, default);
    * ``"record_chapter3_order"`` (exploratory only): the tie is recorded on the
      result (``tie=True``) and the Chapter 3 order is applied so the run can
      continue; every such step is counted and reported.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Mapping, Optional, Tuple

from rem.algorithms.decision.expected_loss import ExpectedLossDecisionEngine, LossGrid, VerdictTieError
from rem.algorithms.decision.policy import PredicatePolicy
from rem.core.results import Verdict

__all__ = ["A3Decision", "A3Policy", "CHAPTER3_TIE_ORDER"]

#: Chapter 3 Eq. 3.7 tie order (most restrictive first). Used only in tie_mode
#: "record_chapter3_order". SC-2 remains unresolved.
CHAPTER3_TIE_ORDER: Tuple[Verdict, ...] = (Verdict.BLOCK, Verdict.ESCALATE, Verdict.MODIFY, Verdict.ALLOW)


@dataclass(frozen=True)
class A3Decision:
    """Verdict and its provenance for the audit record."""

    verdict: Verdict
    source: str                                  # "D1", "D2" or "expected_loss"
    probability: float
    tier: int
    risks: Mapping[str, float] = field(default_factory=dict)
    feasible: Tuple[str, ...] = ()
    tie: bool = False
    tie_set: Tuple[str, ...] = ()


class A3Policy:
    """Expected-loss verdict with D1/D2 and a feasible set.

    Args:
        loss_grid: L(v, y, k) (Table 3.13).
        predicates: Declared predicate policy.
        tie_mode: ``"raise"`` or ``"record_chapter3_order"`` (see module doc).
    """

    name = "A3_expected_loss_rem"

    def __init__(self, loss_grid: LossGrid, predicates: PredicatePolicy, *, tie_mode: str = "raise") -> None:
        if tie_mode not in ("raise", "record_chapter3_order"):
            raise ValueError(f"Unknown tie_mode {tie_mode!r}.")
        self.engine = ExpectedLossDecisionEngine(loss_grid)
        self.predicates = predicates
        self.tie_mode = tie_mode

    def decide(self, p: float, tier: int, tool: str, available: Mapping[str, bool]) -> A3Decision:
        """Return the A3 verdict for one proposed call."""
        forced = self.predicates.evaluate(tool, tier, available)
        feasible = self.predicates.feasible(tool)
        if forced.verdict is not None:
            return A3Decision(forced.verdict, forced.source or "predicate", float(p), int(tier),
                              feasible=tuple(v.value for v in feasible))
        risks: Dict[Verdict, float] = {v: self.engine.conditional_risk(v, p, tier) for v in feasible}
        m = min(risks.values())
        winners = [v for v, r in risks.items() if r == m]
        tie = len(winners) > 1
        if tie and self.tie_mode == "raise":
            raise VerdictTieError(
                f"Verdicts {sorted(v.value for v in winners)} tie at p={p!r}, k={tier!r}; "
                "SC-2 is unresolved."
            )
        verdict = next(v for v in CHAPTER3_TIE_ORDER if v in winners) if tie else winners[0]
        return A3Decision(
            verdict=verdict,
            source="expected_loss",
            probability=float(p),
            tier=int(tier),
            risks={v.value: r for v, r in risks.items()},
            feasible=tuple(v.value for v in feasible),
            tie=tie,
            tie_set=tuple(v.value for v in winners) if tie else (),
        )
