"""Firing rates of evidence features on legitimate state-changing steps vs attack steps (R2, descriptive)."""
import collections

import numpy as np

from common import provenance, write_json
from data import build, reference_from_mask

d = build("primary")
refs = {f: reference_from_mask(d, d.fold != f) for f in set(d.fold.tolist())}
out = {"provenance": provenance(), "note": "x_beh4 uses the benign transition set of the step's outer-fold fitting portion"}
for name, mask in (("benign_episode_state_changing_steps", lambda s: s.injection_task_id is None and s.tier >= 2),
                   ("attack_steps_y1", lambda s: s.label == 1)):
    idx = [i for i, s in enumerate(d.steps) if mask(s)]
    rates = collections.defaultdict(list)
    for i in idx:
        s = d.steps[i]
        for k in ("x_ctx2", "x_beh1", "x_beh3", "x_act1", "x_act2", "x_act3"):
            rates[k].append(float(s.features[k] > 0))
        rates["x_beh2_eq_1"].append(float(s.features["x_beh2"] == 1.0))
        rates["x_beh4"].append(float(s.transition not in refs[d.fold[i]].transitions))
    out[name] = {"n": len(idx), **{k: float(np.mean(v)) for k, v in rates.items()}}
write_json("feature_firing_rates.json", out)
print(out)
