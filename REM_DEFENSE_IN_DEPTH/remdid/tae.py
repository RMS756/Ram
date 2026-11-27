"""L1: Trusted Authorization Envelope (TAE) - structured, integrity-protected record of what the user authorized.

Origin rule: entries may be created ONLY by a trusted issuer (``TAEStore.issue``) that holds the integrity key.
Nothing in REM-DiD derives an entry from tool outputs or model text. In the offline evaluation the issuer is an
ORACLE built from benchmark ground truth (see ``oracle.py``) - an upper bound standing in for a trusted,
authenticated approval interface that AgentDojo does not have.

Integrity mechanism actually implemented and tested (tests/test_tae.py):
  HMAC-SHA256 over a canonical JSON serialization of the entry (key held by the store, never by the agent);
  session binding; expiry on a logical clock (decision count) and optional wall clock; single/limited use with an
  atomic use counter; cumulative amount budget (``amount_mode='max'``). Nothing beyond this is claimed: there is no
  key management, no hardware root of trust, and no protection if the store or its key are compromised (AS-3).

Inspiration (file 30/31): AgentCap tokens (short-lived, budget-bounded), AGATE grants (exact parameters, expiry,
limited uses), AIS single-use authority, Progent argument-level policies. Not copied from any of them.
"""
from __future__ import annotations

import enum
import hashlib
import hmac
import json
import os
import threading
import time
from dataclasses import dataclass, field, replace
from decimal import Decimal
from typing import Any, Dict, List, Mapping, Optional, Tuple

from .canonical import canonical_amount
from .provenance import SENSITIVE_FIELDS, canonical_of


class FieldState(str, enum.Enum):
    SPECIFIED = "specified"      # value pinned by the user
    UNSPECIFIED = "unspecified"  # the user did not state it: requires clarification / confirmation
    ANY = "any"                  # explicit wildcard (over-broad authorization; used to model AUTH bypass)


@dataclass(frozen=True)
class FieldSpec:
    state: FieldState
    value: Any = None            # canonical value when SPECIFIED

    def as_json(self):
        v = self.value
        if isinstance(v, Decimal):
            v = str(v)
        return {"state": self.state.value, "value": v}


@dataclass(frozen=True)
class TAEEntry:
    entry_id: str
    session_id: str
    operation: str                           # tool name of the authorized state-changing operation
    fields: Tuple[Tuple[str, FieldSpec], ...]
    amount_mode: str = "exact"               # 'exact' | 'max' (cumulative budget across uses)
    currency: Optional[str] = None           # declared currency; 'not_applicable' if the tool has no currency arg
    source_account: Optional[str] = None
    max_uses: int = 1
    expires_at_decision: Optional[int] = None
    expires_at_wallclock: Optional[float] = None
    nonce: str = ""
    approval_evidence: str = ""              # e.g. 'oracle:ground_truth' - never 'model' or 'tool_output'
    mac: str = ""

    def field(self, name: str) -> Optional[FieldSpec]:
        for k, v in self.fields:
            if k == name:
                return v
        return None

    def payload(self) -> bytes:
        d = {
            "entry_id": self.entry_id, "session_id": self.session_id, "operation": self.operation,
            "fields": [[k, v.as_json()] for k, v in self.fields], "amount_mode": self.amount_mode,
            "currency": self.currency, "source_account": self.source_account, "max_uses": self.max_uses,
            "expires_at_decision": self.expires_at_decision, "expires_at_wallclock": self.expires_at_wallclock,
            "nonce": self.nonce, "approval_evidence": self.approval_evidence,
        }
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()


class AuthStatus(str, enum.Enum):
    AUTHORIZED = "authorized"
    VIOLATION = "violation"            # an entry for the operation exists, a pinned field differs: hard deny
    NO_ENTRY = "no_entry"              # operation not authorized at all: hard deny
    UNSPECIFIED = "unspecified"        # matching entry, but a mandatory field was not specified: confirm
    UNVERIFIABLE = "unverifiable"      # integrity, session, expiry or store failure: never allow
    NOT_APPLICABLE = "not_applicable"  # read-only operation: not gated by 4A


@dataclass
class AuthResult:
    status: AuthStatus
    entry_id: Optional[str] = None
    reasons: Tuple[str, ...] = ()
    pinned: Tuple[str, ...] = ()       # sensitive fields whose value the matching entry pins (SPECIFIED)
    wildcard: Tuple[str, ...] = ()


class TAEStoreError(Exception):
    pass


class TAEStore:
    """Issuer + verifier of TAE entries for ONE session. Thread-safe use counters."""

    def __init__(self, session_id: str, key: Optional[bytes] = None) -> None:
        self.session_id = session_id
        self._key = key or os.urandom(32)
        self._entries: Dict[str, TAEEntry] = {}
        self._uses: Dict[str, int] = {}
        self._spent: Dict[str, Decimal] = {}
        self._lock = threading.Lock()
        self.available = True          # failure injection: store unavailable

    # -- issuing (trusted side only) ----------------------------------------
    def _mac(self, e: TAEEntry) -> str:
        return hmac.new(self._key, e.payload(), hashlib.sha256).hexdigest()

    def issue(self, operation: str, fields: Mapping[str, FieldSpec], *, approval_evidence: str, **kw) -> TAEEntry:
        if approval_evidence.startswith(("model", "tool", "llm")):
            raise TAEStoreError("TAE origin rule: entries may not come from model text or tool output")
        n = len(self._entries)
        e = TAEEntry(entry_id=f"{self.session_id}:{n}", session_id=self.session_id, operation=operation,
                     fields=tuple(sorted(fields.items())), nonce=os.urandom(8).hex(),
                     approval_evidence=approval_evidence, **kw)
        e = replace(e, mac=self._mac(e))
        self._entries[e.entry_id] = e
        self._uses[e.entry_id] = 0
        self._spent[e.entry_id] = Decimal(0)
        return e

    def entries(self) -> List[TAEEntry]:
        return list(self._entries.values())

    def _tamper_for_test(self, entry_id: str, **changes) -> None:
        """Test hook: replace an entry WITHOUT recomputing its MAC (simulates modification at rest)."""
        self._entries[entry_id] = replace(self._entries[entry_id], **changes)

    # -- verification ----------------------------------------------------------
    def verify(self, e: TAEEntry, decision_no: int, session_id: str, now: Optional[float] = None) -> Optional[str]:
        if not hmac.compare_digest(e.mac, self._mac(e)):
            return "integrity_mac_mismatch"
        if e.session_id != session_id or session_id != self.session_id:
            return "cross_session"
        if e.expires_at_decision is not None and decision_no > e.expires_at_decision:
            return "expired_logical"
        if e.expires_at_wallclock is not None and (now if now is not None else time.time()) > e.expires_at_wallclock:
            return "expired_wallclock"
        if self._uses[e.entry_id] >= e.max_uses:
            return "uses_exhausted"
        return None

    def check(self, tool: str, args: Mapping[str, Any], decision_no: int, session_id: str,
              unchanged: Optional[Mapping[str, Any]] = None, consume: bool = True) -> AuthResult:
        """4A matching. ``unchanged``: current stored values (e.g. of a scheduled transaction) - a call that sets a
        field to its current value is not a change. Fields not mentioned by an entry may not be changed."""
        if tool not in SENSITIVE_FIELDS:
            return AuthResult(AuthStatus.NOT_APPLICABLE)
        if not self.available:
            return AuthResult(AuthStatus.UNVERIFIABLE, reasons=("tae_store_unavailable",))
        with self._lock:
            cands = [e for e in self._entries.values() if e.operation == tool]
            if not cands:
                return AuthResult(AuthStatus.NO_ENTRY, reasons=(f"no_entry_for_{tool}",))
            best: Optional[AuthResult] = None
            for e in cands:
                bad = self.verify(e, decision_no, session_id)
                if bad:
                    r = AuthResult(AuthStatus.UNVERIFIABLE, e.entry_id, (bad,))
                    best = best or r
                    continue
                res = self._match(e, tool, args, unchanged or {})
                if res.status is AuthStatus.AUTHORIZED:
                    if consume:
                        self._uses[e.entry_id] += 1
                        a = res_amount = canonical_amount(args.get("amount")) if "amount" in args else None
                        if a is not None:
                            self._spent[e.entry_id] += a
                    return res
                # keep the most informative failure: UNSPECIFIED > VIOLATION > UNVERIFIABLE
                rank = {AuthStatus.UNSPECIFIED: 3, AuthStatus.VIOLATION: 2, AuthStatus.UNVERIFIABLE: 1}
                if best is None or rank.get(res.status, 0) > rank.get(best.status, 0):
                    best = res
            return best or AuthResult(AuthStatus.NO_ENTRY)

    def _match(self, e: TAEEntry, tool: str, args: Mapping[str, Any], unchanged: Mapping[str, Any]) -> AuthResult:
        reasons, unspecified, pinned, wild = [], [], [], []
        for f, kind in SENSITIVE_FIELDS[tool]:
            spec = e.field(f)
            present = f in args and args[f] is not None
            val = canonical_of(kind, args[f]) if present else None
            if spec is None:
                # not authorized to change this field (unless the call leaves it at its current value)
                if present and not (f in unchanged and unchanged[f] is not None and val == unchanged[f]):
                    reasons.append(f"field_not_authorized:{f}")
                continue
            if spec.state is FieldState.ANY:
                wild.append(f)
                continue
            if spec.state is FieldState.UNSPECIFIED:
                if present:
                    unspecified.append(f)
                continue
            # SPECIFIED
            pinned.append(f)
            if not present:
                continue                       # leaving a pinned field untouched is not a violation
            if val is None:
                reasons.append(f"unparseable:{f}")
            elif kind == "amount" and e.amount_mode == "max":
                if val > Decimal(spec.value) - self._spent[e.entry_id]:
                    reasons.append("amount_exceeds_remaining_budget")
            elif val != (Decimal(spec.value) if kind == "amount" else spec.value):
                reasons.append(f"mismatch:{f}")
        if e.currency not in (None, "not_applicable"):
            cur = args.get("currency")
            if cur is not None and str(cur).upper() != e.currency.upper():
                reasons.append("mismatch:currency")
        if e.source_account is not None and args.get("source_account") not in (None, e.source_account):
            reasons.append("mismatch:source_account")
        if reasons:
            return AuthResult(AuthStatus.VIOLATION, e.entry_id, tuple(reasons), tuple(pinned), tuple(wild))
        if unspecified:
            return AuthResult(AuthStatus.UNSPECIFIED, e.entry_id, tuple(f"unspecified:{u}" for u in unspecified),
                              tuple(pinned), tuple(wild))
        return AuthResult(AuthStatus.AUTHORIZED, e.entry_id, (), tuple(pinned), tuple(wild))

    def release_use(self, entry_id: str, amount: Any = None) -> None:
        """Return a consumed use when the call was finally NOT executed (withheld by a later control)."""
        with self._lock:
            if entry_id in self._uses and self._uses[entry_id] > 0:
                self._uses[entry_id] -= 1
                a = canonical_amount(amount) if amount is not None else None
                if a is not None:
                    self._spent[entry_id] -= a
