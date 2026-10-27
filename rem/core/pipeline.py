"""REM runtime pipeline — the FROZEN stage order.

``CLAUDE.md`` § FROZEN REM PIPELINE::

    provenance labeling
    -> context / behavioral / action evidence
    -> ridge logistic regression
    -> Platt calibration on the logit
    -> consequence tier
    -> policy predicates
    -> expected-loss Bayes verdict
    -> deterministic mitigation
    -> audit record

Attribution runs **after** the verdict is final, so linear Shapley output cannot
reach the decision engine. There is no feedback stage: § FROZEN ARCHITECTURE
states there is no feedback-loop layer.

The pipeline contains no mathematics. It sequences layers, enforces causal
evaluation (a step is scored using only the prefix strictly before it), and
records an audit entry for every step.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from rem.agent.trajectory import Trajectory, TrajectoryStep
from rem.core.audit import AuditLog, AuditRecord
from rem.core.interfaces import (
    Attributor,
    BehaviorModel,
    Calibrator,
    ConsequenceTierAssigner,
    ContextProcessor,
    DecisionEngine,
    DesignNotSpecifiedError,
    Detector,
    FeatureVector,
    MitigationEngine,
    PolicyPredicate,
    ProvenanceLabeler,
)
from rem.core.results import (
    AttributionResult,
    BehaviorResult,
    Decision,
    DetectionResult,
    MitigationOutcome,
)

__all__ = ["Layer", "AblationSpec", "StepEvaluation", "RemPipeline"]


class Layer:
    """Ablatable elements of the frozen architecture.

    The five frozen layers, plus the two cross-cutting/audit elements that can
    be switched off without changing the layer count. There is deliberately no
    ``FEEDBACK`` member.
    """

    CONTEXT = "context"            # L1 Input & Context
    DETECTION = "detection"        # L2 Detection
    BEHAVIOR = "behavior"          # L3 Behavioral Analysis
    DECISION = "decision"          # L4 Decision Engine
    MITIGATION = "mitigation"      # L5 Mitigation
    CALIBRATION = "calibration"    # cross-cutting
    ATTRIBUTION = "attribution"    # audit-only

    ALL = (CONTEXT, DETECTION, BEHAVIOR, DECISION, MITIGATION, CALIBRATION, ATTRIBUTION)

    #: The five frozen architecture layers, for assertions and documentation.
    FROZEN_LAYERS = (CONTEXT, DETECTION, BEHAVIOR, DECISION, MITIGATION)


@dataclass(frozen=True)
class AblationSpec:
    """Which elements are disabled for a run.

    Attributes:
        disabled: Element names to disable.
        label: Human-readable configuration name.
    """

    disabled: frozenset = field(default_factory=frozenset)
    label: str = "Full REM"

    @classmethod
    def full(cls) -> "AblationSpec":
        """The complete framework, nothing disabled."""
        return cls(frozenset(), "Full REM")

    @classmethod
    def without(cls, *elements: str) -> "AblationSpec":
        """Disable the named elements.

        Raises:
            ValueError: On an unknown element name.
        """
        unknown = [e for e in elements if e not in Layer.ALL]
        if unknown:
            raise ValueError(
                f"Unknown element(s) {unknown}; expected any of {list(Layer.ALL)}. "
                "Note there is no feedback layer in the frozen architecture."
            )
        pretty = ", ".join(e.capitalize() for e in elements)
        return cls(frozenset(elements), f"REM - {pretty}")

    def enabled(self, element: str) -> bool:
        """Whether ``element`` participates in the run."""
        return element not in self.disabled


@dataclass
class StepEvaluation:
    """Everything REM produced for one step.

    Attributes:
        step: The evaluated step.
        features: Evidence vector ``x_t``, if L1 ran.
        behavior: Behavioural result, if L3 ran.
        raw_detection: Detector output before calibration (``s_t``, ``p_tilde_t``).
        detection: Detection result after calibration (``p_t``).
        consequence_tier: ``k_t``, if assigned.
        predicates: Policy predicate outcomes.
        decision: The verdict, if L4 ran.
        mitigation: The mitigation outcome, if L5 ran.
        attribution: Audit-only attributions, if enabled.
        audit_record: The audit entry written for this step.
    """

    step: TrajectoryStep
    features: Optional[FeatureVector] = None
    behavior: Optional[BehaviorResult] = None
    raw_detection: Optional[DetectionResult] = None
    detection: Optional[DetectionResult] = None
    consequence_tier: Optional[Any] = None
    predicates: Mapping[str, bool] = field(default_factory=dict)
    decision: Optional[Decision] = None
    mitigation: Optional[MitigationOutcome] = None
    attribution: Optional[AttributionResult] = None
    audit_record: Optional[AuditRecord] = None


class RemPipeline:
    """Runtime evaluation and mitigation pipeline for the frozen design.

    Components are injected rather than constructed here, so a run can be
    reconstructed from its configuration and so baselines reuse the harness.
    """

    def __init__(
        self,
        *,
        provenance_labeler: Optional[ProvenanceLabeler] = None,
        context_processor: Optional[ContextProcessor] = None,
        behavior_model: Optional[BehaviorModel] = None,
        detector: Optional[Detector] = None,
        calibrator: Optional[Calibrator] = None,
        tier_assigner: Optional[ConsequenceTierAssigner] = None,
        policy_predicate: Optional[PolicyPredicate] = None,
        decision_engine: Optional[DecisionEngine] = None,
        mitigation_engine: Optional[MitigationEngine] = None,
        attributor: Optional[Attributor] = None,
        audit_log: Optional[AuditLog] = None,
        ablation: Optional[AblationSpec] = None,
    ) -> None:
        """Initialise the pipeline.

        Args:
            provenance_labeler: Stage 1 of the frozen pipeline.
            context_processor: L1 evidence extraction.
            behavior_model: L3 behavioural analysis.
            detector: L2 detection (ridge logistic regression).
            calibrator: Cross-cutting Platt-on-logit calibration.
            tier_assigner: Consequence tier ``k_t``.
            policy_predicate: Policy predicates.
            decision_engine: L4 expected-loss Bayes verdict.
            mitigation_engine: L5 deterministic mitigation.
            attributor: Audit-only linear Shapley attribution.
            audit_log: Destination for audit records; in-memory if ``None``.
            ablation: Which elements to disable.
        """
        self.provenance_labeler = provenance_labeler
        self.context_processor = context_processor
        self.behavior_model = behavior_model
        self.detector = detector
        self.calibrator = calibrator
        self.tier_assigner = tier_assigner
        self.policy_predicate = policy_predicate
        self.decision_engine = decision_engine
        self.mitigation_engine = mitigation_engine
        self.attributor = attributor
        self.audit_log = audit_log or AuditLog()
        self.ablation = ablation or AblationSpec.full()

    # -- introspection ------------------------------------------------------

    def missing_components(self) -> List[str]:
        """Return enabled elements that have no implementation attached."""
        attached = {
            Layer.CONTEXT: self.context_processor,
            Layer.DETECTION: self.detector,
            Layer.BEHAVIOR: self.behavior_model,
            Layer.DECISION: self.decision_engine,
            Layer.MITIGATION: self.mitigation_engine,
            Layer.CALIBRATION: self.calibrator,
            Layer.ATTRIBUTION: self.attributor,
        }
        return [
            name
            for name, impl in attached.items()
            if self.ablation.enabled(name) and impl is None
        ]

    # -- evaluation ---------------------------------------------------------

    def evaluate_step(self, trajectory: Trajectory, step: TrajectoryStep) -> StepEvaluation:
        """Evaluate one step in the frozen stage order.

        Args:
            trajectory: The trajectory containing ``step``.
            step: The step to evaluate.

        Returns:
            The evaluation, with an audit record attached.

        Raises:
            DesignNotSpecifiedError: If calibration is disabled while the
                decision engine is enabled — the frozen decision rule is
                defined on a calibrated probability, so this is not a valid
                ablation of the frozen design.
        """
        history = trajectory.prefix(step.step_index)
        evaluation = StepEvaluation(step=step)

        # Stage 1 — provenance labeling.
        if self.provenance_labeler is not None:
            self.provenance_labeler.label(step)

        # L3 — behavioural analysis, feeding the evidence stage.
        if self.ablation.enabled(Layer.BEHAVIOR) and self.behavior_model:
            evaluation.behavior = self.behavior_model.score(history)

        # Stage 2 / L1 — context, behavioural and action evidence.
        if self.ablation.enabled(Layer.CONTEXT) and self.context_processor:
            evaluation.features = self.context_processor.process(
                step, history, evaluation.behavior
            )

        # Stage 3 / L2 — ridge logistic regression.
        if self.ablation.enabled(Layer.DETECTION) and self.detector:
            features = evaluation.features or FeatureVector({}, producer="none")
            raw = self.detector.detect(features, step)
            evaluation.raw_detection = raw
            evaluation.detection = raw

            # Stage 4 — Platt calibration on the logit.
            if self.ablation.enabled(Layer.CALIBRATION):
                if self.calibrator is None:
                    raise DesignNotSpecifiedError(
                        "pipeline",
                        "a calibrator — the frozen pipeline routes s_t through "
                        "Platt-on-logit before the verdict",
                        supervisor=False,
                    )
                evaluation.detection = self.calibrator.transform(raw)
            elif self.ablation.enabled(Layer.DECISION) and self.decision_engine:
                raise DesignNotSpecifiedError(
                    "pipeline",
                    "calibrated p_t — 'REM - Calibration' is not a valid "
                    "ablation of the frozen design, because the expected-loss "
                    "Bayes verdict is defined on the calibrated probability. "
                    "Ablate the decision layer too, or specify a different "
                    "decision rule as an explicit experimental policy",
                    supervisor=False,
                )

        # Stages 5-7 / L4 — consequence tier, policy predicates, Bayes verdict.
        if self.ablation.enabled(Layer.DECISION) and self.decision_engine:
            if self.tier_assigner is not None:
                evaluation.consequence_tier = self.tier_assigner.assign(step, history)
                step.consequence_tier = evaluation.consequence_tier
            else:
                evaluation.consequence_tier = step.consequence_tier
            if self.policy_predicate is not None:
                evaluation.predicates = dict(self.policy_predicate.evaluate(step, history))
            if evaluation.detection is None:
                raise DesignNotSpecifiedError(
                    "pipeline",
                    "a detection result — the decision engine requires p_t",
                    supervisor=False,
                )
            evaluation.decision = self.decision_engine.decide(
                evaluation.detection,
                evaluation.consequence_tier,
                evaluation.predicates,
                step,
            )
            step.decision = evaluation.decision

        # Stage 8 / L5 — deterministic mitigation.
        if (
            self.ablation.enabled(Layer.MITIGATION)
            and self.mitigation_engine
            and evaluation.decision is not None
        ):
            evaluation.mitigation = self.mitigation_engine.apply(evaluation.decision, step)

        # Audit-only attribution, AFTER the verdict is final.
        if (
            self.ablation.enabled(Layer.ATTRIBUTION)
            and self.attributor
            and evaluation.detection is not None
            and evaluation.features is not None
        ):
            evaluation.attribution = self.attributor.attribute(
                evaluation.features, evaluation.detection
            )

        # Stage 9 — audit record.
        evaluation.audit_record = self.audit_log.write(
            step,
            trajectory.trajectory_id,
            detection=evaluation.detection,
            raw_detection=evaluation.raw_detection,
            behavior=evaluation.behavior,
            decision=evaluation.decision,
            mitigation=evaluation.mitigation,
            attribution=evaluation.attribution,
            predicates=evaluation.predicates,
        )
        return evaluation

    def evaluate(self, trajectory: Trajectory) -> List[StepEvaluation]:
        """Evaluate every step of ``trajectory`` in execution order."""
        return [self.evaluate_step(trajectory, step) for step in trajectory]

    def describe(self) -> Dict[str, Any]:
        """Return a provenance summary of the configured pipeline."""
        return {
            "ablation": self.ablation.label,
            "disabled": sorted(self.ablation.disabled),
            "frozen_layers": list(Layer.FROZEN_LAYERS),
            "components": {
                "provenance_labeler": _describe(self.provenance_labeler),
                Layer.CONTEXT: _describe(self.context_processor),
                Layer.BEHAVIOR: _describe(self.behavior_model),
                Layer.DETECTION: _describe(self.detector),
                Layer.CALIBRATION: _describe(self.calibrator),
                "tier_assigner": _describe(self.tier_assigner),
                "policy_predicate": _describe(self.policy_predicate),
                Layer.DECISION: _describe(self.decision_engine),
                Layer.MITIGATION: _describe(self.mitigation_engine),
                Layer.ATTRIBUTION: _describe(self.attributor),
            },
            "missing": self.missing_components(),
        }


def _describe(component: Any) -> Optional[str]:
    if component is None:
        return None
    return getattr(component, "name", type(component).__name__)
