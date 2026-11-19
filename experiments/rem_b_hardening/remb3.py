"""REM-B3: amendment round 06a (post-hoc, exploratory). REM-B2 (remb2.py, frozen in 06) + F1a + F1b + F2.

Status: [PROPOSED - EXPLORATORY - AMENDMENT]. remb2.py is not edited: make_guard3 wraps a REM-B2 guard's decision
function and only adds withholding checks, so it can never release a call that REM-B2 withholds. A reservation made by REM-B2 for a call turned into a
withholding here is released by the ledger's normal settle-on-failure path (the refused call is ingested as not executed).

  F1a  a restricted money call with no licensing instruction (contract status 'no_contract') is BLOCKED.
  F1b  update_scheduled_transaction may change only licensed fields: recipient -> an account the request gives for a
       modification; amount -> an amount the request states for a modification (or a contract amount binding);
       any other field must equal the object's current value. Unknown current value -> withheld (unresolved).
  F2   an immediate payment / new standing order must carry an amount the request binds to that recipient for that
       effect, whenever the request binds any amount to it.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).resolve().parent))
import remb2 as RB  # noqa: E402

from intent import amount_of, canon_iban  # noqa: E402
from intent_v3 import TOOL_EFFECT  # noqa: E402
from rem.core.results import Verdict  # noqa: E402

B3 = dict(RB.B2, f1=True, f2=True)
CONFIGS3: Dict[str, Dict[str, Any]] = {
    "REM_B3": dict(B3),
    "B3_noF1": dict(B3, f1=False),
    "B3_noF2": dict(B3, f2=False),
}
_MONEY_EFFECT = {"send_money": "transfer_now", "schedule_transaction": "schedule_create"}


def _dec(x):
    v = amount_of(x)
    return None if v is None else Decimal(str(v))


def _same(a, b):
    if isinstance(a, (int, float)) or isinstance(b, (int, float)):
        da, db = _dec(a), _dec(b)
        return da is not None and da == db
    if isinstance(a, str) and isinstance(b, str) and len(a) >= 15 and len(b) >= 15:
        return canon_iban(a) == canon_iban(b)
    return a == b


def f2_check(intent3, tool, args):
    eff = _MONEY_EFFECT.get(tool)
    if eff is None or not isinstance(args.get("recipient"), str):
        return None
    r = canon_iban(args["recipient"])
    bound = {i.amount for i in intent3.instructions if eff in i.effects and i.target == r and i.amount is not None}
    if not bound:
        return None
    a = _dec(args.get("amount"))
    return None if (a is not None and a in {Decimal(str(b)) for b in bound}) else "amount_bound_to_other_instruction"


def f1b_check(intent3, contracts, current, args):
    """None (in scope), 'out_of_scope' (block) or 'unknown_current' (withhold as unresolved)."""
    mods = [i for i in intent3.instructions if i.category == "payment_modification"]
    targets = {i.target for i in mods if i.target}
    amounts = {Decimal(str(i.amount)) for i in mods if i.amount is not None}
    contract_amount = any("schedule_modify" in c.effects and c.binding.kind != "none" for c in contracts)
    for k, v in args.items():
        if k == "id" or v is None:
            continue
        if current is not None and k in current and _same(v, current[k]):
            continue
        if k == "recipient" and isinstance(v, str) and canon_iban(v) in targets:
            continue
        if k == "amount" and (contract_amount or (_dec(v) is not None and _dec(v) in amounts)):
            continue
        if current is None:
            return "unknown_current"
        return "out_of_scope"
    return None


def make_guard3(cfg, cell, ep, st):
    g = RB.make_guard2(cfg, cell, ep, st)
    base = g.decide
    rp_intent = RB.RuntimePermissionV3(ep.objective, dict(RB.RA.CA.OPTS_C)).intent3
    restricted = set(st.restricted)
    reads = SimpleNamespace(rows=[])                     # executed results seen by this guard (for current object values)
    inner_ingest = g.ingest

    def ingest(tool, text, executed):
        reads.rows.append((tool, None, text, bool(executed)))
        return inner_ingest(tool, text, executed)
    g.ingest = ingest

    def current_object(oid):
        snap = RB.sor_snapshot(ep, g) if cfg.get("sor") else None
        objs = snap[1] if snap else None
        if objs is None:
            objs = RB.RA.scheduled_objects(reads) or {}
        return objs.get(oid)

    def decide(c):
        v, src, det = base(c)
        if v is not Verdict.ALLOW or c.tool not in restricted or TOOL_EFFECT.get(c.tool) is None:
            return v, src, det
        args = dict(c.args or {})
        kk = det.get("contract")
        if cfg.get("f1") and kk and kk[0] == "no_contract":
            return Verdict.BLOCK, "contract_no_licence", det
        if cfg.get("f2"):
            why = f2_check(rp_intent, c.tool, args)
            if why:
                return Verdict.BLOCK, why, det
        if cfg.get("f1") and c.tool == "update_scheduled_transaction":
            why = f1b_check(rp_intent, g.contracts, current_object(args.get("id")), args)
            if why == "out_of_scope":
                return Verdict.BLOCK, "modification_out_of_scope", det
            if why == "unknown_current":
                return Verdict.ESCALATE, "modification_current_value_unknown", det
        return v, src, det
    g.decide = decide
    return g


def build_cell3(arm, ep, cell, extra, st):
    if arm in CONFIGS3:
        return make_guard3(CONFIGS3[arm], cell, ep, st)
    return RB.build_cell2(arm, ep, cell, extra, st)


def factory3(key=("S1", "injection_task_0")):
    import progent_manual as PGM
    import rs_run as V1R
    st = V1R.common.make_setup()
    cells, cs = V1R.J.load("cells"), V1R.C.load("cs_cells")
    PGM.load()

    def build(arm, ep):
        return build_cell3(arm, ep, cells[key], cs[key], st)
    build.setup = st
    return build
