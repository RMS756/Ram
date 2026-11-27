"""Figures added in the defence-ready edition. Generated only from audit/number_verification.json (raw-record
recomputation) and from the REM code structure. Palette: categorical #2a78d6 / #eb6834 / #1baf7a (validated with the
dataviz validator; green < 3:1 contrast, so every mark is direct-labelled and every figure has a companion table);
neutral grey #6f6e6b for the no-defence reference."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

D = Path(__file__).resolve().parents[1]
V = json.loads((D / "audit" / "number_verification.json").read_text())
F = D / "figures"
F.mkdir(exist_ok=True)
BLUE, ORANGE, GREEN, GREY, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#6f6e6b", "#1f1e1c", "#52514e"
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e4e3df", "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})

# ------------------------------------------------------------------ Figure: layer-to-implementation map
fig, ax = plt.subplots(figsize=(8.6, 5.8))
ax.set_xlim(0, 104)
ax.set_ylim(0, 100)
ax.axis("off")
layers = [
    ("1  Input & Context", "provenance.py: hygiene, trust labels,\nentity extraction", "A1: not isolatable (labels feed\nx_act, x_beh1, D2); hygiene changes\n0 of 16,727 outputs"),
    ("2  Detection", "instruction_patterns.py: x_ctx2\n(classifier x_ctx1 absent, D-8)", "A2a: x_ctx2\nA2b: x_ctx2 + x_beh1 (coupled)"),
    ("3  Behavioral Analysis", "evidence.py: x_beh1-x_beh4; also\ncomputes x_act1-x_act3 from\nlayer-1 labels", "A3a: behavioral evidence x_beh1-4\nA3b: action / provenance\nevidence x_act1-3"),
    ("4  Decision Engine", "ridge LR, logit calibration, tiers,\npredicates D1/D2, expected loss", "A4a learned decision\nA4b predicates  A4c calibration\nA4d thresholds  A4e Modify"),
    ("5  Mitigation", "RemGuard._mitigate: step-level;\nAllow releases, others withhold", "A5: enforcement off (shadow mode)"),
]
ys = [86, 68, 50, 32, 14]
for (name, impl, abl), y in zip(layers, ys):
    ax.add_patch(FancyBboxPatch((1, y - 6.5), 25, 13, boxstyle="round,pad=0.4,rounding_size=1.5", fc="#eef4fc", ec=BLUE, lw=1.2))
    ax.text(13.5, y, name, ha="center", va="center", fontsize=8.6, color=INK, weight="bold")
    ax.add_patch(FancyBboxPatch((34, y - 6.5), 34, 13, boxstyle="round,pad=0.4,rounding_size=1.5", fc="white", ec="#b9b8b4", lw=0.9))
    ax.text(51, y, impl, ha="center", va="center", fontsize=6.9, color=INK)
    ax.add_patch(FancyBboxPatch((75, y - 6.5), 28, 13, boxstyle="round,pad=0.4,rounding_size=1.5", fc="#fdf1ea", ec=ORANGE, lw=0.9))
    ax.text(89, y, abl, ha="center", va="center", fontsize=6.4, color=INK)
for y0, y1 in zip(ys[:-1], ys[1:]):
    ax.add_patch(FancyArrowPatch((13.5, y0 - 7), (13.5, y1 + 7), arrowstyle="-|>", mutation_scale=10, color=BLUE, lw=1.1))
# couplings
ax.add_patch(FancyArrowPatch((68.8, 66), (68.8, 54), connectionstyle="arc3,rad=-0.5", arrowstyle="-|>", mutation_scale=9, color=ORANGE, lw=1, ls="--"))
ax.text(71.6, 60, "x_beh1 needs x_ctx2", fontsize=6.2, color=MUTED, va="center", rotation=90)
ax.add_patch(FancyArrowPatch((29.6, 84), (29.6, 52), connectionstyle="arc3,rad=-0.22", arrowstyle="-|>", mutation_scale=9, color=ORANGE, lw=1, ls="--"))
ax.text(28.2, 69, "labels feed x_act, x_beh1, D2", fontsize=6.0, color=MUTED, ha="center", va="center", rotation=90)
for x, t in ((13.5, "Architectural layer"), (51, "Implementation (rem/ at 9fddfa7)"), (89, "Ablation variant(s)")):
    ax.text(x, 97, t, ha="center", fontsize=8.5, color=MUTED, style="italic")
ax.text(0, 2, "Solid arrows: runtime flow. Dashed: couplings that prevent removing a layer as one software module.", fontsize=7, color=MUTED)
fig.savefig(F / "fig_layer_mapping.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------ Figure: paired differences by layer (P1)
s21 = V["S21_episode_level_ablation"]["P1_primary"]["paired_vs_A0"]
s19 = V["S19_decision_engine_subablations"]["paired_vs_A0"]
rows = [("A2a − detection feature x_ctx2", s21["A1a"], "Detection"),
        ("A2b − detection layer (x_ctx2, x_beh1)", s21["A1b"], "Detection"),
        ("A3a − behavioral evidence", s21["A2"], "Behavioral"),
        ("A3b − action / provenance evidence", s21["AIC"], "Behavioral"),
        ("A4a − learned decision", s21["A3"], "Decision"),
        ("A4b − predicates D1/D2", s21["A3P"], "Decision"),
        ("A4c − calibration", s19["A2"], "Decision"),
        ("A4d − thresholds instead of expected loss", s19["A3"], "Decision"),
        ("A4e − Modify verdict", s19["A5"], "Decision"),
        ("A5  − enforcement (shadow mode)", s21["A4"], "Mitigation")]
fig, axs = plt.subplots(1, 2, figsize=(7.6, 4.3), sharey=True)
y = list(range(len(rows)))[::-1]
for ax, key, title, col in ((axs[0], "attack", "Δ replay attack outcome (pp)", ORANGE), (axs[1], "benign_completion", "Δ benign task completion (pp)", BLUE)):
    ax.axvline(0, color=MUTED, lw=0.8)
    for yi, (lab, d, _) in zip(y, rows):
        p, lo, hi = d[key]["diff_pp"]
        excl = lo > 0 or hi < 0
        ax.plot([lo, hi], [yi, yi], color=col, lw=1.8, solid_capstyle="round")
        ax.plot(p, yi, "o", ms=6, color=col if excl else "white", mec=col, mew=1.3)
        if abs(p) >= 1:
            ax.annotate(f"{p:+.1f}", (hi, yi), xytext=(4, 0), textcoords="offset points", va="center", fontsize=7, color=INK)
        elif excl or p != 0:
            ax.annotate(f"{p:+.1f}", (hi, yi), xytext=(4, 0), textcoords="offset points", va="center", fontsize=7, color=INK)
    ax.set_title(title, fontsize=9, loc="left", color=INK)
    ax.grid(axis="y", visible=False)
axs[0].set_yticks(y)
axs[0].set_yticklabels([r[0] for r in rows], fontsize=7.6)
axs[0].set_xlim(-3, 38)
axs[1].set_xlim(-10, 48)
fig.text(0, -0.05, "Arm minus full REM v1.0 on identical episodes (primary population: 2,979 attacked, 334 benign). Filled: 95% grouped-bootstrap\n"
         "interval excludes 0; open: includes 0. Offline replay (NO-ADAPT), step-level mitigation, no reviewer. Not live attack success rates.",
         fontsize=6.8, color=MUTED)
fig.savefig(F / "fig_ablation_by_layer.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------ Figure: REM vs Progent security–utility plane
c = V["S22_offline_comparison"]
fig, axs = plt.subplots(1, 2, figsize=(7.6, 3.6), sharey=False)
arms = [("B0", "no defence", GREY, "s", (-8, 10), "right"), ("A0", "REM v1.0", BLUE, "o", (-6, 12), "right"), ("A3", "REM rules only", GREEN, "^", (8, -22), "left"), ("PG", "Progent policy", ORANGE, "D", (8, 12), "left")]
for ax, pop, title in ((axs[0], "P1_primary", "Primary population (2,979 / 334)"), (axs[1], "P3_second_population", "Second population (2,065 / 48)")):
    for a, lab, col, mk, off, ha in arms:
        m = c[pop]["arms"][a]
        bx, blo, bhi = m["benign_pct"]
        sy, slo, shi = m["asr_pct"]
        ax.plot([blo, bhi], [sy, sy], color=col, lw=1.4, alpha=0.8)
        ax.plot([bx, bx], [slo, shi], color=col, lw=1.4, alpha=0.8)
        ax.plot(bx, sy, mk, ms=7, color=col, mec="white", mew=1.0)
        ax.annotate(f"{lab}\n{m['attacks']} att. / {m['benign_completed']} ben.", (bx, sy), xytext=off, textcoords="offset points", fontsize=6.8, color=INK, ha=ha)
    ax.set_title(title, fontsize=9, loc="left", color=INK)
    ax.set_xlabel("benign tasks completed (%)", fontsize=8)
    ax.set_xlim(0, 105)
axs[0].set_ylabel("replay attack outcome (%)", fontsize=8)
fig.text(0, -0.08, "Offline replay of identical recorded episodes (NO-ADAPT): crosses are 95% grouped-bootstrap intervals. Progent: the authors' official\n"
         "checker with their published manual banking policy (task-informed allow-list). Not live attack success rates.", fontsize=6.8, color=MUTED)
fig.savefig(F / "fig_rem_vs_progent.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("written", sorted(p.name for p in F.glob("*.png")))

# ------------------------------------------------------------------ Figure: integration points of the four frameworks
fig, ax = plt.subplots(figsize=(8.2, 4.4))
ax.set_xlim(0, 100)
ax.set_ylim(0, 60)
ax.axis("off")


def box(x, y, w, h, text, fc="white", ec="#b9b8b4", fs=7.6, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc=fc, ec=ec, lw=1.0))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK, weight="bold" if bold else "normal")


def arrow(x0, y0, x1, y1, col=MUTED, ls="-"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=9, color=col, lw=1.0, ls=ls))


box(1, 36, 13, 9, "User request\n(trusted)")
box(20, 33, 18, 15, "Agent LLM\nproposes the next\ntool call", fc="#f4f3f0")
box(46, 36, 16, 9, "Proposed\ntool call")
box(70, 36, 13, 9, "Tool executor")
box(87, 36, 12, 9, "Tool output\n(untrusted)")
arrow(14, 40.5, 20, 40.5)
arrow(38, 40.5, 46, 40.5)
arrow(62, 40.5, 70, 40.5)
arrow(83, 40.5, 87, 40.5)
ax.add_patch(FancyArrowPatch((93, 36), (31, 31.5), connectionstyle="arc3,rad=-0.25", arrowstyle="-|>", mutation_scale=9, color=MUTED, lw=1.0))
ax.text(66, 21.5, "the output returns to the agent", fontsize=6.8, color=MUTED, ha="center")
# REM and Progent at the call boundary
box(55, 49, 30, 9, "REM: verdict on each proposed call\nProgent: policy check on each call", fc="#eef4fc", ec=BLUE, fs=7.0)
arrow(66, 49, 66, 41.5, col=BLUE)
# DRIFT replaces the agent element
ax.add_patch(FancyBboxPatch((18.5, 31.5), 21, 18, boxstyle="round,pad=0.3,rounding_size=1.2", fc="none", ec=ORANGE, lw=1.3, ls="--"))
box(14, 50.5, 30, 8, "DRIFT replaces this element: planner,\nprivilege validator, judge, isolator", fc="#fdf1ea", ec=ORANGE, fs=7.0)
# MELON after each tool turn
box(2, 3, 40, 12, "MELON: after each tool turn, re-runs the agent\nwith the request masked; stops the episode if\nits calls match the masked calls (cosine > 0.8)", fc="#e9f7f1", ec=GREEN, fs=6.6)
arrow(22, 15, 24, 31.5, col=GREEN, ls="--")
ax.text(0, -2, "Schematic of the official implementations (REM: rem/; Progent: secagent; DRIFT: DRIFTLLM; MELON: pi_detector.py).",
        fontsize=6.8, color=MUTED)
fig.savefig(F / "fig_integration_points.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("integration figure written")
