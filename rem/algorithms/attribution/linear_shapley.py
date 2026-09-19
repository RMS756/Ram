"""Linear Shapley attribution — AUDIT ONLY.

``CLAUDE.md`` § MATHEMATICAL LOCK → Attribution::

    Linear Shapley attribution is audit-only.

    It MUST NOT affect the verdict.

§ FORBIDDEN REINTRODUCTIONS additionally bars *SHAP as a decision input*.

Purpose
    Explain a detection result feature-wise for the audit record, so a reviewer
    can see which evidence drove ``s_t``.

Input
    The fitted ridge logistic coefficients, the evidence vector ``x_t``, and a
    background mean ``E[x]`` estimated on the training split.

Output
    :class:`~rem.core.results.AttributionResult`, flagged ``audit_only``. The
    decision engine rejects any object carrying that flag.

Mathematical foundation
    For a linear model ``f(x) = b0 + sum_i b_i x_i`` the exact Shapley value of
    feature ``i`` under feature independence is

        phi_i(f, x) = b_i * (x_i - E[x_i])

    with base value ``phi_0 = f(E[x])``. These satisfy local accuracy:
    ``f(x) = phi_0 + sum_i phi_i``.

    Attribution is computed on the **logit scale**, the scale on which the model
    is linear. The additive decomposition does not survive the sigmoid, so
    attributing ``p_t`` directly would not be a Shapley decomposition.

Academic reference
    Shapley value: Shapley, L. S. (1953). "A Value for n-Person Games." In
    *Contributions to the Theory of Games II*, Annals of Mathematics Studies 28,
    Princeton University Press, pp. 307–317.
    Linear-model case: Lundberg, S. M., & Lee, S.-I. (2017). "A Unified Approach
    to Interpreting Model Predictions." *Advances in Neural Information
    Processing Systems 30*, pp. 4765–4774 — "Linear SHAP".

Equation ID
    NOT ASSIGNED — see ``CLAUDE.md`` § EQUATION-ID LOCK.

Assumptions
    The explained model is linear in the features, and features are treated as
    independent (the condition under which Linear SHAP is exact).

Limitations
    Audit-only by construction. The background mean must be estimated on the
    training split and supplied explicitly; it is not invented, and changing it
    changes every attribution.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from rem.core.interfaces import Attributor, FeatureVector
from rem.core.results import AttributionResult, DetectionResult, FeatureAttribution
from rem.traceability.registry import derivation

__all__ = ["LinearShapleyAttributor"]

_SOURCE = (
    "Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting "
    "Model Predictions. NeurIPS 30, pp. 4765-4774 ('Linear SHAP'); Shapley, "
    "L. S. (1953). A Value for n-Person Games. Contributions to the Theory of "
    "Games II, Princeton University Press, pp. 307-317."
)


class LinearShapleyAttributor(Attributor):
    """Exact Shapley attribution for the frozen linear detector. Audit only.

    Args:
        feature_order: Feature names matching the coefficient order.
        coefficients: The fitted ``beta``.
        intercept: The fitted ``beta_0``.
        background_mean: ``E[x]`` per feature, estimated on the training split.

    Raises:
        ValueError: On length mismatch, or if a background mean is missing for
            any feature — REM does not substitute zero for an unknown mean.
    """

    name = "linear_shapley_attributor"

    def __init__(
        self,
        feature_order: Sequence[str],
        coefficients: Sequence[float],
        intercept: float,
        background_mean: Mapping[str, float],
    ) -> None:
        if len(feature_order) != len(coefficients):
            raise ValueError(
                f"feature_order has {len(feature_order)} names but "
                f"{len(coefficients)} coefficients were supplied."
            )
        missing = [name for name in feature_order if name not in background_mean]
        if missing:
            raise ValueError(
                f"background_mean is missing feature(s) {missing}. Shapley "
                "values are defined relative to a reference; REM does not "
                "substitute a value for an unknown mean."
            )
        self.feature_order = tuple(feature_order)
        self.coefficients = tuple(float(c) for c in coefficients)
        self.intercept = float(intercept)
        self.background_mean = {name: float(background_mean[name]) for name in self.feature_order}

    @derivation(
        statement="phi_i = beta_i * (x_i - E[x_i])",
        algorithm="Linear SHAP (exact Shapley values for a linear model)",
        source=_SOURCE,
        location=(
            "Lundberg & Lee (2017), 'Linear SHAP' — the closed form for a linear "
            "model under feature independence."
        ),
        notes=(
            "Computed on the logit scale, where the model is linear. The "
            "additive decomposition does not survive the sigmoid."
        ),
    )
    def shapley_value(self, index: int, value: float) -> float:
        """Return ``phi_i`` for one feature.

        Args:
            index: Position in :attr:`feature_order`.
            value: The feature's value ``x_i``.

        Returns:
            The Shapley value on the logit scale.
        """
        name = self.feature_order[index]
        return self.coefficients[index] * (float(value) - self.background_mean[name])

    @derivation(
        statement="phi_0 = f(E[x]) = beta_0 + sum_i beta_i * E[x_i]",
        algorithm="Linear SHAP (base value)",
        source=_SOURCE,
        location="Lundberg & Lee (2017), 'Linear SHAP' — base value phi_0.",
        notes=(
            "Together with phi_i this satisfies local accuracy: "
            "f(x) = phi_0 + sum_i phi_i."
        ),
    )
    def base_value(self) -> float:
        """Return ``phi_0``, the model output at the background mean."""
        return self.intercept + sum(
            coefficient * self.background_mean[name]
            for name, coefficient in zip(self.feature_order, self.coefficients)
        )

    def attribute(
        self, features: FeatureVector, detection: DetectionResult
    ) -> AttributionResult:
        """Explain ``detection`` feature-wise.

        Args:
            features: The evidence vector that produced the detection.
            detection: The detection result being explained.

        Returns:
            The attribution result, flagged audit-only.
        """
        values = features.as_sequence(self.feature_order)
        attributions = tuple(
            FeatureAttribution(
                feature=name,
                value=value,
                attribution=self.shapley_value(index, value),
            )
            for index, (name, value) in enumerate(zip(self.feature_order, values))
        )
        ranked = sorted(attributions, key=lambda a: abs(a.attribution), reverse=True)
        leading = ranked[0].feature if ranked else "none"
        return AttributionResult(
            attributions=attributions,
            producer=self.name,
            base_value=self.base_value(),
            source=_SOURCE,
            explanation=(
                f"Largest contribution to s_t: {leading!r}. Attributions are on "
                "the logit scale and are recorded for audit only; they did not "
                "influence the verdict."
            ),
        )
