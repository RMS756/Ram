"""Check the random stratum of the human label-audit package against its generator (R4).

usage: PILOT_RESULTS_DIR=<dir with steps.pkl> python3 REM_FINAL_THESIS/verification/check_label_audit_package_R4.py
Replays the seeded draw of experiments/pilot/r2_analyses.label_audit_pack (no labels are read or changed)
and compares it with results/pilot_R2/label_audit_human_package.csv.
"""
import collections
import csv
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'experiments', 'pilot'))
import numpy as np  # noqa: E402

from common import load_config  # noqa: E402
from data import build  # noqa: E402

CFG = load_config()
data = build("primary")
by = collections.defaultdict(list)
for s in data.steps:
    by[s.episode_id].append(s)
rng = np.random.default_rng(CFG["meta"]["seed"] + 1)
att_eps = sorted(e for e in data.episodes if data.episodes[e].attacked)
drawn = list(rng.choice(att_eps, size=30, replace=False))
with_steps = [e for e in drawn if by[e]]
items = sum(len(by[e]) for e in drawn)
rows = list(csv.DictReader(open(os.path.join(ROOT, 'results', 'pilot_R2', 'label_audit_human_package.csv'), encoding='utf-8')))
pkg = [r for r in rows if r['sample_stratum'] == 'random_episode']
res = {
    'random_drawn': len(drawn), 'random_with_steps': len(with_steps), 'random_items': items,
    'package_random_items': len(pkg), 'package_random_episodes': len({r['episode_id'] for r in pkg}),
    'package_matches_generator': sorted({r['episode_id'] for r in pkg}) == sorted(with_steps) and len(pkg) == items,
    'package_items_total': len(rows),
    'strata': dict(collections.Counter(r['sample_stratum'] for r in rows)),
    'human_annotations_present': sum(1 for r in rows if r['annotator_label_0_1'].strip()),
}
out = os.path.join(ROOT, 'REM_FINAL_THESIS', 'verification', 'label_audit_package_check_R4.json')
json.dump(res, open(out, 'w', encoding='utf-8'), indent=1)
print(res)
