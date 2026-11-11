"""Engineering authorization contracts; NOT a published numerical estimator.
Conceptual sources: PROVISO §3.1 (licensed operation/target), CaMeL §security
policies. Contracts must be constructed by trusted host code, never the agent.
No natural-language authorization extractor is claimed or silently substituted.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re
import unicodedata
from typing import Any, Mapping

READS = frozenset({'get_iban', 'get_balance', 'get_most_recent_transactions',
                   'get_scheduled_transactions', 'read_file', 'get_user_info'})
SCHEMAS = {
 'send_money': ({'recipient','amount','subject','date'}, set()),
 'schedule_transaction': ({'recipient','amount','subject','date','recurring'}, set()),
 'update_scheduled_transaction': ({'id'}, {'recipient','amount','subject','date','recurring'}),
 'update_password': ({'password'}, set()),
 'update_user_info': (set(), {'first_name','last_name','street','city'}),
}
# Checked against the installed banking tool signature by a regression test.

def canonical(key: str, value: Any):
    if key == 'recipient':
        if not isinstance(value, str): raise ValueError('recipient must be a string')
        value = ''.join(c for c in value if not c.isspace() and c != '-' and unicodedata.category(c) != 'Cf').upper()
        if not re.fullmatch(r'[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}', value, flags=re.ASCII):
            raise ValueError('unsupported IBAN representation')
        return value
    if key == 'amount':
        if isinstance(value, bool): raise ValueError('boolean amount')
        try: d = Decimal(str(value))
        except InvalidOperation: raise ValueError('invalid decimal amount') from None
        if not d.is_finite() or d <= 0: raise ValueError('amount must be finite and positive')
        return d
    if key == 'id':
        if type(value) is not int or value < 0: raise ValueError('invalid transaction id')
    if key == 'recurring' and type(value) is not bool: raise ValueError('recurring must be boolean')
    if key not in {'amount','id','recurring'} and not isinstance(value,str):
        raise ValueError('argument must be a string')
    if key == 'date':
        from datetime import date
        date.fromisoformat(value)
    return value


def validate(tool: str, args: Mapping[str, Any]):
    if tool not in SCHEMAS: raise ValueError('unknown mutation tool')
    required, optional = SCHEMAS[tool]
    if not required <= args.keys() or not args.keys() <= required | optional or not args:
        raise ValueError('missing or extra arguments')
    # Optional None values are allowed by AgentDojo; omission has the same effect.
    clean = {k: canonical(k,v) for k,v in args.items() if v is not None}
    if not required <= clean.keys() or not clean: raise ValueError('empty mutation')
    return clean

@dataclass(frozen=True)
class ExternalField:
    """A trusted contract delegates one argument to an independently pinned JSON artifact."""
    sha256: str
    field: str

@dataclass(frozen=True)
class Grant:
    id: str
    tool: str
    args: Mapping[str, Any]
    source: str
    def __post_init__(self):
        if self.source not in {'trusted_user','verified_policy'}:
            raise ValueError('untrusted grant source')
        if not self.id or self.tool not in SCHEMAS: raise ValueError('invalid grant')
        # Snapshot caller-owned mappings to prevent subsequent mutation.
        from types import MappingProxyType
        object.__setattr__(self, 'args', MappingProxyType(dict(self.args)))
        for k,v in self.args.items():
            if not isinstance(v, ExternalField): canonical(k,v)
        required,optional = SCHEMAS[self.tool]
        if not required <= self.args.keys() or not self.args.keys() <= required|optional or not self.args:
            raise ValueError('incomplete grant')

@dataclass(frozen=True)
class Contract:
    grants: tuple[Grant, ...] = ()
    def __post_init__(self):
        object.__setattr__(self,'grants',tuple(self.grants))
        if len({g.id for g in self.grants}) != len(self.grants): raise ValueError('duplicate grant id')
