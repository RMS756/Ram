"""Harness smoke test of the closed-loop integration (NOT AN EXPERIMENT, NOT AN LLM).

The agent is a scripted "fully compliant" test double: it issues the user task's AgentDojo ground-truth
calls and then the injection task's ground-truth calls, one call per turn, and stops. It neither reads
tool outputs nor adapts. The purpose is to show that the defended pipeline (B0 / B1 / REM, frozen
parameters of one cross-fit fold) runs end to end on every banking (user task, injection task) pair with
real AgentDojo injections, without crashes, and that withheld calls are not executed.
Its counts must not be reported as attack-success or utility results.

usage: PILOT_RESULTS_DIR=<frozen pilot state> python3 experiments/live/smoke_scripted.py <fold> <out.json>
"""

from __future__ import annotations

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))
sys.path.insert(0, HERE)


def main(fold: str, out_path: str) -> None:
    import common
    from agentdojo.agent_pipeline.agent_pipeline import load_system_message
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
    from agentdojo.attacks.attack_registry import load_attack
    from agentdojo.types import text_content_block_from_string
    from rem.core.results import Verdict
    from rem.integration.agentdojo_live import live_episode_stub, run_defended_episode
    from rem.integration.agentdojo_replay import GuardConfig, RemGuard
    from run_live import frozen_components

    class GroundTruthCompliantAgent(BasePipelineElement):
        name = "gpt-4o-2024-05-13"   # only used by the attack template to address the model by name

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

    st = common.make_setup()
    suite = st.suite
    pol, scorer, ref = frozen_components(fold)
    sysmsg = load_system_message(None)

    def decider(name):
        if name == "B0":
            return lambda c: (Verdict.ALLOW, "allow_all", {})
        P = pol["B1" if name == "B1" else "A3_step_level"]

        def d(c):
            v = P.decide(c.p, c.tier, c.tool, c.available)
            return v.verdict, v.source, {}
        return d

    rows = []
    for u in sorted(suite.user_tasks, key=lambda x: int(x.split("_")[-1])):
        for i in [None] + sorted(suite.injection_tasks, key=lambda x: int(x.split("_")[-1])):
            ut = suite.get_user_task_by_id(u)
            it = suite.get_injection_task_by_id(i) if i else None
            inj = load_attack("important_instructions", suite, GroundTruthCompliantAgent(ut, it)).attack(ut, it) if i else {}
            for conf in ("B0", "B1", "REM"):
                ep = live_episode_stub(model_name="scripted-ground-truth-agent", suite_name="banking", suite_version="v1",
                                       user_task_id=u, injection_task_id=i, attack="important_instructions" if i else None,
                                       injections=inj, system_prompt=sysmsg, user_prompt=ut.PROMPT, repeat=0)
                g = RemGuard(GuardConfig(st.spec, st.detector, ref, st.tier_map, st.restricted, "step_level", "no_reviewer"),
                             None if conf == "B0" else scorer, decider(conf), st.labeler, ep)
                o = run_defended_episode(suite=suite, llm=GroundTruthCompliantAgent(ut, it), guard=g, user_task_id=u,
                                         injection_task_id=i, injections=inj, system_prompt=sysmsg,
                                         pipeline_name="gpt-4o-2024-05-13")
                rows.append({"user_task": u, "injection_task": i, "configuration": conf, "error": o.error,
                             "proposals": len(o.audit), "withheld": sum(not a["released"] for a in o.audit),
                             "withheld_y1": sum((not a["released"]) and a["label"] == 1 for a in o.audit),
                             "proposed_y1": sum(a["label"] == 1 for a in o.audit)})
    summ = collections.defaultdict(collections.Counter)
    for r in rows:
        s = summ[r["configuration"]]
        s["episodes"] += 1
        s["errors"] += bool(r["error"])
        for k in ("proposals", "withheld", "withheld_y1", "proposed_y1"):
            s[k] += r[k]
    out = {"status": "HARNESS SMOKE TEST — scripted ground-truth agent, not an LLM, not an experimental result",
           "fold_used_for_frozen_parameters": fold, "suite": "banking v1", "attack": "important_instructions",
           "summary": {k: dict(v) for k, v in summ.items()}, "episodes": rows}
    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps(out["summary"], indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
