#!/usr/bin/env python3
"""Generate docs/MATHEMATICAL_TRACEABILITY.md from the code itself.

Importing the REM package registers every ``@derivation``-decorated callable, so
the document is derived from the implementation and cannot drift.

Governed by ``CLAUDE.md`` § EQUATION-ID LOCK, which forbids making a generated
traceability report *appear complete* by inventing identifiers. While the
authoritative Equation-to-Source Registry is absent, this script therefore
reports ``AUTHORITATIVE EQUATION IDs: 0`` and marks every operation
``AWAITING REGISTRY ID``. It never synthesises an ID and never claims a
complete chain.

Exit codes:
    0  Every operation carries a citation.
    1  At least one operation lacks a source, or the document is stale
       (``--check``).

Usage:
    python scripts/generate_traceability.py [--check]
"""

from __future__ import annotations

import argparse
import importlib
import pkgutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from rem.traceability.registry import (  # noqa: E402
    RegisteredOperation,
    TraceStatus,
    registered_operations,
    registry_available,
)

OUTPUT = REPO_ROOT / "docs" / "MATHEMATICAL_TRACEABILITY.md"


def import_all_modules() -> None:
    """Import every module under ``rem`` so all decorators execute."""
    import rem

    for info in pkgutil.walk_packages(rem.__path__, prefix="rem."):
        importlib.import_module(info.name)


def build_document(operations: List[RegisteredOperation]) -> str:
    have_registry = registry_available()
    unsourced = [op for op in operations if not op.source.strip()]
    verified = [op for op in operations if op.status is TraceStatus.VERIFIED]
    awaiting = [op for op in operations if op.status is TraceStatus.AWAITING_REGISTRY_ID]

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: List[str] = [
        "# MATHEMATICAL_TRACEABILITY",
        "",
        "> **Generated file — do not edit by hand.**",
        "> Produced by `scripts/generate_traceability.py` by importing the `rem`",
        "> package and collecting every `@derivation`-decorated callable.",
        "",
        f"Generated: {generated}",
        "",
        "## Registry status",
        "",
    ]

    if have_registry:
        lines += [
            "The authoritative Equation-to-Source Registry **is** configured.",
            "Operations carrying an ID below have been validated against it.",
        ]
    else:
        lines += [
            "**The authoritative Equation-to-Source Registry has NOT been supplied.**",
            "",
            "Per `CLAUDE.md` § EQUATION-ID LOCK, no provisional identifiers have been",
            "created. Every operation below therefore carries a *citation* but no",
            "*equation ID*, and is marked `AWAITING REGISTRY ID`. This report does",
            "**not** represent a complete traceability chain, and must not be read as",
            "one. Supplying the registry and re-running this script is what closes it.",
        ]

    lines += [
        "",
        "## Operations",
        "",
        "| Code Component | Function | Algorithm | Statement | Equation ID | Source | Location | Status |",
        "| -------------- | -------- | --------- | --------- | ----------- | ------ | -------- | ------ |",
    ]

    for op in sorted(operations, key=lambda o: (o.module, o.qualified_name)):
        equation_id = f"`{op.equation_id}`" if op.equation_id else "*not assigned*"
        status = (
            "VERIFIED"
            if op.status is TraceStatus.VERIFIED
            else "**AWAITING REGISTRY ID**"
        )
        if not op.source.strip():
            status = "**UNSOURCED**"
        lines.append(
            f"| `{op.module}` | `{op.qualified_name}` | {_clean(op.algorithm)} | "
            f"`{_clean(op.statement)}` | {equation_id} | {_clean(op.source)} | "
            f"{_clean(op.location)} | {status} |"
        )

    lines += [
        "",
        "## Counts",
        "",
        "```text",
        f"TOTAL MATHEMATICAL OPERATIONS   {len(operations)}",
        f"CITED (source recorded)         {len(operations) - len(unsourced)}",
        f"UNSOURCED                       {len(unsourced)}",
        f"AUTHORITATIVE EQUATION IDs      {len(verified)}",
        f"AWAITING REGISTRY ID            {len(awaiting)}",
        "```",
        "",
    ]

    if awaiting:
        lines += [
            f"{len(awaiting)} operation(s) are cited but carry no authoritative",
            "equation ID. The traceability chain",
            "`Literature -> Requirement -> Algorithm -> Equation -> Code -> Test`",
            "is therefore **open at the Equation link** and cannot be closed until the",
            "authoritative registry is supplied.",
            "",
        ]

    if unsourced:
        lines += [
            "## UNSOURCED MATHEMATICAL OPERATIONS",
            "",
            "The following operations have no citation and must be resolved:",
            "",
        ]
        lines += [f"- `{op.module}.{op.qualified_name}`" for op in unsourced]
        lines.append("")

    return "\n".join(lines)


def _clean(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def _strip_timestamp(text: str) -> str:
    return "\n".join(l for l in text.splitlines() if not l.startswith("Generated:"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed document is current instead of rewriting it",
    )
    args = parser.parse_args()

    import_all_modules()
    operations = registered_operations()
    document = build_document(operations)
    unsourced = [op for op in operations if not op.source.strip()]
    awaiting = [op for op in operations if op.status is TraceStatus.AWAITING_REGISTRY_ID]

    if args.check:
        if not OUTPUT.is_file():
            print(f"{OUTPUT} does not exist; run without --check to generate it.")
            return 1
        current = OUTPUT.read_text(encoding="utf-8")
        if _strip_timestamp(current) != _strip_timestamp(document):
            print(f"{OUTPUT} is out of date; regenerate it.")
            return 1
        print(f"{OUTPUT} is current.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(document, encoding="utf-8")
        print(f"Wrote {OUTPUT} ({len(operations)} operations).")

    if unsourced:
        print(f"UNSOURCED MATHEMATICAL OPERATIONS: {len(unsourced)}", file=sys.stderr)
        for op in unsourced:
            print(f"  - {op.module}.{op.qualified_name}", file=sys.stderr)
        return 1

    print(f"UNSOURCED MATHEMATICAL OPERATIONS: 0")
    print(f"AWAITING REGISTRY ID: {len(awaiting)} (registry not supplied)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
