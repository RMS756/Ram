"""Non-paid integration test of AgentDyn (SaFo-Lab/AgentDyn), a fork of AgentDojo 0.1.35.

Checks: the fork imports; its defence list; whether the banking suite loads; whether the pipelines of the
external defences it integrates (drift, progent, camel) and of AgentDojo's own defences can be CONSTRUCTED.
No pipeline is queried and no request is sent. OpenAI's client refuses to construct without a key, so a
placeholder string is set inside this process only; it is not a credential and no request is made with it
(api.openai.com is also unreachable from this environment).

Usage: python itest_agentdyn.py <out.json>
"""
import importlib.metadata as md
import importlib.resources
import json
import os
import socket
import sys
from pathlib import Path

os.environ["OPENAI_API_KEY"] = "placeholder-not-a-credential"


class NoNetwork:
    """Fail loudly if construction tries to open a socket."""

    def __enter__(self):
        self._orig = socket.socket.connect
        def guard(*a, **k):
            raise RuntimeError("network access attempted during construction")
        socket.socket.connect = guard
        return self

    def __exit__(self, *exc):
        socket.socket.connect = self._orig


def main(out):
    from agentdojo.agent_pipeline.agent_pipeline import DEFENSES, AgentPipeline, PipelineConfig
    from agentdojo.task_suite.load_suites import get_suite, get_suites
    root = Path(str(importlib.resources.files("agentdojo")))
    res = {"agentdojo_dist_version": md.version("agentdojo"), "package_path": str(root), "defenses": list(DEFENSES),
           "suites_v1": sorted(get_suites("v1").keys()), "defense_dirs": sorted(p.name for p in (root / "defenses").iterdir() if p.is_dir()),
           "banking_v1": None, "construct": {}}
    s = get_suite("v1", "banking")
    res["banking_v1"] = [len(s.user_tasks), len(s.injection_tasks), len(s.tools)]
    for d in [None, "repeat_user_prompt", "spotlighting_with_delimiting", "tool_filter", "transformers_pi_detector",
              "piguard_detector", "prompt_guard_2_detector", "drift", "progent", "camel"]:
        try:
            with NoNetwork():
                cfg = PipelineConfig(llm="gpt-4o-2024-05-13", model_id=None, defense=d, system_message_name=None,
                                     system_message=None, tool_delimiter="tool")
                p = AgentPipeline.from_config(cfg)
            res["construct"][str(d)] = {"ok": True, "pipeline_name": getattr(p, "name", None),
                                        "elements": [type(e).__name__ for e in getattr(p, "elements", [])]}
        except BaseException as e:  # recorded, not hidden
            res["construct"][str(d)] = {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}
    Path(out).write_text(json.dumps(res, indent=1))
    for k, v in res["construct"].items():
        print(k, v.get("ok"), v.get("pipeline_name") or v.get("error"))


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]))
