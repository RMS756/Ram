"""Reproducibility manifest of the controlled improvement study (18 November 2026).

Records, from the files themselves: git commits, SHA-256 of every code file the arms and runners use, versions of the
Python packages involved, the AgentDojo installations (installed package vs Progent fork vs trace repository), the banking
task definitions (hash of each task's PROMPT / GOAL and of the suite source files) and the environment variables that
select state (names only; no values that could be secrets).
usage: python3 manifest.py <out.json>
"""
import hashlib
import importlib.metadata as md
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE = ["experiments/progent_competitive", "experiments/improvement_controlled", "experiments/repair_study", "experiments/improve_study",
        "experiments/competitive_study", "experiments/g3_integration", "experiments/pilot", "experiments/authz_study", "rem",
        "tests/test_progent_competitive.py", "tests/test_progent_competitive_amend1.py"]
PKGS = ["agentdojo", "numpy", "scipy", "scikit-learn", "pydantic", "jsonschema", "pyyaml", "openai", "anthropic", "langchain-core",
        "z3-solver", "docstring-parser"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a, cwd=ROOT):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True).stdout.strip()


def main(out):
    files = {}
    for c in CODE:
        p = ROOT / c
        for f in ([p] if p.is_file() else sorted(p.rglob("*.py"))):
            if "__pycache__" not in f.parts:
                files[str(f.relative_to(ROOT))] = sha(f)
    vers = {}
    for k in PKGS:
        try:
            vers[k] = md.version(k)
        except md.PackageNotFoundError:
            vers[k] = None
    import agentdojo
    sys.path.insert(0, str(ROOT / "experiments" / "pilot"))
    import common
    st = common.make_setup()
    suite = st.suite
    tasks = {"user_tasks": {u: hashlib.sha256(suite.get_user_task_by_id(u).PROMPT.encode()).hexdigest()[:16] for u in sorted(suite.user_tasks)},
             "injection_tasks": {i: hashlib.sha256(suite.get_injection_task_by_id(i).GOAL.encode()).hexdigest()[:16] for i in sorted(suite.injection_tasks)}}
    banking_dir = Path(agentdojo.__file__).parent / "default_suites" / "v1" / "banking"
    up = os.environ.get("PROGENT_UPSTREAM", "/home/user/upstream/sunblaze-ucb_progent")
    out_d = {
        "generated_by": "experiments/improvement_controlled/manifest.py",
        "git": {"branch": git("branch", "--show-current"), "head": git("rev-parse", "HEAD"),
                "frozen_commits_verified": {c: git("cat-file", "-t", c) == "commit" for c in ("bdde9d0", "0009d09", "5e91233", "e876962")}},
        "python": sys.version.split()[0], "platform": platform.platform(), "packages": vers,
        "agentdojo": {"installed_package": {"version": vers["agentdojo"], "path": str(Path(agentdojo.__file__).parent),
                                            "banking_suite_files_sha256": {f.name: sha(f) for f in sorted(banking_dir.glob("*.py"))}},
                      "trace_repository": {"path": "/home/user/ethz-spylab/agentdojo", "commit": git("rev-parse", "HEAD", cwd="/home/user/ethz-spylab/agentdojo"),
                                           "describe": git("describe", "--tags", cwd="/home/user/ethz-spylab/agentdojo")},
                      "progent_fork": {"path": up, "commit": git("rev-parse", "HEAD", cwd=up) if os.path.isdir(up) else None,
                                       "agentdojo_version_in_fork": "0.1.29 (agentdojo/pyproject.toml)", "installed": False}},
        "banking_tasks": tasks,
        "state_environment_variables_present": sorted(k for k in ("PYTHONHASHSEED", "PROGENT_UPSTREAM", "PILOT_RESULTS_DIR", "AUTHZ_STATE",
                                                                 "IMPROVE_STATE", "INTEGRATION_STATE", "AGENTDOJO_RUNS", "COMPETITIVE_STATE") if k in os.environ),
        "code_sha256": files,
    }
    Path(out).write_text(json.dumps(out_d, indent=1), encoding="utf-8")
    print("files", len(files), "agentdojo", vers["agentdojo"], "head", out_d["git"]["head"][:7], out_d["git"]["frozen_commits_verified"])


if __name__ == "__main__":
    main(sys.argv[1])
