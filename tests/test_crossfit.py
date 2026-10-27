"""Nested grouped cross-fitting (Procedure 3.1) on synthetic smoke data.

Synthetic data are used ONLY to test the procedure's mechanics; they are not
benchmark results.
"""

import numpy as np

from rem.algorithms.calibration.logit_nll import LabelNLLLogitCalibrator
from rem.algorithms.calibration.platt import PlattLogitCalibrator
from rem.evaluation.crossfit import assign_round_robin, nested_crossfit

ORDER = ("a", "b")


def _data(seed=0):
    rng = np.random.default_rng(seed)
    n = 900
    group = rng.integers(0, 9, n)
    y = (rng.uniform(size=n) < 0.2).astype(int)
    X = np.column_stack([y + rng.normal(0, 0.8, n), rng.normal(0, 1, n)])
    return X, y, group


def test_round_robin():
    assert assign_round_robin(["c", "a", "b", "d"], 2) == {"a": 0, "b": 1, "c": 0, "d": 1}


def test_crossfit_no_leakage_and_outputs():
    X, y, g = _data()
    seen_masks = []

    def design(mask):
        seen_masks.append(mask.copy())
        return X

    for factory in (LabelNLLLogitCalibrator, PlattLogitCalibrator):
        seen_masks.clear()
        res = nested_crossfit(
            design=design, y=y, outer_fold=g, inner_group=g, inner_is_benign_group=np.zeros_like(g, bool),
            feature_order=ORDER, lambda_grid=[0.1, 10.0], inner_folds=4, calibrator_factory=factory,
            alpha_blk=0.01, alpha_mod=0.05, clip=1e-6,
        )
        assert np.all(np.isfinite(res.logit)) and np.all(np.isfinite(res.p_cal))
        assert set(res.fits) == set(range(9))
        for f, fit in res.fits.items():
            assert fit.gamma_1 > 0 and fit.theta_mod <= fit.theta_blk
            assert fit.n_test == int((g == f).sum())
        # every design call excludes at least one outer fold entirely
        for m in seen_masks:
            assert any(not m[g == f].any() for f in range(9))
        # held-out predictions come from models that never saw the fold:
        # perturbing fold-0 labels must not change fold-0 predictions.
    y2 = y.copy()
    y2[g == 0] = 1 - y2[g == 0]
    a = nested_crossfit(design=lambda m: X, y=y, outer_fold=g, inner_group=g,
                        inner_is_benign_group=np.zeros_like(g, bool), feature_order=ORDER, lambda_grid=[1.0],
                        inner_folds=4, calibrator_factory=LabelNLLLogitCalibrator, alpha_blk=None, alpha_mod=None, clip=1e-6)
    b = nested_crossfit(design=lambda m: X, y=y2, outer_fold=g, inner_group=g,
                        inner_is_benign_group=np.zeros_like(g, bool), feature_order=ORDER, lambda_grid=[1.0],
                        inner_folds=4, calibrator_factory=LabelNLLLogitCalibrator, alpha_blk=None, alpha_mod=None, clip=1e-6)
    assert np.allclose(a.logit[g == 0], b.logit[g == 0]) and np.allclose(a.p_cal[g == 0], b.p_cal[g == 0])
