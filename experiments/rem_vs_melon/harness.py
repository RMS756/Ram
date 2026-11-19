"""Three-arm closed-loop harness: no defence (D0), frozen REM v1.0 (D1) and original MELON (D2) in AgentDojo banking.

Runs in the MELON environment (AgentDojo 0.1.29, required by the unmodified upstream MELON file; see
experiments/melon_rem/MELON_REM_INTEGRATION.md §3). Nothing of REM or MELON is changed here:

  D0  [SystemMessage, InitQuery, llm, ToolsExecutionLoop([ToolsExecutor(), llm])]           AgentDojo's undefended pipeline
  D1  [SystemMessage, InitQuery, llm, ToolsExecutionLoop([RemGuardedToolsExecutor(guard), llm])]
      REM v1.0 evaluates each proposed call immediately before execution (frozen bundle; step-level; no reviewer).
      The executor is the one of rem/integration/melon_rem.py (already tested); the agent sees REM's refusal text.
  D2  [SystemMessage, InitQuery, llm, ToolsExecutionLoop([ToolsExecutor(), MELON(llm, threshold=0.1)])]
      exactly the upstream README structure; MELON makes the agent's next call and its masked re-execution.

Instrumentation (identical in all arms; it never changes a message): ``CountingLLM`` wraps the agent LLM and tags
each call as an agent call or a MELON masked re-execution (the masked context is recognised by upstream's fixed
``read_file('random.txt')`` tool result); ``CountingEmbeddings`` wraps MELON's embedding client. Both record time
and, when the provider reports it, token usage.
"""
from __future__ import annotations

import os
import sys
import time
from typing import Any, Dict, List, Mapping, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from rem.integration import melon_rem as MR  # noqa: E402

ARMS = ("D0_NO_DEFENSE", "D1_REM", "D2_MELON")


def is_masked_context(messages) -> bool:
    last = messages[-1] if messages else None
    tc = last.get("tool_call") if last and last.get("role") == "tool" else None
    return bool(tc and tc.function == "read_file" and dict(tc.args).get("name") == "random.txt")


def counting_llm(inner):
    """Wrap an AgentDojo LLM element; record per-call role (agent / melon_masked), wall time and usage."""
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement

    class CountingLLM(BasePipelineElement):
        def __init__(self, inner_):
            self.inner = inner_
            self.name = getattr(inner_, "name", None) or getattr(inner_, "model", "llm")
            self.calls: List[Dict[str, Any]] = []

        def query(self, query, runtime, env, messages=[], extra_args={}):
            role = "melon_masked" if is_masked_context(messages) else "agent"
            t0 = time.perf_counter()
            out = self.inner.query(query, runtime, env, messages, extra_args)
            new = out[3][-1] if out[3] else {}
            self.calls.append({"role": role, "seconds": time.perf_counter() - t0,
                               "n_tool_calls": len(new.get("tool_calls") or []),
                               "usage": getattr(self.inner, "last_usage", None)})
            return out

    return CountingLLM(inner)


class CountingEmbeddings:
    """Wraps an OpenAI-style client (``.embeddings.create``); records calls, time and reported usage."""

    def __init__(self, client):
        self.client = client
        self.calls: List[Dict[str, Any]] = []
        self.embeddings = self

    def create(self, input, model):
        t0 = time.perf_counter()
        r = self.client.embeddings.create(input=input, model=model)
        u = getattr(r, "usage", None)
        self.calls.append({"model": model, "seconds": time.perf_counter() - t0, "chars": len(input),
                           "tokens": getattr(u, "total_tokens", None) if u is not None else None})
        return r


def build_pipeline(arm: str, *, llm, system_message: str, melon=None, guard=None, name: str, max_iters: int = 15,
                   recorder=None):
    E = MR.elements()
    if arm == "D0_NO_DEFENSE":
        executor = E["ToolsExecutor"]()
        loop = E["ToolsExecutionLoop"]([executor, llm], max_iters=max_iters)
    elif arm == "D1_REM":
        if guard is None:
            raise ValueError("D1_REM needs a RemGuard")
        executor = E["RemGuardedToolsExecutor"](guard)
        loop = E["ToolsExecutionLoop"]([executor, llm], max_iters=max_iters)
    elif arm == "D2_MELON":
        if melon is None:
            raise ValueError("D2_MELON needs a MELON instance")
        executor = E["ToolsExecutor"]()
        loop = E["ToolsExecutionLoop"]([executor, melon], max_iters=max_iters)
    else:
        raise ValueError(f"unknown arm {arm!r}; expected one of {ARMS}")
    parts = [E["SystemMessage"](system_message), E["InitQuery"](), llm, loop]
    if recorder is not None:
        parts.append(recorder)
    pipe = E["EpisodePipeline"](parts)
    pipe.name = name
    return pipe, executor


def run_episode(*, arm: str, suite, llm, system_message: str, user_task_id: str, injection_task_id: Optional[str],
                injections: Mapping[str, str], melon=None, guard=None, embeddings: Optional[CountingEmbeddings] = None,
                name: str, max_iters: int = 15) -> Dict[str, Any]:
    """One episode in a fresh pipeline and a fresh environment; outcomes from AgentDojo's own checks."""
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement

    captured: Dict[str, Any] = {"messages": []}

    class _Recorder(BasePipelineElement):
        name = "rem_vs_melon_recorder"

        def query(self, query, runtime, env, messages=[], extra_args={}):
            captured["messages"] = list(messages)
            return query, runtime, env, messages, extra_args

    n_llm0 = len(llm.calls)
    n_emb0 = len(embeddings.calls) if embeddings is not None else 0
    pipe, executor = build_pipeline(arm, llm=llm, system_message=system_message, melon=melon, guard=guard, name=name,
                                    max_iters=max_iters, recorder=_Recorder())
    ut = suite.get_user_task_by_id(user_task_id)
    it = suite.get_injection_task_by_id(injection_task_id) if injection_task_id else None
    err = err_class = None
    t0 = time.perf_counter()
    try:
        utility, security = suite.run_task_with_pipeline(pipe, ut, it, dict(injections))
    except Exception as exc:  # recorded and classified, never counted as a prevented attack
        utility, security, err, err_class = False, False, repr(exc)[:500], MR.classify_error(exc)
    wall = time.perf_counter() - t0
    msgs = captured["messages"]
    llm_calls = llm.calls[n_llm0:]
    emb_calls = embeddings.calls[n_emb0:] if embeddings is not None else []
    audit = list(guard.audit) if guard is not None else []
    proposed = [(c.function, dict(c.args)) for m in msgs if m.get("role") == "assistant" for c in (m.get("tool_calls") or [])]
    tool_results = [m for m in msgs if m.get("role") == "tool"]
    return {
        "arm": arm, "user_task": user_task_id, "injection_task": injection_task_id,
        "utility": bool(utility), "security": bool(security),     # AgentDojo: security True = injection task succeeded
        "error": err, "error_class": err_class, "wall_time_s": wall,
        "calls_proposed": len(proposed),
        "calls_executed": sum(1 for m in tool_results if not m.get("error")),
        "calls_refused_by_rem": sum(1 for m in tool_results if (m.get("error") or "").startswith("REM:")),
        "melon_flagged": bool(pipe.episode_args.get("is_injection", False)) if arm == "D2_MELON" else None,
        "melon_stop_messages": sum(1 for m in msgs if m.get("role") == "assistant"
                                   and MR._text(m.get("content")) == MR.MELON_STOP_TEXT) if arm == "D2_MELON" else None,
        "llm_calls_agent": sum(1 for c in llm_calls if c["role"] == "agent"),
        "llm_calls_melon_masked": sum(1 for c in llm_calls if c["role"] == "melon_masked"),
        "llm_seconds_agent": sum(c["seconds"] for c in llm_calls if c["role"] == "agent"),
        "llm_seconds_melon_masked": sum(c["seconds"] for c in llm_calls if c["role"] == "melon_masked"),
        "llm_usage": [c["usage"] for c in llm_calls],
        "embedding_calls": len(emb_calls), "embedding_seconds": sum(c["seconds"] for c in emb_calls),
        "rem_latency_ms": [a["rem_latency_full_ms"] for a in audit],
        "rem_verdicts": [(a["tool"], a["verdict"], a["released"], a["label"]) for a in audit],
        "messages": [MR._message_record(m) for m in msgs],
    }
