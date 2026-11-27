"""Replay of a recorded AgentDojo episode with REM-DiD at the tool boundary and, when ENF is active, every
executed call routed through the capability gateway (no other execution path exists in this executor).
Mirrors rem.integration.agentdojo_replay.replay_episode (unchanged) except for the executor."""
from __future__ import annotations

from typing import Any

from rem.integration.agentdojo_replay import ReplayOutcome, _agentdojo_elements

from .enforcement import GatewayRefusal


def replay_episode_did(episode, suite, guard) -> ReplayOutcome:
    from ast import literal_eval

    from agentdojo.agent_pipeline import ToolsExecutor
    from agentdojo.agent_pipeline.tool_execution import is_string_list
    from agentdojo.types import ChatToolResultMessage, text_content_block_from_string

    AgentPipeline, SystemMessage, InitQuery, ToolsExecutionLoop, ReplayLLM, _ = _agentdojo_elements()

    class GatewayExecutor(ToolsExecutor):
        def __init__(self, g) -> None:
            super().__init__()
            self.guard = g

        def query(self, query, runtime, env, messages=[], extra_args={}):
            if not messages or messages[-1]["role"] != "assistant" or not messages[-1]["tool_calls"]:
                return query, runtime, env, messages, extra_args
            self.guard.begin_decision_point()
            results = []
            names = {t.name for t in runtime.functions.values()}
            for call in messages[-1]["tool_calls"]:
                for k, v in call.args.items():
                    if isinstance(v, str) and is_string_list(v):
                        call.args[k] = literal_eval(v)
                if call.function not in names:
                    err = f"Invalid tool {call.function} provided."
                    results.append(ChatToolResultMessage(role="tool", content=[text_content_block_from_string("")],
                                                         tool_call_id=call.id, tool_call=call, error=err))
                    self.guard.ingest(call.function, "", executed=False)
                    continue
                release, notice = self.guard.evaluate(call.function, dict(call.args))
                text, err, executed = "", notice, False
                if release:
                    gw = getattr(self.guard, "gateway", None)
                    try:
                        if gw is not None:
                            res, err = gw.execute(self.guard.last_permit, call.function, dict(call.args),
                                                  self.guard.decision_no,
                                                  lambda: runtime.run_function(env, call.function, call.args))
                        else:
                            res, err = runtime.run_function(env, call.function, call.args)
                        text = self.output_formatter(res)
                        executed = err is None
                    except GatewayRefusal as r:
                        text, err, executed = "", f"REM-DiD gateway refused: {r}", False
                        self.guard.audit[-1]["released"] = False
                        self.guard.audit[-1]["mechanism"] = f"gateway_refused:{r}"
                results.append(ChatToolResultMessage(role="tool", content=[text_content_block_from_string(text)],
                                                     tool_call_id=call.id, tool_call=call, error=err))
                self.guard.ingest(call.function, text if executed else (err or ""), executed=executed)
            return query, runtime, env, [*messages, *results], extra_args

    llm = ReplayLLM(episode)
    pipe = AgentPipeline([SystemMessage(episode.system_prompt), InitQuery(), llm,
                          ToolsExecutionLoop([GatewayExecutor(guard), llm])])
    pipe.name = "remdid_replay"
    ut = suite.get_user_task_by_id(episode.user_task_id)
    it = suite.get_injection_task_by_id(episode.injection_task_id) if episode.injection_task_id else None
    err = None
    try:
        utility, security = suite.run_task_with_pipeline(pipe, ut, it, dict(episode.injections))
    except Exception as exc:
        utility, security, err = False, False, repr(exc)[:300]
    return ReplayOutcome(episode_id=episode.episode_id, utility=bool(utility), security=bool(security),
                         recorded_utility=episode.utility, recorded_security=episode.security,
                         audit=guard.audit, latencies_ms=guard.latencies_ms, error=err)
