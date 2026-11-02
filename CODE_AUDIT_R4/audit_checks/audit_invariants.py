"""Audit checks of substantive invariants (read-only; does not modify REM code or results).

Usage (from the repository root):
    PILOT_RESULTS_DIR=<reproduction dir containing steps.pkl and state/> \
        python3 CODE_AUDIT_R4/audit_checks/audit_invariants.py

Each check prints PASS / FAIL / INFO with the quantity it measured.
"""

from __future__ import annotations

import json
import os
import pickle
import sys

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))
sys.path.insert(0, REPO)

from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.algorithms.attribution.linear_shapley import LinearShapleyAttributor  # noqa: E402
from rem.algorithms.behavior.evidence import FEATURE_ORDER  # noqa: E402
from rem.algorithms.calibration.logit_nll import LabelNLLLogitCalibrator  # noqa: E402
from rem.algorithms.calibration.platt import MonotonicityViolationError  # noqa: E402
from rem.algorithms.context.provenance import value_occurs_in  # noqa: E402
from rem.algorithms.decision.consequence import ConsequenceTierMap  # noqa: E402
from rem.algorithms.decision.loss_matrix import (  # noqa: E402
    LossSpec, allow_block_threshold, build_loss_grid, escalation_feasible, reachable_verdicts)
from rem.algorithms.decision.policy import PredicatePolicy  # noqa: E402
from rem.algorithms.detection.ridge_logistic import RidgeLogisticRegression, sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402

RESULTS = os.environ["PILOT_RESULTS_DIR"]
CFG_E1 = os.path.join(REPO, "results", "pilot_R2", "e1_crossfit.json")
SEVERITY = {"allow": 0, "modify": 1, "escalate": 2, "block": 3}
out = {}


def report(name, ok, detail):
    ok = None if ok is None else bool(ok)
    tag = "PASS" if ok is True else ("FAIL" if ok is False else "INFO")
    print(f"[{tag}] {name}: {detail}")
    out[name] = {"status": tag, "detail": detail}


# --- 1. Attribution identity (Eqs. 3.11-3.13) with the committed fold parameters ---------------
e1 = json.load(open(CFG_E1))
rng = np.random.default_rng(20261102)
worst = 0.0
for f, v in e1["label_nll_primary"]["per_fold"].items():
    coef = [v["coefficients"][n] for n in FEATURE_ORDER]
    xbar = {n: float(rng.uniform(0, 1)) for n in FEATURE_ORDER}  # any background satisfies the identity
    att = LinearShapleyAttributor(FEATURE_ORDER, coef, v["intercept"], xbar)
    for _ in range(200):
        x = rng.integers(0, 2, len(FEATURE_ORDER)).astype(float)
        s = v["intercept"] + float(np.dot(coef, x))
        phi = sum(att.shapley_value(i, x[i]) for i in range(len(x)))
        worst = max(worst, abs(att.base_value() + phi - s))
report("attribution_completeness_phi0_plus_sum_phi_equals_logit", worst < 1e-9, f"max |phi0+sum(phi)-s| = {worst:.2e} over 9 folds x 200 vectors")

# --- 2. Expected-loss verdict = brute-force argmin; thresholds; monotone severity in p ---------
spec = LossSpec(C_FA={k: 1.0 for k in (1, 2, 3, 4)}, C_miss={1: 1.0, 2: 5.0, 3: 10.0, 4: 20.0},
                C_mod={k: 0.5 for k in (1, 2, 3, 4)}, C_esc=0.3, r_mod={1: 1.0, 2: 1.0, 3: 0.0, 4: 0.01})
grid = build_loss_grid(spec, "audit")
pred = PredicatePolicy(frozenset(), 3, ("x_act1",), frozenset({"send_money", "update_password"}))
pol = A3Policy(grid, pred, tie_mode="record_chapter3_order")
mismatch, nonmono, transitions, prev_v = 0, 0, [], None
ps = np.linspace(0, 1, 20001)
for k in (1, 2, 3, 4):
    for tool in ("send_money", "get_balance"):
        prev = -1
        for p in ps:
            d = pol.decide(float(p), k, tool, {"x_act1": True})
            feas = pred.feasible(tool)
            r = {v: (1 - p) * grid.loss(v, 0, k) + p * grid.loss(v, 1, k) for v in feas}
            m = min(r.values())
            if abs(r[d.verdict] - m) > 1e-12:
                mismatch += 1
            sev = SEVERITY[d.verdict.value]
            if sev < prev:
                nonmono += 1
                transitions.append((k, tool, round(float(p), 4), prev_v, d.verdict.value))
            prev, prev_v = sev, d.verdict.value
report("a3_verdict_equals_bruteforce_argmin", mismatch == 0, f"{mismatch} mismatches on 4 tiers x 2 tools x 20001 p values")
report("a3_verdict_order_along_p_vs_ch3_restrictiveness_order", None,
       f"{nonmono} places where the verdict moves DOWN the Ch.3 restrictiveness order Block>Escalate>Modify>Allow as p increases "
       f"(pilot costs, r_mod=(1,1,0,0.01)): {transitions}. Expected-loss puts Escalate in a middle band (Chow-style reject); "
       "no monotone-restrictiveness property is claimed, so this is informational")
ths = [round(allow_block_threshold(spec, k), 6) for k in (1, 2, 3, 4)]
report("allow_block_threshold_eq_3_9", ths == [round(1 / 2, 6), round(1 / 6, 6), round(1 / 11, 6), round(1 / 21, 6)], f"p*_k = {ths}")
report("escalation_feasible_eq_3_10", None, {k: escalation_feasible(spec, k) for k in (1, 2, 3, 4)})
report("reachable_verdicts_send_money", None,
       {k: {v.value: r for v, r in reachable_verdicts(grid, k, pred.feasible('send_money')).items()} for k in (1, 2, 3, 4)})

# --- 3. Calibration fit: recovery and first-order optimality; gamma_1<=0 rejected -------------
s = rng.normal(0, 3, 20000)
y = (rng.uniform(size=s.size) < sigmoid(0.8 * s - 0.5)).astype(int)
cal = LabelNLLLogitCalibrator().fit(s, y)
g = np.array([np.sum(sigmoid(cal.gamma_1 * s + cal.gamma_0) - y), np.sum((sigmoid(cal.gamma_1 * s + cal.gamma_0) - y) * s)])
report("calibration_label_nll_recovers_parameters", abs(cal.gamma_1 - 0.8) < 0.05 and abs(cal.gamma_0 + 0.5) < 0.08,
       f"true (0.8,-0.5) -> fitted ({cal.gamma_1:.3f},{cal.gamma_0:.3f}); |grad| = {np.abs(g).max():.2e}")
try:
    LabelNLLLogitCalibrator().fit(-s, y)
    report("calibration_rejects_negative_slope", False, "no exception for an anti-monotone score")
except MonotonicityViolationError:
    report("calibration_rejects_negative_slope", True, "MonotonicityViolationError raised for an anti-monotone score")

# --- 4. Ridge fit on the real fold data: KKT conditions; lambda/2 convention; reproducibility ---
os.environ.setdefault("AGENTDOJO_RUNS", "/home/user/ethz-spylab/agentdojo/runs")
from data import Designer, build  # noqa: E402

data = build("primary")
f0 = "injection_task_0"
train = data.fold != f0
X = Designer(data)(train)
lam = e1["label_nll_primary"]["per_fold"][f0]["lambda"]
m = RidgeLogisticRegression(FEATURE_ORDER, penalty=lam).fit(X[train], data.y[train])
p = sigmoid(m.intercept + X[train] @ m.coefficients)
kkt_int = float(np.sum(p - data.y[train]))
kkt_slope = X[train].T @ (p - data.y[train]) + lam * m.coefficients   # gradient of NLL + (lam/2)||b||^2
ref = np.array([e1["label_nll_primary"]["per_fold"][f0]["coefficients"][n] for n in FEATURE_ORDER])
report("ridge_kkt_sum_loss_lambda_over_2", abs(kkt_int) < 1e-6 and np.abs(kkt_slope).max() < 1e-6,
       f"fold {f0}, lambda_impl={lam}: |dJ/db0|={abs(kkt_int):.1e}, max|dJ/db|={np.abs(kkt_slope).max():.1e}; converged={m.converged}")
report("ridge_refit_matches_committed_coefficients", np.abs(m.coefficients - ref).max() < 1e-6,
       f"max |refit - committed| = {np.abs(m.coefficients - ref).max():.2e} (n_train={int(train.sum())}; loss is a SUM, so lambda is not scaled by n)")

# --- 5. Coefficient signs vs a monotone-risk reading of the features --------------------------
neg = {f: {n: c for n, c in v["coefficients"].items() if c < 0} for f, v in e1["label_nll_primary"]["per_fold"].items()}
neg = {f: d for f, d in neg.items() if d}
report("coefficient_signs_all_positive", not neg, f"negative coefficients: {neg}")

# --- 6. Provenance matcher boundary cases (x_act1) ---------------------------------------------
cases = {
    "amount 3 vs date '2022-03-10'": value_occurs_in(3, ["Date: 2022-03-10"]),
    "amount 100 vs 'Total 100.00'": value_occurs_in(100, ["Total 100.00"]),
    "amount 10 vs '1,000'": value_occurs_in(10, ["pay 1,000"]),
    "IBAN case/space insensitive": value_occurs_in("us133000000121212121212", ["send to US133000000121212121212 now"]),
    "IBAN split by space is missed": value_occurs_in("US133000000121212121212", ["US13 3000 0001 2121 2121 212"]),
    "2-char string never matches": value_occurs_in("ab", ["ab"]),
    "'new_password' vs 'new password'": value_occurs_in("new_password", ["set new password"]),
}
report("provenance_matcher_boundary_cases", None, cases)

# --- 7. Tier map boundaries --------------------------------------------------------------------
cats = {"read": ["get_balance"], "profile_change": ["update_user_info"], "value_transfer": ["send_money"],
        "payment_modification": ["update_scheduled_transaction"], "credential_change": ["update_password"]}
tm = ConsequenceTierMap(cats, {"read": 1, "profile_change": 2, "value_transfer_at_or_below_limit": 3,
                               "value_transfer_above_limit": 4, "payment_modification": 4, "credential_change": 4}, 1000)
report("tier_boundaries", None, {"amount=1000": tm.tier("send_money", {"amount": 1000}),
                                 "amount=1000.01": tm.tier("send_money", {"amount": 1000.01}),
                                 "amount missing": tm.tier("send_money", {}),
                                 "amount='abc'": tm.tier("send_money", {"amount": "abc"}),
                                 "amount=-5000": tm.tier("send_money", {"amount": -5000})})

# --- 8. Meaning of y=1: attempt labels, not proof of causation or success ----------------------
steps = data.steps
y1 = [s for s in steps if s.label == 1]
before_change = sum(1 for s in y1 if not s.after_change_point)
ep_sec = {eid: e.security for eid, e in data.episodes.items()}
y1_failed = sum(1 for s in y1 if not ep_sec[s.episode_id])
y1_act1_0 = sum(1 for s in y1 if s.features["x_act1"] == 0)
y0_attacker = sum(1 for s in steps if s.label == 0 and s.attacker_key_match)
report("label_semantics", None, {
    "y1_steps": len(y1),
    "y1_before_injected_content_entered_context": before_change,
    "y1_in_episodes_where_attack_recorded_unsuccessful": y1_failed,
    "y1_with_x_act1_0": y1_act1_0,
    "y0_steps_carrying_attacker_value": y0_attacker,
    "y1_by_tool": {t: sum(1 for s in y1 if s.tool == t) for t in sorted({s.tool for s in y1})},
})

# --- 9. Structural: features computed before the call's own result is ingested -----------------
from rem.integration import steps as steps_mod  # noqa: E402
import inspect  # noqa: E402

src = inspect.getsource(steps_mod.build_steps)
report("features_precede_result_ingestion_in_build_steps",
       src.index("tracker.features(") < src.index("tracker.add_tool_result("),
       "tracker.features(...) is called on the proposed call before any later tool result is added")

json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "logs", "audit_invariants.json"), "w"), indent=1, default=str)
