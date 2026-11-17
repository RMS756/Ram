"""Typed verification of payment amounts against the trusted request (repair study, 17 November 2026).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. Deterministic; no model call; no fitted
quantity; no equation of this module is a research contribution: it applies elementary exact arithmetic (Python's
``fractions.Fraction`` over ``decimal.Decimal`` operands) to a finite, declared grammar. The frozen compiler,
matchers, direct-value constraint and every scored arm are unchanged and are imported, not edited.

Central rule: recognizing a calculation cue is not verification of the proposed amount. Each payment instruction of
the request (from the frozen revision-3 compiler) receives one AMOUNT BINDING:

  literal          the request states the final amount directly ("send 27.35 to A")
  derived          the request states a supported arithmetic expression whose operands are literals of the request
                   ("half of 100", "25 percent of 200", "3/4 of 80", "twice 40"); the result is computed exactly
  balance_expr     the same expressions with the operand "my (current|account) balance"; the operand is the most
                   recent successful get_balance result (a structured bank field), read at decision time
  record_refund    "refund / return / send back / pay back ... what <they> sent (me)" with no arithmetic cue: the amount
                   of the incoming structured transaction record(s) from the bound account
  unresolved       a calculation cue without a supported expression, an ambiguous number format, an operand that is not
                   available, a result that is not a finite decimal (rounding unspecified), or conflicting statements
  none             the request says nothing about the amount of this instruction (no constraint is added here)

ACCEPTED GRAMMAR (case-insensitive; NUM is a numeric token parsed by the frozen ``parse_amount``; CUR is $, €, £ or the
words dollars, euros, pounds, usd, eur, gbp):

  LITERAL      VERB [the | that | this | exactly | only | just] [CUR] NUM [CUR]          not followed by %, "percent", "per cent",
                                                                              "/", "of" or "times"
               (amount | sum | payment | transfer | refund) of [CUR] NUM
               and [CUR] NUM to ACCOUNT                                     (elided verb: "send 50 to A and 30 to B")
  PERCENT      P (% | percent | per cent) of [the] [CUR] OPERAND            P a NUM; result P x OPERAND / 100
  FRACTION     (half | a half | one half) of [the] [CUR] OPERAND             1/2
               (a third | one third) | two thirds | (a quarter | one quarter) | three quarters   1/3, 2/3, 1/4, 3/4
               a/b of [the] [CUR] OPERAND with integers 1 <= a <= b <= 99, b > 0
  MULTIPLE     (twice | double) [the amount of] [CUR] OPERAND                2 x OPERAND
  OPERAND      NUM | my [current | account] balance
  (a stated amount must be followed by the end of the sentence, punctuation, an account identifier, a capitalised word
   or a function word such as "to", "for", "now"; "send the 3 tickets" states no amount)
  VERB         send | transfer | pay | wire | remit | refund | reimburse | repay | give | return

  A literal or expression binds to the first account identifier that follows it in the same sentence; if none follows,
  to the last one before it; a sentence without an account identifier binds to the instruction without a target.
  Numbers inside quoted text, inside account identifiers, and inside the condition of the sentence are never operands.

  CALCULATION CUES, searched in the sentence after recognised statements are removed (an instruction with one of them and no supported expression or literal is UNRESOLVED):
  half, third, quarter, twice, double, percent, per cent, %, difference, share, split, divide, total, sum of, plus,
  minus, remaining, remainder, the rest, additional, extra, increase, decrease, discount, fee, vat, tax, interest,
  too much, too little, times, more, less, the same amount, as much as.

Rounding: no convention is assumed. A result that is not a finite decimal is unresolved. A finite result must be equal,
exactly, to the proposed amount; a proposed amount with fewer decimal places that lies within one unit of its last place
of the result (e.g. 70.46 for 70.455) is unresolved (withheld), not accepted and not called a mismatch.

Untrusted tool text never supplies an operand, a coefficient, an expected result or an account. The only values read
from tool outputs are structured bank fields: the number returned by get_balance and the ``sender`` and ``amount``
fields of transaction records returned by get_most_recent_transactions (never their free-text ``subject``).
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, List, Mapping, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "improve_study"))

import intent as V1                                   # noqa: E402  (frozen)
from intent import amount_of, canon_iban, clean, parse_amount   # noqa: E402
from intent_v3 import TOOL_EFFECT, _condition_segment, compile_intent_v3   # noqa: E402

_CUR = r"(?:[$€£]\s?)?"
_CURW = r"(?:\s?(?:dollars?|euros?|pounds?|usd|eur|gbp))?"
_NUMT = r"(\d[\d.,]*\d|\d)"
_VERB = r"(?:send|transfer|pay|wire|remit|refund|reimburse|repay|give|return)"
_NOT_COEF = r"(?!\s*(?:%|percent\b|per\s+cent\b|/\s*\d|of\b|times\b)|[\d.,]*\d)"
_LIT1 = re.compile(r"\b" + _VERB + r"\s+(?:(?:the|that|this|exactly|only|just)\s+)?" + _CUR + _NUMT + _NOT_COEF + _CURW, re.I)
_LIT3 = re.compile(r"\band\s+" + _CUR + _NUMT + _NOT_COEF + _CURW + r"(?=\s+to\s+#)", re.I)   # "... and 30 to <account>"
_LIT2 = re.compile(r"\b(?:amount|sum|payment|transfer|refund)\s+of\s+" + _CUR + _NUMT + _NOT_COEF + _CURW, re.I)
_OPERAND = r"(?:the\s+)?" + _CUR + r"(?:" + _NUMT + r"|(my\s+(?:current\s+|account\s+)?balance))"
_PCT = re.compile(r"(?<![\w.,])" + _NUMT + r"\s*(?:%|percent\b|per\s+cent\b)\s+of\s+" + _OPERAND, re.I)
_FRACW = re.compile(r"\b(a\s+half|one\s+half|half|a\s+third|one\s+third|two\s+thirds|a\s+quarter|one\s+quarter|three\s+quarters)\s+of\s+" + _OPERAND, re.I)
_FRACN = re.compile(r"(?<![\w.,/])(\d{1,2})\s*/\s*(\d{1,2})\s+of\s+" + _OPERAND, re.I)
_MULT = re.compile(r"\b(twice|double)\s+(?:the\s+amount\s+of\s+)?" + _OPERAND, re.I)
# A stated amount must be followed by the end of the sentence, punctuation, an account identifier (masked as '#'), a
# capitalised word, or one of these function words; otherwise the number counts something ("send the 3 tickets").
_FOLLOW = re.compile(r"\s*(?:$|[.,;:!?)\]#]|[A-Z]|(?:to|for|from|into|on|at|by|as|and|or|now|today|tomorrow|immediately|back|with|via|"
                     r"in|using|once|monthly|weekly|daily|yearly|each|every|please|right|which|that|so|because|since|before|after|then|"
                     r"but|if|when|until)\b)")
_FRAC_WORDS = {"half": Fraction(1, 2), "a half": Fraction(1, 2), "one half": Fraction(1, 2), "a third": Fraction(1, 3),
               "one third": Fraction(1, 3), "two thirds": Fraction(2, 3), "a quarter": Fraction(1, 4), "one quarter": Fraction(1, 4),
               "three quarters": Fraction(3, 4)}
_CUES = re.compile(r"\b(half|third|thirds|quarter|quarters|twice|double|percent|per\s+cent|difference|share|split|divide|total|sum\s+of|plus|minus|"
                   r"remaining|remainder|the\s+rest|additional|extra|increase[sd]?|decrease[sd]?|discount|fee|vat|tax|interest|too\s+much|too\s+little|"
                   r"times|more|less|the\s+same\s+amount|as\s+much\s+as)\b|%", re.I)
_REFUND = re.compile(r"\b(refund|return|send\s+back|pay\s+back|give\s+back|send\s+\w+\s+back|pay\s+\w+\s+back)\b", re.I)
_SENT_BY = re.compile(r"\bwhat\s+(?:they|he|she|it)\s*(?:'ve|\s+have|\s+has|'s)?\s+(?:sent|paid|transferred)\b", re.I)


@dataclass(frozen=True)
class AmountBinding:
    kind: str                                   # literal | derived | balance_expr | record_refund | unresolved | none
    value: Optional[Fraction] = None            # literal / derived result
    coef: Optional[Fraction] = None             # balance_expr coefficient
    expr: str = ""
    operands: Tuple[Tuple[str, str, str], ...] = ()   # (role, value, source)
    reason: str = ""


@dataclass(frozen=True)
class Verdict:
    status: str                                 # verified | mismatch | unresolved | unconstrained
    expected: Tuple[str, ...] = ()
    reason: str = ""
    bindings: Tuple[AmountBinding, ...] = ()


def _num(tok: str) -> Tuple[Optional[Fraction], bool]:
    v, amb = parse_amount(tok)
    return (Fraction(v) if v is not None else None), amb


def _finite_decimal(x: Fraction) -> bool:
    d = x.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def _places(x: Fraction) -> int:
    """Decimal places of a finite decimal (large for a non-terminating one)."""
    if not _finite_decimal(x):
        return 10 ** 6
    k = 0
    while (x * 10 ** k).denominator != 1:
        k += 1
    return k


def _fmt(x: Fraction) -> str:
    if _finite_decimal(x):
        return str(Decimal(x.numerator) / Decimal(x.denominator))
    return f"{x.numerator}/{x.denominator}"


def _masked(sentence: str) -> str:
    """Same-length copy with quoted text and account identifiers blanked, so they are never operands."""
    out = list(sentence)
    for rx in (V1._QUOTED, V1.IBAN_RE):
        for m in rx.finditer(sentence):
            for k in range(m.start(), m.end()):
                out[k] = "#"
    seg = _condition_segment(sentence)
    if seg is not None:
        s, e, _w = seg
        for k in range(max(0, s - 12), e):             # the condition keyword and its expression
            if out[k].isdigit():
                out[k] = "#"
    return "".join(out)


def _accounts(sentence: str) -> List[Tuple[int, int, str]]:
    return [(m.start(), m.end(), canon_iban(m.group(1))) for m in V1.IBAN_RE.finditer(sentence) if canon_iban(m.group(1))]


def _bind_target(pos: int, accounts: List[Tuple[int, int, str]]) -> Optional[str]:
    after = [a for a in accounts if a[0] >= pos]
    if after:
        return after[0][2]
    before = [a for a in accounts if a[1] <= pos]
    return before[-1][2] if before else None


def _operand(m: re.Match, num_group: int, bal_group: int):
    if m.group(bal_group):
        return "balance", None, False
    v, amb = _num(m.group(num_group))
    return "literal", v, amb


def sentence_bindings(sentence: str, residual: Optional[list] = None) -> List[Tuple[Optional[str], AmountBinding, int]]:
    """All amount statements of one sentence: (bound account or None, binding, position).

    If ``residual`` is a list, the masked sentence with every recognised statement blanked is appended to it (calculation
    cues are searched in that residual text, so the word "half" of a recognised "half of 100" is not a second cue)."""
    text = _masked(sentence)
    accts = _accounts(sentence)
    found = []
    taken = []

    def free(s, e):
        return not any(a < e and s < b for a, b in taken)

    for rx, kind in ((_PCT, "pct"), (_FRACN, "fracn"), (_FRACW, "fracw"), (_MULT, "mult")):
        for m in rx.finditer(text):
            if not free(m.start(), m.end()):
                continue
            if kind == "pct":
                c, amb = _num(m.group(1))
                coef, label = (c / 100 if c is not None else None), f"{m.group(1)}%"
                okind, ov, oamb = _operand(m, 2, 3)
            elif kind == "fracn":
                a, b = int(m.group(1)), int(m.group(2))
                amb = not (1 <= a <= b <= 99)
                coef, label = (Fraction(a, b) if not amb else None), f"{a}/{b}"
                okind, ov, oamb = _operand(m, 3, 4)
            elif kind == "fracw":
                w = re.sub(r"\s+", " ", m.group(1).lower())
                coef, label, amb = _FRAC_WORDS[w], w, False
                okind, ov, oamb = _operand(m, 2, 3)
            else:
                coef, label, amb = Fraction(2), "2 x", False
                okind, ov, oamb = _operand(m, 2, 3)
            taken.append((m.start(), m.end()))
            tgt = _bind_target(m.start(), accts)
            if amb or oamb or coef is None:
                found.append((tgt, AmountBinding("unresolved", expr=m.group(0), reason="ambiguous number format in the expression"), m.start()))
            elif okind == "balance":
                found.append((tgt, AmountBinding("balance_expr", coef=coef, expr=f"{label} of balance",
                                                 operands=(("coefficient", _fmt(coef), "request"), ("operand", "balance", "get_balance"))), m.start()))
            else:
                res = coef * ov
                if not _finite_decimal(res):
                    found.append((tgt, AmountBinding("unresolved", expr=m.group(0), reason="result is not a finite decimal; rounding convention unspecified"), m.start()))
                else:
                    found.append((tgt, AmountBinding("derived", value=res, expr=f"{label} of {_fmt(ov)}" if kind != "mult" else f"2 x {_fmt(ov)}",
                                                     operands=(("coefficient", _fmt(coef), "request"), ("operand", _fmt(ov), "request"))), m.start()))
    for rx in (_LIT1, _LIT2, _LIT3):
        for m in rx.finditer(text):
            s, e = m.start(1), m.end(1)
            if not free(s, e) or not _FOLLOW.match(text, m.end()):
                continue
            taken.append((s, e))
            v, amb = _num(m.group(1))
            tgt = _bind_target(s, accts)
            if amb or v is None:
                found.append((tgt, AmountBinding("unresolved", expr=m.group(1), reason="ambiguous number format of a stated amount"), s))
            else:
                found.append((tgt, AmountBinding("literal", value=v, expr=m.group(1), operands=(("amount", _fmt(v), "request"),)), s))
    if residual is not None:
        out = list(text)
        for a, b in taken:
            for k in range(a, b):
                out[k] = " "
        residual.append("".join(out))
    return found


def _combine(stmts: List[AmountBinding]) -> AmountBinding:
    kinds = {b.kind for b in stmts}
    if "unresolved" in kinds:
        return next(x for x in stmts if x.kind == "unresolved")
    if len(stmts) == 1:
        return stmts[0]
    vals = {x.value for x in stmts if x.kind in ("literal", "derived")}
    if len(vals) == 1 and "balance_expr" not in kinds:
        return next(x for x in stmts if x.kind == "literal") if "literal" in kinds else stmts[0]
    return AmountBinding("unresolved", reason="several different amounts stated for one instruction")


def compile_bindings(objective: str):
    """Per payment instruction of the frozen revision-3 compiler: (instruction, account, binding).

    ``account`` is the account the binding applies to: the instruction's target if it has one; for an instruction
    without a target (the frozen compiler leaves some targets unbound), the account each statement binds to in the
    sentence (None: any account the authority front admits)."""
    out = []
    for ins in compile_intent_v3(objective).instructions:
        if not (ins.effects & {"transfer_now", "schedule_create", "schedule_modify"}):
            continue
        sentence = ins.span.text
        accts = _accounts(sentence)
        residual: list = []
        found = sentence_bindings(sentence, residual)
        cues = bool(_CUES.search(residual[0]))
        if ins.target is not None:
            groups = {ins.target: [b for t, b, _p in found if t == ins.target or (t is None and len(accts) <= 1)]}
        else:
            groups: dict = {}
            for t, b, _p in found:
                groups.setdefault(t, []).append(b)
        groups = {k: v for k, v in groups.items() if v}
        if groups:
            for acct, stmts in groups.items():
                out.append((ins, acct, _combine(stmts)))
            continue
        if cues:
            b = AmountBinding("unresolved", reason="calculation cue without a supported expression")
        elif _REFUND.search(sentence) and _SENT_BY.search(sentence) and len(accts) <= 1:
            b = AmountBinding("record_refund", expr="amount of the incoming record(s) from the bound account",
                              operands=(("operand", "incoming record amount", "get_most_recent_transactions"),))
        else:
            b = AmountBinding("none")
        out.append((ins, ins.target, b))
    return out


@dataclass
class History:
    """Executed tool results seen by the guard (structured bank fields only are used)."""
    rows: List[Tuple[str, str, bool]] = field(default_factory=list)   # (tool, text, executed)

    def balance(self) -> Optional[Fraction]:
        for tool, text, executed in reversed(self.rows):
            if tool == "get_balance" and executed:
                nums = re.findall(r"-?\d[\d.,]*", clean(text or ""))
                if len(nums) == 1 and not nums[0].startswith("-"):
                    v, amb = parse_amount(nums[0])
                    return Fraction(v) if v is not None and not amb else None
                return None
        return None

    def incoming_amounts(self, sender: str) -> set:
        out = set()
        for tool, text, executed in self.rows:
            if tool != "get_most_recent_transactions" or not executed:
                continue
            try:
                import yaml
                recs = yaml.safe_load(clean(text))
            except Exception:
                continue
            for r in recs if isinstance(recs, list) else []:
                if isinstance(r, dict) and isinstance(r.get("sender"), str) and canon_iban(r["sender"]) == sender:
                    a = amount_of(r.get("amount"))
                    if a is not None:
                        out.add(Fraction(a))
        return out


def verify(compiled, history: History, tool: str, args: Mapping[str, Any]) -> Verdict:
    """Status of a proposed call's amount against the instructions that license its effect and account."""
    eff = TOOL_EFFECT.get(tool)
    args = args or {}
    if eff is None or "amount" not in args or args.get("amount") is None:
        return Verdict("unconstrained", reason="no amount argument or not a payment tool")
    rcp = canon_iban(args.get("recipient")) if isinstance(args.get("recipient"), str) else None
    lic = [(i, acct, b) for i, acct, b in compiled if eff in i.effects]
    cand = ([(i, acct, b) for i, acct, b in lic if rcp is not None and i.target == rcp]
            or [(i, acct, b) for i, acct, b in lic if i.target is None and acct in (None, rcp)])
    binds = tuple(b for _i, _a, b in cand if b.kind != "none")
    if not binds:
        return Verdict("unconstrained", reason="the request states nothing about this amount")
    a = amount_of(args.get("amount"))
    if a is None:
        return Verdict("unresolved", reason="proposed amount is not an exact number", bindings=binds)
    a = Fraction(a)
    expected, pending = [], []
    for b in binds:
        if b.kind in ("literal", "derived"):
            expected.append(b.value)
        elif b.kind == "balance_expr":
            bal = history.balance()
            if bal is None:
                pending.append("balance operand not read successfully")
                continue
            res = b.coef * bal
            if not _finite_decimal(res):
                pending.append("result is not a finite decimal; rounding convention unspecified")
                continue
            expected.append(res)
        elif b.kind == "record_refund":
            amts = history.incoming_amounts(rcp) if rcp else set()
            if len(amts) == 1:
                expected.append(next(iter(amts)))
            else:
                pending.append("no single incoming record from the bound account" if not amts else "several incoming records from the bound account")
        else:
            pending.append(b.reason or "unresolved")
    exp = tuple(_fmt(x) for x in expected)
    if a in expected:
        return Verdict("verified", exp, "proposed amount equals the verified amount", binds)
    places = _places(a)
    if any(_places(x) > places and abs(x - a) < Fraction(1, 10 ** places) for x in expected):
        pending.append("proposed amount may be a rounding of the computed amount; rounding convention unspecified")
    if pending:
        return Verdict("unresolved", exp, "; ".join(pending), binds)
    return Verdict("mismatch", exp, "proposed amount differs from the amount the request determines", binds)
