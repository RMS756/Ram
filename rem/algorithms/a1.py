"""A1 — consequence-independent operating-point baseline (Chapter 3 Sec. 3.7.7, B1).

Master-prompt name A1 maps to Chapter 3 baseline B1 under the user decision of
27 Oct 2026 and ``CLAUDE.md`` ("The operating-point threshold policy is a
BASELINE ONLY. It is NOT a second primary methodology.").

Thresholds (Eq. 3.14):
    theta(alpha) = min { theta : FPR_val(theta) <= alpha },
    FPR_val(theta) = |{ i in D_val^benign : p_i >= theta }| / |D_val^benign|,
with theta ranging over the observed benign probabilities.

Verdict: Block if p >= theta(alpha_blk); Modify if theta(alpha_mod) <= p <
theta(alpha_blk) and Modify is feasible, otherwise Block; Allow otherwise.
Predicates D1 and D2 apply as in REM, so B1 issues Escalate only through D2.

Implementation note on Eq. 3.14: theta ranges over observed probabilities; to
keep FPR <= alpha even when the largest benign probability is reached,
``theta`` may also take the value just above the maximum benign probability
(``nextafter(max, inf)``), which flags no benign step.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

from rem.algorithms.decision.policy import PredicatePolicy
from rem.core.results import Verdict

__all__ = ["operating_threshold", "A1Thresholds", "A1Policy", "A1Decision"]


def operating_threshold(benign_probabilities: Sequence[float], alpha: float) -> float:
    """theta(alpha) of Eq. 3.14.

    Raises:
        ValueError: On an empty benign set or alpha outside [0, 1].
    """
    p = np.sort(np.asarray(benign_probabilities, dtype=float))
    if p.size == 0:
        raise ValueError("theta(alpha) needs benign validation probabilities.")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must lie in [0, 1].")
    candidates = np.unique(np.append(p, np.nextafter(p[-1], np.inf)))
    n = p.size
    for theta in candidates:  # ascending: the first feasible one is the minimum
        fpr = np.count_nonzero(p >= theta) / n
        if fpr <= alpha:
            return float(theta)
    return float(candidates[-1])  # pragma: no cover - last candidate has FPR 0


@dataclass(frozen=True)
class A1Thresholds:
    theta_blk: float
    theta_mod: float
    alpha_blk: float
    alpha_mod: float

    @classmethod
    def fit(cls, benign_probabilities: Sequence[float], alpha_blk: float, alpha_mod: float) -> "A1Thresholds":
        if not alpha_mod > alpha_blk:
            raise ValueError("Chapter 3 requires alpha_mod > alpha_blk.")
        return cls(
            theta_blk=operating_threshold(benign_probabilities, alpha_blk),
            theta_mod=operating_threshold(benign_probabilities, alpha_mod),
            alpha_blk=alpha_blk,
            alpha_mod=alpha_mod,
        )


@dataclass(frozen=True)
class A1Decision:
    verdict: Verdict
    source: str
    probability: float


class A1Policy:
    """B1 verdict rule; ignores consequence tiers by construction."""

    name = "A1_B1_threshold_baseline"

    def __init__(self, thresholds: A1Thresholds, predicates: PredicatePolicy) -> None:
        self.t = thresholds
        self.predicates = predicates

    def decide(self, p: float, tier: int, tool: str, available: Mapping[str, bool]) -> A1Decision:
        forced = self.predicates.evaluate(tool, tier, available)
        if forced.verdict is not None:
            return A1Decision(forced.verdict, forced.source or "predicate", float(p))
        if p >= self.t.theta_blk:
            return A1Decision(Verdict.BLOCK, "threshold_blk", float(p))
        if p >= self.t.theta_mod:
            if Verdict.MODIFY in self.predicates.feasible(tool):
                return A1Decision(Verdict.MODIFY, "threshold_mod", float(p))
            return A1Decision(Verdict.BLOCK, "threshold_mod_infeasible", float(p))
        return A1Decision(Verdict.ALLOW, "threshold", float(p))
