"""Tests asserting the CLAUDE.md hard design lock holds in code.

These are the tests that matter most for the thesis defence: each one checks a
clause of the contract directly, so a later well-meaning edit that violates the
frozen design fails the suite rather than quietly shipping.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

import rem.core.interfaces as interfaces
import rem.core.pipeline as pipeline_module
from rem.core.mitigation import CANONICAL_MECHANISM
from rem.core.pipeline import AblationSpec, Layer
from rem.core.results import MitigationAction, ScoreSemantics, Verdict
from rem.traceability.registry import (
    RegistryUnavailableError,
    TraceStatus,
    derivation,
    load_registry,
    registered_operations,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# FROZEN ARCHITECTURE — exactly five layers, no feedback layer
# ---------------------------------------------------------------------------


def test_exactly_five_frozen_layers():
    assert len(Layer.FROZEN_LAYERS) == 5
    assert set(Layer.FROZEN_LAYERS) == {
        "context",
        "detection",
        "behavior",
        "decision",
        "mitigation",
    }


def test_there_is_no_feedback_layer():
    """CLAUDE.md: 'There is NO feedback-loop layer.'"""
    assert "feedback" not in Layer.ALL
    assert not hasattr(Layer, "FEEDBACK")
    with pytest.raises(ValueError, match="no feedback layer"):
        AblationSpec.without("feedback")


def test_no_feedback_sink_exists_anywhere():
    """The removed feedback component must not have crept back in."""
    assert not hasattr(interfaces, "FeedbackSink")
    assert not hasattr(interfaces, "InMemoryFeedbackSink")
    source = Path(pipeline_module.__file__).read_text(encoding="utf-8")
    assert "feedback_sink" not in source


def test_pipeline_has_no_risk_score_layer():
    """CLAUDE.md: 'There is NO separate risk-score layer.'"""
    assert "risk_score" not in Layer.ALL


# ---------------------------------------------------------------------------
# FROZEN verdicts and MITIGATION LOCK
# ---------------------------------------------------------------------------


def test_the_four_frozen_verdicts():
    assert [v.value for v in Verdict] == ["allow", "modify", "escalate", "block"]


def test_canonical_mitigation_mapping_is_the_frozen_one():
    assert CANONICAL_MECHANISM[Verdict.ALLOW] is MitigationAction.RELEASE_ACTION
    assert CANONICAL_MECHANISM[Verdict.MODIFY] is MitigationAction.MODIFY_ACTION
    assert CANONICAL_MECHANISM[Verdict.ESCALATE] is MitigationAction.WITHHOLD_PENDING_REVIEW
    assert CANONICAL_MECHANISM[Verdict.BLOCK] is MitigationAction.PREVENT_EXECUTION


def test_canonical_mapping_is_immutable():
    """The verdict-to-mechanism mapping is frozen design, not configuration."""
    with pytest.raises(TypeError):
        CANONICAL_MECHANISM[Verdict.ALLOW] = MitigationAction.PREVENT_EXECUTION  # type: ignore[index]


def test_no_episode_level_mitigation_mechanisms():
    """Episode-level restriction is a separate policy requiring specification."""
    mechanisms = {m.value for m in MitigationAction}
    assert mechanisms == {
        "release_action",
        "modify_action",
        "withhold_pending_review",
        "prevent_execution",
    }
    for forbidden in ("reduce_privilege", "terminate_execution", "restrict_tool"):
        assert forbidden not in mechanisms


# ---------------------------------------------------------------------------
# EQUATION-ID LOCK
# ---------------------------------------------------------------------------


def test_no_authoritative_registry_is_shipped():
    """CLAUDE.md: if the registry is unavailable, STOP — do not synthesise one."""
    assert not (REPO_ROOT / "docs" / "equation_registry.yaml").is_file()
    with pytest.raises(RegistryUnavailableError, match="will not create provisional"):
        load_registry(force=True)


def test_no_equation_ids_appear_in_implementation_code():
    """CLAUDE.md: 'Do not create provisional equation IDs inside implementation code.'"""
    import rem.algorithms.attribution.linear_shapley  # noqa: F401
    import rem.algorithms.calibration.platt  # noqa: F401
    import rem.algorithms.decision.expected_loss  # noqa: F401
    import rem.algorithms.detection.ridge_logistic  # noqa: F401
    import rem.evaluation.metrics  # noqa: F401
    import rem.evaluation.runtime  # noqa: F401

    with_ids = [op for op in registered_operations() if op.equation_id is not None]
    assert with_ids == [], (
        "Provisional equation IDs found in implementation code: "
        f"{[(o.module, o.qualified_name, o.equation_id) for o in with_ids]}"
    )


def test_every_operation_is_awaiting_a_registry_id():
    import rem.evaluation.metrics  # noqa: F401

    operations = registered_operations()
    assert operations, "no mathematical operations were registered"
    assert all(op.status is TraceStatus.AWAITING_REGISTRY_ID for op in operations)


def test_every_operation_carries_a_citation():
    import rem.evaluation.metrics  # noqa: F401

    for op in registered_operations():
        assert op.source.strip(), f"{op.qualified_name} has no source"
        assert op.location.strip(), f"{op.qualified_name} has no location"
        assert op.statement.strip(), f"{op.qualified_name} states no formula"


def test_supplying_an_equation_id_without_a_registry_raises():
    """An ID may never be accepted on trust."""
    with pytest.raises(RegistryUnavailableError):

        @derivation(
            statement="x = 1",
            source="somewhere",
            location="somewhere",
            algorithm="test",
            equation_id="EQ-INVENTED-01",
        )
        def bogus() -> float:
            return 1.0


def test_derivation_requires_full_provenance():
    for kwargs in (
        {"statement": "", "source": "s", "location": "l", "algorithm": "a"},
        {"statement": "x", "source": "", "location": "l", "algorithm": "a"},
        {"statement": "x", "source": "s", "location": "", "algorithm": "a"},
        {"statement": "x", "source": "s", "location": "l", "algorithm": ""},
    ):
        with pytest.raises(ValueError, match="requires a non-empty"):
            derivation(**kwargs)  # type: ignore[arg-type]


def test_traceability_report_does_not_claim_completeness():
    """CLAUDE.md: do not make reports appear complete by inventing identifiers."""
    report = REPO_ROOT / "docs" / "MATHEMATICAL_TRACEABILITY.md"
    if not report.is_file():
        pytest.skip("traceability report not generated yet")
    text = report.read_text(encoding="utf-8")
    assert "AUTHORITATIVE EQUATION IDs      0" in text
    assert "AWAITING REGISTRY ID" in text
    assert "has NOT been supplied" in text


# ---------------------------------------------------------------------------
# FORBIDDEN REINTRODUCTIONS
# ---------------------------------------------------------------------------


FORBIDDEN_SYMBOLS = [
    "IsotonicCalibrat",
    "TemperatureScal",
    "BetaCalibrat",
    "CusumDecision",
    "SPRT",
    "CareEl",
    "CARE_EL",
    "PrefixBranch",
    "Counterfactual",
]


def test_forbidden_components_are_absent_from_the_codebase():
    """CLAUDE.md § FORBIDDEN REINTRODUCTIONS, checked against the source tree."""
    offenders = []
    for path in (REPO_ROOT / "rem").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for symbol in FORBIDDEN_SYMBOLS:
            # Allow mentions inside docstrings/comments that explain the ban;
            # flag only apparent definitions.
            for marker in (f"class {symbol}", f"def {symbol}"):
                if marker in text:
                    offenders.append(f"{path.relative_to(REPO_ROOT)}: {marker}")
    assert offenders == [], f"Forbidden reintroductions found: {offenders}"


def test_no_composite_risk_equation_is_implemented():
    """'risk = p x S' and 'confidence = sum|beta_i|' are forbidden."""
    from rem.core.results import DetectionResult

    fields = set(inspect.signature(DetectionResult).parameters)
    assert "risk" not in fields
    assert "severity" not in fields
    # confidence exists but must default to None, never be derived from betas.
    result = DetectionResult(
        label="x", score=0.5, semantics=ScoreSemantics.CALIBRATED_PROBABILITY, producer="d"
    )
    assert result.confidence is None


def test_evidence_carries_no_weight_or_severity():
    """Aggregation is the fitted model's job, not the data model's."""
    from rem.agent.trajectory import Evidence

    fields = set(inspect.signature(Evidence).parameters)
    assert "weight" not in fields
    assert "severity" not in fields


# ---------------------------------------------------------------------------
# Score semantics — p_t must come from calibration
# ---------------------------------------------------------------------------


def test_only_calibrated_scores_are_calibrated():
    assert ScoreSemantics.CALIBRATED_PROBABILITY.is_calibrated
    assert not ScoreSemantics.UNCALIBRATED_PROBABILITY.is_calibrated
    assert not ScoreSemantics.LOGIT.is_calibrated
    assert not ScoreSemantics.LOGIT.is_probability


def test_decision_engine_signature_excludes_attribution():
    """Attribution must not be reachable by the decision layer, by signature."""
    parameters = set(
        inspect.signature(interfaces.DecisionEngine.decide).parameters
    )
    assert "attribution" not in parameters
    assert "shap" not in parameters
