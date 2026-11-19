"""Analysis of a LIVE REM vs MELON run (protocol 06). Endpoints, paired grouped-bootstrap intervals, McNemar
sensitivity, per-injection-task ASR, cost/latency, figures. All numbers come from <run_dir>/episodes.jsonl.

Refuses to label anything as a live result unless the run's manifest says "LIVE RUN"; with --diagnostic it may be
pointed at the scripted pilot to test the code path, and every output is then stamped SCRIPTED-DIAGNOSTIC.

usage: python3 experiments/rem_vs_melon/analyze_live.py <run_dir> <out_dir> [--diagnostic]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys

import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO)
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402

KW = dict(resamples=2000, seed=20261027, level=0.95)
ARMS = ["D0_NO_DEFENSE", "D1_REM", "D2_MELON"]


def mcnemar(b, c):
    from math import comb
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--diagnostic", action="store_true")
    a = ap.parse_args()
    man = json.load(open(os.path.join(a.run_dir, "manifest.json")))
    live = "LIVE RUN" in str(man.get("status", ""))
    if not live and not a.diagnostic:
        sys.exit("run is not a LIVE RUN; use --diagnostic to exercise the code on scripted output")
    stamp = "LIVE RUN" if live else "SCRIPTED-DIAGNOSTIC (not a result)"
    os.makedirs(a.out_dir, exist_ok=True)
    rows = [json.loads(l) for l in open(os.path.join(a.run_dir, "episodes.jsonl"))]
    key = lambda r: (r["user_task"], r["injection_task"], r.get("repeat", 0))    # noqa: E731
    by = {}
    for r in rows:
        by.setdefault(key(r), {})[r["arm"]] = r
    complete = {k: v for k, v in by.items() if set(ARMS) <= set(v) and all(v[x]["error"] is None for x in ARMS)}
    att = [k for k in complete if k[1]]
    ben = [k for k in complete if not k[1]]
    inj = lambda k: k[1]    # noqa: E731
    usr = lambda k: k[0]    # noqa: E731
    out = {"status": stamp, "triples_total": len(by), "triples_complete_no_error": len(complete),
           "errors_by_arm": {x: sum(1 for r in rows if r["arm"] == x and r["error"]) for x in ARMS}, "arms": {}, "paired": {}}
    csvrows = []
    for x in ARMS:
        A = [complete[k][x] for k in att]
        B = [complete[k][x] for k in ben]
        lat = [v for k in complete for v in complete[k][x].get("rem_latency_ms", [])]
        m = {"attacked": len(A), "attack_successes": sum(r["security"] for r in A),
             "ASR": grouped_bootstrap(att, inj, lambda s: float(np.mean([complete[k][x]["security"] for k in s])), **KW) if att else None,
             "utility_under_attack": sum(r["utility"] for r in A),
             "benign": len(B), "benign_completed": sum(r["utility"] for r in B),
             "benign_utility": grouped_bootstrap(ben, usr, lambda s: float(np.mean([complete[k][x]["utility"] for k in s])), **KW) if ben else None,
             "false_positive_interventions_benign": sum(1 for r in B if r.get("calls_refused_by_rem") or r.get("melon_flagged")),
             "rem_refusals_benign_calls": sum(r.get("calls_refused_by_rem") or 0 for r in B),
             "agent_llm_calls": sum(r["llm_calls_agent"] for k in complete for r in [complete[k][x]]),
             "melon_masked_calls": sum(r["llm_calls_melon_masked"] for k in complete for r in [complete[k][x]]),
             "embedding_calls": sum(r["embedding_calls"] for k in complete for r in [complete[k][x]]),
             "episode_wall_s_median": float(np.median([complete[k][x]["wall_time_s"] for k in complete])) if complete else None,
             "melon_overhead_s_median": float(np.median([complete[k][x]["llm_seconds_melon_masked"] + complete[k][x]["embedding_seconds"] for k in complete])) if complete else None,
             "rem_latency_ms_median": float(np.median(lat)) if lat else None,
             "rem_latency_ms_p95": float(np.percentile(lat, 95)) if lat else None,
             "cost_usd": sum(complete[k][x].get("cost_usd", 0) or 0 for k in complete),
             "asr_by_injection_task": {i: sum(complete[k][x]["security"] for k in att if k[1] == i) for i in sorted({k[1] for k in att})}}
        out["arms"][x] = m
        csvrows.append({"status": stamp, "arm": x, "attacked": m["attacked"], "attack_successes": m["attack_successes"],
                        "ASR": m["ASR"][0] if m["ASR"] else None, "ASR_lo": m["ASR"][1] if m["ASR"] else None,
                        "ASR_hi": m["ASR"][2] if m["ASR"] else None, "utility_under_attack": m["utility_under_attack"],
                        "benign": m["benign"], "benign_completed": m["benign_completed"],
                        "false_positive_interventions_benign": m["false_positive_interventions_benign"],
                        "agent_llm_calls": m["agent_llm_calls"], "melon_masked_calls": m["melon_masked_calls"],
                        "embedding_calls": m["embedding_calls"], "cost_usd": m["cost_usd"],
                        "rem_latency_ms_median": m["rem_latency_ms_median"], "rem_latency_ms_p95": m["rem_latency_ms_p95"]})
    for p, q in (("D1_REM", "D2_MELON"), ("D1_REM", "D0_NO_DEFENSE"), ("D2_MELON", "D0_NO_DEFENSE")):
        b = sum(1 for k in att if complete[k][p]["security"] and not complete[k][q]["security"])
        c = sum(1 for k in att if complete[k][q]["security"] and not complete[k][p]["security"])
        bu = sum(1 for k in ben if complete[k][p]["utility"] and not complete[k][q]["utility"])
        cu = sum(1 for k in ben if complete[k][q]["utility"] and not complete[k][p]["utility"])
        out["paired"][f"{p} minus {q}"] = {
            "ASR": grouped_bootstrap(att, inj, lambda s: float(np.mean([complete[k][p]["security"] - complete[k][q]["security"] for k in s])), **KW) if att else None,
            "benign_utility": grouped_bootstrap(ben, usr, lambda s: float(np.mean([complete[k][p]["utility"] - complete[k][q]["utility"] for k in s])), **KW) if ben else None,
            "attacks_discordant": [b, c], "mcnemar_p_attacks_ignoring_clustering": mcnemar(b, c),
            "benign_discordant": [bu, cu], "mcnemar_p_benign_ignoring_clustering": mcnemar(bu, cu)}
    json.dump(out, open(os.path.join(a.out_dir, "rem_melon_results.json"), "w"), indent=1, default=float)
    with open(os.path.join(a.out_dir, "rem_melon_results.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(csvrows[0]))
        w.writeheader()
        w.writerows(csvrows)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        col = {"D0_NO_DEFENSE": "#8a8986", "D1_REM": "#eb6834", "D2_MELON": "#2a78d6"}
        fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.2))
        for ax, key_, title in ((axs[0], "ASR", "Attack success rate (%)"), (axs[1], "benign_utility", "Benign utility (%)")):
            for j, x in enumerate(ARMS):
                v = out["arms"][x][key_]
                if v:
                    ax.plot([v[1] * 100, v[2] * 100], [j, j], color=col[x], lw=2)
                    ax.plot(v[0] * 100, j, "o", color=col[x], ms=7, mec="white")
            ax.set_yticks(range(3))
            ax.set_yticklabels(ARMS)
            ax.set_title(title, fontsize=9, loc="left")
            ax.set_xlim(-2, 102)
        fig.text(0, -0.05, f"{stamp}. 95% grouped-bootstrap intervals. Paired triples: {len(complete)}.", fontsize=7)
        fig.savefig(os.path.join(a.out_dir, "fig_rem_melon_asr_utility.png"), dpi=200, bbox_inches="tight")
    except Exception as exc:  # noqa: BLE001
        print("figure skipped:", exc)
    print(json.dumps({k: out[k] for k in ("status", "triples_total", "triples_complete_no_error", "errors_by_arm")}))


if __name__ == "__main__":
    main()
