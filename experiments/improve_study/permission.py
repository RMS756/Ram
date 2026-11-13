"""Typed permission matching (candidate component B) — isolated improvement study.

Status: [PROPOSED — NOT PART OF THE APPROVED REM DESIGN]. Deterministic; no model call; no fitted quantity.

A proposed call to a state-changing tool is matched against (i) the compiled intent of the trusted
request (``intent.py``) and (ii) typed provenance of its material arguments:

* trusted request text: identifiers, amounts and quoted values the user wrote;
* STRUCTURED bank records the agent has read (fields ``recipient``, ``sender``, ``amount``, ``id`` of the
  YAML returned by the transaction tools). Only records the user originated count ("established
  payee"). The free-text ``subject`` of a record and the ``sender`` of an incoming transaction are
  counterparty-controlled and are never treated as trusted;
* a source the user NAMED and the agent read: it may supply an amount or a profile value (scoped
  delegation of a data field). It can never supply an operation, a recipient or a credential.

Result: 'supported', 'denied' (contradicted or not requested) or 'unknown'. Every rule is an engineering
design choice of this study. The evidence is fallible; it is not authenticated authorization.
"""
from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, FrozenSet, List, Mapping, Optional, Sequence, Tuple

from intent import Intent, _NUM, amount_of, canon_iban, clean, compile_intent, parse_amount

PERM_ORDER: Tuple[str, ...] = ("q_sup", "q_den", "q_op", "q_rec", "q_amt")
CATEGORY = {"send_money": "value_transfer", "schedule_transaction": "value_transfer",
            "update_scheduled_transaction": "payment_modification", "update_password": "credential_change",
            "update_user_info": "profile_change"}
LEDGER_TOOLS = ("get_most_recent_transactions", "get_scheduled_transactions")
#: every option True = the candidate; each False is one ablation
DEFAULT_OPTS: Mapping[str, bool] = {"op_check": True, "amount_check": True, "established": True, "delegation": True,
                                    "typed_norm": True}
History = Sequence[Tuple[str, Mapping[str, Any], str, bool]]      # (tool, args, output text, executed)


@dataclass
class Ledger:
    """Typed view of the structured bank records read so far (executed reads only)."""
    established: Dict[str, List[str]] = field(default_factory=dict)   # payee -> subjects of user-originated records
    user_amounts: set = field(default_factory=set)
    scheduled_ids: set = field(default_factory=set)
    scheduled_seen: bool = False

    def ingest(self, tool: str, text: str) -> None:
        if tool not in LEDGER_TOOLS:
            return
        try:
            import yaml
            rows = yaml.safe_load(clean(text))
        except Exception:
            return                                            # unparseable output gives no evidence
        if not isinstance(rows, list):
            return
        if tool == "get_scheduled_transactions":
            self.scheduled_seen = True
        for r in rows:
            if not isinstance(r, dict):
                continue
            rec = canon_iban(r.get("recipient")) if isinstance(r.get("recipient"), str) else None
            sender = r.get("sender")
            mine = tool == "get_scheduled_transactions" or (isinstance(sender, str) and sender.strip().lower() == "me")
            if tool == "get_scheduled_transactions" and isinstance(r.get("id"), int):
                self.scheduled_ids.add(r["id"])
            if not mine:
                continue                                      # incoming records establish nothing
            amt = amount_of(r.get("amount"))
            if amt is not None:
                self.user_amounts.add(amt)
            if rec:
                self.established.setdefault(rec, []).append(str(r.get("subject") or ""))

    def referenced(self, payee: str, words: FrozenSet[str]) -> bool:
        for subj in self.established.get(payee, ()):
            if words & set(re.findall(r"[a-z][a-z\-]{3,}", subj.lower())):
                return True
        return False


@dataclass(frozen=True)
class PermissionEvidence:
    applicable: bool
    category: str
    op: str
    recipient: str
    amount: str
    value: str
    overall: str                      # 'supported' | 'denied' | 'unknown' | 'not_applicable'
    hard: bool                        # denied by an explicit contradiction or prohibition (not merely unrequested)
    conditional: bool
    reasons: Tuple[str, ...]

    def features(self) -> Dict[str, float]:
        ok_r = self.recipient in ("explicit", "referenced", "established_referenced", "unchanged", "n/a") and self.value in ("explicit", "delegated_match", "n/a")
        ok_a = self.amount in ("explicit_match", "history_match", "derived", "delegated_match", "n/a")
        return {"q_sup": float(self.overall == "supported"), "q_den": float(self.overall == "denied"),
                "q_op": float(self.op == "requested"), "q_rec": float(self.applicable and ok_r), "q_amt": float(self.applicable and ok_a)}


NA = PermissionEvidence(False, "", "n/a", "n/a", "n/a", "n/a", "not_applicable", False, False, ())


def _text_amounts(text: str) -> set:
    out = set()
    for m in _NUM.finditer(clean(text)):
        v, amb = parse_amount(m.group(0))
        if v is not None and not amb:
            out.add(v)
    return out


def _norm(s: str) -> str:
    return " ".join(str(s).split()).lower()


def named_source_texts(intent: Intent, history: History) -> List[str]:
    names = {os.path.basename(s).lower() for s in intent.sources}
    out = []
    for tool, args, text, executed in history:
        if executed and tool == "read_file" and isinstance((args or {}).get("file_path"), str) \
                and os.path.basename(args["file_path"]).lower() in names:
            out.append(clean(text or ""))
    return out


def build_ledger(history: History) -> Ledger:
    led = Ledger()
    for tool, _args, text, executed in history:
        if executed:
            led.ingest(tool, text or "")
    return led


def evaluate(intent: Intent, objective: str, history: History, tool: str, args: Mapping[str, Any], tier: int,
             opts: Mapping[str, bool] = DEFAULT_OPTS) -> PermissionEvidence:
    cat = CATEGORY.get(tool)
    if cat is None:
        return NA
    args = args or {}
    op = intent.op(cat)
    reasons: List[str] = []
    hard = False
    denied = False
    if opts["op_check"]:
        if op == "prohibited":
            denied, hard = True, True
            reasons.append("operation prohibited by the request")
        elif op == "absent":
            denied = True
            reasons.append("operation not requested")
    led = build_ledger(history)
    srcs = named_source_texts(intent, history) if opts["delegation"] else []
    targets = {i.canonical for i in intent.ibans if i.role == "target"}
    mentioned = {i.canonical for i in intent.ibans if i.role == "mentioned"}
    historical = {i.canonical for i in intent.ibans if i.role == "historical"}
    modes = intent.amount_modes
    g_low = _norm(objective)

    def recip_status(value, allow_established: bool) -> str:
        if value is None:
            return "unchanged"
        if not opts["typed_norm"]:
            from rem.algorithms.context.provenance import value_occurs_in
            return "explicit" if value_occurs_in(value, [objective]) else "untrusted"
        r = canon_iban(value)
        if r is None:
            return "untrusted"
        if r in targets:
            return "explicit"
        if r in mentioned and (not targets or intent.party_reference):
            return "referenced"
        if r in historical and intent.party_reference:
            return "referenced"
        if allow_established and opts["established"] and r in led.established:
            return "established_referenced" if led.referenced(r, intent.content_words) else "established"
        if r in historical or r in mentioned:
            return "historical"
        if targets and not intent.party_reference and not (modes & {"delegated", "history"}):
            return "contradicted"
        return "untrusted"

    def amount_status(value) -> str:
        if value is None:
            return "n/a"
        if not opts["amount_check"]:
            return "n/a"
        a = amount_of(value)
        if a is None:
            return "unverified"
        if not opts["typed_norm"]:
            from rem.algorithms.context.provenance import value_occurs_in
            return "explicit_match" if value_occurs_in(value, [objective]) else ("derived" if "derived" in modes else "unverified")
        vals = {m.value for m in intent.amounts if m.role == "value" and not m.ambiguous}
        amb = any(m.ambiguous for m in intent.amounts if m.role == "value")
        if a in vals:
            return "explicit_match"
        if vals and not modes and not amb:
            return "contradicted"
        if "history" in modes and a in led.user_amounts:
            return "history_match"
        if "delegated" in modes and any(a in _text_amounts(t) for t in srcs):
            return "delegated_match"
        if "derived" in modes:
            return "derived"
        return "unverified"

    rstat, astat, vstat = "n/a", "n/a", "n/a"
    ok = False
    if cat == "value_transfer":
        rstat = recip_status(args.get("recipient"), True)
        if rstat == "unchanged":
            rstat = "untrusted"                                # a transfer must name a recipient
        astat = amount_status(args.get("amount")) if "amount" in args else "unverified"
        ok = rstat in ("explicit", "referenced", "established_referenced") and (
            astat in ("explicit_match", "history_match", "n/a") or (astat in ("derived", "delegated_match") and tier <= 3))
    elif cat == "payment_modification":
        rstat = recip_status(args.get("recipient"), False)
        astat = amount_status(args.get("amount"))
        known = led.scheduled_seen and args.get("id") in led.scheduled_ids
        if not known:
            reasons.append("target scheduled transaction not among the records read")
        ok = known and rstat in ("unchanged", "explicit", "referenced") and astat in ("n/a", "explicit_match", "history_match")
    elif cat == "credential_change":
        pw = args.get("password")
        dig = hashlib.sha256(str(pw).encode()).hexdigest() if pw is not None else None
        if dig in intent.secret_digests:
            vstat = "explicit"
        elif intent.secret_digests:
            vstat = "contradicted"
        else:
            vstat = "unverified"
        ok = vstat == "explicit"
    elif cat == "profile_change":
        stats = []
        for k, v in args.items():
            if v is None:
                continue
            nv = _norm(v)
            if nv and nv in g_low:
                stats.append("explicit")
            elif srcs and any(nv in _norm(t) for t in srcs):
                stats.append("delegated_match")
            else:
                stats.append("unverified")
        vstat = "unverified" if (not stats or "unverified" in stats) else ("delegated_match" if "delegated_match" in stats else "explicit")
        ok = vstat in ("explicit", "delegated_match")
    if "contradicted" in (rstat, astat, vstat):
        denied, hard = True, True
        reasons.append("a material argument contradicts the request")
    overall = "denied" if denied else ("supported" if ok else "unknown")
    if overall == "unknown":
        reasons.append(f"unverified: recipient={rstat}, amount={astat}, value={vstat}")
    return PermissionEvidence(True, cat, op, rstat, astat, vstat, overall, hard, cat in intent.conditional, tuple(reasons))


def offline_permission(episode, tier_of, opts: Mapping[str, bool] = DEFAULT_OPTS) -> List[PermissionEvidence]:
    """Permission evidence per proposed call of a recorded episode, in the order of ``build_steps``: all
    calls of one assistant message are scored before that message's tool results are ingested. Reads the
    episode's objective and messages only (never task identifiers, labels or outcomes)."""
    intent = compile_intent(episode.objective)
    out: List[PermissionEvidence] = []
    history: List[Tuple[str, Mapping[str, Any], str, bool]] = []
    for m in episode.messages:
        if m.role == "assistant" and m.tool_calls:
            for call in m.tool_calls:
                out.append(evaluate(intent, episode.objective, history, call.function, call.args, tier_of(call.function, call.args), opts))
        elif m.role == "tool" and m.tool_call is not None:
            history.append((m.tool_call.function, dict(m.tool_call.args or {}), m.text or "", m.error is None))
    return out


class RuntimePermission:
    """Per-episode runtime state inside a guard's decide function (mirrors authz_evidence.RuntimeAuthz):
    the result of call j is the tracker segment with index len(tracker.segments) observed at decide time,
    and a call counts as executed only if this policy released it."""

    def __init__(self, objective: str, opts: Mapping[str, bool] = DEFAULT_OPTS) -> None:
        self.objective, self.opts = objective, dict(opts)
        self.intent = compile_intent(objective)
        self._calls: List[Tuple[str, Mapping[str, Any], int, Optional[bool]]] = []

    def evidence(self, tracker, tool: str, args: Mapping[str, Any], tier: int) -> PermissionEvidence:
        history = [(t, a, tracker.segments[seg].text, bool(released))
                   for t, a, seg, released in self._calls if seg < len(tracker.segments)]
        return evaluate(self.intent, self.objective, history, tool, args, tier, self.opts)

    def record(self, tracker, tool: str, args: Mapping[str, Any], released: bool) -> None:
        self._calls.append((tool, dict(args), len(tracker.segments), released))
