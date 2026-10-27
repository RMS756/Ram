"""Discrimination, calibration and bootstrap utilities."""

import numpy as np
import pytest

from rem.evaluation.bootstrap import grouped_bootstrap, stratified_grouped_bootstrap
from rem.evaluation.probabilistic import (
    average_precision,
    brier_binary,
    brier_two_class,
    expected_calibration_error,
    log_loss,
    reliability_table,
    roc_auc,
)


def test_roc_auc_matches_pairwise_definition():
    rng = np.random.default_rng(1)
    y = rng.integers(0, 2, 300)
    p = np.round(rng.uniform(size=300), 1)  # many ties
    pos, neg = p[y == 1], p[y == 0]
    pairwise = np.mean([(a > b) + 0.5 * (a == b) for a in pos for b in neg])
    assert roc_auc(y, p) == pytest.approx(pairwise)
    assert np.isnan(roc_auc([1, 1], [0.1, 0.2]))


def test_average_precision_perfect_and_known():
    assert average_precision([0, 1, 1], [0.1, 0.8, 0.9]) == pytest.approx(1.0)
    # ranking 1,0,1 -> AP = 0.5*1 + 0.5*(2/3)
    assert average_precision([1, 0, 1], [0.9, 0.8, 0.7]) == pytest.approx(0.5 + 1 / 3)


def test_ece_binning_eq_3_20():
    y = [0, 1, 1, 0]
    p = [0.0, 0.1, 0.95, 1.0]
    # bins (M=10): p=0 and 0.1 -> bin 1; 0.95 and 1.0 -> bin 10
    rows = reliability_table(y, p, 10)
    assert rows[0]["count"] == 2 and rows[9]["count"] == 2
    expected = 0.5 * abs(0.5 - 0.05) + 0.5 * abs(0.5 - 0.975)
    assert expected_calibration_error(y, p, 10) == pytest.approx(expected)


def test_log_loss_and_brier():
    assert log_loss([1, 0], [0.5, 0.5], 1e-6) == pytest.approx(np.log(2))
    assert np.isfinite(log_loss([1], [0.0], 1e-6))
    assert brier_two_class([1, 0], [0.8, 0.3]) == pytest.approx(2 * brier_binary([1, 0], [0.8, 0.3]))


def test_grouped_bootstrap_resamples_groups():
    items = [("a", 1.0)] * 5 + [("b", 0.0)] * 5
    pt, lo, hi = grouped_bootstrap(items, lambda r: r[0], lambda s: np.mean([v for _, v in s]), resamples=200, seed=0)
    assert pt == 0.5 and 0.0 <= lo <= pt <= hi <= 1.0
    strata = [(items[:5], lambda r: r[0]), (items[5:], lambda r: r[0])]
    pt2, lo2, hi2 = stratified_grouped_bootstrap(strata, lambda s: np.mean([v for _, v in s]), resamples=50, seed=0)
    assert pt2 == lo2 == hi2 == 0.5   # one group per stratum -> no variability
