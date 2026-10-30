"""Grouped bootstrap confidence intervals (Chapter 3 Sec. 3.11.9).

Resampling is done at the level of groups, not steps or episodes, because
episodes built from the same task templates are dependent (Chapter 3 Sec.
3.11.2). Attacked episodes are resampled by injection-task group and benign
episodes by user-task group, independently (stratified); the statistic is then
recomputed on the resampled collection. Percentile intervals (Efron, 1979).
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Hashable, List, Sequence, Tuple

import numpy as np

__all__ = ["grouped_bootstrap", "stratified_grouped_bootstrap"]


def _groups(items: Sequence[Any], key: Callable[[Any], Hashable]) -> Dict[Hashable, List[Any]]:
    out: Dict[Hashable, List[Any]] = {}
    for it in items:
        out.setdefault(key(it), []).append(it)
    return out


def grouped_bootstrap(
    items: Sequence[Any],
    group_key: Callable[[Any], Hashable],
    statistic: Callable[[Sequence[Any]], float],
    *,
    resamples: int,
    seed: int,
    level: float = 0.95,
) -> Tuple[float, float, float]:
    """Return (point estimate, lower, upper) with groups resampled with replacement."""
    groups = _groups(items, group_key)
    keys = list(groups)
    rng = np.random.default_rng(seed)
    point = float(statistic(items))
    stats = []
    for _ in range(resamples):
        chosen = rng.integers(0, len(keys), size=len(keys))
        sample = [it for c in chosen for it in groups[keys[c]]]
        val = statistic(sample)
        if val == val:  # drop NaN resamples
            stats.append(val)
    if not stats:
        return point, float("nan"), float("nan")
    lo, hi = np.quantile(stats, [(1 - level) / 2, 1 - (1 - level) / 2])
    return point, float(lo), float(hi)


def stratified_grouped_bootstrap(
    strata: Sequence[Tuple[Sequence[Any], Callable[[Any], Hashable]]],
    statistic: Callable[[Sequence[Any]], float],
    *,
    resamples: int,
    seed: int,
    level: float = 0.95,
) -> Tuple[float, float, float]:
    """Resample groups independently within each stratum, then pool."""
    prepared = []
    pooled: List[Any] = []
    for items, key in strata:
        g = _groups(items, key)
        prepared.append((list(g), g))
        pooled.extend(items)
    rng = np.random.default_rng(seed)
    point = float(statistic(pooled))
    stats = []
    for _ in range(resamples):
        sample: List[Any] = []
        for keys, g in prepared:
            if not keys:
                continue
            chosen = rng.integers(0, len(keys), size=len(keys))
            sample.extend(it for c in chosen for it in g[keys[c]])
        val = statistic(sample)
        if val == val:
            stats.append(val)
    if not stats:
        return point, float("nan"), float("nan")
    lo, hi = np.quantile(stats, [(1 - level) / 2, 1 - (1 - level) / 2])
    return point, float(lo), float(hi)
