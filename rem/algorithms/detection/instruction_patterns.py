"""Layer 2 — instruction-pattern indicator x^ctx_2 (Chapter 3, Table 3.8).

Status: CHAPTER 3 SPECIFICATION, PENDING SD-FREEZE. Chapter 3 defines the
feature; the pattern set itself is "declared before evaluation" and is supplied
by the caller (the exploratory pilot declares it in
``configs/exploratory/pilot_e0.yaml``). There is no default pattern set.

x^ctx_1 (the fixed pre-trained injection classifier) is NOT implemented: the
classifier is pending supervisor approval (SD-DET) and the candidate model host
is unreachable from this environment.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Optional, Sequence

__all__ = ["InstructionPatternDetector"]


class InstructionPatternDetector:
    """Binary indicator over untrusted text.

    Args:
        patterns: Regular expressions declared before evaluation.
        tool_names: If given, a mention of any tool name (as a whole word)
            also counts as a match (Chapter 3 Sec. 3.5: "references to tool
            names").

    Raises:
        ValueError: If no pattern and no tool name is supplied — an empty
            pattern set would make the feature identically zero without saying so.
    """

    name = "instruction_pattern_indicator"

    def __init__(self, patterns: Sequence[str], tool_names: Optional[Sequence[str]] = None) -> None:
        if not patterns and not tool_names:
            raise ValueError("A declared instruction-pattern set is required (Chapter 3 Sec. 3.5).")
        self._patterns = [re.compile(p) for p in patterns]
        self._tools = (
            re.compile(r"\b(" + "|".join(re.escape(t) for t in tool_names) + r")\b")
            if tool_names
            else None
        )

    def fired(self, text: str) -> List[str]:
        """Return the identifiers of the patterns that match ``text``."""
        hits = [f"p{i}" for i, p in enumerate(self._patterns) if p.search(text or "")]
        if self._tools is not None and self._tools.search(text or ""):
            hits.append("tool_name")
        return hits

    def matches(self, text: str) -> bool:
        """Whether any declared pattern matches ``text``."""
        return bool(self.fired(text))

    def any_match(self, texts: Iterable[str]) -> int:
        """x^ctx_2: 1 if any of ``texts`` matches, else 0."""
        return int(any(self.matches(t) for t in texts))
