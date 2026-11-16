"""Threshold-selection procedures of the competitive study (16 November 2026). Pure functions; no data access.

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. Nothing here is a new formula.
Each function re-implements a published procedure from its authors' own public implementation, which was
read as data (not executed). The full texts of the papers could not be opened in the session that wrote
this file (publisher hosts outside the network settings); page and equation anchors are therefore not
given here and are listed as open in MATHEMATICAL_SOURCE_REGISTRY.csv.

NP umbrella threshold
    Paper: Tong, Feng and Li (2018), Science Advances 4(2), eaao1659, doi:10.1126/sciadv.aao1659.
    Implementation read: CRAN package nproc 2.1.5 (authors Feng, Li, Tong; GPL-2), file R/npfuns.R,
    function npc.core, branch band = FALSE:
        score.sort <- sort(score0)
        s <- 1 - pbinom(0:(n-1), size = n, prob = 1 - alpha)
        loc <- min(which(s <= delta))
        cutoff <- score.sort[loc]
    and pred.npc.core: pred.label = outer(pred.score, object$cutoff, ">").
    The package describes alpha as "the desirable upper bound on type I error" and delta as "the
    violation rate of the type I error" (man/npc.Rd), with class 0 the class whose misclassification is
    the type I error. Defaults alpha = 0.05, delta = 0.05.

Conformal risk control threshold
    Paper: Angelopoulos, Bates, Fisch, Lei and Schuster, "Conformal Risk Control", arXiv:2208.02814.
    Implementation read: github.com/aangelopoulos/conformal-risk (MIT licence), commit 3eff946,
    file core/get_lhat.py:
        n = calib_loss_table.shape[0]
        rhat = calib_loss_table.mean(axis=0)
        lhat_idx = max(np.argmax(((n/(n+1)) * rhat + B/(n+1)) >= alpha) - 1, 0)
    with the loss table "ordered from small loss to large loss".

Mapping to REM (an adaptation, stated in the protocol): the score is REM's risk logit s (larger = more
likely adversarially induced). A call is RELEASED if and only if s < cutoff. The error that both procedures
bound is the release of an attack-labelled call. Neither formal guarantee is claimed for REM's data: the
calibration units are neither independent nor exchangeable with the evaluation units.
"""
from __future__ import annotations

import math
from typing import Optional, Sequence

import numpy as np
from scipy.stats import binom

NEG_INF = float("-inf")
POS_INF = float("inf")


def np_min_sample_size(alpha: float, delta: float) -> int:
    """Smallest n for which an order statistic qualifies: (1 - alpha)^n <= delta."""
    return int(math.ceil(math.log(delta) / math.log(1.0 - alpha) - 1e-12))


def np_order_index(n: int, alpha: float, delta: float) -> Optional[int]:
    """nproc: s[k] = 1 - pbinom(k - 1, n, 1 - alpha) for k = 1..n; loc = min(which(s <= delta)).

    Returns the 1-based rank k*, or None if no rank qualifies (sample too small)."""
    if n <= 0:
        return None
    k = np.arange(1, n + 1)
    s = binom.sf(k - 1, n, 1.0 - alpha)                  # P(Bin(n, 1 - alpha) >= k)
    ok = np.flatnonzero(s <= delta)
    return int(k[ok[0]]) if ok.size else None


def np_release_cutoff(attack_logits: Sequence[float], alpha: float, delta: float) -> dict:
    """Release cutoff on the risk logit from the left-out attack-labelled sample.

    nproc orients the score so that the class whose error is controlled (its class 0; here: attack-labelled
    calls) has the smaller scores, and predicts the other class if score > cutoff. With np_score = -logit,
    'predict legitimate' (release) is -logit > cutoff_np, i.e. logit < -cutoff_np."""
    x = np.sort(-np.asarray(list(attack_logits), dtype=float))       # ascending NP scores of the controlled class
    n = int(x.size)
    k = np_order_index(n, alpha, delta)
    if k is None:
        return {"cutoff": NEG_INF, "n": n, "k": None, "feasible": False, "min_n": np_min_sample_size(alpha, delta)}
    cut = float(-x[k - 1])
    return {"cutoff": cut, "n": n, "k": k, "feasible": True, "min_n": np_min_sample_size(alpha, delta),
            "left_out_released_fraction": float(np.mean(x > x[k - 1]))}


def get_lhat_reference(calib_loss_table: np.ndarray, lambdas: np.ndarray, alpha: float, B: float = 1.0):
    """Verbatim port of core/get_lhat.py of the official repository (MIT licence, Copyright (c) 2022
    Anastasios Angelopoulos). Used in the tests as the reference for crc_release_cutoff."""
    n = calib_loss_table.shape[0]
    rhat = calib_loss_table.mean(axis=0)
    lhat_idx = max(np.argmax(((n / (n + 1)) * rhat + B / (n + 1)) >= alpha) - 1, 0)   # Can't be -1.
    return lambdas[lhat_idx]


def crc_release_cutoff(unit_min_attack_logit: Sequence[float], n_units: int, alpha: float, B: float = 1.0) -> dict:
    """Release cutoff on the risk logit by conformal risk control.

    Calibration unit: one episode. Loss of a unit at cutoff c: 1 if the unit contains an attack-labelled
    call with logit < c (it would be released), else 0; bounded by B = 1 and non-decreasing in c.
    ``unit_min_attack_logit`` holds, for each calibration unit that contains an attack-labelled call, the
    smallest logit of such a call; the remaining n_units - len(...) units have loss 0 at every cutoff.

    The grid of cutoffs is (-inf, the sorted distinct minima, +inf), ordered from small loss to large loss,
    and the selected index is the one get_lhat selects: the last grid point before the first one at which
    (n/(n+1)) * mean loss + B/(n+1) >= alpha. One edge case differs from the official code and is stated in
    the protocol: if no grid point reaches alpha, the most permissive grid point is returned (the official
    code returns index 0 there, through np.argmax of an all-False array)."""
    m = np.sort(np.asarray(list(unit_min_attack_logit), dtype=float))
    n = int(n_units)
    if n <= 0:
        return {"cutoff": NEG_INF, "n_units": n, "feasible": False}
    grid = np.concatenate(([NEG_INF], np.unique(m), [POS_INF]))
    released = np.array([float(np.sum(m < c)) for c in grid])           # units with loss 1 at cutoff c
    bound = (n / (n + 1.0)) * (released / n) + B / (n + 1.0)
    viol = bound >= alpha
    if not viol.any():
        idx = len(grid) - 1
    else:
        idx = max(int(np.argmax(viol)) - 1, 0)
    feasible = bool(bound[0] < alpha)
    cut = float(grid[idx]) if feasible else NEG_INF
    return {"cutoff": cut, "n_units": n, "units_with_attack_call": int(m.size), "feasible": feasible,
            "calibration_units_released": int(np.sum(m < cut)), "bound_at_cutoff": float(bound[idx]) if feasible else None,
            "min_units": int(math.floor(B / alpha - 1.0) + 1)}
