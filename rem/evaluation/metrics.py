"""Evaluation metrics.

Every function computing a number is decorated with
:func:`~rem.traceability.registry.derivation`, recording the formula and its
citation. No equation IDs appear: ``CLAUDE.md`` § EQUATION-ID LOCK forbids
provisional identifiers while the authoritative registry is unavailable, so
these operations are ``AWAITING_REGISTRY_ID``.

Scope: these are *measurement* metrics — the apparatus used to evaluate REM —
not REM algorithms. The frozen algorithmic equations live in ``rem/algorithms/``.

Undefined-value convention: where a denominator is zero the quantity is
genuinely undefined; these functions return ``float('nan')`` rather than
substituting 0, because substituting a value would be an unsourced convention
that could flatter or penalise a system.

Statistical caution: ``CLAUDE.md`` § DATA / EVALUATION LOCK warns that AgentDojo
is an executable environment, not a set of independent i.i.d. rows. These
functions compute point estimates over whatever is passed to them; they do not
and cannot establish that the inputs are independent observations. The grouping
scheme is unresolved.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Sequence

from rem.core.results import DetectionResult
from rem.traceability.registry import derivation

__all__ = [
    "ConfusionMatrix",
    "confusion_matrix",
    "precision",
    "recall",
    "attack_detection_rate",
    "false_positive_rate",
    "false_negative_rate",
    "f1_score",
    "accuracy",
    "brier_score",
    "brier_score_from_results",
    "security_report",
]

NAN = float("nan")

_FAWCETT = (
    "Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition "
    "Letters, 27(8), 861-874."
)
_FAWCETT_LOC = (
    "Section 2 ('Classifier performance'), p. 862 — definitions read off the "
    "confusion matrix."
)
_VAN_RIJSBERGEN = (
    "van Rijsbergen, C. J. (1979). Information Retrieval (2nd ed.). London: "
    "Butterworths."
)


@dataclass(frozen=True)
class ConfusionMatrix:
    """Counts of the four prediction outcomes.

    The positive class is the attack class: a true positive is a correctly
    detected attack, a false positive a benign step wrongly flagged.

    Attributes:
        tp: True positives.
        fp: False positives.
        tn: True negatives.
        fn: False negatives.
    """

    tp: int
    fp: int
    tn: int
    fn: int

    @property
    def positives(self) -> int:
        """Number of actual positive (attack) instances."""
        return self.tp + self.fn

    @property
    def negatives(self) -> int:
        """Number of actual negative (benign) instances."""
        return self.tn + self.fp

    @property
    def total(self) -> int:
        """Total instances."""
        return self.tp + self.fp + self.tn + self.fn


def confusion_matrix(y_true: Sequence[int], y_pred: Sequence[int]) -> ConfusionMatrix:
    """Tabulate predictions against ground truth.

    Counting, not a derived equation; the metrics built on it are documented
    individually below.

    Args:
        y_true: Ground-truth labels, 1 = attack, 0 = benign.
        y_pred: Predicted labels, same encoding and length.

    Returns:
        The confusion matrix.

    Raises:
        ValueError: If lengths differ, labels are not binary, or input is empty.
    """
    if len(y_true) != len(y_pred):
        raise ValueError(
            f"y_true and y_pred must be the same length; got {len(y_true)} and {len(y_pred)}."
        )
    if not y_true:
        raise ValueError("Cannot evaluate an empty set of predictions.")
    invalid = {v for v in list(y_true) + list(y_pred)} - {0, 1}
    if invalid:
        raise ValueError(f"Labels must be 0 or 1; found {sorted(invalid)}.")
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    return ConfusionMatrix(tp=tp, fp=fp, tn=tn, fn=fn)


@derivation(
    statement="precision = TP / (TP + FP)",
    algorithm="Confusion-matrix evaluation",
    source=_VAN_RIJSBERGEN,
    location="Chapter 7 ('Evaluation') — precision as relevant retrieved / retrieved.",
    notes="Undefined when TP + FP = 0; returns NaN rather than substituting a value.",
)
def precision(cm: ConfusionMatrix) -> float:
    """Proportion of flagged steps that were genuinely attacks.

    Args:
        cm: The confusion matrix.

    Returns:
        Precision, or NaN when no positive predictions were made.
    """
    denominator = cm.tp + cm.fp
    return cm.tp / denominator if denominator else NAN


@derivation(
    statement="recall = TP / (TP + FN)",
    algorithm="Confusion-matrix evaluation",
    source=_FAWCETT,
    location=_FAWCETT_LOC + " tp rate = TP / (TP + FN).",
    notes="Undefined when TP + FN = 0 (no positive instances).",
)
def recall(cm: ConfusionMatrix) -> float:
    """Proportion of actual attacks that REM detected.

    Args:
        cm: The confusion matrix.

    Returns:
        Recall, or NaN when there are no positive instances.
    """
    denominator = cm.tp + cm.fn
    return cm.tp / denominator if denominator else NAN


def attack_detection_rate(cm: ConfusionMatrix) -> float:
    """Attack detection rate — the security-facing name for recall.

    An alias, so that security vocabulary does not introduce a second, subtly
    different definition.

    Args:
        cm: The confusion matrix.

    Returns:
        The value of :func:`recall`.
    """
    return recall(cm)


@derivation(
    statement="FPR = FP / (FP + TN)",
    algorithm="Confusion-matrix evaluation",
    source=_FAWCETT,
    location=_FAWCETT_LOC + " fp rate = FP / (FP + TN).",
    notes="Undefined when FP + TN = 0 (no negative instances).",
)
def false_positive_rate(cm: ConfusionMatrix) -> float:
    """Proportion of benign steps wrongly flagged.

    The direct measure of REM's interference with legitimate agent operation.

    Args:
        cm: The confusion matrix.

    Returns:
        FPR, or NaN when there are no negative instances.
    """
    denominator = cm.fp + cm.tn
    return cm.fp / denominator if denominator else NAN


@derivation(
    statement="FNR = FN / (TP + FN)",
    algorithm="Confusion-matrix evaluation",
    source=_FAWCETT,
    location=_FAWCETT_LOC + " FN rate is the complement of tp rate over the positives.",
    notes="Undefined when TP + FN = 0.",
)
def false_negative_rate(cm: ConfusionMatrix) -> float:
    """Proportion of attacks REM missed.

    Args:
        cm: The confusion matrix.

    Returns:
        FNR, or NaN when there are no positive instances.
    """
    denominator = cm.tp + cm.fn
    return cm.fn / denominator if denominator else NAN


@derivation(
    statement="F1 = 2 * P * R / (P + R)",
    algorithm="Confusion-matrix evaluation",
    source=_VAN_RIJSBERGEN,
    location="Chapter 7 ('Evaluation') — F from the E-measure at beta = 1.",
    notes="Undefined when P + R = 0, or when either P or R is itself undefined.",
)
def f1_score(cm: ConfusionMatrix) -> float:
    """Balanced harmonic mean of precision and recall.

    Args:
        cm: The confusion matrix.

    Returns:
        F1, or NaN when precision or recall is undefined, or both are zero.
    """
    p = precision(cm)
    r = recall(cm)
    if math.isnan(p) or math.isnan(r):
        return NAN
    denominator = p + r
    return 2 * p * r / denominator if denominator else NAN


@derivation(
    statement="accuracy = (TP + TN) / (P + N)",
    algorithm="Confusion-matrix evaluation",
    source=_FAWCETT,
    location=_FAWCETT_LOC + " accuracy = (TP + TN) / (P + N).",
    notes=(
        "Reported for completeness only. Under the class imbalance typical of "
        "attack detection it is not a primary metric."
    ),
)
def accuracy(cm: ConfusionMatrix) -> float:
    """Overall proportion correct.

    Args:
        cm: The confusion matrix.

    Returns:
        Accuracy, or NaN if the matrix is empty.
    """
    return (cm.tp + cm.tn) / cm.total if cm.total else NAN


@derivation(
    statement="BS = (1/n) * sum_i (p_i - o_i)^2",
    algorithm="Brier score (proper scoring rule for probabilistic forecasts)",
    source=(
        "Brier, G. W. (1950). Verification of forecasts expressed in terms of "
        "probability. Monthly Weather Review, 78(1), 1-3."
    ),
    location="Equation (1), pp. 1-2.",
    notes=(
        "Applicable only to genuine probabilities. In the frozen design that "
        "means the output of Platt-on-logit calibration; scoring an "
        "uncalibrated value with a proper scoring rule is not meaningful."
    ),
)
def brier_score(probabilities: Sequence[float], outcomes: Sequence[int]) -> float:
    """Mean squared difference between forecast and outcome. Lower is better.

    Args:
        probabilities: Forecast probabilities of the positive class, in [0, 1].
        outcomes: Realised outcomes, 1 = attack occurred, 0 = benign.

    Returns:
        The Brier score.

    Raises:
        ValueError: On length mismatch, empty input, or out-of-range values.
    """
    if len(probabilities) != len(outcomes):
        raise ValueError("probabilities and outcomes must be the same length.")
    if not probabilities:
        raise ValueError("Cannot score an empty set of forecasts.")
    for p in probabilities:
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"Forecast {p} lies outside [0, 1]; it is not a probability.")
    invalid = set(outcomes) - {0, 1}
    if invalid:
        raise ValueError(f"Outcomes must be 0 or 1; found {sorted(invalid)}.")
    return sum((p - o) ** 2 for p, o in zip(probabilities, outcomes)) / len(probabilities)


def brier_score_from_results(
    results: Sequence[DetectionResult], outcomes: Sequence[int]
) -> float:
    """Brier score over detection results, enforcing calibrated semantics.

    Args:
        results: Detection results whose scores are calibrated probabilities.
        outcomes: Realised outcomes, 1 = attack, 0 = benign.

    Returns:
        The Brier score.

    Raises:
        TypeError: If any result is not a calibrated probability.
    """
    uncalibrated = [r.producer for r in results if not r.semantics.is_calibrated]
    if uncalibrated:
        raise TypeError(
            "Brier score requires calibrated probabilities; these producers "
            f"emitted something else: {sorted(set(uncalibrated))}. Route their "
            "logits through Platt-on-logit calibration first."
        )
    return brier_score([r.probability for r in results], outcomes)


def security_report(y_true: Sequence[int], y_pred: Sequence[int]) -> Dict[str, float]:
    """Compute the security metric set for one set of predictions.

    Args:
        y_true: Ground-truth labels, 1 = attack.
        y_pred: Predicted labels.

    Returns:
        Mapping of metric name to value; undefined metrics are NaN.
    """
    cm = confusion_matrix(y_true, y_pred)
    return {
        "tp": float(cm.tp),
        "fp": float(cm.fp),
        "tn": float(cm.tn),
        "fn": float(cm.fn),
        "precision": precision(cm),
        "recall": recall(cm),
        "attack_detection_rate": attack_detection_rate(cm),
        "false_positive_rate": false_positive_rate(cm),
        "false_negative_rate": false_negative_rate(cm),
        "f1": f1_score(cm),
        "accuracy": accuracy(cm),
    }
