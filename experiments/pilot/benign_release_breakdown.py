"""Verdicts on steps of benign (no-injection) episodes by tier, REM vs B1 (observe-only, held-out)."""

import collections

from common import provenance, write_json
from data import build
from run_main import load_state

data = build("primary")
res = load_state("observe_verdicts")
out = {"provenance": provenance()}
for name in ("REM_step_level", "REM_episode_level", "REMnoEsc_step_level", "B1"):
    vs = res[name][0]
    by = collections.defaultdict(collections.Counter)
    for i, s in enumerate(data.steps):
        if s.injection_task_id is None:
            by[int(s.tier)][vs[i]] += 1
    sc = [k for k in by if k >= 2]
    out[name] = {"by_tier": {k: dict(v) for k, v in sorted(by.items())},
                 "state_changing_released": sum(by[k]["allow"] for k in sc),
                 "state_changing_total": sum(sum(by[k].values()) for k in sc)}
write_json("benign_release_breakdown.json", out)
print({k: (v["state_changing_released"], v["state_changing_total"]) for k, v in out.items() if k != "provenance"})
