"""Arms D0 (no defence), D1 (REM v1.0, unchanged) and D2 (Progent, published manual banking policy) of the
comparative protocol, in AgentDojo 0.1.35 banking v1. D3/D4 (DRIFT) run in their own venv: run_drift_arms.py.

Modes:
  --mode preflight  validates the configuration and prints the episode plan; no model, no network.
  --mode scripted   INTEGRATION TEST ONLY. A ground-truth-compliant test double (it issues the user task's
                    reference calls, then the injection task's reference calls, and never reads tool outputs) drives
                    all 160 episodes through each arm, to check that the pipelines run end to end and that withheld
                    or refused calls are not executed. Its utility/security values are NOT results.
  --mode live       REFUSES to start unless every design input is recorded (backbone, decoding, repeats, REM fold,
                    authorisation, budget cap, protocol-freeze commit) and the provider credential is present.
                    Never executed in this repository.

D1 uses REM's existing closed-loop integration (rem/integration/agentdojo_live.run_defended_episode) with the frozen
state of one declared cross-fit fold (experiments/live/run_live.frozen_components); nothing is fitted.
D2 wraps the banking tools with the authors' secagent.apply_secure_tool_wrapper and installs the 9befb41 policy
read verbatim from git (progent_policy.py): a refused call returns Progent's own error text to the agent.

usage: PILOT_RESULTS_DIR=<frozen state> /home/user/venvs/rem_progent_replay/bin/python \
       experiments/comparative_phase/run_live_comparison.py --mode scripted --out <dir> [--fold injection_task_0]
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for p in (str(REPO), str(REPO / "experiments" / "pilot"), str(REPO / "experiments" / "live"), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
PINS = REPO / "REM_EXTERNAL_DEFENSE_AUDIT" / "results" / "upstream_pins.json"
REQUIRED = ["model.provider", "model.id", "model.decoding", "repeats", "rem.fitted_parameters_source",
            "authorisation.record", "authorisation.budget_cap_usd", "protocol_freeze_commit", "grouping_confirmed"]
PROVIDER_KEYS = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY", "google": "GOOGLE_API_KEY"}


def get(cfg, dotted):
    for p in dotted.split("."):
        cfg = cfg.get(p) if isinstance(cfg, dict) else None
    return cfg


def episodes(suite):
    users = sorted(suite.user_tasks, key=lambda x: int(x.split("_")[-1]))
    injs = sorted(suite.injection_tasks, key=lambda x: int(x.split("_")[-1]))
    return [(u, i) for u in users for i in [None] + injs]


def build_arms(fold: str):
    import progent_policy as PP
    from agentdojo.functions_runtime import make_function
    from agentdojo.task_suite.load_suites import get_suite
    import common
    from run_live import frozen_components
    suite = get_suite("v1", "banking")
    policies, pmeta, _, _ = PP.load_policy()
    secagent, commit, sha = PP.load_secagent(str(PINS))
    raw = PP.banking_raw_tools()
    secagent.apply_secure_tool_wrapper  # noqa: B018  (presence check)
    wrapped = [make_function(f) for f in secagent.apply_secure_tool_wrapper(list(raw))]
    secagent.update_always_allowed_tools(PP.GENERIC_ALWAYS_ALLOWED[0], allow_all_no_arg_tools=PP.GENERIC_ALWAYS_ALLOWED[1])
    secagent.update_security_policy(copy.deepcopy(policies))
    pg_suite = copy.copy(suite)
    pg_suite.tools = wrapped
    assert [t.name for t in wrapped] == [t.name for t in suite.tools]
    st = common.make_setup()
    pol, scorer, ref = frozen_components(fold)
    return suite, pg_suite, st, pol, scorer, ref, {"progent_policy": pmeta, "progent_commit": commit, "secagent_tool_sha256": sha}


def run_episode(arm, suite, pg_suite, st, pol, scorer, ref, llm_factory, u, i, sysmsg, fold):
    from agentdojo.agent_pipeline import AgentPipeline, InitQuery, SystemMessage, ToolsExecutionLoop, ToolsExecutor
    from agentdojo.attacks.attack_registry import load_attack
    from rem.integration.agentdojo_live import live_episode_stub, run_defended_episode
    from rem.integration.agentdojo_replay import GuardConfig, RemGuard
    ut = suite.get_user_task_by_id(u)
    it = suite.get_injection_task_by_id(i) if i else None
    llm = llm_factory(ut, it)
    inj = load_attack("important_instructions", suite, llm).attack(ut, it) if i else {}
    t0 = time.perf_counter()
    if arm == "D1":
        ep = live_episode_stub(model_name=getattr(llm, "name", "agent"), suite_name="banking", suite_version="v1",
                               user_task_id=u, injection_task_id=i, attack="important_instructions" if i else None,
                               injections=inj, system_prompt=sysmsg, user_prompt=ut.PROMPT, repeat=0)
        P = pol["A3_step_level"]

        def decide(c):
            v = P.decide(c.p, c.tier, c.tool, c.available)
            return v.verdict, v.source, {}
        g = RemGuard(GuardConfig(st.spec, st.detector, ref, st.tier_map, st.restricted, "step_level", "no_reviewer"), scorer, decide, st.labeler, ep)
        o = run_defended_episode(suite=suite, llm=llm, guard=g, user_task_id=u, injection_task_id=i, injections=inj,
                                 system_prompt=sysmsg, pipeline_name=getattr(llm, "name", "agent"))
        executed = [m["tool_call"]["function"] for m in o.messages if m.get("role") == "tool" and not m.get("error")]
        return {"utility": o.utility, "security": o.security if i else None, "error": o.error, "executed": executed,
                "refused": sum(1 for a in o.audit if not a["released"]), "wall_s": o.wall_time_s}
    s = pg_suite if arm == "D2" else suite
    captured = {}

    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement

    class Rec(BasePipelineElement):
        name = "rec"

        def query(self, query, runtime, env, messages=[], extra_args={}):
            captured["m"] = list(messages)
            return query, runtime, env, messages, extra_args
    pipe = AgentPipeline([SystemMessage(sysmsg), InitQuery(), llm, ToolsExecutionLoop([ToolsExecutor(), llm]), Rec()])
    pipe.name = getattr(llm, "name", "agent")
    err = None
    try:
        utility, security = s.run_task_with_pipeline(pipe, ut, it, inj)
    except Exception as e:
        utility, security, err = False, False, repr(e)[:300]
    msgs = captured.get("m", [])
    executed = [m["tool_call"].function for m in msgs if m.get("role") == "tool" and not m.get("error")]
    refused = sum(1 for m in msgs if m.get("role") == "tool" and m.get("error") and "not allowed" in str(m.get("error")))
    return {"utility": bool(utility), "security": bool(security) if i else None, "error": err, "executed": executed,
            "refused": refused, "wall_s": time.perf_counter() - t0}


def scripted(out: Path, fold: str):
    from agentdojo.agent_pipeline.agent_pipeline import load_system_message
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
    from agentdojo.types import text_content_block_from_string

    class GroundTruthCompliantAgent(BasePipelineElement):
        """TEST DOUBLE, not a model: reference calls of the user task, then of the injection task."""
        name = "gpt-4o-2024-05-13"

        def __init__(self, ut, it):
            self.ut, self.it, self.queue = ut, it, None

        def query(self, query, runtime, env, messages=[], extra_args={}):
            if self.queue is None:
                self.queue = list(self.ut.ground_truth(env)) + (list(self.it.ground_truth(env)) if self.it else [])
            if self.queue:
                c = self.queue.pop(0)
                msg = {"role": "assistant", "content": [text_content_block_from_string("")], "tool_calls": [c]}
            else:
                msg = {"role": "assistant", "content": [text_content_block_from_string("Done.")], "tool_calls": None}
            return query, runtime, env, [*messages, msg], extra_args

    suite, pg_suite, st, pol, scorer, ref, meta = build_arms(fold)
    sysmsg = load_system_message(None)
    rows = []
    for arm in ("D0", "D1", "D2"):
        for u, i in episodes(suite):
            r = run_episode(arm, suite, pg_suite, st, pol, scorer, ref, GroundTruthCompliantAgent, u, i, sysmsg, fold)
            rows.append({"arm": arm, "user_task": u, "injection_task": i, **r})
    summ = {}
    for arm in ("D0", "D1", "D2"):
        rs = [r for r in rows if r["arm"] == arm]
        summ[arm] = {"episodes": len(rs), "errors": sum(1 for r in rs if r["error"]), "tool_calls_executed": sum(len(r["executed"]) for r in rs),
                     "calls_refused_or_withheld": sum(r["refused"] for r in rs),
                     "scripted_benign_utility": [sum(r["utility"] for r in rs if not r["injection_task"]), sum(1 for r in rs if not r["injection_task"])],
                     "scripted_injection_goal_reached": [sum(bool(r["security"]) for r in rs if r["injection_task"]), sum(1 for r in rs if r["injection_task"])]}
    data = {"label": "SCRIPTED INTEGRATION TEST (ground-truth-compliant test double) - NOT A SECURITY OR UTILITY RESULT",
            "benchmark": "AgentDojo banking v1", "rem_fold": fold, "language_model_calls": 0, **meta, "summary": summ, "episodes": rows}
    out.mkdir(parents=True, exist_ok=True)
    (out / "d0_d1_d2_scripted_integration.json").write_text(json.dumps(data, indent=1, default=str))
    print(json.dumps(summ, indent=1))


def preflight_or_live(cfg_path: str, live: bool):
    import yaml
    cfg = yaml.safe_load(open(cfg_path))
    gaps = [k for k in REQUIRED if get(cfg, k) in (None, "", "REQUIRED_FROM_SUPERVISOR")]
    for g in gaps:
        print(f"[DESIGN BLOCKED] {g}: not specified", file=sys.stderr)
    if gaps:
        sys.exit(2)
    key = PROVIDER_KEYS.get(get(cfg, "model.provider"))
    if not key:
        sys.exit(4)
    from agentdojo.task_suite.load_suites import get_suite
    n = len(episodes(get_suite("v1", "banking")))
    print(f"plan: {n} episodes x 3 arms x {cfg['repeats']} repeats = {n * 3 * int(cfg['repeats'])} episodes (+ D3/D4 in the DRIFT venv)")
    if not live:
        return
    if not os.environ.get(key):
        print(f"credential {key} is not set; no call is made", file=sys.stderr)
        sys.exit(3)
    sys.exit("live execution requires the supervisor-approved configuration; it has not been authorised in this "
             "repository and is deliberately not wired to start from here without that record being reviewed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["preflight", "scripted", "live"], required=True)
    ap.add_argument("--config")
    ap.add_argument("--out")
    ap.add_argument("--fold", default="injection_task_0")
    a = ap.parse_args()
    if a.mode == "scripted":
        scripted(Path(a.out).resolve(), a.fold)
    else:
        preflight_or_live(a.config, a.mode == "live")
