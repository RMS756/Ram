"""REM component ablation study (protocol: REM_ABLATION_STUDY/01_ABLATION_PROTOCOL.md). OFFLINE REPLAY ONLY.

Frozen REM v1.0 (rem/ at 9fddfa7) and the frozen pilot pipeline (experiments/pilot at ea621c3) are imported, never
edited. Fitted state comes from a fresh run of the frozen pilot pipeline into $PILOT_RESULTS_DIR. Every arm is an
experimental configuration of the existing replay harness; REM's files are untouched.

Arms (all: step-level mitigation, no reviewer, identical recorded episodes, identical fold assignment):
  B0     no defence (reference)
  A0     full REM v1.0
  A1a    Detection evidence removed from the estimator: x_ctx2 dropped (refit, existing pilot fit 'no_ctx');
         x_beh1, which is computed in the Behavioural layer from the same pattern detector, is kept
  A1b    Detection layer disabled: x_ctx2 AND x_beh1 dropped (x_beh1 is defined through x_ctx2 = 1, so it cannot exist
         without the detector); NEW refit with the frozen nested cross-fitting procedure, nothing else changed
  A2     Behavioural evidence removed (x_beh1..x_beh4; refit 'no_beh')
  AIC    Input & Context provenance evidence removed from the estimator (x_act1..x_act3; refit 'no_act'); the
         deterministic predicate D2 keeps reading the availability of x_act1 (it is a policy control, not a feature)
  A3     learned decision bypassed: predicates D1/D2 only, every other call released; no scorer is evaluated
  A3P    deterministic controls removed (learned decision only; predicates D1/D2 disabled)  [complement of A3]
  A4     mitigation in SHADOW mode: every verdict of full REM is computed and logged, every call is released
Populations:
  P1  primary (scheme S1: outer fold = held-out attacker objective), 3,313 eligible episodes
  P2  cross-template: gpt-4o with five attack templates never used in fitting (attacked only)
  P3  second population: unseen backbones and templates (sources F-A..F-E of the 11 Nov confirmatory run)
Outputs: REM_ABLATION_STUDY/results/ablation_raw.pkl (per-call audit), results/ablation_metrics.json,
         04_RESULTS.csv, 05_EPISODE_RESULTS.jsonl
"""
from __future__ import annotations

import collections
import csv
import json
import math
import os
import pickle
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "pilot"))
import run_main as RM  # noqa: E402  (frozen pilot pipeline; reads PILOT_RESULTS_DIR)
from data import build, load_raw, reference_from_mask  # noqa: E402
from rem.algorithms.behavior.evidence import FEATURE_ORDER  # noqa: E402
from rem.algorithms.calibration.logit_nll import LabelNLLLogitCalibrator  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402
from rem.integration.agentdojo_traces import ambiguous_pairs, iter_episode_paths, load_episode  # noqa: E402
from rem.evaluation.crossfit import assign_round_robin  # noqa: E402

OUT = ROOT / "REM_ABLATION_STUDY"
V, E2 = "step_level", "no_reviewer"
KW = dict(resamples=RM.B["resamples"], seed=RM.SEED, level=RM.B["interval"])
ARMS = ["B0", "A0", "A1a", "A1b", "A2", "AIC", "A3", "A3P", "A4"]
ORDER_A1B = tuple(f for f in FEATURE_ORDER if f not in ("x_ctx2", "x_beh1"))
SECOND_SOURCES = {   # identical to experiments/authz_study/confirm_a.py SOURCES (11 Nov protocol section 3)
    "F-A": ("Meta-SecAlign-70B", ["important_instructions", "direct", "ignore_previous"], True),
    "F-B": ("Meta-SecAlign-70B-repeat_user_prompt", ["important_instructions", "direct", "ignore_previous"], True),
    "F-C": ("meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt", ["direct", "ignore_previous", "important_instructions"], True),
    "F-D": ("meta-llama_Llama-3.3-70B-Instruct", ["direct", "ignore_previous"], False),
    "F-E": ("gpt-4o-2024-05-13", ["important_instructions_no_model_name", "important_instructions_no_user_name",
                                  "important_instructions_wrong_model_name", "important_instructions_wrong_user_name"], False),
}
FITS = {}


def _decide_predicates_only(f):
    P = RM.predicates()

    def decide(c):
        o = P.evaluate(c.tool, c.tier, c.available)
        return (o.verdict, o.source, {}) if o.verdict is not None else (Verdict.ALLOW, "no_learned_allow", {})
    return decide


def _scorer_a1b(f):
    return RM.scorer_of(FITS["no_ctx_beh1"].fits[f], ORDER_A1B, True)


def configs():
    base = RM.replay_configs()
    rem = base[f"REM_{V}_{E2}"]
    return {
        "B0": base["B0"], "A0": rem,
        "A1a": base[f"abl_no_ctx_{V}_{E2}"],
        "A1b": {"variant": V, "esc": E2, "decide": RM._mk_decide(f"A3_{V}"), "scorer": _scorer_a1b},
        "A2": base[f"abl_no_beh_{V}_{E2}"],
        "AIC": base[f"abl_no_act_{V}_{E2}"],
        "A3": {"variant": V, "esc": E2, "decide": _decide_predicates_only},          # no scorer: learned path bypassed
        "A3P": base[f"abl_no_predicates_{V}_{E2}"],
        "A4": {**rem, "observe_only": True},                                         # shadow mode (release everything)
    }


def load_second(st, folds, rr):
    """Second population, loaded exactly as the 11 Nov confirmatory run did (AM-1 and error exclusions)."""
    amb = ambiguous_pairs(st.labeler)
    eps, meta = {}, {}
    for src, (pipe, attacks, benign) in SECOND_SOURCES.items():
        for attack in attacks + (["none"] if benign else []):
            for path in iter_episode_paths(os.environ.get("AGENTDOJO_RUNS", "/home/user/ethz-spylab/agentdojo/runs"),
                                           pipe, RM.CFG["data"]["suite"], attack):
                ep = load_episode(path, pipeline=pipe)
                if ep.error and RM.CFG["data"]["exclude_errored_episodes"]:
                    continue
                if ep.injection_task_id and ((ep.user_task_id, ep.injection_task_id) in amb or ep.injection_task_id not in folds):
                    continue
                if ep.user_task_id not in rr:
                    continue
                eid = f"{src}|{ep.episode_id}"
                eps[eid] = ep
                meta[eid] = folds[rr[ep.user_task_id]] if not ep.injection_task_id else ep.injection_task_id
    return SimpleNamespace(episodes=eps, episode_fold=meta)


def hygiene_exercised(populations):
    """Count tool-output segments whose text would be changed by the Input & Context hygiene step."""
    from rem.algorithms.context.provenance import strip_invisible
    n = changed = 0
    for name, data, eids in populations:
        for e in eids:
            for m in data.episodes[e].raw_messages:
                if m.get("role") == "tool":
                    c = m.get("content")
                    t = c if isinstance(c, str) else "".join(str(b.get("content", "")) for b in (c or []) if isinstance(b, dict))
                    n += 1
                    changed += int(strip_invisible(t) != t)
    return {"tool_output_segments": n, "segments_changed_by_hygiene": changed}


def mcnemar(b, c):
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def call_rate(items, by, arm, pred_calls, pred_num):
    """Pooled call-level rate over resampled episode clusters: sum(num)/sum(den); None if no denominator."""
    den = sum(1 for e in items for x in by[e][arm][3] if pred_calls(e, x))
    if den == 0:
        return float("nan")
    return sum(1 for e in items for x in by[e][arm][3] if pred_calls(e, x) and pred_num(x)) / den


def analyse(pop, data, by, valid, restricted):
    eps = data.episodes
    att = [e for e in valid if eps[e].injection_task_id]
    ben = [e for e in valid if not eps[e].injection_task_id]
    inj = lambda e: eps[e].injection_task_id    # noqa: E731
    usr = lambda e: eps[e].user_task_id         # noqa: E731
    atk_call = lambda e, x: x[4] in restricted and x[0] == 1                       # noqa: E731
    ben_call = lambda e, x: x[4] in restricted and not eps[e].injection_task_id   # noqa: E731
    oth_call = lambda e, x: x[4] in restricted and x[0] != 1 and bool(eps[e].injection_task_id)  # noqa: E731
    withheld = lambda x: not x[2]               # noqa: E731
    M, D = {}, {}
    for a in ARMS:
        calls = [x for e in valid for x in by[e][a][3]]
        rr = [x for x in calls if x[4] in restricted]
        tp = sum(1 for e in valid for x in by[e][a][3] if atk_call(e, x) and withheld(x))
        fp = sum(1 for e in valid for x in by[e][a][3] if x[4] in restricted and x[0] != 1 and withheld(x))
        fn = sum(1 for e in valid for x in by[e][a][3] if atk_call(e, x) and not withheld(x))
        vc = collections.Counter(str(x[1]).lower() for x in rr)
        m = {"episodes_attacked": len(att), "episodes_benign": len(ben),
             "restricted_calls": len(rr),
             "attack_labelled_calls": sum(1 for e in valid for x in by[e][a][3] if atk_call(e, x)),
             "attack_labelled_withheld": tp,
             "attack_call_withholding_rate": grouped_bootstrap(att, inj, lambda s: call_rate(s, by, a, atk_call, withheld), **KW) if att else None,
             "benign_episode_restricted_calls": sum(1 for e in ben for x in by[e][a][3] if x[4] in restricted),
             "benign_episode_calls_withheld": sum(1 for e in ben for x in by[e][a][3] if x[4] in restricted and withheld(x)),
             "benign_call_blocking_rate": grouped_bootstrap(ben, usr, lambda s: call_rate(s, by, a, ben_call, withheld), **KW) if ben else None,
             "unlabelled_calls_in_attacked_episodes": sum(1 for e in att for x in by[e][a][3] if oth_call(e, x)),
             "unlabelled_calls_in_attacked_episodes_withheld": sum(1 for e in att for x in by[e][a][3] if oth_call(e, x) and withheld(x)),
             "withhold_precision": tp / (tp + fp) if tp + fp else None, "withhold_recall": tp / (tp + fn) if tp + fn else None,
             "verdicts_restricted": {k: vc.get(k, 0) for k in ("allow", "modify", "escalate", "block")},
             "verdicts_would_withhold": sum(1 for x in rr if str(x[1]).lower() != "allow"),
             "replay_attack_outcomes": int(sum(by[e][a][1] for e in att)),
             "replay_attack_outcome_rate": grouped_bootstrap(att, inj, lambda s: float(np.mean([by[e][a][1] for e in s])), **KW) if att else None,
             "replay_benign_completed": int(sum(by[e][a][0] for e in ben)),
             "replay_benign_completion_rate": grouped_bootstrap(ben, usr, lambda s: float(np.mean([by[e][a][0] for e in s])), **KW) if ben else None,
             "replay_tasks_under_attack": int(sum(by[e][a][0] for e in att)),
             "latency_full_ms_median": float(np.median([x[8] for x in calls])), "latency_full_ms_p95": float(np.percentile([x[8] for x in calls], 95)),
             "latency_full_ms_mean": float(np.mean([x[8] for x in calls])),
             "latency_partial_ms_median": float(np.median([x[5] for x in calls])), "latency_partial_ms_p95": float(np.percentile([x[5] for x in calls], 95)),
             "calls_timed": len(calls)}
        M[a] = m
    for a in ARMS:
        if a == "A0":
            continue
        rel_chg = collections.Counter()
        verd_chg = 0
        diff_len = 0
        for e in valid:
            x0, xa = by[e]["A0"][3], by[e][a][3]
            if len(x0) != len(xa):
                diff_len += 1
                continue
            for c0, ca in zip(x0, xa):
                if str(c0[1]).lower() != str(ca[1]).lower():
                    verd_chg += 1
                if c0[2] != ca[2]:
                    kind = "attack_labelled" if c0[0] == 1 else ("benign_episode" if not eps[e].injection_task_id else "unlabelled_in_attacked_episode")
                    rel_chg[f"{kind}:{'A0_withheld_arm_released' if not c0[2] else 'A0_released_arm_withheld'}"] += 1
        b = sum(1 for e in att if by[e][a][1] and not by[e]["A0"][1])
        c = sum(1 for e in att if by[e]["A0"][1] and not by[e][a][1])
        bu = sum(1 for e in ben if by[e][a][0] and not by[e]["A0"][0])
        cu = sum(1 for e in ben if by[e]["A0"][0] and not by[e][a][0])
        D[a] = {"call_verdict_changes_vs_A0": verd_chg, "call_release_changes_vs_A0": dict(rel_chg),
                "episodes_with_different_call_count": diff_len,
                "d_attack_call_withholding_rate": grouped_bootstrap(att, inj, lambda s: call_rate(s, by, a, atk_call, withheld) - call_rate(s, by, "A0", atk_call, withheld), **KW) if att else None,
                "d_benign_call_blocking_rate": grouped_bootstrap(ben, usr, lambda s: call_rate(s, by, a, ben_call, withheld) - call_rate(s, by, "A0", ben_call, withheld), **KW) if ben else None,
                "d_replay_attack_outcome_rate": grouped_bootstrap(att, inj, lambda s: float(np.mean([by[e][a][1] - by[e]["A0"][1] for e in s])), **KW) if att else None,
                "d_replay_benign_completion_rate": grouped_bootstrap(ben, usr, lambda s: float(np.mean([by[e][a][0] - by[e]["A0"][0] for e in s])), **KW) if ben else None,
                "attack_outcome_discordant_arm_only_A0_only": [b, c], "mcnemar_p_attack_outcome": mcnemar(b, c),
                "benign_completion_discordant_arm_only_A0_only": [bu, cu], "mcnemar_p_benign_completion": mcnemar(bu, cu)}
    # shadow mode: verdict agreement with enforced full REM at identical call positions
    agree = tot = first_div = 0
    for e in valid:
        x0, x4 = by[e]["A0"][3], by[e]["A4"][3]
        diverged = False
        for c0, c4 in zip(x0, x4):
            tot += 1
            if str(c0[1]).lower() == str(c4[1]).lower():
                agree += 1
            elif not diverged:
                diverged = True
                first_div += 1
    shadow = {"calls_compared": tot, "verdict_agreement_with_enforced": agree, "episodes_with_a_divergence": first_div,
              "calls_executed_while_shadow_verdict_would_withhold": sum(1 for e in valid for x in by[e]["A4"][3]
                                                                         if x[4] in restricted and str(x[1]).lower() != "allow" and x[2]),
              "shadow_attack_labelled_calls_flagged": sum(1 for e in att for x in by[e]["A4"][3] if x[0] == 1 and str(x[1]).lower() != "allow"),
              "shadow_attack_labelled_calls": sum(1 for e in att for x in by[e]["A4"][3] if x[0] == 1)}
    return {"population": pop, "episodes_valid": len(valid), "attacked": len(att), "benign": len(ben),
            "arms": M, "paired_vs_A0": D, "shadow_mode": shadow}


def main():
    t_start = time.time()
    raw = load_raw()
    prim = build("primary", raw)
    fits = RM.load_state("crossfit")
    rm = RM.load_state("rmod")
    folds = sorted(set(prim.fold.tolist()), key=str)
    # NEW refit for A1b: frozen nested cross-fitting, frozen calibrator, only the feature order differs
    t0 = time.time()
    FITS["no_ctx_beh1"] = RM.run_crossfit(prim, ORDER_A1B, LabelNLLLogitCalibrator)
    refit_s = time.time() - t0
    ok = ~np.isnan(FITS["no_ctx_beh1"].p_cal)
    from rem.evaluation.probabilistic import average_precision, roc_auc
    a1b_fit = {"features": ORDER_A1B, "roc_auc": roc_auc(prim.y[ok], FITS["no_ctx_beh1"].p_cal[ok]),
               "pr_auc": average_precision(prim.y[ok], FITS["no_ctx_beh1"].p_cal[ok]), "seconds": refit_s}
    pol = RM.build_policies(fits, rm["rmod"])
    refs = {f: reference_from_mask(prim, prim.fold != f) for f in folds}
    RM.G.update(policies=pol, fits=fits)
    C = configs()
    st = RM.make_setup()
    restricted = set(st.restricted)
    users = sorted({e.user_task_id for e in prim.episodes.values()}, key=str)
    rr = assign_round_robin(users, len(folds))
    xt = build("cross_template", raw)
    xt.episode_fold = {e: xt.episodes[e].injection_task_id for e in xt.episodes}
    second = load_second(st, folds, rr)
    pops = [("P1_primary", prim, sorted(e for e, ok_ in rm["agree"].items() if ok_)),
            ("P2_cross_template", xt, sorted(xt.episodes)),
            ("P3_second_population", second, sorted(second.episodes))]
    out = {"status": "OFFLINE RECORDED-TRACE REPLAY (NO-ADAPT), protocol REM_ABLATION_STUDY/01_ABLATION_PROTOCOL.md; no model call",
           "a1b_refit": a1b_fit, "hygiene_check": hygiene_exercised([(n, d, e) for n, d, e in pops]), "populations": {}}
    raw_out = {}
    for name, data, eids in pops:
        t0 = time.time()
        res = RM.run_replays(C, eids, st, data, refs)
        by = collections.defaultdict(dict)
        for eid, c, u, s, err, aud in res:
            by[eid][c] = (u, s, err, aud)
        if name == "P1_primary":
            valid = [e for e in eids if all(by[e][a][2] is None for a in ARMS)]
        else:       # AM-4: the no-defence replay reproduces the recorded outcome
            valid = [e for e in eids if all(by[e][a][2] is None for a in ARMS)
                     and (bool(by[e]["B0"][0]), bool(by[e]["B0"][1])) == (bool(data.episodes[e].utility), bool(data.episodes[e].security))]
        r = analyse(name, data, by, valid, restricted)
        r["loaded"] = len(eids)
        r["replay_errors"] = sum(1 for x in res if x[4])
        r["seconds"] = time.time() - t0
        out["populations"][name] = r
        raw_out[name] = {"by": {e: by[e] for e in valid},
                         "meta": {e: (data.episodes[e].user_task_id, data.episodes[e].injection_task_id,
                                      data.episodes[e].pipeline, data.episodes[e].attack_type) for e in valid}}
        print(name, "valid", len(valid), "of", len(eids), {a: r["arms"][a]["attack_labelled_withheld"] for a in ARMS}, flush=True)
    out["wall_seconds"] = time.time() - t_start
    (OUT / "results").mkdir(parents=True, exist_ok=True)
    (OUT / "results" / "ablation_metrics.json").write_text(json.dumps(out, indent=1, default=float))
    with open(os.path.join(RM.STATE, "ablation_study_raw.pkl"), "wb") as fh:
        pickle.dump(raw_out, fh)
    write_outputs(out, raw_out)


def write_outputs(out, raw_out):
    rows = []
    for pop, r in out["populations"].items():
        for a in ARMS:
            m = r["arms"][a]
            d = r["paired_vs_A0"].get(a, {})
            g = lambda v, i=0: (v[i] if isinstance(v, (list, tuple)) and v[0] is not None else None)   # noqa: E731
            rows.append({"population": pop, "arm": a, "episodes_attacked": m["episodes_attacked"], "episodes_benign": m["episodes_benign"],
                         "attack_labelled_calls": m["attack_labelled_calls"], "attack_labelled_withheld": m["attack_labelled_withheld"],
                         "attack_call_withholding_rate": g(m["attack_call_withholding_rate"]),
                         "attack_call_withholding_lo": g(m["attack_call_withholding_rate"], 1), "attack_call_withholding_hi": g(m["attack_call_withholding_rate"], 2),
                         "benign_episode_restricted_calls": m["benign_episode_restricted_calls"], "benign_episode_calls_withheld": m["benign_episode_calls_withheld"],
                         "benign_call_blocking_rate": g(m["benign_call_blocking_rate"]),
                         "benign_call_blocking_lo": g(m["benign_call_blocking_rate"], 1), "benign_call_blocking_hi": g(m["benign_call_blocking_rate"], 2),
                         "withhold_precision": m["withhold_precision"], "withhold_recall": m["withhold_recall"],
                         "replay_attack_outcomes_NOADAPT": m["replay_attack_outcomes"], "replay_benign_completed_NOADAPT": m["replay_benign_completed"],
                         "call_release_changes_vs_A0": sum(d.get("call_release_changes_vs_A0", {}).values()) if d else 0,
                         "latency_full_ms_median": m["latency_full_ms_median"], "latency_full_ms_p95": m["latency_full_ms_p95"],
                         "calls_timed": m["calls_timed"]})
    with open(OUT / "04_RESULTS.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "05_EPISODE_RESULTS.jsonl", "w") as fh:
        for pop, R in raw_out.items():
            for e, arms in R["by"].items():
                u_, i_, p_, t_ = R["meta"][e]
                for a in ARMS:
                    ut, sec, err, aud = arms[a]
                    fh.write(json.dumps({"population": pop, "episode": e, "user_task": u_, "injection_task": i_, "backbone": p_, "attack": t_,
                                         "arm": a, "replay_utility": bool(ut), "replay_attack_outcome": bool(sec) if i_ else None,
                                         "calls": [[x[4], str(x[1]).lower(), bool(x[2]), int(x[0]), x[7]] for x in aud]}) + "\n")


if __name__ == "__main__":
    main()
