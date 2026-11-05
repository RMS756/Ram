"""Figures from committed result files only (no typed value).
usage: python3 REM_EXPERIMENTAL_VALIDATION/04_RESULTS/FIGURES/make_figures.py"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "..", "METRICS", "rem_lite_results.json")))
M = R["replay_metrics"]
CONF = [("No Defense", "B0", "#7f7f7f"), ("REM-Lite", "REMLite_step_level_no_reviewer", "#d08c2f"),
        ("Full REM", "REM_step_level_no_reviewer", "#1f4e79")]

fig, ax = plt.subplots(figsize=(5.6, 4.2))
for name, k, col in CONF:
    a, u = M[k]["ASR"], M[k]["benign_utility"]
    ax.errorbar(u[0], a[0], xerr=[[u[0] - u[1]], [u[2] - u[0]]], yerr=[[a[0] - a[1]], [a[2] - a[0]]],
                fmt="o", color=col, capsize=3, label=name)
ax.set_xlabel("Benign utility (higher is better)")
ax.set_ylabel("Attack success rate (lower is better)")
ax.set_title("Mode A (recorded traces, NO-ADAPT replay)\nMELON: not executed", fontsize=10)
ax.grid(alpha=.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig_security_utility_mode_a.png"), dpi=300)

O = R["observe_only_heldout"]
verd = ["allow", "modify", "escalate", "block"]
cols = ["#bbbbbb", "#d08c2f", "#6a51a3", "#a33"]
fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.4), sharey=True)
for j, (lab, key) in enumerate((("Attack steps (y = 1)", "verdicts_y1"), ("Legitimate steps (y = 0)", "verdicts_y0"))):
    names = ["REM-Lite", "Full REM"]
    bottom = [0.0, 0.0]
    for v, c in zip(verd, cols):
        tot = [sum(O[n][key].values()) for n in names]
        vals = [O[n][key].get(v, 0) / t for n, t in zip(names, tot)]
        ax[j].bar(names, vals, bottom=bottom, color=c, label=v if j == 0 else None)
        bottom = [b + x for b, x in zip(bottom, vals)]
    ax[j].set_title(lab, fontsize=10)
ax[0].set_ylabel("share of held-out steps")
fig.legend(loc="lower center", ncol=4, fontsize=8)
fig.tight_layout(rect=(0, 0.08, 1, 1)); fig.savefig(os.path.join(HERE, "fig_decisions_rem_lite_vs_full.png"), dpi=300)
print("figures written")
