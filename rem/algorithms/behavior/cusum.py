"""Bernoulli CUSUM (Chapter 3 Sec. 3.11.10) — OBSERVE-ONLY.

``CLAUDE.md``: "CUSUM is OPTIONAL and OBSERVE-ONLY. CUSUM MUST NOT enter the core
verdict path." This module produces statistics and alarm times for offline
analysis. It has no interface to the decision engine and no verdict output.

Equations (Chapter 3):
    l_t = e_t ln(q1/q0) + (1 - e_t) ln((1 - q1)/(1 - q0))      (3.15)
    G_t = max(0, G_{t-1} + l_t),  G_0 = 0                         (3.16)
    T_A = min { t : G_t >= h_G }                                   (3.17)
Sources: Page (1954); Basseville & Nikiforov (1993); Bernoulli specialisation
derived by substitution (Reynolds & Stoumbos, 1999, treat Bernoulli CUSUM).

No optimality is claimed: Lorden (1971) and Moustakides (1986) hold under
independence and known pre/post-change distributions, which agent trajectories
do not satisfy.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Mapping, Optional, Sequence

__all__ = ["deviation_indicator", "BernoulliCusum", "OBSERVE_ONLY"]

OBSERVE_ONLY = True


def deviation_indicator(x: Mapping[str, float]) -> int:
    """e_t of Chapter 3 Sec. 3.11.10 [indicator set pending supervisor approval].

    e_t = 1 if any of x_beh1, x_beh3, x_beh4, x_act1 equals 1, or x_beh2 equals 1.
    """
    return int(
        any(float(x.get(k, 0.0)) == 1.0 for k in ("x_beh1", "x_beh3", "x_beh4", "x_act1"))
        or float(x.get("x_beh2", 0.0)) == 1.0
    )


@dataclass(frozen=True)
class BernoulliCusum:
    """CUSUM for Bernoulli observations with declared q0 < q1."""

    q0: float
    q1: float

    def __post_init__(self) -> None:
        if not 0.0 < self.q0 < self.q1 < 1.0:
            raise ValueError("Chapter 3 requires 0 < q0 < q1 < 1.")

    def increment(self, e: int) -> float:
        """l_t (Eq. 3.15)."""
        if e:
            return math.log(self.q1 / self.q0)
        return math.log((1.0 - self.q1) / (1.0 - self.q0))

    def path(self, indicators: Sequence[int]) -> List[float]:
        """G_1..G_T for one episode, reset at the episode start (Eq. 3.16)."""
        g = 0.0
        out = []
        for e in indicators:
            g = max(0.0, g + self.increment(int(e)))
            out.append(g)
        return out

    @staticmethod
    def alarm_time(path: Sequence[float], h: float) -> Optional[int]:
        """T_A (1-based step index) or None if no alarm (Eq. 3.17)."""
        for t, g in enumerate(path, start=1):
            if g >= h:
                return t
        return None
