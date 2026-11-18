"""Figure of the controlled study, generated only from results/ablation_results.json and results/scripted_closed_loop.json."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

D = Path(__file__).resolve().parents[2] / "REM_IMPROVEMENT_CONTROLLED_STUDY_2026_11_18"


def main():
    r = json.load(open(D / "results" / "ablation_results.json"))
    arms = ["B0", "GV_math2", "C1", "C1_noledger", "C1I", "C1L", "C1IL", "PG"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, pop in zip(axes, ("primary_S1", "dev2")):
        m = r["populations"][pop]["metrics"]
        pts = {}
        for a in arms:                                   # arms with identical results share one point and one label
            x = m[a]["attack_objectives_reached"] / m[a]["n_attacked"]
            y = m[a]["all_tasks_completed"] / (m[a]["n_attacked"] + m[a]["n_benign"])
            pts.setdefault((x, y), []).append(a)
        for (x, y), names in pts.items():
            ax.scatter(x, y, s=40)
            ax.annotate(" = ".join(names), (x, y), textcoords="offset points", xytext=(5, 3), fontsize=8)
        ax.set_title(f"{pop}: offline replay (NO-ADAPT)")
        ax.set_xlabel("attack objectives reached / attacked episodes")
        ax.set_ylabel("tasks completed / all episodes")
        ax.grid(alpha=0.3)
    fig.suptitle("Controlled study 18 Nov 2026 - development evidence, not independent validation", fontsize=10)
    fig.tight_layout()
    out = D / "results" / "security_utility_replay.png"
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    main()
