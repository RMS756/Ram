"""Repaired arms, version 2 (dated amendment of 17 November 2026, after the independent review of commit 621a271).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. Version-1 arms (repaired_arms.py) are unchanged.

Stage order, as executed (and as the thesis must describe it):
  1. authority front (unchanged; GV/HVx factory with value_guard=False, or G3);
  2. the arm's rule for calls that pass the front: none (GV), the stored ridge model and calibration (HV), G3's rule;
  3. ONLY IF steps 1-2 release the call (Allow): the typed amount verifier, version 2; mismatch -> Block, unresolved ->
     Escalate (withheld, no reviewer). In version 1 the verifier was computed for every call and applied only to Allow;
     version 2 does not compute it for calls already refused, so "the verifier evaluated this call" is literal.

Arms:  G3_math2, GV_math2, HV_math2         acceptance repair only (D3 coverage, D4 single witness)
       GV_math2x, HV_math2x                 the same plus the appositive grammar extension (measured separately)
GV_math2 and HV_math2 (and GV_math2x and HV_math2x) differ only in step 2.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/repair_study", "experiments/competitive_study", "experiments/g3_integration", "experiments/improve_study",
           "experiments/pilot"):
    sys.path.insert(0, str(ROOT / _p))

import amount_verifier_v2 as AV2  # noqa: E402
from rem.core.results import Verdict  # noqa: E402

ARMS = ("G3_math2", "GV_math2", "HV_math2", "GV_math2x", "HV_math2x")
BASE = {"G3_math2": "G3", "GV_math2": "GV", "HV_math2": "HVx", "GV_math2x": "GV", "HV_math2x": "HVx"}
EXTENSION = {"GV_math2x", "HV_math2x"}
FITTED = ("HV_math2", "HV_math2x")
SOURCES = {"mismatch": (Verdict.BLOCK, "amount_mismatch"), "unresolved": (Verdict.ESCALATE, "amount_unresolved")}


def attach_amount_verifier_v2(guard, appositive: bool = False):
    compiled = AV2.compile_bindings(guard.episode.objective, appositive=appositive)
    hist = AV2.History()
    base_decide, base_evaluate, base_ingest = guard.decide, guard.evaluate, guard.ingest

    def decide(c):
        verdict, source, details = base_decide(c)
        if verdict is not Verdict.ALLOW:
            return verdict, source, {**details, "amount_evaluated": False}
        res = AV2.verify(compiled, hist, c.tool, c.args)
        details = {**details, "amount_evaluated": True, "amount": (res.status, res.expected, res.reason)}
        if res.status in SOURCES:
            v, src = SOURCES[res.status]
            return v, src, {**details, "amount_veto": True, "stage_before_veto": source}
        return verdict, source, details

    def evaluate(tool, args):
        start = time.perf_counter()
        result = base_evaluate(tool, args)
        row = guard.audit[-1]
        if row["verdict_source"].startswith("amount_"):
            row["probability_used_for_verdict"] = False
            row["risk_table"] = "not_applicable"
        row["rem_latency_full_ms"] = (time.perf_counter() - start) * 1000
        guard.full_latencies_ms[-1] = row["rem_latency_full_ms"]
        return result

    def ingest(tool, text, executed):
        hist.rows.append((tool, None, text, bool(executed)))
        return base_ingest(tool, text, executed)

    guard.decide, guard.evaluate, guard.ingest = decide, evaluate, ingest
    guard.amount_history = hist
    return guard


def make_guard(arm, cell, extra, ep, st):
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm}")
    if BASE[arm] == "G3":
        import improve_v3 as V3
        g = V3.make_guard_v3("G3", cell, ep, st)
    else:
        import guards as G
        g = G.make_guard(BASE[arm], cell, extra, ep, st, value_guard=False)
    return attach_amount_verifier_v2(g, appositive=arm in EXTENSION)
