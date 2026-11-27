"""L1: field-level provenance segments and value lineage for financial tool arguments.

Design sources (inspiration, not copies):
  * CaMeL (Debenedetti et al.; repository f083b6b): values carry sources; a state-changing call is checked against the
    sources of its arguments. CaMeL tracks dependencies *inside its own interpreter*; REM cannot, because the agent
    is a black box. REM-DiD therefore INFERS lineage by matching canonical values against labelled context segments.
  * RTBAS (Zhong et al., 2025; abstract level): labels on tool outputs; dependency screening.
  * PACT / ROPE (abstract / repository level): origin of authority-bearing arguments.

What this module does NOT do (stated limitation):
  It does not observe the agent's internal data flow. Lineage is evidence of co-occurrence of a canonical value with
  a labelled source, not proof of derivation. A value computed by the agent (e.g. a difference of two amounts) has
  no matching source and is reported MISSING (derived/unknown), never TRUSTED. Trust is about origin, not truth.
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, Iterable, List, Mapping, Optional, Tuple

import yaml

from .canonical import canonical_amount, canonical_iban, canonical_text, find_amounts, find_ibans


class Source(str, enum.Enum):
    AUTH_USER = "authenticated_user_instruction"
    SYSTEM_CONFIG = "authenticated_system_configuration"
    TRUSTED_FINANCIAL = "trusted_financial_system_field"
    TAE = "trusted_authorization_envelope"
    EXTERNAL_DOCUMENT = "external_document"
    EXTERNAL_EMBEDDED = "free_text_field_in_financial_record"
    TOOL_UNPARSED = "tool_output_unparsed"


TRUSTED: FrozenSet[Source] = frozenset({Source.AUTH_USER, Source.SYSTEM_CONFIG, Source.TRUSTED_FINANCIAL, Source.TAE})
UNTRUSTED: FrozenSet[Source] = frozenset({Source.EXTERNAL_DOCUMENT, Source.EXTERNAL_EMBEDDED, Source.TOOL_UNPARSED})

# Tool-output field policy for the AgentDojo banking API (declared; see 41_DATA_PROVENANCE_AND_LINEAGE_SPEC.md).
FREE_TEXT_FIELDS = frozenset({"subject"})
IBAN_FIELDS = frozenset({"recipient", "sender", "iban"})
AMOUNT_FIELDS = frozenset({"amount", "balance"})           # attacker-writable inside authentic financial records
DOCUMENT_TOOLS = frozenset({"read_file"})           # third-party document content


class LineageStatus(str, enum.Enum):
    TRUSTED = "trusted_only"
    UNTRUSTED = "untrusted_only"
    MIXED = "trusted_and_untrusted"
    MISSING = "no_matching_source"          # derived, computed, or absent: never upgraded to trusted
    UNPARSEABLE = "unparseable_value"


@dataclass(frozen=True)
class Segment:
    text: str
    source: Source
    tool: Optional[str]
    field: Optional[str]
    step: int
    ibans: Tuple[str, ...] = ()
    amounts: Tuple[Any, ...] = ()
    ids: Tuple[int, ...] = ()

    @staticmethod
    def make(text: str, source: Source, tool=None, field_=None, step=0, ids=(), structured=False) -> "Segment":
        """Free text: every IBAN and number is extracted. Structured trusted fields: only from typed fields
        (IBAN fields, amount fields), so that dates and ids never become amount or account evidence."""
        if structured:
            ib = tuple(find_ibans(text)) if (field_ in IBAN_FIELDS or tool == "get_iban") else ()
            am = tuple(find_amounts(text)) if (field_ in AMOUNT_FIELDS or tool == "get_balance") else ()
        else:
            ib, am = tuple(find_ibans(text)), tuple(find_amounts(text))
        return Segment(text=text, source=source, tool=tool, field=field_, step=step, ibans=ib, amounts=am, ids=tuple(ids))


@dataclass(frozen=True)
class Lineage:
    field: str
    kind: str
    canonical: Any
    sources: FrozenSet[Source]
    transformations: FrozenSet[str]
    segments: Tuple[int, ...]
    status: LineageStatus

    @property
    def untrusted(self) -> bool:
        return self.status in (LineageStatus.UNTRUSTED,)


def _walk(obj: Any, tool: str, step: int, path: str = "") -> Iterable[Segment]:
    if isinstance(obj, Mapping):
        ids = (int(obj["id"]),) if isinstance(obj.get("id"), int) and not isinstance(obj.get("id"), bool) else ()
        for k, v in obj.items():
            yield from _walk(v, tool, step, str(k))
        if ids:
            yield Segment.make("", Source.TRUSTED_FINANCIAL, tool, "id", step, ids=ids)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v, tool, step, path)
    else:
        if obj is None:
            return
        if path in FREE_TEXT_FIELDS:
            yield Segment.make(str(obj), Source.EXTERNAL_EMBEDDED, tool, path, step)
        else:
            yield Segment.make(str(obj), Source.TRUSTED_FINANCIAL, tool, path or None, step, structured=True)


def segments_from_tool_output(tool: str, text: str, step: int) -> List[Segment]:
    """Label one tool result. Document tools -> external document; structured banking records -> trusted fields
    except free-text fields; anything that cannot be parsed -> TOOL_UNPARSED (untrusted)."""
    if not text:
        return []
    if tool in DOCUMENT_TOOLS:
        return [Segment.make(text, Source.EXTERNAL_DOCUMENT, tool, None, step)]
    try:
        obj = yaml.safe_load(text)
    except Exception:
        return [Segment.make(text, Source.TOOL_UNPARSED, tool, None, step)]
    if isinstance(obj, (dict, list)):
        return list(_walk(obj, tool, step))
    if isinstance(obj, (int, float, str)):
        return [Segment.make(str(obj), Source.TRUSTED_FINANCIAL, tool, None, step, structured=True)]
    return [Segment.make(text, Source.TOOL_UNPARSED, tool, None, step)]


SENSITIVE_FIELDS: Dict[str, Tuple[Tuple[str, str], ...]] = {
    "send_money": (("recipient", "iban"), ("amount", "amount")),
    "schedule_transaction": (("recipient", "iban"), ("amount", "amount")),
    "update_scheduled_transaction": (("id", "id"), ("recipient", "iban"), ("amount", "amount")),
    "update_password": (("password", "text"),),
    "update_user_info": (("first_name", "text"), ("last_name", "text"), ("street", "text"), ("city", "text")),
}
IDENTITY_KINDS = frozenset({"iban", "text", "id"})   # who/what is affected; amounts are handled separately
STATE_CHANGING = frozenset(SENSITIVE_FIELDS)


def canonical_of(kind: str, value: Any) -> Any:
    if kind == "iban":
        return canonical_iban(value)
    if kind == "amount":
        return canonical_amount(value)
    if kind == "text":
        c = canonical_text(value)
        return c if c and len(c) >= 3 else None
    if kind == "id":
        try:
            return int(value)
        except Exception:
            return None
    return value


class ProvenanceStore:
    """All labelled segments of one episode (L1 state)."""

    def __init__(self, user_prompt: str, system_prompt: str = "") -> None:
        self.segments: List[Segment] = []
        self.step = 0
        if system_prompt:
            self.segments.append(Segment.make(system_prompt, Source.SYSTEM_CONFIG, None, None, 0))
        self.segments.append(Segment.make(user_prompt, Source.AUTH_USER, None, None, 0))
        self.scheduled: Dict[int, Dict[str, Any]] = {}

    def add_tool_output(self, tool: str, text: str) -> List[Segment]:
        self.step += 1
        segs = segments_from_tool_output(tool, text, self.step)
        self.segments.extend(segs)
        if tool == "get_scheduled_transactions":
            try:
                for t in yaml.safe_load(text) or []:
                    if isinstance(t, dict) and isinstance(t.get("id"), int):
                        self.scheduled[t["id"]] = {"recipient": canonical_iban(t.get("recipient")),
                                                   "amount": canonical_amount(t.get("amount"))}
            except Exception:
                pass
        return segs

    def untrusted_segments(self) -> List[Tuple[int, Segment]]:
        return [(i, s) for i, s in enumerate(self.segments) if s.source in UNTRUSTED]

    def lineage(self, field_: str, kind: str, value: Any, extra_trusted: Iterable[Segment] = ()) -> Lineage:
        c = canonical_of(kind, value)
        if c is None:
            return Lineage(field_, kind, None, frozenset(), frozenset(), (), LineageStatus.UNPARSEABLE)
        srcs, trans, idx = set(), set(), []
        raw = str(value)
        for i, s in enumerate(list(self.segments) + list(extra_trusted)):
            hit = False
            if kind == "iban":
                hit = c in s.ibans
            elif kind == "amount":
                hit = any(a == c for a in s.amounts)
            elif kind == "id":
                hit = c in s.ids
            elif kind == "text":
                st = canonical_text(s.text) or ""
                hit = bool(c) and c in st
            if hit:
                srcs.add(s.source)
                idx.append(i)
                trans.add("verbatim" if raw and raw in s.text else "canonicalized")
        if not srcs:
            status = LineageStatus.MISSING
        elif srcs <= TRUSTED:
            status = LineageStatus.TRUSTED
        elif srcs <= UNTRUSTED:
            status = LineageStatus.UNTRUSTED
        else:
            status = LineageStatus.MIXED
        return Lineage(field_, kind, c, frozenset(srcs), frozenset(trans), tuple(idx), status)

    def call_lineage(self, tool: str, args: Mapping[str, Any], extra_trusted: Iterable[Segment] = ()) -> Dict[str, Lineage]:
        out = {}
        for f, kind in SENSITIVE_FIELDS.get(tool, ()):
            if f in args and args[f] is not None:
                out[f] = self.lineage(f, kind, args[f], extra_trusted)
        return out
