"""Task-permission compiler, revision 2 (follow-up of 14 November 2026) — isolated improvement study.

Status: [PROPOSED — NOT PART OF THE APPROVED REM DESIGN]. Deterministic; no model call; no fitted quantity.
The frozen v1 compiler (``intent.py``, commit 9137b03) is unchanged and remains the scored candidate G1.

What v2 adds (every rule is a design choice of this follow-up, written before any v2 arm was scored):

1. **Instruction-level bindings.** The request is represented as a sequence of instructions. Each keeps its
   operation category, target account, amount (or the reason it is not fixed), condition, repeat count and the
   clause it came from TOGETHER. A call must match one coherent instruction; membership of its recipient in the
   set of named accounts and of its amount in the set of stated amounts is no longer sufficient.
2. **Conditions as predicates.** A detected condition is parsed into a predicate if it is of a supported form
   (a comparison of the account balance with a stated amount). Any other condition is kept as
   ``unsupported`` and is never treated as satisfied.
3. **Repeat counts** ("twice", "two times", "three times") so that an explicitly requested repetition is
   distinguished from an unintended duplicate.
4. **Three parser repairs**, prompted by fixture failures seen after scoring v1 (they are therefore not tests
   of v2): a month name must be a whole word (v1 read "Marta 36.40" as a date); ISO and slash dates are not
   amounts; "create/set up/start ... standing order" is a request for a value transfer.

It reads ONLY the request text (label isolation as in v1; tests/test_improve_study_v2.py).
"""
from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Tuple

import intent as V1
from intent import (CATEGORIES, IBAN_RE, AmountMention, Intent, Span, _clause_of, _clauses, _DERIVED, _NUM, _PAST,
                    canon_iban, clean, parse_amount)

# ------------------------------------------------------------------ v1 repairs
_MONTH_WORD = (r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december|"
               r"jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)\.?")
_DATE_TOKEN = re.compile(r"\b\d{4}-\d{1,2}-\d{1,2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b")
_EXTRA_REQ = [r"\b(create|set\s+up|start|open|add)\b[^.;]*\b(standing\s+orders?|recurring\s+(?:payments?|transfers?|transactions?))\b"]

# ------------------------------------------------------------------ conditions
_COND_WORD = re.compile(r"\b(if|unless|only\s+if|provided\s+that|in\s+case)\b", re.I)   # "when" is temporal in most requests
_CMP = {"above": ">", "over": ">", "more than": ">", "greater than": ">", "exceeds": ">", "higher than": ">",
        "at least": ">=", "not less than": ">=",
        "below": "<", "under": "<", "less than": "<", "lower than": "<", "at most": "<=", "not more than": "<="}
_BAL = re.compile(r"\b(?:my\s+)?(?:current\s+|account\s+)?balance\s+(?:is\s+|stays\s+|remains\s+)?(?P<op>not\s+less\s+than|not\s+more\s+than|"
                  r"above|over|more\s+than|greater\s+than|higher\s+than|exceeds|at\s+least|below|under|less\s+than|lower\s+than|at\s+most)"
                  r"\s+[$€£]?\s?(?P<num>\d[\d.,]*\d|\d)", re.I)
_REPEAT = re.compile(r"\b(twice|two\s+times|2\s+times|three\s+times|3\s+times)\b", re.I)


@dataclass(frozen=True)
class Condition:
    kind: str                       # 'balance' | 'unsupported'
    op: str = ""                    # '>', '>=', '<', '<='
    threshold: Optional[Decimal] = None
    negated: bool = False           # 'unless'
    text: str = ""


@dataclass(frozen=True)
class Instruction:
    category: str                   # value_transfer | payment_modification | credential_change | profile_change
    target: Optional[str]           # canonical account identifier, or None if the request does not name one
    amount: Optional[Decimal]       # stated amount bound to this instruction, or None
    amount_ambiguous: bool
    condition: Optional[Condition]
    count: int                      # number of executions the request asks for
    clause: int
    span: Span


@dataclass(frozen=True)
class IntentV2:
    base: Intent                    # v1 representation, with the three parser repairs applied
    instructions: Tuple[Instruction, ...]


def _parse_condition(clause: str) -> Optional[Condition]:
    m = _COND_WORD.search(clause)
    if not m:
        return None
    rest = clause[m.end():]
    b = _BAL.search(rest)
    neg = m.group(1).lower() == "unless"
    if b:
        val, amb = parse_amount(b.group("num"))
        op = _CMP[re.sub(r"\s+", " ", b.group("op").lower())]
        if val is not None and not amb:
            return Condition("balance", op, val, neg, clause[m.start():m.end() + b.end()])
    return Condition("unsupported", negated=neg, text=clause[m.start():].strip()[:120])


def _repeat(clause: str) -> int:
    m = _REPEAT.search(clause)
    if not m:
        return 1
    w = m.group(1).lower()
    return 3 if w.startswith(("three", "3")) else 2


def _amounts_v2(g: str, low: str, clauses, req_money: set, iban_spans, quoted) -> List[AmountMention]:
    """v1 amount extraction with the month-word and date repairs."""
    out = []
    date_spans = [(m.start(), m.end()) for m in _DATE_TOKEN.finditer(g)]
    for m in _NUM.finditer(g):
        s, e = m.start(), m.end()
        if any(a <= s < b or a < e <= b for a, b in iban_spans) or any(a <= s and e <= b for a, b, _ in quoted):
            continue
        if any(a <= s < b for a, b in date_spans):
            continue
        tok = m.group(0).strip()
        ctx_b, ctx_a = low[max(0, s - 24):s], low[e:e + 28]
        if re.search(_MONTH_WORD + r"\s*,?\s*$", ctx_b) or re.fullmatch(r"(19|20)\d\d", tok) and re.search(r"\b(in|of|during|since)\s*$|" + _MONTH_WORD + r"\s*$", ctx_b):
            continue
        if re.match(r"\s*(most\s+recent|recent|latest|last\s+\d|transactions?\b|items?\b|days?\b|weeks?\b|months?\b|years?\b|times?\b|st\b|nd\b|rd\b|th\b)", ctx_a):
            continue
        if re.match(r"\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr|Boulevard|Blvd|Way|Square)\b", g[e:e + 40]) \
                or re.search(r"\b[A-Z]{2}\s*$", g[max(0, s - 4):s]) and re.fullmatch(r"\d{5}", tok):
            continue
        val, amb = parse_amount(tok)
        if val is None and not amb:
            continue
        ci = _clause_of(clauses, s)
        cl = clauses[ci][1]
        if _DERIVED.search(cl):
            role = "base"
        elif ci not in req_money and _PAST.search(cl) and not re.search(r"\b(is|are|will\s+be|should\s+be)\b[^.;]{0,12}$", cl[:s - clauses[ci][0]]):
            role = "historical"
        else:
            role = "value"
        out.append(AmountMention(val, amb, role, Span(s, e, tok)))
    return out


def compile_intent_v2(objective: str) -> IntentV2:
    base = V1.compile_intent(objective)
    g = clean(objective)
    low = g.lower()
    clauses = _clauses(g)
    ops = dict(base.ops)
    spans = list(base.op_spans)
    conditional = set(base.conditional)
    # repair: standing-order request cue
    req_ci = {c: set() for c in CATEGORIES}
    for cat, sp in base.op_spans:
        if base.op(cat) == "requested":
            req_ci[cat].add(_clause_of(clauses, sp.start))
    for ci, (off, cl) in enumerate(clauses):
        for pat in _EXTRA_REQ:
            for m in re.finditer(pat, cl, flags=re.I):
                if ops["value_transfer"] != "prohibited":
                    ops["value_transfer"] = "requested"
                    spans.append(("value_transfer", Span(off + m.start(), off + m.end(), cl[m.start():m.end()])))
                    req_ci["value_transfer"].add(ci)
                    if _COND_WORD.search(cl):
                        conditional.add("value_transfer")
    req_ci = {c: v for c, v in req_ci.items() if ops[c] == "requested"}
    req_money = req_ci.get("value_transfer", set()) | req_ci.get("payment_modification", set())
    iban_spans = [(i.span.start, i.span.end) for i in base.ibans]
    quoted = [(m.start(1), m.end(1), m.group(1)) for m in V1._QUOTED.finditer(g)]
    amounts = _amounts_v2(g, low, clauses, req_money, iban_spans, quoted)
    # repair: ISO dates were read as amounts (and as roles of identifiers) only in amounts; ibans unchanged
    base2 = dataclasses.replace(base, ops=tuple(ops.items()), op_spans=tuple(spans), conditional=frozenset(conditional),
                                amounts=tuple(amounts))
    # ---------------------------------------------------------------- instructions
    money_cats = [c for c in ("value_transfer", "payment_modification") if c in req_ci]
    instrs: List[Instruction] = []
    pending_amounts, pending_targets = [], []
    for ci, (off, cl) in enumerate(clauses):
        in_req = ci in req_money
        tgt = [i for i in base.ibans if _clause_of(clauses, i.span.start) == ci and i.role == "target"]
        amt = [a for a in amounts if _clause_of(clauses, a.span.start) == ci and a.role == "value"]
        if not (in_req or tgt):
            continue
        cats = [c for c in money_cats if ci in req_ci[c]] or money_cats
        if not cats:
            continue
        cond = _parse_condition(cl)
        rep = _repeat(cl)
        toks = sorted([(i.span.start, "I", i) for i in tgt] + [(a.span.start, "A", a) for a in amt], key=lambda t: t[0])
        used, pairs = set(), []
        for k, (pos, kind, obj) in enumerate(toks):         # "<amount> to <account>"
            if kind == "A" and k + 1 < len(toks) and toks[k + 1][1] == "I" and k not in used and k + 1 not in used:
                pairs.append((toks[k + 1][2], obj))
                used |= {k, k + 1}
        for k, (pos, kind, obj) in enumerate(toks):         # "<account> ... <amount>" (declarations: "account is X and rent is 2200")
            if kind == "I" and k + 1 < len(toks) and toks[k + 1][1] == "A" and k not in used and k + 1 not in used \
                    and not (k + 2 < len(toks) and toks[k + 2][1] == "I"):
                pairs.append((obj, toks[k + 1][2]))
                used |= {k, k + 1}
        rest_i = [toks[k][2] for k in range(len(toks)) if k not in used and toks[k][1] == "I"]
        rest_a = [toks[k][2] for k in range(len(toks)) if k not in used and toks[k][1] == "A"]
        if len(rest_i) == 1 and len(rest_a) == 1:
            pairs.append((rest_i[0], rest_a[0]))
            rest_i, rest_a = [], []
        for c in cats:
            for i, a in pairs:
                instrs.append(Instruction(c, i.canonical, a.value, a.ambiguous, cond, rep, ci, Span(off, off + len(cl), cl)))
        if in_req:
            pending_targets += [(i, cats, cond, rep, ci, off, cl) for i in rest_i]
            pending_amounts += [(a, cats, cond, rep, ci, off, cl) for a in rest_a]
            if not pairs and not rest_i and not rest_a:          # a request without a stated account or amount
                for c in cats:
                    instrs.append(Instruction(c, None, None, False, cond, rep, ci, Span(off, off + len(cl), cl)))
        else:
            pending_targets += [(i, cats, cond, rep, ci, off, cl) for i in rest_i]
    # an amount in a request clause and a declared account elsewhere ("Reimburse Marta 36.40 ... Her IBAN is X")
    if len(pending_targets) == 1 and len(pending_amounts) == 1:
        (i, cats, _c1, _r1, _ci1, _o1, _l1), (a, cats2, cond, rep, ci, off, cl) = pending_targets[0], pending_amounts[0]
        for c in cats2:
            instrs.append(Instruction(c, i.canonical, a.value, a.ambiguous, cond, rep, ci, Span(off, off + len(cl), cl)))
    else:
        for i, cats, cond, rep, ci, off, cl in pending_targets:
            for c in cats:
                instrs.append(Instruction(c, i.canonical, None, False, cond, rep, ci, Span(off, off + len(cl), cl)))
        for a, cats, cond, rep, ci, off, cl in pending_amounts:
            for c in cats:
                instrs.append(Instruction(c, None, a.value, a.ambiguous, cond, rep, ci, Span(off, off + len(cl), cl)))
    for c in ("credential_change", "profile_change"):
        for ci in sorted(req_ci.get(c, ())):
            off, cl = clauses[ci]
            instrs.append(Instruction(c, None, None, False, _parse_condition(cl), 1, ci, Span(off, off + len(cl), cl)))
    return IntentV2(base2, tuple(instrs))
