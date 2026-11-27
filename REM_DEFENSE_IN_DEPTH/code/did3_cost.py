"""DiD-3c cost sensitivity (protocol 52_COST_SENSITIVITY_PROTOCOL.md). Writes results/did3_cost.json.
usage: python3 REM_DEFENSE_IN_DEPTH/code/did3_cost.py"""
from __future__ import annotations

import itertools
import json
import multiprocessing as mp
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import did3_common as D  # noqa: E402
from did3_run import ARMS  # noqa: E402

GR = D.rm.CFG["grid"]
CELLS = list(itertools.product(GR["C_miss_multiplier"], GR["C_esc"], GR["amount_limit"]))
COST_ARMS = ("B1", "B9", "X0")


def _job(job):
    cell, arm, eid = job
    ep = D.G["eps"]["POP-P"][eid]
    r = D.run_episode(ARMS[arm], ep, cell=cell)
    att = ep.attacked
    return (cell, arm, att, int(r["security"]) if att else 0, int(r["utility"]) if not att else 0,
            sum(1 for c in r["calls"] if c[0] == 0 and c[2] and not c[1]),
            sum(1 for c in r["calls"] if c[3] == "escalate"), bool(r["error"]))


def main():
    D.setup()
    eids = sorted(D.G["eps"]["POP-P"])
    jobs = [(c, a, e) for c in CELLS for a in COST_ARMS for e in eids]
    t0 = time.time()
    agg = {}
    with mp.get_context("fork").Pool(4) as pool:
        for cell, arm, att, s, u, w, esc, err in pool.imap_unordered(_job, jobs, chunksize=128):
            k = f"{cell[0]}|{cell[1]}|{cell[2]}|{arm}"
            a = agg.setdefault(k, {"C_miss_mult": cell[0], "C_esc": cell[1], "amount_limit": cell[2], "arm": arm,
                                   "successful_attacks": 0, "benign_tasks_completed": 0,
                                   "legit_sc_calls_withheld": 0, "escalations": 0, "errors": 0})
            a["successful_attacks"] += s
            a["benign_tasks_completed"] += u
            a["legit_sc_calls_withheld"] += w
            a["escalations"] += esc
            a["errors"] += err
    out = {"protocol": "52_COST_SENSITIVITY_PROTOCOL.md", "classification": "EXPLORATORY", "cells": len(CELLS),
           "n_attacked": sum(D.G["eps"]["POP-P"][e].attacked for e in eids),
           "n_benign": sum(not D.G["eps"]["POP-P"][e].attacked for e in eids), "rows": sorted(agg.values(), key=lambda r: (r["arm"], r["C_miss_mult"], r["C_esc"], r["amount_limit"]))}
    with open(os.path.join(D.REPO, "REM_DEFENSE_IN_DEPTH", "results", "did3_cost.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"{len(jobs)} replays in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
