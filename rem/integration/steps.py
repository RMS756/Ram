"""Step records from recorded episodes (observe-only fitting data, EXPLORATORY).

Recorded traces are observe-only data by construction: the recorded agents ran
without REM, so no enforced verdict altered the trajectories (Chapter 3 Sec.
3.11.1: fitting data are collected in observe-only mode).

x^beh_4 depends on the benign reference transition set, which must be estimated
within each fold's fitting portion (Sec. 3.11.6). Each record therefore stores
its transition (previous proposed tool, tool); ``design_matrix`` recomputes
x^beh_4 for a given reference. All other features depend only on the episode.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from rem.algorithms.behavior.evidence import (
    FEATURE_ORDER,
    START,
    BenignReference,
    EpisodeTracker,
    EvidenceSpec,
)
from rem.algorithms.decision.consequence import ConsequenceTierMap
from rem.algorithms.detection.instruction_patterns import InstructionPatternDetector
from rem.integration.agentdojo_traces import Episode, ReferenceLabeler

__all__ = ["StepRecord", "build_steps", "design_matrix", "benign_tool_sequences", "injection_entered"]

_EMPTY_REFERENCE = BenignReference(frozenset())


@dataclass(frozen=True)
class StepRecord:
    episode_id: str
    pipeline: str
    user_task_id: str
    injection_task_id: Optional[str]
    attack_type: Optional[str]
    index: int                         # 1-based step index within the episode
    decision_point: int
    tool: str
    args: Mapping[str, object]
    features: Mapping[str, float]      # x^beh_4 computed against an EMPTY reference
    available: Mapping[str, bool]
    transition: Tuple[str, str]
    label: int
    tier: int
    after_change_point: bool           # injected content already in context
    attacker_key_match: bool
    executed_in_record: bool


def _norm_ws(text: str) -> str:
    return " ".join(str(text).split()).lower()


def injection_entered(text: str, injections: Mapping[str, str], probe_chars: int = 40) -> bool:
    """Whether a tool result contains any injected payload of the episode.

    The first ``probe_chars`` characters of each payload, whitespace-collapsed,
    are searched for, because tool outputs are re-serialised (YAML) by AgentDojo.
    """
    hay = _norm_ws(text)
    for payload in injections.values():
        probe = _norm_ws(payload)[:probe_chars]
        if probe and probe in hay:
            return True
    return False


def build_steps(
    episode: Episode,
    spec: EvidenceSpec,
    detector: InstructionPatternDetector,
    tier_map: ConsequenceTierMap,
    labeler: ReferenceLabeler,
) -> List[StepRecord]:
    """One record per proposed tool call, in order."""
    tracker = EpisodeTracker(
        objective=episode.objective,
        trusted_texts=[episode.system_prompt],
        spec=spec,
        detector=detector,
        reference=_EMPTY_REFERENCE,
    )
    out: List[StepRecord] = []
    changed = False
    results: Dict[str, bool] = {}
    # Map tool-call id -> whether the recorded tool message reports no error.
    for m in episode.messages:
        if m.role == "tool" and m.tool_call is not None:
            results[str(m.tool_call.id)] = m.error is None
    idx = 0
    for m in episode.messages:
        if m.role == "assistant" and m.tool_calls:
            tracker.begin_decision_point()
            for call in m.tool_calls:
                idx += 1
                feats, avail = tracker.features(call.function, call.args)
                prev = tracker.proposed[-1][0] if tracker.proposed else START
                out.append(
                    StepRecord(
                        episode_id=episode.episode_id,
                        pipeline=episode.pipeline,
                        user_task_id=episode.user_task_id,
                        injection_task_id=episode.injection_task_id,
                        attack_type=episode.attack_type,
                        index=idx,
                        decision_point=tracker.decision_point,
                        tool=call.function,
                        args=dict(call.args),
                        features=feats,
                        available=avail,
                        transition=(prev, call.function),
                        label=labeler.label(episode.injection_task_id, call.function, call.args),
                        tier=tier_map.tier(call.function, call.args),
                        after_change_point=changed,
                        attacker_key_match=labeler.attacker_key_match(call.function, call.args),
                        executed_in_record=results.get(str(call.id), True),
                    )
                )
                tracker.record_proposal(call.function, call.args)
        elif m.role == "tool":
            tool = m.tool_call.function if m.tool_call is not None else ""
            tracker.add_tool_result(tool, m.text, executed=m.error is None)
            if episode.injections and injection_entered(m.text, episode.injections):
                changed = True
    return out


def benign_tool_sequences(steps: Iterable[StepRecord]) -> List[List[str]]:
    """Proposed-tool sequences of episodes without injection, in step order."""
    seqs: Dict[str, List[Tuple[int, str]]] = {}
    for s in steps:
        if s.injection_task_id is None:
            seqs.setdefault(s.episode_id, []).append((s.index, s.tool))
    return [[t for _, t in sorted(v)] for v in seqs.values()]


def design_matrix(
    steps: Sequence[StepRecord],
    reference: BenignReference,
    feature_order: Sequence[str] = FEATURE_ORDER,
) -> np.ndarray:
    """X (n x d) in ``feature_order`` with x^beh_4 recomputed for ``reference``."""
    X = np.empty((len(steps), len(feature_order)), dtype=float)
    for i, s in enumerate(steps):
        for j, name in enumerate(feature_order):
            if name == "x_beh4":
                X[i, j] = float(s.transition not in reference.transitions)
            else:
                X[i, j] = float(s.features[name])
    return X
