"""Repaired arms of the 17 November 2026 study: the unchanged authority front followed by the typed amount verifier.

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. Nothing frozen is edited. Each repaired arm is the
corresponding scored arm built by its unchanged factory, with one difference: the lexical direct-value constraint
(value_guard.py, which carries defect C2) is replaced by the typed verifier of amount_verifier.py.

  G3_math   G3 (revision-3 matcher; release iff the call is supported)                    + typed verifier
  GV_math   competitive-study GV (front + predicates, no learner), value_guard=False      + typed verifier
  HV_math   competitive-study HVx (front + saved F4 ridge, calibration, two-verdict rule),
            value_guard=False, SAME saved coefficients as HV/HVx                          + typed verifier

GV_math and HV_math share the front and the verifier and differ only in the learned decision. The verifier can only turn
a release (Allow) into a refusal: status 'mismatch' -> Block (source amount_mismatch); 'unresolved' -> Escalate (source
amount_unresolved), withheld because no reviewer exists in these recordings. It reads the trusted request and, from tool
results that were executed, only the structured fields named in amount_verifier.py. It reads no label, task identifier,
injection identifier or outcome.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/repair_study", "experiments/competitive_study", "experiments/g3_integration", "experiments/improve_study",
           "experiments/pilot"):
    sys.path.insert(0, str(ROOT / _p))

import amount_verifier as AV  # noqa: E402
from rem.core.results import Verdict  # noqa: E402

ARMS = ("G3_math", "GV_math", "HV_math")
BASE = {"G3_math": "G3", "GV_math": "GV", "HV_math": "HVx"}
FITTED = ("HV_math",)
SOURCES = {"mismatch": (Verdict.BLOCK, "amount_mismatch"), "unresolved": (Verdict.ESCALATE, "amount_unresolved")}


def attach_amount_verifier(guard):
    compiled = AV.compile_bindings(guard.episode.objective)
    hist = AV.History()
    base_decide, base_evaluate, base_ingest = guard.decide, guard.evaluate, guard.ingest

    def decide(c):
        verdict, source, details = base_decide(c)          # the front also records every proposal for fulfilment
        res = AV.verify(compiled, hist, c.tool, c.args)
        details = {**details, "amount": (res.status, res.expected, res.reason)}
        if verdict is Verdict.ALLOW and res.status in SOURCES:
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
        hist.rows.append((tool, text, bool(executed)))
        return base_ingest(tool, text, executed)

    guard.decide, guard.evaluate, guard.ingest = decide, evaluate, ingest
    guard.amount_history = hist
    return guard


def make_guard(arm, cell, extra, ep, st):
    """cell: integration-package cell (saved fits); extra: competitive-study cell. No refit happens here."""
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm}")
    if arm == "G3_math":
        import improve_v3 as V3    # the factory the integration package uses for G3 (run.guard -> make_guard_v3)
        g = V3.make_guard_v3("G3", cell, ep, st)
    else:
        import guards as G         # competitive study
        g = G.make_guard(BASE[arm], cell, extra, ep, st, value_guard=False)
    return attach_amount_verifier(g)
