"""Task-permission compiler (candidate component A) — isolated improvement study.

Status: [PROPOSED — NOT PART OF THE APPROVED REM DESIGN]. Deterministic; no model call; no fitted quantity.

``compile_intent(objective)`` derives an immutable, schema-level representation of what the trusted
user-role request asks for. It reads ONLY the request text. It never receives tool outputs, task
identifiers, reference solutions, labels or outcomes (see tests/test_improve_study.py, label isolation).

The result is FALLIBLE INFERRED EVIDENCE about the request. It is not authenticated transaction
authorization. Every rule below is an engineering design choice of this study, not a published formula.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Dict, FrozenSet, List, Optional, Tuple

CATEGORIES = ("value_transfer", "payment_modification", "credential_change", "profile_change")
IBAN_RE = re.compile(r"(?<![A-Za-z0-9])([A-Z]{2}\d{2}(?:[ \-]?[A-Z0-9]){10,30})(?![A-Za-z0-9])")
_INVISIBLE = {"Cf", "Cc"}


def clean(text: str) -> str:
    return "".join(ch for ch in (text or "") if unicodedata.category(ch) not in _INVISIBLE or ch in "\n\t")


def canon_iban(value) -> Optional[str]:
    """Type-specific canonical form of an account identifier: separators removed, upper case.
    Returns None if the value is not shaped like an account identifier. Distinct identifiers are never
    equated by similarity."""
    if not isinstance(value, str):
        return None
    c = re.sub(r"[ \-]", "", value.strip()).upper()
    return c if re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{10,30}", c) else None


def parse_amount(token: str) -> Tuple[Optional[Decimal], bool]:
    """Exact decimal value of a numeric token and whether its format is ambiguous.

    Both separators present: the last one is the decimal separator. A single separator followed by
    exactly three digits (``1,150`` or ``1.150``) is ambiguous between grouping and decimals and is
    returned as (None, True). A comma followed by one or two digits is a decimal comma."""
    t = re.sub(r"[\s$€£]", "", token)
    if not re.fullmatch(r"\d[\d.,]*", t) or t[-1] in ".,":
        return None, False
    has_c, has_d = "," in t, "." in t
    try:
        if has_c and has_d:
            dec = "," if t.rfind(",") > t.rfind(".") else "."
            grp = "." if dec == "," else ","
            body, frac = t.rsplit(dec, 1)
            if not all(len(g) == 3 for g in body.split(grp)[1:]) or not frac.isdigit():
                return None, True
            return Decimal(body.replace(grp, "") + "." + frac), False
        if has_c or has_d:
            sep = "," if has_c else "."
            parts = t.split(sep)
            if len(parts) > 2:                                # 1,234,567 -> grouping only
                return (Decimal("".join(parts)), False) if all(len(p) == 3 for p in parts[1:]) else (None, True)
            if len(parts[1]) == 3 and 1 <= len(parts[0]) <= 3:
                return None, True                              # 1,150 / 1.150: ambiguous
            return Decimal(parts[0] + "." + parts[1]), False
        return Decimal(t), False
    except InvalidOperation:
        return None, False


def amount_of(value) -> Optional[Decimal]:
    """Exact decimal of a call argument (numbers and unambiguous numeric strings)."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return Decimal(repr(float(value))).quantize(Decimal("0.01")) if float(value) == round(float(value), 2) else Decimal(repr(float(value)))
    if isinstance(value, str):
        d, amb = parse_amount(value)
        return None if amb or d is None else d
    return None


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    text: str


@dataclass(frozen=True)
class IbanMention:
    raw: str
    canonical: str
    role: str          # 'target' | 'historical' | 'mentioned'
    span: Span


@dataclass(frozen=True)
class AmountMention:
    value: Optional[Decimal]
    ambiguous: bool
    role: str          # 'value' | 'base' (input to a requested computation) | 'historical'
    span: Span


@dataclass(frozen=True)
class Intent:
    """Immutable permission evidence compiled from the trusted request."""
    ops: Tuple[Tuple[str, str], ...]                 # (category, 'requested' | 'prohibited' | 'absent')
    conditional: FrozenSet[str]                      # requested only under a stated condition
    op_spans: Tuple[Tuple[str, Span], ...]
    ibans: Tuple[IbanMention, ...]
    amounts: Tuple[AmountMention, ...]
    amount_modes: FrozenSet[str]                     # subset of {'derived', 'history', 'delegated'}
    party_reference: bool                            # the request refers to a party without restating its identifier
    sources: Tuple[str, ...]                         # sources named by the user (e.g. file names)
    secret_digests: Tuple[str, ...]                  # sha256 of quoted credential values; raw values are not kept
    content_words: FrozenSet[str]
    read_only: bool
    open_delegation: bool                            # "follow the instructions" without naming an operation

    def op(self, category: str) -> str:
        return dict(self.ops).get(category, "absent")


# ------------------------------------------------------------------ lexicon (design choices)
_REQ = {
    "value_transfer": [r"\b(pay|send|transfer|refund|wire|remit|reimburse|repay)\b",
                       r"\bset\s+up\b[^.;]*\b(transactions?|payments?|transfers?|standing orders?)\b",
                       r"\bschedule\b[^.;]*\b(transactions?|payments?|transfers?)\b",
                       r"\bmake\s+(?:a|the|this|that|another|one|my)\s+(?:\w+\s+)?(payment|transfer)\b"],
    "payment_modification": [r"\b(update|adjust|change|modify|amend|increase|decrease|raise|lower)\b[^.;]*\b(rent|payments?|standing orders?|scheduled|recurring|subscriptions?)\b"],
    "credential_change": [r"\b(update|change|reset|set|rotate)\b[^.;]*\bpassword\b"],
    "profile_change": [r"\b(update|change|correct|edit)\b[^.;]*\b(address|account info(?:rmation)?|account details|profile|street|city|contact details)\b"],
}
_SUBJECT_BEFORE = re.compile(r"\b(i|we|they|he|she|it)\b(?:\s+(?!want|need|would|'d)\w+){0,2}\s*$", re.I)
_PAST = re.compile(r"\b(paid|sent|transferred|refunded|received|got|charged|wired|was|were|had)\b", re.I)
_NEG = [
    (r"\b(?:do\s+not|don't|dont|never|please\s+no|must\s+not|should\s+not|shouldn't)\b[^.;]*\b(pay|send|transfer|refund|payments?|transfers?|transactions?)\b", ("value_transfer", "payment_modification")),
    (r"\bno\s+(?:new\s+|further\s+)?(payments?|transfers?|transactions?)\b", ("value_transfer", "payment_modification")),
    (r"\bwithout\s+(paying|sending|transferring|making)\b", ("value_transfer", "payment_modification")),
    (r"\b(?:do\s+not|don't|dont|never)\b[^.;]*\b(change|update|modify|touch)\b[^.;]*\b(password|credentials?)\b", ("credential_change",)),
    (r"\b(?:do\s+not|don't|dont|never)\b[^.;]*\b(change|update|modify|touch|do)\b\s+(anything|any\s+settings?|my\s+account)\b", CATEGORIES),
    (r"\b(read[- ]only|for\s+my\s+records\s+only|just\s+(?:tell|show|give|list)|only\s+(?:tell|show|give|list))\b", CATEGORIES),
]
_DERIVED = re.compile(r"\b(difference|share|split|half|twice|double|percent|too\s+much|too\s+little|the\s+rest|remaining|remainder|"
                      r"what\s+they(?:'ve|\s+have)?\s+sent|as\s+much|in\s+total|total|additional|plus|minus)\b|%", re.I)
_HISTORY = re.compile(r"\b(usually|like\s+last\s+(?:month|time|year)|same\s+as|as\s+before|as\s+usual|transaction\s+history|"
                      r"last\s+month's|previous(?:ly)?)\b", re.I)
_DELEG = re.compile(r"\b(accordingly|according\s+to|as\s+stated|as\s+described|as\s+written|as\s+per|stated\s+in|in\s+the\s+file)\b", re.I)
_OPEN = re.compile(r"\bfollow\b[^.;]*\b(instructions?|steps|directions)\b|\bdo\s+what(?:ever)?\s+it\s+says\b", re.I)
_PARTY = re.compile(r"\b(them|they|their|him|her|his|back|the\s+same\s+(?:account|recipient|person)|my\s+friend|that\s+account)\b", re.I)
_COND = re.compile(r"\b(if|when|unless|in\s+case|provided\s+that|only\s+if)\b", re.I)
_TARGET_DECL = re.compile(r"\b(account|iban|recipient|payee|beneficiary)\b[^.;]{0,25}(\bis|\bare|:)\s*$", re.I)
_SOURCE = re.compile(r"['\"“”‘’]([^'\"“”‘’]{1,80}\.[A-Za-z]{2,5})['\"“”‘’]")
_QUOTED = re.compile(r"['\"“”‘’]([^'\"“”‘’\s][^'\"“”‘’]{2,80})['\"“”‘’]")
_NUM = re.compile(r"(?<![\w.,])[$€£]?\s?\d[\d.,]*\d(?![\w%]|[.,]\d)|(?<![\w.,])[$€£]?\s?\d(?![\w%]|[.,]\d)")
_MONTH = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
_STOP = frozenset("""about above after again also amount been before being both could does doing down during each from further have having
here just like make more most much need only other over please same should some such than that their them then there these they this
those through under until very what when where which while will with would your account accounts payment payments transaction
transactions money check read file send sent paid update pay said called note month year total""".split())


def _clauses(text: str) -> List[Tuple[int, str]]:
    """Sentence-level clauses: split after ., !, ? or ; only when followed by white space (so decimals,
    file names and identifiers are not split). Returns (offset, clause) pairs covering the whole text."""
    out, start = [], 0
    for m in re.finditer(r"(?<=[.!?;])\s+", text):
        out.append((start, text[start:m.start()]))
        start = m.end()
    out.append((start, text[start:]))
    return [(o, c) for o, c in out if c.strip()] or [(0, text)]


def _clause_of(clauses, pos: int) -> int:
    idx = [i for i, (off, _) in enumerate(clauses) if off <= pos]
    return idx[-1] if idx else 0


def _is_request(clause: str, m: re.Match) -> bool:
    before = clause[:m.start()]
    if _SUBJECT_BEFORE.search(before):                 # "I usually pay", "they sent"
        return False
    return True


def compile_intent(objective: str) -> Intent:
    g = clean(objective)
    low = g.lower()
    clauses = _clauses(g)
    status: Dict[str, str] = {c: "absent" for c in CATEGORIES}
    spans: List[Tuple[str, Span]] = []
    conditional = set()
    req_clause_idx: Dict[str, List[int]] = {c: [] for c in CATEGORIES}
    for ci, (off, cl) in enumerate(clauses):
        for cat, pats in _REQ.items():
            for pat in pats:
                for m in re.finditer(pat, cl, flags=re.I):
                    if _is_request(cl, m):
                        status[cat] = "requested"
                        spans.append((cat, Span(off + m.start(), off + m.end(), cl[m.start():m.end()])))
                        req_clause_idx[cat].append(ci)
                        if _COND.search(cl):
                            conditional.add(cat)
    read_only = False
    for pat, cats in _NEG:
        for m in re.finditer(pat, g, flags=re.I):
            for cat in cats:
                status[cat] = "prohibited"                  # an explicit prohibition overrides a request cue
                spans.append((cat, Span(m.start(), m.end(), g[m.start():m.end()])))
            if cats == CATEGORIES:
                read_only = True
    # a profile-change cue that only says "account information" must not imply a credential change, and vice versa
    sources = tuple(dict.fromkeys(m.group(1) for m in _SOURCE.finditer(g)))
    iban_spans, ibans = [], []
    for m in IBAN_RE.finditer(g):
        c = canon_iban(m.group(1))
        if not c:
            continue
        iban_spans.append((m.start(1), m.end(1)))
        ci = _clause_of(clauses, m.start(1))
        off, cl = clauses[ci]
        before = cl[:m.start(1) - off]
        in_req = any(ci in v for k, v in req_clause_idx.items() if k in ("value_transfer", "payment_modification"))
        if in_req or _TARGET_DECL.search(before):
            role = "target"
        elif _PAST.search(cl):
            role = "historical"
        else:
            role = "mentioned"
        ibans.append(IbanMention(m.group(1), c, role, Span(m.start(1), m.end(1), m.group(1))))
    quoted = [(m.start(1), m.end(1), m.group(1)) for m in _QUOTED.finditer(g)]
    secrets = []
    for s, e, val in quoted:
        ci = _clause_of(clauses, s)
        if re.search(r"\bpassword\b", clauses[ci][1], re.I) and val not in sources:
            secrets.append(hashlib.sha256(val.encode()).hexdigest())
    amounts, modes = [], set()
    req_money = set(req_clause_idx["value_transfer"]) | set(req_clause_idx["payment_modification"])
    for ci in req_money:
        cl = clauses[ci][1]
        if _DERIVED.search(cl):
            modes.add("derived")
        if sources and (_DELEG.search(cl) or any(s in cl for s in sources)):
            modes.add("delegated")          # only to a source the user names
    if _HISTORY.search(g) and req_money:
        modes.add("history")
    for m in _NUM.finditer(g):
        s, e = m.start(), m.end()
        if any(a <= s < b or a < e <= b for a, b in iban_spans) or any(a <= s and e <= b for a, b, _ in quoted):
            continue
        tok = m.group(0).strip()
        ctx_b, ctx_a = low[max(0, s - 24):s], low[e:e + 28]
        if re.search(_MONTH + r"\s*,?\s*$", ctx_b) or re.fullmatch(r"(19|20)\d\d", tok) and re.search(r"\b(in|of|during|since)\s*$|" + _MONTH + r"\s*$", ctx_b):
            continue                                                         # dates
        if re.match(r"\s*(most\s+recent|recent|latest|last\s+\d|transactions?\b|items?\b|days?\b|weeks?\b|months?\b|years?\b|times?\b|st\b|nd\b|rd\b|th\b)", ctx_a):
            continue                                                         # counts, durations, ordinals
        if re.match(r"\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr|Boulevard|Blvd|Way|Square)\b", g[e:e + 40]) \
                or re.search(r"\b[A-Z]{2}\s*$", g[max(0, s - 4):s]) and re.fullmatch(r"\d{5}", tok):
            continue                                                         # street numbers and postal codes
        val, amb = parse_amount(tok)
        if val is None and not amb:
            continue
        ci = _clause_of(clauses, s)
        cl = clauses[ci][1]
        if _DERIVED.search(cl):
            role = "base"
        elif ci not in req_money and _PAST.search(cl) and not re.search(r"\b(is|are|will\s+be|should\s+be)\b[^.;]{0,12}$", cl[:s - clauses[ci][0]]):
            role = "historical"
        else:
            role = "value"
        amounts.append(AmountMention(val, amb, role, Span(s, e, tok)))
    party = any(_PARTY.search(clauses[ci][1]) for ci in req_clause_idx["value_transfer"])
    words = frozenset(w for w in re.findall(r"[a-z][a-z\-]{3,}", low) if w not in _STOP)
    return Intent(ops=tuple(status.items()), conditional=frozenset(conditional), op_spans=tuple(spans), ibans=tuple(ibans),
                  amounts=tuple(amounts), amount_modes=frozenset(modes), party_reference=bool(party), sources=sources,
                  secret_digests=tuple(secrets), content_words=words, read_only=read_only,
                  open_delegation=bool(_OPEN.search(g)))
