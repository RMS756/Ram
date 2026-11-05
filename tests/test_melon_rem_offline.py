"""Version-independent checks of the MELON vs MELON + REM tooling: spending guard, analysis, fail-closed runner.
No model call is made; fake clients only."""
from __future__ import annotations

import os
import subprocess
import sys
import threading

import pytest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "experiments", "melon_rem"))
from analyze_melon_rem import summarize  # noqa: E402
from spending_guard import BudgetExceeded, GuardedClient, Ledger  # noqa: E402

PRICES = {"m": {"input": 1.0, "output": 2.0}, "e": {"embedding": 0.5}}   # test prices (USD / 1M tokens), not real


class _Usage:
    def __init__(self, i, o=0):
        self.prompt_tokens, self.completion_tokens, self.total_tokens = i, o, i + o


class FakeOpenAI:
    def __init__(self, i=1000, o=500, gate=None):
        outer = self

        class C:
            def create(self, **kw):
                if gate is not None:
                    gate.wait(5)
                return type("R", (), {"usage": _Usage(outer.i, outer.o)})()

        class E:
            def create(self, **kw):
                return type("R", (), {"usage": _Usage(10)})()
        self.i, self.o = i, o
        self.chat = type("Chat", (), {"completions": C()})()
        self.embeddings = E()


def ledger(cap, **kw):
    return Ledger(cap, PRICES, chars_per_token_lower_bound=2.0, reserve_output_tokens=kw.get("reserve", 1000))


def test_ledger_settles_actual_usage_and_counts_tokens():
    L = ledger(1.0)
    c = GuardedClient(FakeOpenAI(1000, 500), L)
    c.chat.completions.create(model="m", messages=[{"role": "user", "content": "hi"}])
    c.embeddings.create(model="e", input="abc")
    s = L.snapshot()
    assert s["calls"] == 2 and s["tokens"] == {"input": 1000, "output": 500, "embedding": 10}
    assert s["committed_usd"] == pytest.approx(1000 * 1e-6 + 500 * 2e-6 + 10 * 0.5e-6)
    assert s["in_flight_usd"] == 0


def test_call_refused_when_reservation_would_exceed_cap():
    L = ledger(0.001, reserve=1000)                 # output reservation alone costs 0.002
    c = GuardedClient(FakeOpenAI(), L)
    with pytest.raises(BudgetExceeded):
        c.chat.completions.create(model="m", messages=[])
    assert L.snapshot()["calls"] == 0


def test_unpriced_model_is_refused():
    with pytest.raises(BudgetExceeded):
        GuardedClient(FakeOpenAI(), ledger(10)).chat.completions.create(model="unknown", messages=[])


def test_in_flight_reservations_count_against_the_cap():
    gate = threading.Event()
    L = ledger(0.003, reserve=1000)                 # one reservation ~0.002: a second concurrent call must be refused
    c = GuardedClient(FakeOpenAI(gate=gate), L)
    t = threading.Thread(target=lambda: c.chat.completions.create(model="m", messages=[]))
    t.start()
    for _ in range(100):
        if L.snapshot()["in_flight_usd"] > 0:
            break
        threading.Event().wait(0.01)
    with pytest.raises(BudgetExceeded):
        c.chat.completions.create(model="m", messages=[])
    gate.set()
    t.join()
    assert L.snapshot()["in_flight_usd"] == 0


def rec(cond, u, i, sec, util, err=None, rep=0, audit=()):
    return {"condition": cond, "user_task": u, "injection_task": i, "repeat": rep, "security": sec, "utility": util,
            "error_class": err, "wall_time_s": 1.0, "rem_audit": list(audit), "cost_usd": 0.0, "tokens": {},
            "model_calls": 0, "run_id": "test"}


def test_analysis_denominators_errors_and_escalation():
    esc = {"released": False, "verdict": "escalate", "rem_latency_full_ms": 0.3}
    R = [
        rec("MELON", "u1", "i1", True, False), rec("MELON_REM", "u1", "i1", False, False, audit=[esc]),
        rec("MELON", "u2", "i1", False, True), rec("MELON_REM", "u2", "i1", False, True),
        rec("MELON", "u3", "i1", True, False), rec("MELON_REM", "u3", "i1", False, False, err="timeout"),
        rec("MELON", "u1", None, None, True), rec("MELON_REM", "u1", None, None, False, audit=[esc]),
    ]
    s = summarize(R, resamples=200, seed=1)
    m, r = s["conditions"]["MELON"], s["conditions"]["MELON_REM"]
    assert m["ASR"] == pytest.approx(2 / 3) and m["attacked_episodes_without_error"] == 3
    assert r["ASR"] == 0.0 and r["attacked_episodes_without_error"] == 2      # the timeout is excluded, not a prevention
    assert r["errors_by_class"] == {"timeout": 1}
    assert r["benign_utility"] == 0.0                                          # an escalated benign call is not success
    assert r["rem_escalate_verdicts"] == 2
    d = s["paired_differences"]["ASR"]
    assert d["pairs"] == 2 and d["mean_paired_difference_MELON_REM_minus_MELON"] == pytest.approx(-0.5)
    assert d["discordant_REM0_MELON1"] == 1 and d["discordant_REM1_MELON0"] == 0


def test_zero_melon_asr_is_reported_as_such():
    R = [rec("MELON", "u1", "i1", False, True), rec("MELON_REM", "u1", "i1", False, True)]
    assert "no further reduction" in summarize(R, resamples=50)["note_zero_melon_asr"]


def test_runner_is_fail_closed_on_the_template():
    p = subprocess.run([sys.executable, os.path.join(REPO, "experiments", "melon_rem", "run_melon_rem.py"),
                        "--config", os.path.join(REPO, "experiments", "melon_rem", "melon_rem_config_TEMPLATE.yaml"),
                        "--out", os.path.join(REPO, "build", "should_not_exist"), "--dry-run"],
                       capture_output=True, text=True, env={k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"})
    assert p.returncode == 2 and "[DESIGN BLOCKED]" in p.stderr
    assert not os.path.exists(os.path.join(REPO, "build", "should_not_exist"))


def test_budget_projection_uses_only_measured_tokens_and_given_prices():
    from estimate_budget import project
    P = {"m": {"input": 1.0, "output": 2.0}, "text-embedding-3-large": {"embedding": 0.5}}
    R = [{"condition": "MELON", "backbone": "m", "injection_task": "i", "tokens": {"input": 1e6, "output": 0, "embedding": 0}},
         {"condition": "MELON", "backbone": "m", "injection_task": None, "tokens": {"input": 0, "output": 1e6, "embedding": 2e6}}]
    out = project(R, P, cases_attacked=144, cases_benign=16, repeats=2, margin=0.0)
    assert out["central_usd"] == pytest.approx((1.0 * 144 + 3.0 * 16) * 2)
    assert out["recommended_cap_usd"] == pytest.approx(out["conservative_usd"])
