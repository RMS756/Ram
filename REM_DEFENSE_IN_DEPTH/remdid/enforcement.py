"""L5: capability-bound enforcement gateway (independent enforcement boundary) + hash-chained audit (cross-cutting).

A release decision is turned into a PERMIT: HMAC-SHA256 over (session, tool, canonical arguments, nonce, expiry,
budget). The tool adapter executes a call ONLY through ``Gateway.execute``, which re-validates the permit against
the ACTUAL arguments immediately before execution (time-of-check = time-of-use), consumes it, and refuses on any
error (fail-closed). Permits can be attenuated (narrower expiry/budget) but never widened.
Inspiration: AgentCap capability tokens (abstract), AGATE parameter-bound grants (abstract), GuardRail Action
Passport (abstract). Implementation is original and tested in tests/test_enforcement.py; no claim beyond tests.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import threading
from dataclasses import dataclass, replace
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

from .provenance import SENSITIVE_FIELDS, canonical_of


def canonical_args(tool: str, args: Mapping[str, Any]) -> Dict[str, Any]:
    kinds = dict(SENSITIVE_FIELDS.get(tool, ()))
    out = {}
    for k in sorted(args):
        v = args[k]
        c = canonical_of(kinds[k], v) if k in kinds else v
        out[k] = str(c) if c is not None else repr(v)
    return out


@dataclass(frozen=True)
class Permit:
    permit_id: str
    session_id: str
    tool: str
    args_digest: str
    expires_at_decision: int
    budget: int
    mac: str

    def body(self) -> bytes:
        return json.dumps([self.permit_id, self.session_id, self.tool, self.args_digest,
                           self.expires_at_decision, self.budget], separators=(",", ":")).encode()


class GatewayRefusal(Exception):
    pass


class Gateway:
    def __init__(self, session_id: str, key: Optional[bytes] = None, failing: bool = False) -> None:
        self.session_id = session_id
        self._key = key or os.urandom(32)
        self._used: Dict[str, int] = {}
        self._lock = threading.Lock()
        self.failing = failing          # failure injection: gateway itself broken
        self.audit: List[Dict[str, Any]] = []
        self._prev = "0" * 64
        self.executions = 0
        self.refusals = 0

    def _mac(self, p: Permit) -> str:
        return hmac.new(self._key, p.body(), hashlib.sha256).hexdigest()

    @staticmethod
    def digest(tool: str, args: Mapping[str, Any]) -> str:
        return hashlib.sha256(json.dumps([tool, canonical_args(tool, args)], sort_keys=True).encode()).hexdigest()

    def issue(self, tool: str, args: Mapping[str, Any], decision_no: int, ttl: int = 0, budget: int = 1) -> Permit:
        n = os.urandom(8).hex()
        p = Permit(n, self.session_id, tool, self.digest(tool, args), decision_no + ttl, budget, "")
        return replace(p, mac=self._mac(p))

    def attenuate(self, p: Permit, budget: Optional[int] = None, expires_at_decision: Optional[int] = None) -> Permit:
        nb = p.budget if budget is None else min(budget, p.budget)
        ne = p.expires_at_decision if expires_at_decision is None else min(expires_at_decision, p.expires_at_decision)
        q = replace(p, budget=nb, expires_at_decision=ne, mac="")
        return replace(q, mac=self._mac(q))

    def _log(self, event: str, **kw) -> None:
        rec = {"event": event, **kw, "prev": self._prev}
        h = hashlib.sha256(json.dumps(rec, sort_keys=True, default=str).encode()).hexdigest()
        rec["hash"] = h
        self._prev = h
        self.audit.append(rec)

    def verify_chain(self) -> bool:
        prev = "0" * 64
        for r in self.audit:
            body = {k: v for k, v in r.items() if k != "hash"}
            if body["prev"] != prev or hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest() != r["hash"]:
                return False
            prev = r["hash"]
        return True

    def execute(self, permit: Optional[Permit], tool: str, args: Mapping[str, Any], decision_no: int,
                runner: Callable[[], Any]) -> Any:
        """Validate-then-run. Any failure -> GatewayRefusal (the call does not reach the tool)."""
        try:
            if self.failing:
                raise GatewayRefusal("gateway_failure_injected")
            if permit is None:
                raise GatewayRefusal("no_permit")
            if not hmac.compare_digest(permit.mac, self._mac(permit)):
                raise GatewayRefusal("permit_mac_mismatch")
            if permit.session_id != self.session_id:
                raise GatewayRefusal("cross_session_permit")
            if permit.tool != tool:
                raise GatewayRefusal("permit_tool_mismatch")
            if permit.args_digest != self.digest(tool, args):
                raise GatewayRefusal("permit_argument_mismatch")
            if decision_no > permit.expires_at_decision:
                raise GatewayRefusal("permit_expired")
            with self._lock:
                if self._used.get(permit.permit_id, 0) >= permit.budget:
                    raise GatewayRefusal("permit_budget_exhausted")
                self._used[permit.permit_id] = self._used.get(permit.permit_id, 0) + 1
        except GatewayRefusal as r:
            self.refusals += 1
            self._log("refuse", tool=tool, reason=str(r), decision=decision_no)
            raise
        except Exception as exc:                      # fail-closed on internal errors
            self.refusals += 1
            self._log("refuse", tool=tool, reason=f"internal_error:{exc!r}"[:120], decision=decision_no)
            raise GatewayRefusal("internal_error") from exc
        self._log("execute", tool=tool, permit=permit.permit_id, decision=decision_no)
        self.executions += 1
        return runner()
