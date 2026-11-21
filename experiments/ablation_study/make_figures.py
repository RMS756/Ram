"""Figures of the REM component ablation study, generated only from REM_ABLATION_STUDY/results/ablation_metrics.json."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

D = Path(__file__).resolve().parents[2] / "REM_ABLATION_STUDY"
M = json.loads((D / "results" / "ablation_metrics.json").read_text())
F = D / "06_FIGURES"
F.mkdir(exist_ok=True)
ARMS = ["B0", "A0", "A1a", "A1b", "A2", "AIC", "A3", "A3P", "A4"]
LBL = {"B0": "B0 no defence", "A0": "A0 full REM", "A1a": "A1a − detection feature", "A1b": "A1b − detection layer",
       "A2": "A2 − behavioural", "AIC": "AIC − provenance evidence", "A3": "A3 − learned decision",
       "A3P": "A3P − deterministic controls", "A4": "A4 shadow mitigation"}
POPS = [("P1_primary", "P1 primary", "#2a78d6"), ("P2_cross_template", "P2 unseen templates", "#1baf7a"),
        ("P3_second_population", "P3 unseen backbones", "#eb6834")]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e4e3df", "grid.linewidth": 0.6, "axes.axisbelow": True})
NOTE = "Offline recorded-trace replay (NO-ADAPT), step-level mitigation, no reviewer. 95% grouped-bootstrap intervals (clusters: injection task / user task)."


def dotplot(metric, title, fname, pops=POPS, xlim=(-3, 103)):
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    y = np.arange(len(ARMS))[::-1]
    off = {p[0]: o for p, o in zip(pops, np.linspace(0.22, -0.22, len(pops)))}
    for key, name, col in pops:
        r = M["populations"][key]["arms"]
        first = True
        for yi, a in zip(y, ARMS):
            v = r[a][metric]
            if not v or v[0] is None or v[0] != v[0]:
                continue
            ax.plot([v[1] * 100, v[2] * 100], [yi + off[key]] * 2, color=col, lw=1.8)
            ax.plot(v[0] * 100, yi + off[key], "o", color=col, ms=5, mec="white", mew=0.8, label=name if first else None)
            first = False
    ax.set_yticks(y)
    ax.set_yticklabels([LBL[a] for a in ARMS])
    ax.set_xlim(*xlim)
    ax.set_xlabel("%")
    ax.grid(axis="y", visible=False)
    ax.set_title(title, fontsize=9.5, loc="left")
    ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    fig.text(0, -0.04, NOTE, fontsize=6.8, color="#52514e")
    fig.savefig(F / fname, dpi=300, bbox_inches="tight")
    plt.close(fig)


dotplot("attack_call_withholding_rate", "Attack-labelled restricted calls withheld (call-level recall; not an ASR)", "fig1_attack_call_withholding.png")
dotplot("benign_call_blocking_rate", "Restricted calls withheld in benign episodes (call-level false-positive rate)",
        "fig2_benign_call_blocking.png", pops=[POPS[0], POPS[2]])

# paired differences against A0
fig, axs = plt.subplots(1, 2, figsize=(7.6, 3.8), sharey=True)
arms = [a for a in ARMS if a not in ("A0",)]
y = np.arange(len(arms))[::-1]
for ax, key, title in ((axs[0], "d_attack_call_withholding_rate", "Δ attack-call withholding (pp)"),
                       (axs[1], "d_benign_call_blocking_rate", "Δ benign-call blocking (pp)")):
    ax.axvline(0, color="#52514e", lw=0.8)
    for pk, name, col in POPS:
        d = M["populations"][pk]["paired_vs_A0"]
        o = {"P1_primary": 0.22, "P2_cross_template": 0.0, "P3_second_population": -0.22}[pk]
        for yi, a in zip(y, arms):
            v = d[a][key]
            if not v or v[0] is None or v[0] != v[0]:
                continue
            excl = v[1] > 0 or v[2] < 0
            ax.plot([v[1] * 100, v[2] * 100], [yi + o] * 2, color=col, lw=1.6)
            ax.plot(v[0] * 100, yi + o, "o", ms=5, color=col if excl else "white", mec=col, mew=1.2,
                    label=name if (a == arms[0] and ax is axs[0]) else None)
    ax.set_title(title, fontsize=9, loc="left")
    ax.grid(axis="y", visible=False)
axs[0].set_yticks(y)
axs[0].set_yticklabels([LBL[a] for a in arms])
fig.legend(*axs[0].get_legend_handles_labels(), frameon=False, fontsize=7, loc="upper center", ncol=3, bbox_to_anchor=(0.55, 1.04))
fig.text(0, -0.06, "Arm minus A0 on identical episodes and call positions. Filled: 95% interval excludes 0; open: includes 0.\n" + NOTE,
         fontsize=6.6, color="#52514e")
fig.savefig(F / "fig3_paired_differences_vs_A0.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# learned decision: release changes A3 vs A0 by class
fig, ax = plt.subplots(figsize=(6.8, 2.9))
classes = [("attack_labelled:A0_withheld_arm_released", "attack-labelled calls withheld only by the learned decision", "#2a78d6"),
           ("unlabelled_in_attacked_episode:A0_withheld_arm_released", "unlabelled calls in attacked episodes", "#8a8986"),
           ("benign_episode:A0_withheld_arm_released", "calls in benign episodes (false positives)", "#eb6834")]
yy = np.arange(3)[::-1]
for yi, (pk, name, _) in zip(yy, POPS):
    left = 0
    ch = M["populations"][pk]["paired_vs_A0"]["A3"]["call_release_changes_vs_A0"]
    for k, lab, col in classes:
        v = ch.get(k, 0)
        ax.barh(yi, v, left=left, color=col, height=0.55, label=lab if pk == "P1_primary" else None, edgecolor="white", linewidth=1)
        if v > 80:
            ax.annotate(f"{v:,}", (left + v / 2, yi), ha="center", va="center", fontsize=7.5, color="white")
        left += v
ax.set_yticks(yy)
ax.set_yticklabels([p[1] for p in POPS])
ax.set_xlabel("call releases changed by the learned decision (A0 vs A3)")
ax.grid(axis="y", visible=False)
ax.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, 1.32), ncol=1)
fig.text(0, -0.1, "Counts of calls whose release differs between A0 and A3 (P2 has no benign episodes; P3 benign-episode changes: 46). In every class the learned decision withholds\nand the predicates alone release; no call is released only by the learned decision. Offline recorded-trace replay (NO-ADAPT), step-level mitigation, no reviewer.", fontsize=6.4, color="#52514e")
fig.savefig(F / "fig4_learned_decision_release_changes.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# latency
fig, ax = plt.subplots(figsize=(6.4, 3.6))
y = np.arange(len(ARMS))[::-1]
r = M["populations"]["P1_primary"]["arms"]
for yi, a in zip(y, ARMS):
    col = "#eb6834" if a == "A0" else ("#8a8986" if a in ("B0", "A3") else "#2a78d6")
    ax.plot([r[a]["latency_full_ms_median"], r[a]["latency_full_ms_p95"]], [yi, yi], color=col, lw=2)
    ax.plot(r[a]["latency_full_ms_median"], yi, "o", color=col, ms=6, mec="white")
ax.set_yticks(y)
ax.set_yticklabels([LBL[a] for a in ARMS])
ax.set_xlim(0, None)
ax.set_xlabel("ms per call: median (dot) to p95 (bar end), complete-call timer")
ax.grid(axis="y", visible=False)
fig.text(0, -0.05, f"P1, {r['A0']['calls_timed']:,} calls per arm, one CPU container; replay timing, not a deployment latency.",
         fontsize=6.8, color="#52514e")
fig.savefig(F / "fig5_latency_per_arm.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("figures written to", F)
