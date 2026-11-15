"""Typed permission matching, revision 3 (15 November 2026) — isolated improvement study.

Status: [PROPOSED — NOT PART OF THE APPROVED REM DESIGN]. Deterministic; no model call; no fitted quantity.
Revisions 1 and 2 are unchanged. Revision 3 keeps their checks and changes two things:

* **effect**: a call is matched only against the instructions that license ITS effect (send_money: an immediate
  transfer; schedule_transaction: creation of a standing order or scheduled payment; update_scheduled_transaction:
  modification of one). If the request has money instructions and none licenses this effect, the call is denied.
  An account or an amount that the request binds only to an instruction of ANOTHER effect cannot be used for this
  one (denied): "update the standing order to account X and 2200" does not license sending 2200, or anything
  else, to X.
* **condition**: the whole predicate expression of the licensing instruction is evaluated (``intent_v3``);
  an expression that is not completely supported is not evaluable, and the call stays unknown.

Policy for conditions that cannot be evaluated (including every subjective one): the status is *unknown*. The
rule arms withhold unknown calls; in a deployment with a reviewer such a call would be escalated. It is never
treated as satisfied.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, List, Mapping, Optional, Sequence, Tuple

import permission as V1
from intent import amount_of, canon_iban
from intent_v3 import TOOL_EFFECT, ConditionV3, InstructionV3, IntentV3, compile_intent_v3
from permission_v2 import SUPPORTED_RECIPIENT, _balance

PERM3_ORDER: Tuple[str, ...] = ("q3_sup", "q3_den", "q3_op", "q3_rec", "q3_amt")
DEFAULT_OPTS3 = {"effect": True, "bind": True, "cond": True, "fulfil": True}
MONEY = ("value_transfer", "payment_modification")
History = Sequence[Tuple[str, Mapping[str, Any], str, bool]]


@dataclass(frozen=True)
class PermissionEvidenceV3:
    base: V1.PermissionEvidence
    effect: str           # 'n/a' | 'matched' | 'not_requested' | 'other_operation'
    binding: str          # 'n/a' | 'matched' | 'unbound' | 'contradicted'
    condition: str        # 'none' | 'true' | 'false' | 'unevaluable'
    fulfilment: str       # 'n/a' | 'open' | 'duplicate'
    overall: str
    authority: bool
    reasons: Tuple[str, ...]

    @property
    def applicable(self) -> bool:
        return self.base.applicable

    def features(self):
        b = self.base
        ok_a = b.amount in ("explicit_match", "history_match", "derived", "delegated_match", "n/a")
        return {"q3_sup": float(self.overall == "supported"), "q3_den": float(self.overall == "denied"),
                "q3_op": float(b.op == "requested" and self.effect in ("matched", "n/a")), "q3_rec": float(b.applicable and self.authority),
                "q3_amt": float(b.applicable and ok_a and self.binding != "contradicted")}


def holds(c: ConditionV3, bal: Optional[Decimal]) -> Optional[bool]:
    """True/False if the whole expression can be evaluated, None otherwise."""
    if c.kind != "balance_expr" or bal is None or not c.parts:
        return None
    vals = [{">": bal > t, ">=": bal >= t, "<": bal < t, "<=": bal <= t}[op] for op, t in c.parts]
    r = all(vals) if c.mode == "all" else any(vals)
    return (not r) if c.negated else r


def evaluate_v3(intent3: IntentV3, objective: str, history: History, tool: str, args: Mapping[str, Any], tier: int,
                opts3: Mapping[str, bool] = DEFAULT_OPTS3) -> PermissionEvidenceV3:
    ev = V1.evaluate(intent3.base, objective, history, tool, args, tier, V1.DEFAULT_OPTS)
    if not ev.applicable:
        return PermissionEvidenceV3(ev, "n/a", "none", "none", "n/a", "not_applicable", False, ())
    args = args or {}
    cat = ev.category
    eff = TOOL_EFFECT.get(tool)
    reasons = list(ev.reasons)
    denied = ev.overall == "denied"
    effect, binding, cond, fulfil = "n/a", "n/a", "none", "n/a"
    r = canon_iban(args.get("recipient")) if isinstance(args.get("recipient"), str) else None
    a = amount_of(args.get("amount")) if "amount" in args else None
    same_cat = [i for i in intent3.instructions if i.category == cat]
    licensing: List[InstructionV3] = same_cat
    others: List[InstructionV3] = []
    if eff is not None:
        money = [i for i in intent3.instructions if i.category in MONEY]
        if opts3["effect"]:
            mine = [i for i in money if eff in i.effects]
            others = [i for i in money if eff not in i.effects]
            if money and not mine:
                effect, denied = "not_requested", True
                reasons.append("the request asks for another kind of payment operation")
            else:
                effect = "matched" if mine else "n/a"
                if r is not None and any(i.target == r for i in others) and not any(i.target == r for i in mine):
                    effect, denied = "other_operation", True
                    reasons.append("the request names this account for another operation")
            licensing = mine
        else:
            licensing = same_cat
        if opts3["bind"] and not (effect in ("not_requested", "other_operation")):
            bound_here = [i for i in licensing if r is not None and i.target == r and i.amount is not None]
            bound_other = {i.amount for i in licensing if i.target is not None and i.target != r and i.amount is not None}
            bound_other |= {i.amount for i in others if i.target is not None and i.amount is not None}
            free = {i.amount for i in licensing if i.target is None and i.amount is not None}
            if bound_here:
                if a is None or a in {i.amount for i in bound_here}:
                    binding = "matched"
                    licensing = [i for i in bound_here if a is None or i.amount == a]
                else:
                    binding = "contradicted"
                    reasons.append("the request binds this account to another amount")
            elif a is not None and a in bound_other and a not in free:
                binding = "contradicted"
                reasons.append("the request binds this amount to another account or operation")
            else:
                binding = "unbound"
                same = [i for i in licensing if r is not None and i.target == r]
                licensing = same or [i for i in licensing if i.target is None] or licensing
            if binding == "contradicted":
                denied = True
    if opts3["cond"]:
        conds = [i.condition for i in licensing if i.condition is not None]
        if licensing and len(conds) == len(licensing):
            bal = _balance(history)
            vals = [holds(c, bal) for c in conds]
            if any(v is True for v in vals):
                cond = "true"
            elif all(v is False for v in vals):
                cond, denied = "false", True
                reasons.append("the condition stated in the request does not hold")
            else:
                cond = "unevaluable"
                reasons.append("the condition stated in the request cannot be evaluated completely")
    if eff in ("transfer_now", "schedule_create") and opts3["fulfil"] and r is not None and a is not None:
        done = 0
        for t, ar, _txt, executed in history:
            same_effect = (TOOL_EFFECT.get(t) == eff) if opts3["effect"] else (V1.CATEGORY.get(t) == "value_transfer")
            if executed and same_effect and isinstance((ar or {}).get("recipient"), str) \
                    and canon_iban(ar["recipient"]) == r and amount_of((ar or {}).get("amount")) == a:
                done += 1
        allowed = max([i.count for i in licensing], default=1)
        if done >= allowed:
            fulfil, denied = "duplicate", True
            reasons.append("the requested payment was already executed")
        else:
            fulfil = "open"
    if denied:
        overall = "denied"
    elif ev.overall == "supported" and cond in ("none", "true"):
        overall = "supported"
    else:
        overall = "unknown"
    if cat in MONEY:
        auth = ev.recipient in SUPPORTED_RECIPIENT
        if cat == "payment_modification":
            auth = auth and not any("target scheduled transaction" in x for x in ev.reasons)
    elif cat == "credential_change":
        auth = ev.value == "explicit"
    else:
        auth = True
    authority = (not denied) and ev.op == "requested" and auth and cond in ("none", "true")
    return PermissionEvidenceV3(ev, effect, binding, cond, fulfil, overall, authority, tuple(reasons))


def offline_permission_v3(episode, tier_of, opts3: Mapping[str, bool] = DEFAULT_OPTS3) -> List[PermissionEvidenceV3]:
    """Request and messages only; a tool result counts as executed if it has no error."""
    intent3 = compile_intent_v3(episode.objective)
    out, history = [], []
    for m in episode.messages:
        if m.role == "assistant" and m.tool_calls:
            for call in m.tool_calls:
                out.append(evaluate_v3(intent3, episode.objective, history, call.function, call.args, tier_of(call.function, call.args), opts3))
        elif m.role == "tool" and m.tool_call is not None:
            history.append((m.tool_call.function, dict(m.tool_call.args or {}), m.text or "", m.error is None))
    return out


class RuntimePermissionV3:
    """Runtime state inside a guard; execution flags come from the replay's ingest calls (True only without error)."""

    def __init__(self, objective: str, opts3: Mapping[str, bool] = DEFAULT_OPTS3) -> None:
        self.objective, self.opts3 = objective, dict(opts3)
        self.intent3 = compile_intent_v3(objective)
        self._calls: List[Tuple[str, Mapping[str, Any], int]] = []
        self.executed: List[bool] = []

    def evidence(self, tracker, tool: str, args: Mapping[str, Any], tier: int) -> PermissionEvidenceV3:
        history = [(t, a, tracker.segments[seg].text, bool(self.executed[k]) if k < len(self.executed) else False)
                   for k, (t, a, seg) in enumerate(self._calls) if seg < len(tracker.segments)]
        return evaluate_v3(self.intent3, self.objective, history, tool, args, tier, self.opts3)

    def record(self, tracker, tool: str, args: Mapping[str, Any]) -> None:
        self._calls.append((tool, dict(args), len(tracker.segments)))

    def on_ingest(self, executed: bool) -> None:
        self.executed.append(bool(executed))
