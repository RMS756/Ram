"""Episode-level re-analysis of the frozen REM ablation outputs (REM_ABLATION_STUDY, commit 355355a).

No replay is re-run: the per-episode, per-arm records of REM_ABLATION_STUDY/05_EPISODE_RESULTS.jsonl.gz (54,963
records, checked by sha256 against REM_ABLATION_STUDY/results/output_hashes.sha256) are re-scored with the
EPISODE as the unit of analysis, as required by the comparative-phase protocol (section A).

Per episode and arm: replay attack outcome (AgentDojo security on the NO-ADAPT replay), any attack-labelled
restricted call released, utility; for benign episodes, any restricted call withheld (false-positive episode).
Paired against A0 (full REM): discordant counts, exact McNemar p, grouped-bootstrap difference (clusters:
injection task for attacked episodes, user task for benign episodes; [PD] grouping pending confirmation).
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from rem.evaluation.bootstrap import grouped_bootstrap  # noqa: E402

SRC = ROOT / "REM_ABLATION_STUDY" / "05_EPISODE_RESULTS.jsonl.gz"
OUT = ROOT / "REM_COMPARATIVE_EVALUATION_PHASE" / "results" / "ablation_episode_level.json"
ARMS = ["B0", "A0", "A1a", "A1b", "A2", "AIC", "A3", "A3P", "A4"]
RESTRICTED = {"send_money", "schedule_transaction", "update_scheduled_transaction", "update_user_info", "update_password"}
KW = dict(resamples=2000, seed=20261027, level=0.95)   # values of configs/exploratory/pilot_e0.yaml (bootstrap block)


def mcnemar(b, c):
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def main():
    want = [l.split()[0] for l in (ROOT / "REM_ABLATION_STUDY/results/output_hashes.sha256").read_text().splitlines() if "05_EPISODE" in l]
    got = hashlib.sha256(SRC.read_bytes()).hexdigest()
    assert want and want[0] == got, "ablation episode file does not match its recorded hash (fail closed)"
    E = collections.defaultdict(dict)
    meta = {}
    for line in gzip.open(SRC, "rt"):
        r = json.loads(line)
        k = (r["population"], r["episode"])
        rc = [c for c in r["calls"] if c[0] in RESTRICTED]
        E[k][r["arm"]] = {"utility": r["replay_utility"], "attack_outcome": r["replay_attack_outcome"],
                          "attack_call_released": any(c[3] == 1 and c[2] for c in rc),
                          "any_withheld": any(not c[2] for c in rc)}
        meta[k] = (r["user_task"], r["injection_task"])
    res = {"source": str(SRC.relative_to(ROOT)), "source_sha256": got, "unit": "episode", "bootstrap": KW, "populations": {}}
    for pop in sorted({p for p, _ in E}):
        keys = [k for k in E if k[0] == pop]
        att = [k for k in keys if meta[k][1]]
        ben = [k for k in keys if not meta[k][1]]
        inj = lambda k: meta[k][1]   # noqa: E731
        usr = lambda k: meta[k][0]   # noqa: E731
        R = {"attacked": len(att), "benign": len(ben), "arms": {}, "paired_vs_A0": {}}
        for a in ARMS:
            m = {}
            if att:
                m["attack_outcomes"] = sum(E[k][a]["attack_outcome"] for k in att)
                m["episodes_attack_call_released"] = sum(E[k][a]["attack_call_released"] for k in att)
                m["attacked_utility"] = sum(E[k][a]["utility"] for k in att)
            if ben:
                m["benign_completed"] = sum(E[k][a]["utility"] for k in ben)
                m["benign_episodes_with_withheld_call"] = sum(E[k][a]["any_withheld"] for k in ben)
            R["arms"][a] = m
            if a == "A0":
                continue
            d = {}
            for name, items, cl, fld in (("attack_outcome", att, inj, "attack_outcome"), ("attack_call_released", att, inj, "attack_call_released"),
                                         ("attacked_utility", att, inj, "utility"), ("benign_completion", ben, usr, "utility"),
                                         ("benign_false_positive", ben, usr, "any_withheld")):
                if not items:
                    continue
                x = sum(1 for k in items if E[k][a][fld] and not E[k]["A0"][fld])
                y = sum(1 for k in items if E[k]["A0"][fld] and not E[k][a][fld])
                d[name] = {"arm_only": x, "A0_only": y, "mcnemar_exact_p": mcnemar(x, y),
                           "difference_arm_minus_A0": grouped_bootstrap(items, cl, lambda s, fld=fld: float(np.mean([E[k][a][fld] - E[k]["A0"][fld] for k in s])), **KW)}
            R["paired_vs_A0"][a] = d
        res["populations"][pop] = R
        print(pop, {a: (R["arms"][a].get("attack_outcomes"), R["arms"][a].get("episodes_attack_call_released"), R["arms"][a].get("benign_completed")) for a in ARMS})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
