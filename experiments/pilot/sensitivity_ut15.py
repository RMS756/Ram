"""POST-HOC sensitivity (disclosed): exclude user_task_15 from evaluation.

Found after held-out predictions were computed: user_task_15's objective itself
contains the attacker IBAN, so transfers to it in user_task_15 episodes are
label-ambiguous beyond amendment AM-1. No model is refitted; held-out
predictions and replay outcomes of the primary run are re-summarised without
user_task_15 episodes. This is NOT a pre-registered analysis.
"""

import collections

import numpy as np

from common import provenance, write_json
from data import build
from run_main import B, SEED, load_state, prob_metrics
from rem.evaluation.bootstrap import grouped_bootstrap

data = build("primary")
fits = load_state("crossfit")
prim = fits["label_nll_primary"]
keep = np.array([s.user_task_id != "user_task_15" for s in data.steps])
ut15 = ~keep
out = {"provenance": provenance(), "post_hoc": True,
       "user_task_15_positive_steps": int(data.y[ut15].sum()),
       "user_task_15_positive_steps_without_injection_in_context": int(sum(
           1 for i in np.flatnonzero(ut15) if data.y[i] and not data.steps[i].after_change_point)),
       "heldout_metrics_excluding_ut15": prob_metrics(data.y[keep], prim.p_cal[keep]),
       "heldout_metrics_all": prob_metrics(data.y, prim.p_cal)}
res = load_state("replay_main")
rm = load_state("rmod")
by = collections.defaultdict(dict)
for eid, c, u, s, err, aud in res:
    by[eid][c] = (u, s)
valid = [e for e, ok in rm["agree"].items() if ok and data.episodes[e].user_task_id != "user_task_15"]
att = [e for e in valid if data.episodes[e].attacked]
ben = [e for e in valid if not data.episodes[e].attacked]
kw = dict(resamples=B["resamples"], seed=SEED, level=B["interval"])
out["replay_excluding_ut15"] = {}
for c in ("B0", "REM_step_level_no_reviewer", "REM_episode_level_no_reviewer", "REM_episode_level_idealized",
          "B1_step_level_no_reviewer", "B1_episode_level_no_reviewer"):
    out["replay_excluding_ut15"][c] = {
        "ASR": grouped_bootstrap(att, lambda e: data.episodes[e].injection_task_id, lambda s: float(np.mean([by[e][c][1] for e in s])), **kw),
        "benign_utility": grouped_bootstrap(ben, lambda e: data.episodes[e].user_task_id, lambda s: float(np.mean([by[e][c][0] for e in s])), **kw)}
write_json("sensitivity_post_hoc_exclude_user_task_15.json", out)
print({k: v for k, v in out.items() if k != "provenance"})
