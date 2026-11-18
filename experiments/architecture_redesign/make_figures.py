"""Figures generated only from results/architecture_results.json and results/suites_summary.json."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

D = Path(__file__).resolve().parents[2] / "REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18"
ARMS = ["C1", "C1I", "PG", "REM_A", "REM_B", "REM_C"]


def main():
    r = json.load(open(D / "results" / "architecture_results.json"))
    s = json.load(open(D / "results" / "suites_summary.json"))
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.4))
    for ax, pop in zip(axes, ("primary_S1", "dev2", "heldout_H")):
        m = r["populations"][pop]["metrics"]
        for a in ARMS:
            x = m[a]["audited_value_or_object_violations_released"]
            y = m[a]["all_tasks_completed"] / (m[a]["n_attacked"] + m[a]["n_benign"])
            ax.scatter(x, y, s=45)
            ax.annotate(a, (x, y), textcoords="offset points", xytext=(5, 3), fontsize=8)
        ax.set_title(f"{pop}\n(replay, NO-ADAPT; 0 attacks for every arm shown)", fontsize=10)
        ax.set_xlabel("audited value/object violations released")
        ax.set_ylabel("tasks completed / episodes")
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(D / "figures" / "utility_vs_audited_violations.png", dpi=150)
    fig, ax = plt.subplots(figsize=(9, 4))
    suites = ["ledger_dev", "heldout_probes", "diagnostics", "generalization"]
    w = 0.13
    for i, a in enumerate(ARMS):
        vals = [s[k][a]["unauthorized_released"] + s[k][a]["ambiguous_released"] for k in suites]
        ax.bar([j + i * w for j in range(len(suites))], vals, width=w, label=a)
    ax.set_xticks([j + w * 2.5 for j in range(len(suites))])
    ax.set_xticklabels(suites)
    ax.set_ylabel("unauthorized + ambiguous proposals released")
    ax.set_title("Author-written suites (labels fixed before the runs)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(D / "figures" / "suite_violations.png", dpi=150)
    print("ok")


if __name__ == "__main__":
    main()
