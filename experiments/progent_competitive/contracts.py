"""Financial contracts with a per-instruction ledger (candidate C1 of the study of 18 November 2026).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. Specification: 01_DESIGN_DECISION_RECORD.md.
Reuses, unchanged: the revision-3 compiler (instructions, conditions, repeat counts), the version-1 amount grammar
(sentence_bindings: literal, percent, fractions, multiples, balance expressions) and the version-2 evaluation of a binding
(exact rationals; no rounding, currency or tolerance rule). New here:

  * stable contract ids (compile order of the revision-3 instructions);
  * amount SCOPE from the governing payment verb to the next payment verb that starts another instruction, or the end of
    the sentence; it does NOT stop at the account (review F1). Operator words or stray numbers left in the scope make
    the contract unresolved. Descriptive nouns (fee, bill, rent, ...) are not operators;
  * appositive stated amounts ("send the enrolment fee, 320 to X") as part of the grammar;
  * a SINGLE COMPLETE WITNESS: effect, account, own condition, own amount and own remaining allowance (review F2);
  * a LEDGER: reserve the witnessing contract when a call is released, commit on a successful execution signal, release
    on refusal or error; a duplicate success notification for the same call is ignored.

No eval/exec, no floating-point comparison, no model. Labels, task ids and evaluator state are never read.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
for _p in ("experiments/repair_study", "experiments/improve_study"):
    sys.path.insert(0, str(ROOT / _p))

import amount_verifier as V1                                          # noqa: E402  (frozen grammar)
import amount_verifier_v2 as V2                                       # noqa: E402  (frozen v2 binding evaluation)
from amount_verifier import AmountBinding, _accounts, _masked, sentence_bindings  # noqa: E402
from intent import amount_of, canon_iban                             # noqa: E402
from intent_v3 import TOOL_EFFECT, compile_intent_v3                 # noqa: E402
from permission_v3 import holds                                      # noqa: E402

MONEY_EFFECTS = {"transfer_now", "schedule_create", "schedule_modify"}
PAY_VERB = re.compile(r"\b(?:send|transfer|pay|wire|remit|refund|reimburse|repay|give|return|schedule|set\s+up|create|update|change)\b", re.I)
OPERATORS = re.compile(
    r"\b(plus|minus|additional|additionally|extra|more|less|total|totals|totaling|totalling|in\s+total|sum\s+of|difference|"
    r"increase[sd]?|decrease[sd]?|discount(?:ed)?|add|added|adding|including|excluding|times|twice|double|half|halves|third|thirds|"
    r"quarter|quarters|percent|per\s+cent|remaining|remainder|the\s+rest|split|divide[sd]?|too\s+much|too\s+little|same\s+amount|"
    r"as\s+much\s+as|of\s+it|of\s+that)\b|[%+×*/=]|\s-\s", re.I)
REPEAT = re.compile(r"\b(once|twice|thrice|(?:two|three|four|five|\d+)\s+times|every\s+(?:month|week|day|year)|monthly|weekly|daily|yearly|annually)\b", re.I)
DATES = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}(?:st|nd|rd|th)\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b(?:19|20)\d{2}\b(?=\s*(?:[.,;)]|$))", re.I)
IDS = re.compile(r"\b(?:invoice|order|id|ref|reference|no\.?|number|ticket|booking|case)\s*#?\s*[A-Z0-9-]*\d[A-Z0-9-]*", re.I)
APPOS = re.compile(r",\s*(?:[$€£]\s?)?(\d[\d.,]*\d|\d)(?:\s?(?:dollars?|euros?|pounds?|usd|eur|gbp))?(?=\s+to\s+#)", re.I)


def _blank(text: str, rx) -> str:
    return rx.sub(lambda m: " " * len(m.group(0)), text)


@dataclass(frozen=True)
class Contract:
    cid: int
    effects: frozenset
    target: Optional[str]
    account: Optional[str]
    binding: AmountBinding
    condition: Any
    count: int
    clause: str


def _scope(text: str, pos: int) -> Tuple[int, int]:
    verbs = [m.start() for m in PAY_VERB.finditer(text)]
    s = max([v for v in verbs if v <= pos], default=0)
    nxt = [v for v in verbs if v > pos]
    return s, (nxt[0] if nxt else len(text))


def _uncovered(residual: str, s: int, e: int) -> Optional[str]:
    seg = _blank(_blank(_blank(residual[s:e], DATES), IDS), REPEAT)
    m = OPERATORS.search(seg)
    if m:
        return f"the amount expression is not covered completely ('{m.group(0).strip()}' is not part of a supported expression)"
    if re.search(r"\d", seg):
        return "a number in the amount expression is not part of a supported expression"
    return None


def compile_contracts(objective: str) -> List[Contract]:
    out: List[Contract] = []
    for cid, ins in enumerate(compile_intent_v3(objective).instructions):
        if not (ins.effects & MONEY_EFFECTS):
            continue
        sentence = ins.span.text
        accts = _accounts(sentence)
        residual: list = []
        found = list(sentence_bindings(sentence, residual))
        res = residual[0]
        text = _masked(sentence)
        if not found:                                             # appositive stated amount
            for m in APPOS.finditer(text):
                verbs = [x.start() for x in PAY_VERB.finditer(text) if x.start() < m.start()]
                if not verbs or re.search(r"\d", text[verbs[-1]:m.start()]) or OPERATORS.search(text[verbs[-1]:m.start()]):
                    continue
                v, amb = V1._num(m.group(1))
                tgt = V1._bind_target(m.start(1), accts)
                b = (AmountBinding("unresolved", expr=m.group(1), reason="ambiguous number format of a stated amount") if (amb or v is None)
                     else AmountBinding("literal", value=v, expr=m.group(1), operands=(("amount", V1._fmt(v), "request"),)))
                found.append((tgt, b, m.start(1)))
                res = res[:m.start(1)] + " " * (m.end(1) - m.start(1)) + res[m.end(1):]
        count = ins.count
        if any(b.kind == "derived" and b.expr.startswith("2 x") for _t, b, _p in found) and len(re.findall(r"\btwice\b", sentence, re.I)) == 1:
            count = 1                                              # "twice 40" is a multiplier, not a repetition
        groups: Dict[Optional[str], list] = {}
        for t, b, p in found:
            if ins.target is not None and not (t == ins.target or (t is None and len(accts) <= 1)):
                continue
            s, e = _scope(text, p)
            why = _uncovered(res, s, e)
            if why is not None and b.kind != "unresolved":
                b = AmountBinding("unresolved", expr=b.expr, reason=why)
            groups.setdefault(ins.target if ins.target is not None else t, []).append(b)
        if groups:
            for acct, stmts in groups.items():
                out.append(Contract(cid, frozenset(ins.effects), ins.target, acct, V1._combine(stmts), ins.condition, count, sentence))
            continue
        if V1._CUES.search(_blank(res, REPEAT)):
            b = AmountBinding("unresolved", reason="calculation cue without a supported expression")
        elif V1._REFUND.search(sentence) and V1._SENT_BY.search(sentence) and len(accts) <= 1:
            b = AmountBinding("record_refund", expr="amount of the incoming record(s) from the bound account",
                              operands=(("operand", "incoming record amount", "get_most_recent_transactions"),))
        else:
            b = AmountBinding("none")
        out.append(Contract(cid, frozenset(ins.effects), ins.target, ins.target, b, ins.condition, count, sentence))
    # The frozen compiler can split one sentence into two instructions (e.g. "for order #123" yields a second, open-target
    # instruction); once the amount binding is attached to the account, both describe the same payment. Their allowances
    # must not add up: contracts of the same sentence with the same effects, account, binding and condition are merged
    # (the bound target is kept, the larger count, the smaller id).
    merged: Dict[tuple, Contract] = {}
    for c in out:
        k = (c.clause, c.effects, c.account, c.binding.kind, c.binding.value, c.binding.coef, c.binding.expr, c.condition)
        if k in merged:
            m = merged[k]
            merged[k] = Contract(min(m.cid, c.cid), m.effects, m.target if m.target is not None else c.target, m.account, m.binding,
                                 m.condition, max(m.count, c.count), m.clause)
        else:
            merged[k] = c
    return sorted(merged.values(), key=lambda c: (c.cid, c.account or ""))


@dataclass
class Ledger:
    committed: Dict[int, int] = field(default_factory=dict)
    reserved: Dict[int, int] = field(default_factory=dict)
    pending: Optional[Tuple[str, int]] = None               # (tool, contract id) of the last released call, until its result

    def remaining(self, c: Contract) -> int:
        return c.count - self.committed.get(c.cid, 0) - self.reserved.get(c.cid, 0)

    def reserve(self, tool: str, cid: int) -> None:
        self.reserved[cid] = self.reserved.get(cid, 0) + 1
        self.pending = (tool, cid)

    def settle(self, tool: str, success: bool) -> None:
        if self.pending is None or self.pending[0] != tool:
            return                                            # no reservation for this result (refused call, read tool, duplicate)
        _t, cid = self.pending
        self.reserved[cid] -= 1
        if success:
            self.committed[cid] = self.committed.get(cid, 0) + 1
        self.pending = None


@dataclass(frozen=True)
class Decision:
    status: str                   # verified | unconstrained | mismatch | unresolved | exhausted | no_contract
    witness: Optional[int] = None
    expected: Tuple[str, ...] = ()
    reason: str = ""


def decide(contracts: List[Contract], ledger: Ledger, hist: V2.History, tool: str, args: Mapping[str, Any]) -> Decision:
    eff = TOOL_EFFECT.get(tool)
    args = args or {}
    if eff is None:
        return Decision("unconstrained", reason="not a payment tool")
    rcp = canon_iban(args.get("recipient")) if isinstance(args.get("recipient"), str) else None
    lic = [c for c in contracts if eff in c.effects]
    cand = ([c for c in lic if rcp is not None and c.target == rcp]
            or [c for c in lic if c.target is None and c.account in (None, rcp)])
    if not cand:
        return Decision("no_contract", reason="no instruction of the request licenses this effect and account")
    a = amount_of(args.get("amount")) if args.get("amount") is not None else None
    bal = hist.balance()
    ok, pending, exhausted, mismatched, expected = [], [], [], [], []
    for c in cand:
        cond = True if c.condition is None else holds(c.condition, bal)
        if a is None:
            st, x, why = (("unconstrained", None, "no amount argument") if c.binding.kind == "none"
                          else ("unresolved", None, "the call has no exact amount"))
        else:
            st, x, why = V2._binding_status(c.binding, Fraction(a), hist, rcp)
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
        return Decision(st, cid, tuple(expected), why)
    if pending:
        return Decision("unresolved", None, tuple(expected), "; ".join(sorted(set(pending))))
    if exhausted:
        return Decision("exhausted", None, tuple(expected), "; ".join(sorted(set(exhausted))))
    if mismatched:
        return Decision("mismatch", None, tuple(expected), "; ".join(sorted(set(mismatched))))
    return Decision("mismatch", None, tuple(expected), "no instruction whose condition holds licenses this call")
