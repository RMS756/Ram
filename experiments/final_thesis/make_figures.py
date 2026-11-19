"""Figures of the final ablation and external comparison, generated only from stored outputs.

Inputs : REM_FINAL_THESIS_COMPLETION_2026_11_19/results/{ablation_results,external_results}.json
         and, for the reliability diagram, the cross-fitted probabilities in $PILOT_RESULTS_DIR/state (fresh pilot run).
Outputs: REM_FINAL_THESIS_COMPLETION_2026_11_19/figures/*.png (300 dpi, light background for print)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "REM_FINAL_THESIS_COMPLETION_2026_11_19"
FIG = OUT / "figures"
FIG.mkdir(exist_ok=True)
A = json.loads((OUT / "results" / "ablation_results.json").read_text())
X = json.loads((OUT / "results" / "external_results.json").read_text())

BLUE, ORANGE, AQUA, YELLOW, MAGENTA = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
GRAY, INK, INK2, GRID = "#8a8986", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "figure.facecolor": "white", "axes.facecolor": "white", "savefig.dpi": 300})
ARMS = ["B0", "A0", "A1", "A2", "A3", "A4a", "A4b", "A5", "A6", "A7"]
LBL = {"B0": "B0 no defence", "A0": "A0 REM v1.0", "A1": "A1 − behavioural", "A2": "A2 − Platt calibration",
       "A3": "A3 consequence-indep. thresholds", "A4a": "A4a − context", "A4b": "A4b − action/provenance",
       "A5": "A5 − Modify", "A6": "A6 − learned decision", "A7": "A7 − predicates"}


def col(a):
    return ORANGE if a == "A0" else (GRAY if a == "B0" else BLUE)


def save(fig, name):
    fig.savefig(FIG / name, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# 1. security and utility per arm (dot + 95% grouped-bootstrap interval), two panels, shared arm axis
def fig_security_utility():
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.8), sharey=True)
    y = np.arange(len(ARMS))[::-1]
    for ax, key, title, n in ((axs[0], "ASR", "Attack success rate (successes / 2,979)", "attack_successes"),
                              (axs[1], "benign_utility", "Benign utility (completed / 334)", "benign_completed")):
        for yi, a in zip(y, ARMS):
            m = A["arms"][a]
            v, lo, hi = m[key]
            ax.plot([lo * 100, hi * 100], [yi, yi], color=col(a), lw=2, solid_capstyle="round")
            ax.plot(v * 100, yi, "o", ms=6, color=col(a), mec="white", mew=1.2)
            ax.annotate(f"{m[n]}", (hi * 100, yi), xytext=(5, 0), textcoords="offset points", va="center", fontsize=7.5, color=INK2)
        ax.set_title(title, fontsize=9, color=INK, loc="left")
        ax.set_xlabel("%")
        ax.grid(axis="y", visible=False)
    axs[0].set_yticks(y)
    axs[0].set_yticklabels([LBL[a] for a in ARMS])
    axs[0].set_xlim(-2, 40)
    axs[1].set_xlim(0, 80)
    fig.text(0, -0.04, "Dots: point estimates; bars: 95% grouped-bootstrap intervals (ASR clustered by injection task, utility by user task). "
             "Numbers: counts.\nOffline replay (NO-ADAPT), primary population, scheme S1, step-level mitigation, no reviewer.",
             fontsize=7, color=INK2)
    save(fig, "fig_ablation_security_utility.png")


# 2. paired differences against A0 (forest plot)
def fig_contrasts():
    arms = [a for a in ARMS if a != "A0"]
    fig, axs = plt.subplots(1, 3, figsize=(7.6, 3.6), sharey=True)
    y = np.arange(len(arms))[::-1]
    for ax, key, title in ((axs[0], "ASR", "Δ ASR (pp)"), (axs[1], "benign_utility", "Δ benign utility (pp)"),
                           (axs[2], "all_tasks", "Δ all-task completion (pp)")):
        ax.axvline(0, color=INK2, lw=0.8)
        for yi, a in zip(y, arms):
            v, lo, hi = A["paired_vs_A0"][f"{a} minus A0"][key]
            excl = lo > 0 or hi < 0
            c = BLUE if excl else GRAY
            ax.plot([lo * 100, hi * 100], [yi, yi], color=c, lw=2, solid_capstyle="round")
            ax.plot(v * 100, yi, "o" if excl else "o", ms=5.5, color=c if excl else "white", mec=c, mew=1.4)
        ax.set_title(title, fontsize=9, loc="left", color=INK)
        ax.grid(axis="y", visible=False)
    axs[0].set_yticks(y)
    axs[0].set_yticklabels([LBL[a] for a in arms])
    fig.text(0, -0.05, "Arm minus A0 on the same 3,313 episodes. Filled blue: 95% interval excludes 0; hollow grey: includes 0. "
             "Positive Δ ASR = more attacks without the component;\npositive Δ utility = more tasks completed without it. "
             "Grouped bootstrap, 9 (ASR) or 16 (utility) clusters: descriptive intervals.", fontsize=7, color=INK2)
    save(fig, "fig_ablation_paired_differences.png")


# 3. calibration: reliability diagram A0 (calibrated) vs A2 (raw), same held-out steps; metric table beside
def fig_calibration():
    st = os.environ.get("PILOT_RESULTS_DIR")
    sys.path.insert(0, str(ROOT / "experiments" / "pilot"))
    import run_main as RM  # noqa: E402
    from data import build  # noqa: E402
    from rem.evaluation.probabilistic import reliability_table  # noqa: E402
    if not st:
        raise SystemExit("PILOT_RESULTS_DIR (fresh pilot state) is required for the reliability diagram")
    fits = RM.load_state("crossfit")
    data = build("primary")
    common = ~np.isnan(fits["label_nll_primary"].p_cal)
    for k in ("no_beh", "no_ctx", "no_act"):
        common &= ~np.isnan(fits[k].p_cal)
    y = data.y[common]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.4), gridspec_kw={"width_ratios": [1, 1.4]})
    ax.plot([0, 1], [0, 1], color=GRAY, lw=0.8, ls="--")
    for p, name, c, mk in ((fits["label_nll_primary"].p_cal[common], "A0 calibrated", ORANGE, "o"),
                           (fits["label_nll_primary"].p_raw[common], "A2 raw (no Platt)", BLUE, "s")):
        t = [r for r in reliability_table(y, p, RM.E["ece_bins"]) if r["count"]]
        xs = [r["mean_p"] for r in t]
        ys = [r["positive_rate"] for r in t]
        ax.plot(xs, ys, marker=mk, ms=4.5, lw=1.6, color=c, label=name, mec="white", mew=0.8)
    ax.set_xlabel("Mean predicted probability (bin)")
    ax.set_ylabel("Observed attack-label frequency")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    ax.set_title("Reliability, 10 bins, held-out steps", fontsize=9, loc="left")
    ax2.axis("off")
    C = A["calibration_offline"]
    rows = [[a, f"{C[a]['roc_auc']:.3f}", f"{C[a]['pr_auc']:.3f}", f"{C[a]['brier']:.4f}", f"{C[a]['ece_10']:.4f}", f"{C[a]['log_loss']:.4f}"]
            for a in ("A0", "A2", "A1", "A4a", "A4b")]
    tb = ax2.table(cellText=rows, colLabels=["Arm", "ROC-AUC", "PR-AUC", "Brier", "ECE", "Log-loss"], loc="center", cellLoc="center")
    tb.auto_set_font_size(False)
    tb.set_fontsize(7.5)
    tb.scale(1, 1.4)
    tb.auto_set_column_width(list(range(6)))
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor(GRID)
        if r == 0:
            cell.set_text_props(color=INK, weight="bold")
    ax2.set_title(f"Same {int(common.sum()):,} held-out steps ({int(y.sum())} attack-labelled)", fontsize=8.5, loc="left")
    save(fig, "fig_ablation_calibration.png")


# 4. latency per arm (complete-call timer): median dot, p95 bar end
def fig_latency():
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    y = np.arange(len(ARMS))[::-1]
    for yi, a in zip(y, ARMS):
        m = A["arms"][a]
        ax.plot([m["latency_ms_median"], m["latency_ms_p95"]], [yi, yi], color=col(a), lw=2, solid_capstyle="round")
        ax.plot(m["latency_ms_median"], yi, "o", ms=6, color=col(a), mec="white", mew=1.2)
        ax.plot(m["latency_ms_mean"], yi, "|", ms=9, mew=1.6, color=INK2)
    ax.set_yticks(y)
    ax.set_yticklabels([LBL[a] for a in ARMS])
    ax.set_xlabel("ms per evaluated call (complete-call timer)")
    ax.set_xlim(0, None)
    ax.grid(axis="y", visible=False)
    ax.set_title("REM decision latency per call: median (dot) to p95 (bar end); mean (tick)", fontsize=8.5, loc="left")
    fig.text(0, -0.06, f"{A['arms']['A0']['calls_timed']:,} calls per arm; one CPU container; offline replay; not a deployment measurement.",
             fontsize=7, color=INK2)
    save(fig, "fig_ablation_latency.png")


# 5. decision reachability (A0 vs A6 on identical recorded calls)
def fig_reachability():
    R = A["decision_reachability_A0_vs_A6"]
    items = [("Forced by predicates D1/D2\n(before expected loss)", R.get("forced_by_predicates_before_expected_loss", 0), GRAY),
             ("Reached expected loss,\nrelease unchanged by ML", R.get("unchanged_release", 0), GRAY),
             ("ML withheld: attack-labelled", R.get("ml_withheld_attack_labelled", 0), BLUE),
             ("ML withheld: unlabelled call\nin an attacked episode", R.get("ml_withheld_unlabelled_attacked_episode", 0), BLUE),
             ("ML withheld: legitimate call\nin a benign episode", R.get("ml_withheld_legit_benign_episode", 0), ORANGE)]
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
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
    fig.text(0, -0.07, f"Episode level, A0 vs A6: attacks prevented by the learned decision {E['attacks_prevented_due_to_ml']}, admitted "
             f"{E['attacks_admitted_due_to_ml']}; tasks lost {E['tasks_lost_due_to_ml']}, gained {E['tasks_gained_due_to_ml']}.",
             fontsize=7, color=INK2)
    save(fig, "fig_ablation_reachability.png")


# 6. external comparison: two separate panels (never pooled)
def fig_external():
    fig, axs = plt.subplots(1, 2, figsize=(7.6, 3.6), sharex=True, sharey=True)
    names = {"D0": "no defence", "D1": "repeat_user_prompt", "D2": "spotlighting", "D3": "tool_filter", "D4": "pi_detector"}
    cols = {"D0": GRAY, "D1": BLUE, "D2": AQUA, "D3": YELLOW, "D4": MAGENTA}
    ax = axs[0]
    for k, r in X["recorded"].items():
        ax.plot(r["ASR"][0] * 100, r["tasks_under_attack"] / r["n_attacked"] * 100, "o", ms=8, color=cols[k], mec="white", mew=1.2)
        off = {"D1": (-10, 8), "D2": (6, -12), "D0": (6, -12)}.get(k, (6, 3))
        ax.annotate(f"{k} {names[k]}", (r["ASR"][0] * 100, r["tasks_under_attack"] / r["n_attacked"] * 100), xytext=off,
                    textcoords="offset points", fontsize=7.5, color=INK, ha="right" if k == "D1" else "left")
    ax.set_title("Recorded closed loop (AgentDojo runs, gpt-4o)", fontsize=8.5, loc="left")
    ax = axs[1]
    for key, r in X["replay"].items():
        k, arm = key.split("|")
        u = r["tasks_under_attack"] / r["n_attacked"] * 100
        if arm == "REM":
            ax.plot(r["ASR"][0] * 100, u, "D", ms=7, color=cols[k], mec=INK, mew=0.8)
            off = {"D0": (8, 12), "D1": (8, 2), "D2": (8, -8), "D4": (8, -4)}[k]
            ax.annotate(f"{k}+REM ({r['attack_successes']}/{r['n_attacked']})", (r["ASR"][0] * 100, u), xytext=off,
                        textcoords="offset points", fontsize=7, color=INK, va="center")
        else:
            ax.plot(r["ASR"][0] * 100, u, "o", ms=7, color="white", mec=cols[k], mew=1.6)
            ax.annotate(f"{k}", (r["ASR"][0] * 100, u), xytext=(6, 3), textcoords="offset points", fontsize=7.5, color=INK2)
    ax.set_title("Offline replay (NO-ADAPT): without REM ○ / with REM v1.0 ◆", fontsize=8.5, loc="left")
    for ax in axs:
        ax.set_xlabel("ASR (%)")
        ax.set_xlim(-3, 75)
        ax.set_ylim(0, 90)
    axs[0].set_ylabel("Tasks completed under attack (%)")
    fig.text(0, -0.08, "Left and right are different evidence kinds and are never pooled. D3 tool_filter is absent on the right: "
             "its traces are not replayable with the frozen harness (amendment 05a).", fontsize=7, color=INK2)
    save(fig, "fig_external_security_utility.png")


if __name__ == "__main__":
    fig_security_utility()
    fig_contrasts()
    fig_latency()
    fig_reachability()
    fig_external()
    fig_calibration()
    arch = ROOT / "results" / "pilot_R4" / "figures" / "fig_architecture.png"
    if arch.exists():
        shutil.copy(arch, FIG / "fig_architecture_rem_v1.png")
        print("copied architecture figure")
