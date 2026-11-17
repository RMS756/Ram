"""Matched closed-loop comparison with the complete Progent framework (harness; NOT EXECUTED in this session).

Status: [PROPOSED - EXPLORATORY]. Protocol: 05_CLOSED_LOOP_PROTOCOL.md. Every arm runs in the SAME process layout:
Progent's AgentDojo fork (pinned commit, banking suite, its tools wrapped by upstream ``apply_secure_tool_wrapper``), the
same agent model, the same attack, the same tasks and repeats. Arms differ only in what sits at the tool boundary:

  P0_manual / P0_generated / P0_update_autodeny / P0_update_autoapprove  upstream engine only (configs in progent_upstream)
  C1                       REM contract guard only (Progent's check off: SECAGENT_GENERATE=False with no policy installed
                           is NOT used, because upstream then allows every call with a warning; instead the fork is run
                           with SECAGENT_SUITE unset, so its tools are not wrapped)
  C2gen_<config>           REM contract guard first, then the upstream engine inside the tool (conjunction)
  C3gen_<config>           C2gen + the stored learned decision

The REM executor mirrors upstream ``ToolsExecutor.query`` (agentdojo/agent_pipeline/tool_execution.py at the pinned
commit): same string-list conversion, same result formatting, and the same policy-update call after each tool batch
when SECAGENT_UPDATE is "True". A call refused by REM is not executed and is not passed to the update.

Fail-closed preflight: the run refuses to start unless (1) the upstream checkout verifies at the pinned commit; (2) an
agent model and a policy model are declared separately; (3) for a hosted backend, a spending cap in USD is declared by the
operator (REM_SPEND_CAP_USD) and the estimate in 06_BUDGET_ESTIMATE.md for the chosen design is below it; (4) the number
of repeats and the task list are declared; (5) no human-approval configuration is requested (no reviewer exists).
No credential is read, printed or stored by this module; the provider SDKs read their own environment.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

import progent_upstream as PU

LOCAL_PREFIXES = ("meta-llama/", "Qwen/")          # upstream routes these to 127.0.0.1:8000/v1


class PreflightError(RuntimeError):
    """A design input of the closed-loop run is missing (DesignNotSpecified, fail-closed)."""


@dataclass
class RunDesign:
    upstream_path: str
    agent_model: str                       # the experimental agent model (AgentDojo --model)
    policy_model: Optional[str]            # Progent's policy-generation model (SECAGENT_POLICY_MODEL)
    arms: Sequence[str]
    user_tasks: Sequence[str]
    injection_tasks: Sequence[str]
    attack: str
    repeats: int
    spend_cap_usd: Optional[float] = None  # operator-declared; required for any hosted model
    estimate_usd: Optional[float] = None   # from 06_BUDGET_ESTIMATE.md for exactly this design
    out_dir: str = "REM_PROGENT_COMPETITIVE_2026_11_18/closed_loop_results"
    notes: Dict[str, Any] = field(default_factory=dict)


def _hosted(model: Optional[str]) -> bool:
    return bool(model) and not model.startswith(LOCAL_PREFIXES)


def preflight(d: RunDesign) -> None:
    PU.verify_checkout(d.upstream_path)
    if not d.agent_model:
        raise PreflightError("agent model not declared")
    needs_policy = [a for a in d.arms if "generated" in a or "update" in a]
    if needs_policy and not d.policy_model:
        raise PreflightError(f"arms {needs_policy} need a policy model; none declared")
    if any("human" in a for a in d.arms):
        raise PreflightError("a human-approval configuration was requested but no reviewer exists in this study")
    if not d.user_tasks or not d.attack or d.repeats < 1:
        raise PreflightError("tasks, attack and number of repeats must be declared")
    if _hosted(d.agent_model) or (needs_policy and _hosted(d.policy_model)):
        if d.spend_cap_usd is None or d.spend_cap_usd <= 0:
            raise PreflightError("a hosted model is used and no spending cap is declared (REM_SPEND_CAP_USD)")
        if d.estimate_usd is None:
            raise PreflightError("no cost estimate for this exact design; compute it with budget.py first")
        if d.estimate_usd > d.spend_cap_usd:
            raise PreflightError(f"estimate {d.estimate_usd:.2f} USD exceeds the declared cap {d.spend_cap_usd:.2f} USD")
    for a in d.arms:
        base = a.split("_", 1)[1] if a.startswith(("C2gen_", "C3gen_")) else a
        if a not in ("C1",) and base not in PU.CONFIGS:
            raise PreflightError(f"unknown arm {a}")


def rem_executor_class(fork_tool_execution, guard_factory: Callable[[], Any], update: bool, secagent=None):
    """Build an executor from the FORK's ToolsExecutor with a REM guard in front of each call.

    ``fork_tool_execution`` is the fork's ``agentdojo.agent_pipeline.tool_execution`` module (passed in, so this module
    never imports upstream code by itself). ``guard_factory`` returns the REM guard of the episode.
    """
    from ast import literal_eval
    Base = fork_tool_execution.ToolsExecutor
    is_string_list = fork_tool_execution.is_string_list
    from agentdojo.types import ChatToolResultMessage  # the fork's own type

    class RemThenProgentExecutor(Base):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.guard = guard_factory()

        def query(self, query, runtime, env, messages=[], extra_args={}):
            if not messages or messages[-1]["role"] != "assistant" or not messages[-1].get("tool_calls"):
                return query, runtime, env, messages, extra_args
            self.guard.begin_decision_point()
            names = {t.name for t in runtime.functions.values()}
            results, calls, outs = [], [], []
            for call in messages[-1]["tool_calls"]:
                if call.function not in names:
                    results.append(ChatToolResultMessage(role="tool", content="", tool_call_id=call.id, tool_call=call,
                                                         error=f"Invalid tool {call.function} provided."))
                    self.guard.ingest(call.function, "", executed=False)
                    continue
                for k, v in call.args.items():
                    if isinstance(v, str) and is_string_list(v):
                        call.args[k] = literal_eval(v)
                release, notice = self.guard.evaluate(call.function, dict(call.args))
                if release:
                    res, err = runtime.run_function(env, call.function, call.args)   # upstream check runs inside the tool
                    text = self.output_formatter(res)
                    executed = err is None
                    calls.append({"name": call.function, "args": call.args})
                    outs.append(text)
                else:
                    text, err, executed = "", notice, False
                results.append(ChatToolResultMessage(role="tool", content=text, tool_call_id=call.id, tool_call=call, error=err))
                self.guard.ingest(call.function, text if executed else (err or ""), executed=executed)
            if update and secagent is not None and calls:
                secagent.generate_update_security_policy(calls, str(outs), manual_check=False)
            return query, runtime, env, [*messages, *results], extra_args

    return RemThenProgentExecutor


def write_design(d: RunDesign, path: Path) -> None:
    """Record the declared design (no secret: only model names, tasks, repeats, cap and estimate)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({**d.__dict__, "pinned_upstream": PU.PINNED,
                                "roles": {"coding_assistant": "used to write this harness; not part of any arm",
                                          "agent_model": d.agent_model, "policy_model": d.policy_model,
                                          "risk_estimator": "stored ridge F4 + Platt (C3 only); no model call"}},
                               indent=1), encoding="utf-8")


def main() -> None:  # pragma: no cover - requires the pinned fork, a backend and an authorised cap
    raise SystemExit("closed_loop.py is a harness; build a RunDesign, call preflight(), then run inside the pinned fork "
                     "environment as described in 05_CLOSED_LOOP_PROTOCOL.md. Not executed in the authoring session.")


if __name__ == "__main__":
    main()
