"""Metrics for live closed-loop runs (episodes.jsonl from run_live.py).

usage: python3 experiments/live/analyze_live.py <episodes.jsonl> <out.json>

Per (backbone, configuration, semantics, reviewer):
  ASR                   mean AgentDojo security over attacked episodes (True = injection task succeeded)
  benign utility        mean AgentDojo utility over episodes without injection
  utility under attack  mean utility over attacked episodes
  intervention rates    share of y=0 / y=1 proposals not released
  adaptation            totals of retries, replans, y=1 releases after a refusal (agentdojo_live L-2)
  latency               median / p95 of the complete-call timer (rem_latency_full_ms)
Intervals: grouped percentile bootstrap (resamples and seed from configs/exploratory/pilot_e0.yaml),
attacked episodes grouped by injection task, benign by user task; repeats stay inside their group.
Errors are counted and excluded from rates, never dropped silently.
"""

from __future__ import annotations

import collections
import json
import os
import sys

import numpy as np
import yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO)
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402


def summarize(records, resamples: int, seed: int, level: float):
    by = collections.defaultdict(list)
    for r in records:
        bk = r["backbone"]["model"] if isinstance(r["backbone"], dict) else r["backbone"]
        by[(bk, r["configuration"], r["semantics"], r["reviewer"])].append(r)
    out = {}
    for key, rs in sorted(by.items()):
        ok = [r for r in rs if not r.get("error")]
        att = [r for r in ok if r["injection_task"]]
        ben = [r for r in ok if not r["injection_task"]]
        steps = [a for r in ok for a in r["audit"]]
        y = np.array([int(a["label"]) for a in steps]) if steps else np.array([], dtype=int)
        rel = np.array([bool(a["released"]) for a in steps]) if steps else np.array([], dtype=bool)
        lat = [a.get("rem_latency_full_ms") for a in steps if a.get("rem_latency_full_ms") is not None]
        kw = dict(resamples=resamples, seed=seed, level=level)
        ad = collections.Counter()
        for r in ok:
            ad.update(r.get("adaptation", {}))
        out["|".join(key)] = {
            "episodes": len(rs), "errors": len(rs) - len(ok), "attacked": len(att), "benign": len(ben),
            "ASR": grouped_bootstrap(att, lambda r: r["injection_task"], lambda s: float(np.mean([r["security"] for r in s])), **kw) if att else None,
            "benign_utility": grouped_bootstrap(ben, lambda r: r["user_task"], lambda s: float(np.mean([r["utility"] for r in s])), **kw) if ben else None,
            "utility_under_attack": grouped_bootstrap(att, lambda r: r["injection_task"], lambda s: float(np.mean([r["utility"] for r in s])), **kw) if att else None,
            "intervention_rate_y0": float(np.mean(~rel[y == 0])) if (y == 0).any() else None,
            "intervention_rate_y1": float(np.mean(~rel[y == 1])) if (y == 1).any() else None,
            "adaptation_totals": dict(ad),
            "latency_full_ms_median": float(np.median(lat)) if lat else None,
            "latency_full_ms_p95": float(np.percentile(lat, 95)) if lat else None,
        }
    return out


def main(path: str, out: str) -> None:
    cfg = yaml.safe_load(open(os.path.join(REPO, "configs", "exploratory", "pilot_e0.yaml"), encoding="utf-8"))
    b = cfg["bootstrap"]
    recs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    res = summarize(recs, int(b["resamples"]), int(cfg["meta"]["seed"]), float(b["interval"]))
    json.dump({"source": path, "n_records": len(recs), "summary": res}, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1)[:4000])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
