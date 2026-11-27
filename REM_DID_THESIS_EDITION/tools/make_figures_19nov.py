"""Figures of the 19 November 2026 ablation (thesis Figures 4.6-4.8), redrawn with the variant labels of Table 4.25.

The plotted numbers are read from the same stored results as the original figures
(REM_FINAL_THESIS_COMPLETION_2026_11_19/results/ablation_results.json, written by experiments/final_thesis/) and are
cross-checked against the raw-record recomputation (audit/number_verification.json) before anything is drawn.
Only the display labels change. The mapping from the arms of the frozen protocol
(REM_FINAL_THESIS_COMPLETION_2026_11_19/02_FROZEN_ABLATION_PROTOCOL.md, "Arm | Change") to the variants of Table 4.25 is:
  A1 behavioural evidence removed -> A3a      A2 Platt calibration removed -> A4c
  A3 consequence-independent thresholds -> A4d   A4a context evidence removed -> A2a
  A4b action/provenance evidence removed -> A3b  A5 Modify removed -> A4e
  A6 learned decision removed -> A4a           A7 predicates removed -> A4b
The cross-study identity (audit/number_verification.json, cross_study_episode_identity) confirms A1=A2(21 Nov),
A4a=A1a, A4b=AIC, A6=A3 and A7=A3P on every one of the 3,313 episodes.

usage: python3 REM_DEFENCE_READY_THESIS/tools/make_figures_19nov.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

D = Path(__file__).resolve().parents[1]
ROOT = D.parent
A = json.loads((ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19/results/ablation_results.json").read_text())
V = json.loads((D / "audit" / "number_verification.json").read_text())
FIG = D / "figures"

# ---- guard: the stored summary must equal the raw-record recomputation
S19 = V["S19_decision_engine_subablations"]["arms"]
for a, m in A["arms"].items():
    assert m["attack_successes"] == S19[a]["attacks"], a
    assert m["benign_completed"] == S19[a]["benign_completed"], a
    assert m["all_tasks_completed"] == S19[a]["all_tasks"], a
assert A["episode_level_ml_effect"]["attacks_prevented_due_to_ml"] == V["S19_decision_engine_subablations"]["paired_vs_A0"]["A6"]["attack"]["arm_only"]

NEW = {"B0": "No defense", "A0": "Full REM v1.0", "A4a": "A2a − detection feature x_ctx2", "A1": "A3a − behavioral evidence",
       "A4b": "A3b − action/provenance evidence", "A6": "A4a − learned decision", "A7": "A4b − predicates D1/D2",
       "A2": "A4c − calibration", "A3": "A4d − thresholds instead of expected loss", "A5": "A4e − Modify verdict"}
ORDER = ["B0", "A0", "A4a", "A1", "A4b", "A6", "A7", "A2", "A3", "A5"]   # protocol keys, in the order of Table 4.25
BLUE, ORANGE, GRAY, INK, INK2, GRID = "#2a78d6", "#eb6834", "#8a8986", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "figure.facecolor": "white", "axes.facecolor": "white", "savefig.dpi": 300})


def col(a):
    return ORANGE if a == "A0" else (GRAY if a == "B0" else BLUE)


def save(fig, name):
    fig.savefig(FIG / name, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def fig_security_utility():
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.9), sharey=True)
    y = np.arange(len(ORDER))[::-1]
    for ax, key, title, n in ((axs[0], "ASR", "Attack outcomes (of 2,979 attacked episodes)", "attack_successes"),
                              (axs[1], "benign_utility", "Benign tasks completed (of 334)", "benign_completed")):
        for yi, a in zip(y, ORDER):
            m = A["arms"][a]
            v, lo, hi = m[key]
            ax.plot([lo * 100, hi * 100], [yi, yi], color=col(a), lw=2, solid_capstyle="round")
            ax.plot(v * 100, yi, "o", ms=6, color=col(a), mec="white", mew=1.2)
            ax.annotate(f"{m[n]}", (hi * 100, yi), xytext=(5, 0), textcoords="offset points", va="center", fontsize=7.5, color=INK2)
        ax.set_title(title, fontsize=9, color=INK, loc="left")
        ax.set_xlabel("% of episodes")
        ax.grid(axis="y", visible=False)
    axs[0].set_yticks(y)
    axs[0].set_yticklabels([NEW[a] for a in ORDER], fontsize=8)
    axs[0].set_xlim(-2, 40)
    axs[1].set_xlim(0, 80)
    fig.text(0, -0.05, "Dots: point estimates; bars: 95% grouped-bootstrap intervals (attack outcomes clustered by injection task, benign tasks\n"
             "by user task). Numbers: counts. Offline replay (NO-ADAPT), primary population, step-level mitigation, no reviewer. Labels as in Table 4.25.",
             fontsize=7, color=INK2)
    save(fig, "fig_19nov_security_utility.png")


def fig_contrasts():
    arms = [a for a in ORDER if a != "A0"]
    fig, axs = plt.subplots(1, 3, figsize=(7.8, 3.8), sharey=True)
    y = np.arange(len(arms))[::-1]
    for ax, key, title in ((axs[0], "ASR", "Δ attack outcomes (pp)"), (axs[1], "benign_utility", "Δ benign tasks (pp)"),
                           (axs[2], "all_tasks", "Δ all tasks (pp)")):
        ax.axvline(0, color=INK2, lw=0.8)
        for yi, a in zip(y, arms):
            v, lo, hi = A["paired_vs_A0"][f"{a} minus A0"][key]
            excl = lo > 0 or hi < 0
            c = BLUE if excl else GRAY
            ax.plot([lo * 100, hi * 100], [yi, yi], color=c, lw=2, solid_capstyle="round")
            ax.plot(v * 100, yi, "o", ms=5.5, color=c if excl else "white", mec=c, mew=1.4)
        ax.set_title(title, fontsize=9, loc="left", color=INK)
        ax.grid(axis="y", visible=False)
    axs[0].set_yticks(y)
    axs[0].set_yticklabels([NEW[a] for a in arms], fontsize=8)
    fig.text(0, -0.06, "Variant minus full REM v1.0 on the same 3,313 episodes (labels as in Table 4.25). Filled blue: 95% interval excludes 0; "
             "hollow grey: includes 0.\nPositive Δ attack outcomes = more attacks without the component; positive Δ tasks = more tasks completed "
             "without it. Grouped bootstrap,\n9 (attacks) or 16 (tasks) clusters: descriptive intervals.", fontsize=7, color=INK2)
    save(fig, "fig_19nov_paired_differences.png")


def fig_reachability():
    R = A["decision_reachability_A0_vs_A6"]
    items = [("Forced by predicates D1/D2\n(before expected loss)", R["forced_by_predicates_before_expected_loss"], GRAY),
             ("Reached expected loss; release\nunchanged by the learned decision", R["unchanged_release"], GRAY),
             ("Withheld by the learned decision:\nattack-labelled", R["ml_withheld_attack_labelled"], BLUE),
             ("Withheld by the learned decision:\nunlabelled call, attacked episode", R["ml_withheld_unlabelled_attacked_episode"], BLUE),
             ("Withheld by the learned decision:\nlegitimate call, benign episode", R["ml_withheld_legit_benign_episode"], ORANGE)]
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    y = np.arange(len(items))[::-1]
    for yi, (n, v, c) in zip(y, items):
        ax.barh(yi, v, height=0.6, color=c)
        ax.annotate(f"{v:,}", (v, yi), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([i[0] for i in items], fontsize=8)
    ax.set_xlabel("calls")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, max(i[1] for i in items) * 1.15)
    E = A["episode_level_ml_effect"]
    ax.set_title(f"{R['calls_total']:,} recorded calls, all scored by the estimator", fontsize=9, loc="left")
    fig.text(0, -0.08, f"Episode level, full REM v1.0 against variant A4a (learned decision removed): attacks prevented by the learned decision "
             f"{E['attacks_prevented_due_to_ml']}, admitted {E['attacks_admitted_due_to_ml']};\ntasks lost {E['tasks_lost_due_to_ml']}, "
             f"gained {E['tasks_gained_due_to_ml']}.", fontsize=7, color=INK2)
    save(fig, "fig_19nov_reachability.png")


fig_security_utility()
fig_contrasts()
fig_reachability()
