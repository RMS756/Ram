"""Competitive study of 16 November 2026: threshold procedures, the common authority front, label isolation.

These tests use no stored state and no recorded episode. They do not score any arm of the study."""
import ast
import inspect
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from scipy.stats import binom

ROOT = Path(__file__).resolve().parents[1]
for p in ("experiments/competitive_study", "experiments/g3_integration", "experiments/pilot", "experiments/improve_study"):
    sys.path.insert(0, str(ROOT / p))
import candidates as C  # noqa: E402
import guards as G  # noqa: E402
import common  # noqa: E402
from rem.algorithms.behavior.evidence import BenignReference  # noqa: E402

A = "ZK52390800003316720548"
B = "QB71046600002985413307"
F4 = ("x_ctx2", "x_act1", "x_act2", "x_act3", "q3_sup", "q3_den", "q3_op", "q3_rec", "q3_amt")


# ---------------------------------------------------------------------------------- NP umbrella threshold
def test_np_minimum_sample_size_matches_the_documented_requirement():
    assert C.np_min_sample_size(0.05, 0.05) == 59            # (1 - 0.05)^59 <= 0.05 < (1 - 0.05)^58
    assert 0.95 ** 59 <= 0.05 < 0.95 ** 58
    assert C.np_order_index(58, 0.05, 0.05) is None and C.np_order_index(59, 0.05, 0.05) == 59
    assert C.np_min_sample_size(0.01, 0.05) == 299


@pytest.mark.parametrize("n,alpha,delta", [(59, 0.05, 0.05), (100, 0.05, 0.05), (400, 0.05, 0.05), (400, 0.01, 0.05), (1000, 0.1, 0.01)])
def test_np_order_index_is_the_nproc_rule(n, alpha, delta):
    # nproc: s <- 1 - pbinom(0:(n-1), n, 1 - alpha); loc <- min(which(s <= delta))
    s = [1.0 - binom.cdf(k - 1, n, 1 - alpha) for k in range(1, n + 1)]
    loc = next((k for k, v in enumerate(s, 1) if v <= delta), None)
    assert C.np_order_index(n, alpha, delta) == loc
    if loc is not None and loc > 1:
        assert s[loc - 2] > delta                               # the smallest qualifying rank


def test_np_cutoff_orientation_and_strict_inequality():
    logits = np.arange(100, dtype=float)                        # attack-labelled left-out sample; larger = riskier
    r = C.np_release_cutoff(logits, 0.05, 0.05)
    k = C.np_order_index(100, 0.05, 0.05)
    assert r["feasible"] and r["k"] == k
    assert r["cutoff"] == float(100 - k)                        # k-th smallest of (-logit) is the k-th largest logit
    released = np.sum(logits < r["cutoff"])                     # release iff logit < cutoff
    assert released == 100 - k and released / 100 <= 0.05
    assert r["left_out_released_fraction"] == released / 100


def test_np_too_small_sample_fails_closed():
    r = C.np_release_cutoff(np.zeros(20), 0.05, 0.05)
    assert not r["feasible"] and r["cutoff"] == float("-inf") and not (0.0 < r["cutoff"])


def test_np_violation_rate_on_independent_data_is_within_delta():
    # Validation of the implementation on data that satisfy the assumptions of the procedure (independent,
    # identically distributed, continuous scores). REM's data do not satisfy them; no guarantee is claimed for REM.
    rng = np.random.default_rng(20261116)
    alpha, delta, n, reps = 0.05, 0.05, 200, 4000
    viol = 0
    for _ in range(reps):
        cut = C.np_release_cutoff(rng.normal(size=n), alpha, delta)["cutoff"]
        type1 = float(__import__("scipy.stats").stats.norm.cdf(cut))          # P(logit < cutoff) for a new attack call
        viol += type1 > alpha
    assert viol / reps <= delta + 3 * (delta * (1 - delta) / reps) ** 0.5


# ---------------------------------------------------------------------------------- conformal risk control
def _table(mins, n_units):
    m = np.sort(np.asarray(mins, dtype=float))
    grid = np.concatenate(([-np.inf], np.unique(m), [np.inf]))
    table = np.zeros((n_units, grid.size))
    for i, v in enumerate(m):
        table[i] = (v < grid).astype(float)                      # loss 1 if the unit's attack call would be released
    return table, grid


@pytest.mark.parametrize("seed", range(8))
def test_crc_cutoff_equals_the_official_get_lhat(seed):
    rng = np.random.default_rng(seed)
    n_units = int(rng.integers(40, 400))
    mins = rng.normal(size=int(rng.integers(5, n_units)))
    for alpha in (0.05, 0.01, 0.2):
        table, grid = _table(mins, n_units)
        ref = C.get_lhat_reference(table, grid, alpha)
        got = C.crc_release_cutoff(mins, n_units, alpha)
        bound0 = 1.0 / (n_units + 1)
        if bound0 >= alpha:
            assert not got["feasible"] and got["cutoff"] == float("-inf")
        elif ((n_units / (n_units + 1)) * table.mean(axis=0) + 1 / (n_units + 1) >= alpha).any():
            assert got["cutoff"] == ref
            assert (n_units / (n_units + 1)) * np.mean(np.sum(mins < got["cutoff"]) / n_units) + bound0 < alpha
        else:
            assert got["cutoff"] == float("inf")                 # stated edge case: no grid point reaches alpha


def test_crc_needs_enough_units_and_is_monotone_in_alpha():
    assert C.crc_release_cutoff([0.0, 1.0], 8, 0.05)["feasible"] is False      # 1/(8+1) >= 0.05: nine independent groups cannot certify 5%
    assert C.crc_release_cutoff([0.0, 1.0], 8, 0.05)["min_units"] == 20
    mins = np.linspace(-3, 3, 200)
    assert C.crc_release_cutoff(mins, 1000, 0.01)["cutoff"] <= C.crc_release_cutoff(mins, 1000, 0.05)["cutoff"]


# ---------------------------------------------------------------------------------- common authority front
class _Stub:
    """A model that would release everything: score far below any cutoff."""
    def decision_function(self, X):
        return np.full((len(X), 1), -50.0)


def _cell_and_extra():
    rec = {"order": F4, "b0": -50.0, "coef": [0.0] * len(F4), "g0": 0.0, "g1": 1.0, "failed": False}
    cell = {"reference": BenignReference(frozenset()), "models": {("F4", "y"): rec}, "rmod": {3: 0.0, 4: 0.0}}
    cut = {"0.05": {"cutoff": float("inf")}, "0.01": {"cutoff": float("inf")}}
    extra = {"np": {"rec": rec, "cut": cut}, "crc": {"rec": rec, "cut": cut}, "gb": {"clf": _Stub(), "order": F4, "g0": 0.0, "g1": 1.0, "failed": False}}
    return cell, extra


def make(arm, objective):
    st = common.make_setup()
    cell, extra = _cell_and_extra()
    ep = SimpleNamespace(objective=objective, system_prompt="", injection_task_id=None, episode_id="regression")
    return G.make_guard(arm, cell, extra, ep, st)


def call(recipient=A, amount=50):
    return {"recipient": recipient, "amount": amount, "subject": "payment", "date": "2026-11-16"}


@pytest.mark.parametrize("arm", G.ARMS)
def test_every_arm_releases_a_fully_supported_call_when_its_rule_is_permissive(arm):
    g = make(arm, f"Send 50 to {A}.")
    assert g.evaluate("send_money", call())[0]


@pytest.mark.parametrize("arm", G.ARMS)
@pytest.mark.parametrize("objective,args", [
    (f"Send 50 to {A}.", call(B, 50)),                                              # account not supported by the request
    (f"Send 50 to {A} and 100 to {B}.", call(A, 100)),                              # contradicted binding
    (f"Create a monthly standing order for 50 to {A}.", call(A, 50)),               # another effect
    (f"If something looks suspicious, send 50 to {A}.", call(A, 50)),               # unevaluable condition
    (f"Check my balance.", call(A, 50)),                                            # operation not requested
])
def test_no_score_can_override_the_authority_front(arm, objective, args):
    g = make(arm, objective)
    assert not g.evaluate("send_money", args)[0]
    assert g.audit[-1]["verdict_source"] == "permission_guard_authority_v3"


@pytest.mark.parametrize("arm", G.ARMS)
def test_false_condition_is_refused_by_every_arm(arm):
    g = make(arm, f"If my balance is above 1000 and below 5000, send 50 to {A}.")
    g.evaluate("get_balance", {})
    g.ingest("get_balance", "10000", executed=True)
    assert not g.evaluate("send_money", call())[0]


@pytest.mark.parametrize("arm", G.ARMS)
def test_only_successful_execution_consumes_the_payment(arm):
    g = make(arm, f"Send 50 to {A}.")
    assert g.evaluate("send_money", call())[0]
    g.ingest("send_money", "error", executed=False)
    assert g.evaluate("send_money", call())[0]                  # a failed call may be retried
    g.ingest("send_money", "sent", executed=True)
    assert not g.evaluate("send_money", call())[0]              # a repetition of an executed payment is refused


@pytest.mark.parametrize("arm", G.ARMS)
def test_direct_value_constraint_applies_to_every_arm(arm):
    g = make(arm, f"I only owe my half of the shared internet bill, so send 27.35 to {A} once and that's it.")
    assert not g.evaluate("send_money", call(A, 54.70))[0]
    g.ingest("send_money", "withheld", executed=False)
    assert g.evaluate("send_money", call(A, 27.35))[0]
    for amount in (1.25, 1250):
        g = make(arm, f"Send 1,250 to {A}.")
        assert not g.evaluate("send_money", call(A, amount))[0]


@pytest.mark.parametrize("arm", ["NP05", "NP01", "CRC05", "CRC01"])
def test_threshold_arm_withholds_when_the_score_is_not_below_the_cutoff(arm):
    st = common.make_setup()
    cell, extra = _cell_and_extra()
    kind, alpha = G.THRESHOLD_ARMS[arm]
    extra[kind]["cut"][alpha] = {"cutoff": float("-inf")}        # an infeasible calibration fails closed
    ep = SimpleNamespace(objective=f"Send money to {A}.", system_prompt="", injection_task_id=None, episode_id="regression")
    g = G.make_guard(arm, cell, extra, ep, st)
    assert not g.evaluate("send_money", call())[0]
    assert g.audit[-1]["verdict_source"] == f"cs_{kind}_threshold"
    assert g.evaluate("get_balance", {})[0]                      # read-type calls are not subject to the cutoff


def test_guard_only_arm_releases_authorized_value_uncertainty_and_nothing_else():
    g = make("GV", f"Send money to {A}.")                        # account authorized, amount not stated
    assert g.evaluate("send_money", call(A, 77))[0] and g.audit[-1]["verdict_source"] == "cs_guard_only"
    assert not make("GV", f"Send money to {A}.").evaluate("send_money", call(B, 77))[0]


# ---------------------------------------------------------------------------------- isolation
@pytest.mark.parametrize("module", [G, C])
def test_runtime_modules_do_not_read_evaluation_metadata(module):
    names = {n.attr for n in ast.walk(ast.parse(inspect.getsource(module))) if isinstance(n, ast.Attribute)}
    assert not names.intersection({"label", "utility", "security", "attacked", "injections", "user_task_id", "injection_task_id",
                                   "recorded_utility", "recorded_security"})


def test_frozen_and_scored_modules_are_unchanged():
    import hashlib
    import json
    frozen = json.loads((ROOT / "REM_COMPETITIVE_STUDY_2026_11_16" / "FROZEN_INPUT_HASHES.json").read_text())
    for rel, h in frozen.items():
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == h, rel
