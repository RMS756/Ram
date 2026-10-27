"""Runtime overhead measurement.

Measures the wall-clock cost REM adds to agent execution. The only arithmetic is
descriptive statistics over measured durations; there is no model and no
inference.

Sample-quantile definitions differ between statistical packages, so the
definition is pinned explicitly rather than left to whichever library is
installed.
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Sequence

from rem.traceability.registry import derivation

__all__ = ["LatencyRecorder", "mean", "quantile", "latency_report", "throughput"]

_HYNDMAN_FAN = (
    "Hyndman, R. J., & Fan, Y. (1996). Sample Quantiles in Statistical "
    "Packages. The American Statistician, 50(4), 361-365."
)


@derivation(
    statement="mean(x) = (1/n) * sum_i x_i",
    algorithm="Descriptive statistics",
    source=_HYNDMAN_FAN,
    location="p. 361 — sample mean, preceding the quantile definitions.",
    notes="Used for mean latency only; carries no modelling assumption.",
)
def mean(values: Sequence[float]) -> float:
    """Arithmetic mean of ``values``.

    Args:
        values: Observed measurements.

    Returns:
        The mean.

    Raises:
        ValueError: If ``values`` is empty (the mean is undefined).
    """
    if not values:
        raise ValueError("Mean is undefined for an empty sample.")
    return sum(values) / len(values)


@derivation(
    statement=(
        "h = (n - 1)p + 1; Q(p) = x_(floor(h)) + (h - floor(h)) * "
        "(x_(floor(h)+1) - x_(floor(h)))"
    ),
    algorithm="Sample quantile, Hyndman & Fan Definition 7",
    source=_HYNDMAN_FAN,
    location="Definition 7, p. 363.",
    notes=(
        "Quantile definitions genuinely differ between packages; Definition 7 "
        "is the default in R and NumPy and is pinned here for comparability."
    ),
)
def quantile(values: Sequence[float], p: float) -> float:
    """Sample quantile using Hyndman & Fan Definition 7.

    Args:
        values: Observed measurements.
        p: Probability level in [0, 1].

    Returns:
        The sample quantile.

    Raises:
        ValueError: If ``values`` is empty or ``p`` lies outside [0, 1].
    """
    if not values:
        raise ValueError("Quantile is undefined for an empty sample.")
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"Probability level must lie in [0, 1]; got {p}.")
    ordered = sorted(values)
    n = len(ordered)
    if n == 1:
        return ordered[0]
    h = (n - 1) * p + 1
    lower = int(h)
    fraction = h - lower
    if lower >= n:
        return ordered[-1]
    return ordered[lower - 1] + fraction * (ordered[lower] - ordered[lower - 1])


@dataclass
class LatencyRecorder:
    """Collects per-step REM evaluation latencies.

    Attributes:
        samples_ms: Recorded durations in milliseconds.
    """

    samples_ms: List[float] = field(default_factory=list)

    @contextmanager
    def measure(self) -> Iterator[None]:
        """Time the enclosed block and record it.

        Uses :func:`time.perf_counter`, the monotonic high-resolution clock, so
        measurements are unaffected by wall-clock adjustments.
        """
        started = time.perf_counter()
        try:
            yield
        finally:
            self.samples_ms.append((time.perf_counter() - started) * 1000.0)

    def report(self) -> Dict[str, float]:
        """Return the latency summary."""
        return latency_report(self.samples_ms)

    def __len__(self) -> int:
        return len(self.samples_ms)


def latency_report(samples_ms: Sequence[float]) -> Dict[str, float]:
    """Summarise latency measurements.

    Args:
        samples_ms: Durations in milliseconds.

    Returns:
        Mapping with ``n``, ``mean_ms``, ``p50_ms``, ``p95_ms``, ``p99_ms``,
        ``min_ms`` and ``max_ms``.

    Raises:
        ValueError: If ``samples_ms`` is empty.
    """
    if not samples_ms:
        raise ValueError("Cannot summarise an empty latency sample.")
    return {
        "n": float(len(samples_ms)),
        "mean_ms": mean(samples_ms),
        "p50_ms": quantile(samples_ms, 0.50),
        "p95_ms": quantile(samples_ms, 0.95),
        "p99_ms": quantile(samples_ms, 0.99),
        "min_ms": min(samples_ms),
        "max_ms": max(samples_ms),
    }


def throughput(n_steps: int, elapsed_seconds: float) -> float:
    """Steps evaluated per second.

    A rate, i.e. a unit conversion of measured counts, not a statistical
    estimator.

    Args:
        n_steps: Number of steps evaluated.
        elapsed_seconds: Wall-clock duration of the run.

    Returns:
        Steps per second.

    Raises:
        ValueError: If ``elapsed_seconds`` is not positive.
    """
    if elapsed_seconds <= 0:
        raise ValueError("Elapsed time must be positive to compute throughput.")
    return n_steps / elapsed_seconds
