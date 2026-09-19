"""Auditable decision records — the final stage of the frozen pipeline.

REM is a security framework, so every runtime decision must leave a record a
reviewer can reconstruct. Records are append-only JSON Lines.

Because the frozen decision rule is ``v* = argmin_v R_t(v)``, the record stores
the **full conditional-risk table** rather than only the chosen verdict: the
argmin can then be re-checked from the audit trail alone.

Data minimisation: prompts, model outputs and tool arguments are the agent's
payload and may carry sensitive content, so they are recorded as SHA-256
digests by default. That is enough to prove which payload a decision concerned
without retaining it. Verbatim capture is opt-in for offline experiments.

This module contains no mathematics. The digest is an identity function over
content, not a measurement.
"""

from __future__ import annotations

import hashlib
import json
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from rem.agent.trajectory import TrajectoryStep
from rem.core.results import (
    AttributionResult,
    BehaviorResult,
    Decision,
    DetectionResult,
    MitigationOutcome,
)

__all__ = ["AuditRecord", "AuditLog", "content_digest"]


def content_digest(value: Any) -> Optional[str]:
    """Return a short SHA-256 digest identifying ``value``.

    Args:
        value: Any content; non-strings are stringified first.

    Returns:
        A 16-hex-character digest, or ``None`` when ``value`` is ``None``.
    """
    if value is None:
        return None
    payload = value if isinstance(value, str) else repr(value)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass
class AuditRecord:
    """One auditable REM decision.

    Attributes:
        timestamp: When the decision was made (UTC, ISO-8601).
        trajectory_id: Trajectory the step belongs to.
        step_index: Position of the step within the trajectory.
        experiment_id: Experiment that produced the record, if any.
        agent_state: Observed agent state at the step.
        action: Normalised description of the agent's action.
        tool_name: Tool requested, if any.
        tool_arguments_digest: Digest of the tool arguments.
        prompt_digest: Digest of the step's prompt.
        model_output_digest: Digest of the model output.
        evidence: Evidence items extracted by L1.
        detector: Post-calibration detector summary, including ``s_t`` and ``p_t``.
        detector_uncalibrated: Pre-calibration summary, so the effect of the
            calibrator is visible in the record.
        behavior: Behavioural analysis summary.
        consequence_tier: ``k_t`` used.
        policy_predicates: Predicate outcomes.
        conditional_risk: The full ``R_t(v)`` table.
        decision: Verdict and rationale.
        mitigation: Mitigation applied.
        attribution: Ranked attributions (audit-only).
        versions: Code, config and model versions.
        payloads: Verbatim payloads, only when explicitly enabled.
    """

    timestamp: str
    trajectory_id: str
    step_index: int
    experiment_id: Optional[str] = None
    agent_state: Optional[str] = None
    action: Optional[str] = None
    tool_name: Optional[str] = None
    tool_arguments_digest: Optional[str] = None
    prompt_digest: Optional[str] = None
    model_output_digest: Optional[str] = None
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    detector: Optional[Dict[str, Any]] = None
    detector_uncalibrated: Optional[Dict[str, Any]] = None
    behavior: Optional[Dict[str, Any]] = None
    consequence_tier: Optional[Any] = None
    policy_predicates: Dict[str, bool] = field(default_factory=dict)
    conditional_risk: Dict[str, float] = field(default_factory=dict)
    decision: Optional[Dict[str, Any]] = None
    mitigation: Optional[Dict[str, Any]] = None
    attribution: Optional[List[Dict[str, Any]]] = None
    versions: Dict[str, Any] = field(default_factory=dict)
    payloads: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        """Serialise the record as a single JSON line."""
        return json.dumps(asdict(self), default=str, sort_keys=True)


class AuditLog:
    """Append-only audit log writing JSON Lines. Thread-safe."""

    def __init__(
        self,
        path: Optional[Path | str] = None,
        *,
        experiment_id: Optional[str] = None,
        versions: Optional[Mapping[str, Any]] = None,
        record_payloads: bool = False,
    ) -> None:
        """Initialise the log.

        Args:
            path: Destination JSONL file. ``None`` keeps records in memory.
            experiment_id: Stamped onto every record.
            versions: Code/model versions stamped onto every record.
            record_payloads: When ``True``, store prompts, outputs and tool
                arguments verbatim. Off by default (data minimisation).
        """
        self._path = Path(path) if path else None
        self._experiment_id = experiment_id
        self._versions = dict(versions or {})
        self._record_payloads = record_payloads
        self._lock = threading.Lock()
        self._records: List[AuditRecord] = []
        if self._path:
            self._path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def records(self) -> List[AuditRecord]:
        """Records written so far."""
        return list(self._records)

    def write(
        self,
        step: TrajectoryStep,
        trajectory_id: str,
        *,
        detection: Optional[DetectionResult] = None,
        raw_detection: Optional[DetectionResult] = None,
        behavior: Optional[BehaviorResult] = None,
        decision: Optional[Decision] = None,
        mitigation: Optional[MitigationOutcome] = None,
        attribution: Optional[AttributionResult] = None,
        predicates: Optional[Mapping[str, bool]] = None,
    ) -> AuditRecord:
        """Build, append and persist an audit record for ``step``.

        Returns:
            The record written.
        """
        record = AuditRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            trajectory_id=trajectory_id,
            step_index=step.step_index,
            experiment_id=self._experiment_id,
            agent_state=step.agent_state.value if step.agent_state else None,
            action=step.action,
            tool_name=step.tool_call.name if step.tool_call else None,
            tool_arguments_digest=content_digest(dict(step.tool_arguments) or None),
            prompt_digest=content_digest(step.prompt),
            model_output_digest=content_digest(step.model_output),
            evidence=[
                {
                    "name": e.name,
                    "value": e.value,
                    "producer": e.producer,
                    "detail": e.detail,
                }
                for e in step.evidence
            ],
            detector=_summarise_detection(detection),
            detector_uncalibrated=_summarise_detection(raw_detection),
            behavior=_summarise_behavior(behavior),
            consequence_tier=decision.consequence_tier if decision else step.consequence_tier,
            policy_predicates=dict(predicates or {}),
            conditional_risk=dict(decision.conditional_risk) if decision else {},
            decision=_summarise_decision(decision),
            mitigation=_summarise_mitigation(mitigation),
            attribution=_summarise_attribution(attribution),
            versions=dict(self._versions),
            payloads=(
                {
                    "prompt": step.prompt,
                    "model_output": step.model_output,
                    "tool_arguments": dict(step.tool_arguments),
                }
                if self._record_payloads
                else None
            ),
        )
        with self._lock:
            self._records.append(record)
            if self._path:
                with self._path.open("a", encoding="utf-8") as handle:
                    handle.write(record.to_json() + "\n")
        return record


def _summarise_detection(result: Optional[DetectionResult]) -> Optional[Dict[str, Any]]:
    if result is None:
        return None
    return {
        "producer": result.producer,
        "label": result.label,
        "score": result.score,
        "semantics": result.semantics.value,
        "logit": result.logit,
        "source": result.source,
        "evidence": dict(result.evidence),
        "confidence": result.confidence,
    }


def _summarise_behavior(result: Optional[BehaviorResult]) -> Optional[Dict[str, Any]]:
    if result is None:
        return None
    return {
        "producer": result.producer,
        "score": result.score,
        "semantics": result.semantics.value,
        "observe_only": result.observe_only,
        "source": result.source,
    }


def _summarise_decision(decision: Optional[Decision]) -> Optional[Dict[str, Any]]:
    if decision is None:
        return None
    return {
        "verdict": decision.verdict.value,
        "producer": decision.producer,
        "rationale": decision.rationale,
        "calibrated_probability": decision.calibrated_probability,
        "source": decision.source,
    }


def _summarise_mitigation(outcome: Optional[MitigationOutcome]) -> Optional[Dict[str, Any]]:
    if outcome is None:
        return None
    return {
        "action": outcome.action.value,
        "applied": outcome.applied,
        "producer": outcome.producer,
        "detail": outcome.detail,
    }


def _summarise_attribution(result: Optional[AttributionResult]) -> Optional[List[Dict[str, Any]]]:
    if result is None:
        return None
    return [
        {"feature": a.feature, "value": a.value, "attribution": a.attribution}
        for a in result.ranked()
    ]
