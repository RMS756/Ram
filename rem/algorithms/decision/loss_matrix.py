"""Tier-indexed loss structure L(v, y, k) and its validity checks (Chapter 3 Sec. 3.7.5).

Status: the STRUCTURE is Chapter 3 Table 3.13; every NUMBER is policy pending
supervisor approval (SD-1). The builder takes all costs from the caller.

Implements:
  * Table 3.13 rows, with the Modify adversarial entry r_mod(k) * C_miss(k)
    derived under assumption A-Mod (Chapter 3 Eq. 3.5);
  * pairwise indifference thresholds pi_{v,v'}(k) = Delta_0 / (Delta_0 + Delta_1)
    (Eq. 3.8) and the Allow-Block threshold p*_k (Eq. 3.9);
  * the escalation feasibility condition (Eq. 3.10);
  * the dominance check of Sec. 3.7.5: a verdict that is never the strict
    minimiser for any p in [0, 1] is reported as unreachable.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from rem.algorithms.decision.expected_loss import LossGrid
from rem.core.results import Verdict

__all__ = [
    "LossSpec",
    "build_loss_grid",
    "indifference_threshold",
    "allow_block_threshold",
    "escalation_feasible",
    "reachable_verdicts",
    "risk_coefficients",
]


@dataclass(frozen=True)
class LossSpec:
    """Declared costs of Table 3.13 (all in common relative units).

    Attributes:
        C_FA: False intervention by Block on a legitimate action, per tier.
        C_miss: Missed adversarially induced action, per tier.
        C_mod: Modify on a legitimate action, per tier.
        C_esc: Escalation (assumes a reviewer who resolves it correctly).
        r_mod: Measured residual attack-success rate after Modify, per tier.
    """

    C_FA: Mapping[int, float]
    C_miss: Mapping[int, float]
    C_mod: Mapping[int, float]
    C_esc: float
    r_mod: Mapping[int, float]

    def __post_init__(self) -> None:
        tiers = set(self.C_FA)
        for name in ("C_miss", "C_mod", "r_mod"):
            if set(getattr(self, name)) != tiers:
                raise ValueError(f"{name} must cover exactly the tiers {sorted(tiers)}.")
        for name in ("C_FA", "C_miss", "C_mod"):
            if any(float(v) < 0 for v in getattr(self, name).values()):
                raise ValueError(f"{name} must be non-negative (Chapter 3 Sec. 3.7.5).")
        if float(self.C_esc) < 0:
            raise ValueError("C_esc must be non-negative.")
        if any(not 0.0 <= float(v) <= 1.0 for v in self.r_mod.values()):
            raise ValueError("r_mod(k) must lie in [0, 1].")

    @property
    def tiers(self) -> Tuple[int, ...]:
        return tuple(sorted(self.C_FA))


def build_loss_grid(spec: LossSpec, source: str) -> LossGrid:
    """Build L(v, y, k) exactly as Chapter 3 Table 3.13."""
    values = {}
    for k in spec.tiers:
        values[(Verdict.ALLOW, 0, k)] = 0.0
        values[(Verdict.ALLOW, 1, k)] = float(spec.C_miss[k])
        values[(Verdict.MODIFY, 0, k)] = float(spec.C_mod[k])
        values[(Verdict.MODIFY, 1, k)] = float(spec.r_mod[k]) * float(spec.C_miss[k])  # Eq. 3.5
        values[(Verdict.ESCALATE, 0, k)] = float(spec.C_esc)
        values[(Verdict.ESCALATE, 1, k)] = float(spec.C_esc)
        values[(Verdict.BLOCK, 0, k)] = float(spec.C_FA[k])
        values[(Verdict.BLOCK, 1, k)] = 0.0
    return LossGrid(values=values, source=source)


def risk_coefficients(grid: LossGrid, verdict: Verdict, tier: int) -> Tuple[float, float]:
    """Return (a, b) with R(v | p) = a + b p, a = L(v,0,k), b = L(v,1,k) - L(v,0,k)."""
    a = grid.loss(verdict, 0, tier)
    return a, grid.loss(verdict, 1, tier) - a


def indifference_threshold(grid: LossGrid, v: Verdict, v_prime: Verdict, tier: int) -> Optional[float]:
    """pi_{v,v'}(k) = Delta_0 / (Delta_0 + Delta_1) (Eq. 3.8); None if Delta_0 + Delta_1 <= 0."""
    d0 = grid.loss(v_prime, 0, tier) - grid.loss(v, 0, tier)
    d1 = grid.loss(v, 1, tier) - grid.loss(v_prime, 1, tier)
    if d0 + d1 <= 0:
        return None
    return d0 / (d0 + d1)


def allow_block_threshold(spec: LossSpec, tier: int) -> float:
    """p*_k = C_FA(k) / (C_FA(k) + C_miss(k)) (Eq. 3.9)."""
    return float(spec.C_FA[tier]) / (float(spec.C_FA[tier]) + float(spec.C_miss[tier]))


def escalation_feasible(spec: LossSpec, tier: int) -> bool:
    """Eq. 3.10 for {Allow, Escalate, Block}: C_esc < C_FA C_miss / (C_FA + C_miss)."""
    fa, miss = float(spec.C_FA[tier]), float(spec.C_miss[tier])
    return float(spec.C_esc) < fa * miss / (fa + miss)


def reachable_verdicts(
    grid: LossGrid, tier: int, feasible: Iterable[Verdict] = tuple(Verdict)
) -> Dict[Verdict, bool]:
    """Dominance check (Chapter 3 Sec. 3.7.5).

    A verdict is reachable if it is the unique minimiser of R(. | p) for some
    p in [0, 1]. Each R is affine in p, so it suffices to test the endpoints,
    all pairwise intersections inside [0, 1], and midpoints between them.
    """
    feas = list(feasible)
    coef = {v: risk_coefficients(grid, v, tier) for v in feas}
    points = {0.0, 1.0}
    for u, v in combinations(feas, 2):
        (au, bu), (av, bv) = coef[u], coef[v]
        if bu != bv:
            p = (av - au) / (bu - bv)
            if 0.0 <= p <= 1.0:
                points.add(p)
    pts = sorted(points)
    probes = list(pts) + [(a + b) / 2 for a, b in zip(pts, pts[1:])]
    out = {v: False for v in feas}
    for p in probes:
        risks = {v: coef[v][0] + coef[v][1] * p for v in feas}
        m = min(risks.values())
        winners = [v for v, r in risks.items() if r == m]
        if len(winners) == 1:
            out[winners[0]] = True
    return out
