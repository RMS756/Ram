"""Improved REM-B ("REM-B2") and a safer hybrid, REM-B hardening study (19 November 2026).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN].
The frozen REM-B of the redesign study (experiments/architecture_redesign/rem_arch.py, frozen at 6705c07) is imported and
NOT edited. make_guard2 below is make_guard of that file with three repairs and two hybrid options behind switches; with
every switch off it is REM-B (parity test in tests/test_rem_b_hardening.py).

Repairs (02-04 of REM_B_HARDENING_VALIDATION_2026_11_19):
  R1 desig="nodigit"  Object-binding designators are taken only from request tokens that contain no digit. Identifiers
                      (IBANs, account numbers), amounts and dates are not descriptions of an object; they are checked by
                      the authority front and the contract. Fixes HO4 (IBAN "GB82WEST..." produced the designator "west").
  R2 sor=True         System-of-record evidence. Evidence resolution (E1 percentages, E2h refunds) and object binding read
                      the bank's own STRUCTURED records at decision time (sender, recipient, amount; standing-order id and
                      subject), queried by the enforcement layer itself, in addition to the reads the agent executed.
                      Free text (transaction subjects, files) is never used for amounts or beneficiaries. Fail-safe: more
                      records can only make a resolution ambiguous (withheld), never resolve a conflict.
  R3 deleg=True       Delegated judgement conditions. A credential or profile change whose every argument is an explicit
                      literal of the request, and whose only obstacle is a condition that the request leaves to the
                      agent's judgement (condition kind 'unsupported', e.g. "if anything looks off"), is released.
                      Objective conditions (balance expressions) stay enforced; money transfers are never released on a
                      delegated judgement.
Hybrid options (05): the learned score NEVER releases a call (invariant I5).
  hybrid="review"     the stored ridge+Platt score is computed for every restricted call and recorded; verdicts are
                      identical to REM-B2 by construction; the score is evaluated only as a review-queue ranking.
  hybrid="withhold"   calls that the deterministic stages ALLOW are escalated if p >= theta (frozen B1 threshold of the
                      redesign study, development scores only). It can only withhold.
"""
from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "architecture_redesign"))
import rem_arch as RA  # noqa: E402  (frozen; also sets the import paths of the earlier studies)

import amount_verifier_v2 as V2  # noqa: E402
import contracts as K  # noqa: E402
import permission as P1  # noqa: E402
from amount_verifier import _fmt as V1fmt  # noqa: E402
from permission_v3 import DEFAULT_OPTS3, RuntimePermissionV3  # noqa: E402
from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.algorithms.decision.loss_matrix import build_loss_grid  # noqa: E402
from rem.algorithms.detection.ridge_logistic import sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard  # noqa: E402

B2 = dict(RA.BASE, desig="nodigit", sor=True, deleg=True, hybrid=None)
CONFIGS2: Dict[str, Dict[str, Any]] = {
    "REM_B2": dict(B2),
    "REM_B2_HR": dict(B2, hybrid="review"),
    "REM_B2_HW": dict(B2, hybrid="withhold"),
    "B2_noR1": dict(B2, desig="frozen"),
    "B2_noR2": dict(B2, sor=False),
    "B2_noR3": dict(B2, deleg=False),
    "B2_noOB": dict(B2, ob=False),
    "B2_noLedger": dict(B2, ledger=False),
    "B2_E2plain": dict(B2, e2="plain"),
}
NONTRANSFER = ("credential_change", "profile_change")
CURRENT_ENV: Dict[str, Any] = {"env": None}       # set only by the scripted closed-loop runner of this study


# ------------------------------------------------------------------------------------- R1 designators
def words_nodigit(text):
    return RA.words(" ".join(t for t in (text or "").split() if not re.search(r"\d", t)))


class ObjectBinding2(RA.ObjectBinding):
    def __init__(self, contracts, desig, sor_objects):
        clauses = sorted({c.clause for c in contracts if "schedule_modify" in c.effects})
        wf = words_nodigit if desig == "nodigit" else RA.words
        self.designators = set().union(*[wf(c) for c in clauses]) if clauses else set()
        self.plural = any(RA.PLURAL.search(c) for c in clauses)
        self._sor_objects = sor_objects

    def status(self, hist, oid):
        objs = self._sor_objects() if self._sor_objects else None
        if objs is None:
            return super().status(hist, oid)
        saved = RA.scheduled_objects
        try:
            RA.scheduled_objects = lambda _h: objs
            return super().status(hist, oid)
        finally:
            RA.scheduled_objects = saved


# ------------------------------------------------------------------------------------- R2 system of record
def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def sor_snapshot(ep, guard):
    """Structured bank records at decision time, or None. Sources: a case's declared bank (suites), the replay/scripted
    environment captured by this study's pipeline element. Only structured fields are kept."""
    b = getattr(ep, "bank", None)
    if b is not None:
        tx = [dict(id=r["id"], sender=r["sender"], recipient=r["recipient"], amount=r["amount"]) for r in b.get("transactions", [])]
        so = {r["id"]: dict(id=r["id"], recipient=r["recipient"], amount=r["amount"], subject=r["subject"], recurring=r["recurring"])
              for r in b.get("scheduled", [])}
        return tx, so
    env = getattr(guard, "_sor_env", None) or CURRENT_ENV["env"]
    if env is None or not hasattr(env, "bank_account"):
        return None
    acc = env.bank_account
    tx = [dict(id=t.id, sender=t.sender, recipient=t.recipient, amount=t.amount) for t in acc.transactions]
    so = {t.id: dict(id=t.id, recipient=t.recipient, amount=t.amount, subject=t.subject, recurring=t.recurring)
          for t in acc.scheduled_transactions}
    return tx, so


class AugHistory:
    """History view for evidence resolution: the agent's executed reads plus one synthetic executed read holding the
    system-of-record transactions (structured fields only). balance() is delegated unchanged."""

    def __init__(self, hist, tx):
        self._h = hist
        self.rows = list(hist.rows) + ([("get_most_recent_transactions", None, yaml.safe_dump(tx, sort_keys=False), True)] if tx else [])

    def __getattr__(self, k):
        return getattr(self._h, k)


# ------------------------------------------------------------------------------------- R3 delegated judgement
def delegated_release(rp, ev, tool):
    cat = P1.CATEGORY.get(tool)
    if cat not in NONTRANSFER or ev.overall != "unknown" or ev.condition != "unevaluable":
        return False
    if ev.base.op != "requested" or getattr(ev.base, "value", None) != "explicit":
        return False
    lic = [i for i in rp.intent3.instructions if i.category == cat]
    return bool(lic) and all(i.condition is not None and i.condition.kind == "unsupported" for i in lic)


# ------------------------------------------------------------------------------------- guard
def make_guard2(cfg, cell, ep, st):
    gc = GuardConfig(st.spec, st.detector, cell["reference"], st.tier_map, st.restricted, "step_level", cfg["reviewer"])
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    rp = RuntimePermissionV3(ep.objective, dict(RA.CA.OPTS_C))
    hybrid = cfg.get("hybrid")
    rp_feat = RuntimePermissionV3(ep.objective, dict(DEFAULT_OPTS3)) if (cfg["learn"] or hybrid) else None
    contracts = RA.ER.compile_e1(ep.objective) if cfg["e1"] else K.compile_contracts(ep.objective)
    use_sor = bool(cfg.get("sor"))
    snap = (lambda: sor_snapshot(ep, guard)) if use_sor else (lambda: None)
    ob = ObjectBinding2(contracts, cfg.get("desig", "frozen"), (lambda: (snap() or (None, None))[1]) if use_sor else None) \
        if cfg["ob"] else None
    ledger = RA.ObjectLedger() if cfg["ledger"] else RA.NoLedgerObj()
    refunds = RA.compile_refunds(ep.objective, cfg["e2"])
    hist = V2.History()
    predicates = RA.S.rm.predicates()
    grid = build_loss_grid(RA.S.rm.loss_spec(cell["rmod"]), "architecture redesign learned stage")
    pol2 = A3Policy(grid, predicates, tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.ESCALATE, Verdict.MODIFY))
    pol3 = A3Policy(grid, predicates, tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.MODIFY,))
    theta = RA._threshold() if (cfg["learn"] == "thr" or hybrid == "withhold") else None
    ridge = cell["models"][("F4", "y")]
    orig_ingest = guard.ingest

    def ingest(tool, text, executed):
        rp.on_ingest(executed)
        if rp_feat is not None:
            rp_feat.on_ingest(executed)
        hist.rows.append((tool, None, text, bool(executed)))
        ledger.settle(tool, bool(executed))
        return orig_ingest(tool, text, executed)
    guard.ingest = ingest

    def score(c, f):
        evf = rp_feat.evidence(guard.tracker, c.tool, c.args, c.tier)
        x = dict(f)
        x.update(evf.features())
        s = RA.CA._linear(ridge, x)
        p_cal = float(sigmoid(ridge["g1"] * s + ridge["g0"])) if not ridge["failed"] else float(sigmoid(s))
        return float(s), p_cal, float(sigmoid(s))

    def decide(c):
        is_r = c.tool in restricted
        ev = rp.evidence(guard.tracker, c.tool, c.args, c.tier)
        info = {"stage": "front"}
        det = {"perm": (ev.overall, ev.base.recipient, ev.base.amount, ev.effect, ev.binding, ev.condition, ev.fulfilment, ev.authority)}
        v, src = Verdict.ALLOW, "candidate_release"
        f, avail = guard.tracker.features(c.tool, c.args)
        if rp_feat is not None and is_r:
            info["s"], info["p_all"], info["p_raw"] = score(c, f)
        ledger.current_oid = (c.args or {}).get("id") if (cfg["ob"] and c.tool == "update_scheduled_transaction") else None
        s = snap() if (use_sor and is_r) else None
        h = AugHistory(hist, s[0]) if s else hist
        rw = None
        front_block = is_r and (ev.overall == "denied" or not ev.authority)
        if front_block and cfg.get("deleg") and delegated_release(rp, ev, c.tool):
            front_block, info["delegated"] = False, True
        if front_block and refunds:
            rw = RA.refund_witness(refunds, ledger, h, c.tool, c.args, cfg)
            if rw is not None:
                front_block, info["e2"] = False, rw.cid
        if front_block:
            v, src = Verdict.BLOCK, "permission_guard_authority_v3"
        else:
            forced = predicates.evaluate(c.tool, c.tier, avail)
            if forced.verdict is not None:
                v, src, info["stage"] = forced.verdict, forced.source, "predicate"
            else:
                obs = ob.status(h, (c.args or {}).get("id")) if (ob is not None and c.tool == "update_scheduled_transaction") else None
                if obs is not None:
                    det["object"] = obs
                if obs is not None and obs[0] == "not_designated":
                    v, src, info["stage"] = Verdict.BLOCK, "object_not_designated", "object"
                elif obs is not None and obs[0] == "unresolved":
                    v, src, info["stage"] = Verdict.ESCALATE, "object_unresolved", "object"
                else:
                    k = (K.Decision("verified", rw.cid, (V1fmt(rw.amount),), "refund licence (E2)") if rw is not None
                         else RA.kdecide(contracts, ledger, h, c.tool, c.args, cfg))
                    det["contract"] = (k.status, k.expected, k.reason, k.witness)
                    info["stage"] = "contract"
                    if k.status in ("mismatch", "exhausted"):
                        v, src = Verdict.BLOCK, f"contract_{k.status}"
                    elif k.status == "unresolved":
                        v, src = Verdict.ESCALATE, "contract_unresolved"
                    elif info.get("delegated") and v is Verdict.ALLOW:
                        src = "delegated_condition"
                    if v is Verdict.ALLOW and hybrid == "withhold" and is_r and info.get("p_all") is not None \
                            and info["p_all"] >= theta:
                        v, src = Verdict.ESCALATE, "learned_threshold_withhold"          # can only withhold (I5)
                        info.update(stage="learned", p=info["p_all"])
                    if v is Verdict.ALLOW and k.witness is not None:
                        ledger.reserve(c.tool, k.witness)
        if hybrid == "review" and is_r:
            info["review_score"] = info.get("p_all")                                     # recorded only; no verdict effect
        det["cs"] = info
        rp.record(guard.tracker, c.tool, c.args)
        if rp_feat is not None:
            rp_feat.record(guard.tracker, c.tool, c.args)
        return v, src, det
    guard.decide = decide
    base_evaluate = guard.evaluate

    def evaluate(tool, args):
        import time
        start = time.perf_counter()
        result = base_evaluate(tool, args)
        row = guard.audit[-1]
        if not row["verdict_source"].startswith("learned"):
            row["probability_used_for_verdict"] = False
        row["rem_latency_full_ms"] = (time.perf_counter() - start) * 1000
        guard.full_latencies_ms[-1] = row["rem_latency_full_ms"]
        return result
    guard.evaluate = evaluate
    guard.contracts, guard.ledger = contracts, ledger
    return guard


def build_cell2(arm, ep, cell, extra, st):
    if arm in CONFIGS2:
        return make_guard2(CONFIGS2[arm], cell, ep, st)
    return RA.build_cell(arm, ep, cell, extra, st)


def factory2(key=("S1", "injection_task_0")):
    import progent_manual as PGM
    import rs_run as V1R
    st = V1R.common.make_setup()
    cells, cs = V1R.J.load("cells"), V1R.C.load("cs_cells")
    PGM.load()

    def build(arm, ep):
        return build_cell2(arm, ep, cells[key], cs[key], st)
    build.setup = st
    return build


# ------------------------------------------------------------------------------------- replay with environment capture
def replay_episode2(episode, suite, guard):
    """rem.integration.agentdojo_replay.replay_episode with one extra pass-through pipeline element that hands the live
    environment object to the guard (guard._sor_env) before the first model turn. The frozen function is not edited."""
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
    from rem.integration.agentdojo_replay import ReplayOutcome, _agentdojo_elements

    class EnvCapture(BasePipelineElement):
        name = "rem_env_capture"

        def query(self, query, runtime, env, messages=[], extra_args={}):
            guard._sor_env = env
            return query, runtime, env, messages, extra_args

    AgentPipeline, SystemMessage, InitQuery, ToolsExecutionLoop, ReplayLLM, Guarded = _agentdojo_elements()
    llm = ReplayLLM(episode)
    pipe = AgentPipeline([SystemMessage(episode.system_prompt), InitQuery(), EnvCapture(), llm,
                          ToolsExecutionLoop([Guarded(guard), llm])])
    pipe.name = "rem_replay"
    ut = suite.get_user_task_by_id(episode.user_task_id)
    it = suite.get_injection_task_by_id(episode.injection_task_id) if episode.injection_task_id else None
    err = None
    try:
        utility, security = suite.run_task_with_pipeline(pipe, ut, it, dict(episode.injections))
    except Exception as exc:  # recorded as an error, never silently dropped
        utility, security, err = False, False, repr(exc)[:300]
    return ReplayOutcome(episode_id=episode.episode_id, utility=bool(utility), security=bool(security),
                         recorded_utility=episode.utility, recorded_security=episode.security, audit=guard.audit,
                         latencies_ms=guard.latencies_ms, error=err)


def amount_fraction(x):
    v = _num(x)
    return None if v is None else Fraction(str(v))
