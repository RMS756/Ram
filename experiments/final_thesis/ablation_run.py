"""Final ablation study of the frozen REM v1.0 (protocol: REM_FINAL_THESIS_COMPLETION_2026_11_19/02_FROZEN_ABLATION_PROTOCOL.md).

REM v1.0 code (rem/) and the pilot pipeline (experiments/pilot/) are imported, never edited. The fitted state (cross-fitted
ridge models, calibrators, B1 thresholds, r_mod) comes from a fresh run of the frozen pilot pipeline into $PILOT_RESULTS_DIR
(build_dataset, e0_pilot, run_main crossfit rmod replay), whose reproduction of the published REM v1.0 counts is checked
before any arm is scored here.

Arms (step-level mitigation, no reviewer = the deployment configuration of Chapter 3):
  B0  no defence                       A0  REM v1.0 (frozen)
  A1  without behavioural evidence     (refit without the 'beh' group; existing pilot refit)
  A2  without Platt calibration        (raw logistic probability into the same expected-loss engine; loss boundaries fixed)
  A3  consequence-independent thresholds (frozen baseline B1; thresholds selected per outer fold on its training data)
  A4a without context evidence         (refit without 'ctx')        A4b without action/provenance evidence (refit without 'act')
  A5  without Modify                   (Modify removed from the verdict set; expected loss over Allow/Escalate/Block)
  A6  without the learned decision     (policy predicates D1/D2 only; every other call is Allowed)
  A7  without policy predicates        (expected loss only)
Output: REM_FINAL_THESIS_COMPLETION_2026_11_19/results/ablation_*.json, 03_ABLATION_RESULTS.csv
"""
from __future__ import annotations

import collections
import csv
import json
import os
import pickle
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "pilot"))
import run_main as RM  # noqa: E402  (frozen pilot pipeline; reads PILOT_RESULTS_DIR)
from data import build, reference_from_mask  # noqa: E402
from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402
from rem.evaluation.probabilistic import (average_precision, brier_binary, expected_calibration_error, log_loss,  # noqa: E402
                                          roc_auc)

OUT = ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19"
V, E2 = "step_level", "no_reviewer"
KW = dict(resamples=RM.B["resamples"], seed=RM.SEED, level=RM.B["interval"])
ARMS = ["B0", "A0", "A1", "A2", "A3", "A4a", "A4b", "A5", "A6", "A7"]
NAMES = {"B0": "No defence", "A0": "REM v1.0 (frozen)", "A1": "without behavioural evidence", "A2": "without Platt calibration",
         "A3": "consequence-independent thresholds (B1)", "A4a": "without context evidence",
         "A4b": "without action/provenance evidence", "A5": "without Modify", "A6": "without the learned decision (predicates only)",
         "A7": "without policy predicates"}
CATEGORY = {"send_money": "value_transfer", "schedule_transaction": "value_transfer", "update_scheduled_transaction": "payment_modification",
            "update_user_info": "profile_change", "update_password": "credential_change"}


def _decide_predicates_only(f):
    P = RM.predicates()

    def decide(c):
        o = P.evaluate(c.tool, c.tier, c.available)
        return (o.verdict, o.source, {}) if o.verdict is not None else (Verdict.ALLOW, "no_learned_allow", {})
    return decide


def configs():
    base = RM.replay_configs()
    C = {"B0": base["B0"], "A0": base[f"REM_{V}_{E2}"], "A1": base[f"abl_no_beh_{V}_{E2}"],
         "A2": base[f"abl_no_calibration_{V}_{E2}"], "A3": base[f"B1_{V}_{E2}"], "A4a": base[f"abl_no_ctx_{V}_{E2}"],
         "A4b": base[f"abl_no_act_{V}_{E2}"], "A7": base[f"abl_no_predicates_{V}_{E2}"],
         "A5": {"variant": V, "esc": E2, "decide": RM._mk_decide(f"A3_nomod_{V}"), "scorer": RM._mk_scorer("label_nll_primary")},
         "A6": {"variant": V, "esc": E2, "decide": _decide_predicates_only, "scorer": RM._mk_scorer("label_nll_primary")}}
    return C


def calibration(data, fits):
    """Offline probability quality on held-out (cross-fitted) steps."""
    out = {}
    y = data.y
    common = ~np.isnan(fits["label_nll_primary"].p_cal)       # same held-out steps for every arm
    for k in ("no_beh", "no_ctx", "no_act"):
        common &= ~np.isnan(fits[k].p_cal)
    for arm, key, cal in (("A0", "label_nll_primary", True), ("A2", "label_nll_primary", False), ("A1", "no_beh", True),
                          ("A4a", "no_ctx", True), ("A4b", "no_act", True)):
        r = fits[key]
        p = r.p_cal if cal else r.p_raw
        ok = common & ~np.isnan(p)
        yy, pp = y[ok], p[ok]
        out[arm] = {"steps": int(ok.sum()), "positives": int(yy.sum()), "roc_auc": roc_auc(yy, pp), "pr_auc": average_precision(yy, pp),
                    "brier": brier_binary(yy, pp), "ece_10": expected_calibration_error(yy, pp, RM.E["ece_bins"]),
                    "log_loss": log_loss(yy, pp, RM.E["probability_clip"])}
    return out


def main():
    data = build("primary")
    fits = RM.load_state("crossfit")
    rm = RM.load_state("rmod")
    pol = RM.build_policies(fits, rm["rmod"])
    for f in pol:                                            # A5: Modify removed from the verdict set
        pol[f][f"A3_nomod_{V}"] = A3Policy(pol[f][f"grid_{V}"], RM.predicates(), tie_mode="record_chapter3_order",
                                          exclude_from_expected_loss=(Verdict.MODIFY,))
    folds = sorted(set(data.fold.tolist()), key=str)
    refs = {f: reference_from_mask(data, data.fold != f) for f in folds}
    RM.G.update(policies=pol, fits=fits)
    C = configs()
    st = RM.make_setup()
    res = RM.run_replays(C, sorted(data.episodes), st, data, refs)
    with open(os.path.join(RM.STATE, "final_ablation_replays.pkl"), "wb") as fh:
        pickle.dump(res, fh)
    by = collections.defaultdict(dict)
    for eid, c, u, s, err, aud in res:
        by[eid][c] = (u, s, err, aud)
    valid = sorted(e for e, ok in rm["agree"].items() if ok)
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    restricted = set(st.restricted)
    usr = lambda e: data.episodes[e].user_task_id   # noqa: E731
    inj = lambda e: data.episodes[e].injection_task_id   # noqa: E731
    M, rows = {}, []
    for a in ARMS:
        steps = [x for e in valid for x in by[e][a][3]]
        rr = [x for x in steps if x[4] in restricted]
        leg = [x for e in ben for x in by[e][a][3] if x[4] in restricted and x[0] != 1]
        pos = [x for x in rr if x[0] == 1]
        vr = collections.Counter(str(x[1]).lower() for x in rr)
        mod_eps = [e for e in att if any(x[0] == 1 and x[1] == "modify" for x in by[e][a][3])]
        lat = [x[8] for x in steps]
        m = {"arm": a, "name": NAMES[a], "n_attacked": len(att), "n_benign": len(ben),
             "attack_successes": int(sum(by[e][a][1] for e in att)),
             "ASR": grouped_bootstrap(att, inj, lambda s: float(np.mean([by[e][a][1] for e in s])), **KW),
             "benign_completed": int(sum(by[e][a][0] for e in ben)),
             "benign_utility": grouped_bootstrap(ben, usr, lambda s: float(np.mean([by[e][a][0] for e in s])), **KW),
             "tasks_under_attack": int(sum(by[e][a][0] for e in att)),
             "all_tasks_completed": int(sum(by[e][a][0] for e in valid)),
             "attack_labelled_calls": len(pos), "attack_labelled_released": sum(1 for x in pos if x[2]),
             "episodes_with_released_attack_call": sum(1 for e in att if any(x[0] == 1 and x[2] for x in by[e][a][3])),
             "legitimate_calls": len(leg), "legitimate_released": sum(1 for x in leg if x[2]),
             "legitimate_payments": sum(1 for x in leg if CATEGORY.get(x[4]) == "value_transfer"),
             "legitimate_payments_released": sum(1 for x in leg if CATEGORY.get(x[4]) == "value_transfer" and x[2]),
             "restricted_calls": len(rr), **{f"rate_{k}": vr.get(k, 0) / max(1, len(rr)) for k in ("allow", "modify", "escalate", "block")},
             **{f"n_{k}": vr.get(k, 0) for k in ("allow", "modify", "escalate", "block")},
             "residual_ASR_after_modify": (float(np.mean([by[e][a][1] for e in mod_eps])) if mod_eps else None),
             "episodes_with_modify_on_attack_call": len(mod_eps),
             "latency_ms_mean": float(np.mean(lat)), "latency_ms_median": float(np.median(lat)),
             "latency_ms_p95": float(np.percentile(lat, 95)), "calls_timed": len(lat),
             "replay_errors": sum(1 for e in valid if by[e][a][2])}
        m["false_positive_intervention_rate"] = 1 - m["legitimate_released"] / max(1, m["legitimate_calls"])
        # decision-level precision / recall of "withhold" against the attempt label (restricted calls)
        tp = sum(1 for x in rr if x[0] == 1 and not x[2])
        fp = sum(1 for x in rr if x[0] != 1 and not x[2])
        fn = sum(1 for x in rr if x[0] == 1 and x[2])
        m["withhold_precision"] = tp / (tp + fp) if tp + fp else None
        m["withhold_recall"] = tp / (tp + fn) if tp + fn else None
        m["withhold_f1"] = (2 * tp / (2 * tp + fp + fn)) if tp else 0.0
        M[a] = m
        rows.append({k: (v[0] if isinstance(v, list) else v) for k, v in m.items()})
    diffs = {}
    for a in ARMS:
        if a == "A0":
            continue
        diffs[f"{a} minus A0"] = {
            "ASR": grouped_bootstrap(att, inj, lambda s: float(np.mean([by[e][a][1] - by[e]["A0"][1] for e in s])), **KW),
            "benign_utility": grouped_bootstrap(ben, usr, lambda s: float(np.mean([by[e][a][0] - by[e]["A0"][0] for e in s])), **KW),
            "all_tasks": grouped_bootstrap(valid, usr, lambda s: float(np.mean([by[e][a][0] - by[e]["A0"][0] for e in s])), **KW),
            "attacks_gained_removed": [sum(1 for e in att if by[e][a][1] and not by[e]["A0"][1]),
                                       sum(1 for e in att if by[e]["A0"][1] and not by[e][a][1])],
            "tasks_gained_lost": [sum(1 for e in valid if by[e][a][0] and not by[e]["A0"][0]),
                                  sum(1 for e in valid if by[e]["A0"][0] and not by[e][a][0])]}
    # decision reachability of A0 against A6 (same recorded call sequence under NO-ADAPT)
    reach = collections.Counter()
    for e in valid:
        x0, x6 = by[e]["A0"][3], by[e]["A6"][3]
        if len(x0) != len(x6):
            reach["different_call_sequence_episodes"] += 1
            continue
        for a0, a6 in zip(x0, x6):
            reach["calls_total"] += 1
            reach["calls_scored_by_estimator"] += 1
            if a0[7] in ("D1", "D2"):
                reach["forced_by_predicates_before_expected_loss"] += 1
                continue
            reach["reached_expected_loss"] += 1
            if a0[4] in restricted:
                reach["reached_expected_loss_restricted"] += 1
            if a0[2] == a6[2]:
                reach["unchanged_release"] += 1
                continue
            kind = "attack_labelled" if a0[0] == 1 else ("legit_benign_episode" if not data.episodes[e].attacked else "unlabelled_attacked_episode")
            reach[f"ml_withheld_{kind}"] += 1
    ep_change = {"tasks_lost_due_to_ml": sum(1 for e in valid if by[e]["A6"][0] and not by[e]["A0"][0]),
                 "tasks_gained_due_to_ml": sum(1 for e in valid if by[e]["A0"][0] and not by[e]["A6"][0]),
                 "attacks_prevented_due_to_ml": sum(1 for e in att if by[e]["A6"][1] and not by[e]["A0"][1]),
                 "attacks_admitted_due_to_ml": sum(1 for e in att if by[e]["A0"][1] and not by[e]["A6"][1])}
    out = {"status": "CONTROLLED EVIDENCE under 02_FROZEN_ABLATION_PROTOCOL.md; offline replay (NO-ADAPT) of recorded AgentDojo "
                     "banking episodes; primary population, scheme S1 (held-out attacker objective); no model call",
           "episodes_valid": len(valid), "n_attacked": len(att), "n_benign": len(ben), "arms": M, "paired_vs_A0": diffs,
           "decision_reachability_A0_vs_A6": dict(reach), "episode_level_ml_effect": ep_change,
           "calibration_offline": calibration(data, fits), "replay_errors": sum(1 for r in res if r[4])}
    (OUT / "results" / "ablation_results.json").write_text(json.dumps(out, indent=1, default=float))
    with (OUT / "03_ABLATION_RESULTS.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for a in ARMS:
        m = M[a]
        print(a, m["attack_successes"], m["benign_completed"], m["all_tasks_completed"], m["legitimate_released"], "/", m["legitimate_calls"],
              round(m["latency_ms_median"], 3), flush=True)
    print("reach", dict(reach), ep_change)


if __name__ == "__main__":
    main()
