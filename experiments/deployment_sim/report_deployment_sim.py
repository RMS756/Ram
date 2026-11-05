"""Tables (Markdown) and one figure from a deployment-simulation run's summary.json. No value is recomputed
except formatting; thesis replay reference values are read from results/pilot_R2/e4_e5_enforcement_replay.json.

usage: python3 experiments/deployment_sim/report_deployment_sim.py results/deployment_sim/<run_id>
"""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KEY = {"B0": "B0", "B1": "B1_step_level_no_reviewer", "REM": "REM_step_level_no_reviewer"}


def f(x, n=3):
    return "—" if x is None else f"{x:.{n}f}"


def main(run):
    s = json.load(open(os.path.join(run, "summary.json")))
    ref = json.load(open(os.path.join(REPO, "results", "pilot_R2", "e4_e5_enforcement_replay.json")))["configs"]
    L = ["# Deployment simulation — results", "", f"Run: `{run}`; REM commit `{s['manifest']['rem_commit'][:7]}`; "
         f"{s['manifest']['episodes']} recorded episodes; {s['manifest']['cpu_count']} vCPU; main concurrency "
         f"{s['manifest']['concurrency_main']}.", "", "## 1. Parity with the thesis's in-process replay", "",
         "| Configuration | Episodes compared | Mismatches (utility / security / error / per-call verdicts) |", "|---|---:|---|"]
    for c, p in s["parity_with_offline_replay"].items():
        m = p["mismatches"]
        L.append(f"| {c} | {p['episodes_compared']} | {m.get('utility', 0)} / {m.get('security', 0)} / "
                 f"{m.get('error_status', 0)} / {m.get('verdict_sequence', 0)} |")
    L += ["", "## 2. Outcomes (valid episodes; NO-ADAPT)", "",
          "| Configuration | ASR (deployed) | ASR (thesis §4.6) | Utility under attack | Benign utility |", "|---|---:|---:|---:|---:|"]
    for c, o in s["outcomes_valid_episodes"].items():
        L.append(f"| {c} | {f(o['ASR'])} | {f(ref[KEY[c]]['ASR'][0])} | {f(o['utility_under_attack'])} | {f(o['benign_utility'])} |")
    L += ["", "## 3. Latency and throughput (main run)", "",
          "| Configuration | Episodes/s | Calls | REM time per call, median / p95 (ms) | Turn round trip, median / p95 (ms) | Backend per executed call, median (ms) | Errors |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for c, r in s["configs"].items():
        la = r["latency"]
        L.append(f"| {c} | {r['episodes_per_s']:.1f} | {la['calls']} | {f(la['rem_ms_per_call']['median'], 2)} / "
                 f"{f(la['rem_ms_per_call']['p95'], 2)} | {f(la['batch_rtt_ms']['median'], 1)} / {f(la['batch_rtt_ms']['p95'], 1)} | "
                 f"{f(la['backend_ms_per_executed_call']['median'], 2)} | {r['errors']} |")
    L += ["", "## 4. Concurrency sweep (REM; same 400 episodes)", "",
          "| Concurrent episodes | Episodes/s | Calls/s | Turn round trip median / p95 (ms) | REM time per call median / p95 (ms) | Errors |",
          "|---:|---:|---:|---:|---:|---:|"]
    xs, thr, p95 = [], [], []
    for c, r in sorted(s["sweep"].items(), key=lambda kv: int(kv[0])):
        la = r["latency"]
        xs.append(int(c)); thr.append(r["calls_per_s"]); p95.append(la["batch_rtt_ms"]["p95"])
        L.append(f"| {c} | {r['episodes_per_s']:.1f} | {r['calls_per_s']:.1f} | {f(la['batch_rtt_ms']['median'], 1)} / "
                 f"{f(la['batch_rtt_ms']['p95'], 1)} | {f(la['rem_ms_per_call']['median'], 2)} / {f(la['rem_ms_per_call']['p95'], 2)} | {r['errors']} |")
    a = s["audit_checks"]
    L += ["", "## 5. Audit completeness and enforcement", "",
          f"- Episodes: {a['episodes']}; calls released: {a['released_calls']}; calls withheld: {a['withheld_calls']}.",
          f"- Calls executed by the backend: {a['backend_executed_calls']}; episodes where the backend log differs from the released calls: "
          f"{a.get('episodes_released_ne_executed', 0)}.",
          "", "## 6. Fail-closed probes", ""] + [f"- {k}: {v}" for k, v in s["fail_closed_probes"].items()]
    L += ["", f"Gateway counters: `{json.dumps(s.get('gateway_counters', {}))}`; gateway start-up (loading frozen components): "
          f"{s['manifest']['gateway_startup_s']:.0f} s."]
    open(os.path.join(run, "RESULTS.md"), "w").write("\n".join(L) + "\n")
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(xs, thr, marker="o", color="#1f4e79"); ax[0].set_xlabel("concurrent episodes"); ax[0].set_ylabel("tool calls per second")
    ax[0].set_title("Throughput (REM gateway)", fontsize=10)
    ax[1].plot(xs, p95, marker="o", color="#a33"); ax[1].set_xlabel("concurrent episodes"); ax[1].set_ylabel("ms")
    ax[1].set_title("Agent-turn round trip, 95th percentile", fontsize=10)
    for x in ax:
        x.grid(alpha=.3); x.set_xscale("log", base=2); x.set_xticks(xs); x.set_xticklabels(xs)
    fig.tight_layout(); fig.savefig(os.path.join(run, "concurrency_sweep.png"), dpi=300)
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1])
