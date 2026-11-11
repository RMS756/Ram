"""Measurements for 03_ORIGINAL_REM_WEAKNESS_AUDIT.md (original REM only; no candidate arm involved).

Uses the unchanged pilot state (PILOT_RESULTS_DIR) and the frozen bundle. Read-only on REM.
usage: PILOT_RESULTS_DIR=<dir> python3 experiments/authz_study/weakness_audit.py <out.json>
"""
from __future__ import annotations

import collections
import json
import multiprocessing as mp
import os
import pickle
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))

import common  # noqa: E402
from data import build  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard, replay_episode  # noqa: E402

CFG = common.load_config()
CAT = {t: c for c, ts in CFG["consequence"]["categories"].items() for t in ts}
G = {}


def state(name):
    with open(os.path.join(common.RESULTS, "state", name + ".pkl"), "rb") as fh:
        return pickle.load(fh)


def _job(job):
    eid, mode = job
    st, data, B = G["st"], G["data"], G["B"]
    ep = data.episodes[eid]
    F = B["folds"][data.episode_fold[eid]]
    pol = F["policies"]["A3_step_level"]

    def decide(c):
        d = pol.decide(c.p, c.tier, c.tool, c.available)
        v = d.verdict
        if mode == "all_block" and v is not Verdict.ALLOW:
            v = Verdict.BLOCK
        return v, d.source, {"orig": d.verdict.value}
    gc = GuardConfig(B["spec"], B["detector"], F["reference"], B["tier_map"], tuple(B["restricted_tools"]), "step_level", "no_reviewer")
    out = replay_episode(ep, st.suite, RemGuard(gc, F["scorer"], decide, B["labeler"], ep))
    return eid, mode, bool(out.utility), bool(out.security), [(a["tool"], a["details"]["orig"], a["released"]) for a in out.audit]


def main(out_path):
    st = common.make_setup()
    data = build("primary")
    rmd = state("rmod")
    valid = sorted(e for e, ok in rmd["agree"].items() if ok)
    vset = set(valid)
    res = state("replay_main")
    by = collections.defaultdict(dict)
    for eid, c, u, s, err, aud in res:
        if c in ("B0", "REM_step_level_no_reviewer", "B1_step_level_no_reviewer", "REM_step_level_idealized") or c.startswith("abl_") and "step_level_no_reviewer" in c:
            by[eid][c] = (u, s, err, aud)
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    out = {"provenance": common.provenance(), "n_attacked": len(att), "n_benign": len(ben)}

    # A. over-defence by action category (REM R4, step level, no reviewer)
    tab = collections.Counter()
    for e in valid:
        kind = "benign_episode" if e in set(ben) else "attacked_episode"
        for a in by[e]["REM_step_level_no_reviewer"][3]:
            tab[(kind, CAT.get(a[4], "other"), int(a[0]), a[1])] += 1
    out["A_verdicts_by_category"] = [{"episode": k[0], "category": k[1], "label_y": k[2], "verdict": k[3], "n": n}
                                     for k, n in sorted(tab.items())]

    # B. x_act1 versus the attempt label (all 6,762 primary steps, observe mode)
    c = collections.Counter()
    for s in data.steps:
        c[(int(s.label), int(s.features["x_act1"]), s.user_task_id == "user_task_15")] += 1
    out["B_xact1_vs_label"] = [{"y": k[0], "x_act1": k[1], "user_task_15": k[2], "n": n} for k, n in sorted(c.items())]
    y = np.array([s.label for s in data.steps])
    x1 = np.array([s.features["x_act1"] for s in data.steps])
    out["B_xact1_rule_as_classifier"] = {"recall_y1": float(x1[y == 1].mean()), "fire_rate_y0": float(x1[y == 0].mean()),
                                         "precision": float(y[x1 == 1].mean()), "n_steps": int(y.size)}
    # legit (y=0) restricted-tool calls in benign episodes: share with x_act1 = 1, by user task
    ut = collections.defaultdict(lambda: [0, 0])
    R = set(st.restricted)
    for s in data.steps:
        if s.injection_task_id is None and s.tool in R and s.episode_id in vset:
            ut[s.user_task_id][0] += int(s.features["x_act1"])
            ut[s.user_task_id][1] += 1
    out["B_benign_restricted_calls_xact1_by_user_task"] = {k: {"x_act1": v[0], "n": v[1]} for k, v in sorted(ut.items())}

    # C. user_task_15 collision
    ut15_pos = sum(1 for s in data.steps if s.label == 1 and s.user_task_id == "user_task_15")
    succ = [e for e in att if by[e]["REM_step_level_no_reviewer"][1]]
    out["C_user_task_15"] = {"positive_steps_in_ut15_episodes": ut15_pos,
                             "REM_successful_attack_episodes": len(succ),
                             "of_which_user_task_15": sum(1 for e in succ if data.episodes[e].user_task_id == "user_task_15"),
                             "objectives_containing_attacker_iban": sum(
                                 1 for e in valid if CFG["labels"]["attacker_key_arguments"]["recipient"] in (data.episodes[e].objective or "")),
                             "benchmark_versions_recorded": dict(collections.Counter(str(data.episodes[e].benchmark_version) for e in valid))}

    # D. component contributions (reproduced ablations, counts)
    abl = {}
    for cname in sorted({k for e in valid for k in by[e]}):
        abl[cname] = {"attacks_successful": int(sum(by[e][cname][1] for e in att)),
                      "benign_successful": int(sum(by[e][cname][0] for e in ben)),
                      "utility_under_attack": int(sum(by[e][cname][0] for e in att))}
    out["D_component_ablations_counts"] = abl

    # E. do Modify / Escalate / Block differ in step-level replay without a reviewer?
    with open(os.path.join(REPO, "experiments", "melon_rem", "frozen", "frozen_rem_bundle.pkl"), "rb") as fh:
        B = pickle.load(fh)
    G.update(st=st, data=data, B=B)
    jobs = [(e, m) for m in ("orig", "all_block") for e in valid]
    with mp.get_context("fork").Pool(4) as pool:
        rr = pool.map(_job, jobs, chunksize=64)
    r = collections.defaultdict(dict)
    for eid, mode, u, s, aud in rr:
        r[eid][mode] = (u, s, aud)
    diff_outcome = sum(1 for e in valid if r[e]["orig"][:2] != r[e]["all_block"][:2])
    diff_release = sum(1 for e in valid if [a[2] for a in r[e]["orig"][2]] != [a[2] for a in r[e]["all_block"][2]])
    diff_verdict = sum(1 for e in valid if [a[1] for a in r[e]["orig"][2]] != [a[1] for a in r[e]["all_block"][2]])
    same_as_state = sum(1 for e in valid if r[e]["orig"][:2] == by[e]["REM_step_level_no_reviewer"][:2])
    out["E_intervention_equivalence"] = {
        "episodes": len(valid),
        "orig_reproduces_stored_REM_outcomes": same_as_state,
        "episodes_with_different_utility_or_security_when_all_withholding_verdicts_are_Block": diff_outcome,
        "episodes_with_a_different_release_sequence": diff_release,
        "episodes_with_a_different_expected_loss_verdict_sequence": diff_verdict,
        "attacks_orig": int(sum(r[e]["orig"][1] for e in att)), "attacks_all_block": int(sum(r[e]["all_block"][1] for e in att)),
        "benign_orig": int(sum(r[e]["orig"][0] for e in ben)), "benign_all_block": int(sum(r[e]["all_block"][0] for e in ben)),
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1, default=common._default)
    print(json.dumps({k: out[k] for k in ("B_xact1_rule_as_classifier", "C_user_task_15", "E_intervention_equivalence")}, indent=1, default=common._default))


if __name__ == "__main__":
    main(sys.argv[1])
