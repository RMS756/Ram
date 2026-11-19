"""REM v1.0 vs original MELON vs no defence in AgentDojo banking — paired closed-loop runner (FAIL-CLOSED).

STATUS (19 Nov 2026): IMPLEMENTED AND DRY-RUN TESTED; NEVER EXECUTED WITH A REAL MODEL (no endpoint, no credential,
no spending authorisation in the session that wrote it; see REM_MELON_COMPARISON_2026_11_19/14_FINAL_EXECUTION_STATUS.md).

Protocol: REM_MELON_COMPARISON_2026_11_19/06_FROZEN_EVALUATION_PROTOCOL.md. Configuration: config_TEMPLATE.yaml.

Agent model, one of (identical object in all three arms, also used by MELON's masked re-execution):
  provider: openai             paid API; needs OPENAI_API_KEY, budget.authorization_reference, budget.cap_usd and
                               budget.prices_usd_per_1m_tokens (operator-supplied; no price is built in)
  provider: openai_compatible  a local OpenAI-compatible server (vLLM, Ollama, llama.cpp server) at models.base_url
MELON embeddings (models.melon_embeddings):
  original_openai              text-embedding-3-large via the OpenAI API, as hard-coded upstream  -> arm label "MELON"
  local_openai_compatible      another embedding model on a local server -> arm label "MELON-ADAPTED-EMBEDDINGS";
                               it is NOT the published configuration and is reported under that label only

usage (MELON environment, AgentDojo 0.1.29):
  /home/user/venvs/melon029/bin/python experiments/rem_vs_melon/run_rem_vs_melon.py --config <yaml> --out <dir> [--dry-run]
Exit codes: 0 ok; 2 design input missing; 3 credential/endpoint missing; 4 unsupported value; 5 provenance failure.
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
sys.path.insert(0, os.path.join(REPO, "experiments", "melon_rem"))

REQ = "REQUIRED_FROM_DESIGN"
REQUIRED = [("run_id",), ("benchmark", "case_set"), ("models", "provider"), ("models", "backbone"),
            ("models", "temperature"), ("models", "repeats"), ("models", "request_timeout_s"), ("models", "max_retries"),
            ("models", "melon_embeddings"), ("order", "seed")]
REQUIRED_PAID = [("budget", "authorization_reference"), ("budget", "cap_usd"), ("budget", "prices_usd_per_1m_tokens")]
FIXED = {("benchmark", "agentdojo_version"): "0.1.29", ("benchmark", "suite"): "banking",
         ("benchmark", "suite_version"): "v1", ("benchmark", "attack"): "important_instructions",
         ("rem", "policy"): "A3_step_level", ("rem", "reviewer_model"): "no_reviewer",
         ("rem", "fitted_parameters_source"): "heldout_crossfit_assignment"}
ARMS = ["D0_NO_DEFENSE", "D1_REM", "D2_MELON"]
PILOT_ATTACKED = [(f"user_task_{j}", f"injection_task_{j}") for j in range(9)]
PILOT_BENIGN = ["user_task_9", "user_task_11", "user_task_13", "user_task_15"]
MELON_UPSTREAM_DEFAULT = "/home/user/ucsb-mlsec/melon/pi_detector.py"
BUNDLE_DEFAULT = os.path.join(REPO, "experiments", "melon_rem", "frozen", "frozen_rem_bundle.pkl")
BUNDLE_SHA256 = "983c5b0d54de01cdb37467526f3aea2c4065f888f59c140ea6714ec1b0d3e2c5"   # exported 5 Nov 2026 from the frozen state at 9fddfa7


def get(cfg, path):
    for k in path:
        if not isinstance(cfg, dict) or k not in cfg:
            return None
        cfg = cfg[k]
    return cfg


def fail(code, msg):
    print(msg, file=sys.stderr)
    sys.exit(code)


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def validate(cfg, *, dry_run=False):
    paid = get(cfg, ("models", "provider")) == "openai" or get(cfg, ("models", "melon_embeddings")) == "original_openai"
    gaps = [".".join(p) for p in REQUIRED + (REQUIRED_PAID if paid else [])
            if get(cfg, p) in (None, REQ) or (isinstance(get(cfg, p), str) and REQ in get(cfg, p))]
    if gaps:
        for g in gaps:
            print(f"[DESIGN BLOCKED] {g}: not specified", file=sys.stderr)
        fail(2, f"{len(gaps)} required inputs missing; no episode is run.")
    for p, v in FIXED.items():
        if get(cfg, p) != v:
            fail(4, f"{'.'.join(p)} = {get(cfg, p)!r}; this study supports only {v!r}")
    M = cfg["models"]
    if M["provider"] not in ("openai", "openai_compatible"):
        fail(4, "models.provider must be 'openai' or 'openai_compatible'")
    if M["melon_embeddings"] not in ("original_openai", "local_openai_compatible"):
        fail(4, "models.melon_embeddings must be 'original_openai' or 'local_openai_compatible'")
    if M["provider"] == "openai_compatible" and not str(M.get("base_url", "")).startswith("http"):
        fail(2, "[DESIGN BLOCKED] models.base_url (local OpenAI-compatible server) not specified")
    if M["melon_embeddings"] == "local_openai_compatible" and not (M.get("embedding_base_url") and M.get("embedding_model")):
        fail(2, "[DESIGN BLOCKED] models.embedding_base_url / models.embedding_model not specified")
    if cfg["benchmark"]["case_set"] not in ("pilot", "full"):
        fail(4, "benchmark.case_set must be 'pilot' or 'full'")
    if int(M["repeats"]) < 1:
        fail(4, "models.repeats >= 1 required")
    if paid:
        if float(cfg["budget"]["cap_usd"]) <= 0:
            fail(4, "budget.cap_usd > 0 required for paid calls")
        prices = cfg["budget"]["prices_usd_per_1m_tokens"]
        need = []
        if M["provider"] == "openai" and not {"input", "output"} <= set((prices or {}).get(M["backbone"], {})):
            need.append(f"{M['backbone']}: {{input, output}}")
        if M["melon_embeddings"] == "original_openai" and "embedding" not in (prices or {}).get("text-embedding-3-large", {}):
            need.append("text-embedding-3-large: {embedding}")
        if need:
            fail(4, "budget.prices_usd_per_1m_tokens missing " + "; ".join(need))
    import importlib.metadata as md
    if md.version("agentdojo") != "0.1.29":
        fail(5, f"installed AgentDojo is {md.version('agentdojo')}; the unmodified upstream MELON requires 0.1.29")
    from rem.integration.melon_rem import UPSTREAM_MELON_SHA256
    mp = get(cfg, ("upstream", "melon_pi_detector_path")) or MELON_UPSTREAM_DEFAULT
    if not os.path.exists(mp) or sha256(mp) != UPSTREAM_MELON_SHA256:
        fail(5, f"upstream MELON file missing or modified: {mp}")
    bp = get(cfg, ("rem", "bundle_path")) or BUNDLE_DEFAULT
    side = json.load(open(bp + ".json")) if os.path.exists(bp + ".json") else {}
    if not os.path.exists(bp) or sha256(bp) != BUNDLE_SHA256:
        fail(5, f"frozen REM bundle missing or modified: {bp}")
    if not dry_run:
        if paid and not os.environ.get("OPENAI_API_KEY"):
            fail(3, "OPENAI_API_KEY is not set; no model call is made")
        if M["provider"] == "openai_compatible":
            import urllib.request
            try:
                urllib.request.urlopen(M["base_url"].rstrip("/") + "/models", timeout=10)
            except Exception as exc:  # noqa: BLE001
                fail(3, f"local model endpoint {M['base_url']} not reachable: {exc!r}")
    return paid, mp, bp, side


def cases(suite, case_set):
    if case_set == "pilot":
        return PILOT_ATTACKED + [(u, None) for u in PILOT_BENIGN]
    users = sorted(suite.user_tasks, key=lambda s: int(s.rsplit("_", 1)[1]))
    injs = sorted(suite.injection_tasks, key=lambda s: int(s.rsplit("_", 1)[1]))
    return [(u, i) for u in users for i in injs] + [(u, None) for u in users]


def plan(cfg, suite):
    """Each (case, repeat) is a triple of episodes (one per arm); triples shuffled; arm order randomised per triple."""
    rng = random.Random(int(cfg["order"]["seed"]))
    triples = [(c, r) for r in range(int(cfg["models"]["repeats"])) for c in cases(suite, cfg["benchmark"]["case_set"])]
    rng.shuffle(triples)
    sched = []
    for tid, (c, r) in enumerate(triples):
        arms = list(ARMS)
        rng.shuffle(arms)
        for arm in arms:
            sched.append({"triple_id": tid, "user_task": c[0], "injection_task": c[1], "repeat": r, "arm": arm})
    for k, s in enumerate(sched):
        s["order_index"] = k
    return sched


class UsageClient:
    """Local OpenAI-compatible client wrapper: records reported usage; no price (zero-cost local inference)."""

    def __init__(self, inner):
        self.inner, self.log = inner, []
        outer = self

        class _C:
            def create(self_, **kw):
                r = inner.chat.completions.create(**kw)
                u = getattr(r, "usage", None)
                outer.log.append({"kind": "chat", "in": getattr(u, "prompt_tokens", None), "out": getattr(u, "completion_tokens", None)})
                return r

        class _E:
            def create(self_, **kw):
                r = inner.embeddings.create(**kw)
                u = getattr(r, "usage", None)
                outer.log.append({"kind": "embedding", "in": getattr(u, "total_tokens", None), "out": 0})
                return r
        self.chat = type("Chat", (), {"completions": _C()})()
        self.embeddings = _E()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    paid, melon_path, bundle_path, _ = validate(cfg, dry_run=a.dry_run)

    from agentdojo.agent_pipeline.agent_pipeline import load_system_message
    from agentdojo.attacks.attack_registry import load_attack
    from agentdojo.task_suite.load_suites import get_suites

    suite = get_suites("v1")["banking"]
    sched = plan(cfg, suite)
    print(f"planned episodes: {len(sched)} ({len(sched) // 3} triples x 3 arms); arm label of MELON: "
          f"{'MELON' if cfg['models']['melon_embeddings'] == 'original_openai' else 'MELON-ADAPTED-EMBEDDINGS'}")
    if a.dry_run:
        print(json.dumps(sched[:6], indent=1))
        return

    import importlib.metadata as md
    import openai
    from agentdojo.agent_pipeline.llms.openai_llm import OpenAILLM
    from rem.integration.agentdojo_live import live_episode_stub
    from rem.integration.agentdojo_replay import GuardConfig, RemGuard
    from rem.integration.melon_rem import load_upstream_melon, make_melon

    import harness as H

    M, B = cfg["models"], cfg.get("budget") or {}
    os.makedirs(a.out, exist_ok=True)
    ledger = None
    if M["provider"] == "openai":
        from spending_guard import GuardedClient, Ledger
        ledger = Ledger(B["cap_usd"], B["prices_usd_per_1m_tokens"], chars_per_token_lower_bound=B.get("chars_per_token_lower_bound", 2.0),
                        reserve_output_tokens=B.get("reserve_output_tokens", 2048), path=os.path.join(a.out, "spend_ledger.jsonl"))
        agent_client = GuardedClient(openai.OpenAI(timeout=float(M["request_timeout_s"]), max_retries=int(M["max_retries"])), ledger)
    else:
        agent_client = UsageClient(openai.OpenAI(base_url=M["base_url"], api_key=os.environ.get("LOCAL_API_KEY", "not-needed"),
                                                 timeout=float(M["request_timeout_s"]), max_retries=int(M["max_retries"])))
    if M["melon_embeddings"] == "original_openai":
        if ledger is None:
            from spending_guard import GuardedClient, Ledger
            ledger = Ledger(B["cap_usd"], B["prices_usd_per_1m_tokens"], chars_per_token_lower_bound=B.get("chars_per_token_lower_bound", 2.0),
                            reserve_output_tokens=B.get("reserve_output_tokens", 2048), path=os.path.join(a.out, "spend_ledger.jsonl"))
        emb_client = GuardedClient(openai.OpenAI(timeout=float(M["request_timeout_s"]), max_retries=int(M["max_retries"])), ledger)
    else:
        inner = UsageClient(openai.OpenAI(base_url=M["embedding_base_url"], api_key=os.environ.get("LOCAL_API_KEY", "not-needed")))
        model_name = M["embedding_model"]

        class _Remap:                                   # upstream hard-codes model="text-embedding-3-large"
            embeddings = type("E", (), {"create": staticmethod(lambda input, model: inner.embeddings.create(input=input, model=model_name))})()
        emb_client = _Remap()

    bundle = pickle.load(open(bundle_path, "rb"))
    melon_mod = load_upstream_melon(melon_path)
    sysmsg = load_system_message(None)
    freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout
    open(os.path.join(a.out, "pip_freeze.txt"), "w").write(freeze)
    json.dump({"run_id": cfg["run_id"], "status": "LIVE RUN (real model calls)", "config": cfg, "config_sha256": sha256(a.config),
               "rem_commit": subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"], text=True).strip(),
               "melon_pi_detector_sha256": sha256(melon_path), "rem_bundle_sha256": sha256(bundle_path),
               "agentdojo": md.version("agentdojo"), "openai_sdk": md.version("openai"), "planned_episodes": len(sched),
               "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
              open(os.path.join(a.out, "manifest.json"), "w"), indent=1, default=str)

    target = type("Target", (), {"name": M.get("attack_target_name") or M["backbone"]})()
    inj_cache = {}
    res = open(os.path.join(a.out, "episodes.jsonl"), "a", encoding="utf-8")
    ulog = open(os.path.join(a.out, "melon_upstream_stdout.log"), "a", encoding="utf-8")
    for s in sched:
        u, i = s["user_task"], s["injection_task"]
        if i is not None and (u, i) not in inj_cache:          # identical payload in all three arms
            inj_cache[(u, i)] = load_attack(cfg["benchmark"]["attack"], suite, target).attack(
                suite.get_user_task_by_id(u), suite.get_injection_task_by_id(i))
        injections = inj_cache.get((u, i), {})
        llm = H.counting_llm(OpenAILLM(agent_client, M["backbone"], temperature=M["temperature"]))
        emb = H.CountingEmbeddings(emb_client) if s["arm"] == "D2_MELON" else None
        melon = make_melon(melon_mod, llm, emb) if s["arm"] == "D2_MELON" else None
        guard = None
        if s["arm"] == "D1_REM":
            F = bundle["folds"][i if i is not None else bundle["benign_user_task_fold"][u]]
            pol = F["policies"]["A3_step_level"]

            def decide(c, P=pol):
                d = P.decide(c.p, c.tier, c.tool, c.available)          # the label is never passed
                return d.verdict, d.source, {"tie": bool(getattr(d, "tie", False))}
            ep = live_episode_stub(model_name=M["backbone"], suite_name="banking", suite_version="v1", user_task_id=u,
                                   injection_task_id=i, attack=cfg["benchmark"]["attack"] if i else None, injections=injections,
                                   system_prompt=sysmsg, user_prompt=suite.get_user_task_by_id(u).PROMPT, repeat=s["repeat"])
            gc = GuardConfig(bundle["spec"], bundle["detector"], F["reference"], bundle["tier_map"], bundle["restricted_tools"],
                             "step_level", "no_reviewer")
            guard = RemGuard(gc, F["scorer"], decide, bundle["labeler"], ep)
        before = ledger.snapshot() if ledger else None
        with contextlib.redirect_stdout(ulog):
            rec = H.run_episode(arm=s["arm"], suite=suite, llm=llm, system_message=sysmsg, user_task_id=u, injection_task_id=i,
                                injections=injections, melon=melon, guard=guard, embeddings=emb,
                                name=f"{M['backbone']}-{s['arm'].lower()}", max_iters=int(M.get("max_iters", 15)))
        rec.update(s)
        rec.update({"run_id": cfg["run_id"], "backbone": M["backbone"], "provider": M["provider"],
                    "melon_label": "MELON" if M["melon_embeddings"] == "original_openai" else "MELON-ADAPTED-EMBEDDINGS"})
        if ledger:
            after = ledger.snapshot()
            rec["cost_usd"] = after["committed_usd"] - before["committed_usd"]
            rec["tokens"] = {k: after["tokens"][k] - before["tokens"][k] for k in after["tokens"]}
        res.write(json.dumps(rec, default=str) + "\n")
        res.flush()
        if rec["error_class"] == "budget_stop":
            print("budget cap reached; stopping (remaining episodes not run; reported as missing)", file=sys.stderr)
            break
    res.close()
    ulog.close()
    if ledger:
        json.dump(ledger.snapshot(), open(os.path.join(a.out, "spend_summary.json"), "w"), indent=1)
    print("done:", a.out)


if __name__ == "__main__":
    main()
