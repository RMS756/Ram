"""L1: canonical forms of security-sensitive financial values.

Canonicalization is a declared, finite set of rules (no learned component):
  IBAN-like identifiers: remove spaces, hyphens, dots and zero-width characters; upper-case.
  Amounts: exact decimal value (Decimal), sign kept, trailing zeros removed ('98.70' == '98.7' == 98.7).
A value that cannot be parsed is returned as None ("unparseable"); callers must treat None as untrusted/unknown.
"""
from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any, List, Optional

_ZW = "​‌‍⁠﻿"
_SEP = re.compile(r"[\s\-\. " + _ZW + r"]")
# two letters, two digits, then 10-30 alphanumerics possibly separated by single separators
_IBAN_LOOSE = re.compile(r"\b([A-Za-z]{2}[0-9]{2}(?:[\s\-\. " + _ZW + r"]?[A-Za-z0-9]){10,30})\b")
_NUM = re.compile(r"(?<![A-Za-z0-9])[-+]?\d{1,3}(?:[,  ]\d{3})+(?:\.\d+)?|(?<![A-Za-z0-9])[-+]?\d+(?:\.\d+)?")


def canonical_iban(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    s = _SEP.sub("", value).upper()
    if re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z0-9]{10,30}", s):
        return s
    return None


_START = re.compile(r"(?<![A-Za-z0-9])([A-Za-z]{2}[0-9]{2}[A-Za-z0-9]*)")
_GROUP = re.compile(r"[\s\-\.\u00a0" + _ZW + r"]([A-Za-z0-9]+)")


def find_ibans(text: str) -> List[str]:
    """All canonical IBAN-like identifiers in ``text``. Separator-delimited groups are appended only while they look
    like account groups (contain a digit, or are short upper-case letter groups such as 'NWBK'), so that a following
    word ('today', 'that') is never swallowed into the identifier."""
    if not text:
        return []
    out = []
    for m in _START.finditer(text):
        parts, pos = [m.group(1)], m.end()
        while True:
            g = _GROUP.match(text, pos)
            if not g:
                break
            tok = g.group(1)
            if any(ch.isdigit() for ch in tok) or (tok.isalpha() and tok.isupper() and len(tok) <= 4):
                parts.append(tok)
                pos = g.end()
                if sum(len(p) for p in parts) >= 34:
                    break
            else:
                break
        c = canonical_iban("".join(parts))
        if c:
            out.append(c)
    return out


def canonical_amount(value: Any) -> Optional[Decimal]:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        try:
            return Decimal(repr(value)).normalize() if isinstance(value, float) else Decimal(value).normalize()
        except InvalidOperation:
            return None
    if isinstance(value, str):
        s = value.strip().replace(",", "").replace(" ", "").replace(" ", "")
        s = re.sub(r"^[^\d\-+]+", "", s)  # leading currency symbols
        try:
            return Decimal(s).normalize()
        except InvalidOperation:
            return None
    return None


def find_amounts(text: str) -> List[Decimal]:
    if not text:
        return []
    out = []
    for m in _NUM.finditer(text):
        d = canonical_amount(m.group(0))
        if d is not None:
            out.append(d)
    return out


def canonical_text(value: Any) -> Optional[str]:
    """Whitespace- and case-normalized text for free-text sensitive fields (password, street, city)."""
    if not isinstance(value, str):
        return None
    return re.sub(r"\s+", " ", value.replace("\t", " ")).strip().lower()
