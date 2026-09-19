"""Tests for reproducibility support."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from rem.utils.reproducibility import (
    EnvironmentManifest,
    file_digest,
    new_experiment_id,
    seed_everything,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_seeding_makes_runs_reproducible():
    seed_everything(1234)
    first = [random.random() for _ in range(5)]
    seed_everything(1234)
    assert first == [random.random() for _ in range(5)]


def test_different_seeds_differ():
    seed_everything(1)
    first = [random.random() for _ in range(5)]
    seed_everything(2)
    assert first != [random.random() for _ in range(5)]


def test_seed_report_names_the_sources():
    report = seed_everything(7)
    assert report["seed"] == 7
    assert report["python_random"] is True
    assert report["numpy"] is not None


def test_experiment_ids_are_prefixed():
    assert new_experiment_id("ablation").startswith("ablation-")


def test_file_digest_detects_change(tmp_path: Path):
    path = tmp_path / "data.csv"
    path.write_text("a,b\n1,2\n", encoding="utf-8")
    original = file_digest(path)
    assert original and len(original) == 64
    path.write_text("a,b\n1,3\n", encoding="utf-8")
    assert file_digest(path) != original


def test_file_digest_missing_file_is_none(tmp_path: Path):
    assert file_digest(tmp_path / "absent.csv") is None


def test_manifest_records_the_contract_digest():
    """A run must record which frozen design it was produced under."""
    manifest = EnvironmentManifest.capture("exp-test", seed=42)
    assert manifest.contract_digest is not None
    assert manifest.contract_digest == file_digest(REPO_ROOT / "CLAUDE.md")


def test_manifest_captures_environment(tmp_path: Path):
    dataset = tmp_path / "dataset.jsonl"
    dataset.write_text("{}\n", encoding="utf-8")
    manifest = EnvironmentManifest.capture("exp-test", seed=42, dataset_files=[dataset])
    assert manifest.experiment_id == "exp-test"
    assert manifest.seed == 42
    assert manifest.rem_version
    assert manifest.dataset_files[str(dataset)] is not None
    assert manifest.dependencies


def test_manifest_round_trips_to_disk(tmp_path: Path):
    manifest = EnvironmentManifest.capture("exp-test", seed=1)
    path = manifest.save(tmp_path / "runs" / "manifest.json")
    assert path.is_file()
    assert '"experiment_id": "exp-test"' in path.read_text(encoding="utf-8")
