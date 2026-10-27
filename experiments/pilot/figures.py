"""Figures for the EXPLORATORY pilot (static PNG, light surface)."""

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from common import LABEL, RESULTS  # noqa: E402

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
FIG = os.path.join(RESULTS, "figures")
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "figure.facecolor": SURF, "axes.facecolor": SURF})


def load(name):
    with open(os.path.join(RESULTS, name), encoding="utf-8") as fh:
        return json.load(fh)


def stamp(fig):
    fig.text(0.01, 0.005, LABEL, fontsize=6.5, color=INK2)


def reliability():
    d = load("e1_crossfit.json")["label_nll_primary"]
    fig, ax = plt.subplots(figsize=(4.2, 4.0))
    ax.plot([0, 1], [0, 1], color=INK2, lw=1, ls=(0, (3, 3)))
    for key, color, name in (("reliability", BLUE, "Calibrated p (label-NLL Platt)"),
                             ("reliability_uncalibrated", ORANGE, "Uncalibrated sigma(s)")):
        rows = [r for r in d[key] if r["count"] > 0]
        ax.plot([r["mean_p"] for r in rows], [r["positive_rate"] for r in rows], color=color, lw=2,
                marker="o", ms=4, label=name, markeredgecolor=SURF, markeredgewidth=1)
    ax.set_xlabel("Mean predicted probability (bin)")
    ax.set_ylabel("Observed positive rate (bin)")
    ax.set_xlim(0, 1), ax.set_ylim(0, 1)
    ax.grid(color=GRID, lw=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper left")
    ax.set_title("Held-out reliability, 10 equal-width bins", color=INK, fontsize=10)
    stamp(fig)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(FIG, "fig_reliability.png"), dpi=200)


def enforcement():
    d = load("e4_e5_enforcement_replay.json")["configs"]
    rows = [("B0 no defense", "B0"), ("B1 step, no reviewer", "B1_step_level_no_reviewer"),
            ("B1 episode, no reviewer", "B1_episode_level_no_reviewer"),
            ("REM step, no reviewer", "REM_step_level_no_reviewer"),
            ("REM episode, no reviewer", "REM_episode_level_no_reviewer"),
            ("REM step, idealized reviewer", "REM_step_level_idealized"),
            ("REM episode, idealized reviewer", "REM_episode_level_idealized")]
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.4), sharey=True)
    for ax, metric, title in ((axes[0], "ASR", "Attack success rate"), (axes[1], "benign_utility", "Benign utility")):
        for i, (name, key) in enumerate(rows):
            pt, lo, hi = d[key][metric]
            ax.plot([lo, hi], [i, i], color=BLUE, lw=2, solid_capstyle="round")
            ax.plot([pt], [i], "o", color=BLUE, ms=6, markeredgecolor=SURF, markeredgewidth=1.5)
            ax.text(hi + 0.02, i, f"{pt:.3f}", va="center", fontsize=8, color=INK)
        ax.set_xlim(0, 1)
        ax.set_title(title, color=INK, fontsize=10)
        ax.grid(axis="x", color=GRID, lw=0.6)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_yticks(range(len(rows)), [r[0] for r in rows])
    axes[0].invert_yaxis()
    fig.suptitle("Enforcement replay (NO-ADAPT), point and 95% grouped-bootstrap interval", fontsize=9.5, color=INK2)
    stamp(fig)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(FIG, "fig_enforcement_replay.png"), dpi=200)


if __name__ == "__main__":
    reliability()
    enforcement()
    print(os.listdir(FIG))
