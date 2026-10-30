"""Dataset arrays, fold assignment and fold-specific design matrices (EXPLORATORY)."""

from __future__ import annotations

import hashlib
import os
import pickle
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import numpy as np

from common import RESULTS

from rem.algorithms.behavior.evidence import FEATURE_GROUPS, FEATURE_ORDER, BenignReference
from rem.evaluation.crossfit import assign_round_robin
from rem.integration.steps import StepRecord, design_matrix


@dataclass
class Data:
    steps: List[StepRecord]
    episodes: Dict[str, object]          # episode_id -> Episode
    role: Dict[str, str]                 # episode_id -> role
    y: np.ndarray
    attacked: np.ndarray                 # step belongs to an attacked episode
    fold: np.ndarray                     # outer fold (injection-task name) per step
    inner_group: np.ndarray
    episode_fold: Dict[str, str]


def load_raw():
    with open(os.path.join(RESULTS, "steps.pkl"), "rb") as fh:
        return pickle.load(fh)


def build(role: str = "primary", raw=None, grouping: str = "injection_task") -> Data:
    """Steps of one role with outer folds per Chapter 3 Sec. 3.11.5.

    grouping:
      ``injection_task`` (primary): attacked -> injection task; benign episodes ->
          user task assigned round robin to the nine folds.
      ``user_task`` (sensitivity): every step -> its user task.
      ``pipeline``: leave-one-backbone-out.
    """
    raw = raw or load_raw()
    eps = {e["episode"].episode_id: e["episode"] for e in raw["episodes"] if e["role"] == role}
    roles = {e["episode"].episode_id: e["role"] for e in raw["episodes"]}
    steps = [s for r, _, ss in raw["steps"] if r == role for s in ss]
    inj = sorted({e.injection_task_id for e in eps.values() if e.injection_task_id}, key=str)
    users = sorted({e.user_task_id for e in eps.values()}, key=str)
    rr = assign_round_robin(users, len(inj))
    ep_fold = {}
    for eid, e in eps.items():
        if grouping == "injection_task":
            ep_fold[eid] = e.injection_task_id if e.injection_task_id else inj[rr[e.user_task_id]]
        elif grouping == "user_task":
            ep_fold[eid] = e.user_task_id
        elif grouping == "pipeline":
            ep_fold[eid] = e.pipeline
        else:
            raise ValueError(grouping)
    y = np.array([s.label for s in steps], dtype=int)
    attacked = np.array([s.injection_task_id is not None for s in steps])
    fold = np.array([ep_fold[s.episode_id] for s in steps], dtype=object)
    inner = np.array([s.injection_task_id if s.injection_task_id else s.user_task_id for s in steps], dtype=object)
    return Data(steps, eps, roles, y, attacked, fold, inner, ep_fold)


def reference_from_mask(data: Data, mask: np.ndarray) -> BenignReference:
    """Benign transition set from episodes WITHOUT injection inside ``mask`` (AM-2)."""
    seqs: Dict[str, list] = {}
    for i in np.flatnonzero(mask & ~data.attacked):
        s = data.steps[i]
        seqs.setdefault(s.episode_id, []).append((s.index, s.tool))
    return BenignReference.fit([[t for _, t in sorted(v)] for v in seqs.values()])


class Designer:
    """design(mask) -> X with x^beh_4 from the masked benign episodes; cached."""

    def __init__(self, data: Data, feature_order: Sequence[str] = FEATURE_ORDER, steps: Optional[list] = None):
        self.data = data
        self.order = tuple(feature_order)
        self.steps = steps if steps is not None else data.steps
        self._cache: Dict[str, np.ndarray] = {}

    def __call__(self, mask: np.ndarray) -> np.ndarray:
        key = hashlib.sha1(np.packbits(mask).tobytes()).hexdigest()
        if key not in self._cache:
            self._cache[key] = design_matrix(self.steps, reference_from_mask(self.data, mask), self.order)
        return self._cache[key]


def features_without(groups: Sequence[str]) -> tuple:
    drop = {f for g in groups for f in FEATURE_GROUPS[g]}
    return tuple(f for f in FEATURE_ORDER if f not in drop)
