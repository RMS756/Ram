"""Configuration loading with mandatory provenance.

Implements the rule that no experimentally variable parameter may be buried in
source code, and that every parameter declares:

    value | meaning | default | source | justification

A parameter whose ``value`` or ``source`` is ``REQUIRED_FROM_DESIGN`` is
*declared but unresolved*: reading it raises
:class:`UnspecifiedParameterError`. This is the configuration-layer form of
``CLAUDE.md`` § IMPLEMENTATION FAIL-CLOSED REQUIREMENT — a missing design input
must fail loudly rather than become a guessed default.

This module contains no mathematics.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping

import yaml

__all__ = [
    "REQUIRED",
    "Parameter",
    "ConfigSection",
    "RemConfig",
    "UnspecifiedParameterError",
    "MalformedParameterError",
    "load_config",
    "load_directory",
]

#: Sentinel marking a value or citation that must come from the design and has
#: not been supplied.
REQUIRED = "REQUIRED_FROM_DESIGN"

_REQUIRED_FIELDS = ("meaning", "source", "justification")


class UnspecifiedParameterError(RuntimeError):
    """Raised when code reads a parameter still awaiting a design decision."""


class MalformedParameterError(ValueError):
    """Raised when a parameter declaration is missing provenance fields."""


@dataclass(frozen=True)
class Parameter:
    """A configurable parameter and its provenance.

    Attributes:
        name: Dotted parameter name.
        value: The configured value, or :data:`REQUIRED` if unresolved.
        meaning: What the parameter controls, in one sentence.
        default: Value used when unset, or ``None`` if there is no safe default.
        source: Citation justifying the value or the procedure selecting it.
        justification: Why this value/procedure is defensible.
        status: Design status — ``FROZEN``, ``PD``, ``UNVERIFIED`` or
            ``CONFLICT``, matching the reconciliation vocabulary.
        experimental: ``True`` when selected experimentally rather than fixed by
            literature (the ``[EXPERIMENTAL]`` tag).
    """

    name: str
    value: Any
    meaning: str
    default: Any
    source: str
    justification: str
    status: str = "UNVERIFIED"
    experimental: bool = False

    @property
    def is_resolved(self) -> bool:
        """Whether the parameter has both a concrete value and a citation."""
        return self.value != REQUIRED and self.source != REQUIRED

    def resolve(self) -> Any:
        """Return the value, or raise if it is still unresolved.

        Raises:
            UnspecifiedParameterError: If value or source is still the sentinel.
        """
        if self.value == REQUIRED:
            raise UnspecifiedParameterError(
                f"\n## DESIGN BLOCKED\n"
                f"**Item:** {self.name}\n"
                f"**Why required:** {self.meaning}\n"
                f"**Current source status:** not frozen ({self.status}).\n"
                f"**Safe action:** STOP — do not choose a value.\n"
                f"**Supervisor decision needed:** YES\n"
                f"See RECONCILIATION.md."
            )
        if self.source == REQUIRED:
            raise UnspecifiedParameterError(
                f"Parameter {self.name!r} has a value ({self.value!r}) but no "
                "academic or specification source. An unsourced parameter is "
                "not admissible."
            )
        return self.value


class ConfigSection(Mapping[str, Parameter]):
    """An immutable, named group of parameters."""

    def __init__(self, name: str, parameters: Dict[str, Parameter]) -> None:
        self._name = name
        self._parameters = dict(parameters)

    @property
    def name(self) -> str:
        return self._name

    def __getitem__(self, key: str) -> Parameter:
        try:
            return self._parameters[key]
        except KeyError:
            raise KeyError(
                f"No parameter {key!r} declared in section {self._name!r}. "
                "Parameters must be declared in configs/, not introduced in code."
            ) from None

    def __iter__(self) -> Iterator[str]:
        return iter(self._parameters)

    def __len__(self) -> int:
        return len(self._parameters)

    def value(self, key: str) -> Any:
        """Return the resolved value of ``key``."""
        return self[key].resolve()

    def unresolved(self) -> List[Parameter]:
        """Return parameters still awaiting a design decision."""
        return [p for p in self._parameters.values() if not p.is_resolved]


class RemConfig(Mapping[str, ConfigSection]):
    """A full REM configuration, composed of named sections."""

    def __init__(self, sections: Dict[str, ConfigSection], origin: str) -> None:
        self._sections = dict(sections)
        self._origin = origin

    @property
    def origin(self) -> str:
        """Path the configuration was loaded from."""
        return self._origin

    def __getitem__(self, key: str) -> ConfigSection:
        try:
            return self._sections[key]
        except KeyError:
            raise KeyError(
                f"No configuration section {key!r} in {self._origin}. "
                f"Available: {sorted(self._sections)}"
            ) from None

    def __iter__(self) -> Iterator[str]:
        return iter(self._sections)

    def __len__(self) -> int:
        return len(self._sections)

    def unresolved(self) -> List[Parameter]:
        """Return every unresolved parameter across all sections."""
        found: List[Parameter] = []
        for section in self._sections.values():
            found.extend(section.unresolved())
        return found

    def require_fully_resolved(self) -> None:
        """Raise unless every declared parameter is resolved.

        Raises:
            UnspecifiedParameterError: Listing every unresolved parameter.
        """
        missing = self.unresolved()
        if missing:
            listing = "\n".join(f"  - {p.name} [{p.status}]: {p.meaning}" for p in missing)
            raise UnspecifiedParameterError(
                f"{len(missing)} parameter(s) in {self._origin} are still "
                f"awaiting a frozen design decision:\n{listing}"
            )


def _parse_parameter(section: str, key: str, raw: Any) -> Parameter:
    if not isinstance(raw, dict):
        raise MalformedParameterError(
            f"{section}.{key} must be a mapping declaring "
            f"{', '.join(_REQUIRED_FIELDS)}; got {type(raw).__name__}."
        )
    missing = [f for f in _REQUIRED_FIELDS if f not in raw]
    if missing:
        raise MalformedParameterError(
            f"{section}.{key} is missing required provenance field(s): "
            f"{', '.join(missing)}."
        )
    if "value" not in raw:
        raise MalformedParameterError(f"{section}.{key} declares no 'value'.")
    return Parameter(
        name=f"{section}.{key}",
        value=raw["value"],
        meaning=str(raw["meaning"]),
        default=raw.get("default"),
        source=str(raw["source"]),
        justification=str(raw["justification"]),
        status=str(raw.get("status", "UNVERIFIED")).upper(),
        experimental=bool(raw.get("experimental", False)),
    )


def load_config(path: Path | str) -> RemConfig:
    """Load and validate a REM configuration file.

    Args:
        path: Path to a YAML configuration file.

    Returns:
        The parsed configuration.

    Raises:
        FileNotFoundError: If the file does not exist.
        MalformedParameterError: If any parameter lacks provenance fields.
    """
    resolved = Path(path)
    if not resolved.is_file():
        raise FileNotFoundError(f"Configuration file not found: {resolved}")
    raw = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise MalformedParameterError(f"{resolved} must contain a mapping at top level.")

    sections: Dict[str, ConfigSection] = {}
    for section_name, body in raw.items():
        if section_name.startswith("_"):
            continue
        if not isinstance(body, dict):
            raise MalformedParameterError(
                f"Section {section_name!r} in {resolved} must be a mapping."
            )
        parameters = {
            key: _parse_parameter(section_name, key, value) for key, value in body.items()
        }
        sections[section_name] = ConfigSection(section_name, parameters)
    return RemConfig(sections, origin=str(resolved))


def load_directory(directory: Path | str) -> Dict[str, RemConfig]:
    """Load every ``*.yaml`` configuration in a directory.

    Args:
        directory: Directory containing configuration files.

    Returns:
        Mapping from file stem to parsed configuration.
    """
    base = Path(directory)
    return {p.stem: load_config(p) for p in sorted(base.glob("*.yaml"))}
