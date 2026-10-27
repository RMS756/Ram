"""Shared setup for the EXPLORATORY pilot (configs/exploratory/pilot_e0.yaml).

Every declared value is read from the pre-registered configuration; nothing is
defaulted here. Outputs go to results/pilot/ and are stamped with LABEL.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO)

from rem.algorithms.behavior.evidence import EvidenceSpec  # noqa: E402
from rem.algorithms.decision.consequence import ConsequenceTierMap  # noqa: E402
from rem.algorithms.detection.instruction_patterns import InstructionPatternDetector  # noqa: E402
from rem.integration.agentdojo_traces import ReferenceLabeler, ReferenceSolutions  # noqa: E402

CONFIG = os.path.join(REPO, "configs", "exploratory", "pilot_e0.yaml")
AMENDMENTS = os.path.join(REPO, "configs", "exploratory", "pilot_e0_amendments.yaml")
RESULTS = os.path.join(REPO, "results", "pilot")
RUNS = os.environ.get("AGENTDOJO_RUNS", "/home/user/ethz-spylab/agentdojo/runs")


def load_config() -> Dict[str, Any]:
    with open(CONFIG, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


LABEL = load_config()["meta"]["label"]


@dataclass
class Setup:
    cfg: Dict[str, Any]
    suite: Any
    spec: EvidenceSpec
    detector: InstructionPatternDetector
    tier_map: ConsequenceTierMap
    labeler: ReferenceLabeler
    restricted: Tuple[str, ...]


def make_setup(amount_limit: float = None) -> Setup:
    from agentdojo.task_suite.load_suites import get_suites

    cfg = load_config()
    F, C, D = cfg["features"], cfg["consequence"], cfg["data"]
    suite = get_suites(D["suite_version_for_replay"])[D["suite"]]
    spec = EvidenceSpec(F["n_max"], F["key_arguments"], F["privilege_map"], F["sensitive_read_tools"])
    det = InstructionPatternDetector(
        F["instruction_patterns"], [t.name for t in suite.tools] if F["mention_tool_names"] else None
    )
    tm = ConsequenceTierMap(C["categories"], C["tier_map"], C["amount_limit"] if amount_limit is None else amount_limit)
    lab = ReferenceLabeler(
        ReferenceSolutions.from_agentdojo(D["suite_version_for_replay"], D["suite"]),
        cfg["labels"]["attacker_key_arguments"],
        C["categories"]["read"],
        bool(cfg["labels"]["induced_read_steps_positive"]),
    )
    return Setup(cfg, suite, spec, det, tm, lab, tuple(C["restricted_tools_T_R"]))


def provenance() -> Dict[str, Any]:
    """Versions recorded with every result file (Chapter 3 Sec. 3.11.1)."""
    import agentdojo
    import numpy

    def sha(path):
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()

    try:
        commit = subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"], text=True).strip()
    except Exception:  # pragma: no cover
        commit = None
    try:
        runs_commit = subprocess.check_output(["git", "-C", os.path.dirname(RUNS), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        runs_commit = None
    return {
        "label": LABEL,
        "rem_commit": commit,
        "config_sha256": sha(CONFIG),
        "amendments_sha256": sha(AMENDMENTS),
        "agentdojo_package": getattr(agentdojo, "__version__", None) or _pkg_version("agentdojo"),
        "agentdojo_runs_commit": runs_commit,
        "python": platform.python_version(),
        "numpy": numpy.__version__,
    }


def _pkg_version(name):
    try:
        from importlib.metadata import version

        return version(name)
    except Exception:
        return None


def write_json(name: str, obj: Any) -> str:
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"_label": LABEL, **obj} if isinstance(obj, dict) else {"_label": LABEL, "data": obj},
                  fh, indent=1, default=_default)
    return path


def _default(o):
    import numpy as np

    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, frozenset, tuple)):
        return list(o)
    return str(o)
