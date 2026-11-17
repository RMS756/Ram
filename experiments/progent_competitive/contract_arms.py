"""Candidate arms C1, C2[PG] and C3[PG] of the study of 18 November 2026 (replay-capable; no model call).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. See 01_DESIGN_DECISION_RECORD.md.
Frozen components are imported, not edited: the revision-3 front (RuntimePermissionV3), the REM guard and predicates
D1/D2, the stored F4 ridge model and calibration, the A3 policy, and REM's replay adaptation of Progent's manual banking
policy (progent_manual.allowed).

Stage order, as executed:
  1. authority front: revision 3 with bind=False and fulfil=False (operation requested, effect, recipient authority,
     condition); a denied call or one without established authority is blocked;
  2. C2/C3 only: the Progent policy check (manual banking policy of commit 9befb41, REM's replay adaptation);
  3. declared predicates D1/D2 (as in GV);
  4. the financial contract witness (contracts.decide): verified/unconstrained -> continue; mismatch/exhausted ->
     Block; unresolved -> Escalate (withheld, no reviewer); no_contract -> continue (the front has licensed the call);
  5. C3 only: the stored ridge / calibration / two-verdict expected-loss decision on the frozen evidence features (as
     trained), which can only withhold;
  6. if released, the witnessing contract is reserved; the next result of that tool commits it (success) or releases it.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/progent_competitive", "experiments/repair_study", "experiments/competitive_study", "experiments/improve_study",
           "experiments/authz_study", "experiments/g3_integration", "experiments/pilot"):
    sys.path.insert(0, str(ROOT / _p))

import contracts as K  # noqa: E402
import amount_verifier_v2 as V2  # noqa: E402
import study as S  # noqa: E402
from permission_v3 import DEFAULT_OPTS3, RuntimePermissionV3  # noqa: E402
from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.algorithms.decision.loss_matrix import build_loss_grid  # noqa: E402
from rem.algorithms.detection.ridge_logistic import sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard  # noqa: E402

ARMS = ("C1", "C2PG", "C3PG")
FITTED = ("C3PG",)
OPTS_C = {"effect": True, "bind": False, "cond": True, "fulfil": False}
_PG = {}


def _pg():
    if not _PG:
        import progent_manual as PGM
        PGM.load()
        _PG["m"] = PGM
    return _PG["m"]


def _linear(rec, x):
    return rec["b0"] + sum(co * x[n] for n, co in zip(rec["order"], rec["coef"]))


def make_guard(arm, cell, extra, ep, st):
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm}")
    gc = GuardConfig(st.spec, st.detector, cell["reference"], st.tier_map, st.restricted, "step_level", "no_reviewer")
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    rp = RuntimePermissionV3(ep.objective, dict(OPTS_C))             # authority front of the candidates
    rp_feat = RuntimePermissionV3(ep.objective, dict(DEFAULT_OPTS3)) if arm == "C3PG" else None   # features as trained
    contracts = K.compile_contracts(ep.objective)
    ledger = K.Ledger()
    hist = V2.History()
    predicates = S.rm.predicates()
    pol2 = A3Policy(build_loss_grid(S.rm.loss_spec(cell["rmod"]), f"candidate {arm}"), predicates, tie_mode="record_chapter3_order",
                    exclude_from_expected_loss=(Verdict.ESCALATE, Verdict.MODIFY))
    ridge = cell["models"][("F4", "y")]
    pg = _pg() if arm in ("C2PG", "C3PG") else None
    orig_ingest = guard.ingest

    def ingest(tool, text, executed):
        rp.on_ingest(executed)
        if rp_feat is not None:
            rp_feat.on_ingest(executed)
        hist.rows.append((tool, None, text, bool(executed)))
        ledger.settle(tool, bool(executed))
        return orig_ingest(tool, text, executed)
    guard.ingest = ingest

    def decide(c):
        is_r = c.tool in restricted
        ev = rp.evidence(guard.tracker, c.tool, c.args, c.tier)
        info = {"stage": "front"}
        det = {"perm": (ev.overall, ev.base.recipient, ev.base.amount, ev.effect, ev.binding, ev.condition, ev.fulfilment, ev.authority)}
        v, src = Verdict.ALLOW, "candidate_release"
        if is_r and (ev.overall == "denied" or not ev.authority):
            v, src = Verdict.BLOCK, "permission_guard_authority_v3"
        elif pg is not None and not pg.allowed(c.tool, dict(c.args)):
            v, src, info["stage"] = Verdict.BLOCK, "progent_policy", "progent_policy"
        else:
            f, avail = guard.tracker.features(c.tool, c.args)
            forced = predicates.evaluate(c.tool, c.tier, avail)
            if forced.verdict is not None:
                v, src, info["stage"] = forced.verdict, forced.source, "predicate"
            else:
                k = K.decide(contracts, ledger, hist, c.tool, c.args)
                det["contract"] = (k.status, k.expected, k.reason, k.witness)
                info["stage"] = "contract"
                if k.status in ("mismatch", "exhausted"):
                    v, src = Verdict.BLOCK, f"contract_{k.status}"
                elif k.status == "unresolved":
                    v, src = Verdict.ESCALATE, "contract_unresolved"
                elif arm == "C3PG" and is_r:
                    evf = rp_feat.evidence(guard.tracker, c.tool, c.args, c.tier)
                    x = dict(f)
                    x.update(evf.features())
                    s = _linear(ridge, x)
                    p = float(sigmoid(ridge["g1"] * s + ridge["g0"])) if not ridge["failed"] else float(sigmoid(s))
                    d = pol2.decide(p, c.tier, c.tool, avail)
                    v, src = d.verdict, d.source
                    info.update(stage="learned", s=float(s), p=p)
                if v is Verdict.ALLOW and k.witness is not None:
                    ledger.reserve(c.tool, k.witness)
        det["cs"] = info
        rp.record(guard.tracker, c.tool, c.args)
        if rp_feat is not None:
            rp_feat.record(guard.tracker, c.tool, c.args)
        return v, src, det
    guard.decide = decide
    base_evaluate = guard.evaluate

    def evaluate(tool, args):
        start = time.perf_counter()
        result = base_evaluate(tool, args)
        row = guard.audit[-1]
        if row["verdict_source"].startswith(("contract_", "progent_")) or row["verdict_source"] == "candidate_release":
            row["probability_used_for_verdict"] = False
        row["rem_latency_full_ms"] = (time.perf_counter() - start) * 1000
        guard.full_latencies_ms[-1] = row["rem_latency_full_ms"]
        return result
    guard.evaluate = evaluate
    guard.contracts, guard.ledger = contracts, ledger
    return guard
