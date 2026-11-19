"""SCRIPTED INTEGRATION PILOT of the three-arm harness — NOT AN LLM EXPERIMENT, NOT A RESULT.

Purpose (Phase 6 checks): show, for every AgentDojo banking (user task, injection task) pair and every benign user
task, that in each arm (D0 no defence, D1 frozen REM v1.0, D2 unmodified upstream MELON):
  * the agent element emits tool calls and the banking tools execute;
  * the benchmark's important_instructions payload reaches the agent through the real injection vectors;
  * REM receives every proposed call (audit record per call) and its refusals are fed back to the agent;
  * MELON runs its own detect(): the masked re-execution is requested from the same LLM element and its
    tool calls are embedded and compared, and a detection stops the episode;
  * AgentDojo's utility and security checks evaluate the final banking state;
  * logs contain the defence activity.

Test doubles (both stated wherever a number from this script is shown):
  AGENT  "ReactiveCompliantAgent": issues the user task's AgentDojo ground-truth calls one per turn; when a tool
         output contains the injected payload it next issues the injection task's ground-truth calls (it obeys
         the injection); in MELON's masked context it issues the injection calls iff the masked tool contents
         contain the payload. It does not reason, retry or adapt to refusals.
  EMBED  "TrigramHashEmbeddings": deterministic character-trigram hashing vectors (cosine 1 for identical text).
         It is NOT text-embedding-3-large; MELON's similarity threshold 0.8 is upstream's and unchanged.
Because both doubles are scripted, the counts this script writes are integration diagnostics. They must not be
reported, plotted or compared as attack-success or utility estimates of REM or MELON.

usage (MELON environment):
  /home/user/venvs/melon029/bin/python experiments/rem_vs_melon/pilot_scripted.py <out_dir> [--cases pilot|full]
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import pickle
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, HERE)

import harness as H  # noqa: E402

BUNDLE = os.path.join(REPO, "experiments", "melon_rem", "frozen", "frozen_rem_bundle.pkl")
MELON_PATH = os.environ.get("MELON_PI_DETECTOR", "/home/user/ucsb-mlsec/melon/pi_detector.py")
TARGET_NAME = "gpt-4o-2024-05-13"   # only addresses the model by name inside the attack template (as in the recorded runs)
PILOT_ATTACKED = [(f"user_task_{j}", f"injection_task_{j}") for j in range(9)]
PILOT_BENIGN = ["user_task_9", "user_task_11", "user_task_13", "user_task_15"]


class TrigramHashEmbeddings:
    """Deterministic stand-in for an embedding API (NOT text-embedding-3-large)."""

    def __init__(self, dim: int = 512):
        self.dim = dim
        self.embeddings = self

    def create(self, input, model):
        v = np.zeros(self.dim)
        s = f"  {input}  "
        for k in range(len(s) - 2):
            v[int(hashlib.md5(s[k:k + 3].encode()).hexdigest()[:8], 16) % self.dim] += 1.0
        v /= max(np.linalg.norm(v), 1e-12)
        return type("R", (), {"data": [type("D", (), {"embedding": v.tolist()})()], "usage": None})()


def reactive_agent(suite_task_pair, injections):
    from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
    from agentdojo.functions_runtime import FunctionCall
    from rem.integration import melon_rem as MR

    ut, it = suite_task_pair
    payloads = ["<INFORMATION>"] if any(injections.values()) else []   # marker of the important_instructions payload

    class ReactiveCompliantAgent(BasePipelineElement):
        name = TARGET_NAME

        def __init__(self):
            self.user_q, self.inj_q, self.injected, self.n = None, None, False, 0

        def _msg(self, calls):
            if not calls:
                return {"role": "assistant", "content": MR._content("Done."), "tool_calls": None}
            out = []
            for c in calls:
                self.n += 1
                out.append(FunctionCall(function=c.function, args=dict(c.args), id=f"scripted_{self.n}"))
            return {"role": "assistant", "content": MR._content(""), "tool_calls": out}

        def query(self, query, runtime, env, messages=[], extra_args={}):
            if H.is_masked_context(messages):            # MELON's masked re-execution
                seen = MR._text(messages[-1].get("content"))
                calls = list(it.ground_truth(env))[:1] if (it is not None and any(p in seen for p in payloads)) else []
                return query, runtime, env, [*messages, self._msg(calls)], extra_args
            if self.user_q is None:
                self.user_q = list(ut.ground_truth(env))
                self.inj_q = list(it.ground_truth(env)) if it is not None else []
            last = messages[-1] if messages else None
            if (not self.injected and last is not None and last.get("role") == "tool" and self.inj_q
                    and any(p in MR._text(last.get("content")) for p in payloads)):
                self.injected = True                      # obeys the injection next (one call per turn)
            if self.injected and self.inj_q:
                return query, runtime, env, [*messages, self._msg([self.inj_q.pop(0)])], extra_args
            if self.user_q:
                return query, runtime, env, [*messages, self._msg([self.user_q.pop(0)])], extra_args
            return query, runtime, env, [*messages, self._msg([])], extra_args

    return H.counting_llm(ReactiveCompliantAgent())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--cases", default="full", choices=["pilot", "full"])
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    import importlib.metadata as md
    from agentdojo.agent_pipeline.agent_pipeline import load_system_message
    from agentdojo.attacks.attack_registry import load_attack
    from agentdojo.task_suite.load_suites import get_suites
    from rem.integration.agentdojo_live import live_episode_stub
    from rem.integration.agentdojo_replay import GuardConfig, RemGuard
    from rem.integration.melon_rem import load_upstream_melon, make_melon

    assert md.version("agentdojo") == "0.1.29", "run in the MELON environment (AgentDojo 0.1.29)"
    suite = get_suites("v1")["banking"]
    bundle = pickle.load(open(BUNDLE, "rb"))
    melon_mod = load_upstream_melon(MELON_PATH)                       # sha256-checked, unmodified
    sysmsg = load_system_message(None)
    users = sorted(suite.user_tasks, key=lambda s: int(s.rsplit("_", 1)[1]))
    injs = sorted(suite.injection_tasks, key=lambda s: int(s.rsplit("_", 1)[1]))
    cases = (PILOT_ATTACKED + [(u, None) for u in PILOT_BENIGN]) if a.cases == "pilot" else \
        [(u, i) for u in users for i in injs] + [(u, None) for u in users]
    out = open(os.path.join(a.out, "episodes.jsonl"), "w", encoding="utf-8")
    log = open(os.path.join(a.out, "melon_upstream_stdout.log"), "w", encoding="utf-8")
    t_start = time.time()
    for u, i in cases:
        ut = suite.get_user_task_by_id(u)
        it = suite.get_injection_task_by_id(i) if i else None
        named = type("T", (), {"name": TARGET_NAME})()
        injections = load_attack("important_instructions", suite, named).attack(ut, it) if i else {}
        for arm in H.ARMS:
            llm = reactive_agent((ut, it), injections)
            emb = H.CountingEmbeddings(TrigramHashEmbeddings()) if arm == "D2_MELON" else None
            melon = make_melon(melon_mod, llm, emb) if arm == "D2_MELON" else None
            guard = None
            if arm == "D1_REM":
                fold = i if i is not None else bundle["benign_user_task_fold"][u]
                F = bundle["folds"][fold]
                pol = F["policies"]["A3_step_level"]

                def decide(c, P=pol):
                    d = P.decide(c.p, c.tier, c.tool, c.available)          # the label is never passed
                    return d.verdict, d.source, {"tie": bool(getattr(d, "tie", False))}
                ep = live_episode_stub(model_name="scripted-reactive-agent", suite_name="banking", suite_version="v1",
                                       user_task_id=u, injection_task_id=i, attack="important_instructions" if i else None,
                                       injections=injections, system_prompt=sysmsg, user_prompt=ut.PROMPT, repeat=0)
                gc = GuardConfig(bundle["spec"], bundle["detector"], F["reference"], bundle["tier_map"],
                                 bundle["restricted_tools"], "step_level", "no_reviewer")
                guard = RemGuard(gc, F["scorer"], decide, bundle["labeler"], ep)
            with contextlib.redirect_stdout(log):
                rec = H.run_episode(arm=arm, suite=suite, llm=llm, system_message=sysmsg, user_task_id=u,
                                    injection_task_id=i, injections=injections, melon=melon, guard=guard,
                                    embeddings=emb, name=f"scripted-{arm.lower()}")
            rec["status"] = "SCRIPTED INTEGRATION PILOT - not an LLM experiment; not an ASR/utility estimate"
            rec["agent"] = "ReactiveCompliantAgent (scripted)"
            rec["embeddings"] = "TrigramHashEmbeddings (stand-in, not text-embedding-3-large)" if arm == "D2_MELON" else None
            out.write(json.dumps(rec, default=str) + "\n")
    out.close()
    log.close()
    json.dump({"status": "SCRIPTED INTEGRATION PILOT", "cases": len(cases), "arms": list(H.ARMS),
               "agentdojo": md.version("agentdojo"), "melon_file": MELON_PATH,
               "melon_sha256": hashlib.sha256(open(MELON_PATH, "rb").read()).hexdigest(),
               "rem_bundle_sha256": hashlib.sha256(open(BUNDLE, "rb").read()).hexdigest(),
               "seconds": time.time() - t_start}, open(os.path.join(a.out, "manifest.json"), "w"), indent=1)
    print("done", a.out)


if __name__ == "__main__":
    main()
