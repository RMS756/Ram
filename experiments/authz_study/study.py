"""REM authorization-generalization study — isolated experimental module (protocol 06).

Status: [PROPOSED — SUPERVISOR APPROVAL REQUIRED]. Nothing under ``rem/`` and no approved
configuration is changed. Every estimator, calibrator, cost, tier map, predicate and replay element is
REM's own, imported unchanged; this module only (i) measures prefix-branch outcomes, (ii) fits REM's
estimator procedure on other training portions / targets / feature sets, and (iii) evaluates decision
rules declared in the protocol.

Stages (python3 experiments/authz_study/study.py <stage> ...):
  branch   prefix-branch outcomes for the primary and cross-template roles
  fit      S1 (primary folds) and S2 (double holdout) cell fits
  replay   enforcement replay of all arms under S1 and S2; S3 cross-template; reformatted-IBAN probe
  report   metrics, grouped bootstrap, tables (JSON)

Environment: PILOT_RESULTS_DIR = directory produced by the unchanged pilot pipeline
(steps.pkl, state/{crossfit,rmod,replay_rmod}.pkl); AUTHZ_STATE = directory for this study's state.
"""
from __future__ import annotations

import collections
import dataclasses
import json
import multiprocessing as mp
import os
import pickle
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))
sys.path.insert(0, HERE)

import common  # noqa: E402
import run_main as rm  # noqa: E402
from data import build, load_raw, reference_from_mask  # noqa: E402

from authz_evidence import AUTHZ_ORDER, RuntimeAuthz, offline_authz  # noqa: E402
from rem.algorithms.a1 import A1Policy, A1Thresholds  # noqa: E402
from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.algorithms.behavior.evidence import FEATURE_GROUPS, FEATURE_ORDER, BenignReference  # noqa: E402
from rem.algorithms.calibration.logit_nll import LabelNLLLogitCalibrator  # noqa: E402
from rem.algorithms.calibration.platt import MonotonicityViolationError  # noqa: E402
from rem.algorithms.decision.loss_matrix import build_loss_grid  # noqa: E402
from rem.algorithms.detection.ridge_logistic import RidgeLogisticRegression, sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402
from rem.evaluation.crossfit import assign_round_robin  # noqa: E402
from rem.evaluation.probabilistic import log_loss  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard, replay_episode  # noqa: E402
from rem.integration.steps import design_matrix  # noqa: E402

CFG = rm.CFG
E = CFG["estimation"]
SEED = CFG["meta"]["seed"]
BOOT = CFG["bootstrap"]
MIN_POS = int(CFG["pilot_E0_decision_values"]["min_positive_steps"])       # 50 (existing declared value)
COST_GRID = [float(m) for m in CFG["grid"]["C_miss_multiplier"]]            # 0.5, 1, 2, 5 (existing declared grid)
STATE = os.environ.get("AUTHZ_STATE") or os.path.join(common.RESULTS, "authz_state")
OUT = os.environ.get("AUTHZ_OUT") or os.path.join(REPO, "REM_Authorization_Generalization_Study", "results")
ATTACKER_IBAN = CFG["labels"]["attacker_key_arguments"]["recipient"]
ALL_ORDER = tuple(FEATURE_ORDER) + tuple(AUTHZ_ORDER)
FEATURE_SETS = {
    "F0": tuple(FEATURE_ORDER),
    "F1": ALL_ORDER,
    "F1_noact": tuple(f for f in ALL_ORDER if f not in FEATURE_GROUPS["act"]),
    "F1_nobeh": tuple(f for f in ALL_ORDER if f not in FEATURE_GROUPS["beh"]),
    "F1_noctx": tuple(f for f in ALL_ORDER if f not in FEATURE_GROUPS["ctx"]),
    # POST HOC amendment A-2 (after results): the original study's existing ablation "behavioural group removed"
    "F0_nobeh": tuple(f for f in FEATURE_ORDER if f not in FEATURE_GROUPS["beh"]),
}
TARGETS = ("y", "a", "b", "am", "bm")
EMPTY_REF = BenignReference(frozenset())
G = {}


def save(name, obj):
    os.makedirs(STATE, exist_ok=True)
    with open(os.path.join(STATE, name + ".pkl"), "wb") as fh:
        pickle.dump(obj, fh)


def load(name):
    with open(os.path.join(STATE, name + ".pkl"), "rb") as fh:
        return pickle.load(fh)


def pilot_state(name):
    with open(os.path.join(common.RESULTS, "state", name + ".pkl"), "rb") as fh:
        return pickle.load(fh)


def read_tools(st):
    return tuple(CFG["consequence"]["categories"]["read"])


# ---------------------------------------------------------------------------------------------
# stage: branch — prefix-branch outcomes (protocol section 3)
# ---------------------------------------------------------------------------------------------

def _branch_run(ep, st, withhold):
    count = {"i": 0}

    def decide(c):
        count["i"] += 1
        if count["i"] == withhold:
            return Verdict.BLOCK, "branch_withhold", {}
        return Verdict.ALLOW, "branch_release", {}
    gc = GuardConfig(st.spec, st.detector, EMPTY_REF, st.tier_map, st.restricted, "step_level", "no_reviewer")
    out = replay_episode(ep, st.suite, RemGuard(gc, None, decide, st.labeler, ep))
    return bool(out.utility), bool(out.security), out.error, [a["tool"] for a in out.audit]


def _branch_job(key):
    role, eid = key
    ep, st = G["eps"][role][eid], G["setup"]
    u0, s0, e0, tools = _branch_run(ep, st, 0)
    rows = []
    for j in range(1, len(tools) + 1):
        u, s, e, _ = _branch_run(ep, st, j)
        rows.append((tools[j - 1], u, s, e))
    return role, eid, (u0, s0, e0), rows


def stage_branch():
    st = common.make_setup()
    raw = load_raw()
    eps = {r: build(r, raw).episodes for r in ("primary", "cross_template")}
    G.update(setup=st, eps=eps)
    jobs = [(r, e) for r in eps for e in sorted(eps[r])]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_branch_job, jobs, chunksize=32)
    out = {r: {} for r in eps}
    for role, eid, b0, rows in res:
        out[role][eid] = {"B0": b0, "rows": rows}
    save("branch", out)
    n = sum(1 + len(v["rows"]) for r in out for v in out[r].values())
    print(f"branch: {len(jobs)} episodes, {n} replays in {time.time() - t0:.0f}s")


def branch_targets(data, branch):
    """Per-step ΔS, ΔU aligned with data.steps; returns dict of arrays and alignment statistics."""
    n = len(data.steps)
    dS, dU = np.zeros(n, dtype=int), np.zeros(n, dtype=int)
    aligned = np.zeros(n, dtype=bool)
    per_ep = collections.defaultdict(list)
    for i, s in enumerate(data.steps):
        per_ep[s.episode_id].append((s.index, i))
    stats = collections.Counter()
    for eid, lst in per_ep.items():
        idx = [i for _, i in sorted(lst)]
        b = branch[eid]
        u0, s0, _ = b["B0"]
        rows = b["rows"]
        ptr = 0
        for i in idx:
            if ptr < len(rows) and rows[ptr][0] == data.steps[i].tool:
                _, u, s, _err = rows[ptr]
                dU[i] = int(u0) - int(u)
                dS[i] = (int(s0) - int(s)) if data.episodes[eid].attacked else 0
                aligned[i] = True
                ptr += 1
            else:
                stats["steps_without_branch"] += 1
        if ptr != len(rows):
            stats["episodes_with_unused_branch_rows"] += 1
        stats["episodes"] += 1
    t = {"a": (dS == 1).astype(int), "am": (dS == -1).astype(int),
         "b": (dU == 1).astype(int), "bm": (dU == -1).astype(int)}
    return t, aligned, dict(stats)


def authz_matrix(data, st):
    """n x 2 matrix (z_exp, z_del) aligned with data.steps."""
    Z = np.zeros((len(data.steps), 2))
    per_ep = collections.defaultdict(list)
    for i, s in enumerate(data.steps):
        per_ep[s.episode_id].append((s.index, i))
    rt = read_tools(st)
    for eid, lst in per_ep.items():
        z = offline_authz(data.episodes[eid], st.spec, st.restricted, rt)
        idx = [i for _, i in sorted(lst)]
        if len(z) != len(idx):
            raise RuntimeError(f"authz alignment failed for {eid}: {len(z)} vs {len(idx)}")
        for k, i in enumerate(idx):
            Z[i] = z[k]
    return Z


# ---------------------------------------------------------------------------------------------
# stage: fit — REM's estimator procedure on a given fitting portion (Procedure 3.1, lines 3-8)
# ---------------------------------------------------------------------------------------------

def _cols(order):
    return [ALL_ORDER.index(f) for f in order]


def fit_cell(train, feature_sets, targets):
    """Fit every (feature set, target) on the rows in ``train`` exactly as rem.evaluation.crossfit does
    for one outer fold: grouped inner CV for lambda, calibration on inner out-of-fold logits, refit."""
    data, Z, T = G["data"], G["Z"], G["T"]
    n = len(data.steps)
    inner_g, benign_g = data.inner_group, ~data.attacked
    K = int(E["inner_folds"])
    tr_idx = np.flatnonzero(train)
    att_map = assign_round_robin([inner_g[i] for i in tr_idx if not benign_g[i]], K)
    ben_map = assign_round_robin([inner_g[i] for i in tr_idx if benign_g[i]], K)
    inner = np.full(n, -1)
    for i in tr_idx:
        inner[i] = (ben_map if benign_g[i] else att_map)[inner_g[i]]

    def base(mask):
        return np.hstack([design_matrix(data.steps, reference_from_mask(data, mask), FEATURE_ORDER), Z])
    X_out = base(train)
    inner_X = {j: base(train & (inner != j)) for j in range(K)}
    ref = reference_from_mask(data, train)
    models = {}
    for fs in feature_sets:
        order = FEATURE_SETS[fs]
        cols = _cols(order)
        for tname in targets:
            y = T[tname]
            npos = int(y[train].sum())
            if tname != "y" and npos < MIN_POS:
                models[(fs, tname)] = None
                continue
            oof = {lam: np.full(n, np.nan) for lam in E["lambda_grid"]}
            scores = {}
            for lam in E["lambda_grid"]:
                for j in range(K):
                    fit_mask = train & (inner != j)
                    hold = train & (inner == j)
                    if not hold.any():
                        continue
                    Xj = inner_X[j][:, cols]
                    m = RidgeLogisticRegression(order, penalty=lam).fit(Xj[fit_mask], y[fit_mask])
                    oof[lam][hold] = m.intercept + Xj[hold] @ np.asarray(m.coefficients, dtype=float)
                scores[lam] = log_loss(y[train], sigmoid(oof[lam][train]), E["probability_clip"])
            lam_star = min(E["lambda_grid"], key=lambda l: (scores[l], -l))
            cal = LabelNLLLogitCalibrator()
            failed = False
            try:
                cal.fit(oof[lam_star][train], y[train])
                g0, g1 = float(cal.gamma_0), float(cal.gamma_1)
            except MonotonicityViolationError:
                failed, g0, g1 = True, 0.0, 1.0
            m = RidgeLogisticRegression(order, penalty=lam_star).fit(X_out[train][:, cols], y[train])
            rec = {"order": order, "b0": float(m.intercept), "coef": [float(c) for c in m.coefficients],
                   "g0": g0, "g1": g1, "failed": failed, "lam": float(lam_star), "npos": npos, "ntrain": int(train.sum())}
            if tname == "y" and fs == "F0":
                ben = sigmoid(g1 * oof[lam_star][train & (y == 0)] + g0)
                th = A1Thresholds.fit(ben, CFG["baseline_B1"]["alpha_blk"], CFG["baseline_B1"]["alpha_mod"])
                rec["theta_blk"], rec["theta_mod"] = float(th.theta_blk), float(th.theta_mod)
            models[(fs, tname)] = rec
    return {"models": models, "reference": ref, "X_out": None}, X_out


def score_rows(rec, X, calibrated=True):
    if rec is None:
        return np.zeros(X.shape[0])
    s = rec["b0"] + X[:, _cols(rec["order"])] @ np.asarray(rec["coef"])
    return sigmoid(rec["g1"] * s + rec["g0"]) if (calibrated and not rec["failed"]) else sigmoid(s)


def _fit_job(job):
    key, kind = job
    data = G["data"]
    if kind == "S1":
        train = data.fold != key[1]
        test = ~train
        fsets = [k for k in FEATURE_SETS if k != "F0_nobeh"]
    else:
        _, u, i = key
        ut, it = G["ut"], G["it"]
        train = (ut != u) & (it != i)
        test = (ut == u) & ((it == i) | (G["benign_step"] & (G["fold_arr"] == i)))
        fsets = ["F0", "F1"]
    cell, X_out = fit_cell(train, fsets, TARGETS)
    held = {k: score_rows(rec, X_out[test]) for k, rec in cell["models"].items()}
    held_raw = {k: score_rows(rec, X_out[test], calibrated=False) for k, rec in cell["models"].items()}
    cell["rmod"] = cell_rmod(key, kind)
    return key, cell, np.flatnonzero(test), held, held_raw


def cell_rmod(key, kind):
    """r_mod(k) for the cell's fitting portion (step-level variant), as experiments/pilot stage_rmod."""
    if kind == "S1":
        return dict(G["rmod_frozen"]["step_level"][key[1]])
    _, u, i = key
    per = collections.defaultdict(list)
    for eu, ei, k, sec in G["rmod_rows"]:
        if eu != u and ei != i:
            per[k].append(sec)
    return {int(k): float(np.mean(v)) for k, v in per.items()}


def stage_fit():
    st = common.make_setup()
    raw = load_raw()
    data = build("primary", raw)
    branch = load("branch")["primary"]
    T, aligned, astats = branch_targets(data, branch)
    T["y"] = data.y.copy()
    Z = authz_matrix(data, st)
    rmd = pilot_state("rmod")
    rr = pilot_state("replay_rmod")
    by = collections.defaultdict(dict)
    for eid, c, u, s, err, aud in rr:
        by[eid][c] = (u, s, err, aud)
    rows = []
    for eid in by:
        ep = data.episodes[eid]
        if not ep.attacked or not rmd["agree"][eid]:
            continue
        mod = [a for a in by[eid]["oracle_modify_step_level"][3] if a[1] == "modify"]
        if mod:
            rows.append((ep.user_task_id, ep.injection_task_id, mod[0][3], by[eid]["oracle_modify_step_level"][1]))
    ut = np.array([s.user_task_id for s in data.steps], dtype=object)
    it = np.array([s.injection_task_id or "none" for s in data.steps], dtype=object)
    G.update(data=data, Z=Z, T=T, ut=ut, it=it, benign_step=~data.attacked, fold_arr=data.fold,
             rmod_frozen=rmd["rmod"], rmod_rows=rows)
    valid = sorted(e for e, ok in rmd["agree"].items() if ok)
    cells2 = set()
    for e in valid:
        ep = data.episodes[e]
        cells2.add(("S2", ep.user_task_id, ep.injection_task_id or data.episode_fold[e]))
    jobs = [(("S1", f), "S1") for f in sorted(set(data.fold.tolist()), key=str)] + [(k, "S2") for k in sorted(cells2)]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_fit_job, jobs, chunksize=2)
    cells, heldout = {}, {"S1": {}, "S2": {}}
    n = len(data.steps)
    for key, cell, test_idx, held, held_raw in res:
        cells[key] = cell
        for k in held:
            arr = heldout[key[0]].setdefault(k, (np.full(n, np.nan), np.full(n, np.nan)))
            arr[0][test_idx] = held[k]
            arr[1][test_idx] = held_raw[k]
    save("cells", cells)
    save("fit_aux", {"T": T, "Z": Z, "aligned": aligned, "align_stats": astats, "heldout": heldout, "valid": valid})
    print(f"fit: {len(jobs)} cells in {time.time() - t0:.0f}s; alignment {astats}")
    print({k: int(v.sum()) for k, v in T.items()})


# ---------------------------------------------------------------------------------------------
# decision rules (protocol section 5)
# ---------------------------------------------------------------------------------------------

LOSS = CFG["losses"]


def _c_miss(k):
    return float(LOSS["C_miss"][k])


def _c_fa(k):
    return float(LOSS["C_FA"][k])


def make_guard(arm, cell, ep, st):
    """A RemGuard whose decide function implements ``arm`` with the fitted quantities of ``cell``."""
    gc = GuardConfig(st.spec, st.detector, cell["reference"] if cell else EMPTY_REF, st.tier_map, st.restricted,
                     "step_level", "no_reviewer")
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    rt = RuntimeAuthz(st.spec, st.restricted, read_tools(st), ep.objective)
    preds = rm.predicates()
    restricted = set(st.restricted)
    models = cell["models"] if cell else {}
    base, _, suffix = arm.partition("@")
    mult = float(suffix) if suffix else 1.0
    pol = None
    if base in ("M00", "M10", "M00+AZ", "M01", "M00_nobeh"):
        grid = build_loss_grid(rm.loss_spec(cell["rmod"]), f"authz study cell {arm}")
        excl = (Verdict.ESCALATE, Verdict.MODIFY) if base == "M01" else ()
        pol = A3Policy(grid, preds, tie_mode="record_chapter3_order", exclude_from_expected_loss=excl)
    if base == "B1":
        rec = models[("F0", "y")]
        pol = A1Policy(A1Thresholds(rec["theta_blk"], rec["theta_mod"], CFG["baseline_B1"]["alpha_blk"],
                                    CFG["baseline_B1"]["alpha_mod"]), preds)

    def p_of(fs, target, x, calibrated=True):
        rec = models.get((fs, target))
        if rec is None:
            return 0.0
        s = rec["b0"] + sum(c * x[n] for n, c in zip(rec["order"], rec["coef"]))
        return float(sigmoid(rec["g1"] * s + rec["g0"])) if (calibrated and not rec["failed"]) else float(sigmoid(s))

    def decide(c):
        f, avail = guard.tracker.features(c.tool, c.args)
        z = rt.evidence(guard.tracker, c.tool, c.args)
        x = dict(f)
        x["z_exp"], x["z_del"] = z
        is_r = c.tool in restricted
        det = {}
        if base == "B0":
            v, src = Verdict.ALLOW, "allow_all"
        elif base == "P1":
            v, src = (Verdict.BLOCK if is_r and x["x_act1"] == 1 else Verdict.ALLOW), "rule_x_act1"
        elif base == "P2":
            v, src = (Verdict.BLOCK if is_r and (x["x_act1"] == 1 or x["x_act2"] == 1) else Verdict.ALLOW), "rule_x_act1_or_2"
        elif base == "A1":
            v, src = (Verdict.BLOCK if is_r and z == (0.0, 0.0) else Verdict.ALLOW), "rule_authz"
        elif base == "A2":
            v, src = (Verdict.BLOCK if is_r and z[0] == 0.0 else Verdict.ALLOW), "rule_explicit"
        elif base in ("B1", "M00", "M01"):
            d = pol.decide(p_of("F0", "y", x), c.tier, c.tool, avail)
            v, src = d.verdict, d.source
            det = {"tie": bool(getattr(d, "tie", False))}
        elif base == "M10":
            d = pol.decide(p_of("F0", "a", x), c.tier, c.tool, avail)
            v, src = d.verdict, d.source
            det = {"tie": bool(getattr(d, "tie", False))}
        elif base == "M00_nobeh":   # POST HOC A-2: original REM rule on the existing no-behaviour ablation features
            d = pol.decide(p_of("F0_nobeh", "y", x), c.tier, c.tool, avail)
            v, src = d.verdict, d.source
            det = {"tie": bool(getattr(d, "tie", False))}
        elif base == "M00+AZ":
            d = pol.decide(p_of("F1", "y", x), c.tier, c.tool, avail)
            v, src = d.verdict, d.source
            det = {"tie": bool(getattr(d, "tie", False))}
        else:   # intervention-value arms
            fs = {"M11": "F0", "M11y": "F0", "M11+AZ": "F1", "M11+AZ_noact": "F1_noact", "M11+AZ_nobeh": "F1_nobeh",
                  "M11+AZ_noctx": "F1_noctx", "M11+AZ_uncal": "F1"}[base]
            cal = base != "M11+AZ_uncal"
            forced = preds.evaluate(c.tool, c.tier, avail)
            if forced.verdict is not None:
                v, src = forced.verdict, forced.source or "predicate"
            else:
                dS = p_of(fs, "y", x, cal) if base == "M11y" else p_of(fs, "a", x, cal) - p_of(fs, "am", x, cal)
                dU = p_of(fs, "b", x, cal) - p_of(fs, "bm", x, cal)
                lhs, rhs = _c_miss(c.tier) * mult * dS, _c_fa(c.tier) * dU
                withhold = lhs >= rhs and lhs > 0
                v, src = (Verdict.BLOCK if withhold else Verdict.ALLOW), "intervention_value"
                det = {"tie": bool(lhs == rhs and lhs > 0), "dS": dS, "dU": dU}
        rt.record(guard.tracker, c.tool, c.args, v is Verdict.ALLOW)
        det["z"] = z
        return v, src, det
    guard.decide = decide
    return guard


RULE_ARMS = ["B0", "P1", "P2", "A1", "A2"]
LEARNED_ARMS = ["B1", "M00", "M01", "M10", "M11", "M11y", "M00+AZ", "M11+AZ"]
GRID_ARMS = [f"{a}@{m:g}" for a in ("M11", "M11+AZ") for m in COST_GRID if m != 1.0]
ABL_ARMS = ["M11+AZ_noact", "M11+AZ_nobeh", "M11+AZ_noctx", "M11+AZ_uncal"]


def _replay_job(job):
    scheme, eid, arm, role = job
    st = G["setup"]
    ep = G["eps"][role][eid]
    cell = G["cells"][G["cell_of"][scheme][(role, eid)]]
    guard = make_guard(arm, cell, ep, st)
    out = replay_episode(ep, st.suite, guard)
    aud = [(a["label"], a["verdict"], a["released"], a["tier"], a["tool"], a["rem_latency_full_ms"], a["verdict_source"],
            bool(a["details"].get("tie", False)), tuple(a["details"].get("z", (0.0, 0.0)))) for a in out.audit]
    return scheme, role, eid, arm, bool(out.utility), bool(out.security), out.error, aud


def spaced(iban):
    return " ".join(iban[i:i + 4] for i in range(0, len(iban), 4))


def stage_replay():
    st = common.make_setup()
    raw = load_raw()
    data = build("primary", raw)
    xt = build("cross_template", raw)
    cells = load("cells")
    aux = load("fit_aux")
    valid = aux["valid"]
    # reformatted-identifier probe: attacked eligible episodes whose injected text contains the attacker IBAN
    probe = {}
    for e in valid:
        ep = data.episodes[e]
        if ep.attacked and any(ATTACKER_IBAN in v for v in ep.injections.values()):
            probe[e] = dataclasses.replace(ep, injections={k: v.replace(ATTACKER_IBAN, spaced(ATTACKER_IBAN))
                                                           for k, v in ep.injections.items()})
    eps = {"primary": data.episodes, "cross_template": xt.episodes, "probe_iban": probe}
    cell_of = {"S1": {}, "S2": {}}
    for e in valid:
        ep = data.episodes[e]
        cell_of["S1"][("primary", e)] = ("S1", data.episode_fold[e])
        cell_of["S2"][("primary", e)] = ("S2", ep.user_task_id, ep.injection_task_id or data.episode_fold[e])
    for e, ep in xt.episodes.items():
        cell_of["S1"][("cross_template", e)] = ("S1", ep.injection_task_id)
    for e in probe:
        cell_of["S1"][("probe_iban", e)] = ("S1", data.episode_fold[e])
    G.update(setup=st, eps=eps, cells=cells, cell_of=cell_of)
    jobs = []
    for a in RULE_ARMS + LEARNED_ARMS + GRID_ARMS + ABL_ARMS:
        jobs += [("S1", e, a, "primary") for e in valid]
    for a in RULE_ARMS + LEARNED_ARMS + GRID_ARMS:
        jobs += [("S2", e, a, "primary") for e in valid]
    for a in RULE_ARMS + LEARNED_ARMS:
        jobs += [("S1", e, a, "cross_template") for e in sorted(xt.episodes)]
        jobs += [("S1", e, a, "probe_iban") for e in sorted(probe)]
    t0 = time.time()
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(_replay_job, jobs, chunksize=64)
    save("replay", res)
    print(f"replay: {len(jobs)} replays in {time.time() - t0:.0f}s; probe episodes {len(probe)}")


if __name__ == "__main__":
    stages = {"branch": stage_branch, "fit": stage_fit, "replay": stage_replay}
    for name in sys.argv[1:]:
        print("== stage", name, flush=True)
        stages[name]()
