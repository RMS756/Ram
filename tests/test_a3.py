"""A3 (frozen REM decision layer + Chapter 3 predicates and feasible set)."""

import math

import pytest

from rem.algorithms.a3 import A3Policy
from rem.algorithms.decision.expected_loss import VerdictTieError
from rem.algorithms.decision.loss_matrix import (
    LossSpec,
    allow_block_threshold,
    build_loss_grid,
    escalation_feasible,
    indifference_threshold,
    reachable_verdicts,
)
from rem.algorithms.decision.policy import PredicatePolicy
from rem.core.results import Verdict

TIERS = (1, 2, 3, 4)


def spec(C_esc=0.3, r_mod=1.0, C_mod=0.5):
    return LossSpec(
        C_FA={k: 1.0 for k in TIERS},
        C_miss={1: 1.0, 2: 5.0, 3: 10.0, 4: 20.0},
        C_mod={k: C_mod for k in TIERS},
        C_esc=C_esc,
        r_mod={k: r_mod for k in TIERS},
    )


def preds(enabled=True, prohibited=(), restricted=("send_money",)):
    return PredicatePolicy(frozenset(prohibited), 3, ("x_act1",), frozenset(restricted), enabled)


AVAIL = {"x_act1": True}


def test_table_3_13_rows():
    g = build_loss_grid(spec(r_mod=0.25), "test")
    assert g.loss(Verdict.ALLOW, 0, 4) == 0 and g.loss(Verdict.ALLOW, 1, 4) == 20
    assert g.loss(Verdict.MODIFY, 0, 4) == 0.5 and g.loss(Verdict.MODIFY, 1, 4) == 5.0  # r_mod * C_miss
    assert g.loss(Verdict.ESCALATE, 0, 4) == g.loss(Verdict.ESCALATE, 1, 4) == 0.3
    assert g.loss(Verdict.BLOCK, 0, 4) == 1 and g.loss(Verdict.BLOCK, 1, 4) == 0


def test_thresholds_eq_3_8_and_3_9():
    s = spec()
    g = build_loss_grid(s, "test")
    assert allow_block_threshold(s, 4) == pytest.approx(1 / 21)
    assert indifference_threshold(g, Verdict.ALLOW, Verdict.BLOCK, 4) == pytest.approx(1 / 21)


def test_escalation_feasibility_eq_3_10():
    assert escalation_feasible(spec(C_esc=0.3), 4)       # 0.3 < 20/21
    assert not escalation_feasible(spec(C_esc=0.6), 1)   # 0.6 >= 1/2


def test_argmin_is_eq_3_7_over_feasible_set():
    pol = A3Policy(build_loss_grid(spec(), "t"), preds(), tie_mode="raise")
    # Read tool (Modify infeasible), tier 1: Allow for small p, Block for large p.
    assert pol.decide(0.01, 1, "get_balance", AVAIL).verdict is Verdict.ALLOW
    assert pol.decide(0.99, 1, "get_balance", AVAIL).verdict is Verdict.BLOCK
    d = pol.decide(0.2, 4, "send_money", AVAIL)
    assert d.source == "expected_loss"
    assert d.verdict.value == min(d.risks, key=d.risks.get)
    for v, r in d.risks.items():
        p = 0.2
        g = build_loss_grid(spec(), "t")
        assert r == pytest.approx((1 - p) * g.loss(Verdict(v), 0, 4) + p * g.loss(Verdict(v), 1, 4))


def test_modify_only_feasible_for_restricted_tools():
    pol = A3Policy(build_loss_grid(spec(r_mod=0.0, C_mod=0.01), "t"), preds())
    assert "modify" not in pol.decide(0.5, 2, "update_user_info", AVAIL).feasible
    assert pol.decide(0.5, 4, "send_money", AVAIL).verdict is Verdict.MODIFY


def test_predicates_d1_d2_fix_the_verdict():
    pol = A3Policy(build_loss_grid(spec(), "t"), preds(prohibited=("update_password",)))
    d1 = pol.decide(0.0, 4, "update_password", AVAIL)
    assert (d1.verdict, d1.source) == (Verdict.BLOCK, "D1")
    d2 = pol.decide(0.0, 3, "send_money", {"x_act1": False})
    assert (d2.verdict, d2.source) == (Verdict.ESCALATE, "D2")
    # Below k_D2 missing evidence does not escalate.
    assert pol.decide(0.0, 2, "send_money", {"x_act1": False}).source == "expected_loss"
    # Disabled predicates (ablation 6).
    off = A3Policy(build_loss_grid(spec(), "t"), preds(enabled=False, prohibited=("update_password",)))
    assert off.decide(0.0, 4, "update_password", AVAIL).source == "expected_loss"


def test_ties_raise_or_are_recorded_never_silently_resolved():
    s = spec()
    p_star = allow_block_threshold(s, 1)   # Allow-Block tie for a read tool at tier 1
    grid = build_loss_grid(LossSpec(s.C_FA, s.C_miss, s.C_mod, 10.0, s.r_mod), "t")  # Escalate dominated
    with pytest.raises(VerdictTieError):
        A3Policy(grid, preds(), tie_mode="raise").decide(p_star, 1, "get_balance", AVAIL)
    d = A3Policy(grid, preds(), tie_mode="record_chapter3_order").decide(p_star, 1, "get_balance", AVAIL)
    assert d.tie and set(d.tie_set) == {"allow", "block"} and d.verdict is Verdict.BLOCK


def test_dominance_check():
    g = build_loss_grid(spec(C_esc=0.6), "t")
    r = reachable_verdicts(g, 1, (Verdict.ALLOW, Verdict.ESCALATE, Verdict.BLOCK))
    assert r == {Verdict.ALLOW: True, Verdict.ESCALATE: False, Verdict.BLOCK: True}
    r4 = reachable_verdicts(build_loss_grid(spec(C_esc=0.3), "t"), 4, (Verdict.ALLOW, Verdict.ESCALATE, Verdict.BLOCK))
    assert all(r4.values())


def test_loss_spec_validation():
    with pytest.raises(ValueError):
        LossSpec({1: 1.0}, {1: 1.0}, {1: 1.0}, 0.1, {1: 1.5})
    with pytest.raises(ValueError):
        LossSpec({1: 1.0}, {1: 1.0, 2: 1.0}, {1: 1.0}, 0.1, {1: 0.5})
