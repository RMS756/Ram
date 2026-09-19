#!/usr/bin/env python3
"""Experiment runner.

Handles everything that does not depend on the unresolved design items: seeding,
experiment identity, environment capture (including the digest of ``CLAUDE.md``,
so a run records which frozen design produced it), configuration validation,
audit setup and readiness reporting.

It then refuses to run, because 19 design items remain UNVERIFIED. That refusal
is ``CLAUDE.md`` § IMPLEMENTATION FAIL-CLOSED REQUIREMENT working as intended:
a failed run is acceptable, an invented scientific decision is not.

Usage:
    python experiments/run_experiment.py --dry-run
    python experiments/run_experiment.py --seed 42
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from rem.config.loader import load_directory  # noqa: E402
from rem.core.audit import AuditLog  # noqa: E402
from rem.core.pipeline import AblationSpec, Layer, RemPipeline  # noqa: E402
from rem.utils.reproducibility import EnvironmentManifest, new_experiment_id  # noqa: E402


def build_pipeline(ablation: AblationSpec, audit_log: AuditLog) -> RemPipeline:
    """Construct the pipeline for a run.

    The frozen algorithms exist and could be attached here, but they cannot be
    *configured*: the feature set, ridge penalty, consequence tiers and loss grid
    are unresolved. Attaching them with invented parameters is exactly what the
    contract forbids, so the slots stay empty until the design supplies them.

    Args:
        ablation: Which elements to disable.
        audit_log: Destination for audit records.

    Returns:
        The pipeline, with unfilled slots.
    """
    return RemPipeline(audit_log=audit_log, ablation=ablation)


def ablations() -> List[AblationSpec]:
    """The ablation configurations over the frozen architecture.

    Note that ``REM - Calibration`` is absent: the expected-loss Bayes verdict is
    defined on the calibrated probability, so removing calibration does not
    ablate the frozen design, it replaces it. The pipeline refuses that
    combination rather than silently substituting ``p_tilde``.
    """
    return [
        AblationSpec.full(),
        AblationSpec.without(Layer.CONTEXT),
        AblationSpec.without(Layer.BEHAVIOR),
        AblationSpec.without(Layer.ATTRIBUTION),
        AblationSpec.without(Layer.MITIGATION),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=REPO_ROOT / "configs")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "experiments" / "results")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--experiment-id", type=str, default=None)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate configuration and report readiness without running",
    )
    args = parser.parse_args()

    experiment_id = args.experiment_id or new_experiment_id()
    print(f"Experiment: {experiment_id}")

    configs = load_directory(args.config_dir)
    print(f"Loaded {len(configs)} configuration file(s) from {args.config_dir}")

    seed = args.seed
    if seed is None:
        try:
            seed = configs["experiment"]["experiment"].value("random_seed")
        except Exception:
            seed = None

    unresolved = [p for config in configs.values() for p in config.unresolved()]
    frozen = [
        p
        for config in configs.values()
        for section in config.values()
        for p in section.values()
        if p.status == "FROZEN"
    ]

    manifest = EnvironmentManifest.capture(
        experiment_id,
        seed=seed,
        config_files=sorted(args.config_dir.glob("*.yaml")),
    )
    output_dir = args.output_dir / experiment_id
    manifest.save(output_dir / "manifest.json")
    print(f"Environment manifest: {output_dir / 'manifest.json'}")
    print(f"Frozen design digest (CLAUDE.md): {manifest.contract_digest}")

    audit_log = AuditLog(
        output_dir / "audit.jsonl",
        experiment_id=experiment_id,
        versions={"rem": manifest.rem_version, "git": manifest.git_commit},
    )
    pipeline = build_pipeline(AblationSpec.full(), audit_log)
    missing = pipeline.missing_components()

    readiness = {
        "experiment_id": experiment_id,
        "seed": seed,
        "contract_digest": manifest.contract_digest,
        "frozen_parameters": len(frozen),
        "unresolved_parameters": [
            {"name": p.name, "status": p.status, "meaning": " ".join(p.meaning.split())}
            for p in unresolved
        ],
        "unattached_components": missing,
        "planned_ablations": [spec.label for spec in ablations()],
        "ready": not unresolved and not missing,
    }
    (output_dir / "readiness.json").write_text(
        json.dumps(readiness, indent=2), encoding="utf-8"
    )

    print(f"\nFROZEN parameters:      {len(frozen)}")
    print(f"UNVERIFIED parameters:  {len(unresolved)}")
    for parameter in unresolved:
        print(f"  - {parameter.name}: {' '.join(parameter.meaning.split())[:80]}")
    print(f"\nUnattached components:  {len(missing)}")
    for name in missing:
        print(f"  - {name}")

    if readiness["ready"]:
        print("\nConfiguration is complete. Attach algorithms in build_pipeline() to run.")
        return 0

    if args.dry_run:
        print(f"\nDry run complete. Readiness report: {output_dir / 'readiness.json'}")
        return 0

    print(
        "\n## DESIGN BLOCKED\n"
        f"**Item:** {len(unresolved)} unresolved design parameters\n"
        "**Why required:** REM cannot produce a verdict without the loss grid, "
        "consequence tiers, feature set and ridge penalty.\n"
        "**Current source status:** listed as unresolved in CLAUDE.md "
        "DATA / EVALUATION LOCK; Stage 2 report not supplied.\n"
        "**Safe action:** STOP — do not choose values.\n"
        "**Supervisor decision needed:** YES\n"
        "See RECONCILIATION.md.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
