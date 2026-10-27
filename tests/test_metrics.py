"""Tests for evaluation metrics and runtime statistics."""

from __future__ import annotations

import math

import pytest

from rem.core.results import DetectionResult, ScoreSemantics
from rem.evaluation.metrics import (
    accuracy,
    attack_detection_rate,
    brier_score,
    brier_score_from_results,
    confusion_matrix,
    f1_score,
    false_negative_rate,
    false_positive_rate,
    precision,
    recall,
    security_report,
)
from rem.evaluation.runtime import (
    LatencyRecorder,
    latency_report,
    mean,
    quantile,
    throughput,
)


@pytest.fixture
def cm():
    # 4 attacks (3 detected), 6 benign (1 wrongly flagged)
    return confusion_matrix(
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    )


def test_confusion_matrix_counts(cm):
    assert (cm.tp, cm.fp, cm.tn, cm.fn) == (3, 1, 5, 1)
    assert cm.positives == 4 and cm.negatives == 6 and cm.total == 10


def test_precision(cm):
    assert precision(cm) == pytest.approx(3 / 4)


def test_recall_and_detection_rate_agree(cm):
    assert recall(cm) == pytest.approx(3 / 4)
    assert attack_detection_rate(cm) == recall(cm)


def test_false_positive_rate(cm):
    assert false_positive_rate(cm) == pytest.approx(1 / 6)


def test_false_negative_rate(cm):
    assert false_negative_rate(cm) == pytest.approx(1 / 4)


def test_f1(cm):
    p = r = 3 / 4
    assert f1_score(cm) == pytest.approx(2 * p * r / (p + r))


def test_accuracy(cm):
    assert accuracy(cm) == pytest.approx(8 / 10)


def test_perfect_detector():
    perfect = confusion_matrix([1, 1, 0, 0], [1, 1, 0, 0])
    assert precision(perfect) == 1.0
    assert recall(perfect) == 1.0
    assert false_positive_rate(perfect) == 0.0
    assert f1_score(perfect) == 1.0


def test_undefined_metrics_are_nan_not_zero():
    """No positive predictions: precision is undefined, not 0."""
    none_flagged = confusion_matrix([1, 0, 0], [0, 0, 0])
    assert math.isnan(precision(none_flagged))
    assert math.isnan(f1_score(none_flagged))
    assert recall(none_flagged) == 0.0  # defined: one positive instance exists


def test_undefined_fpr_when_no_negatives():
    assert math.isnan(false_positive_rate(confusion_matrix([1, 1], [1, 0])))


def test_confusion_matrix_input_validation():
    with pytest.raises(ValueError, match="same length"):
        confusion_matrix([1, 0], [1])
    with pytest.raises(ValueError, match="empty"):
        confusion_matrix([], [])
    with pytest.raises(ValueError, match="Labels must be 0 or 1"):
        confusion_matrix([1, 2], [1, 0])


def test_security_report_keys():
    report = security_report([1, 1, 0, 0], [1, 0, 1, 0])
    assert set(report) >= {"precision", "recall", "false_positive_rate", "f1"}


# --- Brier score ------------------------------------------------------------


def test_brier_score_perfect_forecast():
    assert brier_score([1.0, 0.0, 1.0], [1, 0, 1]) == pytest.approx(0.0)


def test_brier_score_hand_computed():
    # ((0.8-1)^2 + (0.3-0)^2) / 2 = (0.04 + 0.09) / 2
    assert brier_score([0.8, 0.3], [1, 0]) == pytest.approx(0.065)


def test_brier_score_rejects_non_probabilities():
    with pytest.raises(ValueError, match="not a probability"):
        brier_score([1.5], [1])


def test_brier_score_rejects_uncalibrated_results():
    """A proper scoring rule must not be applied to p_tilde."""
    results = [
        DetectionResult(
            label="unthresholded",
            score=0.9,
            semantics=ScoreSemantics.UNCALIBRATED_PROBABILITY,
            producer="ridge_logistic_regression",
            logit=2.0,
        )
    ]
    with pytest.raises(TypeError, match="Platt-on-logit"):
        brier_score_from_results(results, [1])


def test_brier_score_accepts_calibrated_results():
    results = [
        DetectionResult(
            label="unthresholded",
            score=1.0,
            semantics=ScoreSemantics.CALIBRATED_PROBABILITY,
            producer="ridge+platt",
            logit=9.0,
        )
    ]
    assert brier_score_from_results(results, [1]) == pytest.approx(0.0)


# --- Runtime statistics -----------------------------------------------------


def test_mean():
    assert mean([1.0, 2.0, 3.0]) == pytest.approx(2.0)


def test_mean_undefined_on_empty():
    with pytest.raises(ValueError, match="undefined"):
        mean([])


def test_quantile_definition_7():
    """Hyndman & Fan Definition 7 on 1..10: median 5.5, p95 9.55."""
    values = [float(i) for i in range(1, 11)]
    assert quantile(values, 0.5) == pytest.approx(5.5)
    assert quantile(values, 0.0) == pytest.approx(1.0)
    assert quantile(values, 1.0) == pytest.approx(10.0)
    assert quantile(values, 0.95) == pytest.approx(9.55)


def test_quantile_single_sample():
    assert quantile([7.0], 0.95) == 7.0


def test_quantile_validates_probability_level():
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        quantile([1.0], 1.5)


def test_latency_recorder_reports():
    recorder = LatencyRecorder()
    for _ in range(5):
        with recorder.measure():
            pass
    report = recorder.report()
    assert report["n"] == 5.0
    assert report["min_ms"] <= report["p50_ms"] <= report["max_ms"]


def test_latency_report_rejects_empty():
    with pytest.raises(ValueError, match="empty"):
        latency_report([])


def test_throughput():
    assert throughput(100, 2.0) == pytest.approx(50.0)
    with pytest.raises(ValueError, match="positive"):
        throughput(1, 0.0)
