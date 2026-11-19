"""Figure: utility under attack on H2 vs unauthorised releases on the held-out probes (v2 + v3), per arm. Stored results only."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

D = Path(__file__).resolve().parents[2] / "REM_B_HARDENING_VALIDATION_2026_11_19"
fr = json.loads((D / "results/hardening_results.json").read_text())["populations"]["heldout_H2"]["metrics"]
am = json.loads((D / "results/hardening_results_amendment.json").read_text())["populations"]["heldout_H2"]["metrics"]
s3 = json.loads((D / "results/suites3_summary.json").read_text())
arms = ["C1", "PG", "REM_B", "REM_B2", "REM_B3"]
x = [s3["heldout_probes2"][a]["unauthorized_released"] + s3["heldout_probes3"][a]["unauthorized_released"] for a in arms]
y = [(fr.get(a) or am.get(a))["all_tasks_completed"] for a in arms]
fig, ax = plt.subplots(figsize=(6.4, 4.2))
for a, xi, yi in zip(arms, x, y):
    ax.scatter(xi, yi, s=60)
    ax.annotate(a, (xi, yi), textcoords="offset points", xytext=(6, -12) if a == "C1" else (6, 4), fontsize=9)
ax.set_xlabel("unauthorised proposals released on held-out probes v2 + v3 (of 56)")
ax.set_ylabel("tasks completed under attack on H2 (of 681)")
ax.set_title("Offline replay (NO-ADAPT); 0 attack successes for every arm shown", fontsize=9)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(D / "figures/h2_utility_vs_probe_violations.png", dpi=150)
print(dict(zip(arms, zip(x, y))))
