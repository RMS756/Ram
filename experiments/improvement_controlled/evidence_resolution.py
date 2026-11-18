"""Evidence-resolution candidate E1 + E2 (04_IMPROVEMENT_DESIGN.md). Status: [PROPOSED - EXPLORATORY].

Wraps the frozen contract compiler (progent_competitive/contracts.py, unchanged) and adds:
  E1  'record_percent' binding: [the difference of] [an] [additional] P% / P percent of the amount (we|I) paid
      [(+|plus) [a fee of] L], value = P/100 * R + L, R = amount of the SINGLE outgoing record (sender 'me') to the call's
      recipient in an EXECUTED get_most_recent_transactions result. Applied only to contracts that the frozen compiler left
      unresolved by its calculation cue, and only if nothing else (operator word, stray number) remains in the sentence.
  E2  refund licence: a sentence of the user's request with 'refund', a received-money phrase (got / received / sent me),
      exactly one stated amount L and no account, licenses ONE send_money of exactly L to the sender of the SINGLE incoming
      record of amount L in an executed get_most_recent_transactions result.
Exact rationals (Fraction); equality only; no rounding rule; no eval; structured record fields only (never free text).
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, List, Mapping, Optional

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/progent_competitive", "experiments/repair_study", "experiments/improve_study"):
    sys.path.insert(0, str(ROOT / _p))

import contracts as K  # noqa: E402
import amount_verifier as V1  # noqa: E402
import amount_verifier_v2 as V2  # noqa: E402
from amount_verifier import AmountBinding  # noqa: E402
from intent import amount_of, canon_iban  # noqa: E402
from intent_v3 import TOOL_EFFECT  # noqa: E402
from permission_v3 import holds  # noqa: E402

NUM = r"(\d+(?:\.\d+)?)"
E1_RX = re.compile(r"(?:the\s+difference\s+of\s+)?(?:an\s+)?(?:additional\s+)?" + NUM + r"\s*(?:%|percent)\s+of\s+the\s+amount\s+"
                   r"(?:that\s+)?(?:we|i)\s+paid(?:\s*(?:\+|plus)\s*(?:a\s+fee\s+of\s+)?(?:[$€£]\s?)?" + NUM + r")?", re.I)
E2_REFUND = re.compile(r"\brefund\b", re.I)
E2_RECEIVED = re.compile(r"\b(?:got|received|sent\s+me|have\s+been\s+sent)\b", re.I)
CUE_REASON = "calculation cue without a supported expression"
E2_BASE = 1000                       # contract ids of refund licences (distinct from compile-order ids)


def _records(hist: V2.History):
    import yaml
    for tool, _a, text, executed in hist.rows:
        if tool != "get_most_recent_transactions" or not executed:
            continue
        try:
            recs = yaml.safe_load(V1.clean(text))
        except Exception:
            continue
        for r in recs if isinstance(recs, list) else []:
            if isinstance(r, dict):
                yield r


def outgoing_amounts(hist, rcp) -> set:
    out = set()
    for r in _records(hist):
        if r.get("sender") == "me" and isinstance(r.get("recipient"), str) and canon_iban(r["recipient"]) == rcp:
            a = amount_of(r.get("amount"))
            if a is not None:
                out.add(Fraction(a))
    return out


def incoming_senders(hist, amount: Fraction) -> set:
    out = set()
    for r in _records(hist):
        a = amount_of(r.get("amount"))
        if r.get("recipient") == "me" and isinstance(r.get("sender"), str) and a is not None and Fraction(a) == amount:
            out.add(canon_iban(r["sender"]))
    return out


def _e1(contract: K.Contract) -> Optional[AmountBinding]:
    text = K._masked(contract.clause)
    ms = list(E1_RX.finditer(text))
    if len(ms) != 1:
        return None
    m = ms[0]
    rest = text[:m.start()] + " " * (m.end() - m.start()) + text[m.end():]
    if K._uncovered(rest, 0, len(rest)) is not None:            # anything else computational left -> stays unresolved
        return None
    pct, fee = Fraction(m.group(1)), Fraction(m.group(2)) if m.group(2) else Fraction(0)
    return AmountBinding("record_percent", value=fee, coef=pct / 100, expr=m.group(0).strip(),
                         operands=(("operand", "single outgoing record amount to the recipient", "get_most_recent_transactions"),))


@dataclass(frozen=True)
class Refund:
    cid: int
    amount: Fraction
    clause: str


def compile_e1(objective: str) -> List[K.Contract]:
    out = []
    for c in K.compile_contracts(objective):
        if c.binding.kind == "unresolved" and c.binding.reason == CUE_REASON:
            b = _e1(c)
            if b is not None:
                c = K.Contract(c.cid, c.effects, c.target, c.account, b, c.condition, c.count, c.clause)
        out.append(c)
    return out


def compile_e2(objective: str) -> List[Refund]:
    out = []
    for n, s in enumerate(re.split(r"(?<=[.!?])\s+", objective)):
        if not (E2_REFUND.search(s) and E2_RECEIVED.search(s)) or V1._accounts(s):
            continue
        clause = re.split(r"\b(?:and|also)\b(?=\s+(?:send|pay|transfer|update|schedule))", s, flags=re.I)[0]
        nums = re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])", K._blank(K._blank(clause, K.DATES), K.IDS))
        if len(nums) != 1:
            continue
        out.append(Refund(E2_BASE + n, Fraction(nums[0]), clause))
    return out


def binding_status(b: AmountBinding, a: Fraction, hist, rcp):
    if b.kind != "record_percent":
        return V2._binding_status(b, a, hist, rcp)
    amts = outgoing_amounts(hist, rcp) if rcp else set()
    if len(amts) != 1:
        return "unresolved", None, ("no single outgoing record to the recipient" if not amts else "several outgoing records")
    x = b.coef * next(iter(amts)) + b.value
    if a == x:
        return "verified", x, "equal to the amount the instruction determines"
    return "mismatch", x, "differs from the amount the instruction determines"


def decide(contracts, ledger, hist, tool: str, args: Mapping[str, Any]) -> K.Decision:
    """contracts.decide with the E1 binding; otherwise identical (same candidate order and status precedence)."""
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
            st, x, why = binding_status(c.binding, Fraction(a), hist, rcp)
        if x is not None:
            expected.append(V1._fmt(x))
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


def refund_witness(refunds: List[Refund], ledger, hist, tool: str, args: Mapping[str, Any]) -> Optional[Refund]:
    """The E2 licence that covers this call, or None."""
    if tool != "send_money" or not refunds:
        return None
    rcp = canon_iban(args.get("recipient")) if isinstance(args.get("recipient"), str) else None
    a = amount_of(args.get("amount")) if args.get("amount") is not None else None
    if rcp is None or a is None:
        return None
    for r in refunds:
        if Fraction(a) == r.amount and incoming_senders(hist, r.amount) == {rcp}:
            if ledger.committed.get(r.cid, 0) + ledger.reserved.get(r.cid, 0) < 1:
                return r
    return None
