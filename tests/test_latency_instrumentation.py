"""Timer boundaries of RemGuard.evaluate, checked with a fake clock (no wall-clock assertions).

R4 regression check for the independent review of 1 Nov 2026 (Finding 2): the
historical timer ``rem_latency_ms`` stops before attribution, audit-record
construction and history recording; the complete-call timer
``rem_latency_full_ms`` stops after all of them.
"""

import numpy as np

import rem.integration.agentdojo_replay as replay
from rem.integration.agentdojo_replay import FrozenScorer, RemGuard
from tests.test_mitigation_semantics import _guard


def _instrumented(monkeypatch):
    events = []
    ticks = iter(range(1000))

    def clock():
        t = next(ticks)
        events.append(("clock", t))
        return float(t)

    base = _guard("step_level")
    names = tuple(base.tracker.features("get_balance", {})[0])
    scorer = FrozenScorer(names, 0.0, tuple(0.1 for _ in names), 0.0, 1.0, tuple(0.0 for _ in names))
    g = RemGuard(base.config, scorer, base.decide, base.labeler, base.episode)

    shapley, record, digest = g._attr.shapley_value, g.tracker.record_proposal, replay.content_digest

    def shapley_logged(*a):
        events.append(("attribution", None))
        return shapley(*a)

    def record_logged(*a):
        events.append(("history", None))
        return record(*a)

    def digest_logged(*a):
        events.append(("audit", None))
        return digest(*a)

    monkeypatch.setattr(g._attr, "shapley_value", shapley_logged)
    monkeypatch.setattr(g.tracker, "record_proposal", record_logged)
    monkeypatch.setattr(replay, "content_digest", digest_logged)
    monkeypatch.setattr(replay.time, "perf_counter", clock)
    return g, events


def test_partial_timer_stops_before_attribution_audit_and_history(monkeypatch):
    g, events = _instrumented(monkeypatch)
    g.evaluate("send_money", {"recipient": "X", "amount": 10})
    kinds = [k for k, _ in events]
    clocks = [i for i, k in enumerate(kinds) if k == "clock"]
    assert len(clocks) == 3                      # start, partial stop, full stop
    start, partial_stop, full_stop = clocks
    first = {k: kinds.index(k) for k in ("attribution", "audit", "history")}
    assert start < partial_stop < min(first.values())
    assert max(i for i, k in enumerate(kinds) if k != "clock") < full_stop
    assert first["attribution"] < first["audit"] < first["history"]


def test_both_timers_are_recorded_and_full_is_not_shorter(monkeypatch):
    g, _ = _instrumented(monkeypatch)
    g.evaluate("send_money", {"recipient": "X", "amount": 10})
    rec = g.audit[-1]
    assert rec["rem_latency_ms"] == 1000.0      # one fake tick
    assert rec["rem_latency_full_ms"] == 2000.0  # two fake ticks
    assert g.latencies_ms == [1000.0] and g.full_latencies_ms == [2000.0]
    assert np.isfinite(rec["additivity_error"])
