"""Discrimination and calibration metrics (Chapter 3 Sec. 3.12.2).

* ROC-AUC (Fawcett, 2006): probability that a random positive outranks a random
  negative, ties counted one half (Mann-Whitney form).
* PR-AUC (Davis & Goadrich, 2006 discuss the PR curve): computed here as
  average precision, AP = sum_n (R_n - R_{n-1}) P_n over descending thresholds.
  AP is a step-wise estimate of the area, NOT the interpolated area; the thesis
  must call the reported number "average precision (PR-AUC estimate)".
* ECE, Chapter 3 Eq. 3.20: binary form on the positive class (Naeini et al.,
  2015) with M equal-width bins (Guo et al., 2017); bin m holds
  (m-1)/M < p <= m/M and p = 0 goes to the first bin.
* Log-loss, Eq. 3.21, with probabilities clipped to [eps, 1 - eps].
* Brier score (SC-5, UNRESOLVED): ``brier_binary`` is the mean squared error of
  the positive-class probability; Brier's (1950) original definition sums the
  squared error over all r classes, which for r = 2 equals twice the binary
  value (``brier_two_class``). Both are returned; the convention must be stated
  wherever a number is reported.
"""

from __future__ import annotations

from typing import Dict, List, Sequence

import numpy as np

__all__ = [
    "roc_auc",
    "average_precision",
    "expected_calibration_error",
    "reliability_table",
    "log_loss",
    "brier_binary",
    "brier_two_class",
]


def _arrays(y: Sequence[int], p: Sequence[float]):
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    if y.shape != p.shape or y.size == 0:
        raise ValueError("y and p must be non-empty and of equal length.")
    return y, p


def roc_auc(y: Sequence[int], p: Sequence[float]) -> float:
    """ROC-AUC with ties counted 1/2. NaN if only one class is present."""
    y, p = _arrays(y, p)
    pos, neg = p[y == 1], p[y == 0]
    if pos.size == 0 or neg.size == 0:
        return float("nan")
    order = np.argsort(np.concatenate([pos, neg]), kind="mergesort")
    allv = np.concatenate([pos, neg])[order]
    ranks = np.empty_like(allv)
    i = 0
    while i < allv.size:  # average ranks over ties
        j = i
        while j + 1 < allv.size and allv[j + 1] == allv[i]:
            j += 1
        ranks[i : j + 1] = (i + j) / 2.0 + 1.0
        i = j + 1
    r = np.empty_like(ranks)
    r[order] = ranks
    r_pos = r[: pos.size].sum()
    return float((r_pos - pos.size * (pos.size + 1) / 2.0) / (pos.size * neg.size))


def average_precision(y: Sequence[int], p: Sequence[float]) -> float:
    """Average precision over distinct thresholds (ties grouped). NaN without positives."""
    y, p = _arrays(y, p)
    n_pos = y.sum()
    if n_pos == 0:
        return float("nan")
    order = np.argsort(-p, kind="mergesort")
    ys, ps = y[order], p[order]
    ap, tp, fp, prev_recall = 0.0, 0.0, 0.0, 0.0
    i = 0
    while i < ps.size:
        j = i
        while j + 1 < ps.size and ps[j + 1] == ps[i]:
            j += 1
        tp += ys[i : j + 1].sum()
        fp += (j + 1 - i) - ys[i : j + 1].sum()
        recall = tp / n_pos
        precision = tp / (tp + fp)
        ap += (recall - prev_recall) * precision
        prev_recall = recall
        i = j + 1
    return float(ap)


def _bin_index(p: np.ndarray, bins: int) -> np.ndarray:
    idx = np.ceil(p * bins).astype(int) - 1     # (m-1)/M < p <= m/M  ->  m-1
    return np.clip(idx, 0, bins - 1)            # p = 0 -> first bin


def reliability_table(y: Sequence[int], p: Sequence[float], bins: int) -> List[Dict[str, float]]:
    """Per-bin count, mean predicted probability and observed positive rate."""
    y, p = _arrays(y, p)
    idx = _bin_index(p, bins)
    rows = []
    for m in range(bins):
        mask = idx == m
        n = int(mask.sum())
        rows.append(
            {
                "bin": m + 1,
                "lower": m / bins,
                "upper": (m + 1) / bins,
                "count": n,
                "mean_p": float(p[mask].mean()) if n else float("nan"),
                "positive_rate": float(y[mask].mean()) if n else float("nan"),
            }
        )
    return rows


def expected_calibration_error(y: Sequence[int], p: Sequence[float], bins: int) -> float:
    """ECE of Chapter 3 Eq. 3.20."""
    y, p = _arrays(y, p)
    idx = _bin_index(p, bins)
    total = 0.0
    for m in range(bins):
        mask = idx == m
        if mask.any():
            total += mask.sum() / y.size * abs(y[mask].mean() - p[mask].mean())
    return float(total)


def log_loss(y: Sequence[int], p: Sequence[float], eps: float) -> float:
    """Mean negative log-likelihood, Chapter 3 Eq. 3.21."""
    y, p = _arrays(y, p)
    q = np.clip(p, eps, 1.0 - eps)
    return float(-np.mean(y * np.log(q) + (1.0 - y) * np.log(1.0 - q)))


def brier_binary(y: Sequence[int], p: Sequence[float]) -> float:
    """Mean squared error of the positive-class probability (see module note)."""
    y, p = _arrays(y, p)
    return float(np.mean((p - y) ** 2))


def brier_two_class(y: Sequence[int], p: Sequence[float]) -> float:
    """Brier's two-class sum, = 2 * brier_binary (see module note)."""
    return 2.0 * brier_binary(y, p)
