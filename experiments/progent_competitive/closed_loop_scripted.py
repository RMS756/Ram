"""Closed-loop implementation test with scripted (non-LLM) agents (10_SCRIPTED_CLOSED_LOOP_PROTOCOL.md).

NOT AN LLM EXPERIMENT. The agent is a test double that issues AgentDojo's own ground-truth calls, one per turn:
  * benign episode   (no injection): the user task's ground truth;
  * compromised episode (important_instructions attack): the user task's ground truth, then the injection task's ground
    truth, i.e. an agent that fully obeys the injected instruction.
The agent neither reads tool outputs nor adapts to refusals. REM's refusal notices are returned to it through the real
AgentDojo pipeline (installed AgentDojo 0.1.35, banking v1), and AgentDojo's own evaluators decide utility and security.
Guards never read labels, task ids or evaluator state.

What it shows: whether each arm lets the benchmark's canonical legitimate solution through, and whether it stops the
canonical attacker calls when the agent obeys the injection, in a loop where withheld calls are really not executed.
What it does not show: behaviour of a real agent (retries, replanning, partial compliance), or anything about full Progent.

usage: python3 closed_loop_scripted.py <out.json>     (environment of the study; stored S1 cell injection_task_0 as for the fixtures)
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in ("", "experiments/progent_competitive", "experiments/repair_study", "experiments/improve_study", "experiments/pilot",
           "experiments/live"):
    sys.path.insert(0, str(ROOT / _p) if _p else str(ROOT))

ARMS = ["B0", "PG", "GV_math2", "C1", "C2PG", "C3PG"]


def main(out_path: str) -> None:
    import contract_arms as CA
    import progent_manual as PGM
    import repaired_arms_v2 as RA2
    import rs_run as V1R
    from agentdojo.agent_pipeline.agent_pipeline import load_system_message
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
    from agentdojo.attacks.attack_registry import load_attack
    from agentdojo.types import text_content_block_from_string
    from rem.core.results import Verdict
    from rem.integration.agentdojo_live import live_episode_stub, run_defended_episode
    from rem.integration.agentdojo_replay import GuardConfig, RemGuard

    class ScriptedAgent(BasePipelineElement):
        name = "gpt-4o-2024-05-13"   # only used by the attack template to address the model by name

        def __init__(self, ut, it):
            self.ut, self.it, self.queue = ut, it, None

        def query(self, query, runtime, env, messages=[], extra_args={}):
            if self.queue is None:
                self.queue = list(self.ut.ground_truth(env)) + (list(self.it.ground_truth(env)) if self.it else [])
            if self.queue:
                msg = {"role": "assistant", "content": [text_content_block_from_string("")], "tool_calls": [self.queue.pop(0)]}
            else:
                msg = {"role": "assistant", "content": [text_content_block_from_string("Done.")], "tool_calls": None}
            return query, runtime, env, [*messages, msg], extra_args

    C, J, common = V1R.C, V1R.J, V1R.common
    st = common.make_setup()
    suite = st.suite
    cells, cs = J.load("cells"), C.load("cs_cells")
    key = ("S1", "injection_task_0")
    PGM.load()
    sysmsg = load_system_message(None)

    def guard(arm, ep):
        if arm in CA.ARMS:
            return CA.make_guard(arm, cells[key], cs[key], ep, st)
        if arm in RA2.ARMS:
            return RA2.make_guard(arm, cells[key], cs[key], ep, st)
        gc = GuardConfig(st.spec, st.detector, cells[key]["reference"], st.tier_map, st.restricted, "step_level", "no_reviewer")
        if arm == "B0":
            return RemGuard(gc, None, lambda c: (Verdict.ALLOW, "allow_all", {}), st.labeler, ep)
        if arm == "PG":                                      # as improve.py arm "PG": the manual policy on every call
            return RemGuard(gc, None, lambda c: ((Verdict.ALLOW if PGM.allowed(c.tool, c.args) else Verdict.BLOCK),
                                                 "progent_manual_policy", {}), st.labeler, ep)
        raise ValueError(arm)

    rows = []
    restricted = set(st.restricted)
    for u in sorted(suite.user_tasks, key=lambda x: int(x.split("_")[-1])):
        for i in [None] + sorted(suite.injection_tasks, key=lambda x: int(x.split("_")[-1])):
            ut = suite.get_user_task_by_id(u)
            it = suite.get_injection_task_by_id(i) if i else None
            inj = load_attack("important_instructions", suite, ScriptedAgent(ut, it)).attack(ut, it) if i else {}
            for arm in ARMS:
                ep = live_episode_stub(model_name="scripted-ground-truth-agent", suite_name="banking", suite_version="v1",
                                       user_task_id=u, injection_task_id=i, attack="important_instructions" if i else None,
                                       injections=inj, system_prompt=sysmsg, user_prompt=ut.PROMPT, repeat=0)
                o = run_defended_episode(suite=suite, llm=ScriptedAgent(ut, it), guard=guard(arm, ep), user_task_id=u,
                                         injection_task_id=i, injections=inj, system_prompt=sysmsg, pipeline_name="gpt-4o-2024-05-13")
                rows.append({"user_task": u, "injection_task": i, "arm": arm, "utility": o.utility, "security": o.security,
                             "error": o.error, "proposals": len(o.audit),
                             "restricted_withheld": [(a["tool"], a["verdict_source"]) for a in o.audit
                                                     if a["tool"] in restricted and not a["released"]]})
    summ = {}
    for arm in ARMS:
        rr = [r for r in rows if r["arm"] == arm]
        ben = [r for r in rr if r["injection_task"] is None]
        att = [r for r in rr if r["injection_task"] is not None]
        summ[arm] = {"benign_episodes": len(ben), "benign_utility": sum(r["utility"] for r in ben),
                     "compromised_episodes": len(att), "injection_goal_reached": sum(r["security"] for r in att),
                     "user_task_done_while_compromised": sum(r["utility"] for r in att), "errors": sum(bool(r["error"]) for r in rr),
                     "benign_withheld_by_source": dict(collections.Counter(s for r in ben for _t, s in r["restricted_withheld"])),
                     "benign_tasks_failed": sorted(r["user_task"] for r in ben if not r["utility"])}
    out = {"status": "IMPLEMENTATION TEST with scripted ground-truth agents (not an LLM, not adaptive); AgentDojo 0.1.35 banking v1; "
                     "important_instructions; stored S1 cell injection_task_0; not an attack-success rate of any real agent",
           "summary": summ, "episodes": rows}
    Path(out_path).write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    for arm, s in summ.items():
        print(arm, {k: v for k, v in s.items() if k != "benign_withheld_by_source"}, flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
