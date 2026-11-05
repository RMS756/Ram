"""Tests of the REM deployment gateway (rem.deployment.gateway) with the simulated banking API.

Both services run in-process on free localhost ports; REM decisions come from fixed test decide functions
(the frozen components are exercised by experiments/deployment_sim/run_deployment_sim.py). Checks:
withheld calls never reach the backend, released calls execute exactly once, ids and order preserved,
fail-closed on internal error, 4xx on unknown/malformed requests, backend failure classified as an
infrastructure error, per-episode isolation under concurrency."""
from __future__ import annotations

import concurrent.futures as cf
import os
import sys
import threading

import pytest

pytest.importorskip("agentdojo")
import importlib.metadata as md  # noqa: E402

if md.version("agentdojo") != "0.1.35":
    pytest.skip("deployment simulation targets the main environment (AgentDojo 0.1.35)", allow_module_level=True)
requests = pytest.importorskip("requests")

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "experiments", "deployment_sim"))
sys.path.insert(0, os.path.dirname(__file__))

import bank_backend  # noqa: E402
from http.server import ThreadingHTTPServer  # noqa: E402

from rem.core.results import Verdict  # noqa: E402
from rem.deployment.gateway import RemGateway, serve  # noqa: E402
from test_live_integration import ATTACKER, guard as make_guard  # noqa: E402

TOOLS = {t.name for t in bank_backend.SUITE.tools}
LEGIT = "FR7630006000011234567890189"


def pay(to, amount=10):
    return {"function": "send_money", "args": {"recipient": to, "amount": amount, "subject": "s", "date": "2022-01-01"}}


@pytest.fixture()
def services():
    store = bank_backend.Store()
    bsrv = ThreadingHTTPServer(("127.0.0.1", 0), bank_backend.handler(store))
    threading.Thread(target=bsrv.serve_forever, daemon=True).start()
    rules = {}

    def provider(meta):
        decide = rules.get(meta["configuration"])
        if decide is None:
            raise ValueError("unknown configuration")
        return make_guard(decide), TOOLS
    gw = RemGateway(provider, f"http://127.0.0.1:{bsrv.server_address[1]}")
    gsrv = serve(gw)
    threading.Thread(target=gsrv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{gsrv.server_address[1]}"
    yield base, rules, store, gw, bsrv
    gsrv.shutdown()
    bsrv.shutdown()


def open_ep(base, sid, conf):
    r = requests.post(f"{base}/v1/episodes", json={"episode_id": sid, "configuration": conf, "pipeline": "test",
                                                   "user_task_id": "user_task_0", "injection_task_id": "injection_task_0",
                                                   "injections": {}, "system_prompt": "s", "user_prompt": "u"})
    assert r.status_code == 200, r.text


def block_attacker(c):
    return (Verdict.BLOCK, "t", {}) if c.args.get("recipient") == ATTACKER else (Verdict.ALLOW, "t", {})


def test_withheld_never_reaches_backend_and_released_executes_once(services):
    base, rules, store, gw, _ = services
    rules["R"] = block_attacker
    open_ep(base, "e1", "R")
    calls = [dict(pay(LEGIT), id="c1"), dict(pay(ATTACKER), id="c2"), {"id": "c3", "function": "get_balance", "args": {}}]
    res = requests.post(f"{base}/v1/episodes/e1/calls", json={"calls": calls}).json()["results"]
    assert [r["tool_call_id"] for r in res] == ["c1", "c2", "c3"]
    assert [r["released"] for r in res] == [True, False, True]
    assert res[1]["error"].startswith("REM:") and res[1]["verdict"] == "block"
    executed = store.eps["e1"]["executed"]
    assert [e["function"] for e in executed] == ["send_money", "get_balance"]
    assert all(e["args"].get("recipient") != ATTACKER for e in executed)
    out = requests.post(f"{base}/v1/episodes/e1/close", json={"model_output": [], "function_calls": calls}).json()
    assert len(out["audit"]) == 3 and len(out["backend_executed"]) == 2


def test_fail_closed_on_internal_rem_error(services):
    base, rules, store, gw, _ = services

    def broken(c):
        raise RuntimeError("policy failure")
    rules["X"] = broken
    open_ep(base, "e2", "X")
    res = requests.post(f"{base}/v1/episodes/e2/calls", json={"calls": [dict(pay(ATTACKER), id="c1")]}).json()["results"]
    assert res[0]["released"] is False and "fail-closed" in res[0]["error"]
    assert store.eps["e2"]["executed"] == [] and gw.counters["fail_closed"] == 1


def test_unknown_and_malformed_requests_execute_nothing(services):
    base, rules, store, gw, _ = services
    assert requests.post(f"{base}/v1/episodes/missing/calls", json={"calls": [pay(ATTACKER)]}).status_code == 404
    assert requests.post(f"{base}/v1/episodes", data=b"{bad", headers={"Content-Type": "application/json"}).status_code == 400
    assert requests.post(f"{base}/v1/episodes", json={"episode_id": "z", "configuration": "nope",
                                                      "user_task_id": "user_task_0"}).status_code == 400
    assert store.eps == {}


def test_invalid_tool_name_is_refused_without_execution(services):
    base, rules, store, gw, _ = services
    rules["R"] = block_attacker
    open_ep(base, "e3", "R")
    res = requests.post(f"{base}/v1/episodes/e3/calls", json={"calls": [{"id": "c", "function": "drop_tables", "args": {}}]}).json()["results"]
    assert res[0]["error"] == "Invalid tool drop_tables provided." and store.eps["e3"]["executed"] == []


def test_backend_failure_is_an_infrastructure_error_not_a_decision(services):
    base, rules, store, gw, bsrv = services
    rules["R"] = block_attacker
    open_ep(base, "e4", "R")
    bsrv.shutdown()
    bsrv.server_close()
    res = requests.post(f"{base}/v1/episodes/e4/calls", json={"calls": [dict(pay(LEGIT), id="c1")]}).json()["results"]
    assert res[0]["released"] is True and res[0]["error"].startswith("backend unavailable")
    assert gw.counters["backend_errors"] == 1


def test_concurrent_episodes_are_isolated(services):
    base, rules, store, gw, _ = services
    rules["R"] = block_attacker

    def one(i):
        sid = f"c{i}"
        open_ep(base, sid, "R")
        requests.post(f"{base}/v1/episodes/{sid}/calls", json={"calls": [dict(pay(LEGIT, amount=i + 1), id="a"),
                                                                         dict(pay(ATTACKER), id="b")]})
        ex = list(store.eps[sid]["executed"])
        out = requests.post(f"{base}/v1/episodes/{sid}/close", json={"model_output": [], "function_calls": []}).json()
        return i, ex, out["audit"]
    with cf.ThreadPoolExecutor(8) as pool:
        res = list(pool.map(one, range(24)))
    for i, ex, audit in res:
        assert len(ex) == 1 and ex[0]["args"]["amount"] == i + 1        # only this episode's legitimate call
        assert [a["released"] for a in audit] == [True, False]
    assert store.eps == {} and gw.episodes == {}
