"""DRIFT arms of the comparative protocol: D3 (all three DRIFT modules) and D4 (DRIFT agent, modules disabled).

Two modes. Run in the DRIFT venv (/home/user/venvs/drift: agentdojo 0.1.35 + DRIFT requirements.txt).

  --mode scripted   INTEGRATION TEST ONLY. Official DRIFT code (SaFo-Lab/DRIFT@6fd3df4, loaded by path, unmodified)
                    on all 160 banking v1 episodes, with the labelled test-double client of
                    experiments/external_defense_audit/itest_drift.py in place of the LLM. Records errors, tool
                    calls and the model calls DRIFT would make per module. Its utility/security values are set by
                    the scripted answers and are NOT results.
  --mode live       Runs the authors' command line (pipeline_main.py) in a fresh export of the pinned commit, once
                    per repeat, with --benchmark_version v1. REFUSES to start unless the configuration is complete,
                    the provider credential is present, and a spending authorisation and provider-side hard cap are
                    recorded (DRIFT's client has no spending guard; it cannot be capped from outside without editing
                    DRIFT). Never executed in this repository.

usage: DRIFT_UPSTREAM=/home/user/upstream/SaFo-Lab_DRIFT /home/user/venvs/drift/bin/python \
       experiments/comparative_phase/run_drift_arms.py --mode scripted --out <dir>
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PIN = "6fd3df4763fad77398c3c273c2a4fe14dd50f7ea"
REQUIRED = ["model.provider", "model.id", "repeats", "authorisation.record", "authorisation.provider_side_hard_cap_usd",
            "protocol_freeze_commit"]
PROVIDER_KEYS = {"openai": "OPENAI_API_KEY", "google": "GOOGLE_API_KEY", "openrouter": "OPENROUTER_API_KEY"}


def get(cfg, dotted):
    for p in dotted.split("."):
        cfg = cfg.get(p) if isinstance(cfg, dict) else None
    return cfg


def scripted(out: Path):
    sys.path.insert(0, str(REPO / "experiments" / "external_defense_audit"))
    import itest_drift as T   # official DRIFT imported by path inside; chdir to the DRIFT checkout
    from agentdojo.task_suite.load_suites import get_suite

    class ArgsOff:
        build_constraints = injection_isolation = dynamic_validation = adaptive_attack = False

    suite = get_suite("v1", "banking")
    users = sorted(suite.user_tasks, key=lambda x: int(x.split("_")[-1]))
    injs = sorted(suite.injection_tasks, key=lambda x: int(x.split("_")[-1]))
    rows = []
    settings = [("D3", "S1_detector_finds_nothing_judge_no", "none", "No"), ("D3", "S2_detector_echoes_goal_judge_yes", "echo", "Yes"),
                ("D4", "modules_off", "none", "Yes")]
    for arm, sname, det, judge in settings:
        if arm == "D4":
            T.Args, saved = ArgsOff, T.Args          # the official command line without the three module flags
        for u in users:
            for i in [None] + injs:
                t0 = time.perf_counter()
                try:
                    r = T.run_case("v1", u, i, det, judge)
                    r["error"] = None
                except Exception as e:      # recorded, never dropped
                    r = {"user_task": u, "injection_task": i, "error": f"{type(e).__name__}: {str(e)[:300]}"}
                r.update(arm=arm, setting=sname, wall_s=round(time.perf_counter() - t0, 3))
                r.pop("drift_log_tail", None)
                rows.append(r)
        if arm == "D4":
            T.Args = saved
    summ = {}
    for arm, sname, _, _ in settings:
        rs = [r for r in rows if r["arm"] == arm and r["setting"] == sname]
        mods = {}
        for r in rs:
            for k, v in (r.get("test_double_calls_by_drift_module") or {}).items():
                mods[k] = mods.get(k, 0) + v
        summ[f"{arm}:{sname}"] = {"episodes": len(rs), "errors": sum(1 for r in rs if r["error"]),
                                  "tool_calls_executed": sum(len(r.get("executed_tool_calls", [])) for r in rs),
                                  "drift_refusals": sum(len(r.get("drift_refusals", [])) for r in rs),
                                  "model_calls_by_module_total": mods,
                                  "model_calls_per_episode_mean": round(sum(mods.values()) / max(1, len(rs)), 2)}
    data = {"label": "SCRIPTED INTEGRATION TEST (test-double model) - NOT A SECURITY OR UTILITY RESULT",
            "drift_commit": PIN, "benchmark_version": "v1", "language_model_calls": 0, "summary": summ, "episodes": rows}
    out.mkdir(parents=True, exist_ok=True)
    (out / "drift_scripted_integration.json").write_text(json.dumps(data, indent=1, default=str))
    print(json.dumps(summ, indent=1))


def live(cfg_path: str, out: Path):
    import yaml
    cfg = yaml.safe_load(open(cfg_path))
    gaps = [k for k in REQUIRED if get(cfg, k) in (None, "", "REQUIRED_FROM_SUPERVISOR")]
    if gaps:
        for g in gaps:
            print(f"[DESIGN BLOCKED] {g}: not specified", file=sys.stderr)
        sys.exit(2)
    key = PROVIDER_KEYS.get(get(cfg, "model.provider"))
    if not key or not os.environ.get(key):
        print("credential for the configured provider is not set; no call is made", file=sys.stderr)
        sys.exit(3)
    up = Path(os.environ["DRIFT_UPSTREAM"])
    head = subprocess.run(["git", "-C", str(up), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != PIN:
        print(f"DRIFT checkout at {head}, pinned {PIN}", file=sys.stderr)
        sys.exit(4)
    for rep in range(int(cfg["repeats"])):
        for arm, flags in (("D3", ["--build_constraints", "--injection_isolation", "--dynamic_validation"]), ("D4", [])):
            wd = out / f"{arm}_rep{rep}"
            wd.mkdir(parents=True, exist_ok=False)
            subprocess.run(f"git -C {up} archive {PIN} | tar -x -C {wd}", shell=True, check=True)
            for attack in (False, True):
                cmd = [sys.executable, "pipeline_main.py", "--model", cfg["model"]["id"], "--benchmark_version", "v1",
                       "--suites", "banking", "--seed", str(cfg.get("drift_seed", 98)), *flags]
                if attack:
                    cmd += ["--do_attack", "--attack_type", "important_instructions"]
                subprocess.run(cmd, cwd=wd, check=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["scripted", "live"], required=True)
    ap.add_argument("--config")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.mode == "scripted":
        scripted(Path(a.out).resolve())
    else:
        if not a.config:
            sys.exit("--config is required for --mode live")
        live(a.config, Path(a.out).resolve())
