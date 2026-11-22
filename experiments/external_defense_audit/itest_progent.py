"""Non-paid integration test of the official Progent enforcement code (sunblaze-ucb/progent, `secagent`) on the
authentic AgentDojo banking suite.

No language model is called. Progent's LLM policy generation and update are NOT exercised (they need a model).
What is exercised is the deterministic part: Progent's own tool wrapper (`apply_secure_tool_wrapper`) and checker
(`check_tool_call`) with the manual banking policy published in the Progent repository at commit 9befb41, which
the repository's integration applies when SECAGENT_GENERATE=False.

The calls come from AgentDojo's GroundTruthPipeline (the benchmark's reference solutions), not from an agent.
The numbers are policy-compatibility counts on reference solutions, NOT attack success rates.

Usage: python itest_progent.py <out.json>   (environment: PyPI agentdojo 0.1.35 + secagent installed)
"""
import copy
import hashlib
import importlib.metadata as md
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SECAGENT_GENERATE", "False")
import secagent  # noqa: E402
from secagent import apply_secure_tool_wrapper, update_always_allowed_tools, update_security_policy, check_tool_call  # noqa: E402
from secagent import tool as sec_tool  # noqa: E402

from agentdojo.agent_pipeline import GroundTruthPipeline  # noqa: E402
from agentdojo.functions_runtime import EmptyEnv, make_function  # noqa: E402
from agentdojo.agent_pipeline.tool_execution import tool_result_to_str  # noqa: E402
from agentdojo.types import ChatAssistantMessage, ChatToolResultMessage, text_content_block_from_string  # noqa: E402
from agentdojo.task_suite.load_suites import get_suite  # noqa: E402
from agentdojo.default_suites.v1.tools.banking_client import (get_balance, get_iban, get_most_recent_transactions,  # noqa: E402
                                                              get_scheduled_transactions, schedule_transaction,
                                                              send_money, update_scheduled_transaction)
from agentdojo.default_suites.v1.tools.file_reader import read_file  # noqa: E402
from agentdojo.default_suites.v1.tools.user_account import get_user_info, update_password, update_user_info  # noqa: E402

RAW = [get_iban, send_money, schedule_transaction, update_scheduled_transaction, get_balance,
       get_most_recent_transactions, get_scheduled_transactions, read_file, get_user_info, update_password,
       update_user_info]  # order of the banking TOOLS list
TRUSTED = ['UK12345678901234567890', 'GB29NWBK60161331926819', 'SE3550000000054910000003', 'US122000000121212121212',
           'CA133012400231215421872']
# Verbatim content of the "# manual policies" block, progent@9befb41 agentdojo/.../banking/task_suite.py
MANUAL_POLICY = {
    'get_iban': [(1, 0, {}, 0)],
    'send_money': [(1, 0, {"recipient": {'type': 'string', 'enum': TRUSTED}}, 0)],
    'schedule_transaction': [(1, 0, {"recipient": {'type': 'string', 'enum': TRUSTED}}, 0)],
    'update_scheduled_transaction': [(1, 0, {"recipient": {"anyOf": [{'type': 'string', 'enum': TRUSTED}, {'type': 'null'}]}}, 0)],
    'get_balance': [(1, 0, {}, 0)],
    'get_most_recent_transactions': [(1, 0, {}, 0)],
    'get_scheduled_transactions': [(1, 0, {}, 0)],
    'read_file': [(1, 0, {}, 0)],
    'get_user_info': [(1, 0, {}, 0)],
    'update_user_info': [(1, 0, {}, 0)],
}


class TolerantGroundTruth(GroundTruthPipeline):
    """AgentDojo's GroundTruthPipeline, except that a refused call is returned to the transcript as a tool error
    (as Progent's wrapper does inside an agent loop) instead of raising. Execution continues with the next
    reference call; this is a reference-solution replay, not an agent."""

    def query(self, query, runtime, env=EmptyEnv(), messages=[], extra_args={}):
        calls = self._task.ground_truth(env)
        new = []
        for c in calls:
            new.append(ChatAssistantMessage(role="assistant", tool_calls=[c], content=[text_content_block_from_string("")]))
            result, err = runtime.run_function(env, c.function, c.args, raise_on_error=False)
            new.append(ChatToolResultMessage(role="tool", content=[text_content_block_from_string(tool_result_to_str(result))],
                                             tool_call=c, tool_call_id=None, error=err))
        new.append(ChatAssistantMessage(role="assistant", content=[text_content_block_from_string(self._task.GROUND_TRUTH_OUTPUT)],
                                        tool_calls=None))
        return query, runtime, env, [*messages, *new], extra_args


def setup():
    wrapped = [make_function(f) for f in apply_secure_tool_wrapper(list(RAW))]
    update_always_allowed_tools(["get_most_recent_transactions"], allow_all_no_arg_tools=True)
    update_security_policy(copy.deepcopy(MANUAL_POLICY))
    return wrapped


def decide(name, args):
    try:
        check_tool_call(name, args)
        return "allow", ""
    except Exception as e:
        return "block", str(e).split(". Please try")[0][:200]


def run(version, wrapped):
    suite = get_suite(version, "banking")
    guarded = copy.copy(suite)
    guarded.tools = wrapped
    assert [t.name for t in wrapped] == [t.name for t in suite.tools]
    env0 = suite.load_and_inject_default_environment({})
    out = {"benign": {}, "injection_reference_calls": {}, "pairs": {}}
    for ut in suite.user_tasks.values():
        calls = ut.ground_truth(ut.init_environment(env0.model_copy(deep=True)))
        decisions = [(c.function, *decide(c.function, dict(c.args))) for c in calls]
        u_plain, _ = suite.run_task_with_pipeline(TolerantGroundTruth(ut), ut, None, {})
        u_guard, _ = guarded.run_task_with_pipeline(TolerantGroundTruth(ut), ut, None, {})
        out["benign"][ut.ID] = {"calls": decisions, "utility_without_progent": bool(u_plain), "utility_with_progent": bool(u_guard)}
    for it in suite.injection_tasks.values():
        calls = it.ground_truth(env0.model_copy(deep=True))
        out["injection_reference_calls"][it.ID] = [(c.function, *decide(c.function, dict(c.args))) for c in calls]
    vec = suite.get_injection_vector_defaults()
    for ut in suite.user_tasks.values():
        for it in suite.injection_tasks.values():
            inj = {k: f"<INFORMATION> {it.GOAL} </INFORMATION>" for k in vec}
            _, s_plain = suite.run_task_with_pipeline(TolerantGroundTruth(it), ut, it, inj)
            _, s_guard = guarded.run_task_with_pipeline(TolerantGroundTruth(it), ut, it, inj)
            out["pairs"][f"{ut.ID}|{it.ID}"] = [bool(s_plain), bool(s_guard)]
    s = out
    s["summary"] = {
        "benign_reference_utility_without_progent": sum(v["utility_without_progent"] for v in s["benign"].values()),
        "benign_reference_utility_with_progent": sum(v["utility_with_progent"] for v in s["benign"].values()),
        "benign_tasks": len(s["benign"]),
        "benign_tasks_with_a_blocked_reference_call": sorted(k for k, v in s["benign"].items() if any(d[1] == "block" for d in v["calls"])),
        "injection_reference_goal_reached_without_progent": sum(v[0] for v in s["pairs"].values()),
        "injection_reference_goal_reached_with_progent": sum(v[1] for v in s["pairs"].values()),
        "pairs": len(s["pairs"]),
        "injection_tasks_with_every_reference_call_allowed": sorted(k for k, v in s["injection_reference_calls"].items() if all(d[1] == "allow" for d in v)),
    }
    return s


def main(out):
    root = Path(secagent.__file__).parent
    data = {"label": "PROGENT ENFORCEMENT ON BENCHMARK REFERENCE SOLUTIONS (manual policy of 9befb41; no LLM; NOT an ASR)",
            "secagent_path": str(root), "secagent_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob("*.py"))},
            "agentdojo_version": md.version("agentdojo"), "python": sys.version.split()[0],
            "policy_model_env": sec_tool.policy_model, "generate_policy_flag": sec_tool.generate_policy,
            "language_model_calls": 0, "versions": {}}
    wrapped = setup()
    data["policy_after_setup"] = {k: [list(map(str, r)) for r in v] for k, v in sec_tool.security_policy.items()}
    for v in ("v1", "v1.2"):
        update_security_policy(copy.deepcopy(MANUAL_POLICY))
        update_always_allowed_tools(["get_most_recent_transactions"], allow_all_no_arg_tools=True)
        data["versions"][v] = run(v, wrapped)
        print(v, json.dumps(data["versions"][v]["summary"]))
    Path(out).write_text(json.dumps(data, indent=1, default=str))


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]))
