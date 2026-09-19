"""Layer contracts for the FROZEN REM architecture.

``CLAUDE.md`` § FROZEN ARCHITECTURE fixes exactly five layers:

    L1 Input & Context
    L2 Detection
    L3 Behavioral Analysis
    L4 Decision Engine
    L5 Mitigation

Offline fitting and recalibration are cross-cutting. There is no sixth layer,
no separate risk-score layer, no operator/user-interaction node and **no
feedback-loop layer**. Attribution is audit-only and is therefore not a layer.

This module defines contracts and fail-closed placeholders only. It contains no
mathematics; the frozen equations live in ``rem/algorithms/``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Sequence

from rem.agent.trajectory import Trajectory, TrajectoryStep
from rem.core.results import (
    AttributionResult,
    BehaviorResult,
    Decision,
    DetectionResult,
    MitigationOutcome,
)

__all__ = [
    "DesignNotSpecifiedError",
    "FeatureVector",
    "ProvenanceLabeler",
    "ContextProcessor",
    "Detector",
    "BehaviorModel",
    "Calibrator",
    "ConsequenceTierAssigner",
    "PolicyPredicate",
    "DecisionEngine",
    "MitigationEngine",
    "Attributor",
    "UnspecifiedProvenanceLabeler",
    "UnspecifiedContextProcessor",
    "UnspecifiedConsequenceTierAssigner",
    "UnspecifiedPolicyPredicate",
    "NullBehaviorModel",
]


class DesignNotSpecifiedError(NotImplementedError):
    """Raised when a component whose design input is unresolved is invoked.

    This is the runtime form of ``CLAUDE.md`` § IMPLEMENTATION FAIL-CLOSED
    REQUIREMENT: REM must refuse to run rather than fall back to a guessed
    default, an arbitrary threshold, an arbitrary cost or an arbitrary feature
    definition.
    """

    def __init__(self, component: str, needs: str, *, supervisor: bool = True) -> None:
        super().__init__(
            f"\n## DESIGN BLOCKED\n"
            f"**Item:** {needs}\n"
            f"**Why required:** component {component!r} cannot run without it.\n"
            f"**Current source status:** not frozen in any supplied document.\n"
            f"**Safe action:** STOP — do not choose a value.\n"
            f"**Supervisor decision needed:** {'YES' if supervisor else 'NO'}\n"
            f"See RECONCILIATION.md."
        )
        self.component = component
        self.needs = needs
        self.supervisor = supervisor


class FeatureVector(Mapping[str, float]):
    """The evidence vector ``x_t`` consumed by the Detection layer.

    Named rather than positional, so that Shapley attributions tie back to a
    meaningful feature name and so that adding a feature cannot silently shift
    the meaning of an existing index.
    """

    def __init__(self, values: Mapping[str, float], producer: str) -> None:
        self._values = dict(values)
        self._producer = producer

    @property
    def producer(self) -> str:
        """Identifier of the component that produced this vector."""
        return self._producer

    @property
    def names(self) -> Sequence[str]:
        """Feature names in insertion order."""
        return tuple(self._values)

    def as_sequence(self, order: Sequence[str]) -> list[float]:
        """Return values in an explicit feature order.

        Args:
            order: The feature order the fitted model was trained with.

        Returns:
            Values in that order.

        Raises:
            KeyError: If a required feature is absent. Silently substituting a
                value for a missing feature would corrupt ``s_t``.
        """
        missing = [name for name in order if name not in self._values]
        if missing:
            raise KeyError(
                f"FeatureVector from {self._producer!r} is missing required "
                f"feature(s) {missing}; REM does not impute missing evidence."
            )
        return [float(self._values[name]) for name in order]

    def __getitem__(self, key: str) -> float:
        return self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"FeatureVector(producer={self._producer!r}, names={list(self._values)})"


# ---------------------------------------------------------------------------
# L1 — Input & Context
# ---------------------------------------------------------------------------


class ProvenanceLabeler(ABC):
    """Assigns provenance labels to content reaching the agent.

    First stage of the frozen pipeline. The labeling rule is not frozen.
    """

    name: str = "provenance_labeler"

    @abstractmethod
    def label(self, step: TrajectoryStep) -> TrajectoryStep:
        """Assign provenance labels to ``step`` in place and return it."""


class ContextProcessor(ABC):
    """Extracts context / behavioural / action evidence into ``x_t``.

    The frozen pipeline's second stage is *context / behavioral / action
    evidence*, so behavioural analysis (L3) feeds this stage rather than
    bypassing it into the verdict.
    """

    name: str = "context_processor"

    @abstractmethod
    def process(
        self,
        step: TrajectoryStep,
        history: Trajectory,
        behavior: Optional[BehaviorResult] = None,
    ) -> FeatureVector:
        """Extract the evidence vector for ``step``.

        Args:
            step: The step being evaluated.
            history: Trajectory prefix strictly preceding ``step``.
            behavior: Behavioural analysis output for the prefix, when L3 is
                enabled. Observe-only signals must not be turned into features.

        Returns:
            The evidence vector ``x_t``.
        """


# ---------------------------------------------------------------------------
# L2 — Detection
# ---------------------------------------------------------------------------


class Detector(ABC):
    """Produces ``s_t`` and ``p_tilde_t`` for a step.

    In the frozen design the detector is ridge logistic regression.
    """

    name: str = "detector"

    @abstractmethod
    def detect(
        self,
        features: FeatureVector,
        step: TrajectoryStep,
    ) -> DetectionResult:
        """Return the detection result for ``step``."""


# ---------------------------------------------------------------------------
# L3 — Behavioral Analysis
# ---------------------------------------------------------------------------


class BehaviorModel(ABC):
    """Analyses behaviour over a trajectory prefix.

    Any behavioural signal that is observe-only (CUSUM, per § FROZEN REM
    PIPELINE) must set ``observe_only=True`` on its result. The decision engine
    refuses observe-only inputs.
    """

    name: str = "behavior_model"

    @abstractmethod
    def score(self, history: Trajectory) -> BehaviorResult:
        """Analyse the behaviour observed in ``history``."""


# ---------------------------------------------------------------------------
# Cross-cutting — offline fitting and recalibration
# ---------------------------------------------------------------------------


class Calibrator(ABC):
    """Maps the detector logit onto a calibrated probability.

    The adopted calibrator is Platt/logistic calibration on the logit. Beta,
    isotonic and temperature calibration are forbidden reintroductions.

    ``fit`` and ``transform`` are separate so calibration is fitted on a
    held-out split and never on test data.
    """

    name: str = "calibrator"

    @abstractmethod
    def fit(self, logits: Sequence[float], labels: Sequence[int]) -> None:
        """Fit the calibration map on held-out logits and labels."""

    @abstractmethod
    def transform(self, result: DetectionResult) -> DetectionResult:
        """Return ``result`` with ``p_t`` and calibrated semantics."""


# ---------------------------------------------------------------------------
# L4 — Decision Engine
# ---------------------------------------------------------------------------


class ConsequenceTierAssigner(ABC):
    """Assigns the consequence tier ``k_t`` to a step.

    ``k_t`` indexes the loss function ``L(v, y, k_t)``. Tiers are unresolved.
    """

    name: str = "consequence_tier_assigner"

    @abstractmethod
    def assign(self, step: TrajectoryStep, history: Trajectory) -> Any:
        """Return ``k_t`` for ``step``."""


class PolicyPredicate(ABC):
    """A policy predicate evaluated between tiering and the Bayes verdict.

    Named in the frozen pipeline; contents unresolved.
    """

    name: str = "policy_predicate"

    @abstractmethod
    def evaluate(self, step: TrajectoryStep, history: Trajectory) -> Mapping[str, bool]:
        """Return the predicate outcomes for ``step``."""


class DecisionEngine(ABC):
    """Selects a verdict. In the frozen design: expected-loss Bayes."""

    name: str = "decision_engine"

    @abstractmethod
    def decide(
        self,
        detection: DetectionResult,
        consequence_tier: Any,
        predicates: Mapping[str, bool],
        step: TrajectoryStep,
    ) -> Decision:
        """Return the verdict for ``step``.

        Note the absence of an attribution parameter: linear Shapley attribution
        is audit-only and must not reach this method.
        """


# ---------------------------------------------------------------------------
# L5 — Mitigation
# ---------------------------------------------------------------------------


class MitigationEngine(ABC):
    """Applies the canonical mechanism for a verdict."""

    name: str = "mitigation_engine"

    @abstractmethod
    def apply(self, decision: Decision, step: TrajectoryStep) -> MitigationOutcome:
        """Apply mitigation for ``decision`` to ``step``."""


# ---------------------------------------------------------------------------
# Audit-only — not a layer
# ---------------------------------------------------------------------------


class Attributor(ABC):
    """Explains a detection result feature-wise. AUDIT ONLY."""

    name: str = "attributor"

    @abstractmethod
    def attribute(
        self,
        features: FeatureVector,
        detection: DetectionResult,
    ) -> AttributionResult:
        """Return per-feature attributions for ``detection``."""


# ---------------------------------------------------------------------------
# Fail-closed placeholders for unresolved design items
# ---------------------------------------------------------------------------


class UnspecifiedProvenanceLabeler(ProvenanceLabeler):
    """Placeholder: the provenance labeling rule is not frozen."""

    name = "unspecified_provenance_labeler"

    def label(self, step: TrajectoryStep) -> TrajectoryStep:
        raise DesignNotSpecifiedError(
            self.name,
            "the provenance labeling rule (first stage of the frozen pipeline; "
            "named in CLAUDE.md but never defined)",
        )


class UnspecifiedContextProcessor(ContextProcessor):
    """Placeholder: the final feature set is unresolved."""

    name = "unspecified_context_processor"

    def process(
        self,
        step: TrajectoryStep,
        history: Trajectory,
        behavior: Optional[BehaviorResult] = None,
    ) -> FeatureVector:
        raise DesignNotSpecifiedError(
            self.name,
            "the final feature set x_t (listed as unresolved in CLAUDE.md "
            "DATA / EVALUATION LOCK)",
        )


class UnspecifiedConsequenceTierAssigner(ConsequenceTierAssigner):
    """Placeholder: consequence tiers are unresolved."""

    name = "unspecified_consequence_tier_assigner"

    def assign(self, step: TrajectoryStep, history: Trajectory) -> Any:
        raise DesignNotSpecifiedError(
            self.name,
            "the consequence tiers k_t (listed as unresolved in CLAUDE.md "
            "DATA / EVALUATION LOCK)",
        )


class UnspecifiedPolicyPredicate(PolicyPredicate):
    """Placeholder: policy predicates are unresolved."""

    name = "unspecified_policy_predicate"

    def evaluate(self, step: TrajectoryStep, history: Trajectory) -> Mapping[str, bool]:
        raise DesignNotSpecifiedError(
            self.name,
            "the policy predicates (named in the frozen pipeline; contents "
            "never specified)",
        )


class NullBehaviorModel(BehaviorModel):
    """Inert behavioural model, for the ``REM - Behavioral Analysis`` ablation."""

    name = "ablation_no_behavior"

    def score(self, history: Trajectory) -> BehaviorResult:
        raise DesignNotSpecifiedError(
            self.name,
            "nothing — this is an ablation stub and must not be scored",
            supervisor=False,
        )
