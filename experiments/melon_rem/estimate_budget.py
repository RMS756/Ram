"""Project the cost of the final run from MEASURED pilot usage (no price or token count is assumed).

usage: python3 experiments/melon_rem/estimate_budget.py <pilot_run>/episodes.jsonl <prices.yaml> \
           --cases 160 --repeats R [--margin 0.25]

prices.yaml: {<backbone>: {input: USD_per_1M, output: USD_per_1M}, text-embedding-3-large: {embedding: USD_per_1M}}
(taken by the operator from the provider's price list on the day; the pilot ledger already used the same prices).

Per condition c, from the pilot episodes (all cases, attacked and benign, errors included because they are billed):
  mean_c = mean per-episode cost recomputed from recorded tokens x prices
  p95_c  = 95th percentile per-episode cost
Projection for N cases x R repeats:  sum_c mean_c * N * R      (central)
                                      sum_c p95_c  * N * R      (conservative)
and the recommended cap = conservative * (1 + margin). The pilot mixes 9 attacked and 4 benign cases;
the full set has 144 attacked and 16 benign, so costs are also reported separately and re-weighted.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict

import yaml


def cost(r, prices, backbone):
    t = r.get("tokens") or {}
    pb, pe = prices[backbone], prices["text-embedding-3-large"]
    return (t.get("input", 0) * pb["input"] + t.get("output", 0) * pb["output"] + t.get("embedding", 0) * pe["embedding"]) / 1e6


def p95(xs):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(0.95 * (len(xs) - 1))))] if xs else 0.0


def project(recs, prices, cases_attacked=144, cases_benign=16, repeats=1, margin=0.25):
    by = defaultdict(lambda: {"attacked": [], "benign": []})
    for r in recs:
        by[r["condition"]]["attacked" if r.get("injection_task") else "benign"].append(cost(r, prices, r["backbone"]))
    out = {"per_condition": {}, "central_usd": 0.0, "conservative_usd": 0.0}
    for c, d in by.items():
        ma = sum(d["attacked"]) / len(d["attacked"]) if d["attacked"] else 0.0
        mb = sum(d["benign"]) / len(d["benign"]) if d["benign"] else 0.0
        central = (ma * cases_attacked + mb * cases_benign) * repeats
        cons = (p95(d["attacked"]) * cases_attacked + p95(d["benign"]) * cases_benign) * repeats
        out["per_condition"][c] = {"mean_attacked_episode_usd": ma, "mean_benign_episode_usd": mb,
                                   "p95_attacked_episode_usd": p95(d["attacked"]), "p95_benign_episode_usd": p95(d["benign"]),
                                   "pilot_episodes": len(d["attacked"]) + len(d["benign"]),
                                   "central_usd": central, "conservative_usd": cons}
        out["central_usd"] += central
        out["conservative_usd"] += cons
    out["recommended_cap_usd"] = out["conservative_usd"] * (1 + margin)
    out["note"] = "Projection from a small pilot; per-episode cost varies with agent behaviour. Re-check after the first 10% of the final run."
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes")
    ap.add_argument("prices")
    ap.add_argument("--attacked-cases", type=int, default=144)
    ap.add_argument("--benign-cases", type=int, default=16)
    ap.add_argument("--repeats", type=int, required=True)
    ap.add_argument("--margin", type=float, default=0.25)
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(a.episodes, encoding="utf-8") if l.strip()]
    print(json.dumps(project(recs, yaml.safe_load(open(a.prices)), a.attacked_cases, a.benign_cases, a.repeats, a.margin), indent=1))
