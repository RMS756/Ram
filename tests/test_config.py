"""Tests for configuration loading and provenance enforcement."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from rem.config.loader import (
    REQUIRED,
    MalformedParameterError,
    UnspecifiedParameterError,
    load_config,
    load_directory,
)

CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs"


def _write(tmp_path: Path, body: dict) -> Path:
    path = tmp_path / "cfg.yaml"
    path.write_text(yaml.safe_dump(body), encoding="utf-8")
    return path


def test_parameter_without_source_is_rejected(tmp_path: Path):
    path = _write(
        tmp_path,
        {"decision": {"loss": {"value": 1.0, "meaning": "m", "justification": "j"}}},
    )
    with pytest.raises(MalformedParameterError, match="source"):
        load_config(path)


def test_parameter_without_justification_is_rejected(tmp_path: Path):
    path = _write(
        tmp_path, {"decision": {"loss": {"value": 1.0, "meaning": "m", "source": "s"}}}
    )
    with pytest.raises(MalformedParameterError, match="justification"):
        load_config(path)


def test_parameter_without_value_is_rejected(tmp_path: Path):
    path = _write(
        tmp_path,
        {"decision": {"l": {"meaning": "m", "source": "s", "justification": "j"}}},
    )
    with pytest.raises(MalformedParameterError, match="no 'value'"):
        load_config(path)


def test_resolved_parameter_reads_back(tmp_path: Path):
    path = _write(
        tmp_path,
        {
            "detection": {
                "algorithm": {
                    "value": "ridge_logistic_regression",
                    "meaning": "m",
                    "source": "CLAUDE.md MATHEMATICAL LOCK",
                    "justification": "j",
                    "status": "FROZEN",
                }
            }
        },
    )
    config = load_config(path)
    assert config["detection"].value("algorithm") == "ridge_logistic_regression"
    assert config["detection"]["algorithm"].status == "FROZEN"


def test_unresolved_value_reports_design_blocked(tmp_path: Path):
    path = _write(
        tmp_path,
        {
            "decision": {
                "loss_grid": {
                    "value": REQUIRED,
                    "meaning": "L(v, y, k)",
                    "source": REQUIRED,
                    "justification": "j",
                    "status": "UNVERIFIED",
                }
            }
        },
    )
    config = load_config(path)
    with pytest.raises(UnspecifiedParameterError, match="DESIGN BLOCKED"):
        config["decision"].value("loss_grid")


def test_value_without_source_is_still_inadmissible(tmp_path: Path):
    """A number with no citation must not be usable, however plausible."""
    path = _write(
        tmp_path,
        {
            "detection": {
                "lambda": {
                    "value": 1.0,
                    "meaning": "m",
                    "source": REQUIRED,
                    "justification": "j",
                }
            }
        },
    )
    config = load_config(path)
    with pytest.raises(UnspecifiedParameterError, match="no academic or specification source"):
        config["detection"].value("lambda")


def test_require_fully_resolved_lists_every_gap(tmp_path: Path):
    path = _write(
        tmp_path,
        {
            "d": {
                "a": {"value": REQUIRED, "meaning": "A", "source": "s", "justification": "j"},
                "b": {"value": REQUIRED, "meaning": "B", "source": "s", "justification": "j"},
            }
        },
    )
    config = load_config(path)
    with pytest.raises(UnspecifiedParameterError) as excinfo:
        config.require_fully_resolved()
    assert "d.a" in str(excinfo.value) and "d.b" in str(excinfo.value)


def test_unknown_key_names_the_problem(tmp_path: Path):
    path = _write(
        tmp_path,
        {"d": {"a": {"value": 1, "meaning": "m", "source": "s", "justification": "j"}}},
    )
    config = load_config(path)
    with pytest.raises(KeyError, match="must be declared in configs"):
        config["d"]["nope"]
    with pytest.raises(KeyError, match="No configuration section"):
        config["nope"]


# --- the shipped configuration files ---------------------------------------


def test_shipped_configs_all_parse():
    configs = load_directory(CONFIG_DIR)
    assert set(configs) == {
        "attribution",
        "behavior",
        "calibration",
        "decision",
        "detection",
        "experiment",
        "mitigation",
    }


def test_shipped_configs_declare_full_provenance():
    for name, config in load_directory(CONFIG_DIR).items():
        for section in config.values():
            for key, parameter in section.items():
                where = f"{name}:{section.name}.{key}"
                assert parameter.meaning.strip(), f"{where} lacks meaning"
                assert parameter.source.strip(), f"{where} lacks source"
                assert parameter.justification.strip(), f"{where} lacks justification"
                assert parameter.status in {"FROZEN", "PD", "UNVERIFIED", "CONFLICT"}


def test_frozen_algorithms_are_recorded_as_frozen():
    """The algorithms CLAUDE.md freezes must be marked FROZEN, not guessed."""
    configs = load_directory(CONFIG_DIR)
    assert configs["detection"]["detection"]["algorithm"].status == "FROZEN"
    assert configs["detection"]["detection"].value("algorithm") == "ridge_logistic_regression"
    assert configs["calibration"]["calibration"].value("method") == "platt_on_logit"
    assert configs["decision"]["decision"].value("mechanism") == "expected_loss_bayes"
    assert configs["attribution"]["attribution"].value("method") == "linear_shapley"
    assert configs["attribution"]["attribution"].value("role") == "audit_only"


def test_blocked_items_are_unresolved_not_defaulted():
    """Every item CLAUDE.md lists as unresolved must stay unresolved."""
    configs = load_directory(CONFIG_DIR)
    for config_name, section, key in [
        ("detection", "detection", "ridge_penalty_lambda"),
        ("detection", "detection", "feature_set"),
        ("detection", "detection", "injection_classifier"),
        ("decision", "decision", "loss_grid"),
        ("decision", "decision", "consequence_tiers"),
        ("decision", "decision", "policy_predicates"),
        ("mitigation", "mitigation", "modify_mechanism"),
        ("experiment", "experiment", "agentdojo_version"),
        ("experiment", "experiment", "grouping_scheme"),
        ("experiment", "experiment", "number_of_repeats"),
    ]:
        parameter = configs[config_name][section][key]
        assert parameter.value == REQUIRED, (
            f"{config_name}.{key} has been given a value ({parameter.value!r}) "
            "though the design leaves it unresolved."
        )
        assert parameter.status == "UNVERIFIED"


def test_cusum_is_observe_only():
    configs = load_directory(CONFIG_DIR)
    assert configs["behavior"]["behavior"].value("cusum_status") == "optional_observe_only"


def test_operating_point_is_baseline_only():
    configs = load_directory(CONFIG_DIR)
    assert configs["detection"]["detection"].value("operating_point_policy") == "baseline_only"


def test_mitigation_scope_is_step_level():
    configs = load_directory(CONFIG_DIR)
    assert configs["mitigation"]["mitigation"].value("scope") == "step_level"
