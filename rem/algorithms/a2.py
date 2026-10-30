"""A2 — observe-only sequential behavioural analysis (Chapter 3 Sec. 3.11.10).

Under the user decision of 27 Oct 2026 and ``CLAUDE.md``, A2 is the optional,
offline, observe-only CUSUM analysis. It reports alarms, per-episode false-alarm
rates and detection delays; it issues NO verdict and has NO mitigation. An
A2-driven enforcement policy and an A3+A2 retrained variant are recorded as
SUPERVISOR DECISION REQUIRED and are deliberately not implemented.

Parameter determination (Chapter 3):
    q0   empirical rate of e_t = 1 on benign fitting steps, floored at q0_floor;
    q1   declared and reported over a range;
    h_G  smallest value for which the per-episode false-alarm rate (Eq. 3.18)
         on benign fitting episodes does not exceed the declared target.
Detection delay tau_d = T_A - nu, T_A >= nu (Eq. 3.19), where nu is the first
step at which injected content enters the context.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import numpy as np

from rem.algorithms.behavior.cusum import BernoulliCusum

__all__ = ["A2Fit", "fit_a2", "episode_false_alarm_rate", "A2EpisodeResult", "evaluate_episode"]


@dataclass(frozen=True)
class A2Fit:
    q0: float
    q1: float
    h: float
    benign_false_alarm: float
    q0_raw: float


def episode_false_alarm_rate(cusum: BernoulliCusum, benign_episodes: Sequence[Sequence[int]], h: float) -> float:
    """FA_ep(h) = fraction of benign episodes whose max G_t >= h (Eq. 3.18)."""
    if not benign_episodes:
        raise ValueError("No benign episodes.")
    hits = sum(1 for ep in benign_episodes if ep and max(cusum.path(ep)) >= h)
    return hits / len(benign_episodes)


def fit_a2(
    benign_episodes: Sequence[Sequence[int]],
    q1: float,
    q0_floor: float,
    false_alarm_target: float,
) -> A2Fit:
    """Estimate q0, then choose the smallest h_G meeting the false-alarm target."""
    steps = [e for ep in benign_episodes for e in ep]
    if not steps:
        raise ValueError("No benign steps to estimate q0.")
    q0_raw = float(np.mean(steps))
    q0 = max(q0_raw, q0_floor)
    if not q0 < q1:
        raise ValueError(f"Estimated q0={q0:.4f} is not below declared q1={q1}; CUSUM undefined.")
    cusum = BernoulliCusum(q0, q1)
    maxima = sorted({max(cusum.path(ep)) for ep in benign_episodes if ep})
    # Candidate thresholds: just above each attained maximum, plus the smallest positive increment.
    candidates = sorted({np.nextafter(m, np.inf) for m in maxima} | {cusum.increment(1)})
    for h in candidates:
        if h <= 0:
            continue
        fa = episode_false_alarm_rate(cusum, benign_episodes, h)
        if fa <= false_alarm_target:
            return A2Fit(q0=q0, q1=q1, h=float(h), benign_false_alarm=fa, q0_raw=q0_raw)
    raise RuntimeError("No threshold meets the false-alarm target.")  # pragma: no cover


@dataclass(frozen=True)
class A2EpisodeResult:
    alarm_time: Optional[int]
    max_statistic: float
    delay: Optional[int]
    alarm_before_change: bool


def evaluate_episode(fit: A2Fit, indicators: Sequence[int], change_point: Optional[int]) -> A2EpisodeResult:
    """Run the fitted CUSUM on one episode.

    Args:
        indicators: e_1..e_T.
        change_point: nu (1-based) — first step whose context contains injected
            content; None for benign episodes.
    """
    cusum = BernoulliCusum(fit.q0, fit.q1)
    path = cusum.path(indicators)
    t_a = cusum.alarm_time(path, fit.h)
    delay = None
    before = False
    if t_a is not None and change_point is not None:
        if t_a >= change_point:
            delay = t_a - change_point
        else:
            before = True
    return A2EpisodeResult(t_a, max(path) if path else 0.0, delay, before)
