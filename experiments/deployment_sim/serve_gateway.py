"""Start the REM deployment gateway with the frozen REM components (no refitting).

usage: PILOT_RESULTS_DIR=<frozen pilot state> python3 experiments/deployment_sim/serve_gateway.py \
           --port 8700 --backend http://127.0.0.1:8701

Components are built exactly as in the recorded-trace replay (experiments/pilot/run_main.py, stage_replay):
frozen cross-fit fits and r_mod -> build_policies; scorer_of(fold fit, FEATURE_ORDER); benign reference of the
fold's fitting portion; setup (evidence spec, detector, tier map, restricted tools, labeler) from
configs/exploratory/pilot_e0.yaml. Fold per episode = the held-out cross-fit assignment (attacked: its
injection task; benign: round-robin fold of the user task) - the same assignment the replay used.

Configurations served (mitigation semantics step_level; reviewer model no_reviewer):
  B0   allow-all (REM disabled; latency and outcome reference)
  B1   consequence-independent operating-point baseline on the same estimator
  REM  A3 expected-loss verdict
EXPLORATORY design values (pilot_e0, not supervisor-approved).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))

import common  # noqa: E402
import run_main as rm  # noqa: E402
from data import build, reference_from_mask  # noqa: E402
from rem.algorithms.behavior.evidence import FEATURE_ORDER  # noqa: E402
from rem.core.results import Verdict  # noqa: E402
from rem.deployment.gateway import RemGateway, serve  # noqa: E402
from rem.evaluation.crossfit import assign_round_robin  # noqa: E402
from rem.integration.agentdojo_replay import GuardConfig, RemGuard  # noqa: E402
from rem.integration.agentdojo_traces import Episode, Message  # noqa: E402

CONFIGS = ("B0", "B1", "REM")
VARIANT, REVIEWER = "step_level", "no_reviewer"


def sha256(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def build_provider():
    state = os.path.join(common.RESULTS, "state")
    fits = pickle.load(open(os.path.join(state, "crossfit.pkl"), "rb"))
    rmod = pickle.load(open(os.path.join(state, "rmod.pkl"), "rb"))["rmod"]
    pol = rm.build_policies(fits, rmod)
    st = common.make_setup()
    data = build("primary")
    folds = sorted(set(data.fold.tolist()), key=str)
    refs = {f: reference_from_mask(data, data.fold != f) for f in folds}
    scorers = {f: rm.scorer_of(fits["label_nll_primary"].fits[f], FEATURE_ORDER) for f in folds}
    inj = sorted({e.injection_task_id for e in data.episodes.values() if e.injection_task_id}, key=str)
    users = sorted({e.user_task_id for e in data.episodes.values()}, key=str)
    rr = assign_round_robin(users, len(inj))
    benign_fold = {u: inj[rr[u]] for u in users}
    tool_names = {t.name for t in st.suite.tools}

    def decider(conf, f):
        if conf == "B0":
            return lambda c: (Verdict.ALLOW, "allow_all", {})
        P = pol[f]["B1" if conf == "B1" else f"A3_{VARIANT}"]

        def decide(c):
            d = P.decide(c.p, c.tier, c.tool, c.available)                 # the label is never passed
            return d.verdict, d.source, {"tie": bool(getattr(d, "tie", False)), "risks": dict(getattr(d, "risks", {}) or {})}
        return decide

    def provider(meta):
        conf = meta["configuration"]
        if conf not in CONFIGS:
            raise ValueError(f"unknown configuration {conf!r}")
        f = meta.get("injection_task_id") or benign_fold[meta["user_task_id"]]
        ep = Episode(path=f"deploy://{meta['episode_id']}", pipeline=meta["pipeline"], suite="banking",
                     user_task_id=meta["user_task_id"], injection_task_id=meta.get("injection_task_id"),
                     attack_type=meta.get("attack_type"), injections=dict(meta.get("injections") or {}),
                     messages=(Message("system", meta["system_prompt"]), Message("user", meta["user_prompt"])),
                     utility=False, security=False, error=None, benchmark_version="v1")
        gc = GuardConfig(st.spec, st.detector, refs[f], st.tier_map, st.restricted, VARIANT, REVIEWER)
        g = RemGuard(gc, None if conf == "B0" else scorers[f], decider(conf, f), st.labeler, ep)
        return g, tool_names

    prov = {"crossfit_pkl_sha256": sha256(os.path.join(state, "crossfit.pkl")),
            "rmod_pkl_sha256": sha256(os.path.join(state, "rmod.pkl")),
            "pilot_config_sha256": sha256(os.path.join(REPO, "configs", "exploratory", "pilot_e0.yaml")),
            "variant": VARIANT, "reviewer": REVIEWER, "configurations": list(CONFIGS)}
    return provider, prov


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--backend", required=True)
    a = ap.parse_args()
    provider, prov = build_provider()
    srv = serve(RemGateway(provider, a.backend), port=a.port)
    print("gateway ready " + json.dumps(prov), flush=True)
    srv.serve_forever()
