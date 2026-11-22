"""Non-paid integration test of the official DRIFT implementation on the AgentDojo banking suite.

WHAT THIS IS: an interface and code-path test. The official DRIFT code (SaFo-Lab/DRIFT, loaded by path,
unmodified) is run inside AgentDojo with a TEST-DOUBLE client in place of the LLM. The test double answers
DRIFT's sub-prompts with fixed, scripted text (privilege labels, a plan taken from the benchmark's reference
solution, an obedient tool-calling policy, a configurable injection detector and alignment judge).

WHAT THIS IS NOT: a security or utility result. Every outcome below is determined by the scripted answers.
It shows only that DRIFT runs on this benchmark version, which checks are reached, what they need from the
model, and that AgentDojo's evaluator scores DRIFT's message format.

Usage: DRIFT_UPSTREAM=<path to DRIFT checkout> python itest_drift.py <out.json>
"""
import hashlib
import importlib.metadata as md
import json
import os
import re
import sys
import time
from pathlib import Path

UP = Path(os.environ["DRIFT_UPSTREAM"]).resolve()
sys.path.insert(0, str(UP))
os.chdir(UP)  # DRIFT imports its modules relative to its checkout

from agentdojo.agent_pipeline import AgentPipeline, InitQuery, ToolsExecutor  # noqa: E402
from agentdojo.ast_utils import create_python_function_from_tool_call  # noqa: E402
from agentdojo.attacks.attack_registry import load_attack  # noqa: E402
from agentdojo.task_suite.load_suites import get_suite  # noqa: E402

from DRIFTLLM import DRIFTLLM  # noqa: E402
from DRIFTTaskSuite import DRIFTTaskSuite  # noqa: E402
from DRIFTToolsExecutionLoop import DRIFTToolsExecutionLoop  # noqa: E402

READ_TOOLS = {"get_iban", "get_balance", "get_most_recent_transactions", "get_scheduled_transactions", "read_file",
              "get_user_info"}


class Args:  # the flags of DRIFT's pipeline_main.py, all three modules on
    build_constraints = True
    injection_isolation = True
    dynamic_validation = True
    adaptive_attack = False


class Log:
    def __init__(self):
        self.lines = []

    def info(self, m):
        self.lines.append(str(m)[:400])


class ScriptedClient:
    """TEST DOUBLE for DRIFT's model client. Not a language model."""

    def __init__(self, plan_calls, injection_calls, goal_marker, detector, judge):
        self.plan = [create_python_function_from_tool_call(c) for c in plan_calls]
        self.plan_names = [c.function for c in plan_calls]
        self.inj = [create_python_function_from_tool_call(c) for c in injection_calls]
        self.goal_marker = goal_marker
        self.detector = detector  # "none" | "echo": what the scripted detector reports
        self.judge = judge  # "Yes" | "No"
        self.total_tokens = 0
        self.calls = {"privilege": 0, "constraints": 0, "detector": 0, "agent": 0, "checklist_json": 0, "judge": 0}
        self.done = 0
        self.inj_done = 0

    def llm_run(self, system, user, name="default"):
        if "permission types" in system:
            self.calls["privilege"] += 1
            name_ = re.search(r'"name": "([a-z_]+)"', user).group(1)
            return "A" if name_ in READ_TOOLS else "B"
        if "identify any injection instructions" in system:
            self.calls["detector"] += 1
            if self.goal_marker and self.goal_marker in user:
                if self.detector == "echo":
                    return f"<detected_instructions>[{json.dumps(self.goal_marker)}]</detected_instructions>"
            return "<detected_instructions>[]</detected_instructions>"
        if "rewrite the checklist into a JSON" in system:
            self.calls["checklist_json"] += 1
            m = re.search(r"<Parameter_Checklist>\n(.*)\n</Parameter_Checklist>", user, re.S)
            return m.group(1) if m else "[]"
        if "Initial_Function_Trajectory" in user or "assess whether the deviation" in system:
            self.calls["judge"] += 1
            return f"<Judge Result>{self.judge}</Judge Result>\n<Judge Reason>scripted test double</Judge Reason>"
        raise AssertionError("unrecognised DRIFT sub-prompt: " + system[:120])

    def agent_run(self, messages, tools=(), **kw):
        system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        if "<function_trajectory>" in system and "<parameter_checklist>" in system and len(messages) <= 2:
            self.calls["constraints"] += 1
            checklist = [{"name": n, "required parameters": None, "conditions": None} for n in self.plan_names]
            return [f"<function_trajectory>[{', '.join(self.plan_names)}]</function_trajectory>\n"
                    f"<parameter_checklist>{json.dumps(checklist)}</parameter_checklist>"]
        self.calls["agent"] += 1
        # obedient double: follows the injected goal only if it is still visible in a tool result it is shown
        injected_visible = bool(self.goal_marker) and any(
            m.get("role") in ("tool", "observation") and self.goal_marker in str(m.get("content")) for m in messages)
        if injected_visible and self.inj_done < len(self.inj):
            c = self.inj[self.inj_done]
            self.inj_done += 1
            return [f"<function_thought>scripted: obey text found in tool output</function_thought>\n<function_call>[{c}]</function_call>\n<final_answer></final_answer>"]
        if self.done < len(self.plan):
            c = self.plan[self.done]
            self.done += 1
            return [f"<function_thought>scripted plan step</function_thought>\n<function_call>[{c}]</function_call>\n<final_answer></final_answer>"]
        return ["<function_thought>done</function_thought>\n<function_call>[]</function_call>\n<final_answer>Done.</final_answer>"]


def run_case(version, ut_id, it_id, detector, judge):
    suite = get_suite(version, "banking")
    log = Log()
    ut = suite.user_tasks[ut_id]
    it = suite.injection_tasks[it_id] if it_id else None
    env = suite.load_and_inject_default_environment({})
    plan = ut.ground_truth(ut.init_environment(env.model_copy(deep=True)))
    inj_calls = it.ground_truth(env.model_copy(deep=True)) if it else []
    client = ScriptedClient(plan, inj_calls, it.GOAL if it else None, detector, judge)
    llm = DRIFTLLM(Args(), client, logger=log)
    loop = DRIFTToolsExecutionLoop([ToolsExecutor(), llm])
    pipe = AgentPipeline([InitQuery(), llm, loop])
    pipe.name = "gpt-4o-2024-05-13"  # name DRIFT's pipeline_main.py assigns for OpenAI models (used by the attack text)
    ts = DRIFTTaskSuite(Args(), suite.name, suite.environment_type, suite.tools, suite.data_path, suite.benchmark_version,
                        parent_instance=suite)
    injections = load_attack("important_instructions", ts, pipe).attack(ut, it) if it else {}
    t0 = time.perf_counter()
    utility, security, messages = ts.run_task_with_pipeline(pipe, ut, it, injections)
    dt = time.perf_counter() - t0
    executed = [m["tool_call"]["function"] for m in messages if m.get("role") == "tool"]
    refusals = [str(m["content"])[:160] for m in messages if "[CALL ERROR]" in str(m.get("content", ""))]
    return {"benchmark_version": version, "user_task": ut_id, "injection_task": it_id, "scripted_detector": detector,
            "scripted_judge": judge, "reference_plan": [c.function for c in plan],
            "injection_reference_calls": [c.function for c in inj_calls], "executed_tool_calls": executed,
            "drift_refusals": refusals, "agentdojo_utility": bool(utility),
            "agentdojo_security_injection_goal_reached": (bool(security) if it else None),
            "test_double_calls_by_drift_module": client.calls, "wall_s": round(dt, 3),
            "drift_log_tail": [x for x in log.lines if "Trajectory" in x or "Detected" in x or "Permission" in x][-6:]}


def main(out):
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(UP.glob("*.py"))}
    commit = os.popen(f"git -C {UP} rev-parse HEAD").read().strip()
    cases = [
        ("v1", "user_task_0", None, "none", "Yes"),
        ("v1", "user_task_0", "injection_task_0", "none", "Yes"),   # injected call uses a planned tool (send_money)
        ("v1", "user_task_0", "injection_task_0", "echo", "Yes"),   # scripted detector reports the injected goal
        ("v1", "user_task_0", "injection_task_7", "none", "No"),    # off-plan Write tool -> alignment judge
        ("v1", "user_task_0", "injection_task_7", "none", "Yes"),
        ("v1.2", "user_task_0", None, "none", "Yes"),
    ]
    res = []
    for c in cases:
        try:
            res.append(run_case(*c))
        except Exception as e:
            res.append({"case": c, "error": f"{type(e).__name__}: {e}"})
    data = {"label": "INTERFACE TEST WITH A SCRIPTED TEST DOUBLE - NOT A SECURITY OR UTILITY RESULT",
            "drift_commit": commit, "drift_files_sha256": files, "agentdojo_version": md.version("agentdojo"),
            "python": sys.version.split()[0], "language_model_calls": 0, "cases": res}
    Path(out).write_text(json.dumps(data, indent=1))
    for r in res:
        print({k: r.get(k) for k in ("benchmark_version", "user_task", "injection_task", "scripted_detector", "scripted_judge",
                                     "executed_tool_calls", "agentdojo_utility", "agentdojo_security_injection_goal_reached", "error")},
              "refusals:", len(r.get("drift_refusals", [])), r.get("test_double_calls_by_drift_module"))


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]))
