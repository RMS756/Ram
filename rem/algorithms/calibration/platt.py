"""Platt calibration on the logit — the FROZEN calibrator (cross-cutting).

``CLAUDE.md`` § MATHEMATICAL LOCK → Calibration::

    Platt/logistic calibration on the logit:

    p_t = sigmoid(gamma_1 * s_t + gamma_0)

    gamma_1 > 0 is required for the monotone interpretation.

Purpose
    Map the detector's linear score ``s_t`` onto a calibrated probability
    ``p_t``, which is the only quantity admissible in the expected-loss Bayes
    verdict.

Input
    Held-out logits and binary labels for fitting; a
    :class:`~rem.core.results.DetectionResult` carrying ``s_t`` at runtime.

Output
    A ``DetectionResult`` whose score is ``p_t`` with
    ``CALIBRATED_PROBABILITY`` semantics.

Mathematical foundation
    ``gamma_0`` and ``gamma_1`` are fitted by minimising the negative
    log-likelihood of ``sigmoid(gamma_1 * s + gamma_0)`` against Platt's
    smoothed targets

        t+ = (N+ + 1) / (N+ + 2)     for positive examples
        t- =        1 / (N- + 2)     for negative examples

    where ``N+`` and ``N-`` are the counts of positive and negative examples in
    the calibration split. The smoothing is part of Platt's published method,
    not an addition: it is what keeps the fit finite when the held-out scores
    are separable.

Academic reference
    Frozen runtime equation: ``CLAUDE.md`` § MATHEMATICAL LOCK.
    Method: Platt, J. C. (1999). "Probabilistic Outputs for Support Vector
    Machines and Comparisons to Regularized Likelihood Methods." In *Advances
    in Large Margin Classifiers*, MIT Press, pp. 61–74.

Equation ID
    NOT ASSIGNED — see ``CLAUDE.md`` § EQUATION-ID LOCK.

Assumptions
    The score-to-probability relationship is sigmoidal in the logit, and the
    calibration split is disjoint from both training and test data.

Limitations
    Beta, isotonic and temperature calibration are forbidden reintroductions
    (``CLAUDE.md`` § FORBIDDEN REINTRODUCTIONS) and are deliberately absent.
    Note also that REM's frozen parameterisation ``sigmoid(gamma_1*s + gamma_0)``
    is sign-flipped relative to Platt's own ``1/(1 + exp(A*f + B))``; the
    frozen form is implemented, so ``gamma_1 = -A``.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from rem.algorithms.detection.ridge_logistic import sigmoid
from rem.core.interfaces import Calibrator
from rem.core.results import DetectionResult, ScoreSemantics
from rem.traceability.registry import derivation

__all__ = ["PlattLogitCalibrator", "MonotonicityViolationError"]

_FROZEN_SOURCE = (
    "CLAUDE.md, MATHEMATICAL LOCK -> Calibration (frozen specification); method "
    "per Platt, J. C. (1999), 'Probabilistic Outputs for Support Vector Machines "
    "and Comparisons to Regularized Likelihood Methods', in Advances in Large "
    "Margin Classifiers, MIT Press, pp. 61-74."
)


class MonotonicityViolationError(RuntimeError):
    """Raised when the fitted calibration map is not increasing in ``s_t``.

    ``CLAUDE.md`` requires ``gamma_1 > 0``. A fitted ``gamma_1 <= 0`` would mean
    a higher detector score maps to a *lower* attack probability, inverting the
    detector. REM refuses such a map rather than silently using it.
    """


class PlattLogitCalibrator(Calibrator):
    """The frozen REM calibrator.

    Args:
        max_iterations: Newton-Raphson iteration cap (numerical setting).
        tolerance: Convergence tolerance on the maximum absolute parameter
            change (numerical setting, not a decision threshold).
    """

    name = "platt_logit_calibrator"

    def __init__(self, *, max_iterations: int = 100, tolerance: float = 1e-10) -> None:
        self.max_iterations = int(max_iterations)
        self.tolerance = float(tolerance)
        self._gamma_0: Optional[float] = None
        self._gamma_1: Optional[float] = None
        self._converged = False

    @property
    def is_fitted(self) -> bool:
        """Whether the calibration map exists."""
        return self._gamma_1 is not None

    @property
    def gamma_0(self) -> float:
        """The fitted intercept ``gamma_0``."""
        self._require_fit()
        assert self._gamma_0 is not None
        return self._gamma_0

    @property
    def gamma_1(self) -> float:
        """The fitted slope ``gamma_1``, guaranteed positive."""
        self._require_fit()
        assert self._gamma_1 is not None
        return self._gamma_1

    @property
    def converged(self) -> bool:
        """Whether the Newton iteration met the tolerance."""
        return self._converged

    def _require_fit(self) -> None:
        if self._gamma_1 is None:
            raise RuntimeError(
                f"{self.name} is not fitted. Fit it on the held-out calibration "
                "split before transforming runtime scores."
            )

    @derivation(
        statement=(
            "fit gamma_0, gamma_1 by minimising "
            "-sum_i [t_i log p_i + (1-t_i) log(1-p_i)], "
            "p_i = sigmoid(gamma_1 * s_i + gamma_0), with Platt's smoothed "
            "targets t+ = (N+ + 1)/(N+ + 2) and t- = 1/(N- + 2)"
        ),
        algorithm="Platt (logistic) calibration on the logit",
        source=(
            "Platt, J. C. (1999). Probabilistic Outputs for Support Vector "
            "Machines and Comparisons to Regularized Likelihood Methods. In "
            "Advances in Large Margin Classifiers, MIT Press, pp. 61-74."
        ),
        location=(
            "Section 2 — the sigmoid fit and its regularised (smoothed) targets."
        ),
        notes=(
            "The smoothed targets are part of the published method. REM's frozen "
            "parameterisation sigmoid(gamma_1*s + gamma_0) is sign-flipped "
            "relative to Platt's 1/(1+exp(A*f+B)), so gamma_1 = -A."
        ),
    )
    def fit(self, logits: Sequence[float], labels: Sequence[int]) -> "PlattLogitCalibrator":
        """Fit the calibration map on a held-out split.

        Args:
            logits: Detector scores ``s_i`` from the calibration split.
            labels: Binary labels, 1 = attack.

        Returns:
            ``self``, fitted.

        Raises:
            ValueError: On length mismatch, empty input, non-binary labels, or a
                split containing only one class.
            MonotonicityViolationError: If the fitted ``gamma_1`` is not positive.
        """
        scores = np.asarray(logits, dtype=float)
        target_labels = np.asarray(labels, dtype=float)
        if scores.shape[0] != target_labels.shape[0]:
            raise ValueError("logits and labels must be the same length.")
        if scores.shape[0] == 0:
            raise ValueError("Cannot calibrate on an empty split.")
        invalid = set(np.unique(target_labels)) - {0.0, 1.0}
        if invalid:
            raise ValueError(f"Labels must be 0 or 1; found {sorted(invalid)}.")

        n_positive = float(np.sum(target_labels == 1.0))
        n_negative = float(np.sum(target_labels == 0.0))
        if n_positive == 0 or n_negative == 0:
            raise ValueError(
                "The calibration split must contain both classes; got "
                f"{int(n_positive)} positive and {int(n_negative)} negative. "
                "A single-class split cannot identify gamma_1."
            )

        # Platt's smoothed targets.
        high_target = (n_positive + 1.0) / (n_positive + 2.0)
        low_target = 1.0 / (n_negative + 2.0)
        targets = np.where(target_labels == 1.0, high_target, low_target)

        design = np.column_stack([np.ones_like(scores), scores])
        theta = np.zeros(2)

        self._converged = False
        for _ in range(self.max_iterations):
            linear = design @ theta
            probabilities = sigmoid(linear)
            gradient = design.T @ (probabilities - targets)
            weights = probabilities * (1.0 - probabilities)
            hessian = (design.T * weights) @ design
            try:
                step = np.linalg.solve(hessian, gradient)
            except np.linalg.LinAlgError:  # pragma: no cover - degenerate split
                step = np.linalg.lstsq(hessian, gradient, rcond=None)[0]
            theta = theta - step
            if np.max(np.abs(step)) < self.tolerance:
                self._converged = True
                break

        gamma_0, gamma_1 = float(theta[0]), float(theta[1])
        if not gamma_1 > 0.0:
            raise MonotonicityViolationError(
                f"{self.name} fitted gamma_1 = {gamma_1:.6g}, which is not "
                "positive. CLAUDE.md MATHEMATICAL LOCK requires gamma_1 > 0 for "
                "the monotone interpretation: a non-positive slope would map "
                "higher detector scores to lower attack probabilities. REM will "
                "not adopt this map. Check the detector's orientation and the "
                "calibration split."
            )
        self._gamma_0, self._gamma_1 = gamma_0, gamma_1
        return self

    @derivation(
        statement="p_t = sigmoid(gamma_1 * s_t + gamma_0)",
        algorithm="Platt (logistic) calibration on the logit",
        source=_FROZEN_SOURCE,
        location="CLAUDE.md, MATHEMATICAL LOCK -> Calibration.",
        notes=(
            "Output carries CALIBRATED_PROBABILITY semantics and is the only "
            "value admissible as p_t in the expected-loss Bayes verdict."
        ),
    )
    def calibrate(self, logit: float) -> float:
        """Map one logit to a calibrated probability.

        Args:
            logit: The detector score ``s_t``.

        Returns:
            ``p_t``.
        """
        self._require_fit()
        assert self._gamma_0 is not None and self._gamma_1 is not None
        return float(sigmoid(self._gamma_1 * float(logit) + self._gamma_0))

    def transform(self, result: DetectionResult) -> DetectionResult:
        """Return ``result`` with a calibrated score.

        Args:
            result: A detection result carrying ``logit``.

        Returns:
            A new result with ``p_t`` and ``CALIBRATED_PROBABILITY`` semantics.

        Raises:
            ValueError: If the result carries no logit. Platt calibration in the
                frozen design operates on the logit; calibrating a probability
                instead would be a different method.
        """
        if result.logit is None:
            raise ValueError(
                f"{self.name} requires the detector logit s_t, but "
                f"{result.producer!r} supplied none. The frozen design "
                "calibrates on the logit."
            )
        return DetectionResult(
            label=result.label,
            score=self.calibrate(result.logit),
            semantics=ScoreSemantics.CALIBRATED_PROBABILITY,
            producer=f"{result.producer}+{self.name}",
            logit=result.logit,
            source=_FROZEN_SOURCE,
            evidence=dict(result.evidence),
            confidence=result.confidence,
        )
