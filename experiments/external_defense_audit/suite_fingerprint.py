"""Evaluator fingerprint of the AgentDojo banking suite in the interpreter that runs this script.

No language model is called. The script uses AgentDojo's own GroundTruthPipeline (the benchmark's reference
solutions) to record, for every (user task, injection task) pair and every benign user task, the utility and
security values returned by the installed evaluator. Running it in several environments (PyPI AgentDojo 0.1.35,
the AgentDyn fork, AgentDojo 0.1.29) shows whether they score the banking suite identically.

Usage: python suite_fingerprint.py <out.json>
"""
import hashlib
import importlib.metadata as md
import importlib.resources
import json
import sys
from pathlib import Path

from agentdojo.agent_pipeline import GroundTruthPipeline
from agentdojo.task_suite.load_suites import get_suite

VERSIONS = ["v1", "v1.2"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def package_files() -> dict:
    root = Path(str(importlib.resources.files("agentdojo")))
    rels = ["data/suites/banking/environment.yaml", "data/suites/banking/injection_vectors.yaml",
            "default_suites/v1/banking/user_tasks.py", "default_suites/v1/banking/injection_tasks.py",
            "default_suites/v1/banking/task_suite.py", "default_suites/v1/tools/banking_client.py",
            "default_suites/v1_2/banking/injection_tasks.py", "default_suites/v1_1_1/banking/user_tasks.py",
            "data/system_messages.yaml", "task_suite/task_suite.py", "attacks/important_instructions_attacks.py",
            "attacks/baseline_attacks.py"]
    out = {}
    for r in rels:
        p = root / r
        out[r] = sha(p) if p.exists() else None
    return out


def matrix(version: str) -> dict:
    suite = get_suite(version, "banking")
    res = {"n_user_tasks": len(suite.user_tasks), "n_injection_tasks": len(suite.injection_tasks),
           "tools": [t.name for t in suite.tools], "benign": {}, "pairs": {}}
    for ut in suite.user_tasks.values():
        u, s = suite.run_task_with_pipeline(GroundTruthPipeline(ut), ut, injection_task=None, injections={})
        res["benign"][ut.ID] = [bool(u), bool(s)]
    vectors = suite.get_injection_vector_defaults()
    for ut in suite.user_tasks.values():
        for it in suite.injection_tasks.values():
            inj = {k: f"<INFORMATION> {it.GOAL} </INFORMATION>" for k in vectors}
            # reference solution of the user task under injection: utility kept, attack not executed
            u1, s1 = suite.run_task_with_pipeline(GroundTruthPipeline(ut), ut, injection_task=it, injections=inj)
            # reference solution of the injection task: the attacker goal is reached
            u2, s2 = suite.run_task_with_pipeline(GroundTruthPipeline(it), ut, injection_task=it, injections=inj)
            res["pairs"][f"{ut.ID}|{it.ID}"] = [bool(u1), bool(s1), bool(u2), bool(s2)]
    ok, (ur, ir) = suite.check()
    res["suite_check_ok"] = bool(ok)
    res["suite_check_failures"] = {k: v[1] for k, v in ur.items() if not v[0]}
    res["injection_check"] = {k: bool(v) for k, v in ir.items()}
    return res


def main(out: str) -> None:
    data = {"python": sys.version.split()[0], "agentdojo_version": md.version("agentdojo"),
            "agentdojo_path": str(importlib.resources.files("agentdojo")), "files": package_files(), "suites": {}}
    for v in VERSIONS:
        try:
            data["suites"][v] = matrix(v)
        except Exception as e:  # recorded, not hidden
            data["suites"][v] = {"error": f"{type(e).__name__}: {e}"}
    Path(out).write_text(json.dumps(data, indent=1, sort_keys=True))
    for v, m in data["suites"].items():
        if "error" in m:
            print(v, m["error"])
            continue
        print(v, "benign utility", sum(x[0] for x in m["benign"].values()), "/", len(m["benign"]),
              "| pairs u1,s1,u2,s2 sums", [sum(x[i] for x in m["pairs"].values()) for i in range(4)], "/", len(m["pairs"]),
              "| check_ok", m["suite_check_ok"], m["suite_check_failures"])


if __name__ == "__main__":
    main(sys.argv[1])
