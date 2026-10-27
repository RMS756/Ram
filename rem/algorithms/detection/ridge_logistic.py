"""Ridge logistic regression — the FROZEN probability estimator (L2 Detection).

``CLAUDE.md`` § MATHEMATICAL LOCK → Probability estimation::

    Ridge logistic regression is the estimator.

    Runtime:
    s_t = beta_0 + beta^T x_t
    p_tilde_t = sigmoid(s_t)

Purpose
    Produce the linear score ``s_t`` for a step's evidence vector. ``s_t`` is
    the quantity Platt calibration consumes; ``p_tilde_t`` is reported for
    inspection but is **uncalibrated** and must not enter the verdict.

Input
    ``x_t`` — the evidence vector from L1, in the fitted feature order.

Output
    :class:`~rem.core.results.DetectionResult` carrying ``s_t`` as ``logit`` and
    ``p_tilde_t`` as an ``UNCALIBRATED_PROBABILITY``.

Mathematical foundation
    Runtime form: frozen above. Fitting minimises the L2-penalised negative
    log-likelihood

        J(b0, b) = -sum_i [ y_i log p_i + (1 - y_i) log(1 - p_i) ]
                   + (lambda / 2) * ||b||^2

    with the intercept left unpenalised, solved by Newton-Raphson (equivalently
    iteratively reweighted least squares).

Academic reference
    Frozen runtime equations: ``CLAUDE.md`` § MATHEMATICAL LOCK.
    Logistic regression and its Newton-Raphson/IRLS fitting: Hastie, T.,
    Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical
    Learning* (2nd ed.), Springer, § 4.4 and § 4.4.1.
    L2 (ridge) penalty: same volume, § 3.4.1.

Equation ID
    NOT ASSIGNED. The authoritative Equation-to-Source Registry has not been
    supplied, and ``CLAUDE.md`` § EQUATION-ID LOCK forbids provisional IDs in
    implementation code.

Assumptions
    Features are numeric and in a fixed order; the intercept is unpenalised;
    the positive class is the attack class.

Limitations
    The **feature set** and the **ridge penalty lambda** are unresolved
    (``CLAUDE.md`` § DATA / EVALUATION LOCK and RECONCILIATION.md). This class
    refuses to fit without an explicitly supplied lambda and refuses to score
    before it is fitted.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np

from rem.agent.trajectory import TrajectoryStep
from rem.core.interfaces import DesignNotSpecifiedError, Detector, FeatureVector
from rem.core.results import DetectionResult, ScoreSemantics
from rem.traceability.registry import derivation

__all__ = ["RidgeLogisticRegression", "sigmoid", "NotFittedError"]

_FROZEN_SOURCE = (
    "CLAUDE.md, MATHEMATICAL LOCK -> Probability estimation (frozen "
    "specification); fitting per Hastie, Tibshirani & Friedman (2009), The "
    "Elements of Statistical Learning (2nd ed.), Springer."
)


class NotFittedError(RuntimeError):
    """Raised when a model is scored before its parameters exist."""


@derivation(
    statement="sigmoid(z) = 1 / (1 + exp(-z))",
    algorithm="Logistic (sigmoid) link",
    source=(
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of "
        "Statistical Learning (2nd ed.). Springer."
    ),
    location="Section 4.4, 'Logistic Regression' — the logistic link function.",
    notes=(
        "Implemented in the numerically stable branch form so that large |z| "
        "does not overflow exp(). Mathematically identical to the textbook "
        "expression."
    ),
)
def sigmoid(z: np.ndarray | float) -> np.ndarray:
    """Logistic function, evaluated without overflow.

    Args:
        z: Real-valued input, scalar or array.

    Returns:
        ``1 / (1 + exp(-z))`` elementwise.
    """
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    positive = z >= 0
    out[positive] = 1.0 / (1.0 + np.exp(-z[positive]))
    exp_z = np.exp(z[~positive])
    out[~positive] = exp_z / (1.0 + exp_z)
    return out


@dataclass
class _Fit:
    """Fitted parameters and convergence diagnostics."""

    intercept: float
    coefficients: np.ndarray
    iterations: int
    converged: bool
    objective: float


class RidgeLogisticRegression(Detector):
    """The frozen REM detector.

    Args:
        feature_order: Feature names in the order the coefficients correspond
            to. Fixing the order explicitly prevents a reordered evidence
            vector from silently changing ``s_t``.
        penalty: The ridge penalty ``lambda``. There is deliberately no default:
            it is unresolved in the design, and adopting a library default would
            be exactly the silent invention the contract forbids.
        max_iterations: Newton-Raphson iteration cap. A numerical solver
            setting, not a scientific parameter.
        tolerance: Convergence tolerance on the maximum absolute parameter
            change. A numerical solver setting, not a decision threshold.

    Raises:
        DesignNotSpecifiedError: On ``fit`` when ``penalty`` is ``None``.
    """

    name = "ridge_logistic_regression"

    def __init__(
        self,
        feature_order: Sequence[str],
        *,
        penalty: Optional[float] = None,
        max_iterations: int = 100,
        tolerance: float = 1e-8,
    ) -> None:
        if not feature_order:
            raise ValueError("feature_order must name at least one feature.")
        self.feature_order = tuple(feature_order)
        self.penalty = penalty
        self.max_iterations = int(max_iterations)
        self.tolerance = float(tolerance)
        self._fit: Optional[_Fit] = None

    # -- properties ---------------------------------------------------------

    @property
    def is_fitted(self) -> bool:
        """Whether coefficients exist."""
        return self._fit is not None

    @property
    def intercept(self) -> float:
        """``beta_0``."""
        return self._require_fit().intercept

    @property
    def coefficients(self) -> np.ndarray:
        """``beta``, aligned with :attr:`feature_order`."""
        return self._require_fit().coefficients.copy()

    @property
    def converged(self) -> bool:
        """Whether the Newton iteration met the tolerance."""
        return self._require_fit().converged

    def _require_fit(self) -> _Fit:
        if self._fit is None:
            raise NotFittedError(
                f"{self.name} has no coefficients. Call fit() on the training "
                "split before scoring."
            )
        return self._fit

    # -- fitting ------------------------------------------------------------

    @derivation(
        statement=(
            "minimise J(b0, b) = -sum_i [y_i log p_i + (1-y_i) log(1-p_i)] "
            "+ (lambda/2)||b||^2, solved by Newton-Raphson: "
            "b <- b - H^-1 g, g = X^T(p - y) + lambda*b, H = X^T W X + lambda*I, "
            "W = diag(p_i(1-p_i)); the intercept is unpenalised"
        ),
        algorithm="Ridge (L2-penalised) logistic regression, Newton-Raphson/IRLS",
        source=(
            "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of "
            "Statistical Learning (2nd ed.). Springer."
        ),
        location=(
            "Section 4.4.1 'Fitting Logistic Regression Models' for the "
            "Newton-Raphson/IRLS procedure; Section 3.4.1 'Ridge Regression' "
            "for the L2 penalty."
        ),
        notes=(
            "lambda is UNRESOLVED in the REM design and must be supplied by the "
            "caller. The penalty is applied to the slope coefficients only, "
            "leaving the intercept free, which is the standard convention."
        ),
    )
    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> "RidgeLogisticRegression":
        """Fit the estimator on a training split.

        Args:
            X: Design matrix, rows ordered as :attr:`feature_order`.
            y: Binary labels, 1 = attack.

        Returns:
            ``self``, fitted.

        Raises:
            DesignNotSpecifiedError: If the ridge penalty was not supplied.
            ValueError: On shape mismatch, empty input, or non-binary labels.
        """
        if self.penalty is None:
            raise DesignNotSpecifiedError(
                self.name,
                "the ridge penalty lambda (not frozen in any supplied document; "
                "a library default must not be adopted)",
            )
        if float(self.penalty) <= 0.0:
            raise ValueError(
                f"penalty must be positive; got {self.penalty}. A zero penalty "
                "is unpenalised logistic regression, not the frozen ridge "
                "estimator."
            )

        design = np.asarray(X, dtype=float)
        target = np.asarray(y, dtype=float)
        if design.ndim != 2:
            raise ValueError(f"X must be 2-dimensional; got shape {design.shape}.")
        if design.shape[0] == 0:
            raise ValueError("Cannot fit on an empty training set.")
        if design.shape[1] != len(self.feature_order):
            raise ValueError(
                f"X has {design.shape[1]} columns but feature_order names "
                f"{len(self.feature_order)}."
            )
        if target.shape[0] != design.shape[0]:
            raise ValueError("X and y must have the same number of rows.")
        invalid = set(np.unique(target)) - {0.0, 1.0}
        if invalid:
            raise ValueError(f"Labels must be 0 or 1; found {sorted(invalid)}.")

        n_samples, n_features = design.shape
        # Augment with a leading column of ones for the intercept.
        augmented = np.hstack([np.ones((n_samples, 1)), design])
        theta = np.zeros(n_features + 1)

        # Penalty applies to slopes only; the intercept entry stays zero.
        penalty_diagonal = np.full(n_features + 1, float(self.penalty))
        penalty_diagonal[0] = 0.0

        converged = False
        iterations = 0
        for iterations in range(1, self.max_iterations + 1):
            scores = augmented @ theta
            probabilities = sigmoid(scores)
            gradient = augmented.T @ (probabilities - target) + penalty_diagonal * theta
            weights = probabilities * (1.0 - probabilities)
            hessian = (augmented.T * weights) @ augmented + np.diag(penalty_diagonal)
            try:
                step = np.linalg.solve(hessian, gradient)
            except np.linalg.LinAlgError:  # pragma: no cover - guarded by penalty
                step = np.linalg.lstsq(hessian, gradient, rcond=None)[0]
            theta = theta - step
            if np.max(np.abs(step)) < self.tolerance:
                converged = True
                break

        self._fit = _Fit(
            intercept=float(theta[0]),
            coefficients=theta[1:].copy(),
            iterations=iterations,
            converged=converged,
            objective=self._objective(augmented, target, theta, penalty_diagonal),
        )
        return self

    def _objective(
        self,
        augmented: np.ndarray,
        target: np.ndarray,
        theta: np.ndarray,
        penalty_diagonal: np.ndarray,
    ) -> float:
        scores = augmented @ theta
        # log(1 + exp(s)) evaluated stably.
        log_terms = np.logaddexp(0.0, scores)
        negative_log_likelihood = float(np.sum(log_terms - target * scores))
        ridge = 0.5 * float(np.sum(penalty_diagonal * theta**2))
        return negative_log_likelihood + ridge

    # -- runtime scoring ----------------------------------------------------

    @derivation(
        statement="s_t = beta_0 + beta^T x_t",
        algorithm="Ridge logistic regression (runtime score)",
        source=_FROZEN_SOURCE,
        location="CLAUDE.md, MATHEMATICAL LOCK -> Probability estimation.",
        notes=(
            "s_t is the LOGIT. It is the input to Platt-on-logit calibration; "
            "it is not a probability and must not be used as p_t."
        ),
    )
    def decision_function(self, x: Sequence[float]) -> float:
        """Return the linear score ``s_t`` for one evidence vector.

        Args:
            x: Feature values in :attr:`feature_order`.

        Returns:
            ``s_t``.
        """
        fit = self._require_fit()
        values = np.asarray(x, dtype=float)
        if values.shape != fit.coefficients.shape:
            raise ValueError(
                f"Expected {fit.coefficients.shape[0]} features, got {values.shape[0]}."
            )
        return float(fit.intercept + fit.coefficients @ values)

    @derivation(
        statement="p_tilde_t = sigmoid(s_t)",
        algorithm="Ridge logistic regression (uncalibrated probability)",
        source=_FROZEN_SOURCE,
        location="CLAUDE.md, MATHEMATICAL LOCK -> Probability estimation.",
        notes=(
            "UNCALIBRATED. The frozen pipeline routes s_t through Platt "
            "calibration before the expected-loss verdict; p_tilde_t is "
            "reported for inspection only."
        ),
    )
    def uncalibrated_probability(self, x: Sequence[float]) -> float:
        """Return ``p_tilde_t = sigmoid(s_t)``.

        Args:
            x: Feature values in :attr:`feature_order`.

        Returns:
            The uncalibrated probability.
        """
        return float(sigmoid(self.decision_function(x)))

    def detect(self, features: FeatureVector, step: TrajectoryStep) -> DetectionResult:
        """Score ``step`` and return the L2 detection result.

        Args:
            features: Evidence vector from L1.
            step: The step being evaluated.

        Returns:
            The detection result, carrying ``s_t`` and the uncalibrated
            ``p_tilde_t``.
        """
        values = features.as_sequence(self.feature_order)
        logit = self.decision_function(values)
        probability = float(sigmoid(logit))
        return DetectionResult(
            # No class label is emitted. In the frozen design the verdict comes
            # from the expected-loss Bayes rule on the calibrated p_t, not from
            # thresholding the detector; the operating-point threshold policy is
            # BASELINE ONLY (CLAUDE.md, FROZEN REM PIPELINE). Applying 0.5 here
            # would be an invented operating point.
            label="unthresholded",
            score=probability,
            semantics=ScoreSemantics.UNCALIBRATED_PROBABILITY,
            producer=self.name,
            logit=logit,
            source=_FROZEN_SOURCE,
            evidence={
                "s_t": logit,
                "features": dict(zip(self.feature_order, values)),
            },
        )
