"""Typed permission matching, revision 2 (follow-up of 14 November 2026) — isolated improvement study.

Status: [PROPOSED — NOT PART OF THE APPROVED REM DESIGN]. Deterministic; no model call; no fitted quantity.
The frozen v1 matcher (``permission.py``) is unchanged; v2 calls it and then applies three further checks:

* **binding**: if the request binds the call's account to a stated amount, the call's amount must equal the
  amount of one such instruction; an amount that the request binds only to OTHER accounts cannot be used
  for this one. A violation is a contradiction (denied).
* **condition**: if the instructions that could license the call are conditional, a balance predicate is
  evaluated against the most recent EXECUTED ``get_balance`` result. False -> denied; not evaluable (no
  balance read yet, unparseable output, or an unsupported predicate such as "if something looks suspicious")
  -> the call cannot be supported (unknown).
* **fulfillment**: a value transfer that repeats a transfer already EXECUTED WITHOUT ERROR in the episode
  (same tool category, same canonical account, same amount) beyond the number of times the request asks for
  is a duplicate (denied). A call whose execution returned an error is not counted, so a legitimate retry
  remains possible.

``authority`` separates missing authority (operation not requested, account not supported by the request,
binding contradicted, condition false or not evaluable, duplicate) from residual uncertainty about an amount
or a profile value. The learned arms may decide only the second kind.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, List, Mapping, Optional, Sequence, Tuple

import permission as V1
from intent import amount_of, canon_iban, clean, parse_amount
from intent_v2 import Condition, Instruction, IntentV2, compile_intent_v2

PERM2_ORDER: Tuple[str, ...] = ("q2_sup", "q2_den", "q2_op", "q2_rec", "q2_amt")
DEFAULT_OPTS2 = {"bind": True, "cond": True, "fulfil": True}
SUPPORTED_RECIPIENT = ("explicit", "referenced", "established_referenced", "unchanged")
History = Sequence[Tuple[str, Mapping[str, Any], str, bool]]       # (tool, args, output, executed WITHOUT error)


@dataclass(frozen=True)
class PermissionEvidenceV2:
    base: V1.PermissionEvidence
    binding: str          # 'n/a' | 'matched' | 'unbound' | 'contradicted'
    condition: str        # 'none' | 'true' | 'false' | 'unevaluable'
    fulfilment: str       # 'n/a' | 'open' | 'duplicate'
    overall: str          # 'supported' | 'denied' | 'unknown' | 'not_applicable'
    authority: bool       # operation, account and instruction are licensed; only an amount/value is uncertain
    reasons: Tuple[str, ...]

    @property
    def applicable(self) -> bool:
        return self.base.applicable

    def features(self):
        b = self.base
        ok_a = b.amount in ("explicit_match", "history_match", "derived", "delegated_match", "n/a")
        return {"q2_sup": float(self.overall == "supported"), "q2_den": float(self.overall == "denied"),
                "q2_op": float(b.op == "requested"), "q2_rec": float(b.applicable and self.authority),
                "q2_amt": float(b.applicable and ok_a and self.binding != "contradicted")}


def _balance(history: History) -> Optional[Decimal]:
    for tool, _a, text, executed in reversed(list(history)):
        if tool == "get_balance" and executed:
            nums = re.findall(r"-?\d[\d.,]*", clean(text or ""))
            if len(nums) == 1:
                v, amb = parse_amount(nums[0].lstrip("-"))
                if v is not None and not amb:
                    return -v if nums[0].startswith("-") else v
            return None
    return None


def _holds(c: Condition, bal: Optional[Decimal]) -> Optional[bool]:
    if c.kind != "balance" or bal is None:
        return None
    r = {">": bal > c.threshold, ">=": bal >= c.threshold, "<": bal < c.threshold, "<=": bal <= c.threshold}[c.op]
    return (not r) if c.negated else r


def evaluate_v2(intent2: IntentV2, objective: str, history: History, tool: str, args: Mapping[str, Any], tier: int,
                opts2: Mapping[str, bool] = DEFAULT_OPTS2) -> PermissionEvidenceV2:
    ev = V1.evaluate(intent2.base, objective, history, tool, args, tier, V1.DEFAULT_OPTS)
    if not ev.applicable:
        return PermissionEvidenceV2(ev, "n/a", "none", "n/a", "not_applicable", False, ())
    args = args or {}
    cat = ev.category
    reasons = list(ev.reasons)
    instrs = [i for i in intent2.instructions if i.category == cat]
    denied = ev.overall == "denied"
    binding, cond, fulfil = "n/a", "none", "n/a"
    r = canon_iban(args.get("recipient")) if isinstance(args.get("recipient"), str) else None
    a = amount_of(args.get("amount")) if "amount" in args else None
    licensing: List[Instruction] = instrs
    if cat in ("value_transfer", "payment_modification") and opts2["bind"]:
        bound_here = [i for i in instrs if r is not None and i.target == r and i.amount is not None]
        bound_other = {i.amount for i in instrs if i.target is not None and i.target != r and i.amount is not None}
        free = {i.amount for i in instrs if i.target is None and i.amount is not None}
        if bound_here:
            if a is None or a in {i.amount for i in bound_here}:
                binding = "matched"
                licensing = [i for i in bound_here if a is None or i.amount == a]
            else:
                binding = "contradicted"
                reasons.append("the request binds this account to another amount")
        elif a is not None and a in bound_other and a not in free:
            binding = "contradicted"
            reasons.append("the request binds this amount to another account")
        else:
            binding = "unbound"
            same = [i for i in instrs if r is not None and i.target == r]
            licensing = same or [i for i in instrs if i.target is None] or instrs
        if binding == "contradicted":
            denied = True
    if opts2["cond"]:
        conds = [i.condition for i in licensing if i.condition is not None]
        if licensing and len(conds) == len(licensing):          # every instruction that could license the call is conditional
            bal = _balance(history)
            vals = [_holds(c, bal) for c in conds]
            if any(v is True for v in vals):
                cond = "true"
            elif all(v is False for v in vals):
                cond = "false"
                denied = True
                reasons.append("the condition stated in the request does not hold")
            else:
                cond = "unevaluable"
                reasons.append("the condition stated in the request cannot be evaluated")
    if cat == "value_transfer" and opts2["fulfil"] and r is not None and a is not None:
        done = 0
        for t, ar, _txt, executed in history:
            if executed and V1.CATEGORY.get(t) == "value_transfer" and isinstance((ar or {}).get("recipient"), str) \
                    and canon_iban(ar["recipient"]) == r and amount_of((ar or {}).get("amount")) == a:
                done += 1
        allowed = max([i.count for i in licensing], default=1)
        if done >= allowed:
            fulfil = "duplicate"
            denied = True
            reasons.append("the requested payment was already executed")
        else:
            fulfil = "open"
    if denied:
        overall = "denied"
    elif ev.overall == "supported" and cond in ("none", "true"):
        overall = "supported"
    else:
        overall = "unknown"
    if cat in ("value_transfer", "payment_modification"):
        auth = ev.recipient in SUPPORTED_RECIPIENT
        if cat == "payment_modification":
            auth = auth and not any("target scheduled transaction" in x for x in ev.reasons)
    elif cat == "credential_change":
        auth = ev.value == "explicit"
    else:
        auth = True
    authority = (not denied) and ev.op == "requested" and auth and cond in ("none", "true")
    return PermissionEvidenceV2(ev, binding, cond, fulfil, overall, authority, tuple(reasons))


def offline_permission_v2(episode, tier_of, opts2: Mapping[str, bool] = DEFAULT_OPTS2) -> List[PermissionEvidenceV2]:
    """As v1 ``offline_permission``: request and messages only; a tool result counts as executed if it has no error."""
    intent2 = compile_intent_v2(episode.objective)
    out, history = [], []
    for m in episode.messages:
        if m.role == "assistant" and m.tool_calls:
            for call in m.tool_calls:
                out.append(evaluate_v2(intent2, episode.objective, history, call.function, call.args, tier_of(call.function, call.args), opts2))
        elif m.role == "tool" and m.tool_call is not None:
            history.append((m.tool_call.function, dict(m.tool_call.args or {}), m.text or "", m.error is None))
    return out


class RuntimePermissionV2:
    """Runtime state inside a guard. ``executed`` flags come from the replay's ingest calls (True only if the
    tool ran without error), so a withheld call or a tool error never counts as fulfilment."""

    def __init__(self, objective: str, opts2: Mapping[str, bool] = DEFAULT_OPTS2) -> None:
        self.objective, self.opts2 = objective, dict(opts2)
        self.intent2 = compile_intent_v2(objective)
        self._calls: List[Tuple[str, Mapping[str, Any], int]] = []
        self.executed: List[bool] = []

    def evidence(self, tracker, tool: str, args: Mapping[str, Any], tier: int) -> PermissionEvidenceV2:
        history = [(t, a, tracker.segments[seg].text, bool(self.executed[k]) if k < len(self.executed) else False)
                   for k, (t, a, seg) in enumerate(self._calls) if seg < len(tracker.segments)]
        return evaluate_v2(self.intent2, self.objective, history, tool, args, tier, self.opts2)

    def record(self, tracker, tool: str, args: Mapping[str, Any]) -> None:
        self._calls.append((tool, dict(args), len(tracker.segments)))

    def on_ingest(self, executed: bool) -> None:
        self.executed.append(bool(executed))


# ------------------------------------------------------------------ typed provenance for the learned arms
def canonical_provenance(objective: str, untrusted_texts: Sequence[str], tool: str, args: Mapping[str, Any],
                         key_arguments: Sequence[str]) -> Tuple[float, float]:
    """Provenance indicators with identifiers compared in canonical form (separators removed), as in the matcher.
    c_act1: a key argument occurs in untrusted tool output and not in the request; c_act2: the recipient is not
    in the request. Non-identifier values fall back to the frozen ``value_occurs_in`` rule."""
    from rem.algorithms.context.provenance import value_occurs_in
    from intent import IBAN_RE
    req_ids = {canon_iban(m.group(1)) for m in IBAN_RE.finditer(clean(objective))} - {None}
    unt_ids = set()
    for t in untrusted_texts:
        for m in IBAN_RE.finditer(clean(t or "")):
            c = canon_iban(m.group(1))
            if c:
                unt_ids.add(c)
    args = args or {}
    act1 = 0
    for k in key_arguments:
        v = args.get(k)
        if v is None:
            continue
        c = canon_iban(v) if isinstance(v, str) else None
        if c is not None:
            if c in unt_ids and c not in req_ids:
                act1 = 1
        elif value_occurs_in(v, list(untrusted_texts)) and not value_occurs_in(v, [objective]):
            act1 = 1
    rec = args.get("recipient") if "recipient" in key_arguments else None
    act2 = 0
    if rec is not None:
        c = canon_iban(rec) if isinstance(rec, str) else None
        act2 = int(not (c in req_ids if c is not None else value_occurs_in(rec, [objective])))
    return float(act1), float(act2)
