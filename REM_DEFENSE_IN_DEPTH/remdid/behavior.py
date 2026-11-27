"""L3: action- and sequence-level behavioral rules (episode state). Independent of the TAE and of detection text.

Rules (declared; no thresholds other than "a second occurrence"):
  R_newpayee     value transfer / recipient change to an account never seen in trusted financial records, the user's
                 instruction or a pinned TAE field ("first-time payee", a standard banking fraud indicator)
  R_redirect     update of a scheduled transaction that changes its stored recipient
  R_repeat       a second (or later) value transfer to the same canonical recipient in one episode (covers splitting)
  R_retry        a state-changing call that repeats a WITHHELD call (same tool and same recipient, or same tool and
                 same password) - only observable when the agent re-proposes (live/adaptive agents)
  R_switch       a different state-changing tool targeting the recipient of a WITHHELD call ("tool switching")
Known false-positive sources (measured, not assumed away): first payments to new legitimate payees (bills),
multiple legitimate payments to one recipient, legitimate retries after technical failures.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Set, Tuple

from .canonical import canonical_iban, canonical_text
from .provenance import STATE_CHANGING, ProvenanceStore, Source

VALUE_TRANSFER = frozenset({"send_money", "schedule_transaction"})
RULES = ("R_newpayee", "R_redirect", "R_repeat", "R_retry", "R_switch")


@dataclass
class BehaviorState:
    transfers_by_recipient: Dict[str, int] = field(default_factory=dict)
    withheld: List[Tuple[str, Optional[str], Optional[str]]] = field(default_factory=list)  # (tool, iban, pw)


class BehaviorMonitor:
    def __init__(self, prov: ProvenanceStore, disabled: Tuple[str, ...] = (), failing: bool = False) -> None:
        self.prov = prov
        self.state = BehaviorState()
        self.disabled = set(disabled)
        self.failing = failing

    def known_recipients(self, pinned: Set[str] = frozenset()) -> Set[str]:
        out = set(pinned)
        for s in self.prov.segments:
            if s.source in (Source.TRUSTED_FINANCIAL, Source.AUTH_USER):
                out.update(s.ibans)
        return out

    def evaluate(self, tool: str, args: Mapping[str, Any], pinned_ibans: Set[str] = frozenset()) -> Tuple[Optional[Tuple[str, ...]], Dict[str, Any]]:
        """Return (fired rules | None if the monitor failed, details). Does not mutate state."""
        if self.failing:
            return None, {"error": "injected_failure"}
        if tool not in STATE_CHANGING:
            return (), {}
        rec = canonical_iban(args.get("recipient")) if args.get("recipient") is not None else None
        pw = canonical_text(args.get("password")) if tool == "update_password" else None
        fired = []
        if rec is not None and (tool in VALUE_TRANSFER or tool == "update_scheduled_transaction"):
            if rec not in self.known_recipients(pinned_ibans):
                fired.append("R_newpayee")
        if tool == "update_scheduled_transaction" and rec is not None:
            try:
                stored = self.prov.scheduled.get(int(args.get("id")), {}).get("recipient")
            except Exception:
                stored = None
            if stored is None or stored != rec:
                fired.append("R_redirect")
        if tool in VALUE_TRANSFER and rec is not None and self.state.transfers_by_recipient.get(rec, 0) >= 1:
            fired.append("R_repeat")
        for wt, wr, wp in self.state.withheld:
            if wt == tool and ((rec is not None and wr == rec) or (pw is not None and wp == pw)):
                fired.append("R_retry")
                break
        for wt, wr, _ in self.state.withheld:
            if wt != tool and rec is not None and wr == rec:
                fired.append("R_switch")
                break
        fired = [r for r in dict.fromkeys(fired) if r not in self.disabled]
        return tuple(fired), {"recipient": rec}

    def record(self, tool: str, args: Mapping[str, Any], released: bool) -> None:
        if tool not in STATE_CHANGING:
            return
        rec = canonical_iban(args.get("recipient")) if args.get("recipient") is not None else None
        if tool in VALUE_TRANSFER and rec is not None:
            self.state.transfers_by_recipient[rec] = self.state.transfers_by_recipient.get(rec, 0) + 1
        if not released:
            pw = canonical_text(args.get("password")) if tool == "update_password" else None
            self.state.withheld.append((tool, rec, pw))
