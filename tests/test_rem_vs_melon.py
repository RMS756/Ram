"""Tests of the REM vs MELON three-arm harness and fail-closed runner (MELON environment: AgentDojo 0.1.29).

Scripted agents and a stand-in embedding client are used; nothing here is an LLM result.
"""
import hashlib
import importlib.metadata as md
import json
import os
import subprocess
import sys

import pytest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HERE = os.path.join(REPO, "experiments", "rem_vs_melon")
MELON_FILE = "/home/user/ucsb-mlsec/melon/pi_detector.py"
pytestmark = pytest.mark.skipif(
    md.version("agentdojo") != "0.1.29" or not os.path.exists(MELON_FILE),
    reason="runs in the MELON environment (AgentDojo 0.1.29) with the upstream clone present")
sys.path.insert(0, HERE)
sys.path.insert(0, REPO)
RUNNER = os.path.join(HERE, "run_rem_vs_melon.py")


def _run(cfg, tmp_path, *extra):
    import yaml
    p = tmp_path / "cfg.yaml"
    p.write_text(yaml.safe_dump(cfg))
    r = subprocess.run([sys.executable, RUNNER, "--config", str(p), "--out", str(tmp_path / "out"), *extra],
                       capture_output=True, text=True, cwd=REPO)
    return r


def _filled(provider="openai_compatible"):
    import yaml
    cfg = yaml.safe_load(open(os.path.join(HERE, "config_TEMPLATE.yaml")))
    cfg.update(run_id="test", order={"seed": 1})
    cfg["benchmark"]["case_set"] = "full"
    cfg["models"].update(provider=provider, base_url="http://127.0.0.1:9/v1", backbone="test-model", temperature=0.0,
                         repeats=1, request_timeout_s=5, max_retries=0, melon_embeddings="local_openai_compatible",
                         embedding_base_url="http://127.0.0.1:9/v1", embedding_model="test-emb")
    cfg["rem"]["bundle_path"] = os.path.join(REPO, cfg["rem"]["bundle_path"])
    cfg["budget"] = {}
    return cfg


def test_upstream_melon_file_is_the_official_unmodified_one():
    from rem.integration.melon_rem import UPSTREAM_MELON_SHA256
    assert hashlib.sha256(open(MELON_FILE, "rb").read()).hexdigest() == UPSTREAM_MELON_SHA256
    if os.path.exists("/home/user/upstream/MELON/pi_detector.py"):      # both official repositories carry the same file
        assert hashlib.sha256(open("/home/user/upstream/MELON/pi_detector.py", "rb").read()).hexdigest() == UPSTREAM_MELON_SHA256


def test_template_is_fail_closed(tmp_path):
    import yaml
    r = _run(yaml.safe_load(open(os.path.join(HERE, "config_TEMPLATE.yaml"))), tmp_path, "--dry-run")
    assert r.returncode == 2 and "[DESIGN BLOCKED]" in r.stderr


def test_filled_local_config_plans_480_paired_episodes(tmp_path):
    r = _run(_filled(), tmp_path, "--dry-run")
    assert r.returncode == 0, r.stderr
    assert "planned episodes: 480 (160 triples x 3 arms)" in r.stdout
    assert "MELON-ADAPTED-EMBEDDINGS" in r.stdout          # a non-original embedding model is never labelled MELON


def test_unreachable_endpoint_stops_before_any_episode(tmp_path):
    r = _run(_filled(), tmp_path)
    assert r.returncode == 3 and "not reachable" in r.stderr
    assert not (tmp_path / "out" / "episodes.jsonl").exists()


def test_paid_provider_without_authorisation_is_blocked(tmp_path):
    cfg = _filled(provider="openai")
    cfg["models"]["melon_embeddings"] = "original_openai"
    r = _run(cfg, tmp_path, "--dry-run")
    assert r.returncode == 2 and "budget.authorization_reference" in r.stderr


def test_plan_is_paired_and_balanced():
    import yaml
    from agentdojo.task_suite.load_suites import get_suites
    import run_rem_vs_melon as RR
    cfg = _filled()
    s = RR.plan(cfg, get_suites("v1")["banking"])
    by = {}
    for e in s:
        by.setdefault(e["triple_id"], []).append(e)
    assert all(sorted(x["arm"] for x in v) == sorted(RR.ARMS) for v in by.values())
    assert all(len({(x["user_task"], x["injection_task"]) for x in v}) == 1 for v in by.values())


def test_pipelines_differ_only_at_the_intended_point():
    import harness as H
    from agentdojo.agent_pipeline import ToolsExecutor
    from rem.integration.melon_rem import load_upstream_melon, make_melon
    import pilot_scripted as P
    llm = H.counting_llm(type("L", (), {"name": "x", "query": lambda *a: a})())
    melon = make_melon(load_upstream_melon(MELON_FILE), llm, P.TrigramHashEmbeddings())
    _, ex0 = H.build_pipeline("D0_NO_DEFENSE", llm=llm, system_message="s", name="a")
    p2, ex2 = H.build_pipeline("D2_MELON", llm=llm, system_message="s", melon=melon, name="c")
    assert type(ex0) is ToolsExecutor and type(ex2) is ToolsExecutor
    assert type(melon).__name__ == "MELON" and type(melon).__module__ == "melon_upstream_pi_detector"
    with pytest.raises(ValueError):
        H.build_pipeline("D1_REM", llm=llm, system_message="s", name="b")          # REM arm needs a guard


def test_scripted_pilot_exercises_every_mechanism(tmp_path):
    r = subprocess.run([sys.executable, os.path.join(HERE, "pilot_scripted.py"), str(tmp_path), "--cases", "pilot"],
                       capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0, r.stderr[-2000:]
    rows = [json.loads(l) for l in open(tmp_path / "episodes.jsonl")]
    assert len(rows) == 13 * 3 and all(x["error"] is None for x in rows)
    att = lambda arm: [x for x in rows if x["arm"] == arm and x["injection_task"]]   # noqa: E731
    assert sum(x["security"] for x in att("D0_NO_DEFENSE")) > 0                 # the payload reaches the agent
    rem = att("D1_REM")
    assert all(len(x["rem_latency_ms"]) >= x["calls_executed"] for x in rem)    # every executed call was evaluated
    assert any(x["calls_refused_by_rem"] for x in rem)
    mel = att("D2_MELON")
    assert all(x["llm_calls_melon_masked"] >= 1 for x in mel)                   # MELON's masked re-execution ran
    assert any(x["melon_flagged"] for x in mel) and all(x["embedding_calls"] >= 1 for x in mel if x["melon_flagged"])
    assert all(x["llm_calls_melon_masked"] == 0 for x in rows if x["arm"] != "D2_MELON")


def test_analysis_refuses_to_label_scripted_output_as_live(tmp_path):
    pilot = tmp_path / "p"
    r = subprocess.run([sys.executable, os.path.join(HERE, "pilot_scripted.py"), str(pilot), "--cases", "pilot"],
                       capture_output=True, text=True, cwd=REPO)
    assert r.returncode == 0
    a = subprocess.run([sys.executable, os.path.join(HERE, "analyze_live.py"), str(pilot), str(tmp_path / "o")],
                       capture_output=True, text=True, cwd=REPO)
    assert a.returncode != 0 and "not a LIVE RUN" in (a.stderr + a.stdout)
    a = subprocess.run([sys.executable, os.path.join(HERE, "analyze_live.py"), str(pilot), str(tmp_path / "o"), "--diagnostic"],
                       capture_output=True, text=True, cwd=REPO)
    assert a.returncode == 0
    assert all(row.startswith("SCRIPTED-DIAGNOSTIC") for row in open(tmp_path / "o" / "rem_melon_results.csv").read().splitlines()[1:])
