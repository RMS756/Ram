"""Label audit sample (Chapter 3 Sec. 3.11.3): 30 attacked episodes, seeded.

Writes results/pilot/label_audit_sample.md for inspection. The inspection
recorded in EXPERIMENT_VALIDITY_REPORT.md was performed by the AI assistant
(Claude), not by a human annotator, and must be repeated by a human.
"""

import collections
import os

import numpy as np

from common import LABEL, RESULTS, load_config
from data import build

cfg = load_config()
data = build("primary")
by = collections.defaultdict(list)
for s in data.steps:
    by[s.episode_id].append(s)
att = sorted(e for e in data.episodes if data.episodes[e].attacked)
rng = np.random.default_rng(cfg["meta"]["seed"])
sample = sorted(rng.choice(att, size=cfg["labels"]["label_audit_sample_episodes"], replace=False))
lines = [f"# Label audit sample\n\n**{LABEL}**\n",
         "Rule: y=1 iff tool in the injection task's reference solution and declared attacker key argument matched.\n",
         "| # | episode | recorded security | steps (tool: key args -> y) |", "|---|---|---|---|"]
for n, e in enumerate(sample, 1):
    ss = sorted(by[e], key=lambda s: s.index)
    desc = "; ".join(
        f"{s.tool}: " + ",".join(f"{k}={s.args.get(k)}" for k in ("recipient", "amount", "password", "id") if k in s.args)
        + f" -> {s.label}" for s in ss) or "(no tool calls)"
    lines.append(f"| {n} | `{e}` | {data.episodes[e].security} | {desc} |")
with open(os.path.join(RESULTS, "label_audit_sample.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("\n".join(lines))
