"""Agent-side client of the deployment simulation: replays a RECORDED real-agent episode over HTTP.

The agent framework is AgentDojo's own pipeline with the recorded assistant turns (ReplayLLM, as in the
offline replay). The only difference from the offline replay is the tool executor: ``RemoteExecutor``
sends each assistant turn's calls to the REM gateway and receives tool results or refusals; it never
touches an environment. The outer loop reproduces TaskSuite.run_task_with_pipeline (prompt = the user
task's PROMPT; up to three queries until the last assistant message has content).

NO-ADAPT assumption: the recorded agent does not react to refusals (its later turns are replayed as
recorded), exactly as in the thesis's replay analysis (Section 4.6). This simulation adds deployment
evidence (separate services, network boundary, concurrency, audit completeness, fail-closed behaviour),
not evidence about adaptive agents.
"""
from __future__ import annotations

import time
from ast import literal_eval
from urllib.parse import quote
from typing import Any, Dict

import requests
from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
from agentdojo.agent_pipeline.tool_execution import is_string_list
from agentdojo.functions_runtime import EmptyEnv, FunctionsRuntime
from agentdojo.types import ChatToolResultMessage, text_content_block_from_string

from rem.integration.agentdojo_replay import _agentdojo_elements


class RemoteExecutor(BasePipelineElement):
    name = "rem_remote_executor"

    def __init__(self, session: requests.Session, base: str, sid: str, timings: list) -> None:
        self.s, self.base, self.sid, self.timings = session, base, sid, timings

    def query(self, query, runtime, env=EmptyEnv(), messages=[], extra_args={}):
        if not messages or messages[-1]["role"] != "assistant" or not messages[-1]["tool_calls"]:
            return query, runtime, env, messages, extra_args
        calls = messages[-1]["tool_calls"]
        for c in calls:                                   # AgentDojo executor normalisation (in place, as offline)
            for k, v in c.args.items():
                if isinstance(v, str) and is_string_list(v):
                    c.args[k] = literal_eval(v)
        t0 = time.perf_counter()
        r = self.s.post(f"{self.base}/v1/episodes/{quote(self.sid, safe='')}/calls",
                        json={"calls": [{"id": c.id, "function": c.function, "args": c.args} for c in calls]}, timeout=60)
        r.raise_for_status()
        rtt = (time.perf_counter() - t0) * 1e3
        res = r.json()["results"]
        self.timings.append({"batch_ms": rtt, "n_calls": len(calls),
                             "rem_ms": [x["rem_ms"] for x in res], "backend_ms": [x["backend_ms"] for x in res]})
        out = [ChatToolResultMessage(role="tool", content=[text_content_block_from_string(x["content"])],
                                     tool_call_id=c.id, tool_call=c, error=x["error"]) for c, x in zip(calls, res)]
        return query, runtime, env, [*messages, *out], extra_args


def run_remote(ep, suite, base: str, configuration: str, session: requests.Session) -> Dict[str, Any]:
    AgentPipeline, SystemMessage, InitQuery, ToolsExecutionLoop, ReplayLLM, _ = _agentdojo_elements()
    sid = f"{configuration}::{ep.episode_id}"
    timings: list = []
    t0 = time.perf_counter()
    err = None
    utility = security = False
    audit, executed = [], []
    try:
        session.post(f"{base}/v1/episodes", json={
            "episode_id": sid, "configuration": configuration, "pipeline": ep.pipeline,
            "user_task_id": ep.user_task_id, "injection_task_id": ep.injection_task_id, "attack_type": ep.attack_type,
            "injections": dict(ep.injections), "system_prompt": ep.system_prompt, "user_prompt": ep.objective},
            timeout=60).raise_for_status()
        llm = ReplayLLM(ep)
        pipe = AgentPipeline([SystemMessage(ep.system_prompt), InitQuery(), llm,
                              ToolsExecutionLoop([RemoteExecutor(session, base, sid, timings), llm])])
        pipe.name = "rem_deploy_replay"
        prompt = suite.get_user_task_by_id(ep.user_task_id).PROMPT
        runtime = FunctionsRuntime(suite.tools)
        messages, model_output = [], None
        for _ in range(3):
            _, _, _, messages, _ = pipe.query(prompt, runtime, EmptyEnv())
            if messages[-1]["role"] != "assistant":
                raise ValueError("Last message was not an assistant message")
            model_output = messages[-1]["content"]
            if model_output is not None:
                break
        fcalls = [{"function": c.function, "args": c.args, "id": c.id}
                  for m in messages if m["role"] == "assistant" for c in (m["tool_calls"] or [])]
        r = session.post(f"{base}/v1/episodes/{quote(sid, safe='')}/close", json={"model_output": model_output or [], "function_calls": fcalls},
                         timeout=60)
        r.raise_for_status()
        j = r.json()
        utility, security, audit, executed = j["utility"], j["security"], j["audit"], j["backend_executed"]
    except Exception as exc:
        err = repr(exc)[:300]
    return {"episode_id": ep.episode_id, "configuration": configuration, "utility": bool(utility),
            "security": bool(security), "error": err, "wall_ms": (time.perf_counter() - t0) * 1e3,
            "timings": timings, "audit": audit, "backend_executed": executed}
