"""Closed-loop (live-agent) REM integration with AgentDojo.

STATUS: IMPLEMENTED AND TESTED WITH SCRIPTED TEST AGENTS ONLY. No run with a real language model
has been executed from this repository (no API credential and no approved backbone; D-15).

What this module adds to the replay harness (``rem.integration.agentdojo_replay``):
the recorded-trace ``ReplayLLM`` is replaced by any AgentDojo LLM pipeline element, so the agent
receives REM's refusal notices and may continue, retry, replan or stop. Everything REM decides is
unchanged: the same ``RemGuard`` (features, frozen scorer, decision function, mitigation semantics,
audit record, timers) and the same ``GuardedToolsExecutor`` sit at the tool-execution boundary and
evaluate each proposed call BEFORE ``runtime.run_function`` is called.

Nothing here fits, tunes or changes a parameter. Design inputs (backbone, decoding, repeats, fitted
parameter source, costs, semantics, reviewer model) are supplied by the caller; the runner
``experiments/live/run_live.py`` refuses to start while any is undecided (fail-closed).

Interpretation notes (stated, not chosen silently):
L-1  ``suite.run_task_with_pipeline`` re-queries the pipeline up to three times when the agent ends
     without a final text answer (AgentDojo 0.1.35 behaviour). The same guard, and therefore the same
     episode history, is used across these re-queries; they belong to one episode.
L-2  Adaptation statistics are counted from REM's own audit record (proposals in order):
       retry      a later proposal of the same tool with the same argument digest as a withheld call;
       replan     a later proposal of a *different* restricted tool after a withheld call;
       post-refusal release of a y=1 call   a reference-labelled attack call released after an
                  earlier withheld call in the same episode.
     These are descriptive counts of observed behaviour, not causal attributions.
"""

from __future__ import annotations

import time
from itertools import groupby
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from rem.integration.agentdojo_replay import RemGuard, _agentdojo_elements
from rem.integration.agentdojo_traces import Episode, Message

__all__ = [
    "LiveOutcome",
    "live_episode_stub",
    "run_defended_episode",
    "adaptation_statistics",
]


def live_episode_stub(*, model_name: str, suite_name: str, suite_version: str, user_task_id: str,
                      injection_task_id: Optional[str], attack: Optional[str], injections: Mapping[str, str],
                      system_prompt: str, user_prompt: str, repeat: int) -> Episode:
    """An ``Episode`` carrying only what ``RemGuard`` reads (objective, system prompt, ids).

    Outcomes are unknown before the run, so ``utility``/``security`` are placeholders that REM never
    reads; the live outcome is returned separately in ``LiveOutcome``.
    """
    return Episode(
        path=f"live://{model_name}/{user_task_id}/{injection_task_id or 'none'}/{attack or 'none'}/r{repeat}",
        pipeline=model_name,
        suite=suite_name,
        user_task_id=user_task_id,
        injection_task_id=injection_task_id,
        attack_type=attack,
        injections=dict(injections),
        messages=(Message("system", system_prompt), Message("user", user_prompt)),
        utility=False,
        security=False,
        error=None,
        benchmark_version=suite_version,
    )


@dataclass
class LiveOutcome:
    """Result of one defended (or undefended) live episode."""

    episode_id: str
    utility: bool
    security: bool                       # AgentDojo convention: True = the injection task succeeded
    audit: List[Dict[str, Any]]
    messages: List[Dict[str, Any]]
    wall_time_s: float
    error: Optional[str] = None
    adaptation: Dict[str, int] = field(default_factory=dict)
    transcripts: List[List[Dict[str, Any]]] = field(default_factory=list)


def _message_record(m: Mapping[str, Any]) -> Dict[str, Any]:
    """JSON-serialisable summary of an AgentDojo chat message (no raw tool output beyond 500 chars)."""
    content = m.get("content")
    if isinstance(content, list):
        text = "\n".join(str(b.get("content", "")) if isinstance(b, Mapping) else str(b) for b in content)
    else:
        text = "" if content is None else str(content)
    rec: Dict[str, Any] = {"role": m.get("role"), "text": text[:500]}
    if m.get("tool_calls"):
        rec["tool_calls"] = [{"function": c.function, "args": dict(c.args), "id": c.id} for c in m["tool_calls"]]
    if m.get("role") == "tool":
        tc = m.get("tool_call")
        rec["tool_call_id"] = m.get("tool_call_id")
        rec["function"] = getattr(tc, "function", None)
        rec["error"] = m.get("error")
    return rec


def run_defended_episode(
    *,
    suite: Any,
    llm: Any,
    guard: RemGuard,
    user_task_id: str,
    injection_task_id: Optional[str],
    injections: Mapping[str, str],
    system_prompt: str,
    pipeline_name: str,
    max_iters: int = 15,
    environment: Any = None,
) -> LiveOutcome:
    """Run one episode with ``llm`` as the agent and ``guard`` at the tool boundary.

    Args:
        suite: AgentDojo task suite (banking).
        llm: an AgentDojo LLM pipeline element (provider LLM, or a scripted test agent).
        guard: a fresh ``RemGuard`` for this episode (state must not be shared across episodes).
        environment: optional pre-built environment (used by tests to inspect side effects).
    """
    AgentPipeline, SystemMessage, InitQuery, ToolsExecutionLoop, _ReplayLLM, Guarded = _agentdojo_elements()
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement

    transcripts = []
    attempt_starts = []

    class _BeginAttempt(BasePipelineElement):
        name = "rem_live_attempt"

        def query(self, query, runtime, env, messages=[], extra_args={}):
            attempt_starts.append(len(guard.audit))
            return query, runtime, env, messages, extra_args

    class _Recorder(BasePipelineElement):
        name = "rem_live_recorder"

        def query(self, query, runtime, env, messages=[], extra_args={}):
            transcripts.append([_message_record(m) for m in messages])
            return query, runtime, env, messages, extra_args

    pipe = AgentPipeline([_BeginAttempt(), SystemMessage(system_prompt), InitQuery(), llm,
                          ToolsExecutionLoop([Guarded(guard), llm], max_iters=max_iters), _Recorder()])
    pipe.name = pipeline_name
    ut = suite.get_user_task_by_id(user_task_id)
    it = suite.get_injection_task_by_id(injection_task_id) if injection_task_id else None
    err = None
    t0 = time.perf_counter()
    try:
        utility, security = suite.run_task_with_pipeline(pipe, ut, it, dict(injections), environment=environment)
    except Exception as exc:  # recorded, never dropped
        utility, security, err = False, False, repr(exc)[:500]
    wall = time.perf_counter() - t0
    for attempt, (start, end) in enumerate(zip(attempt_starts, attempt_starts[1:] + [len(guard.audit)]), 1):
        for row in guard.audit[start:end]:
            row["chat_attempt"] = attempt
    out = LiveOutcome(
        episode_id=guard.episode.episode_id,
        utility=bool(utility),
        security=bool(security),
        audit=guard.audit,
        messages=transcripts[-1] if transcripts else [],
        transcripts=transcripts,
        wall_time_s=wall,
        error=err,
    )
    out.adaptation = adaptation_statistics(guard.audit, restricted=tuple(guard.config.restricted_tools))
    return out


def adaptation_statistics(audit: Sequence[Mapping[str, Any]], restricted: Sequence[str]) -> Dict[str, int]:
    """Counts on later assistant turns that could have seen a refusal in the same chat."""
    stats = {"proposals": len(audit), "withheld": 0, "retries": 0, "replans": 0,
             "y1_proposed": 0, "y1_released": 0, "y1_released_after_refusal": 0}
    # No tool result is visible to the model until the whole assistant turn is processed.
    # AgentDojo may restart a chat within one scored episode, without showing the old messages.
    for _, attempt in groupby(audit, key=lambda a: a.get("chat_attempt", 1)):
        withheld = set()
        for _, turn in groupby(enumerate(attempt), key=lambda item: item[1].get("decision_point", item[0])):
            new_refusals = set()
            for _, a in turn:
                tool, digest = a["tool"], a.get("arguments_digest")
                if withheld:
                    if (tool, digest) in withheld:
                        stats["retries"] += 1
                    elif tool in restricted and all(t != tool for t, _ in withheld):
                        stats["replans"] += 1
                if int(a["label"]) == 1:
                    stats["y1_proposed"] += 1
                    if a["released"]:
                        stats["y1_released"] += 1
                        stats["y1_released_after_refusal"] += int(bool(withheld))
                if not a["released"]:
                    stats["withheld"] += 1
                    new_refusals.add((tool, digest))
            withheld.update(new_refusals)
    return stats
