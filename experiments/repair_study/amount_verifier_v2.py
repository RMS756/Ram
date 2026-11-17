"""Typed amount verifier, version 2 (dated amendment of 17 November 2026, after the independent review of commit 621a271).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. Version 1 (amount_verifier.py) and its scored
results are unchanged. Version 2 changes ACCEPTANCE only, to repair two defects found by the review:

  D3  a supported PREFIX of a compound calculation was accepted ("half of 100 plus an additional 10": 50 verified).
      Version 2 requires the recognised statement to cover the whole AMOUNT PHRASE: the text from the payment verb that
      governs the statement to the account the statement binds to (or to the end of the sentence). Any operator or
      calculation word, or any number, left in that phrase after the recognised statements are removed makes the
      instruction UNRESOLVED. No new operation is supported; a prefix is no longer accepted.

  D4  the amount was taken from any instruction with the same effect and account, including one whose condition does not
      hold. Version 2 accepts a call only on ONE WITNESS: a single instruction whose effect and account license the call,
      whose own condition holds (or that has none), and whose own amount binding verifies the proposed amount (or states
      nothing about it). An instruction whose condition is false is not a witness; one whose condition cannot be evaluated
      makes the result unresolved unless another instruction is a complete witness. Conditions are evaluated exactly as
      by the frozen front (permission_v3.holds on the most recent executed get_balance, permission_v2._balance).

Optional grammar EXTENSION (separate flag, separate arms, measured separately): an appositive stated amount
"VERB <description>, NUM to ACCOUNT" (e.g. "send the enrolment fee, 320 to X"), whose description contains no number and
no operator word; descriptive nouns such as "fee" are then not calculation words.

Everything else (typed bindings, exact rationals, evidence rules, no rounding/currency/tolerance assumption) is version 1.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, List, Mapping, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "improve_study"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import amount_verifier as V1                                     # noqa: E402  (frozen version 1; reused, not changed)
from amount_verifier import AmountBinding, _accounts, _finite_decimal, _fmt, _masked, _places, sentence_bindings  # noqa: E402
from intent import amount_of, canon_iban, clean                 # noqa: E402
from intent_v3 import TOOL_EFFECT, compile_intent_v3             # noqa: E402
from permission_v2 import _balance                               # noqa: E402  (frozen front: balance used for conditions)
from permission_v3 import holds                                  # noqa: E402  (frozen front: condition evaluation)

_VERB = re.compile(r"\b(?:send|transfer|pay|wire|remit|refund|reimburse|repay|give|return|schedule|set\s+up|create|update|change)\b", re.I)
# operator and calculation words; any of them left in the amount phrase makes the instruction unresolved
_OPS = re.compile(r"\b(plus|minus|additional|additionally|extra|total|totals|totaling|totalling|difference|more|less|increase[sd]?|"
                  r"decrease[sd]?|discount(?:ed)?|add|added|adding|including|excluding|minus|times|twice|double|half|halves|third|"
                  r"thirds|quarter|quarters|percent|per\s+cent|remaining|remainder|rest|split|divide[sd]?|share|fee|fees|tax|vat|"
                  r"interest|too\s+much|too\s+little|same\s+amount|as\s+much\s+as|of\s+it|of\s+that)\b|[%+×*/=]|\s-\s", re.I)
_NOUNS = re.compile(r"\b(fee|fees|tax|vat|interest|share|bill|rent|invoice|deposit|subscription|payment)\b", re.I)
_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}(?:st|nd|rd|th)\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b", re.I)
_CURW = r"(?:\s?(?:dollars?|euros?|pounds?|usd|eur|gbp))?"
_APPOS = re.compile(r",\s*(?:[$€£]\s?)?(\d[\d.,]*\d|\d)" + _CURW + r"(?=\s+to\s+#)", re.I)


def _phrase(text: str, pos: int, accts) -> Tuple[int, int]:
    """Amount phrase of a statement at pos: from the governing verb to the bound account (or the end of the sentence)."""
    starts = [m.start() for m in _VERB.finditer(text) if m.start() <= pos]
    s = starts[-1] if starts else 0
    after = [a for a in accts if a[0] >= pos]
    e = after[0][0] if after else len(text)
    return s, e


def _uncovered(residual: str, s: int, e: int, desc: Optional[Tuple[int, int]] = None) -> Optional[str]:
    """Reason why the amount phrase residual[s:e] is not covered, or None. With the extension, descriptive nouns inside
    the appositive description desc are names, not calculation words."""
    seg = residual[s:e]
    if desc is not None:
        a, b = max(desc[0], s) - s, min(desc[1], e) - s
        if a < b:
            seg = seg[:a] + _NOUNS.sub(lambda m: " " * len(m.group(0)), seg[a:b]) + seg[b:]
    seg = _DATE.sub(lambda m: " " * len(m.group(0)), seg)
    m = _OPS.search(seg)
    if m:
        return f"amount phrase not covered by a supported expression ('{m.group(0).strip()}')"
    if re.search(r"\d", seg):
        return "a number in the amount phrase is not part of a supported expression"
    return None


@dataclass(frozen=True)
class Witness:
    ins: Any
    account: Optional[str]
    binding: AmountBinding


def compile_bindings(objective: str, appositive: bool = False) -> List[Witness]:
    """Per payment instruction of the frozen compiler: one binding per account, with the D3 coverage check."""
    out: List[Witness] = []
    for ins in compile_intent_v3(objective).instructions:
        if not (ins.effects & {"transfer_now", "schedule_create", "schedule_modify"}):
            continue
        sentence = ins.span.text
        accts = _accounts(sentence)
        residual: list = []
        found = list(sentence_bindings(sentence, residual))
        res = residual[0]
        text = _masked(sentence)
        appos_desc = {}
        if appositive and not found:
            for m in _APPOS.finditer(text):
                v, amb = V1._num(m.group(1))
                verbs = [x.start() for x in _VERB.finditer(text) if x.start() < m.start()]
                if not verbs:
                    continue
                desc = (verbs[-1], m.start())
                if re.search(r"\d", text[desc[0]:desc[1]]) or _OPS.search(_NOUNS.sub(" ", text[desc[0]:desc[1]])):
                    continue
                tgt = V1._bind_target(m.start(1), accts)
                b = (AmountBinding("unresolved", expr=m.group(1), reason="ambiguous number format of a stated amount") if (amb or v is None)
                     else AmountBinding("literal", value=v, expr=m.group(1), operands=(("amount", _fmt(v), "request"),)))
                found.append((tgt, b, m.start(1)))
                appos_desc[m.start(1)] = desc
                res = res[:m.start(1)] + " " * (m.end(1) - m.start(1)) + res[m.end(1):]
        groups: dict = {}
        for t, b, p in found:
            if ins.target is not None and not (t == ins.target or (t is None and len(accts) <= 1)):
                continue
            s, e = _phrase(text, p, accts)
            why = _uncovered(res, s, e, appos_desc.get(p))
            if why is not None and b.kind != "unresolved":
                b = AmountBinding("unresolved", expr=b.expr, reason=why)
            groups.setdefault(ins.target if ins.target is not None else t, []).append(b)
        if groups:
            for acct, stmts in groups.items():
                out.append(Witness(ins, acct, V1._combine(stmts)))
            continue
        if V1._CUES.search(res):                             # identical to version 1 when no statement is found
            b = AmountBinding("unresolved", reason="calculation cue without a supported expression")
        elif V1._REFUND.search(sentence) and V1._SENT_BY.search(sentence) and len(accts) <= 1:
            b = AmountBinding("record_refund", expr="amount of the incoming record(s) from the bound account",
                              operands=(("operand", "incoming record amount", "get_most_recent_transactions"),))
        else:
            b = AmountBinding("none")
        out.append(Witness(ins, ins.target, b))
    return out


@dataclass
class History:
    """Executed tool results (frozen-front format: tool, args, text, executed)."""
    rows: List[Tuple[str, Any, str, bool]] = field(default_factory=list)

    def balance(self):
        return _balance(self.rows)

    def v1(self) -> V1.History:
        return V1.History([(t, x, e) for t, _a, x, e in self.rows])


@dataclass(frozen=True)
class Verdict:
    status: str                     # verified | mismatch | unresolved | unconstrained
    expected: Tuple[str, ...] = ()
    reason: str = ""
    witness: Optional[str] = None   # clause of the witnessing instruction


def _binding_status(b: AmountBinding, a: Fraction, hist: History, rcp) -> Tuple[str, Optional[Fraction], str]:
    if b.kind == "none":
        return "unconstrained", None, "the instruction states nothing about the amount"
    if b.kind in ("literal", "derived"):
        x = b.value
    elif b.kind == "balance_expr":
        bal = hist.v1().balance()
        if bal is None:
            return "unresolved", None, "balance operand not read successfully"
        x = b.coef * bal
        if not _finite_decimal(x):
            return "unresolved", None, "result is not a finite decimal; rounding convention unspecified"
    elif b.kind == "record_refund":
        amts = hist.v1().incoming_amounts(rcp) if rcp else set()
        if len(amts) != 1:
            return "unresolved", None, ("no single incoming record from the bound account" if not amts else "several incoming records")
        x = next(iter(amts))
    else:
        return "unresolved", None, b.reason or "unresolved"
    if a == x:
        return "verified", x, "equal to the amount the instruction determines"
    p = _places(a)
    if _places(x) > p and abs(x - a) < Fraction(1, 10 ** p):
        return "unresolved", x, "proposed amount may be a rounding of the computed amount; rounding convention unspecified"
    return "mismatch", x, "differs from the amount the instruction determines"


def verify(compiled: List[Witness], hist: History, tool: str, args: Mapping[str, Any]) -> Verdict:
    """Accept only on one witnessing instruction (effect, account, own condition, own amount)."""
    eff = TOOL_EFFECT.get(tool)
    args = args or {}
    if eff is None or "amount" not in args or args.get("amount") is None:
        return Verdict("unconstrained", reason="no amount argument or not a payment tool")
    rcp = canon_iban(args.get("recipient")) if isinstance(args.get("recipient"), str) else None
    lic = [w for w in compiled if eff in w.ins.effects]
    cand = ([w for w in lic if rcp is not None and w.ins.target == rcp]
            or [w for w in lic if w.ins.target is None and w.account in (None, rcp)])
    if not cand:
        return Verdict("unconstrained", reason="no instruction of the request licenses this effect and account")
    a = amount_of(args.get("amount"))
    if a is None:
        return Verdict("unresolved", reason="proposed amount is not an exact number")
    a = Fraction(a)
    bal = hist.balance()
    pending, mismatched, expected = [], [], []
    for w in cand:
        c = w.ins.condition
        ok = True if c is None else holds(c, bal)
        st, x, why = _binding_status(w.binding, a, hist, rcp)
        if x is not None:
            expected.append(_fmt(x))
        if ok is False:
            continue                                        # not a witness: its condition does not hold
        if ok is None:
            pending.append("the condition of the instruction cannot be evaluated")
            continue
        if st in ("verified", "unconstrained"):
            return Verdict("verified" if st == "verified" else "unconstrained", tuple(expected), why, w.ins.span.text[:80])
        (pending if st == "unresolved" else mismatched).append(why)
    if pending:
        return Verdict("unresolved", tuple(expected), "; ".join(sorted(set(pending))))
    if mismatched:
        return Verdict("mismatch", tuple(expected), "; ".join(sorted(set(mismatched))))
    return Verdict("mismatch", tuple(expected), "no instruction whose condition holds licenses this call")
