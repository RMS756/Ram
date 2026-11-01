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


def architecture():
    """REM runtime architecture as implemented (five layers; offline fitting cross-cutting)."""
    from matplotlib.patches import FancyBboxPatch

    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.set_xlim(0, 100), ax.set_ylim(0, 60), ax.axis("off")

    def box(x, y, w, h, title, body="", fill="#eef4fc", edge=BLUE, ls="-"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    fc=fill, ec=edge, lw=1.3, ls=ls))
        ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="top", fontsize=8.5, weight="bold", color=INK)
        if body:
            ax.text(x + w / 2, y + h - 6.2, body, ha="center", va="top", fontsize=6.8, color=INK2, linespacing=1.35)

    def arrow(x1, y1, x2, y2, ls="-"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.1, ls=ls))

    box(2, 47, 26, 10, "LLM agent (unmodified)", "proposes tool call a_t\nreceives tool results", fill="#f4f3f0", edge=INK2)
    box(72, 47, 26, 10, "Tool environment", "AgentDojo banking sandbox\n(simulated accounts)", fill="#f4f3f0", edge=INK2)
    ax.text(50, 58.5, "REM sits at the tool-execution boundary (guarded ToolsExecutor)", ha="center", fontsize=8, color=INK2)
    # R4 (review of 1 Nov 2026): Layers 2 and 3 are drawn as two independent branches from
    # Layer 1 into Layer 4. They are independent computations (neither uses the other's
    # output); the implementation evaluates them one after the other, not concurrently.
    box(2, 22, 18, 19, "1 Input & Context",
        "provenance labels\ninvisible-char removal\n(analysis copy only)\nentity extraction")
    box(25, 30.5, 18, 10, "2 Detection", "x_ctx2 instruction patterns\n(x_ctx1 classifier: absent)")
    box(25, 17, 18, 10.5, "3 Behavioral Analysis", "x_beh1-4 history\nx_act1-3 action evidence")
    ax.text(34, 28.9, "independent computations; run in sequence", ha="center", va="center", fontsize=6, color=INK2)
    box(48, 22, 20, 19, "4 Decision Engine", "ridge LR: s_t\nPlatt on logit: p_t\ntier k_t, D1/D2\nargmin expected loss")
    box(73, 22, 20, 19, "5 Mitigation",
        "Allow / Modify /\nEscalate / Block\n(step-level reference;\nepisode-level variant)")
    arrow(20.2, 34, 24.8, 35.5)
    arrow(20.2, 29, 24.8, 23)
    arrow(43.2, 35.5, 47.8, 34)
    arrow(43.2, 23, 47.8, 29)
    arrow(68.2, 31.5, 72.8, 31.5)
    arrow(15, 47, 10, 41.5)
    arrow(85, 41.5, 85, 47)
    ax.text(87, 44, "released\ncalls only", fontsize=6.5, color=INK2, ha="left")
    arrow(80, 44.6, 24, 44.6, ls=(0, (2, 2)))
    ax.text(52, 45.6, "tool results return to the agent and enter Layer 1 as untrusted context", fontsize=6.5, color=INK2, ha="center")
    box(52, 2, 46, 13, "Audit record (append-only, per step)",
        "x_t, s_t, p_t, k_t, risk table or 'not applicable' (D1/D2), verdict + source,\n"
        "mitigation, tool name + argument digest; linear attribution (audit-only,\ncomputed after the verdict, cannot reach it)",
        fill="#fbfbf9", edge=INK2)
    box(2, 2, 47, 13, "Offline fitting & recalibration (not at runtime)",
        "grouped cross-fitting: lambda, beta, Platt (gamma_1>0), B1 thresholds,\n"
        "benign transition set, x-bar, r_mod(k); optional CUSUM (observe-only,\nnever in the verdict path)",
        fill="#fdf1ec", edge=ORANGE, ls=(0, (4, 2)))
    arrow(40, 15.4, 56, 21.5, ls=(0, (4, 2)))
    arrow(83, 21.5, 83, 15.4)
    # no EXPLORATORY stamp: this is the design diagram, not a result
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    fig.savefig(os.path.join(FIG, "fig_architecture.png"), dpi=200)


if __name__ == "__main__":
    reliability()
    enforcement()
    architecture()
    print(os.listdir(FIG))
