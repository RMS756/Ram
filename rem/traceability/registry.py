"""Mathematical provenance and Equation-to-Source traceability.

Governed by ``CLAUDE.md`` § EQUATION-ID LOCK:

    Never fabricate an EQUATION_ID.
    If the authoritative registry is unavailable: STOP.
    Do not create provisional equation IDs inside implementation code.
    Do not make generated traceability reports appear complete by inventing
    identifiers.

Two distinct things are therefore kept apart:

* **Citation** — the academic source of a mathematical operation. Always
  recorded, because a source is a fact about the literature.
* **Equation ID** — a key into the authoritative Equation-to-Source Registry.
  Recorded only when that registry is supplied and contains the ID. Never
  synthesised.

An operation with a citation but no ID is ``AWAITING_REGISTRY_ID``. It is **not**
verified, and the generated traceability report says so rather than presenting a
complete chain.

This module contains no mathematics; it is bookkeeping.
"""

from __future__ import annotations

import functools
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, TypeVar

import yaml

__all__ = [
    "TraceStatus",
    "EquationRecord",
    "EquationRegistry",
    "RegistryUnavailableError",
    "UnregisteredEquationError",
    "RegisteredOperation",
    "derivation",
    "registered_operations",
    "load_registry",
    "registry_available",
    "REGISTRY_PATH_ENV",
]

F = TypeVar("F", bound=Callable[..., Any])

#: Environment variable naming the authoritative registry file. No default path
#: is used: a registry that is not explicitly supplied does not exist.
REGISTRY_PATH_ENV = "REM_EQUATION_REGISTRY"


class TraceStatus(str, Enum):
    """Traceability state of one mathematical operation.

    Members:
        VERIFIED: Carries an equation ID present in the authoritative registry.
        AWAITING_REGISTRY_ID: Carries a checkable citation but no registry ID,
            because the authoritative registry has not been supplied. Not
            verified, and must not be reported as such.
    """

    VERIFIED = "verified"
    AWAITING_REGISTRY_ID = "awaiting_registry_id"


class RegistryUnavailableError(RuntimeError):
    """Raised when code requires the registry and it has not been supplied."""


class UnregisteredEquationError(LookupError):
    """Raised when code claims an equation ID absent from the registry."""


@dataclass(frozen=True)
class EquationRecord:
    """One entry of the authoritative Equation-to-Source Registry."""

    equation_id: str
    name: str
    algorithm: str
    source: str
    location: str
    notes: str = ""

    def __post_init__(self) -> None:
        for attribute in ("equation_id", "name", "algorithm", "source", "location"):
            if not str(getattr(self, attribute)).strip():
                raise ValueError(
                    f"Registry entry {self.equation_id!r} has an empty {attribute!r}; "
                    "an equation with no source is not admissible."
                )


@dataclass
class EquationRegistry:
    """An in-memory authoritative Equation-to-Source Registry."""

    records: Dict[str, EquationRecord] = field(default_factory=dict)
    origin: str = "<none>"

    @classmethod
    def from_file(cls, path: Path) -> "EquationRegistry":
        """Load the authoritative registry from a YAML file.

        Args:
            path: Path to the registry supplied with the thesis design.

        Returns:
            The populated registry.

        Raises:
            RegistryUnavailableError: If the file is missing or malformed.
        """
        if not path.is_file():
            raise RegistryUnavailableError(
                f"Authoritative Equation-to-Source Registry not found at {path}. "
                f"Set {REGISTRY_PATH_ENV} to its location. REM does not ship a "
                "registry and will not synthesise one."
            )
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:  # pragma: no cover - defensive
            raise RegistryUnavailableError(f"Malformed registry at {path}: {exc}") from exc

        entries = raw.get("equations")
        if not isinstance(entries, list):
            raise RegistryUnavailableError(
                f"Registry at {path} must contain a top-level 'equations' list."
            )

        records: Dict[str, EquationRecord] = {}
        for entry in entries:
            if not isinstance(entry, dict):
                raise RegistryUnavailableError(
                    f"Registry at {path} contains a non-mapping equation entry."
                )
            record = EquationRecord(
                equation_id=str(entry.get("id", "")).strip(),
                name=str(entry.get("name", "")).strip(),
                algorithm=str(entry.get("algorithm", "")).strip(),
                source=str(entry.get("source", "")).strip(),
                location=str(entry.get("location", "")).strip(),
                notes=str(entry.get("notes", "") or "").strip(),
            )
            if record.equation_id in records:
                raise RegistryUnavailableError(
                    f"Duplicate equation ID {record.equation_id!r} in {path}."
                )
            records[record.equation_id] = record
        return cls(records=records, origin=str(path))

    def require(self, equation_id: str) -> EquationRecord:
        """Return the record for ``equation_id`` or raise."""
        try:
            return self.records[equation_id]
        except KeyError:
            raise UnregisteredEquationError(
                f"Equation ID {equation_id!r} is not present in the authoritative "
                f"registry ({self.origin}). Equation IDs may not be invented."
            ) from None

    def __contains__(self, equation_id: object) -> bool:
        return equation_id in self.records

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self) -> Iterator[EquationRecord]:
        return iter(self.records.values())


_registry: Optional[EquationRegistry] = None
_registry_checked = False


def load_registry(path: Optional[Path] = None, *, force: bool = False) -> EquationRegistry:
    """Load the authoritative registry.

    Args:
        path: Explicit path; defaults to ``$REM_EQUATION_REGISTRY``.
        force: Reload even if already cached.

    Returns:
        The registry.

    Raises:
        RegistryUnavailableError: If no path is configured or the file is absent.
    """
    global _registry, _registry_checked
    if _registry is not None and not force and path is None:
        return _registry
    configured = path or os.environ.get(REGISTRY_PATH_ENV)
    if not configured:
        _registry_checked = True
        raise RegistryUnavailableError(
            "No authoritative Equation-to-Source Registry is configured. "
            f"Set {REGISTRY_PATH_ENV} to its path. Per CLAUDE.md "
            "§ EQUATION-ID LOCK, REM will not create provisional identifiers."
        )
    _registry = EquationRegistry.from_file(Path(configured))
    _registry_checked = True
    return _registry


def registry_available() -> bool:
    """Whether an authoritative registry is configured and loadable."""
    try:
        load_registry()
    except RegistryUnavailableError:
        return False
    return True


@dataclass(frozen=True)
class RegisteredOperation:
    """A mathematical operation in the codebase, with its provenance.

    Attributes:
        qualified_name: Qualified name of the implementing callable.
        module: Module it lives in.
        statement: The formula, stated plainly.
        source: Full academic citation, or the frozen specification clause.
        location: Equation number / page / section within that source.
        algorithm: The method the operation belongs to.
        equation_id: Authoritative registry ID, or ``None`` when unavailable.
        status: See :class:`TraceStatus`.
        notes: Conventions and caveats.
    """

    qualified_name: str
    module: str
    statement: str
    source: str
    location: str
    algorithm: str
    equation_id: Optional[str]
    status: TraceStatus
    notes: str = ""


_operations: List[RegisteredOperation] = []


def registered_operations() -> List[RegisteredOperation]:
    """Return every ``@derivation``-decorated callable imported so far."""
    return list(_operations)


def derivation(
    *,
    statement: str,
    source: str,
    location: str,
    algorithm: str,
    equation_id: Optional[str] = None,
    notes: str = "",
) -> Callable[[F], F]:
    """Record the provenance of a mathematical operation.

    Args:
        statement: The formula, stated plainly (e.g. ``"p_t = sigmoid(g1*s + g0)"``).
        source: Full citation, or the frozen specification clause that fixes it.
        location: Equation number / page / section inside that source.
        algorithm: The method this operation belongs to.
        equation_id: Authoritative registry ID. Supply this **only** when the
            authoritative registry is available; it is validated against the
            registry and a missing registry is an error, never a reason to
            invent one.
        notes: Conventions, edge cases, caveats.

    Returns:
        The decorator.

    Raises:
        ValueError: If ``statement``, ``source``, ``location`` or ``algorithm``
            is empty — an undocumented mathematical operation is inadmissible.
        RegistryUnavailableError: If ``equation_id`` is given but no
            authoritative registry is configured.
        UnregisteredEquationError: If ``equation_id`` is not in the registry.
    """
    for name, value in (
        ("statement", statement),
        ("source", source),
        ("location", location),
        ("algorithm", algorithm),
    ):
        if not str(value).strip():
            raise ValueError(
                f"derivation() requires a non-empty {name!r}: a mathematical "
                "operation may not be implemented without stating what it "
                "computes and where it comes from."
            )

    def decorator(func: F) -> F:
        resolved_status = TraceStatus.AWAITING_REGISTRY_ID
        if equation_id is not None:
            # Raises if the registry is absent — never falls back to accepting
            # the identifier on trust.
            load_registry().require(equation_id)
            resolved_status = TraceStatus.VERIFIED

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        operation = RegisteredOperation(
            qualified_name=func.__qualname__,
            module=func.__module__,
            statement=statement.strip(),
            source=" ".join(source.split()),
            location=" ".join(location.split()),
            algorithm=algorithm.strip(),
            equation_id=equation_id,
            status=resolved_status,
            notes=" ".join(notes.split()),
        )
        wrapper.__derivation__ = operation  # type: ignore[attr-defined]
        _operations.append(operation)
        return wrapper  # type: ignore[return-value]

    return decorator
