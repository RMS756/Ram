"""Tests for the FROZEN mathematical core.

Each frozen equation from ``CLAUDE.md`` § MATHEMATICAL LOCK is checked against
hand-computed values, and the contract's guard conditions (gamma_1 > 0,
attribution audit-only, fail-closed on unresolved inputs) are checked directly.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from rem.agent.trajectory import AgentState, ToolCall, Trajectory, TrajectoryStep
from rem.algorithms.attribution.linear_shapley import LinearShapleyAttributor
from rem.algorithms.calibration.platt import (
    MonotonicityViolationError,
    PlattLogitCalibrator,
)
from rem.algorithms.decision.expected_loss import (
    ExpectedLossDecisionEngine,
    LossGrid,
    VerdictTieError,
)
from rem.algorithms.detection.ridge_logistic import (
    NotFittedError,
    RidgeLogisticRegression,
    sigmoid,
)
from rem.core.interfaces import DesignNotSpecifiedError, FeatureVector
from rem.core.results import DetectionResult, ScoreSemantics, Verdict


# ---------------------------------------------------------------------------
# Ridge logistic regression — s_t = b0 + b^T x_t, p~ = sigmoid(s_t)
# ---------------------------------------------------------------------------


def test_sigmoid_matches_definition():
    assert sigmoid(0.0) == pytest.approx(0.5)
    assert sigmoid(1.0) == pytest.approx(1.0 / (1.0 + math.exp(-1.0)))
    assert sigmoid(-1.0) == pytest.approx(1.0 / (1.0 + math.exp(1.0)))


def test_sigmoid_is_overflow_safe():
    """Large |z| must not overflow; the naive exp form would."""
    values = sigmoid(np.array([-1e4, 0.0, 1e4]))
    assert values[0] == pytest.approx(0.0)
    assert values[1] == pytest.approx(0.5)
    assert values[2] == pytest.approx(1.0)
    assert np.all(np.isfinite(values))


def test_decision_function_is_the_frozen_linear_form():
    """s_t = b0 + b^T x_t, checked against a hand-set parameter vector."""
    model = RidgeLogisticRegression(["a", "b"], penalty=1.0)
    model.fit([[0.0, 0.0], [1.0, 1.0], [2.0, 0.0], [0.0, 2.0]], [0, 1, 1, 0])
    b0, beta = model.intercept, model.coefficients
    x = [0.7, -0.3]
    assert model.decision_function(x) == pytest.approx(b0 + beta[0] * x[0] + beta[1] * x[1])


def test_uncalibrated_probability_is_sigmoid_of_the_logit():
    model = RidgeLogisticRegression(["a"], penalty=0.5)
    model.fit([[0.0], [1.0], [2.0], [3.0]], [0, 0, 1, 1])
    x = [1.5]
    assert model.uncalibrated_probability(x) == pytest.approx(
        float(sigmoid(model.decision_function(x)))
    )


def test_fit_without_penalty_is_design_blocked():
    """lambda is unresolved; a library default must not be adopted."""
    model = RidgeLogisticRegression(["a"])
    with pytest.raises(DesignNotSpecifiedError, match="ridge penalty lambda"):
        model.fit([[0.0], [1.0]], [0, 1])


def test_zero_penalty_is_not_ridge():
    model = RidgeLogisticRegression(["a"], penalty=0.0)
    with pytest.raises(ValueError, match="not the frozen ridge estimator"):
        model.fit([[0.0], [1.0]], [0, 1])


def test_scoring_before_fitting_raises():
    with pytest.raises(NotFittedError):
        RidgeLogisticRegression(["a"], penalty=1.0).decision_function([1.0])


def test_ridge_penalty_shrinks_coefficients():
    """Larger lambda must shrink the slope — the defining property of ridge."""
    X = [[0.0], [1.0], [2.0], [3.0], [4.0], [5.0]]
    y = [0, 0, 0, 1, 1, 1]
    weak = RidgeLogisticRegression(["a"], penalty=0.01).fit(X, y)
    strong = RidgeLogisticRegression(["a"], penalty=100.0).fit(X, y)
    assert abs(strong.coefficients[0]) < abs(weak.coefficients[0])


def test_intercept_is_unpenalised():
    """With a huge penalty the slope collapses but the intercept still fits."""
    X = [[0.0], [1.0], [0.0], [1.0]]
    y = [1, 1, 1, 0]  # base rate 3/4
    model = RidgeLogisticRegression(["a"], penalty=1e6).fit(X, y)
    assert abs(model.coefficients[0]) < 1e-3
    # Intercept should approach logit of the base rate, not zero.
    assert model.intercept == pytest.approx(math.log(3.0), abs=0.05)


def test_fit_converges_and_validates_shapes():
    model = RidgeLogisticRegression(["a", "b"], penalty=1.0)
    model.fit([[0.0, 1.0], [1.0, 0.0]], [0, 1])
    assert model.converged
    with pytest.raises(ValueError, match="columns"):
        RidgeLogisticRegression(["a"], penalty=1.0).fit([[0.0, 1.0]], [0])
    with pytest.raises(ValueError, match="Labels must be 0 or 1"):
        RidgeLogisticRegression(["a"], penalty=1.0).fit([[0.0], [1.0]], [0, 2])


def test_detector_emits_no_thresholded_label():
    """The frozen design takes the verdict from the Bayes rule, not a 0.5 cut."""
    model = RidgeLogisticRegression(["a"], penalty=1.0).fit(
        [[0.0], [1.0], [2.0], [3.0]], [0, 0, 1, 1]
    )
    result = model.detect(FeatureVector({"a": 3.0}, "test"), TrajectoryStep(0))
    assert result.label == "unthresholded"
    assert result.semantics is ScoreSemantics.UNCALIBRATED_PROBABILITY
    assert result.logit is not None


def test_detector_refuses_missing_features():
    model = RidgeLogisticRegression(["a", "b"], penalty=1.0).fit(
        [[0.0, 0.0], [1.0, 1.0]], [0, 1]
    )
    with pytest.raises(KeyError, match="does not impute"):
        model.detect(FeatureVector({"a": 1.0}, "test"), TrajectoryStep(0))


# ---------------------------------------------------------------------------
# Platt calibration — p_t = sigmoid(gamma_1 * s_t + gamma_0), gamma_1 > 0
# ---------------------------------------------------------------------------


@pytest.fixture
def calibrator():
    logits = [-4.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 4.0]
    labels = [0, 0, 0, 0, 1, 1, 1, 1]
    return PlattLogitCalibrator().fit(logits, labels)


def test_platt_produces_the_frozen_form(calibrator):
    s = 1.25
    expected = 1.0 / (1.0 + math.exp(-(calibrator.gamma_1 * s + calibrator.gamma_0)))
    assert calibrator.calibrate(s) == pytest.approx(expected)


def test_platt_slope_is_positive(calibrator):
    """CLAUDE.md requires gamma_1 > 0 for the monotone interpretation."""
    assert calibrator.gamma_1 > 0.0


def test_platt_is_monotone_increasing(calibrator):
    scores = [-5.0, -1.0, 0.0, 1.0, 5.0]
    probabilities = [calibrator.calibrate(s) for s in scores]
    assert probabilities == sorted(probabilities)


def test_platt_rejects_an_inverted_detector():
    """An inverted detector yields gamma_1 < 0, which must be refused."""
    logits = [-4.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 4.0]
    inverted = [1, 1, 1, 1, 0, 0, 0, 0]
    with pytest.raises(MonotonicityViolationError, match="gamma_1 > 0"):
        PlattLogitCalibrator().fit(logits, inverted)


def test_platt_requires_both_classes():
    with pytest.raises(ValueError, match="both classes"):
        PlattLogitCalibrator().fit([1.0, 2.0], [1, 1])


def test_platt_smoothed_targets_keep_separable_data_finite():
    """Perfectly separable scores must still yield a finite, usable map."""
    logits = [-10.0, -9.0, 9.0, 10.0]
    labels = [0, 0, 1, 1]
    fitted = PlattLogitCalibrator().fit(logits, labels)
    assert math.isfinite(fitted.gamma_0)
    assert math.isfinite(fitted.gamma_1)
    assert 0.0 < fitted.calibrate(0.0) < 1.0


def test_transform_marks_the_score_calibrated(calibrator):
    raw = DetectionResult(
        label="unthresholded",
        score=0.9,
        semantics=ScoreSemantics.UNCALIBRATED_PROBABILITY,
        producer="detector",
        logit=2.0,
    )
    out = calibrator.transform(raw)
    assert out.semantics is ScoreSemantics.CALIBRATED_PROBABILITY
    assert out.score == pytest.approx(calibrator.calibrate(2.0))
    assert out.logit == 2.0


def test_transform_requires_a_logit(calibrator):
    """The frozen design calibrates on the logit, not on a probability."""
    raw = DetectionResult(
        label="x",
        score=0.9,
        semantics=ScoreSemantics.UNCALIBRATED_PROBABILITY,
        producer="detector",
        logit=None,
    )
    with pytest.raises(ValueError, match="calibrates on the logit"):
        calibrator.transform(raw)


def test_calibrating_before_fitting_raises():
    with pytest.raises(RuntimeError, match="not fitted"):
        PlattLogitCalibrator().calibrate(1.0)


# ---------------------------------------------------------------------------
# Expected-loss Bayes verdict
# ---------------------------------------------------------------------------


def _grid(**overrides: float) -> LossGrid:
    """A complete single-tier loss grid for testing the frozen rule."""
    base = {
        (Verdict.ALLOW, 0, "t1"): 0.0,
        (Verdict.ALLOW, 1, "t1"): 10.0,
        (Verdict.MODIFY, 0, "t1"): 1.0,
        (Verdict.MODIFY, 1, "t1"): 4.0,
        (Verdict.ESCALATE, 0, "t1"): 2.0,
        (Verdict.ESCALATE, 1, "t1"): 2.0,
        (Verdict.BLOCK, 0, "t1"): 5.0,
        (Verdict.BLOCK, 1, "t1"): 0.0,
    }
    base.update({k: v for k, v in overrides.items()})  # type: ignore[arg-type]
    return LossGrid(values=base, source="test fixture — not a REM design value")


def test_conditional_risk_matches_the_frozen_equation():
    """R_t(v) = (1-p)L(v,0,k) + p L(v,1,k), hand-computed."""
    engine = ExpectedLossDecisionEngine(_grid())
    p = 0.3
    assert engine.conditional_risk(Verdict.ALLOW, p, "t1") == pytest.approx(
        0.7 * 0.0 + 0.3 * 10.0
    )
    assert engine.conditional_risk(Verdict.MODIFY, p, "t1") == pytest.approx(
        0.7 * 1.0 + 0.3 * 4.0
    )
    assert engine.conditional_risk(Verdict.BLOCK, p, "t1") == pytest.approx(
        0.7 * 5.0 + 0.3 * 0.0
    )


def test_argmin_selects_allow_when_risk_is_low():
    engine = ExpectedLossDecisionEngine(_grid())
    verdict, risks = engine.argmin_verdict(0.01, "t1")
    assert verdict is Verdict.ALLOW
    assert risks["allow"] == pytest.approx(0.1)


def test_argmin_selects_block_when_risk_is_high():
    engine = ExpectedLossDecisionEngine(_grid())
    verdict, _ = engine.argmin_verdict(0.99, "t1")
    assert verdict is Verdict.BLOCK


def test_argmin_can_select_an_intermediate_verdict():
    """Escalate wins in the middle — the reject/abstain region."""
    engine = ExpectedLossDecisionEngine(_grid())
    verdict, _ = engine.argmin_verdict(0.5, "t1")
    assert verdict in (Verdict.MODIFY, Verdict.ESCALATE)


def test_risk_table_covers_all_four_verdicts():
    engine = ExpectedLossDecisionEngine(_grid())
    _, risks = engine.argmin_verdict(0.4, "t1")
    assert set(risks) == {"allow", "modify", "escalate", "block"}


def test_exact_tie_raises_rather_than_choosing():
    """No tie-breaking rule is frozen, so REM must not invent one."""
    symmetric = LossGrid(
        values={
            (v, y, "t1"): 1.0
            for v in Verdict
            for y in (0, 1)
        },
        source="test fixture — deliberately symmetric",
    )
    engine = ExpectedLossDecisionEngine(symmetric)
    with pytest.raises(VerdictTieError, match="will not choose one"):
        engine.argmin_verdict(0.5, "t1")


def test_engine_without_loss_grid_is_design_blocked():
    with pytest.raises(DesignNotSpecifiedError, match="loss grid"):
        ExpectedLossDecisionEngine()


def test_loss_grid_requires_a_source():
    with pytest.raises(ValueError, match="must declare its source"):
        LossGrid(values={(Verdict.ALLOW, 0, "t1"): 1.0}, source="")


def test_incomplete_loss_grid_is_rejected():
    with pytest.raises(ValueError, match="incomplete"):
        LossGrid(
            values={(Verdict.ALLOW, 0, "t1"): 1.0, (Verdict.ALLOW, 1, "t1"): 1.0},
            source="test",
        )


def test_unknown_tier_is_design_blocked():
    engine = ExpectedLossDecisionEngine(_grid())
    with pytest.raises(DesignNotSpecifiedError, match="does not cover this consequence tier"):
        engine.conditional_risk(Verdict.ALLOW, 0.5, "tier-that-does-not-exist")


def test_decide_requires_a_calibrated_probability():
    """p_tilde must not be accepted as p_t."""
    engine = ExpectedLossDecisionEngine(_grid())
    uncalibrated = DetectionResult(
        label="unthresholded",
        score=0.6,
        semantics=ScoreSemantics.UNCALIBRATED_PROBABILITY,
        producer="detector",
        logit=0.4,
    )
    with pytest.raises(TypeError, match="Platt-on-logit"):
        engine.decide(uncalibrated, "t1", {}, TrajectoryStep(0))


def test_decide_requires_a_consequence_tier():
    engine = ExpectedLossDecisionEngine(_grid())
    calibrated = DetectionResult(
        label="x", score=0.6, semantics=ScoreSemantics.CALIBRATED_PROBABILITY,
        producer="d", logit=0.4,
    )
    with pytest.raises(DesignNotSpecifiedError, match="consequence tier"):
        engine.decide(calibrated, None, {}, TrajectoryStep(0))


def test_firing_predicate_without_policy_is_design_blocked():
    """A predicate that fires must not be silently ignored."""
    engine = ExpectedLossDecisionEngine(_grid())
    calibrated = DetectionResult(
        label="x", score=0.6, semantics=ScoreSemantics.CALIBRATED_PROBABILITY,
        producer="d", logit=0.4,
    )
    with pytest.raises(DesignNotSpecifiedError, match="policy-predicate semantics"):
        engine.decide(calibrated, "t1", {"tool_is_irreversible": True}, TrajectoryStep(0))


def test_non_firing_predicates_do_not_block():
    engine = ExpectedLossDecisionEngine(_grid())
    calibrated = DetectionResult(
        label="x", score=0.02, semantics=ScoreSemantics.CALIBRATED_PROBABILITY,
        producer="d", logit=-4.0,
    )
    decision = engine.decide(calibrated, "t1", {"p": False}, TrajectoryStep(0))
    assert decision.verdict is Verdict.ALLOW
    assert decision.conditional_risk


def test_decision_records_the_full_risk_table():
    """The audit record must allow the argmin to be re-checked."""
    engine = ExpectedLossDecisionEngine(_grid())
    calibrated = DetectionResult(
        label="x", score=0.8, semantics=ScoreSemantics.CALIBRATED_PROBABILITY,
        producer="d", logit=1.4,
    )
    decision = engine.decide(calibrated, "t1", {}, TrajectoryStep(0))
    assert set(decision.conditional_risk) == {"allow", "modify", "escalate", "block"}
    chosen = decision.conditional_risk[decision.verdict.value]
    assert chosen == pytest.approx(min(decision.conditional_risk.values()))


# ---------------------------------------------------------------------------
# Linear Shapley attribution — audit only
# ---------------------------------------------------------------------------


@pytest.fixture
def attributor():
    return LinearShapleyAttributor(
        feature_order=["a", "b"],
        coefficients=[2.0, -3.0],
        intercept=0.5,
        background_mean={"a": 1.0, "b": 2.0},
    )


def test_shapley_value_matches_the_closed_form(attributor):
    """phi_i = beta_i * (x_i - E[x_i])."""
    assert attributor.shapley_value(0, 4.0) == pytest.approx(2.0 * (4.0 - 1.0))
    assert attributor.shapley_value(1, 0.0) == pytest.approx(-3.0 * (0.0 - 2.0))


def test_base_value_is_the_model_at_the_background_mean(attributor):
    assert attributor.base_value() == pytest.approx(0.5 + 2.0 * 1.0 + (-3.0) * 2.0)


def test_local_accuracy_holds(attributor):
    """f(x) = phi_0 + sum_i phi_i — the defining property of Shapley values."""
    x = {"a": 4.0, "b": 0.0}
    features = FeatureVector(x, "test")
    result = attributor.attribute(
        features,
        DetectionResult("x", 0.5, ScoreSemantics.CALIBRATED_PROBABILITY, "d", logit=0.0),
    )
    total = result.base_value + sum(a.attribution for a in result.attributions)
    model_output = 0.5 + 2.0 * x["a"] + (-3.0) * x["b"]
    assert total == pytest.approx(model_output)


def test_attribution_is_flagged_audit_only(attributor):
    result = attributor.attribute(
        FeatureVector({"a": 1.0, "b": 2.0}, "test"),
        DetectionResult("x", 0.5, ScoreSemantics.CALIBRATED_PROBABILITY, "d", logit=0.0),
    )
    assert result.audit_only is True


def test_attribution_cannot_reach_the_decision_engine(attributor):
    """SHAP as a decision input is a forbidden reintroduction."""
    engine = ExpectedLossDecisionEngine(_grid())
    result = attributor.attribute(
        FeatureVector({"a": 1.0, "b": 2.0}, "test"),
        DetectionResult("x", 0.5, ScoreSemantics.CALIBRATED_PROBABILITY, "d", logit=0.0),
    )
    with pytest.raises(TypeError, match="audit-only"):
        engine.decide(result, "t1", {}, TrajectoryStep(0))  # type: ignore[arg-type]


def test_attributor_requires_a_background_mean_for_every_feature():
    with pytest.raises(ValueError, match="background_mean is missing"):
        LinearShapleyAttributor(["a", "b"], [1.0, 1.0], 0.0, {"a": 0.0})


def test_ranking_is_by_magnitude_without_rescaling(attributor):
    result = attributor.attribute(
        FeatureVector({"a": 1.5, "b": -4.0}, "test"),
        DetectionResult("x", 0.5, ScoreSemantics.CALIBRATED_PROBABILITY, "d", logit=0.0),
    )
    ranked = result.ranked()
    assert abs(ranked[0].attribution) >= abs(ranked[1].attribution)
    assert ranked[0].attribution == pytest.approx(-3.0 * (-4.0 - 2.0))
