"""A2 = observe-only Bernoulli CUSUM (Chapter 3 Eqs. 3.15-3.19)."""

import inspect
import math

import pytest

import rem.algorithms.a2 as a2
from rem.algorithms.behavior.cusum import OBSERVE_ONLY, BernoulliCusum, deviation_indicator


def test_increments_and_recursion():
    c = BernoulliCusum(0.1, 0.5)
    assert c.increment(1) == pytest.approx(math.log(5))
    assert c.increment(0) == pytest.approx(math.log(0.5 / 0.9))
    path = c.path([1, 0, 1, 1])
    g = 0.0
    for e, v in zip([1, 0, 1, 1], path):
        g = max(0.0, g + c.increment(e))
        assert v == pytest.approx(g)
    assert c.alarm_time(path, path[2]) == 3
    assert c.alarm_time(path, 1e9) is None


def test_requires_q0_below_q1():
    with pytest.raises(ValueError):
        BernoulliCusum(0.5, 0.3)


def test_indicator_set():
    assert deviation_indicator({"x_beh1": 1.0}) == 1
    assert deviation_indicator({"x_beh2": 1 / 3}) == 0
    assert deviation_indicator({"x_beh2": 1.0}) == 1
    assert deviation_indicator({"x_ctx2": 1.0, "x_act2": 1.0}) == 0


def test_fit_meets_false_alarm_target_and_delay():
    benign = [[0, 0, 1, 0], [0, 0, 0], [1, 0, 0, 0, 0], [0] * 6] * 5
    fit = a2.fit_a2(benign, q1=0.5, q0_floor=0.01, false_alarm_target=0.05)
    assert fit.benign_false_alarm <= 0.05
    assert fit.q0 == pytest.approx(max(fit.q0_raw, 0.01))
    res = a2.evaluate_episode(fit, [0, 0, 1, 1, 1, 1], change_point=3)
    assert res.alarm_time is not None and res.delay == res.alarm_time - 3 and not res.alarm_before_change


def test_a2_is_observe_only_and_issues_no_verdict():
    assert OBSERVE_ONLY is True
    src = inspect.getsource(a2)
    assert "Verdict" not in src.split('"""', 2)[2]   # no verdict use outside the docstring
    assert not any(n.lower().startswith("decide") for n in dir(a2))
