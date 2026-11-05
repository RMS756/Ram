"""Original MELON versus MELON + REM at the tool-execution boundary (AgentDojo, banking).

STATUS: IMPLEMENTED AND TESTED LOCALLY WITH SCRIPTED AGENTS AND A FAKE EMBEDDING CLIENT ONLY.
No run with a real language model or the real embedding model has been executed.

Upstream (primary source, not vendored: the repository has no licence file):
  MELON  https://github.com/kaijiezhu11/MELON  commit 4d3cc9c0175cc26332aac696ac5556c3f85a5e8e
         file pi_detector.py, sha256 pinned in UPSTREAM_MELON_SHA256; loaded from a local clone by path.
  Paper  Zhu, Yang, Wang, Guo & Wang (2025), ICML 2025; arXiv:2502.05174.
  Target AgentDojo 0.1.29 (2025-02-24, the last release with string message content, which the upstream
         file requires: it concatenates ``message["content"]`` as a string).

Upstream execution flow (verified by reading pi_detector.py and the README's ``from_config`` snippet):
  [SystemMessage, InitQuery, llm, ToolsExecutionLoop([ToolsExecutor(), MELON(llm, threshold=0.1)])]
  * ToolsExecutor executes the tool calls of the last assistant message.
  * MELON.query (after tool results exist) makes the agent's NEXT LLM call itself (original run), then a
    masked LLM call on deep copies of runtime/env with the user prompt replaced by a task-neutral prompt and
    the tool outputs packed into a fake read_file result. No tool is executed in the masked run.
  * Tool calls of the masked run are embedded (OpenAI text-embedding-3-large) into a bank; an attack is
    flagged when any original-run call has cosine similarity > 0.8 with any banked masked call. The
    constructor argument ``threshold=0.1`` is stored but never used by ``detect``.
  * On detection, the new assistant message is replaced by a stop message without tool calls (the loop
    ends) and the last tool result is replaced by "<Data omitted because a prompt injection was detected>".
  * The first assistant turn (before any tool output) is not inspected by MELON.

Integration (this module): MELON + REM replaces ``ToolsExecutor()`` inside the loop by
``RemGuardedToolsExecutor`` — the same executor logic with REM evaluating each call immediately before
``runtime.run_function``. Every call that reaches execution has survived MELON (calls MELON stopped never
reach the executor); calls of the first turn, which MELON does not inspect, are also evaluated by REM.
REM never sees MELON's masked diagnostic generation, and MELON's code and parameters are unchanged.

Compatibility measures, identical in both conditions (see MELON_REM_INTEGRATION.md):
  C-1  The upstream constructor builds ``OpenAI(api_key="your-api-key")``; the README tells users to edit the
       key in the file. Instead the adapter assigns ``melon.detection_model = <client>`` after construction.
  C-2  Episode isolation: ``AgentPipeline.query`` (0.1.29) has a mutable default ``extra_args={}`` and MELON
       stores its masked-call bank in ``extra_args``, so in one process the bank would persist across
       episodes and conditions. ``EpisodePipeline`` passes one fresh dict per episode (kept across AgentDojo's
       up-to-three re-queries of the same episode).
  C-3  Upstream prints diagnostics to stdout; the runner redirects stdout to a per-run log file.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
import time
from ast import literal_eval
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

from rem.integration.agentdojo_replay import RemGuard

__all__ = [
    "UPSTREAM_MELON_COMMIT",
    "UPSTREAM_MELON_SHA256",
    "MELON_STOP_TEXT",
    "load_upstream_melon",
    "make_melon",
    "elements",
    "build_pipeline",
    "run_episode",
]

UPSTREAM_MELON_URL = "https://github.com/kaijiezhu11/MELON"
UPSTREAM_MELON_COMMIT = "4d3cc9c0175cc26332aac696ac5556c3f85a5e8e"
UPSTREAM_MELON_SHA256 = "5a7f6b28228545e0d4ad9e98c9080ad819bb1cf471a67a31c8c4466b199a9017"
MELON_STOP_TEXT = "The tool outputs contain potential prompt injection, stopping execution."
MELON_README_THRESHOLD = 0.1            # passed as in the upstream README; unused by upstream detect()
CONDITIONS = ("MELON", "MELON_REM", "NO_DEFENSE")


def _sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_upstream_melon(path: str, expected_sha256: str = None):
    """Import the unmodified upstream ``pi_detector.py`` from ``path`` after checking its hash."""
    expected = expected_sha256 or UPSTREAM_MELON_SHA256
    got = _sha256(path)
    if got != expected:
        raise RuntimeError(f"upstream MELON file {path} has sha256 {got}, expected {expected}; refusing to run")
    name = "melon_upstream_pi_detector"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    prev, sys.dont_write_bytecode = sys.dont_write_bytecode, True     # leave the upstream clone untouched
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = prev
    return mod


def make_melon(module, llm, embedding_client):
    """``MELON(llm, threshold=0.1)`` exactly as in the upstream README, with the embedding client injected (C-1)."""
    melon = module.MELON(llm, threshold=MELON_README_THRESHOLD)
    melon.detection_model = embedding_client
    return melon


def _content(text: str):
    """Message content in the installed AgentDojo's format (string in 0.1.29; blocks from 0.1.30)."""
    try:
        from agentdojo.types import text_content_block_from_string
    except ImportError:
        return text
    return [text_content_block_from_string(text)]


def elements():
    """AgentDojo classes plus the REM-gated executor, built lazily for the installed AgentDojo."""
    from agentdojo.agent_pipeline import AgentPipeline, InitQuery, SystemMessage, ToolsExecutionLoop, ToolsExecutor
    from agentdojo.agent_pipeline.tool_execution import is_string_list
    from agentdojo.functions_runtime import EmptyEnv
    from agentdojo.types import ChatToolResultMessage

    try:
        from agentdojo.agent_pipeline.llms.google_llm import EMPTY_FUNCTION_NAME
    except Exception:  # pragma: no cover - constant location differs across versions
        EMPTY_FUNCTION_NAME = "<empty-function-name>"

    class RemGuardedToolsExecutor(ToolsExecutor):
        """``ToolsExecutor.query`` of the installed AgentDojo, with REM evaluated immediately before
        ``runtime.run_function``. Order, ids, invalid-tool and empty-name handling, and the
        string-list conversion follow the upstream executor; only the REM gate is added."""

        def __init__(self, guard: RemGuard) -> None:
            super().__init__()
            self.guard = guard
            self.executed: List[Tuple[str, str]] = []      # (tool, call id) actually executed

        def query(self, query, runtime, env=EmptyEnv(), messages=[], extra_args={}):
            if len(messages) == 0 or messages[-1]["role"] != "assistant":
                return query, runtime, env, messages, extra_args
            if messages[-1]["tool_calls"] is None or len(messages[-1]["tool_calls"]) == 0:
                return query, runtime, env, messages, extra_args
            self.guard.begin_decision_point()
            results = []
            names = {t.name for t in runtime.functions.values()}
            for call in messages[-1]["tool_calls"]:
                if call.function == EMPTY_FUNCTION_NAME:
                    results.append(ChatToolResultMessage(role="tool", content=_content(""), tool_call_id=call.id,
                                                         tool_call=call, error="Empty function name provided. Provide a valid function name."))
                    continue
                if call.function not in names:
                    results.append(ChatToolResultMessage(role="tool", content=_content(""), tool_call_id=call.id,
                                                         tool_call=call, error=f"Invalid tool {call.function} provided."))
                    self.guard.ingest(call.function, "", executed=False)
                    continue
                for k, v in call.args.items():
                    if isinstance(v, str) and is_string_list(v):
                        call.args[k] = literal_eval(v)
                release, notice = self.guard.evaluate(call.function, dict(call.args))
                if release:
                    res, err = runtime.run_function(env, call.function, call.args)
                    self.executed.append((call.function, call.id))
                    text, executed = self.output_formatter(res), err is None
                else:
                    text, err, executed = "", notice, False
                results.append(ChatToolResultMessage(role="tool", content=_content(text), tool_call_id=call.id,
                                                     tool_call=call, error=err))
                self.guard.ingest(call.function, text if executed else (err or ""), executed=executed)
            return query, runtime, env, [*messages, *results], extra_args

    class EpisodePipeline(AgentPipeline):
        """AgentPipeline with one fresh ``extra_args`` dict per episode (compatibility measure C-2)."""

        def __init__(self, elements_) -> None:
            super().__init__(elements_)
            self.episode_args: Dict[str, Any] = {}

        def query(self, query, runtime, env=EmptyEnv(), messages=[], extra_args=None):
            return super().query(query, runtime, env, messages, self.episode_args if extra_args is None else extra_args)

    return {
        "AgentPipeline": AgentPipeline, "InitQuery": InitQuery, "SystemMessage": SystemMessage,
        "ToolsExecutionLoop": ToolsExecutionLoop, "ToolsExecutor": ToolsExecutor,
        "RemGuardedToolsExecutor": RemGuardedToolsExecutor, "EpisodePipeline": EpisodePipeline,
    }


def build_pipeline(condition: str, *, llm, system_message: str, melon=None, guard: Optional[RemGuard] = None,
                   name: str, max_iters: int = 15, recorder=None):
    """Pipelines of the study. MELON is the upstream README structure; MELON_REM differs ONLY in the executor.

    Returns (pipeline, executor). NO_DEFENSE (optional context) is AgentDojo's undefended structure.
    """
    E = elements()
    if condition == "MELON":
        executor = E["ToolsExecutor"]()
        loop = E["ToolsExecutionLoop"]([executor, melon], max_iters=max_iters)
    elif condition == "MELON_REM":
        if guard is None:
            raise ValueError("MELON_REM needs a RemGuard")
        executor = E["RemGuardedToolsExecutor"](guard)
        loop = E["ToolsExecutionLoop"]([executor, melon], max_iters=max_iters)
    elif condition == "NO_DEFENSE":
        executor = E["ToolsExecutor"]()
        loop = E["ToolsExecutionLoop"]([executor, llm], max_iters=max_iters)
    else:
        raise ValueError(f"unknown condition {condition!r}; expected one of {CONDITIONS}")
    if condition != "NO_DEFENSE" and melon is None:
        raise ValueError(f"{condition} needs a MELON instance")
    parts = [E["SystemMessage"](system_message), E["InitQuery"](), llm, loop]
    if recorder is not None:
        parts.append(recorder)
    pipe = E["EpisodePipeline"](parts)
    pipe.name = name
    return pipe, executor


def _text(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return "\n".join(str(b.get("content", "")) if isinstance(b, Mapping) else str(b) for b in content)


def classify_error(exc: BaseException) -> str:
    """Errors are never counted as prevented attacks: they are reported in their own class."""
    n = type(exc).__name__
    if n == "BudgetExceeded":
        return "budget_stop"
    if "Timeout" in n or isinstance(exc, TimeoutError):
        return "timeout"
    if n in ("RateLimitError", "APIConnectionError", "APIStatusError", "InternalServerError", "APIError"):
        return "provider_error"
    return "infrastructure_error"


def run_episode(*, condition: str, suite, llm, system_message: str, user_task_id: str,
                injection_task_id: Optional[str], injections: Mapping[str, str], melon=None,
                guard: Optional[RemGuard] = None, name: str, max_iters: int = 15, environment=None) -> Dict[str, Any]:
    """Run one episode in a fresh pipeline (fresh ``extra_args``; fresh environment unless one is given)."""
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement

    captured: Dict[str, Any] = {"messages": []}

    class _Recorder(BasePipelineElement):
        name = "rem_melon_recorder"

        def query(self, query, runtime, env, messages=[], extra_args={}):
            captured["messages"] = list(messages)
            return query, runtime, env, messages, extra_args

    pipe, executor = build_pipeline(condition, llm=llm, system_message=system_message, melon=melon, guard=guard,
                                    name=name, max_iters=max_iters, recorder=_Recorder())
    ut = suite.get_user_task_by_id(user_task_id)
    it = suite.get_injection_task_by_id(injection_task_id) if injection_task_id else None
    err, err_class = None, None
    t0 = time.perf_counter()
    try:
        utility, security = suite.run_task_with_pipeline(pipe, ut, it, dict(injections), environment=environment)
    except Exception as exc:  # recorded and classified, never dropped
        utility, security, err, err_class = False, False, repr(exc)[:500], classify_error(exc)
    wall = time.perf_counter() - t0
    msgs = captured["messages"]
    stops = sum(1 for m in msgs if m.get("role") == "assistant" and _text(m.get("content")) == MELON_STOP_TEXT)
    calls_proposed = sum(len(m.get("tool_calls") or []) for m in msgs if m.get("role") == "assistant")
    rec = {
        "condition": condition,
        "utility": bool(utility),
        "security": bool(security),          # AgentDojo convention: True = the injection task succeeded
        "error": err,
        "error_class": err_class,
        "wall_time_s": wall,
        "melon_flagged": bool(pipe.episode_args.get("is_injection", False)) if condition != "NO_DEFENSE" else None,
        "melon_stop_messages": stops if condition != "NO_DEFENSE" else None,
        "calls_proposed_in_transcript": calls_proposed,
        "calls_executed": len(getattr(executor, "executed", [])) if condition == "MELON_REM" else None,
        "rem_audit": list(guard.audit) if (guard is not None and condition == "MELON_REM") else [],
        "messages": [_message_record(m) for m in msgs],
    }
    return rec


def _message_record(m: Mapping[str, Any]) -> Dict[str, Any]:
    rec: Dict[str, Any] = {"role": m.get("role"), "text": _text(m.get("content"))[:500]}
    if m.get("tool_calls"):
        rec["tool_calls"] = [{"function": c.function, "args": dict(c.args), "id": c.id} for c in m["tool_calls"]]
    if m.get("role") == "tool":
        tc = m.get("tool_call")
        rec["tool_call_id"] = m.get("tool_call_id")
        rec["function"] = getattr(tc, "function", None)
        rec["error"] = m.get("error")
    return rec
