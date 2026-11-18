"""REM-A, REM-B, REM-C and their ablations (architecture-redesign study, 18 November 2026).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. Designs: 04_REM_A_DESIGN.md, 05_REM_B_DESIGN.md,
06_REM_C_DESIGN.md; threat model and invariants: 03_THREAT_MODEL_AND_SECURITY_CONTRACT.md.
Frozen components are imported, not edited: revision-3 front, compiler, contracts and ledger (contracts.py), E1 parser
(evidence_resolution.py), stored F4 ridge + Platt fits, frozen A3 expected-loss engine, frozen B1 operating threshold,
frozen escalation models.

Switches (CONFIGS): ob (object binding), ledger, e1, e2 ('h' hardened | 'plain' | None), prov ('strict' | 'any'),
learn (None | 'all2' | 'unres3' | 'thr' | 'unres3raw'), reviewer ('no_reviewer' | 'idealized').
"""
from __future__ import annotations

import json
import re
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/architecture_redesign", "experiments/improvement_controlled", "experiments/progent_competitive",
           "experiments/repair_study", "experiments/competitive_study", "experiments/improve_study", "experiments/authz_study",
           "experiments/g3_integration", "experiments/pilot", ""):
    sys.path.insert(0, str(ROOT / _p) if _p else str(ROOT))

import yaml  # noqa: E402

import amount_verifier as V1  # noqa: E402
import amount_verifier_v2 as V2  # noqa: E402
import arms as AR  # noqa: E402
import contract_arms as CA  # noqa: E402
import contracts as K  # noqa: E402
import evidence_resolution as ER  # noqa: E402
import study as S  # noqa: E402
from amount_verifier import _fmt as V1fmt  # noqa: E402
from intent import amount_of, canon_iban  # noqa: E402
from intent_v3 import TOOL_EFFECT  # noqa: E402
from permission_v3 import DEFAULT_OPTS3, RuntimePermissionV3, holds  # noqa: E402
from rem.algorithms.a3 import A3Policy  # noqa: E402
from rem.algorithms.decision.loss_matrix import build_loss_grid  # noqa: E402
from rem.algorithms.detection.ridge_logistic import sigmoid  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard  # noqa: E402

BASE = dict(ob=True, ledger=True, e1=True, e2="h", prov="strict", learn=None, reviewer="no_reviewer")
CONFIGS: Dict[str, Dict[str, Any]] = {
    "REM_B": dict(BASE),
    "REM_A": dict(BASE, learn="all2"),
    "REM_C": dict(BASE, learn="unres3"),
    "REM_C_T": dict(BASE, learn="thr"),
    "REM_C_raw": dict(BASE, learn="unres3raw"),
    "REM_B_R": dict(BASE, reviewer="idealized"),             # upper bound: idealised reviewer (uses labels; never deployable)
    "B_noOB": dict(BASE, ob=False),
    "B_noLedger": dict(BASE, ledger=False),
    "B_noE1": dict(BASE, e1=False),
    "B_noE2": dict(BASE, e2=None),
    "B_E2plain": dict(BASE, e2="plain"),
    "B_noProv": dict(BASE, prov="any"),
}
THRESHOLD_FILE = ROOT / "REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18" / "results" / "development_threshold.json"
STOP = set("""standing order orders scheduled schedule payment payments transfer transfers transaction transactions account accounts
new old update updates change changes move modify set please the and for from now with that this they them pay pays paid fee
fees stays same accordingly also its their our your bank banks monthly recurring next month into make sure adjust what has have
been was were will just did does would should could can may might there here which who whom whose about after before over under
again then than but not all any each every some such only own same very much more most less least many few one two subscriptions
subscription my me our is are be to of in on at by an it as or so if no yes landlord""".split())
PLURAL = re.compile(r"\b(?:standing\s+orders|orders|payments|transfers|subscriptions)\b", re.I)


# ------------------------------------------------------------------------------------- trusted records
def _yaml_rows(text):
    try:
        v = yaml.safe_load(V1.clean(text or ""))
    except Exception:
        return []
    return [r for r in v if isinstance(r, dict)] if isinstance(v, list) else []


def records(hist, tool="get_most_recent_transactions", prov="strict"):
    for t, _a, text, executed in hist.rows:
        if not executed or (prov == "strict" and t != tool):
            continue
        yield from _yaml_rows(text)


def outgoing_amounts(hist, rcp, prov):
    return {Fraction(amount_of(r["amount"])) for r in records(hist, prov=prov)
            if r.get("sender") == "me" and isinstance(r.get("recipient"), str) and canon_iban(r["recipient"]) == rcp
            and amount_of(r.get("amount")) is not None}


def outgoing_recipients(hist, prov):
    return {canon_iban(r["recipient"]) for r in records(hist, prov=prov) if r.get("sender") == "me" and isinstance(r.get("recipient"), str)}


def incoming_senders(hist, amount, prov):
    return {canon_iban(r["sender"]) for r in records(hist, prov=prov)
            if r.get("recipient") == "me" and isinstance(r.get("sender"), str) and amount_of(r.get("amount")) is not None
            and Fraction(amount_of(r["amount"])) == amount}


def scheduled_objects(hist):
    """Latest executed get_scheduled_transactions result (the user's own standing orders; trusted fields)."""
    objs = None
    for t, _a, text, executed in hist.rows:
        if t == "get_scheduled_transactions" and executed:
            rows = _yaml_rows(text)
            objs = {r["id"]: r for r in rows if "id" in r}
    return objs


# ------------------------------------------------------------------------------------- object binding (I3)
def words(text):
    return {w for w in re.findall(r"[a-z]+", (text or "").lower()) if len(w) >= 3 and w not in STOP}


class ObjectBinding:
    def __init__(self, contracts):
        clauses = sorted({c.clause for c in contracts if "schedule_modify" in c.effects})
        self.designators = set().union(*[words(c) for c in clauses]) if clauses else set()
        self.plural = any(PLURAL.search(c) for c in clauses)

    def status(self, hist, oid):
        """('designated' | 'not_designated' | 'unresolved', reason)."""
        objs = scheduled_objects(hist)
        if not objs or oid not in objs:
            return "unresolved", "the object was not established by an executed read of the standing orders"
        if self.designators:
            d = {i for i, o in objs.items() if words(str(o.get("subject", ""))) & self.designators}
        else:
            d = set(objs) if len(objs) == 1 else set()
            if not d:
                return "unresolved", "the request designates no standing order and several exist"
        if not d:
            return "unresolved", "no standing order matches the request's designation"
        if not self.plural and len(d) > 1:
            return "unresolved", "a singular reference matches several standing orders"
        if oid not in d:
            return "not_designated", "the request does not designate this standing order"
        return "designated", "designated by the request"


class ObjectLedger(K.Ledger):
    """Allowance consumed per (instruction, object) for modifications of existing objects; per instruction otherwise."""
    current_oid: Optional[Any] = None

    def _key(self, cid):
        return (cid, self.current_oid) if self.current_oid is not None else cid

    def remaining(self, c):
        k = self._key(c.cid)
        return c.count - self.committed.get(k, 0) - self.reserved.get(k, 0)

    def reserve(self, tool, cid):
        k = self._key(cid)
        self.reserved[k] = self.reserved.get(k, 0) + 1
        self.pending = (tool, k)


class NoLedgerObj(ObjectLedger):
    def remaining(self, c):
        return 1


# ------------------------------------------------------------------------------------- contract decision with E1
def binding_status(b, a, hist, rcp, cfg):
    if b.kind != "record_percent":
        return V2._binding_status(b, a, hist, rcp)
    amts = outgoing_amounts(hist, rcp, cfg["prov"]) if rcp else set()
    if len(amts) != 1:
        return "unresolved", None, ("no single outgoing record to the recipient" if not amts else "several outgoing records")
    x = b.coef * next(iter(amts)) + b.value
    return ("verified", x, "equal to the amount the instruction determines") if a == x else \
        ("mismatch", x, "differs from the amount the instruction determines")


def kdecide(contracts, ledger, hist, tool, args, cfg):
    """contracts.decide / evidence_resolution.decide, with the E1 binding read under the configured provenance."""
    eff = TOOL_EFFECT.get(tool)
    args = args or {}
    if eff is None:
        return K.Decision("unconstrained", reason="not a payment tool")
    rcp = canon_iban(args.get("recipient")) if isinstance(args.get("recipient"), str) else None
    lic = [c for c in contracts if eff in c.effects]
    cand = ([c for c in lic if rcp is not None and c.target == rcp]
            or [c for c in lic if c.target is None and c.account in (None, rcp)])
    if not cand:
        return K.Decision("no_contract", reason="no instruction of the request licenses this effect and account")
    a = amount_of(args.get("amount")) if args.get("amount") is not None else None
    bal = hist.balance()
    ok, pending, exhausted, mismatched, expected = [], [], [], [], []
    for c in cand:
        cond = True if c.condition is None else holds(c.condition, bal)
        if a is None:
            st, x, why = (("unconstrained", None, "no amount argument") if c.binding.kind == "none"
                          else ("unresolved", None, "the call has no exact amount"))
        else:
            st, x, why = binding_status(c.binding, Fraction(a), hist, rcp, cfg)
        if x is not None:
            expected.append(V1fmt(x))
        if cond is False:
            continue
        if cond is None:
            pending.append("the condition of the instruction cannot be evaluated")
            continue
        if st in ("verified", "unconstrained"):
            if ledger.remaining(c) > 0:
                ok.append((0 if st == "verified" else 1, c.cid, st, why))
            else:
                exhausted.append(f"instruction {c.cid} has no remaining allowance")
            continue
        (pending if st == "unresolved" else mismatched).append(why)
    if ok:
        _r, cid, st, why = sorted(ok)[0]
        return K.Decision(st, cid, tuple(expected), why)
    if pending:
        return K.Decision("unresolved", None, tuple(expected), "; ".join(sorted(set(pending))))
    if exhausted:
        return K.Decision("exhausted", None, tuple(expected), "; ".join(sorted(set(exhausted))))
    if mismatched:
        return K.Decision("mismatch", None, tuple(expected), "; ".join(sorted(set(mismatched))))
    return K.Decision("mismatch", None, tuple(expected), "no instruction whose condition holds licenses this call")


# ------------------------------------------------------------------------------------- E2 (plain / hardened)
def compile_refunds(objective, mode):
    if mode is None:
        return []
    if mode == "plain":
        return ER.compile_e2(objective)
    out = []
    for n, s in enumerate(re.split(r"(?<=[.!?])\s+", objective)):
        if not (ER.E2_REFUND.search(s) and ER.E2_RECEIVED.search(s)):
            continue
        clause = re.split(r"\b(?:and|also)\b(?=\s+(?:send|pay|transfer|update|schedule))", s, flags=re.I)[0]
        if V1._accounts(clause):
            continue                                                    # an account in the refund clause: the front handles it
        nums = re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])", K._blank(K._blank(clause, K.DATES), K.IDS))
        if len(nums) == 1:
            out.append(ER.Refund(ER.E2_BASE + n, Fraction(nums[0]), clause))
    return out


def refund_witness(refunds, ledger, hist, tool, args, cfg):
    if tool != "send_money" or not refunds:
        return None
    rcp = canon_iban(args.get("recipient")) if isinstance(args.get("recipient"), str) else None
    a = amount_of(args.get("amount")) if args.get("amount") is not None else None
    if rcp is None or a is None:
        return None
    for r in refunds:
        if Fraction(a) != r.amount or incoming_senders(hist, r.amount, cfg["prov"]) != {rcp}:
            continue
        if cfg["e2"] == "h" and rcp not in outgoing_recipients(hist, cfg["prov"]):
            continue                                                    # I6: unknown counterparty (refund-scam defence)
        if ledger.committed.get(r.cid, 0) + ledger.reserved.get(r.cid, 0) < 1:
            return r
    return None


# ------------------------------------------------------------------------------------- guard
def _threshold():
    return json.loads(THRESHOLD_FILE.read_text())["theta"]


def make_guard(cfg, cell, ep, st):
    gc = GuardConfig(st.spec, st.detector, cell["reference"], st.tier_map, st.restricted, "step_level", cfg["reviewer"])
    guard = RemGuard(gc, None, lambda c: (Verdict.ALLOW, "init", {}), st.labeler, ep)
    restricted = set(st.restricted)
    rp = RuntimePermissionV3(ep.objective, dict(CA.OPTS_C))
    rp_feat = RuntimePermissionV3(ep.objective, dict(DEFAULT_OPTS3)) if cfg["learn"] else None
    contracts = ER.compile_e1(ep.objective) if cfg["e1"] else K.compile_contracts(ep.objective)
    ob = ObjectBinding(contracts) if cfg["ob"] else None
    ledger = ObjectLedger() if cfg["ledger"] else NoLedgerObj()
    refunds = compile_refunds(ep.objective, cfg["e2"])
    hist = V2.History()
    predicates = S.rm.predicates()
    grid = build_loss_grid(S.rm.loss_spec(cell["rmod"]), "architecture redesign learned stage")
    pol2 = A3Policy(grid, predicates, tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.ESCALATE, Verdict.MODIFY))
    pol3 = A3Policy(grid, predicates, tie_mode="record_chapter3_order", exclude_from_expected_loss=(Verdict.MODIFY,))
    theta = _threshold() if cfg["learn"] == "thr" else None
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
        s = CA._linear(ridge, x)
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
        rw = None
        front_block = is_r and (ev.overall == "denied" or not ev.authority)
        if front_block and refunds:
            rw = refund_witness(refunds, ledger, hist, c.tool, c.args, cfg)
            if rw is not None:
                front_block, info["e2"] = False, rw.cid
        if front_block:
            v, src = Verdict.BLOCK, "permission_guard_authority_v3"
        else:
            forced = predicates.evaluate(c.tool, c.tier, avail)
            if forced.verdict is not None:
                v, src, info["stage"] = forced.verdict, forced.source, "predicate"
            else:
                obs = ob.status(hist, (c.args or {}).get("id")) if (ob is not None and c.tool == "update_scheduled_transaction") else None
                if obs is not None:
                    det["object"] = obs
                if obs is not None and obs[0] == "not_designated":
                    v, src, info["stage"] = Verdict.BLOCK, "object_not_designated", "object"
                elif obs is not None and obs[0] == "unresolved":
                    v, src, info["stage"] = Verdict.ESCALATE, "object_unresolved", "object"
                else:
                    k = (K.Decision("verified", rw.cid, (V1fmt(rw.amount),), "refund licence (E2)") if rw is not None
                         else kdecide(contracts, ledger, hist, c.tool, c.args, cfg))
                    det["contract"] = (k.status, k.expected, k.reason, k.witness)
                    info["stage"] = "contract"
                    if k.status in ("mismatch", "exhausted"):
                        v, src = Verdict.BLOCK, f"contract_{k.status}"
                    elif k.status == "unresolved":
                        v, src = Verdict.ESCALATE, "contract_unresolved"
                        if cfg["learn"] in ("unres3", "thr", "unres3raw") and is_r:          # eligible unresolved call (I5)
                            p = info["p_raw"] if cfg["learn"] == "unres3raw" else info["p_all"]
                            if cfg["learn"] == "thr":
                                v, src = (Verdict.ALLOW, "learned_threshold_allow") if p < theta else (Verdict.ESCALATE, "learned_threshold_escalate")
                            else:
                                d = pol3.decide(p, c.tier, c.tool, avail)
                                v, src = d.verdict, "learned_" + d.source
                            info.update(stage="learned", p=p)
                    elif cfg["learn"] == "all2" and is_r:
                        d = pol2.decide(info["p_all"], c.tier, c.tool, avail)
                        v, src = d.verdict, d.source
                        info.update(stage="learned", p=info["p_all"])
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
        if not row["verdict_source"].startswith("learned") and row["verdict_source"] not in ("expected_loss",):
            row["probability_used_for_verdict"] = False
        row["rem_latency_full_ms"] = (time.perf_counter() - start) * 1000
        guard.full_latencies_ms[-1] = row["rem_latency_full_ms"]
        return result
    guard.evaluate = evaluate
    guard.contracts, guard.ledger = contracts, ledger
    return guard


def build_cell(arm, ep, cell, extra, st):
    if arm in CONFIGS:
        return make_guard(CONFIGS[arm], cell, ep, st)
    return AR.build_cell(arm, ep, cell, extra, st)


def factory(key=("S1", "injection_task_0")):
    import progent_manual as PGM
    import rs_run as V1R
    st = V1R.common.make_setup()
    cells, cs = V1R.J.load("cells"), V1R.C.load("cs_cells")
    PGM.load()

    def build(arm, ep):
        return build_cell(arm, ep, cells[key], cs[key], st)
    build.setup = st
    return build
