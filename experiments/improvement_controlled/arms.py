"""Arms of the controlled improvement study (18 November 2026).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN].

Frozen arms are delegated, unchanged, to their original modules:
  B0        allow every call
  PG        Progent's manual banking policy on every call (as improve.py arm "PG"; REM's replay checker of commit 9befb41)
  GV_math2  repair-study v2 (repaired_arms_v2)
  C1, C2PG, C3PG   progent-competitive study (contract_arms)

Parameterised arms re-implement contract_arms.make_guard with explicit switches, so that one component can be removed
or added at a time. With the switches of a frozen arm the decisions must equal the frozen arm (tests/test_improvement_controlled.py):
  ledger    per-instruction allowance tracking (off: every eligible contract always has allowance)
  pg        Progent manual policy after the front
  learner   stored ridge F4 + Platt + two-verdict expected loss after the contract witness (may only withhold)
  compile   contract compiler (frozen contracts.compile_contracts, or an evidence-resolution variant)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/improvement_controlled", "experiments/progent_competitive", "experiments/repair_study", "experiments/competitive_study",
           "experiments/improve_study", "experiments/authz_study", "experiments/g3_integration", "experiments/pilot", ""):
    sys.path.insert(0, str(ROOT / _p) if _p else str(ROOT))

import contracts as K  # noqa: E402
import evidence_resolution as ER  # noqa: E402
import contract_arms as CA  # noqa: E402
import amount_verifier_v2 as V2  # noqa: E402
import repaired_arms_v2 as RA2  # noqa: E402
import study as S  # noqa: E402
from permission_v3 import DEFAULT_OPTS3, RuntimePermissionV3  # noqa: E402
from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.algorithms.decision.loss_matrix import build_loss_grid  # noqa: E402
from rem.algorithms.detection.ridge_logistic import sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard  # noqa: E402
from amount_verifier import _fmt as V1fmt  # noqa: E402

FROZEN = ("B0", "PG", "GV_math2", "C1", "C2PG", "C3PG")


class NoLedger(K.Ledger):
    """Ablation: allowance never runs out (reserve / settle are recorded but never limit)."""

    def remaining(self, c):
        return 1


PARAM = {
    "C1p": dict(ledger=True, pg=False, learner=False, compile="frozen"),        # parity copy of C1
    "C2PGp": dict(ledger=True, pg=True, learner=False, compile="frozen"),       # parity copy of C2PG
    "C3PGp": dict(ledger=True, pg=True, learner=True, compile="frozen"),        # parity copy of C3PG
    "C1_noledger": dict(ledger=False, pg=False, learner=False, compile="frozen"),
    "C1L": dict(ledger=True, pg=False, learner=True, compile="frozen"),
    "C1I": dict(ledger=True, pg=False, learner=False, compile="e1", e2=True),         # evidence resolution E1 + E2
    "C1IL": dict(ledger=True, pg=False, learner=True, compile="e1", e2=True),
}
COMPILERS = {"frozen": K.compile_contracts, "e1": ER.compile_e1}


def register_compiler(name, fn):
    COMPILERS[name] = fn


def make_param_guard(cfg, cell, ep, st):
    gc = GuardConfig(st.spec, st.detector, cell["reference"], st.tier_map, st.restricted, "step_level", "no_reviewer")
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    rp = RuntimePermissionV3(ep.objective, dict(CA.OPTS_C))
    rp_feat = RuntimePermissionV3(ep.objective, dict(DEFAULT_OPTS3)) if cfg["learner"] else None
    contracts = COMPILERS[cfg["compile"]](ep.objective)
    kdecide = ER.decide if cfg["compile"] == "e1" else K.decide
    refunds = ER.compile_e2(ep.objective) if cfg.get("e2") else []
    ledger = K.Ledger() if cfg["ledger"] else NoLedger()
    hist = V2.History()
    predicates = S.rm.predicates()
    pol2 = A3Policy(build_loss_grid(S.rm.loss_spec(cell["rmod"]), "controlled study learned stage"), predicates,
                    tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.ESCALATE, Verdict.MODIFY))
    ridge = cell["models"][("F4", "y")]
    pg = CA._pg() if cfg["pg"] else None
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
        rw = None
        f0, avail0 = guard.tracker.features(c.tool, c.args)
        if cfg["learner"] and is_r:                       # learned score computed for every restricted call (record only)
            evf0 = rp_feat.evidence(guard.tracker, c.tool, c.args, c.tier)
            x0 = dict(f0)
            x0.update(evf0.features())
            s0 = CA._linear(ridge, x0)
            info["p_all"] = float(sigmoid(ridge["g1"] * s0 + ridge["g0"])) if not ridge["failed"] else float(sigmoid(s0))
        front_block = is_r and (ev.overall == "denied" or not ev.authority)
        if front_block and refunds:
            rw = ER.refund_witness(refunds, ledger, hist, c.tool, c.args)
            if rw is not None:
                front_block = False
                info["e2"] = rw.cid
        if front_block:
            v, src = Verdict.BLOCK, "permission_guard_authority_v3"
        elif pg is not None and not pg.allowed(c.tool, dict(c.args)):
            v, src, info["stage"] = Verdict.BLOCK, "progent_policy", "progent_policy"
        else:
            f, avail = guard.tracker.features(c.tool, c.args)
            forced = predicates.evaluate(c.tool, c.tier, avail)
            if forced.verdict is not None:
                v, src, info["stage"] = forced.verdict, forced.source, "predicate"
            else:
                k = (K.Decision("verified", rw.cid, (V1fmt(rw.amount),), "refund licence from the single incoming record (E2)")
                     if rw is not None else kdecide(contracts, ledger, hist, c.tool, c.args))
                det["contract"] = (k.status, k.expected, k.reason, k.witness)
                info["stage"] = "contract"
                if k.status in ("mismatch", "exhausted"):
                    v, src = Verdict.BLOCK, f"contract_{k.status}"
                elif k.status == "unresolved":
                    v, src = Verdict.ESCALATE, "contract_unresolved"
                elif cfg["learner"] and is_r:
                    evf = rp_feat.evidence(guard.tracker, c.tool, c.args, c.tier)
                    x = dict(f)
                    x.update(evf.features())
                    s = CA._linear(ridge, x)
                    p = float(sigmoid(ridge["g1"] * s + ridge["g0"])) if not ridge["failed"] else float(sigmoid(s))
                    d = pol2.decide(p, c.tier, c.tool, avail)
                    v, src = d.verdict, d.source
                    info.update(stage="learned", s=float(s), p=p, tier=c.tier)
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


def factory(key=("S1", "injection_task_0")):
    """Guard factory on the stored S1 cell `key` (as the fixtures, diagnostics and scripted loop of the earlier studies)."""
    import progent_manual as PGM
    import rs_run as V1R
    st = V1R.common.make_setup()
    cells, cs = V1R.J.load("cells"), V1R.C.load("cs_cells")
    PGM.load()

    def build(arm, ep):
        return build_cell(arm, ep, cells[key], cs[key], st)
    build.setup = st
    return build


def build_cell(arm, ep, cell, extra, st):
    import progent_manual as PGM
    if arm in CA.ARMS:
        return CA.make_guard(arm, cell, extra, ep, st)
    if arm in RA2.ARMS:
        return RA2.make_guard(arm, cell, extra, ep, st)
    if arm in PARAM:
        return make_param_guard(PARAM[arm], cell, ep, st)
    gc = GuardConfig(st.spec, st.detector, cell["reference"], st.tier_map, st.restricted, "step_level", "no_reviewer")
    if arm == "B0":
        return RemGuard(gc, None, lambda c: (Verdict.ALLOW, "allow_all", {}), st.labeler, ep)
    if arm == "PG":
        return RemGuard(gc, None, lambda c: ((Verdict.ALLOW if PGM.allowed(c.tool, c.args) else Verdict.BLOCK),
                                             "progent_manual_policy", {}), st.labeler, ep)
    raise ValueError(f"unknown arm {arm}")
