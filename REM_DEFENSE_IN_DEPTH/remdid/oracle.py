"""Offline TAE issuers for the AgentDojo banking evaluation. These are EVALUATION ORACLES, not deployable sources.

AgentDojo has no trusted authorization channel (file 25, AS-T1). The modes model what a trusted approval interface
could have produced, so that the authorization control can be studied at all:
  oracle    every sensitive field of every ground-truth state-changing call is SPECIFIED (upper bound: the user
            confirmed exact parameters in a trusted interface)
  explicit  a field is SPECIFIED only if its canonical value occurs in the user's own instruction; otherwise
            UNSPECIFIED -> the call needs confirmation (Escalate). No natural-language intent compilation is used
            (earlier studies found compilation errors released unauthorised calls: REM-B2/B3 NO-GO)
  broad     every field is ANY (wildcard) and uses are unbounded: an over-broad authorization. Used ONLY to model
            the bypass of the authorization control ("attacker acts within an authorized operation")
  none      no entries (authorization unavailable)
The operation set comes from ground truth in every mode (it is what the user asked for).
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .canonical import canonical_amount, canonical_iban, canonical_text, find_amounts, find_ibans
from .provenance import SENSITIVE_FIELDS, canonical_of
from .tae import FieldSpec, FieldState, TAEStore

_GT_CACHE: Dict[str, List[Tuple[str, Dict[str, Any]]]] = {}


def ground_truth_calls(suite, user_task_id: str) -> List[Tuple[str, Dict[str, Any]]]:
    if user_task_id not in _GT_CACHE:
        env = suite.load_and_inject_default_environment({})
        ut = suite.get_user_task_by_id(user_task_id)
        _GT_CACHE[user_task_id] = [(c.function, dict(c.args)) for c in ut.ground_truth(env)
                                   if c.function in SENSITIVE_FIELDS]
    return _GT_CACHE[user_task_id]


def _in_prompt(kind: str, canon: Any, prompt: str) -> bool:
    if kind == "iban":
        return canon in find_ibans(prompt)
    if kind == "amount":
        return any(a == canon for a in find_amounts(prompt))
    if kind == "text":
        return canon in (canonical_text(prompt) or "")
    return False   # ids of stored standing orders are never stated by the user


def build_store(suite, user_task_id: str, prompt: str, mode: str, session_id: str) -> TAEStore:
    store = TAEStore(session_id)
    if mode == "none":
        return store
    for tool, args in ground_truth_calls(suite, user_task_id):
        fields: Dict[str, FieldSpec] = {}
        for f, kind in SENSITIVE_FIELDS[tool]:
            if f not in args:
                continue
            c = canonical_of(kind, args[f])
            if mode == "oracle":
                fields[f] = FieldSpec(FieldState.SPECIFIED, c)
            elif mode == "explicit":
                fields[f] = FieldSpec(FieldState.SPECIFIED, c) if _in_prompt(kind, c, prompt) else FieldSpec(FieldState.UNSPECIFIED)
            elif mode == "broad":
                fields[f] = FieldSpec(FieldState.ANY)
            else:
                raise ValueError(mode)
        if mode == "broad":
            # over-broad: any value for every sensitive field of the operation, unbounded uses
            fields = {f: FieldSpec(FieldState.ANY) for f, _ in SENSITIVE_FIELDS[tool]}
        store.issue(tool, fields, approval_evidence=f"oracle:{mode}:ground_truth", currency="not_applicable",
                    max_uses=10 ** 6 if mode == "broad" else 1)
    return store
