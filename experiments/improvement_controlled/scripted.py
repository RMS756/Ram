"""Scripted closed-loop harness of the controlled improvement study (no LLM).

Differences from the frozen harness (progent_competitive/closed_loop_scripted.py, kept unchanged):
  * the test double ends with the user task's GROUND_TRUTH_OUTPUT, as AgentDojo's own GroundTruthPipeline does
    (agent_pipeline/ground_truth_pipeline.py l.50); the frozen double ended with "Done.", which made the two
    question-answering tasks (user_task_1, user_task_7) fail for every arm;
  * the order of the obedient agent's calls is a parameter: 'user_first' (frozen behaviour: user ground truth, then the
    injection ground truth) or 'injection_first' (injection ground truth, then the user ground truth);
  * 'user_only' runs only the user ground truth in the INJECTED environment (collision scan: does the user's own
    legitimate work already satisfy the attacker's evaluator?).
Additional per-episode outputs: whether every reference call of the user task was released ("reference_released"), and
the full audit of restricted calls (tool, args, label, released, source).
Guards never read labels, task ids or evaluator state; AgentDojo's evaluators decide utility and security.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in ("", "experiments/progent_competitive", "experiments/repair_study", "experiments/improve_study", "experiments/pilot",
           "experiments/live", "experiments/improvement_controlled"):
    sys.path.insert(0, str(ROOT / _p) if _p else str(ROOT))


def make_agent_class():
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
    from agentdojo.types import text_content_block_from_string

    class ScriptedAgent(BasePipelineElement):
        name = "gpt-4o-2024-05-13"   # only used by the attack template to address the model by name

        def __init__(self, ut, it, mode="user_first"):
            self.ut, self.it, self.mode, self.queue = ut, it, mode, None

        def query(self, query, runtime, env, messages=[], extra_args={}):
            if self.queue is None:
                u = list(self.ut.ground_truth(env))
                i = list(self.it.ground_truth(env)) if (self.it and self.mode != "user_only") else []
                if self.mode == "injection_first":
                    self.queue = i + u
                elif self.mode == "injection_after_first_read":       # the injected calls right after the user's first read
                    reads = [n for n, c in enumerate(u) if c.function.startswith(("get_", "read_"))]
                    cut = reads[0] + 1 if reads else 0
                    self.queue = u[:cut] + i + u[cut:]
                else:
                    self.queue = u + i
            if self.queue:
                msg = {"role": "assistant", "content": [text_content_block_from_string("")], "tool_calls": [self.queue.pop(0)]}
            else:
                msg = {"role": "assistant", "content": [text_content_block_from_string(self.ut.GROUND_TRUTH_OUTPUT or "Done.")],
                       "tool_calls": None}
            return query, runtime, env, [*messages, msg], extra_args

    return ScriptedAgent


def run(arms, guard_factory, modes=("user_first",), include_benign=True, pairs=None):
    """guard_factory(arm, episode) -> fresh guard. Returns one row per (user task, injection task, mode, arm)."""
    import rs_run as V1R
    from agentdojo.agent_pipeline.agent_pipeline import load_system_message
    from agentdojo.attacks.attack_registry import load_attack
    from rem.integration.agentdojo_live import live_episode_stub, run_defended_episode

    Agent = make_agent_class()
    st = V1R.common.make_setup()
    suite = st.suite
    restricted = set(st.restricted)
    sysmsg = load_system_message(None)
    rows = []
    users = sorted(suite.user_tasks, key=lambda x: int(x.split("_")[-1]))
    injs = sorted(suite.injection_tasks, key=lambda x: int(x.split("_")[-1]))
    for u in users:
        ut = suite.get_user_task_by_id(u)
        n_ref = len(ut.ground_truth(suite.load_and_inject_default_environment({})))
        for i in ([None] if include_benign else []) + injs:
            if pairs is not None and (u, i) not in pairs:
                continue
            it = suite.get_injection_task_by_id(i) if i else None
            inj = load_attack("important_instructions", suite, Agent(ut, it)).attack(ut, it) if i else {}
            for mode in (modes if i else ("benign",)):
                for arm in arms:
                    ep = live_episode_stub(model_name="scripted-ground-truth-agent", suite_name="banking", suite_version="v1",
                                           user_task_id=u, injection_task_id=i, attack="important_instructions" if i else None,
                                           injections=inj, system_prompt=sysmsg, user_prompt=ut.PROMPT, repeat=0)
                    g = guard_factory(arm, ep)
                    seen = []                                    # benchmark (synthetic) arguments, captured by the harness
                    _ev = g.evaluate

                    def _cap(tool, args, _ev=_ev, seen=seen):
                        seen.append(dict(args))
                        return _ev(tool, args)
                    g.evaluate = _cap
                    o = run_defended_episode(suite=suite, llm=Agent(ut, it, "user_only" if mode == "benign" else mode), guard=g,
                                             user_task_id=u, injection_task_id=i, injections=inj, system_prompt=sysmsg,
                                             pipeline_name="gpt-4o-2024-05-13")
                    aud = o.audit
                    rows.append({"user_task": u, "injection_task": i, "mode": mode, "arm": arm, "utility": bool(o.utility),
                                 "security": bool(o.security) if i else None, "error": o.error, "proposals": len(aud),
                                 "reference_calls": n_ref,
                                 "restricted": [{"tool": a["tool"], "args": seen[k] if k < len(seen) else None, "label": a["label"],
                                                 "released": bool(a["released"]), "verdict": str(a["verdict"]), "source": a["verdict_source"],
                                                 "tier": a["tier"], "p": a["p"], "stage": (a["details"].get("cs") or {}).get("stage"),
                                                 "learned_p": (a["details"].get("cs") or {}).get("p"),
                                                 "contract": a["details"].get("contract"), "latency_ms": a.get("rem_latency_full_ms")}
                                                for k, a in enumerate(aud) if a["tool"] in restricted],
                                 "latencies_ms": [a.get("rem_latency_full_ms") for a in aud],
                                 "all_released": all(a["released"] for a in aud)})
    return rows
