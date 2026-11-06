"""REM-Lite ablation: development-data thresholds on the uncalibrated scale give the same verdicts as the
calibrated operating-point baseline whenever the calibration map is strictly increasing (gamma_1 > 0).
Synthetic data only; the real-data check (6,762/6,762 identical verdicts) is in results/rem_lite/."""
import numpy as np

from rem.algorithms.a1 import A1Thresholds
from rem.algorithms.detection.ridge_logistic import sigmoid


def test_raw_and_calibrated_operating_thresholds_give_identical_verdicts():
    rng = np.random.default_rng(0)
    g0, g1 = -0.7, 0.93                                  # gamma_1 > 0: strictly increasing calibration
    dev_logits = rng.normal(-2.5, 1.2, 4000)             # development (benign, inner out-of-fold) logits
    test_logits = rng.normal(-1.5, 2.0, 6000)            # held-out logits
    cal = lambda s: sigmoid(g1 * s + g0)
    t_cal = A1Thresholds.fit(cal(dev_logits), 0.01, 0.05)
    # REM-Lite: invert the stored calibrated values, re-select on the raw scale
    pc = cal(dev_logits)
    t_raw = A1Thresholds.fit(sigmoid((np.log(pc / (1 - pc)) - g0) / g1), 0.01, 0.05)

    def verdict(p, t):
        return np.where(p >= t.theta_blk, 2, np.where(p >= t.theta_mod, 1, 0))
    assert np.array_equal(verdict(cal(test_logits), t_cal), verdict(sigmoid(test_logits), t_raw))


def test_thresholds_respect_declared_false_alarm_targets_on_development_data():
    rng = np.random.default_rng(1)
    p = sigmoid(rng.normal(-3, 1, 5000))
    t = A1Thresholds.fit(p, 0.01, 0.05)
    assert np.mean(p >= t.theta_blk) <= 0.01 and np.mean(p >= t.theta_mod) <= 0.05 and t.theta_blk >= t.theta_mod
