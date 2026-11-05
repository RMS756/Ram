"""Spending guard for OpenAI-compatible clients (chat completions and embeddings).

Wraps a client object; the wrapped object is passed to AgentDojo's OpenAILLM and to MELON's
``detection_model``, so EVERY paid call of both conditions (agent turns, MELON's masked re-execution,
MELON's embedding calls) passes through one ledger.

Before a call, a worst-case cost is RESERVED:
  chat:       ceil(chars(messages + tools) / chars_per_token_lower_bound) * input_price
              + reserve_output_tokens * output_price
  embeddings: ceil(chars(input) / chars_per_token_lower_bound) * embedding_price
The call is refused (``BudgetExceeded``) when committed + reserved(in flight) + this reservation > cap.
After the call, the reservation is replaced by the cost computed from the provider's reported usage.

Prices are NOT built in: they must be supplied in the run configuration (USD per 1M tokens), taken by the
operator from the provider's price list on the day of the run. No price is invented here.

Limitations (stated in MELON_REM_EXPERIMENT_PROTOCOL.md):
  * the guard sees only calls made through the wrapped client in this process (one process per run);
  * the input-token reservation is a character-based upper-bound heuristic, not the provider tokenizer;
  * if a response exceeds reserve_output_tokens (no max_tokens is sent by AgentDojo 0.1.29), the actual
    cost can exceed the reservation for that one call; the cap can therefore be overshot by at most the
    excess of the in-flight calls; set cap with this margin;
  * provider-side billing (cached-input discounts, rounding, retries inside the SDK) may differ from the
    ledger; reconcile with the provider's usage dashboard after the run;
  * a call refused by the guard is recorded as ``budget_stop`` (never as a prevented attack).
"""
from __future__ import annotations

import json
import math
import threading
import time
from typing import Any, Dict, Optional


class BudgetExceeded(RuntimeError):
    pass


class Ledger:
    def __init__(self, cap_usd: float, prices: Dict[str, Dict[str, float]], *, chars_per_token_lower_bound: float,
                 reserve_output_tokens: int, path: Optional[str] = None) -> None:
        if cap_usd is None or float(cap_usd) <= 0:
            raise ValueError("a positive spending cap (USD) is required")
        self.cap = float(cap_usd)
        self.prices = prices
        self.cpt = float(chars_per_token_lower_bound)
        self.reserve_out = int(reserve_output_tokens)
        self.path = path
        self.committed = 0.0
        self.in_flight: Dict[int, float] = {}
        self.calls = 0
        self.tokens = {"input": 0, "output": 0, "embedding": 0}
        self._lock = threading.Lock()
        self._next = 0

    def _price(self, model: str, kind: str) -> float:
        if model not in self.prices or kind not in self.prices[model]:
            raise BudgetExceeded(f"no declared price for model {model!r} ({kind}); refusing the call")
        return float(self.prices[model][kind]) / 1e6

    def reserve(self, model: str, kind: str, chars: int) -> int:
        est_in = math.ceil(chars / self.cpt)
        if kind == "chat":
            amount = est_in * self._price(model, "input") + self.reserve_out * self._price(model, "output")
        else:
            amount = est_in * self._price(model, "embedding")
        with self._lock:
            if self.committed + sum(self.in_flight.values()) + amount > self.cap:
                raise BudgetExceeded(
                    f"call refused: committed {self.committed:.4f} + in-flight {sum(self.in_flight.values()):.4f}"
                    f" + reservation {amount:.4f} > cap {self.cap:.4f} USD")
            self._next += 1
            self.in_flight[self._next] = amount
            return self._next

    def settle(self, rid: int, model: str, kind: str, usage: Any) -> float:
        if kind == "chat":
            tin = int(getattr(usage, "prompt_tokens", 0) or 0)
            tout = int(getattr(usage, "completion_tokens", 0) or 0)
            cost = tin * self._price(model, "input") + tout * self._price(model, "output")
        else:
            tin, tout = int(getattr(usage, "prompt_tokens", 0) or getattr(usage, "total_tokens", 0) or 0), 0
            cost = tin * self._price(model, "embedding")
        with self._lock:
            self.in_flight.pop(rid, None)
            self.committed += cost
            self.calls += 1
            if kind == "chat":
                self.tokens["input"] += tin
                self.tokens["output"] += tout
            else:
                self.tokens["embedding"] += tin
        self._log({"t": time.time(), "model": model, "kind": kind, "in": tin, "out": tout, "cost_usd": cost,
                   "committed_usd": self.committed})
        return cost

    def release(self, rid: int) -> None:
        with self._lock:
            self.in_flight.pop(rid, None)

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {"committed_usd": self.committed, "in_flight_usd": sum(self.in_flight.values()),
                    "cap_usd": self.cap, "calls": self.calls, "tokens": dict(self.tokens)}

    def _log(self, rec: Dict[str, Any]) -> None:
        if self.path:
            with open(self.path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec) + "\n")


def _chars(obj: Any) -> int:
    try:
        return len(json.dumps(obj, default=str))
    except Exception:
        return len(str(obj))


class _Completions:
    def __init__(self, inner, ledger: Ledger) -> None:
        self._inner, self._ledger = inner, ledger

    def create(self, **kw):
        model = kw.get("model")
        rid = self._ledger.reserve(model, "chat", _chars(kw.get("messages")) + _chars(kw.get("tools")))
        try:
            resp = self._inner.create(**kw)
        except BaseException:
            self._ledger.release(rid)      # a failed call is billed by usage only if the provider reports it
            raise
        self._ledger.settle(rid, model, "chat", getattr(resp, "usage", None))
        return resp


class _Chat:
    def __init__(self, inner, ledger) -> None:
        self.completions = _Completions(inner.completions, ledger)


class _Embeddings:
    def __init__(self, inner, ledger: Ledger) -> None:
        self._inner, self._ledger = inner, ledger

    def create(self, **kw):
        model = kw.get("model")
        rid = self._ledger.reserve(model, "embedding", _chars(kw.get("input")))
        try:
            resp = self._inner.create(**kw)
        except BaseException:
            self._ledger.release(rid)
            raise
        self._ledger.settle(rid, model, "embedding", getattr(resp, "usage", None))
        return resp


class GuardedClient:
    """Drop-in replacement for the parts of ``openai.OpenAI`` used by AgentDojo's OpenAILLM and by MELON."""

    def __init__(self, client, ledger: Ledger) -> None:
        self._client = client
        self.ledger = ledger
        self.chat = _Chat(client.chat, ledger)
        self.embeddings = _Embeddings(client.embeddings, ledger)
