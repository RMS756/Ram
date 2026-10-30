"""Layer 1 — provenance labelling and entity extraction (Chapter 3, Sec. 3.4).

Status: CHAPTER 3 SPECIFICATION, PENDING SD-FREEZE. The provenance rule is a
design definition stated in Chapter 3 Sec. 3.4.2; ``CLAUDE.md`` lists the
provenance labelling rule as not frozen. Nothing here is a default: the trust
order below *is* the Chapter 3 rule, and callers that do not accept it must not
use this module.

Chapter 3 Sec. 3.4.2:
    "Each context segment receives one label from the ordered set trusted
    (system prompt) > semi-trusted (user input) > untrusted (tool output,
    retrieved content, memory). Content derived from several segments inherits
    the least-trusted label among them, and processing never promotes content
    to a more trusted label."

Chapter 3 Sec. 3.4.1: invisible and formatting characters are removed from
untrusted text before further processing (deterministic hygiene).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Iterable, List, Sequence

from rem.agent.trajectory import Provenance

__all__ = [
    "TrustLevel",
    "trust_of",
    "least_trusted",
    "strip_invisible",
    "Segment",
    "value_occurs_in",
    "extract_ibans",
    "STATUS",
]

STATUS = "CHAPTER 3 SPECIFICATION (Sec. 3.4) — PENDING SD-FREEZE"


class TrustLevel(IntEnum):
    """Ordered trust labels. A larger value is more trusted."""

    UNTRUSTED = 0
    SEMI_TRUSTED = 1
    TRUSTED = 2


_CHANNEL_TRUST = {
    Provenance.SYSTEM: TrustLevel.TRUSTED,
    Provenance.USER: TrustLevel.SEMI_TRUSTED,
    Provenance.TOOL_OUTPUT: TrustLevel.UNTRUSTED,
}


def trust_of(provenance: Provenance) -> TrustLevel:
    """Map a source channel to its Chapter 3 trust label.

    Raises:
        ValueError: For ``UNLABELLED`` or ``MODEL`` content. Model-generated
            content is *derived* content and must be labelled by inheritance
            (``least_trusted``), never by channel.
    """
    try:
        return _CHANNEL_TRUST[provenance]
    except KeyError:
        raise ValueError(
            f"No channel trust for {provenance!r}: derived content inherits the "
            "least-trusted label of its inputs (Chapter 3 Sec. 3.4.2)."
        ) from None


def least_trusted(levels: Iterable[TrustLevel]) -> TrustLevel:
    """Least-trusted inheritance: derived content takes the minimum label.

    Raises:
        ValueError: If no input labels are supplied (derivation from nothing
            has no defined provenance).
    """
    collected = list(levels)
    if not collected:
        raise ValueError("Cannot derive a trust label from no inputs.")
    return TrustLevel(min(collected))


# Zero-width and bidirectional formatting characters, plus every Unicode
# "format" (Cf) code point, are removed. Ordinary whitespace is kept.
_INVISIBLE = re.compile("[​-‏‪-‮⁠-⁤⁦-⁩﻿]")


def strip_invisible(text: str) -> str:
    """Remove invisible and formatting characters (Chapter 3 Sec. 3.4.1).

    This reduces some encoding-based concealment; it does not prevent
    paraphrase-based evasion and is not claimed to.
    """
    text = _INVISIBLE.sub("", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


@dataclass(frozen=True)
class Segment:
    """One context segment with its provenance label.

    Attributes:
        text: Sanitised text (``strip_invisible`` applied for untrusted text).
        trust: Chapter 3 trust label.
        source: Channel detail, e.g. ``"system"``, ``"user"`` or a tool name.
        decision_point: Index of the agent decision point after which the
            segment entered the context (0 = before the first proposal).
    """

    text: str
    trust: TrustLevel
    source: str
    decision_point: int


_IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
_NUMBER = re.compile(r"(?<![\w.])-?\d+(?:[.,]\d+)?(?![\w])")


def extract_ibans(text: str) -> List[str]:
    """Return IBAN-formatted strings in ``text`` (Chapter 3 Sec. 3.4.3)."""
    return _IBAN.findall(text or "")


def _norm_text(value: str) -> str:
    return " ".join(str(value).lower().split())


def _numbers_in(text: str) -> List[float]:
    out: List[float] = []
    for token in _NUMBER.findall(text or ""):
        try:
            out.append(float(token.replace(",", "")))
        except ValueError:  # pragma: no cover - regex guarantees parseable
            continue
    return out


def value_occurs_in(value: Any, texts: Sequence[str]) -> bool:
    """Whether an argument value occurs in any of ``texts``.

    Matching rule (declared, Chapter 3 Sec. 3.4.3 "extraction patterns are
    declared in configuration"):

    * numbers (int/float, or strings that parse as numbers) match a numeric
      token of equal value;
    * other strings match as case-insensitive substrings after whitespace
      normalisation; strings shorter than 3 characters never match, so that
      trivial values cannot create provenance links.
    """
    if value is None or isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        target = float(value)
        return any(abs(n - target) < 1e-9 for t in texts for n in _numbers_in(t))
    text_value = str(value).strip()
    try:
        target = float(text_value.replace(",", ""))
        return any(abs(n - target) < 1e-9 for t in texts for n in _numbers_in(t))
    except ValueError:
        pass
    needle = _norm_text(text_value)
    if len(needle) < 3:
        return False
    return any(needle in _norm_text(t) for t in texts)
