"""Nested grouped cross-fitting (Chapter 3 Procedure 3.1, Sec. 3.11.5).

For each outer fold f:
  3  benign reference (transition set, x-bar) from benign data of D_train;
  4  lambda selected by grouped inner CV on D_train (held-out log-loss);
  5  out-of-fold logits on D_train from the inner fits with the selected
     lambda; (gamma_1, gamma_0) fitted on them;
  6  gamma_1 <= 0 is recorded as a calibration failure for fold f;
  7  (beta_0, beta) refitted on all of D_train;
  8  theta(alpha_blk), theta(alpha_mod) from out-of-fold calibrated benign
     (y = 0) steps of D_train (Eq. 3.14);
  9  D_test scored; predictions stored for evaluation only.

Inner-fold benign references are re-estimated without the inner held-out
groups, so out-of-fold logits are not optimistically biased on x^beh_4.

Lambda convention (mismatch M1, PROJECT_AUDIT.md): the frozen estimator
minimises NLL + (lambda/2)||beta||^2; Chapter 3 Eq. 3.2 writes lambda||beta||^2.
The grid is applied to the implementation's lambda and reported as such.

The caller supplies ``design(train_mask) -> X`` so that every feature that
depends on fitted reference quantities is recomputed from the fitting rows only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Hashable, List, Optional, Sequence

import numpy as np

from rem.algorithms.a1 import A1Thresholds
from rem.algorithms.calibration.platt import MonotonicityViolationError
from rem.algorithms.detection.ridge_logistic import RidgeLogisticRegression, sigmoid
from rem.evaluation.probabilistic import log_loss

__all__ = ["assign_round_robin", "FoldFit", "CrossFitResult", "nested_crossfit"]


def assign_round_robin(keys: Sequence[Hashable], n_folds: int) -> Dict[Hashable, int]:
    """Sorted distinct keys -> fold index i mod n_folds."""
    distinct = sorted(set(keys), key=str)
    return {k: i % n_folds for i, k in enumerate(distinct)}


@dataclass
class FoldFit:
    fold: Hashable
    lam: float
    inner_logloss: Dict[float, float]
    intercept: float
    coefficients: List[float]
    gamma_0: Optional[float]
    gamma_1: Optional[float]
    calibration_failed: bool
    theta_blk: Optional[float]
    theta_mod: Optional[float]
    n_train: int
    n_test: int
    n_train_pos: int
    n_test_pos: int
    xbar: List[float] = field(default_factory=list)
    benign_oof_p: List[float] = field(default_factory=list)   # for Eq. 3.14 at other alphas


@dataclass
class CrossFitResult:
    logit: np.ndarray            # held-out s_t
    p_raw: np.ndarray            # held-out sigma(s_t)
    p_cal: np.ndarray            # held-out calibrated p_t (NaN where calibration failed)
    fold_of: np.ndarray          # outer fold index per row (object array)
    fits: Dict[Hashable, FoldFit]


def _fit(X: np.ndarray, y: np.ndarray, lam: float, order: Sequence[str]) -> RidgeLogisticRegression:
    return RidgeLogisticRegression(order, penalty=lam).fit(X, y)


def _logit(model: RidgeLogisticRegression, X: np.ndarray) -> np.ndarray:
    return model.intercept + X @ np.asarray(model.coefficients, dtype=float)


def nested_crossfit(
    *,
    design: Callable[[np.ndarray], np.ndarray],
    y: Sequence[int],
    outer_fold: Sequence[Hashable],
    inner_group: Sequence[Hashable],
    inner_is_benign_group: Sequence[bool],
    feature_order: Sequence[str],
    lambda_grid: Sequence[float],
    inner_folds: int,
    calibrator_factory: Callable[[], object],
    alpha_blk: Optional[float],
    alpha_mod: Optional[float],
    clip: float,
) -> CrossFitResult:
    """Run Procedure 3.1 lines 1-9.

    Args:
        design: Maps a boolean fitting mask over all rows to the full design
            matrix X (all rows), computed with reference quantities estimated
            on the masked rows only.
        y: Labels.
        outer_fold: Outer fold id per row.
        inner_group: Inner grouping key per row (injection task for attacked
            rows, user task for benign-episode rows).
        inner_is_benign_group: Whether a row's inner group is a benign-episode
            group; attacked and benign groups are assigned to inner folds
            separately, round robin.
        calibrator_factory: Returns an unfitted logit calibrator
            (``fit(logits, labels)``, ``gamma_0``, ``gamma_1``).
        alpha_blk, alpha_mod: B1 targets; ``None`` skips threshold selection.
        clip: Probability clip for the inner log-loss.
    """
    y = np.asarray(y, dtype=int)
    outer = np.asarray(outer_fold, dtype=object)
    inner_g = np.asarray(inner_group, dtype=object)
    benign_g = np.asarray(inner_is_benign_group, dtype=bool)
    n = y.size
    logit = np.full(n, np.nan)
    p_cal = np.full(n, np.nan)
    fits: Dict[Hashable, FoldFit] = {}

    for f in sorted(set(outer.tolist()), key=str):
        test = outer == f
        train = ~test
        X_out = design(train)

        # Inner fold assignment within D_train.
        tr_idx = np.flatnonzero(train)
        att_map = assign_round_robin([inner_g[i] for i in tr_idx if not benign_g[i]], inner_folds)
        ben_map = assign_round_robin([inner_g[i] for i in tr_idx if benign_g[i]], inner_folds)
        inner = np.full(n, -1)
        for i in tr_idx:
            inner[i] = (ben_map if benign_g[i] else att_map)[inner_g[i]]

        inner_X = {}
        for j in range(inner_folds):
            fit_mask = train & (inner != j)
            inner_X[j] = design(fit_mask)

        oof = {lam: np.full(n, np.nan) for lam in lambda_grid}
        scores: Dict[float, float] = {}
        for lam in lambda_grid:
            for j in range(inner_folds):
                fit_mask = train & (inner != j)
                hold = train & (inner == j)
                if not hold.any():
                    continue
                Xj = inner_X[j]
                model = _fit(Xj[fit_mask], y[fit_mask], lam, feature_order)
                oof[lam][hold] = _logit(model, Xj[hold])
            scores[lam] = log_loss(y[train], sigmoid(oof[lam][train]), clip)
        lam_star = min(lambda_grid, key=lambda l: (scores[l], -l))  # ties -> stronger penalty

        cal = calibrator_factory()
        failed = False
        try:
            cal.fit(oof[lam_star][train], y[train])
            g0, g1 = float(cal.gamma_0), float(cal.gamma_1)
        except MonotonicityViolationError:
            failed, g0, g1 = True, None, None

        model = _fit(X_out[train], y[train], lam_star, feature_order)
        logit[test] = _logit(model, X_out[test])

        theta_blk = theta_mod = None
        benign_oof = np.array([])
        if not failed:
            p_cal[test] = sigmoid(g1 * logit[test] + g0)
            benign_oof = sigmoid(g1 * oof[lam_star][train & (y == 0)] + g0)
            if alpha_blk is not None and alpha_mod is not None:
                th = A1Thresholds.fit(benign_oof, alpha_blk, alpha_mod)
                theta_blk, theta_mod = th.theta_blk, th.theta_mod

        fits[f] = FoldFit(
            fold=f,
            lam=float(lam_star),
            inner_logloss={float(k): float(v) for k, v in scores.items()},
            intercept=float(model.intercept),
            coefficients=[float(c) for c in model.coefficients],
            gamma_0=g0,
            gamma_1=g1,
            calibration_failed=failed,
            theta_blk=theta_blk,
            theta_mod=theta_mod,
            n_train=int(train.sum()),
            n_test=int(test.sum()),
            n_train_pos=int(y[train].sum()),
            n_test_pos=int(y[test].sum()),
            xbar=[float(v) for v in X_out[train & (y == 0)].mean(axis=0)],
            benign_oof_p=[float(v) for v in benign_oof],
        )

    return CrossFitResult(logit=logit, p_raw=sigmoid(logit), p_cal=p_cal, fold_of=outer, fits=fits)
