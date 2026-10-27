"""Structured results exchanged between REM layers.

Verdict set and mitigation semantics are fixed by ``CLAUDE.md``
§ FROZEN REM PIPELINE and § MITIGATION LOCK. The score-semantics machinery
enforces that a value is only called a probability when the producing algorithm
actually yields one — in the frozen design, only after Platt calibration.

This module contains no mathematics: it labels and carries values computed
elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, Optional, Sequence

__all__ = [
    "ScoreSemantics",
    "DetectionResult",
    "BehaviorResult",
    "Verdict",
    "Decision",
    "MitigationAction",
    "MitigationOutcome",
    "FeatureAttribution",
    "AttributionResult",
]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ScoreSemantics(str, Enum):
    """What a numeric output actually means.

    In the frozen pipeline the detector emits a LOGIT (``s_t``) and an
    uncalibrated probability (``p_tilde_t = sigmoid(s_t)``); only the output of
    Platt-on-logit is a CALIBRATED_PROBABILITY and may be used in the
    expected-loss Bayes verdict.

    Members:
        LOGIT: The linear score ``s_t = b0 + b^T x_t``. Unbounded. Not a
            probability. This is the quantity Platt calibration consumes.
        UNCALIBRATED_PROBABILITY: ``sigmoid(s_t)``. In [0, 1] but carries no
            calibration guarantee, so it must not enter the decision rule.
        CALIBRATED_PROBABILITY: Output of the adopted Platt calibrator. The only
            semantics admissible as ``p_t`` in the conditional-risk equation.
        RAW_SCORE: An unnormalised decision-function value from some other
            method. Ordering meaningful, magnitude not calibrated.
        ANOMALY_SCORE: Output of an anomaly/novelty method. Not a probability.
    """

    LOGIT = "logit"
    UNCALIBRATED_PROBABILITY = "uncalibrated_probability"
    CALIBRATED_PROBABILITY = "calibrated_probability"
    RAW_SCORE = "raw_score"
    ANOMALY_SCORE = "anomaly_score"

    @property
    def is_probability(self) -> bool:
        """Whether values with these semantics lie on a probability scale."""
        return self in (
            ScoreSemantics.UNCALIBRATED_PROBABILITY,
            ScoreSemantics.CALIBRATED_PROBABILITY,
        )

    @property
    def is_calibrated(self) -> bool:
        """Whether values may be used as ``p_t`` or scored with a proper rule."""
        return self is ScoreSemantics.CALIBRATED_PROBABILITY


@dataclass(frozen=True)
class DetectionResult:
    """Output of the Detection layer (L2) for one trajectory step.

    Attributes:
        label: Predicted class label as defined by the detector.
        score: The detector's numeric output.
        semantics: What ``score`` means.
        producer: Identifier of the algorithm that produced this result.
        logit: The linear score ``s_t``, carried separately because Platt
            calibration in the frozen design operates on the logit rather than
            on a probability.
        source: Citation of the equation(s) used, since authoritative equation
            IDs are unavailable (``CLAUDE.md`` § EQUATION-ID LOCK).
        evidence: Named values supporting the result, for audit.
        confidence: Present only if the producing algorithm defines one. REM
            does not manufacture a confidence value, and in particular the
            removed ``confidence = sum|beta_i|`` construction is forbidden by
            § FORBIDDEN REINTRODUCTIONS.
        timestamp: When the result was produced (UTC).
    """

    label: str
    score: float
    semantics: ScoreSemantics
    producer: str
    logit: Optional[float] = None
    source: str = ""
    evidence: Mapping[str, Any] = field(default_factory=dict)
    confidence: Optional[Any] = None
    timestamp: datetime = field(default_factory=_utcnow)

    def __post_init__(self) -> None:
        if self.semantics.is_probability and not 0.0 <= float(self.score) <= 1.0:
            raise ValueError(
                f"{self.producer}: score {self.score} is declared "
                f"{self.semantics.value} but lies outside [0, 1]."
            )

    @property
    def probability(self) -> float:
        """Return ``score`` as a probability.

        Raises:
            TypeError: If the semantics are not probabilistic.
        """
        if not self.semantics.is_probability:
            raise TypeError(
                f"{self.producer} produced a {self.semantics.value}, which is "
                "not a probability."
            )
        return float(self.score)

    @property
    def calibrated_probability(self) -> float:
        """Return ``score`` as the calibrated ``p_t`` of the frozen decision rule.

        Raises:
            TypeError: If the score has not been through the adopted calibrator.
                The expected-loss Bayes verdict is defined on a calibrated
                probability; feeding it an uncalibrated one would silently
                change the decision layer.
        """
        if not self.semantics.is_calibrated:
            raise TypeError(
                f"{self.producer} produced a {self.semantics.value}. The "
                "expected-loss Bayes verdict requires p_t from Platt-on-logit "
                "calibration (CLAUDE.md MATHEMATICAL LOCK)."
            )
        return float(self.score)


@dataclass(frozen=True)
class BehaviorResult:
    """Output of the Behavioral Analysis layer (L3) over a trajectory prefix.

    Attributes:
        score: The model's numeric output for the prefix.
        semantics: What ``score`` means.
        producer: Identifier of the behavioural algorithm.
        source: Citation of the equation(s) used.
        evidence: Supporting named values for audit.
        observe_only: ``True`` marks a signal that must not enter the verdict
            path. CUSUM, if used, is observe-only per § FROZEN REM PIPELINE.
        timestamp: When the result was produced (UTC).
    """

    score: float
    semantics: ScoreSemantics
    producer: str
    source: str = ""
    evidence: Mapping[str, Any] = field(default_factory=dict)
    observe_only: bool = False
    timestamp: datetime = field(default_factory=_utcnow)


class Verdict(str, Enum):
    """The four frozen REM verdicts (``CLAUDE.md`` § FROZEN REM PIPELINE).

    These are an adaptation of cost-sensitive expected-loss decision theory.
    Elkan supports the expected-cost decision principle and Chow is conceptual
    support for reject/abstain-style escalation; neither source may be presented
    as having invented REM's four-action architecture.
    """

    ALLOW = "allow"
    MODIFY = "modify"
    ESCALATE = "escalate"
    BLOCK = "block"


@dataclass(frozen=True)
class Decision:
    """A verdict from the Decision Engine layer (L4).

    Attributes:
        verdict: The selected verdict.
        producer: Identifier of the decision mechanism.
        rationale: Why this verdict was selected, in auditable terms.
        conditional_risk: ``R_t(v)`` for every verdict considered, so the
            argmin can be re-checked from the audit record alone.
        calibrated_probability: The ``p_t`` used.
        consequence_tier: The ``k_t`` used.
        source: Citation of the decision equation.
        timestamp: When the decision was made (UTC).
    """

    verdict: Verdict
    producer: str
    rationale: str
    conditional_risk: Mapping[str, float] = field(default_factory=dict)
    calibrated_probability: Optional[float] = None
    consequence_tier: Optional[Any] = None
    source: str = ""
    timestamp: datetime = field(default_factory=_utcnow)


class MitigationAction(str, Enum):
    """Canonical mitigation mechanisms (``CLAUDE.md`` § MITIGATION LOCK).

    The mapping from verdict to mechanism is fixed by the lock, not configurable:

    * ``RELEASE_ACTION`` — Allow: release the current action.
    * ``MODIFY_ACTION`` — Modify: apply ONE declared modification mechanism to
      the current action or execution context.
    * ``WITHHOLD_PENDING_REVIEW`` — Escalate: withhold the current action
      pending review.
    * ``PREVENT_EXECUTION`` — Block: prevent execution of the current proposed
      action.

    All four are **step-level**. Episode-level restrictions (disabling a tool
    class or all state-changing tools for the remainder of an episode) are a
    separate experimental policy requiring explicit specification, and are not
    part of this enumeration.
    """

    RELEASE_ACTION = "release_action"
    MODIFY_ACTION = "modify_action"
    WITHHOLD_PENDING_REVIEW = "withhold_pending_review"
    PREVENT_EXECUTION = "prevent_execution"


@dataclass(frozen=True)
class MitigationOutcome:
    """Result of applying the canonical mechanism for a verdict (L5).

    Attributes:
        action: The mechanism applied.
        applied: Whether it changed what the agent may do.
        producer: Identifier of the mitigation engine.
        detail: What concretely changed.
        replacement: Substituted content when ``action`` is ``MODIFY_ACTION``.
        timestamp: When the mitigation was applied (UTC).
    """

    action: MitigationAction
    applied: bool
    producer: str
    detail: str = ""
    replacement: Optional[Any] = None
    timestamp: datetime = field(default_factory=_utcnow)


@dataclass(frozen=True)
class FeatureAttribution:
    """Attribution assigned to a single feature.

    Attributes:
        feature: Feature name.
        value: The feature's value for the instance being explained.
        attribution: The Shapley value on the model's own (logit) scale.
    """

    feature: str
    value: Any
    attribution: float


@dataclass(frozen=True)
class AttributionResult:
    """Output of linear Shapley attribution — AUDIT ONLY.

    ``CLAUDE.md`` § MATHEMATICAL LOCK: linear Shapley attribution is audit-only
    and MUST NOT affect the verdict. § FORBIDDEN REINTRODUCTIONS additionally
    bars SHAP as a decision input. The pipeline enforces this structurally by
    computing attribution only after the decision is final.

    Attributes:
        attributions: Per-feature Shapley values.
        producer: Identifier of the attribution method.
        base_value: The reference value ``phi_0``, i.e. the model output at the
            background mean.
        source: Citation of the attribution equation.
        explanation: Security-facing summary derived from the attributions.
        timestamp: When produced (UTC).
    """

    attributions: Sequence[FeatureAttribution]
    producer: str
    base_value: Optional[float] = None
    source: str = ""
    explanation: str = ""
    timestamp: datetime = field(default_factory=_utcnow)

    #: Marks this payload as inadmissible to the decision layer. Checked by the
    #: decision engine, which refuses to accept an object carrying it.
    audit_only: bool = True

    def ranked(self) -> Sequence[FeatureAttribution]:
        """Return attributions ordered by decreasing magnitude.

        Ordering only — no aggregation or rescaling, so no unsourced arithmetic
        is introduced.
        """
        return tuple(
            sorted(self.attributions, key=lambda a: abs(a.attribution), reverse=True)
        )
