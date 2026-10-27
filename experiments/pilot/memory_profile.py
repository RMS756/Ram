"""Peak traced allocation of REM per-step evaluation (tracemalloc), EXPLORATORY.

Measures RemGuard.evaluate only (features, score, verdict, mitigation, audit
record), excluding tool execution and environment set-up, on 300 episodes.
"""

import tracemalloc

import numpy as np

from common import make_setup, provenance, write_json
from data import build, reference_from_mask
from run_main import G, _mk_decide, _mk_scorer, build_policies, load_state
from rem.integration.agentdojo_replay import GuardConfig, RemGuard, replay_episode

st = make_setup()
data = build("primary")
fits = load_state("crossfit")
pol = build_policies(fits, load_state("rmod")["rmod"])
G.update(policies=pol, fits=fits)
eids = sorted(data.episodes)[:: max(1, len(data.episodes) // 300)][:300]
peaks = []
for e in eids:
    f = data.episode_fold[e]
    gc = GuardConfig(st.spec, st.detector, reference_from_mask(data, data.fold != f), st.tier_map, st.restricted,
                     "episode_level", "no_reviewer")
    g = RemGuard(gc, _mk_scorer("label_nll_primary")(f), _mk_decide("A3_episode_level")(f), st.labeler, data.episodes[e])
    orig = g.evaluate

    def wrapped(tool, args, orig=orig):
        tracemalloc.start()
        try:
            return orig(tool, args)
        finally:
            peaks.append(tracemalloc.get_traced_memory()[1])
            tracemalloc.stop()
    g.evaluate = wrapped
    replay_episode(data.episodes[e], st.suite, g)
res = {"provenance": provenance(), "steps_measured": len(peaks), "episodes": len(eids),
       "peak_bytes_per_step_median": float(np.median(peaks)), "peak_bytes_per_step_p95": float(np.percentile(peaks, 95)),
       "peak_bytes_per_step_max": float(np.max(peaks))}
write_json("latency_memory_profile.json", res)
print(res)
