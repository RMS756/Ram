"""Reproducibility support: seeding, experiment identity, environment capture.

No mathematics; seeding and manifest capture only.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

__all__ = ["seed_everything", "new_experiment_id", "EnvironmentManifest", "file_digest"]


def seed_everything(seed: int) -> Dict[str, Any]:
    """Seed every random source REM may use.

    Seeds the stdlib generator and ``PYTHONHASHSEED``, plus NumPy and PyTorch if
    installed, and reports what was actually seeded so an experiment log shows
    which sources were under control.

    Args:
        seed: The seed value.

    Returns:
        Mapping from source name to what was seeded.
    """
    seeded: Dict[str, Any] = {"seed": seed}
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    seeded["python_random"] = True

    try:
        import numpy as np

        np.random.seed(seed)
        seeded["numpy"] = np.__version__
    except ImportError:  # pragma: no cover - numpy is a dependency
        seeded["numpy"] = None

    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():  # pragma: no cover - hardware dependent
            torch.cuda.manual_seed_all(seed)
        seeded["torch"] = torch.__version__
    except ImportError:
        seeded["torch"] = None

    return seeded


def new_experiment_id(prefix: str = "exp") -> str:
    """Return a timestamped experiment identifier.

    Args:
        prefix: Short experiment-family prefix.

    Returns:
        e.g. ``exp-20260919T044000Z``.
    """
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{stamp}"


def file_digest(path: Path | str) -> Optional[str]:
    """Return a SHA-256 digest of a file, for dataset and config versioning.

    Args:
        path: File to digest.

    Returns:
        Full hex digest, or ``None`` if the file does not exist.
    """
    resolved = Path(path)
    if not resolved.is_file():
        return None
    digest = hashlib.sha256()
    with resolved.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git(*args: str) -> Optional[str]:
    try:
        return subprocess.check_output(
            ["git", *args], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):  # pragma: no cover
        return None


@dataclass
class EnvironmentManifest:
    """A snapshot of everything needed to reproduce a run.

    Attributes:
        experiment_id: Identifier of the run.
        created_at: Capture time (UTC, ISO-8601).
        python_version: Interpreter version.
        platform: OS and architecture.
        git_commit: HEAD commit of the working tree.
        git_dirty: Whether the tree had uncommitted changes.
        rem_version: Version of this package.
        contract_digest: Digest of ``CLAUDE.md``, so a run records which
            frozen design it was produced under.
        seed: Seed used, if any.
        seeded_sources: What :func:`seed_everything` reported.
        config_files: Configuration files and their digests.
        dataset_files: Dataset files and their digests.
        dependencies: Installed distributions and versions.
        notes: Free-text annotations.
    """

    experiment_id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    python_version: str = field(default_factory=lambda: sys.version.split()[0])
    platform: str = field(default_factory=platform.platform)
    git_commit: Optional[str] = None
    git_dirty: Optional[bool] = None
    rem_version: Optional[str] = None
    contract_digest: Optional[str] = None
    seed: Optional[int] = None
    seeded_sources: Dict[str, Any] = field(default_factory=dict)
    config_files: Dict[str, Optional[str]] = field(default_factory=dict)
    dataset_files: Dict[str, Optional[str]] = field(default_factory=dict)
    dependencies: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    @classmethod
    def capture(
        cls,
        experiment_id: str,
        *,
        seed: Optional[int] = None,
        config_files: Optional[List[Path | str]] = None,
        dataset_files: Optional[List[Path | str]] = None,
        contract_path: Optional[Path | str] = None,
    ) -> "EnvironmentManifest":
        """Capture the current environment.

        Args:
            experiment_id: Identifier for the run.
            seed: Seed to apply and record.
            config_files: Configuration files to digest.
            dataset_files: Dataset files to digest.
            contract_path: Path to ``CLAUDE.md``; defaults to the repository root.

        Returns:
            The populated manifest.
        """
        from rem import __version__

        manifest = cls(experiment_id=experiment_id, rem_version=__version__)
        manifest.git_commit = _git("rev-parse", "HEAD")
        status = _git("status", "--porcelain")
        manifest.git_dirty = bool(status) if status is not None else None
        contract = Path(contract_path) if contract_path else _default_contract_path()
        manifest.contract_digest = file_digest(contract)
        if seed is not None:
            manifest.seed = seed
            manifest.seeded_sources = seed_everything(seed)
        manifest.config_files = {str(p): file_digest(p) for p in (config_files or [])}
        manifest.dataset_files = {str(p): file_digest(p) for p in (dataset_files or [])}
        manifest.dependencies = _installed_distributions()
        return manifest

    def to_json(self, indent: int = 2) -> str:
        """Serialise the manifest as JSON."""
        return json.dumps(asdict(self), indent=indent, sort_keys=True, default=str)

    def save(self, path: Path | str) -> Path:
        """Write the manifest to ``path``, creating parent directories."""
        resolved = Path(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(self.to_json(), encoding="utf-8")
        return resolved


def _default_contract_path() -> Path:
    return Path(__file__).resolve().parents[2] / "CLAUDE.md"


def _installed_distributions() -> Dict[str, str]:
    try:
        from importlib.metadata import distributions

        found: Dict[str, str] = {}
        for dist in distributions():
            name = dist.metadata["Name"]
            if name:
                found[name] = dist.version or ""
        return dict(sorted(found.items()))
    except Exception:  # pragma: no cover - defensive
        return {}
