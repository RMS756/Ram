"""Checks of the comparative evaluation phase (REM_COMPARATIVE_EVALUATION_PHASE). Stored outputs only."""
import collections
import gzip
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "REM_COMPARATIVE_EVALUATION_PHASE"
R = D / "results"
HAS_O1 = (R / "offline_comparison_episodes.jsonl.gz").exists()
RESTRICTED = {"send_money", "schedule_transaction", "update_scheduled_transaction", "update_user_info", "update_password"}


def _hashes(name):
    return {p.strip(): h for h, p in (l.split(maxsplit=1) for l in (D / name).read_text().splitlines())}


def test_frozen_protocol_files_unchanged_or_amended():
    frozen, amended = _hashes("01_PROTOCOL_HASHES.sha256"), _hashes("01a_AMENDMENT_HASHES.sha256")
    for p, h in frozen.items():
        got = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        assert got == amended.get(p, h), p
    for p, h in amended.items():
        assert hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h, p


@pytest.fixture(scope="module")
def o1():
    rows = [json.loads(l) for l in gzip.open(R / "offline_comparison_episodes.jsonl.gz", "rt")]
    return rows, json.loads((R / "offline_comparison_metrics.json").read_text())


@pytest.mark.skipif(not HAS_O1, reason="O1 outputs absent")
def test_o1_counts_recompute_from_episode_records(o1):
    rows, m = o1
    for pop, P in m["populations"].items():
        rs = [r for r in rows if r["population"] == pop]
        att = [r for r in rs if r["injection_task"]]
        ben = [r for r in rs if not r["injection_task"]]
        assert (len(att), len(ben)) == (P["attacked_episodes"], P["benign_episodes"])
        for a, A in P["arms"].items():
            if att:
                assert sum(r["arms"][a]["attack_outcome"] for r in att) == A["replay_attack_outcomes"]
                assert sum(r["arms"][a]["attack_call_released"] for r in att) == A["episodes_attack_call_released"]
            if ben:
                assert sum(r["arms"][a]["utility"] for r in ben) == A["benign_completed"]
                assert sum(r["arms"][a]["any_restricted_withheld"] for r in ben) == A["benign_episodes_with_a_withheld_call"]


@pytest.mark.skipif(not HAS_O1, reason="O1 outputs absent")
def test_o1_shared_arms_reproduce_the_frozen_ablation_episode_by_episode(o1):
    rows, _ = o1
    abl = collections.defaultdict(dict)
    for l in gzip.open(ROOT / "REM_ABLATION_STUDY" / "05_EPISODE_RESULTS.jsonl.gz", "rt"):
        r = json.loads(l)
        if r["arm"] in ("B0", "A0", "A3"):
            abl[(r["population"], r["episode"])][r["arm"]] = (r["replay_utility"], r["replay_attack_outcome"], [c[2] for c in r["calls"]])
    assert len(abl) == len(rows)
    for r in rows:
        for a in ("B0", "A0", "A3"):
            u, s, rel = abl[(r["population"], r["episode"])][a]
            x = r["arms"][a]
            assert (x["utility"], x["attack_outcome"]) == (u, s)
            assert [c[2] for c in x["calls_detail"]] == rel


@pytest.mark.skipif(not HAS_O1, reason="O1 outputs absent")
def test_progent_arm_decides_only_by_progent_and_uses_the_verbatim_policy(o1):
    rows, m = o1
    assert all(c[4] in ("progent_allow", "progent_block") for r in rows for c in r["arms"]["PG"]["calls_detail"])
    blk = (R / "progent_policy_9befb41_block.txt").read_text()
    assert hashlib.sha256(blk.encode()).hexdigest() == m["progent_policy"]["block_sha256"]
    assert m["progent_policy"]["commit"] == "9befb41cbf992b49dbf035cbd3d53eb953d3b351"
    assert "NOT A LIVE ASR" in m["status"]


@pytest.mark.parametrize("name", ["d0_d1_d2_scripted_integration.json", "drift_scripted_integration.json"])
def test_scripted_outputs_are_labelled_and_model_free(name):
    p = R / name
    if not p.exists():
        pytest.skip("absent")
    d = json.loads(p.read_text())
    assert d["label"].startswith("SCRIPTED INTEGRATION TEST") and d["language_model_calls"] == 0
    assert all(v["errors"] == 0 for v in d["summary"].values())
