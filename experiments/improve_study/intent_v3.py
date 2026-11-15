"""Task-permission compiler, revision 3 (15 November 2026) — isolated improvement study.

Status: [PROPOSED — NOT PART OF THE APPROVED REM DESIGN]. Deterministic; no model call; no fitted quantity.
The scored revisions 1 and 2 (``intent.py``, ``intent_v2.py``) are unchanged.

Revision 3 repairs two defects of revision 2 found by an external review of 15 November 2026:

* **Effect of the operation.** Revision 2 put an immediate transfer and the creation of a standing order in one
  category, so a request to create a monthly standing order licensed an immediate ``send_money``. Each
  instruction now carries the EFFECTS it licenses: ``transfer_now`` (send_money), ``schedule_create``
  (schedule_transaction) or ``schedule_modify`` (update_scheduled_transaction).
* **Whole condition.** Revision 2 evaluated the first balance comparison it recognized and ignored the rest
  ("above 1000 and below 5000" held at 10000). A condition is now a predicate EXPRESSION that must be parsed
  completely; anything not parsed completely is ``unsupported`` and is never treated as satisfied. Numbers that
  belong to a condition are thresholds and are no longer read as payment amounts.

SUPPORTED SYNTAX (everything else is handled conservatively, as stated):

  effect      transfer_now     a request verb: pay, send, transfer, refund, wire, remit, reimburse, repay,
                               "make a payment/transfer"
              schedule_create  one of those verbs or create/set up/start/open/add/arrange together with a
                               recurrence cue (standing order, recurring, scheduled, monthly, weekly, every/each
                               month|week|year), or the verb "schedule"
              schedule_modify  update/adjust/change/modify/amend/increase/decrease/raise/lower ... rent, payment,
                               standing order, scheduled, recurring, subscription
              ambiguous        "set up/arrange a payment" without a recurrence cue, or a transfer verb with an
                               explicit calendar date: both transfer_now and schedule_create are licensed
  declaration a sentence that only declares an account or amount ("The recipient is X", "My landlord's account is
              X and rent is 2200") takes the effects of the nearest preceding request sentence that has a money
              effect, otherwise of the nearest following one
  condition   introduced by if / unless / only if / provided that / in case / as long as; a leading condition
              must end at a comma or "then"; the expression is balance comparisons joined by "and" (or "but")
              or by "or" (not mixed): "[my] balance [is] <above|over|more than|greater than|higher than|exceeds|
              at least|below|under|less than|lower than|at most|not less than|not more than> N",
              "[my] balance is between N and M" (inclusive), and elliptic continuations ("... and below M")
              any other condition, including every subjective one, is ``unsupported``
"""
from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import FrozenSet, List, Optional, Tuple

import intent as V1
import intent_v2 as V2
from intent import Intent, Span, _clause_of, _clauses, _is_request, clean, parse_amount

EFFECTS = ("transfer_now", "schedule_create", "schedule_modify")
TOOL_EFFECT = {"send_money": "transfer_now", "schedule_transaction": "schedule_create", "update_scheduled_transaction": "schedule_modify"}
COMPAT = {"value_transfer": frozenset({"transfer_now", "schedule_create"}), "payment_modification": frozenset({"schedule_modify"})}

_NOW = [r"\b(pay|send|transfer|refund|wire|remit|reimburse|repay)\b", r"\bmake\s+(?:a|the|this|that|another|one|my)\s+(?:\w+\s+)?(payment|transfer)\b"]
_SETUP = r"\b(create|set\s+up|start|open|add|arrange)\b[^.;]*\b(transactions?|payments?|transfers?|standing\s+orders?)\b"
_SCHEDULE_VERB = r"\bschedule\b[^.;]*\b(transactions?|payments?|transfers?)\b"
_RECUR = re.compile(r"\b(standing\s+orders?|recurring|scheduled|monthly|weekly|every\s+(?:month|week|year)|each\s+(?:month|week|year)|per\s+month)\b", re.I)
_MODIFY = V1._REQ["payment_modification"]

_COND_WORD = re.compile(r"\b(only\s+if|if|unless|provided\s+that|in\s+case|as\s+long\s+as)\b", re.I)
_OPS = (r"not\s+less\s+than|not\s+more\s+than|above|over|more\s+than|greater\s+than|higher\s+than|exceeds|at\s+least|below|under|less\s+than|"
        r"lower\s+than|at\s+most")
_N = r"[$€£]?\s?(\d[\d.,]*\d|\d)"
_SUBJ = r"(?:my\s+|the\s+)?(?:current\s+|account\s+)?balance\s+(?:is\s+|stays\s+|remains\s+)?"
_FULL_BETWEEN = re.compile(_SUBJ + r"between\s+" + _N + r"\s+and\s+" + _N, re.I)
_FULL = re.compile(_SUBJ + r"(" + _OPS + r")\s+" + _N, re.I)
_ELLIPTIC = re.compile(r"(?:it\s+)?(?:is\s+)?(" + _OPS + r")\s+" + _N, re.I)
_CONJ = re.compile(r"\s*,?\s*(and|but|or)\s+", re.I)
_CMP = dict(V2._CMP)


@dataclass(frozen=True)
class ConditionV3:
    kind: str                                   # 'balance_expr' | 'unsupported'
    parts: Tuple[Tuple[str, Decimal], ...] = () # (comparison, threshold)
    mode: str = "all"                           # 'all' (and) | 'any' (or)
    negated: bool = False                       # 'unless'
    text: str = ""


@dataclass(frozen=True)
class InstructionV3:
    category: str
    effects: FrozenSet[str]                     # money effects licensed (empty for credential and profile changes)
    target: Optional[str]
    amount: Optional[Decimal]
    amount_ambiguous: bool
    condition: Optional[ConditionV3]
    count: int
    clause: int
    span: Span


@dataclass(frozen=True)
class IntentV3:
    base: Intent
    instructions: Tuple[InstructionV3, ...]


def _condition_segment(clause: str) -> Optional[Tuple[int, int, str]]:
    """(start, end, condition word) of the condition expression inside a clause, or None."""
    m = _COND_WORD.search(clause)
    if not m:
        return None
    # Amendment 1 (15 November 2026, after scoring): a condition is LEADING when no request cue precedes it, so that an
    # introductory phrase ("After that, if ...") no longer makes it a trailing condition that runs to the end of the sentence.
    prefix = clause[:m.start()]
    leading = not any(re.search(pat, prefix, flags=re.I) for pats in V1._REQ.values() for pat in pats) and not re.search(_SETUP, prefix, flags=re.I)
    if leading:
        end = None
        c = re.search(r",\s|\s+then\s", clause[m.end():])
        if c:
            end = m.end() + c.start()
        return (m.end(), end if end is not None else len(clause), m.group(1).lower())
    return (m.end(), len(clause), m.group(1).lower())           # trailing condition: runs to the end of the sentence


def parse_condition_v3(clause: str) -> Optional[ConditionV3]:
    seg = _condition_segment(clause)
    if seg is None:
        return None
    s, e, word = seg
    neg = word == "unless"
    text = clause[s:e].strip().rstrip(".!?").strip()
    bad = ConditionV3("unsupported", negated=neg, text=clause[max(0, s - len(word) - 1):].strip()[:160])
    rest = clause[e:]
    if re.match(r"\s*,?\s*(and|or|but|as\s+well\s+as)\b", rest, re.I) or _COND_WORD.search(rest):
        return bad                                             # the condition continues after the comma, or a second condition follows
    if len(_COND_WORD.findall(clause)) > 1:
        return bad
    pos, parts, conjs = 0, [], set()
    while True:
        m = _FULL_BETWEEN.match(text, pos)
        if m:
            lo, a1 = parse_amount(m.group(1))
            hi, a2 = parse_amount(m.group(2))
            if lo is None or hi is None or a1 or a2:
                return bad
            parts += [(">=", lo), ("<=", hi)]
            conjs.add("and")
        else:
            m = _FULL.match(text, pos) or (_ELLIPTIC.match(text, pos) if parts else None)
            if not m:
                return bad
            val, amb = parse_amount(m.group(2))
            if val is None or amb:
                return bad
            parts.append((_CMP[re.sub(r"\s+", " ", m.group(1).lower())], val))
        pos = m.end()
        if pos >= len(text):
            break
        c = _CONJ.match(text, pos)
        if not c:
            return bad                                         # residue that is not part of a supported expression
        conjs.add("or" if c.group(1).lower() == "or" else "and")
        pos = c.end()
    if conjs == {"and", "or"}:
        return bad                                             # mixed connectives need precedence rules: not supported
    return ConditionV3("balance_expr", tuple(parts), "any" if conjs == {"or"} else "all", neg, clause[max(0, s - len(word) - 1):e].strip())


def _mask_thresholds(text: str) -> str:
    """Replace the digits of condition expressions by 'x' (same length), so that thresholds are not read as amounts."""
    out = list(text)
    keep = [(m.start(1), m.end(1)) for m in V1._QUOTED.finditer(text)] + [(m.start(1), m.end(1)) for m in V1.IBAN_RE.finditer(text)]
    for off, cl in _clauses(text):
        seg = _condition_segment(cl)
        if seg is None:
            continue
        s, e, _w = seg
        for k in range(off + s, off + e):
            if out[k].isdigit() and not any(a <= k < b for a, b in keep):     # Amendment 1: quoted values and identifiers are never masked
                out[k] = "x"
    return "".join(out)


def _clause_effects(cl: str) -> FrozenSet[str]:
    eff = set()
    req = lambda pat: any(_is_request(cl, m) for m in re.finditer(pat, cl, flags=re.I))
    if any(req(p) for p in _MODIFY):
        eff.add("schedule_modify")
    now = any(req(p) for p in _NOW)
    setup, sched, recur = req(_SETUP), req(_SCHEDULE_VERB), bool(_RECUR.search(cl))
    modify_only_recur = "schedule_modify" in eff and not (now or setup or sched)
    if sched or ((now or setup) and recur and not modify_only_recur):
        eff.add("schedule_create")
    elif setup:
        eff |= {"transfer_now", "schedule_create"}             # "set up a payment": ambiguous
    elif now:
        eff.add("transfer_now")
        if V2._DATE_TOKEN.search(cl):
            eff.add("schedule_create")                         # a transfer with an explicit calendar date: ambiguous
    return frozenset(eff)


def compile_intent_v3(objective: str) -> IntentV3:
    g = clean(objective)
    i2 = V2.compile_intent_v2(_mask_thresholds(g))             # same offsets; thresholds are not amounts
    clauses = _clauses(g)
    eff = [_clause_effects(cl) for _off, cl in clauses]
    money = [k for k, e in enumerate(eff) if e]

    def effects_of(ci: int, category: str) -> FrozenSet[str]:
        compat = COMPAT.get(category)
        if compat is None:
            return frozenset()
        own = eff[ci] & compat if ci < len(eff) else frozenset()
        if eff[ci] if ci < len(eff) else False:
            return own
        prev = [k for k in money if k < ci]
        nxt = [k for k in money if k > ci]
        src = prev[-1] if prev else (nxt[0] if nxt else None)   # a declaration takes the effects of the nearest request
        if src is None:
            return compat                                       # a request cue of revision 1 without a revision-3 cue: ambiguous
        return eff[src] & compat

    out: List[InstructionV3] = []
    for ins in i2.instructions:
        cl = clauses[ins.clause][1] if ins.clause < len(clauses) else ""
        e = effects_of(ins.clause, ins.category)
        if ins.category in COMPAT and not e:
            continue                                            # the request does not give this instruction this kind of effect
        out.append(InstructionV3(ins.category, e, ins.target, ins.amount, ins.amount_ambiguous, parse_condition_v3(cl), ins.count,
                                 ins.clause, ins.span))
    return IntentV3(i2.base, tuple(out))
