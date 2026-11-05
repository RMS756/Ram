"""MELON vs MELON + REM in AgentDojo banking — paired, interleaved runner (fail-closed).

STATUS: IMPLEMENTED; NEVER EXECUTED WITH A REAL MODEL. Paid calls require a completed configuration
including an explicit spending authorisation and cap (budget.*), and OPENAI_API_KEY in the environment.

usage (MELON environment: AgentDojo 0.1.29, see MELON_REM_EXPERIMENT_PROTOCOL.md):
  /home/user/venvs/melon029/bin/python experiments/melon_rem/run_melon_rem.py --config <yaml> --out <dir>
  ... --dry-run   validate everything and print the planned episodes; no model call, no credential needed

Exit codes: 0 done / dry run ok; 2 design input missing; 3 credential missing; 4 unsupported value;
5 provenance check failed (AgentDojo version, upstream MELON hash, REM bundle hash).
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import pickle
import random
import subprocess
import sys
import time

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, HERE)

REQ = "REQUIRED_FROM_DESIGN"
REQUIRED_KEYS = [
    ("run_id",), ("benchmark", "case_set"), ("models", "backbone"), ("models", "temperature"),
    ("models", "repeats"), ("models", "request_timeout_s"), ("models", "max_retries"),
    ("rem", "bundle_path"), ("rem", "bundle_sha256"), ("rem", "fitted_parameters_source"),
    ("budget", "authorization_reference"), ("budget", "cap_usd"), ("budget", "prices_usd_per_1m_tokens"),
    ("order", "seed"),
]
FIXED = {
    ("benchmark", "agentdojo_version"): "0.1.29", ("benchmark", "suite"): "banking",
    ("benchmark", "suite_version"): "v1", ("benchmark", "attack"): "important_instructions",
    ("models", "provider"): "openai", ("models", "embedding_model"): "text-embedding-3-large",
    ("rem", "policy"): "A3", ("rem", "costs_and_tiers"): "pilot_e0_exploratory",
    ("rem", "mitigation_semantics"): "step_level", ("rem", "reviewer_model"): "no_reviewer",
}
PILOT_ATTACKED = [(f"user_task_{j}", f"injection_task_{j}") for j in range(9)]
PILOT_BENIGN = ["user_task_9", "user_task_11", "user_task_13", "user_task_15"]


def get(cfg, path):
    for k in path:
        if not isinstance(cfg, dict) or k not in cfg:
            return None
        cfg = cfg[k]
    return cfg


def missing(cfg):
    out = []
    for p in REQUIRED_KEYS:
        v = get(cfg, p)
        if v is None or v == REQ or (isinstance(v, str) and REQ in v):
            out.append(".".join(p))
    return out


def fail(code, msg):
    print(msg, file=sys.stderr)
    sys.exit(code)


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def validate(cfg, *, dry_run=False):
    gaps = missing(cfg)
    if gaps:
        for g in gaps:
            print(f"[DESIGN BLOCKED] {g}: not specified", file=sys.stderr)
        fail(2, f"{len(gaps)} required inputs missing; no episode is run.")
    for p, v in FIXED.items():
        if get(cfg, p) != v:
            fail(4, f"{'.'.join(p)} = {get(cfg, p)!r}; this study supports only {v!r}")
    conds = cfg.get("conditions") or []
    if not {"MELON", "MELON_REM"} <= set(conds) or not set(conds) <= {"MELON", "MELON_REM", "NO_DEFENSE"}:
        fail(4, "conditions must contain MELON and MELON_REM (NO_DEFENSE optional)")
    if cfg["benchmark"]["case_set"] not in ("pilot", "full"):
        fail(4, "benchmark.case_set must be 'pilot' or 'full'")
    fps = str(cfg["rem"]["fitted_parameters_source"])
    if fps != "heldout_crossfit_assignment" and not fps.startswith("fold:"):
        fail(4, "rem.fitted_parameters_source must be 'heldout_crossfit_assignment' or 'fold:<id>'")
    if int(cfg["models"]["repeats"]) < 1 or float(cfg["budget"]["cap_usd"]) <= 0:
        fail(4, "models.repeats >= 1 and budget.cap_usd > 0 are required")
    prices = cfg["budget"]["prices_usd_per_1m_tokens"]
    b = cfg["models"]["backbone"]
    if not isinstance(prices, dict) or not {"input", "output"} <= set(prices.get(b, {})) \
            or "embedding" not in prices.get("text-embedding-3-large", {}):
        fail(4, f"budget.prices_usd_per_1m_tokens needs {b}: {{input, output}} and text-embedding-3-large: {{embedding}}")
    # provenance
    import importlib.metadata as md
    if md.version("agentdojo") != "0.1.29":
        fail(5, f"installed AgentDojo is {md.version('agentdojo')}; this study requires 0.1.29")
    from rem.integration.melon_rem import UPSTREAM_MELON_SHA256
    mp = cfg["upstream"]["melon_pi_detector_path"]
    if not os.path.exists(mp) or sha256(mp) != UPSTREAM_MELON_SHA256:
        fail(5, f"upstream MELON file missing or modified: {mp}")
    bp = cfg["rem"]["bundle_path"]
    if not os.path.exists(bp) or sha256(bp) != cfg["rem"]["bundle_sha256"]:
        fail(5, f"REM bundle missing or hash mismatch: {bp}")
    if not dry_run and not os.environ.get("OPENAI_API_KEY"):
        fail(3, "OPENAI_API_KEY is not set; no model call is made")


def cases(suite, case_set):
    if case_set == "pilot":
        return PILOT_ATTACKED + [(u, None) for u in PILOT_BENIGN]
    users = sorted(suite.user_tasks, key=lambda s: int(s.rsplit("_", 1)[1]))
    injs = sorted(suite.injection_tasks, key=lambda s: int(s.rsplit("_", 1)[1]))
    return [(u, i) for u in users for i in injs] + [(u, None) for u in users]


def fold_for(case, source, bundle):
    u, i = case
    if source.startswith("fold:"):
        return source.split(":", 1)[1]
    return i if i is not None else bundle["benign_user_task_fold"][u]


def plan(cfg, suite):
    """Paired schedule: each (case, repeat) is a pair; pairs shuffled; condition order randomised per pair."""
    rng = random.Random(int(cfg["order"]["seed"]))
    pairs = [(c, r) for r in range(int(cfg["models"]["repeats"])) for c in cases(suite, cfg["benchmark"]["case_set"])]
    rng.shuffle(pairs)
    sched = []
    for pid, (c, r) in enumerate(pairs):
        conds = list(cfg["conditions"])
        rng.shuffle(conds)
        for cond in conds:
            sched.append({"pair_id": pid, "user_task": c[0], "injection_task": c[1], "repeat": r, "condition": cond})
    for k, s in enumerate(sched):
        s["order_index"] = k
    return sched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    validate(cfg, dry_run=a.dry_run)

    from agentdojo.agent_pipeline.agent_pipeline import load_system_message
    from agentdojo.attacks.attack_registry import load_attack
    from agentdojo.task_suite.load_suites import get_suites

    suite = get_suites("v1")["banking"]
    sched = plan(cfg, suite)
    n_pairs = len({s["pair_id"] for s in sched})
    print(f"planned episodes: {len(sched)} ({n_pairs} pairs x {len(cfg['conditions'])} conditions); "
          f"each episode makes several model calls (agent turns, MELON masked re-executions, embeddings)")
    if a.dry_run:
        print(json.dumps(sched[:6], indent=1))
        return

    import openai
    from agentdojo.agent_pipeline.llms.openai_llm import OpenAILLM
    from rem.core.results import Verdict
    from rem.integration.agentdojo_live import live_episode_stub
    from rem.integration.agentdojo_replay import GuardConfig, RemGuard
    from rem.integration.melon_rem import load_upstream_melon, make_melon, run_episode
    from spending_guard import GuardedClient, Ledger

    os.makedirs(a.out, exist_ok=True)
    bundle = pickle.load(open(cfg["rem"]["bundle_path"], "rb"))
    B, M = cfg["budget"], cfg["models"]
    ledger = Ledger(B["cap_usd"], B["prices_usd_per_1m_tokens"], chars_per_token_lower_bound=B["chars_per_token_lower_bound"],
                    reserve_output_tokens=B["reserve_output_tokens"], path=os.path.join(a.out, "spend_ledger.jsonl"))
    client = GuardedClient(openai.OpenAI(timeout=float(M["request_timeout_s"]), max_retries=int(M["max_retries"])), ledger)
    melon_mod = load_upstream_melon(cfg["upstream"]["melon_pi_detector_path"])
    system_message = load_system_message(None)
    import importlib.metadata as md
    freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout
    manifest = {
        "run_id": cfg["run_id"], "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "LIVE RUN (real model calls)",
        "rem_commit": subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"], text=True).strip(),
        "rem_worktree_dirty": bool(subprocess.check_output(["git", "-C", REPO, "status", "--porcelain"], text=True).strip()),
        "config_sha256": sha256(a.config), "config": cfg,
        "melon": {"commit": cfg["upstream"]["melon_commit"], "pi_detector_sha256": sha256(cfg["upstream"]["melon_pi_detector_path"])},
        "agentdojo_version": md.version("agentdojo"), "openai_sdk_version": md.version("openai"),
        "pip_freeze_sha256": hashlib.sha256(freeze.encode()).hexdigest(),
        "rem_bundle_sha256": cfg["rem"]["bundle_sha256"], "rem_bundle_provenance": bundle["provenance"],
        "planned_episodes": len(sched),
    }
    open(os.path.join(a.out, "pip_freeze.txt"), "w").write(freeze)
    json.dump(manifest, open(os.path.join(a.out, "manifest.json"), "w"), indent=1, default=str)

    target = type("Target", (), {"name": M["backbone"]})()
    injections_cache = {}
    res_f = open(os.path.join(a.out, "episodes.jsonl"), "a", encoding="utf-8")
    upstream_log = open(os.path.join(a.out, "melon_upstream_stdout.log"), "a", encoding="utf-8")
    for s in sched:
        u, i = s["user_task"], s["injection_task"]
        if i is not None and (u, i) not in injections_cache:     # identical payload for both conditions
            injections_cache[(u, i)] = load_attack(cfg["benchmark"]["attack"], suite, target).attack(
                suite.get_user_task_by_id(u), suite.get_injection_task_by_id(i))
        injections = injections_cache.get((u, i), {})
        llm = OpenAILLM(client, M["backbone"], temperature=M["temperature"])
        melon = make_melon(melon_mod, llm, client) if s["condition"] != "NO_DEFENSE" else None
        guard, fold = None, None
        if s["condition"] == "MELON_REM":
            fold = fold_for((u, i), str(cfg["rem"]["fitted_parameters_source"]), bundle)
            F = bundle["folds"][fold]
            pol = F["policies"]["A3_step_level"]

            def decide(c, P=pol):
                d = P.decide(c.p, c.tier, c.tool, c.available)     # the label is never passed
                return d.verdict, d.source, {"tie": bool(getattr(d, "tie", False)), "risks": dict(getattr(d, "risks", {}) or {})}
            ep = live_episode_stub(model_name=M["backbone"], suite_name="banking", suite_version="v1", user_task_id=u,
                                   injection_task_id=i, attack=cfg["benchmark"]["attack"] if i else None,
                                   injections=injections, system_prompt=system_message,
                                   user_prompt=suite.get_user_task_by_id(u).PROMPT, repeat=s["repeat"])
            gc = GuardConfig(bundle["spec"], bundle["detector"], F["reference"], bundle["tier_map"],
                             bundle["restricted_tools"], "step_level", "no_reviewer")
            guard = RemGuard(gc, F["scorer"], decide, bundle["labeler"], ep)
        before = ledger.snapshot()
        with contextlib.redirect_stdout(upstream_log):
            rec = run_episode(condition=s["condition"], suite=suite, llm=llm, system_message=system_message,
                              user_task_id=u, injection_task_id=i, injections=injections, melon=melon, guard=guard,
                              name=f"{M['backbone']}-{s['condition'].lower()}", max_iters=int(M["max_iters"]))
        after = ledger.snapshot()
        rec.update(s)
        rec.update({"run_id": cfg["run_id"], "attack": cfg["benchmark"]["attack"] if i else None,
                    "backbone": M["backbone"], "rem_fold": fold,
                    "cost_usd": after["committed_usd"] - before["committed_usd"],
                    "tokens": {k: after["tokens"][k] - before["tokens"][k] for k in after["tokens"]},
                    "model_calls": after["calls"] - before["calls"]})
        res_f.write(json.dumps(rec, default=str) + "\n")
        res_f.flush()
        if rec["error_class"] == "budget_stop":
            print("budget cap reached; stopping the run (remaining episodes not run)", file=sys.stderr)
            break
    res_f.close()
    upstream_log.close()
    json.dump(ledger.snapshot(), open(os.path.join(a.out, "spend_summary.json"), "w"), indent=1)
    print("done:", a.out)


if __name__ == "__main__":
    main()
