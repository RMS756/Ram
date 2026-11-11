"""Metrics, grouped bootstrap and tables for the authorization-generalization study (protocol 06, sections 7-10).

usage: PILOT_RESULTS_DIR=<dir> AUTHZ_STATE=<dir> python3 experiments/authz_study/analyze.py
Writes JSON files to REM_Authorization_Generalization_Study/results/.
"""
from __future__ import annotations

import collections
import json
import os
import sys
from types import SimpleNamespace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import study as S  # noqa: E402
from study import BOOT, CFG, SEED, common, grouped_bootstrap, rm  # noqa: E402
from data import build, load_raw  # noqa: E402
from rem.integration.agentdojo_traces import ReferenceSolutions  # noqa: E402

CAT = {t: c for c, ts in CFG["consequence"]["categories"].items() for t in ts}
KW = dict(resamples=BOOT["resamples"], seed=SEED, level=BOOT["interval"])
HEADLINE = ["B0", "B1", "M00", "P1", "P2", "A1", "A2", "M01", "M10", "M11", "M11y", "M00+AZ", "M11+AZ"]
POSTHOC = ["M00_nobeh"]
PRIMARY_CONTRASTS = [("M11+AZ", "M00"), ("M11+AZ", "P1")]
EXPLORATORY_CONTRASTS = [("M11+AZ", "M11"), ("M11+AZ", "M00+AZ"), ("M11", "M00"), ("M01", "M00"), ("M10", "M00"),
                         ("M00+AZ", "M00"), ("P1", "M00"), ("A1", "P1"), ("A1", "M00"), ("M11y", "M11"), ("M11+AZ", "B1"),
                         ("M11", "P1"), ("P1", "B1"),
                         # added after results were seen (exploratory, post hoc): rule baselines against the original REM
                         ("P2", "M00"), ("A2", "M00"), ("A2", "P1"), ("M01", "P1"), ("M11y", "M00"),
                         # POST HOC A-2: the original study's existing no-behaviour ablation
                         ("M00_nobeh", "M00"), ("M00_nobeh", "P1"), ("M00_nobeh", "P2"), ("M00_nobeh", "A2"), ("M11+AZ", "M00_nobeh")]


def ci(items, key, stat):
    p, lo, hi = grouped_bootstrap(items, key, stat, **KW)
    return [p, lo, hi]


def arm_metrics(by, arm, att, ben, data, restricted, user_tools):
    sec = {e: by[e][arm][1] for e in att}
    uti = {e: by[e][arm][0] for e in att + ben}
    inj = lambda e: data.episodes[e].injection_task_id
    usr = lambda e: data.episodes[e].user_task_id
    uscr = {e: any(a[0] == 1 and a[2] for a in by[e][arm][3]) for e in att}
    # authorized (benign-episode) restricted calls
    calls = [(e, a) for e in ben for a in by[e][arm][3] if a[4] in restricted]
    calls_ref = [(e, a) for e, a in calls if a[4] in user_tools[usr(e)]]
    pos = [(e, a) for e in att for a in by[e][arm][3] if a[0] == 1]
    lat = [a[5] for e in att + ben for a in by[e][arm][3]]
    cat = collections.Counter()
    for e, a in calls:
        cat[("benign_call", CAT.get(a[4], "other"), bool(a[2]))] += 1
    for e, a in pos:
        cat[("attack_call", CAT.get(a[4], "other"), bool(a[2]))] += 1
    reads = [(e, a) for e in ben for a in by[e][arm][3] if CAT.get(a[4]) == "read"]
    m = {
        "attacks_successful": int(sum(sec.values())), "n_attacked": len(att),
        "benign_successful": int(sum(uti[e] for e in ben)), "n_benign": len(ben),
        "utility_under_attack_successes": int(sum(uti[e] for e in att)),
        "uscr_episodes": int(sum(uscr.values())),
        "ASR": ci(att, inj, lambda s: float(np.mean([sec[e] for e in s]))),
        "benign_utility": ci(ben, usr, lambda s: float(np.mean([uti[e] for e in s]))),
        "utility_under_attack": ci(att, inj, lambda s: float(np.mean([uti[e] for e in s]))),
        "USCR": ci(att, inj, lambda s: float(np.mean([uscr[e] for e in s]))),
        "AAR_released": int(sum(1 for _, a in calls if a[2])), "AAR_n": len(calls),
        "AAR": ci(calls, lambda x: usr(x[0]), lambda s: float(np.mean([x[1][2] for x in s]))) if calls else None,
        "AARref_released": int(sum(1 for _, a in calls_ref if a[2])), "AARref_n": len(calls_ref),
        "escalated_authorized_calls": int(sum(1 for _, a in calls if a[1] == "escalate")),
        "attack_calls_withheld": int(sum(1 for _, a in pos if not a[2])), "attack_calls_n": len(pos),
        "benign_reads_released": int(sum(1 for _, a in reads if a[2])), "benign_reads_n": len(reads),
        "by_category": [{"kind": k[0], "category": k[1], "released": k[2], "n": n} for k, n in sorted(cat.items())],
        "verdicts_on_authorized_calls": dict(collections.Counter(a[1] for _, a in calls)),
        "ties": int(sum(1 for e in att + ben for a in by[e][arm][3] if a[7])),
        "replay_errors": int(sum(1 for e in att + ben if by[e][arm][2])),
        "decision_ms_median": float(np.median(lat)) if lat else None,
        "decision_ms_p95": float(np.percentile(lat, 95)) if lat else None,
    }
    return m


def paired(by, a, b, att, ben, data):
    inj = lambda e: data.episodes[e].injection_task_id
    usr = lambda e: data.episodes[e].user_task_id
    uscr = lambda e, arm: any(x[0] == 1 and x[2] for x in by[e][arm][3])
    return {
        "ASR_diff": ci(att, inj, lambda s: float(np.mean([by[e][a][1] - by[e][b][1] for e in s]))),
        "benign_utility_diff": ci(ben, usr, lambda s: float(np.mean([by[e][a][0] - by[e][b][0] for e in s]))),
        "utility_under_attack_diff": ci(att, inj, lambda s: float(np.mean([by[e][a][0] - by[e][b][0] for e in s]))),
        "USCR_diff": ci(att, inj, lambda s: float(np.mean([uscr(e, a) - uscr(e, b) for e in s]))),
        "benign_discordant": [int(sum(1 for e in ben if by[e][a][0] and not by[e][b][0])),
                              int(sum(1 for e in ben if by[e][b][0] and not by[e][a][0]))],
        "attack_discordant": [int(sum(1 for e in att if by[e][a][1] and not by[e][b][1])),
                              int(sum(1 for e in att if by[e][b][1] and not by[e][a][1]))],
    }


def pareto(M, arms):
    pts = {a: (M[a]["ASR"][0], M[a]["benign_utility"][0]) for a in arms}
    nd = []
    for a, (asr, bu) in pts.items():
        if not any((o_asr <= asr and o_bu >= bu) and (o_asr < asr or o_bu > bu) for o, (o_asr, o_bu) in pts.items() if o != a):
            nd.append(a)
    return {"points": {a: {"ASR": v[0], "benign_utility": v[1]} for a, v in pts.items()}, "non_dominated": sorted(nd)}


def main():
    os.makedirs(S.OUT, exist_ok=True)
    st = common.make_setup()
    raw = load_raw()
    data = build("primary", raw)
    xt = build("cross_template", raw)
    aux = S.load("fit_aux")
    valid = aux["valid"]
    res = S.load("replay")
    if os.path.exists(os.path.join(S.STATE, "replay_posthoc_a1.pkl")):
        res = res + S.load("replay_posthoc_a1")       # POST HOC amendment A-1 (S2 run of one S1 ablation arm)
    if os.path.exists(os.path.join(S.STATE, "replay_posthoc_a2.pkl")):
        res = res + S.load("replay_posthoc_a2")       # POST HOC amendment A-2 (existing no-behaviour ablation of the original REM)
    refsol = ReferenceSolutions.from_agentdojo(CFG["data"]["suite_version_for_replay"], CFG["data"]["suite"])
    user_tools = {u: {c.function for c in calls} for u, calls in refsol.user.items()}
    restricted = set(st.restricted)
    B = collections.defaultdict(lambda: collections.defaultdict(dict))
    for scheme, role, eid, arm, u, s, err, aud in res:
        B[(scheme, role)][eid][arm] = (u, s, err, aud)
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    out = {"provenance": common.provenance(), "evaluation_mode": "offline recorded-trace replay, step level, no reviewer, NO-ADAPT",
           "n_attacked": len(att), "n_benign": len(ben)}

    # --- branch-outcome labels and authorization evidence: descriptive statistics --------------
    T, Z = aux["T"], aux["Z"]
    y = T["y"]
    ev = np.array([s.episode_id in set(valid) for s in data.steps])
    R = np.array([s.tool in restricted for s in data.steps])
    benign_step = ~data.attacked
    desc = {"targets_positive_counts_all_steps": {k: int(v.sum()) for k, v in T.items()},
            "alignment": aux["align_stats"],
            "y_vs_a": [[int(((y == i) & (T["a"] == j)).sum()) for j in (0, 1)] for i in (0, 1)],
            "y_vs_b": [[int(((y == i) & (T["b"] == j)).sum()) for j in (0, 1)] for i in (0, 1)],
            "authz_on_restricted_calls": {}}
    for name, mask in (("benign_episode_calls", ev & R & benign_step), ("attack_calls_y1", ev & R & (y == 1)),
                       ("attacked_episode_legit_calls_y0", ev & R & ~benign_step & (y == 0))):
        desc["authz_on_restricted_calls"][name] = {
            "n": int(mask.sum()), "z_exp": int(Z[mask, 0].sum()), "z_del": int(Z[mask, 1].sum()),
            "neither": int(((Z[mask, 0] == 0) & (Z[mask, 1] == 0)).sum())}
    per_ut = collections.defaultdict(lambda: collections.Counter())
    for i in np.flatnonzero(ev & R & benign_step):
        per_ut[data.steps[i].user_task_id]["z_exp" if Z[i, 0] else "z_del" if Z[i, 1] else "neither"] += 1
    desc["authz_benign_calls_by_user_task"] = {k: dict(v) for k, v in sorted(per_ut.items())}
    out["labels_and_evidence"] = desc

    # --- model-level metrics on held-out predictions -------------------------------------------
    mm = {}
    for scheme in ("S1", "S2"):
        mm[scheme] = {}
        for (fs, t), (pc, pr) in aux["heldout"][scheme].items():
            if fs not in ("F0", "F1") or t in ("am", "bm"):
                continue
            ok = ~np.isnan(pc)
            if ok.sum() == 0 or T[t][ok].sum() == 0:
                continue
            mm[scheme][f"{fs}|{t}"] = {"calibrated": rm.prob_metrics(T[t][ok], pc[ok]), "uncalibrated": rm.prob_metrics(T[t][ok], pr[ok])}
    out["model_metrics_heldout"] = mm

    # --- S1 / S2 enforcement replay -----------------------------------------------------------
    for scheme in ("S1", "S2"):
        by = B[(scheme, "primary")]
        arms = sorted({a for e in valid for a in by[e]})
        M = {a: arm_metrics(by, a, att, ben, data, restricted, user_tools) for a in arms}
        block = {"arms": M,
                 "primary_contrasts": {f"{a} minus {b}": paired(by, a, b, att, ben, data) for a, b in PRIMARY_CONTRASTS},
                 "exploratory_contrasts": {f"{a} minus {b}": paired(by, a, b, att, ben, data) for a, b in EXPLORATORY_CONTRASTS},
                 "pareto_headline": pareto(M, HEADLINE),
                 "pareto_including_posthoc": pareto(M, HEADLINE + [a for a in POSTHOC if a in M])}
        if scheme == "S1":
            block["ablation_contrasts_exploratory"] = {f"M11+AZ minus {a}": paired(by, "M11+AZ", a, att, ben, data)
                                                       for a in S.ABL_ARMS}
        # sensitivity: without user_task_15
        att2 = [e for e in att if data.episodes[e].user_task_id != "user_task_15"]
        ben2 = [e for e in ben if data.episodes[e].user_task_id != "user_task_15"]
        block["sensitivity_without_user_task_15"] = {
            a: {"attacks_successful": int(sum(by[e][a][1] for e in att2)), "n_attacked": len(att2),
                "benign_successful": int(sum(by[e][a][0] for e in ben2)), "n_benign": len(ben2),
                "uscr_episodes": int(sum(1 for e in att2 if any(x[0] == 1 and x[2] for x in by[e][a][3])))}
            for a in HEADLINE + [x for x in POSTHOC if x in M]}
        block["benign_success_by_user_task"] = {
            a: {u: [int(sum(by[e][a][0] for e in ben if data.episodes[e].user_task_id == u)),
                    int(sum(1 for e in ben if data.episodes[e].user_task_id == u))]
                for u in sorted({data.episodes[e].user_task_id for e in ben}, key=lambda s: int(s.split("_")[-1]))}
            for a in ("B0", "M00", "P1", "A1", "A2", "M01", "M11", "M11+AZ", "M00_nobeh") if a in M}
        block["attack_success_by_injection_task"] = {
            a: {i: [int(sum(by[e][a][1] for e in att if data.episodes[e].injection_task_id == i)),
                    int(sum(1 for e in att if data.episodes[e].injection_task_id == i))]
                for i in sorted({data.episodes[e].injection_task_id for e in att})}
            for a in ("B0", "M00", "P1", "A1", "A2", "M01", "M11", "M11+AZ", "M00_nobeh") if a in M}
        out[scheme] = block

    # --- S3 cross-template ---------------------------------------------------------------------
    by = B[("S1", "cross_template")]
    xv = [e for e in sorted(xt.episodes) if by[e]["B0"][0] == xt.episodes[e].utility and by[e]["B0"][1] == xt.episodes[e].security
          and by[e]["B0"][2] is None]
    s3 = {"episodes": len(xt.episodes), "replay_valid": len(xv), "arms": {}, "by_template": {}}
    for a in sorted({k for e in xv for k in by[e]}):
        s3["arms"][a] = {"attacks_successful": int(sum(by[e][a][1] for e in xv)),
                         "utility_under_attack_successes": int(sum(by[e][a][0] for e in xv)),
                         "uscr_episodes": int(sum(1 for e in xv if any(x[0] == 1 and x[2] for x in by[e][a][3]))),
                         "n": len(xv),
                         "ASR": ci(xv, lambda e: xt.episodes[e].injection_task_id, lambda s, a=a: float(np.mean([by[e][a][1] for e in s]))),
                         "utility_under_attack": ci(xv, lambda e: xt.episodes[e].injection_task_id,
                                                    lambda s, a=a: float(np.mean([by[e][a][0] for e in s])))}
    for t in sorted({xt.episodes[e].attack_type for e in xv}):
        ee = [e for e in xv if xt.episodes[e].attack_type == t]
        s3["by_template"][t] = {a: [int(sum(by[e][a][1] for e in ee)), int(sum(by[e][a][0] for e in ee)), len(ee)]
                                for a in ("B0", "B1", "M00", "P1", "A1", "A2", "M11", "M11+AZ", "M00_nobeh") if a in by[ee[0]]}
    out["S3_cross_template"] = s3

    # --- reformatted-identifier probe ----------------------------------------------------------
    by = B[("S1", "probe_iban")]
    by1 = B[("S1", "primary")]
    pe = sorted(by)
    pv = [e for e in pe if by[e]["B0"][0] == data.episodes[e].utility and by[e]["B0"][1] == data.episodes[e].security]
    pr = {"episodes": len(pe), "B0_still_reproduces_record": len(pv), "arms": {}}
    for a in sorted({k for e in pv for k in by[e]}):
        pr["arms"][a] = {"attacks_successful_reformatted": int(sum(by[e][a][1] for e in pv)),
                         "attacks_successful_original_text": int(sum(by1[e][a][1] for e in pv)),
                         "uscr_reformatted": int(sum(1 for e in pv if any(x[0] == 1 and x[2] for x in by[e][a][3]))),
                         "uscr_original_text": int(sum(1 for e in pv if any(x[0] == 1 and x[2] for x in by1[e][a][3]))),
                         "utility_under_attack_reformatted": int(sum(by[e][a][0] for e in pv)), "n": len(pv)}
    out["probe_reformatted_iban"] = pr

    # --- cost-ratio frontier -------------------------------------------------------------------
    fr = {}
    for scheme in ("S1", "S2"):
        M = out[scheme]["arms"]
        fr[scheme] = {a: {"attacks_successful": M[a]["attacks_successful"], "benign_successful": M[a]["benign_successful"],
                          "uscr_episodes": M[a]["uscr_episodes"], "AAR_released": M[a]["AAR_released"], "AAR_n": M[a]["AAR_n"]}
                      for a in M if a.startswith("M11")}
    out["cost_ratio_frontier"] = fr

    # --- fixtures (call-level probes; counts only) ---------------------------------------------
    out["fixtures"] = fixtures(st)
    if os.path.exists(os.path.join(S.STATE, "memory_kib.pkl")):
        out["memory"] = S.load("memory_kib")
    out["posthoc_A1_note"] = ("S2 results of arm M11+AZ_noact were computed AFTER results were seen (amendment A-1); "
                              "exploratory, not a candidate.")
    with open(os.path.join(S.OUT, "study_results.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=common._default)
    brief(out)


def fixtures(st):
    sys.path.insert(0, os.path.join(S.REPO, "REM_AUTHORIZATION_AUDIT", "tools"))
    import trace_fixtures as tf
    cells = S.load("cells")
    cell = cells[("S1", "injection_task_0")]
    arms = ["B0", "B1", "M00", "P1", "P2", "A1", "A2", "M01", "M10", "M11", "M11y", "M00+AZ", "M11+AZ"]
    if os.path.exists(os.path.join(S.STATE, "cells_posthoc_a2.pkl")):
        cell["models"].update(S.load("cells_posthoc_a2")[("S1", "injection_task_0")]["models"])
        arms.append("M00_nobeh")
    rows = []
    for fx in tf.load_fixtures():
        for arm in arms:
            rec = {"fixture": fx["id"], "set": fx["set"], "kind": fx["kind"], "arm": arm}
            for role in ("legitimate", "unsafe"):
                ep = SimpleNamespace(objective=fx["objective"], system_prompt=tf.SYSTEM_PROMPT, injection_task_id=None, episode_id="fixture")
                g = S.make_guard(arm, cell, ep, st)
                g.begin_decision_point()
                g.evaluate("read_file", {"file_path": "document.txt"})
                g.ingest("read_file", fx["tool_output"], executed=True)
                g.begin_decision_point()
                call = fx[f"{role}_call"]
                g.evaluate(call["tool"], dict(call["args"]))
                a = g.audit[-1]
                rec[f"{role}_verdict"], rec[f"{role}_released"] = a["verdict"], bool(a["released"])
                rec[f"{role}_z"] = list(a["details"].get("z", ()))
            rows.append(rec)
    summ = {}
    for arm in arms:
        rr = [r for r in rows if r["arm"] == arm]
        pay = [r for r in rr if r["kind"] != "read_only_converted_to_payment"]
        ro = [r for r in rr if r["kind"] == "read_only_converted_to_payment"]
        summ[arm] = {"legit_payments_released": sum(r["legitimate_released"] for r in pay), "n_payment_fixtures": len(pay),
                     "substituted_payments_released": sum(r["unsafe_released"] for r in pay),
                     "both_correct_payment_pairs": sum(r["legitimate_released"] and not r["unsafe_released"] for r in pay),
                     "read_only_legit_read_released": sum(r["legitimate_released"] for r in ro), "n_read_only_fixtures": len(ro),
                     "read_only_unrequested_payment_released": sum(r["unsafe_released"] for r in ro),
                     "unsafe_released_ids": [r["fixture"] for r in rr if r["unsafe_released"]]}
    return {"summary": summ, "rows": rows}


def brief(out):
    for scheme in ("S1", "S2"):
        print(f"--- {scheme}")
        for a in HEADLINE + [x for x in POSTHOC if x in out[scheme]["arms"]]:
            m = out[scheme]["arms"][a]
            print(f"{a:8s} atk {m['attacks_successful']:4d}/{m['n_attacked']} ben {m['benign_successful']:3d}/{m['n_benign']} "
                  f"UA {m['utility_under_attack_successes']:4d} USCR {m['uscr_episodes']:4d} AAR {m['AAR_released']:3d}/{m['AAR_n']} "
                  f"atkcalls withheld {m['attack_calls_withheld']}/{m['attack_calls_n']} ms {m['decision_ms_median']:.3f}")
        for k, v in out[scheme]["primary_contrasts"].items():
            print(" PRIMARY", k, "BU", [round(x, 4) for x in v["benign_utility_diff"]], "ASR", [round(x, 4) for x in v["ASR_diff"]],
                  "USCR", [round(x, 4) for x in v["USCR_diff"]])
        print(" pareto", out[scheme]["pareto_headline"]["non_dominated"])


if __name__ == "__main__":
    main()
