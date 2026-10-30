"""A1 = baseline B1 (Chapter 3 Eq. 3.14)."""

import numpy as np
import pytest

from rem.algorithms.a1 import A1Policy, A1Thresholds, operating_threshold
from rem.algorithms.decision.policy import PredicatePolicy
from rem.core.results import Verdict


def test_threshold_is_minimum_meeting_fpr_target():
    benign = np.linspace(0.0, 0.99, 100)
    for alpha in (0.0, 0.01, 0.05, 0.5):
        th = operating_threshold(benign, alpha)
        assert np.mean(benign >= th) <= alpha
        smaller = benign[benign < th]
        if smaller.size:
            assert np.mean(benign >= smaller.max()) > alpha


def test_alpha_zero_flags_no_benign_step():
    benign = [0.1, 0.2, 0.9]
    assert np.mean(np.asarray(benign) >= operating_threshold(benign, 0.0)) == 0.0


def test_threshold_invariant_under_monotone_recalibration():
    rng = np.random.default_rng(0)
    p = rng.uniform(size=200)
    f = lambda q: q ** 3  # strictly increasing
    th = operating_threshold(p, 0.05)
    th_f = operating_threshold(f(p), 0.05)
    assert np.array_equal(p >= th, f(p) >= th_f)


def test_requires_alpha_mod_above_alpha_blk():
    with pytest.raises(ValueError):
        A1Thresholds.fit([0.1, 0.2], 0.05, 0.01)
    with pytest.raises(ValueError):
        operating_threshold([], 0.1)


def test_verdict_rule():
    t = A1Thresholds(theta_blk=0.8, theta_mod=0.5, alpha_blk=0.01, alpha_mod=0.05)
    pol = A1Policy(t, PredicatePolicy(frozenset(), 3, ("x_act1",), frozenset({"send_money"})))
    av = {"x_act1": True}
    assert pol.decide(0.9, 1, "send_money", av).verdict is Verdict.BLOCK
    assert pol.decide(0.6, 1, "send_money", av).verdict is Verdict.MODIFY
    assert pol.decide(0.6, 1, "get_balance", av).verdict is Verdict.BLOCK      # Modify infeasible
    assert pol.decide(0.1, 4, "send_money", av).verdict is Verdict.ALLOW       # tier ignored
    assert pol.decide(0.1, 4, "send_money", {"x_act1": False}).verdict is Verdict.ESCALATE  # via D2 only
