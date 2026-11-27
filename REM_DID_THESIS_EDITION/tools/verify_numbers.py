"""Independent recomputation of every ablation and comparison number used in the defence-ready thesis.

Reads only RAW per-episode / per-call records (never a summary table) and writes audit/number_verification.json.
Sources (all committed):
  S19  REM_FINAL_THESIS_COMPLETION_2026_11_19/results/raw/ablation_episodes.csv.gz, ablation_calls.csv.gz (19 Nov 2026)
  S19x REM_FINAL_THESIS_COMPLETION_2026_11_19/results/raw/external_episodes.csv.gz (REM replay on distributed-defence traces)
  S21  REM_ABLATION_STUDY/05_EPISODE_RESULTS.jsonl.gz (21 Nov 2026)
  S22  REM_COMPARATIVE_EVALUATION_PHASE/results/offline_comparison_episodes.jsonl.gz (22 Nov 2026)
  REC  ethz-spylab/agentdojo@089ed468 runs/gpt-4o-2024-05-13[-defence]/banking (recorded closed-loop runs)
  REF  REM_EXTERNAL_DEFENSE_AUDIT/results/itest_progent.json (Progent on reference solutions, per task)
  SCR  REM_COMPARATIVE_EVALUATION_PHASE/results/drift_scripted_integration.json, d0_d1_d2_scripted_integration.json
"""
import collections
import csv
import gzip
import io
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402

KW = dict(resamples=2000, seed=20261027, level=0.95)
RESTRICTED = {"send_money", "schedule_transaction", "update_scheduled_transaction", "update_user_info", "update_password"}
RUNS = Path(os.environ.get("AGENTDOJO_RUNS", "/home/user/ethz-spylab/agentdojo/runs"))
OUT = ROOT / "REM_DEFENCE_READY_THESIS" / "audit" / "number_verification.json"


def mcnemar(b, c):
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def paired(items, cl, f_arm, f_ref):
    x = sum(1 for k in items if f_arm(k) and not f_ref(k))
    y = sum(1 for k in items if f_ref(k) and not f_arm(k))
    d = grouped_bootstrap(items, cl, lambda s: float(np.mean([f_arm(k) - f_ref(k) for k in s])), **KW)
    return {"arm_only": x, "ref_only": y, "mcnemar_p": mcnemar(x, y), "diff_pp": [round(v * 100, 2) for v in d]}


def rate(items, cl, f):
    d = grouped_bootstrap(items, cl, lambda s: float(np.mean([f(k) for k in s])), **KW)
    return [round(v * 100, 2) for v in d]


# ---------------------------------------------------------------- S21 (21 Nov): episode-level, all populations
def s21():
    E = collections.defaultdict(dict)
    meta = {}
    for line in gzip.open(ROOT / "REM_ABLATION_STUDY/05_EPISODE_RESULTS.jsonl.gz", "rt"):
        r = json.loads(line)
        rc = [c for c in r["calls"] if c[0] in RESTRICTED]
        E[(r["population"], r["episode"])][r["arm"]] = {
            "u": bool(r["replay_utility"]), "s": bool(r["replay_attack_outcome"]),
            "acr": any(c[3] == 1 and c[2] for c in rc), "w": any(not c[2] for c in rc),
            "legit_rel": sum(1 for c in rc if c[2]), "legit_n": len(rc)}
        meta[(r["population"], r["episode"])] = (r["user_task"], r["injection_task"], r["backbone"])
    out = {}
    for pop in sorted({p for p, _ in E}):
        keys = [k for k in E if k[0] == pop]
        att = [k for k in keys if meta[k][1]]
        ben = [k for k in keys if not meta[k][1]]
        inj = lambda k: meta[k][1]  # noqa: E731
        usr = lambda k: meta[k][0]  # noqa: E731
        R = {"attacked": len(att), "benign": len(ben), "backbones": len({meta[k][2] for k in keys}),
             "user_tasks": len({meta[k][0] for k in keys}), "injection_tasks": len({meta[k][1] for k in att}), "arms": {}, "paired_vs_A0": {}}
        for a in ["B0", "A0", "A1a", "A1b", "A2", "AIC", "A3", "A3P", "A4"]:
            m = {"attacks": sum(E[k][a]["s"] for k in att), "attack_call_released_eps": sum(E[k][a]["acr"] for k in att),
                 "utility_under_attack": sum(E[k][a]["u"] for k in att)}
            if att:
                m["asr_pct"] = rate(att, inj, lambda k, a=a: E[k][a]["s"])
            if ben:
                m.update(benign_completed=sum(E[k][a]["u"] for k in ben), benign_fp_eps=sum(E[k][a]["w"] for k in ben),
                         benign_legit_calls_released=sum(E[k][a]["legit_rel"] for k in ben), benign_legit_calls=sum(E[k][a]["legit_n"] for k in ben),
                         benign_pct=rate(ben, usr, lambda k, a=a: E[k][a]["u"]), benign_fp_pct=rate(ben, usr, lambda k, a=a: E[k][a]["w"]))
            R["arms"][a] = m
            if a != "A0":
                d = {"attack": paired(att, inj, lambda k, a=a: E[k][a]["s"], lambda k: E[k]["A0"]["s"]),
                     "attack_call_released": paired(att, inj, lambda k, a=a: E[k][a]["acr"], lambda k: E[k]["A0"]["acr"]),
                     "utility_under_attack": paired(att, inj, lambda k, a=a: E[k][a]["u"], lambda k: E[k]["A0"]["u"])}
                if ben:
                    d["benign_completion"] = paired(ben, usr, lambda k, a=a: E[k][a]["u"], lambda k: E[k]["A0"]["u"])
                    d["benign_fp"] = paired(ben, usr, lambda k, a=a: E[k][a]["w"], lambda k: E[k]["A0"]["w"])
                R["paired_vs_A0"][a] = d
        R["A0_attacks_by_user_task"] = dict(collections.Counter(meta[k][0] for k in att if E[k]["A0"]["s"]))
        out[pop] = R
    return out, E, meta


# ---------------------------------------------------------------- S19 (19 Nov): Decision-engine sub-ablations
def s19(valid_p1):
    rows = list(csv.DictReader(io.TextIOWrapper(gzip.open(ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19/results/raw/ablation_episodes.csv.gz"))))
    E = collections.defaultdict(dict)
    for r in rows:
        E[r["episode_id"]][r["arm"]] = (r["utility"] == "1", r["security"] == "1")
    ids_all = sorted(E)
    ids = [e for e in ids_all if e in valid_p1]
    att = [e for e in ids if e.split("|")[2] != "none"]
    ben = [e for e in ids if e.split("|")[2] == "none"]
    inj = lambda e: e.split("|")[2]  # noqa: E731
    usr = lambda e: e.split("|")[1]  # noqa: E731
    out = {"episodes_in_file": len(ids_all), "episodes_in_valid_P1": len(ids), "attacked": len(att), "benign": len(ben), "arms": {}, "paired_vs_A0": {}}
    for a in sorted(next(iter(E.values()))):
        out["arms"][a] = {"attacks": sum(E[e][a][1] for e in att), "benign_completed": sum(E[e][a][0] for e in ben),
                          "all_tasks": sum(E[e][a][0] for e in ids)}
        if a != "A0":
            out["paired_vs_A0"][a] = {"attack": paired(att, inj, lambda e, a=a: E[e][a][1], lambda e: E[e]["A0"][1]),
                                      "benign_completion": paired(ben, usr, lambda e, a=a: E[e][a][0], lambda e: E[e]["A0"][0])}
    return out, E


def s19_calls(valid_p1, E19):
    """Call-level quantities of the 19-Nov arms on the valid primary episodes (from ablation_calls.csv.gz)."""
    C = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19/results/raw/ablation_calls.csv.gz"))):
        if r["set"] == "primary" and r["episode_id"] in valid_p1:
            C[r["arm"]][r["episode_id"]].append((r["tool"], r["label"] == "1", r["released"] == "True"))
    att = sorted(e for e in valid_p1 if e.split("|")[2] != "none")
    ben = sorted(e for e in valid_p1 if e.split("|")[2] == "none")
    out = {}
    for a in sorted(C):
        ce = C[a]
        rc = lambda e: [c for c in ce.get(e, []) if c[0] in RESTRICTED]  # noqa: E731
        out[a] = {"attack_call_released_eps": sum(any(c[1] and c[2] for c in rc(e)) for e in att),
                  "benign_fp_eps": sum(any(not c[2] for c in rc(e)) for e in ben),
                  "legit_released": sum(sum(1 for c in rc(e) if c[2]) for e in ben),
                  "legit_n": sum(len(rc(e)) for e in ben),
                  "utility_under_attack": sum(E19[e][a][0] for e in att),
                  "attack_calls_withheld": sum(sum(1 for c in rc(e) if c[1] and not c[2]) for e in att),
                  "attack_calls": sum(sum(1 for c in rc(e) if c[1]) for e in att)}
    # paired episode-level differences from A0 for the call-derived outcomes (same definitions as in s21)
    inj = lambda e: e.split("|")[2]  # noqa: E731
    usr = lambda e: e.split("|")[1]  # noqa: E731
    acr = {a: {e: any(c[1] and c[2] for c in C[a].get(e, []) if c[0] in RESTRICTED) for e in att} for a in C}
    fp = {a: {e: any(not c[2] for c in C[a].get(e, []) if c[0] in RESTRICTED) for e in ben} for a in C}
    for a in sorted(C):
        if a == "A0":
            continue
        out[a]["paired_vs_A0"] = {
            "attack_call_released": paired(att, inj, lambda e, a=a: acr[a][e], lambda e: acr["A0"][e]),
            "utility_under_attack": paired(att, inj, lambda e, a=a: E19[e][a][0], lambda e: E19[e]["A0"][0]),
            "benign_fp": paired(ben, usr, lambda e, a=a: fp[a][e], lambda e: fp["A0"][e])}
    return out


def recorded():
    res = {}
    for name in ["", "-repeat_user_prompt", "-spotlighting_with_delimiting", "-tool_filter", "-transformers_pi_detector"]:
        d = RUNS / f"gpt-4o-2024-05-13{name}" / "banking"
        att = [json.load(open(p)) for p in d.glob("user_task_*/important_instructions/injection_task_*.json")]
        ben = [json.load(open(p)) for p in d.glob("user_task_*/none/none.json")]
        res[name.strip("-") or "none"] = {"attacked_runs": len(att), "attack_successes": sum(bool(x["security"]) for x in att),
                                         "utility_under_attack": sum(bool(x["utility"]) for x in att),
                                         "benign_runs": len(ben), "benign_completed": sum(bool(x["utility"]) for x in ben),
                                         "errors": sum(1 for x in att + ben if x.get("error"))}
    return res


def s22():
    rows = [json.loads(l) for l in gzip.open(ROOT / "REM_COMPARATIVE_EVALUATION_PHASE/results/offline_comparison_episodes.jsonl.gz", "rt")]
    out = {}
    for pop in sorted({r["population"] for r in rows}):
        rs = [r for r in rows if r["population"] == pop]
        att = [r for r in rs if r["injection_task"]]
        ben = [r for r in rs if not r["injection_task"]]
        k_att = list(range(len(att)))
        k_ben = list(range(len(ben)))
        R = {"attacked": len(att), "benign": len(ben), "arms": {}, "paired": {}}
        for a in ("B0", "A0", "A3", "PG"):
            m = {"attacks": sum(r["arms"][a]["attack_outcome"] for r in att), "attack_call_released_eps": sum(r["arms"][a]["attack_call_released"] for r in att),
                 "utility_under_attack": sum(r["arms"][a]["utility"] for r in att)}
            if att:
                m["asr_pct"] = rate(k_att, lambda i: att[i]["injection_task"], lambda i, a=a: att[i]["arms"][a]["attack_outcome"])
            if ben:
                m.update(benign_completed=sum(r["arms"][a]["utility"] for r in ben), benign_fp_eps=sum(r["arms"][a]["any_restricted_withheld"] for r in ben),
                         benign_pct=rate(k_ben, lambda i: ben[i]["user_task"], lambda i, a=a: ben[i]["arms"][a]["utility"]))
            R["arms"][a] = m
        for a, b in (("A0", "B0"), ("PG", "B0"), ("A0", "PG"), ("A0", "A3")):
            d = {"attack": paired(k_att, lambda i: att[i]["injection_task"], lambda i: att[i]["arms"][a]["attack_outcome"], lambda i: att[i]["arms"][b]["attack_outcome"]),
                 "utility_under_attack": paired(k_att, lambda i: att[i]["injection_task"], lambda i: att[i]["arms"][a]["utility"], lambda i: att[i]["arms"][b]["utility"])}
            if ben:
                d["benign_completion"] = paired(k_ben, lambda i: ben[i]["user_task"], lambda i: ben[i]["arms"][a]["utility"], lambda i: ben[i]["arms"][b]["utility"])
            R["paired"][f"{a}-{b}"] = d
        R["A0_only_attack_user_tasks"] = dict(collections.Counter(r["user_task"] for r in att if r["arms"]["A0"]["attack_outcome"] and not r["arms"]["PG"]["attack_outcome"]))
        R["PG_benign_zero_tasks"] = sorted({r["user_task"] for r in ben} - {r["user_task"] for r in ben if r["arms"]["PG"]["utility"]})
        R["A0_benign_zero_tasks"] = sorted({r["user_task"] for r in ben} - {r["user_task"] for r in ben if r["arms"]["A0"]["utility"]})
        out[pop] = R
    return out, rows


def main():
    res = {}
    res["S21_episode_level_ablation"], E21, meta21 = s21()
    valid_p1 = {e for (p, e) in E21 if p == "P1_primary"}
    res["S19_decision_engine_subablations"], E19 = s19(valid_p1)
    res["S19_call_level_valid_P1"] = s19_calls(valid_p1, E19)
    # cross-study per-episode identity (same frozen state; same definitions)
    pairs = {"A0": "A0", "A6": "A3", "A1": "A2", "A4a": "A1a", "A4b": "AIC", "A7": "A3P", "B0": "B0"}
    cross = {}
    for a19, a21 in pairs.items():
        same = sum(1 for e in valid_p1 if (E19[e][a19][0], E19[e][a19][1] if meta21[("P1_primary", e)][1] else E21[("P1_primary", e)][a21]["s"])
                   == (E21[("P1_primary", e)][a21]["u"], E21[("P1_primary", e)][a21]["s"]))
        cross[f"{a19}(19Nov)=={a21}(21Nov)"] = [same, len(valid_p1)]
    res["cross_study_episode_identity"] = cross
    res["S22_offline_comparison"], rows22 = s22()
    ids22 = {(r["population"], r["episode"]) for r in rows22}
    res["S22_vs_S21_same_episode_sets"] = ids22 == set(E21)
    res["S22_vs_S21_shared_arms_identical"] = all(
        (r["arms"][a]["utility"], r["arms"][a]["attack_outcome"]) == (E21[(r["population"], r["episode"])][a]["u"],
                                                                      E21[(r["population"], r["episode"])][a]["s"] if r["injection_task"] else None)
        for r in rows22 for a in ("B0", "A0", "A3"))
    res["REC_recorded_closed_loop"] = recorded()
    ex = list(csv.DictReader(io.TextIOWrapper(gzip.open(ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19/results/raw/external_episodes.csv.gz"))))
    res["S19x_rem_replay_on_defence_traces_rows"] = dict(collections.Counter((r["set"], r["arm"]) for r in ex).items().__iter__()) if False else \
        {f"{k[0]}:{k[1]}": v for k, v in collections.Counter((r["set"], r["arm"]) for r in ex).items()}
    ref = json.load(open(ROOT / "REM_EXTERNAL_DEFENSE_AUDIT/results/itest_progent.json"))
    res["REF_progent_reference_solutions"] = {v: {"benign_with": sum(t["utility_with_progent"] for t in ref["versions"][v]["benign"].values()),
                                                  "benign_without": sum(t["utility_without_progent"] for t in ref["versions"][v]["benign"].values()),
                                                  "pairs_goal_with": sum(p[1] for p in ref["versions"][v]["pairs"].values()),
                                                  "pairs_goal_without": sum(p[0] for p in ref["versions"][v]["pairs"].values()),
                                                  "pairs": len(ref["versions"][v]["pairs"])} for v in ref["versions"]}
    drift = json.load(open(ROOT / "REM_COMPARATIVE_EVALUATION_PHASE/results/drift_scripted_integration.json"))
    eps = drift["episodes"]
    res["SCR_drift"] = {k: {"episodes": len([e for e in eps if f'{e["arm"]}:{e["setting"]}' == k]),
                            "errors": sum(1 for e in eps if f'{e["arm"]}:{e["setting"]}' == k and e.get("error")),
                            "model_calls_excl_privilege_per_episode": round(np.mean([sum(v for m, v in e["test_double_calls_by_drift_module"].items() if m != "privilege")
                                                                                       for e in eps if f'{e["arm"]}:{e["setting"]}' == k]), 2)}
                        for k in sorted({f'{e["arm"]}:{e["setting"]}' for e in eps})}
    scr = json.load(open(ROOT / "REM_COMPARATIVE_EVALUATION_PHASE/results/d0_d1_d2_scripted_integration.json"))
    res["SCR_d0_d1_d2"] = {a: {"episodes": sum(1 for e in scr["episodes"] if e["arm"] == a), "errors": sum(1 for e in scr["episodes"] if e["arm"] == a and e["error"])} for a in ("D0", "D1", "D2")}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps({k: res[k] for k in ("cross_study_episode_identity", "S22_vs_S21_same_episode_sets", "S22_vs_S21_shared_arms_identical",
                                          "REC_recorded_closed_loop", "REF_progent_reference_solutions", "SCR_drift", "SCR_d0_d1_d2")}, indent=1))


if __name__ == "__main__":
    main()
