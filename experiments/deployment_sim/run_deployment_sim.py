"""REM deployment simulation: gateway service + simulated banking API + recorded real-agent traffic.

usage: PILOT_RESULTS_DIR=<frozen pilot state> python3 experiments/deployment_sim/run_deployment_sim.py \
           --out results/deployment_sim/<run_id> [--concurrency 4] [--sweep 1,2,4,8,16] [--sweep-episodes 400]

Three processes on localhost: the simulated banking API (bank_backend.py), the REM gateway (serve_gateway.py)
and this client, which replays all 3,334 recorded episodes of 21 real LLM agents (AgentDojo banking v1,
important_instructions + benign) through the gateway under B0, B1 and REM (step-level, no reviewer).

Measured: (1) parity of every episode outcome and every per-call verdict with the in-process replay of the
thesis (state/replay_main.pkl); (2) ASR / utility as in Section 4.6; (3) per-call REM time, backend time and
end-to-end latency; throughput under concurrency; (4) audit completeness and that no withheld call reached
the backend; (5) fail-closed responses to malformed / unknown requests.
NO-ADAPT assumption (recorded agents do not react to refusals). Simulated bank only; no real money or API.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import hashlib
import json
import os
import pickle
import platform
import random
import socket
import subprocess
import sys
import threading
import time

import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))

REPLAY_KEY = {"B0": "B0", "B1": "B1_step_level_no_reviewer", "REM": "REM_step_level_no_reviewer"}


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def wait_health(url, proc, timeout=900):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if proc.poll() is not None:
            raise RuntimeError(f"service exited early: {url}")
        try:
            if requests.get(url + "/health", timeout=2).ok:
                return
        except requests.RequestException:
            pass
        time.sleep(1)
    raise TimeoutError(url)


def pct(x, q):
    return float(np.percentile(x, q)) if len(x) else None


def run_batch(episodes, conf, base, suite, concurrency):
    from replay_client import run_remote
    local = threading.local()

    def job(ep):
        if not hasattr(local, "s"):
            local.s = requests.Session()
        return run_remote(ep, suite, base, conf, local.s)
    t0 = time.perf_counter()
    with cf.ThreadPoolExecutor(concurrency) as ex:
        out = list(ex.map(job, episodes))
    return out, time.perf_counter() - t0


def latency_stats(recs):
    batch = [t["batch_ms"] for r in recs for t in r["timings"]]
    rem = [x for r in recs for t in r["timings"] for x in t["rem_ms"]]
    back = [x for r in recs for t in r["timings"] for x in t["backend_ms"] if x > 0]
    wall = [r["wall_ms"] for r in recs]
    calls = sum(t["n_calls"] for r in recs for t in r["timings"])
    return {"calls": calls, "batches": len(batch),
            "batch_rtt_ms": {"median": pct(batch, 50), "p95": pct(batch, 95)},
            "rem_ms_per_call": {"median": pct(rem, 50), "p95": pct(rem, 95)},
            "backend_ms_per_executed_call": {"median": pct(back, 50), "p95": pct(back, 95)},
            "episode_wall_ms": {"median": pct(wall, 50), "p95": pct(wall, 95)}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--sweep", default="1,2,4,8,16")
    ap.add_argument("--sweep-episodes", type=int, default=400)
    ap.add_argument("--limit", type=int, default=0, help="debug: only the first N episodes")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    import common
    from agentdojo.task_suite.load_suites import get_suites
    from data import build

    suite = get_suites("v1")["banking"]
    data = build("primary")
    eids = sorted(data.episodes)
    if a.limit:
        eids = eids[: a.limit]
    episodes = [data.episodes[e] for e in eids]
    state = os.path.join(common.RESULTS, "state")
    agree = pickle.load(open(os.path.join(state, "rmod.pkl"), "rb"))["agree"]
    replay = pickle.load(open(os.path.join(state, "replay_main.pkl"), "rb"))
    ref = {(eid, c): (u, s, err, aud) for eid, c, u, s, err, aud in replay if c in REPLAY_KEY.values()}

    bp, gp = free_port(), free_port()
    env = dict(os.environ)
    logs = {n: open(os.path.join(a.out, f"{n}.log"), "w") for n in ("backend", "gateway")}
    backend = subprocess.Popen([sys.executable, os.path.join(HERE, "bank_backend.py"), "--port", str(bp)],
                               stdout=logs["backend"], stderr=subprocess.STDOUT, env=env)
    gateway = subprocess.Popen([sys.executable, os.path.join(HERE, "serve_gateway.py"), "--port", str(gp),
                                "--backend", f"http://127.0.0.1:{bp}"], stdout=logs["gateway"], stderr=subprocess.STDOUT, env=env)
    base = f"http://127.0.0.1:{gp}"
    results = {"configs": {}, "sweep": {}, "fail_closed_probes": {}}
    try:
        t0 = time.time()
        wait_health(f"http://127.0.0.1:{bp}", backend)
        wait_health(base, gateway)
        startup_s = time.time() - t0
        # ---------------- fail-closed probes (nothing may be executed) ----------------
        p = {}
        p["unknown_episode_calls"] = requests.post(f"{base}/v1/episodes/nope/calls", json={"calls": [
            {"id": "x", "function": "send_money", "args": {"recipient": "X", "amount": 1, "subject": "s", "date": "2022-01-01"}}]}).status_code
        p["malformed_json"] = requests.post(f"{base}/v1/episodes", data=b"{not json", headers={"Content-Type": "application/json"}).status_code
        p["unknown_configuration"] = requests.post(f"{base}/v1/episodes", json={"episode_id": "probe", "configuration": "NONE",
                                                   "user_task_id": "user_task_0"}).status_code
        p["backend_open_episodes_after_probes"] = requests.get(f"http://127.0.0.1:{bp}/health").json()["open_episodes"]
        results["fail_closed_probes"] = p
        # ---------------- main run: all episodes x B0, B1, REM ----------------
        all_recs = []
        for conf in ("B0", "B1", "REM"):
            recs, secs = run_batch(episodes, conf, base, suite, a.concurrency)
            all_recs += recs
            results["configs"][conf] = {"episodes": len(recs), "wall_s": secs, "episodes_per_s": len(recs) / secs,
                                        "errors": sum(1 for r in recs if r["error"]), "latency": latency_stats(recs)}
            print(conf, results["configs"][conf]["episodes_per_s"], "ep/s", flush=True)
        with open(os.path.join(a.out, "episodes.jsonl"), "w") as fh:
            for r in all_recs:
                slim = dict(r)
                slim["audit"] = [(x.get("label"), x.get("verdict"), x.get("released"), x.get("tier"), x.get("tool"),
                                  x.get("p")) for x in r["audit"]]
                fh.write(json.dumps(slim, default=str) + "\n")
        # ---------------- concurrency sweep (REM) ----------------
        rng = random.Random(20261105)
        sub = rng.sample(episodes, min(a.sweep_episodes, len(episodes)))
        for c in [int(x) for x in a.sweep.split(",") if x]:
            recs, secs = run_batch(sub, "REM", base, suite, c)
            results["sweep"][c] = {"episodes": len(recs), "wall_s": secs, "episodes_per_s": len(recs) / secs,
                                   "calls_per_s": sum(t["n_calls"] for r in recs for t in r["timings"]) / secs,
                                   "errors": sum(1 for r in recs if r["error"]), "latency": latency_stats(recs)}
            print("sweep", c, results["sweep"][c]["episodes_per_s"], flush=True)
        results["gateway_counters"] = requests.get(base + "/health").json()["counters"]
    finally:
        for proc in (gateway, backend):
            proc.terminate()
        for f in logs.values():
            f.close()

    # ---------------- parity with the in-process replay ----------------
    par = {}
    for conf in ("B0", "B1", "REM"):
        mism = collections.Counter()
        examples = []
        for r in (x for x in all_recs if x["configuration"] == conf):
            u, s, err, aud = ref[(r["episode_id"], REPLAY_KEY[conf])]
            mine = [(x.get("label"), x.get("verdict"), x.get("released"), x.get("tier"), x.get("tool")) for x in r["audit"]]
            theirs = [(t[0], t[1], t[2], t[3], t[4]) for t in aud]
            for k, ok in (("utility", r["utility"] == u), ("security", r["security"] == s),
                          ("error_status", (r["error"] is None) == (err is None)), ("verdict_sequence", mine == theirs)):
                if not ok:
                    mism[k] += 1
                    if len(examples) < 5:
                        examples.append({"episode": r["episode_id"], "field": k})
        par[conf] = {"episodes_compared": sum(1 for x in all_recs if x["configuration"] == conf),
                     "mismatches": dict(mism), "examples": examples}
    results["parity_with_offline_replay"] = par

    # ---------------- audit completeness and withheld-never-executed ----------------
    aud = collections.Counter()
    for r in all_recs:
        released = [x["tool"] for x in r["audit"] if x.get("released")]
        executed = [x["function"] for x in r["backend_executed"]]
        aud["episodes"] += 1
        aud["withheld_calls"] += sum(1 for x in r["audit"] if not x.get("released"))
        aud["released_calls"] += len(released)
        aud["backend_executed_calls"] += len(executed)
        if released != executed:
            aud["episodes_released_ne_executed"] += 1
    results["audit_checks"] = dict(aud)

    # ---------------- outcome metrics (valid episodes, as in Section 4.6) ----------------
    met = {}
    for conf in ("B0", "B1", "REM"):
        rs = [r for r in all_recs if r["configuration"] == conf and agree.get(r["episode_id"], False)]
        att = [r for r in rs if data.episodes[r["episode_id"]].attacked]
        ben = [r for r in rs if not data.episodes[r["episode_id"]].attacked]
        met[conf] = {"valid_episodes": len(rs), "ASR": float(np.mean([r["security"] for r in att])),
                     "utility_under_attack": float(np.mean([r["utility"] for r in att])),
                     "benign_utility": float(np.mean([r["utility"] for r in ben])),
                     "n_attacked": len(att), "n_benign": len(ben)}
    results["outcomes_valid_episodes"] = met
    commit = subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"], text=True).strip()
    import importlib.metadata as md
    results["manifest"] = {
        "status": "DEPLOYMENT SIMULATION - recorded real-agent traffic (NO-ADAPT); simulated bank; exploratory design values",
        "rem_commit": commit, "agentdojo": md.version("agentdojo"), "python": platform.python_version(),
        "cpu_count": os.cpu_count(), "platform": platform.platform(), "gateway_startup_s": startup_s,
        "concurrency_main": a.concurrency, "episodes": len(episodes),
        "crossfit_pkl_sha256": hashlib.sha256(open(os.path.join(state, "crossfit.pkl"), "rb").read()).hexdigest(),
        "replay_main_pkl_sha256": hashlib.sha256(open(os.path.join(state, "replay_main.pkl"), "rb").read()).hexdigest()}
    json.dump(results, open(os.path.join(a.out, "summary.json"), "w"), indent=1, default=str)
    print(json.dumps({k: results[k] for k in ("parity_with_offline_replay", "audit_checks", "outcomes_valid_episodes",
                                              "fail_closed_probes")}, indent=1, default=str))


if __name__ == "__main__":
    main()
