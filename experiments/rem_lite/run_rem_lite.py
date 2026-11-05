"""REM-Lite ablation (Mode A: recorded traces) — nothing is refitted.

REM-Lite = existing REM features + the SAME ridge logistic regression (per outer fold) + FIXED decision
thresholds; Platt/logit calibration and the expected-loss decision are REMOVED from the decision path.
  probability : p~ = sigmoid(s)                       (uncalibrated; same fitted model as Full REM)
  thresholds  : theta_blk, theta_mod chosen on DEVELOPMENT data only = the benign inner out-of-fold
                probabilities of each outer fold's fitting portion, at the declared operating points
                alpha_blk = 0.01, alpha_mod = 0.05 (configs/exploratory/pilot_e0.yaml, baseline_B1);
                re-selected on the uncalibrated scale (the stored calibrated values are mapped back
                through the fold's inverse calibration, which is strictly monotone because gamma_1 > 0)
  verdicts    : Block if p~ >= theta_blk; Modify if theta_mod <= p~ < theta_blk (Block if Modify infeasible);
                Allow otherwise; predicates D1/D2 unchanged (Escalate only through D2)
  everything else unchanged: features, folds, tiers (audit only), predicates, mitigation semantics, logging.

Outputs (results/rem_lite/<run>/): rem_lite_results.json and the per-episode replay records.
usage: PILOT_RESULTS_DIR=<frozen pilot state> python3 experiments/rem_lite/run_rem_lite.py results/rem_lite/<run>
"""
from __future__ import annotations

import collections
import json
import os
import pickle
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))

import run_main as rm  # noqa: E402
from common import make_setup, provenance  # noqa: E402
from data import build, reference_from_mask  # noqa: E402
from rem.algorithms.a1 import A1Policy, A1Thresholds  # noqa: E402
from rem.algorithms.detection.ridge_logistic import sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402

LITE, FULL, B1KEY = "REMLite_step_level_no_reviewer", "REM_step_level_no_reviewer", "B1_step_level_no_reviewer"


def lite_policies(fits):
    a_blk, a_mod = rm.CFG["baseline_B1"]["alpha_blk"], rm.CFG["baseline_B1"]["alpha_mod"]
    out, th = {}, {}
    for f, ff in fits["label_nll_primary"].fits.items():
        pc = np.clip(np.asarray(ff.benign_oof_p, dtype=float), 1e-15, 1 - 1e-15)
        s = (np.log(pc / (1 - pc)) - ff.gamma_0) / ff.gamma_1          # inverse of p = sigmoid(g1 s + g0)
        t = A1Thresholds.fit(sigmoid(s), a_blk, a_mod)
        out[f] = A1Policy(t, rm.predicates())
        th[str(f)] = {"theta_blk_raw": t.theta_blk, "theta_mod_raw": t.theta_mod,
                      "theta_blk_calibrated_B1": ff.theta_blk, "theta_mod_calibrated_B1": ff.theta_mod,
                      "n_benign_development": int(pc.size)}
    return out, th


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    data = build("primary")
    fits, rmd = rm.load_state("crossfit"), rm.load_state("rmod")
    pol = rm.build_policies(fits, rmd["rmod"])
    lite, thresholds = lite_policies(fits)
    for f in pol:
        pol[f]["REMLite"] = lite[f]
    prim = fits["label_nll_primary"]
    y = np.asarray(data.y)
    tiers = [s.tier for s in data.steps]
    res = {"_label": "EXPLORATORY ablation on recorded traces (Mode A) - NOT a live-agent result",
           "provenance": provenance(), "definition": __doc__.split("\n\n")[1], "thresholds_per_fold": thresholds}

    # ---- (1) observe-only on held-out steps: REM-Lite vs B1 vs Full REM ---------------------------------
    def run(policy_key, p):
        v = []
        for i, s in enumerate(data.steps):
            v.append(pol[data.fold[i]][policy_key].decide(float(p[i]), int(tiers[i]), s.tool, s.available).verdict.value)
        return np.asarray(v, dtype=object)
    V = {"REM-Lite": run("REMLite", prim.p_raw), "B1 (thesis)": run("B1", prim.p_cal), "Full REM": run("A3_step_level", prim.p_cal)}
    obs = {}
    for name, v in V.items():
        loss = float(np.mean([pol[data.fold[i]]["grid_step_level"].loss(Verdict(v[i]), int(y[i]), int(tiers[i])) for i in range(len(v))]))
        obs[name] = {"intervention_y1": float(np.mean(v[y == 1] != "allow")), "intervention_y0": float(np.mean(v[y == 0] != "allow")),
                     "verdicts_y1": dict(collections.Counter(v[y == 1].tolist())), "verdicts_y0": dict(collections.Counter(v[y == 0].tolist())),
                     "realized_loss_declared_grid_base": loss}
    obs["identical_verdicts_REM-Lite_vs_B1"] = int(np.sum(V["REM-Lite"] == V["B1 (thesis)"]))
    obs["steps"] = int(len(y))
    obs["changed_verdicts_Full_REM_vs_REM-Lite"] = int(np.sum(V["REM-Lite"] != V["Full REM"]))
    res["observe_only_heldout"] = obs

    # ---- (2) calibration (held-out, step level): existing E1 values, raw vs calibrated -----------------
    e1 = json.load(open(os.path.join(REPO, "results", "pilot_R2", "e1_crossfit.json")))["label_nll_primary"]
    res["calibration_step_level_heldout"] = {"REM-Lite (uncalibrated p~)": e1["pooled_uncalibrated"],
                                             "Full REM (calibrated p)": e1["pooled_calibrated"],
                                             "source": "results/pilot_R2/e1_crossfit.json (label_nll_primary)"}

    # ---- (3) NO-ADAPT replay of all recorded episodes ---------------------------------------------------
    st = make_setup()
    folds = sorted(set(data.fold.tolist()), key=str)
    refs = {f: reference_from_mask(data, data.fold != f) for f in folds}
    rm.G.update(policies=pol, fits=fits)
    cfg = {LITE: {"variant": "step_level", "esc": "no_reviewer", "decide": rm._mk_decide("REMLite"),
                  "scorer": rm._mk_scorer("label_nll_primary", calibrated=False)}}
    t0 = time.time()
    out = rm.run_replays(cfg, sorted(data.episodes), st, data, refs)
    res["replay_seconds"] = time.time() - t0
    by = collections.defaultdict(dict)
    for eid, c, u, s, err, aud in out:
        by[eid][c] = (u, s, err, aud)
    for eid, c, u, s, err, aud in pickle.load(open(os.path.join(rm.RESULTS, "state", "replay_main.pkl"), "rb")):
        if c in ("B0", B1KEY, FULL):
            by[eid][c] = (u, s, err, aud)
    valid = sorted(e for e, ok in rmd["agree"].items() if ok)
    res["replay_valid_episodes"] = len(valid)
    res["replay_metrics"] = {c: rm.episode_metrics(data, by, c, valid) for c in ("B0", B1KEY, LITE, FULL)}
    same = sum(1 for e in data.episodes if by[e][LITE][:2] == by[e][B1KEY][:2]
               and [a[1] for a in by[e][LITE][3]] == [a[1] for a in by[e][B1KEY][3]])
    res["replay_REM-Lite_identical_to_B1_episodes"] = {"identical": same, "total": len(data.episodes)}
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    kw = dict(resamples=rm.B["resamples"], seed=rm.SEED, level=rm.B["interval"])
    diffs = {}
    for a, b in ((FULL, LITE), (LITE, "B0"), (FULL, "B0")):
        disc = collections.Counter((int(by[e][a][1]), int(by[e][b][1])) for e in att)
        diffs[f"{a}_minus_{b}"] = {
            "ASR": grouped_bootstrap(att, lambda x: data.episodes[x].injection_task_id,
                                     lambda s: float(np.mean([by[x][a][1] - by[x][b][1] for x in s])), **kw),
            "utility_under_attack": grouped_bootstrap(att, lambda x: data.episodes[x].injection_task_id,
                                                      lambda s: float(np.mean([by[x][a][0] - by[x][b][0] for x in s])), **kw),
            "benign_utility": grouped_bootstrap(ben, lambda x: data.episodes[x].user_task_id,
                                                lambda s: float(np.mean([by[x][a][0] - by[x][b][0] for x in s])), **kw),
            "attacked_pairs_security_(a,b)": {f"{k[0]},{k[1]}": v for k, v in disc.items()}}
    res["paired_differences_replay"] = diffs
    json.dump(res, open(os.path.join(out_dir, "rem_lite_results.json"), "w"), indent=1, default=str)
    with open(os.path.join(out_dir, "rem_lite_replay_episodes.jsonl"), "w") as fh:
        for eid in sorted(by):
            u, s, err, aud = by[eid][LITE]
            fh.write(json.dumps({"episode_id": eid, "utility": u, "security": s, "error": err,
                                 "audit": [list(a) for a in aud]}) + "\n")
    print(json.dumps({k: res[k] for k in ("observe_only_heldout", "replay_REM-Lite_identical_to_B1_episodes")}, indent=1, default=str))


if __name__ == "__main__":
    main(sys.argv[1])
