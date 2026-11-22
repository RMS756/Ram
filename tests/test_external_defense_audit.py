"""Checks of the external-defence audit outputs (REM_EXTERNAL_DEFENSE_AUDIT). They read stored results only."""
import json
from pathlib import Path

import pytest

R = Path(__file__).resolve().parents[1] / "REM_EXTERNAL_DEFENSE_AUDIT" / "results"
FP = ["pypi_0135", "drift_env", "agentdyn", "pypi_0129_melon_env", "progent_fork_0129"]
HAS = all((R / f"fingerprint_{k}.json").exists() for k in FP)


def load(name):
    return json.loads((R / name).read_text())


@pytest.mark.skipif(not HAS, reason="fingerprints absent")
def test_banking_scoring_identical_in_every_environment():
    ref = load("fingerprint_pypi_0135.json")
    for k in FP:
        d = load(f"fingerprint_{k}.json")
        for v in ("v1", "v1.2"):
            assert d["suites"][v]["benign"] == ref["suites"][v]["benign"], (k, v)
            assert d["suites"][v]["pairs"] == ref["suites"][v]["pairs"], (k, v)
            assert d["suites"][v]["n_user_tasks"] == 16 and d["suites"][v]["n_injection_tasks"] == 9


@pytest.mark.skipif(not (R / "itest_drift.json").exists(), reason="drift test absent")
def test_drift_test_is_labelled_and_made_no_model_calls():
    d = load("itest_drift.json")
    assert d["label"].startswith("INTERFACE TEST WITH A SCRIPTED TEST DOUBLE")
    assert d["language_model_calls"] == 0 and d["agentdojo_version"] == "0.1.35"
    assert d["drift_commit"] == "6fd3df4763fad77398c3c273c2a4fe14dd50f7ea"
    assert all("error" not in c for c in d["cases"])


@pytest.mark.skipif(not (R / "itest_progent.json").exists(), reason="progent test absent")
def test_progent_reference_counts_are_internally_consistent():
    d = load("itest_progent.json")
    assert "NOT an ASR" in d["label"] and d["language_model_calls"] == 0
    for v, s in d["versions"].items():
        assert s["summary"]["pairs"] == 144 and s["summary"]["benign_tasks"] == 16
        assert s["summary"]["injection_reference_goal_reached_with_progent"] == sum(x[1] for x in s["pairs"].values())
        assert s["summary"]["benign_reference_utility_with_progent"] == sum(x["utility_with_progent"] for x in s["benign"].values())
    assert "user_task_15" in d["versions"]["v1"]["summary"]["benign_tasks_with_a_blocked_reference_call"]
    assert "user_task_15" not in d["versions"]["v1.2"]["summary"]["benign_tasks_with_a_blocked_reference_call"]


@pytest.mark.skipif(not (R / "environment_check.json").exists(), reason="environment check absent")
def test_no_provider_credentials_were_present():
    d = load("environment_check.json")
    assert not any(d["provider_key_variables_set"].values())
