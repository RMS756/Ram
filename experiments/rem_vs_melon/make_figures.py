"""Figures from stored outputs only. Live-result figures are produced by analyze_live.py after a live run; until then
the only figure is the PLANNING workload per arm (from results/workload_estimate.json, recorded gpt-4o trajectories).
usage: python3 experiments/rem_vs_melon/make_figures.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

D = os.path.join(os.path.dirname(__file__), "..", "..", "REM_MELON_COMPARISON_2026_11_19")
W = json.load(open(os.path.join(D, "results", "workload_estimate.json")))
os.makedirs(os.path.join(D, "figures"), exist_ok=True)
arms = ["D0 no defence", "D1 REM v1.0", "D2 MELON"]
agent = W["per_arm_D0_or_D1"]["agent_calls"]
masked = W["D2_extra"]["melon_masked_calls"]
cin = W["per_arm_D0_or_D1"]["agent_input_chars"] / 1e6
min_ = W["D2_extra"]["melon_masked_input_chars"] / 1e6
fig, axs = plt.subplots(1, 2, figsize=(8.2, 3.0), gridspec_kw={"wspace": 0.55})
for ax, base, extra, title in ((axs[0], agent, masked, "Model calls per arm (160 episodes)"),
                               (axs[1], cin, min_, "Input characters per arm (millions)")):
    vals = [base, base, base]
    ax.barh(range(3), vals, color="#2a78d6", height=0.55, label="agent calls")
    ax.barh([2], [extra], left=[base], color="#eb6834", height=0.55, label="MELON masked re-execution")
    for j, v in enumerate(vals):
        tot = v + (extra if j == 2 else 0)
        ax.annotate(f"{tot:,.0f}" if base > 100 else f"{tot:.2f}", (tot, j), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8)
    ax.set_yticks(range(3))
    ax.set_yticklabels(arms)
    ax.set_title(title, fontsize=9, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, (base + extra) * 1.35)
fig.legend(*axs[0].get_legend_handles_labels(), frameon=False, fontsize=7, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.06))
fig.text(0, -0.08, "PLANNING ESTIMATE, not a measurement of the arms: computed from AgentDojo's recorded undefended gpt-4o banking "
         "trajectories with the call model of the code\n(REM adds no model call; MELON adds one masked re-execution after each tool turn, plus "
         f"up to {W['D2_extra']['embedding_calls_upper_bound']} embedding calls). No live REM vs MELON run was executed.", fontsize=6.5)
fig.savefig(os.path.join(D, "figures", "fig_planned_workload_per_arm.png"), dpi=300, bbox_inches="tight")
print("wrote fig_planned_workload_per_arm.png")
