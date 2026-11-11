"""C4: bounded permission acquisition from a trusted request + bank receipt.
Engineering capability/verification policy inspired by CaMeL §5.2 and PROVISO
§3.1, not their exact algorithms. No new mathematical score or risk formula.
A production connector must authenticate ledger facts independently of the
agent's lower-trust content. No benchmark solution or hidden label is read.
"""
from dataclasses import dataclass
from decimal import Decimal
import re
from experiments.authorization_generalization.authorization import READS, canonical, validate
from experiments.authorization_generalization.candidate_policy import Decision
from rem.core.results import Verdict
from .provenance_policy import ProvenancePolicy

# Intentionally bounded FULL-request grammar, not general natural-language NLU.
_REFUND=re.compile(
    r"\s*(?:please\s+)?refund\s+(?P<iban>[A-Za-z]{2}[0-9]{2}[A-Za-z0-9\s-]{11,60}?)\s+"
    r"(?:for what they(?:'ve| have) sent me|the amount they sent me)\.?\s*", re.IGNORECASE|re.ASCII)

def parse_refund(objective):
    m=_REFUND.fullmatch(objective)
    if not m:return None
    try:return canonical('recipient',m.group('iban'))
    except (ValueError,TypeError):return None

@dataclass(frozen=True)
class Receipt:
    id: int
    sender: str
    recipient: str
    amount: str
    date: str

@dataclass(frozen=True)
class VerifiedLedger:
    """Trusted-host object; the agent cannot supply this object or its trust bit.
    'authenticated' is a host assertion, NOT a cryptographic implementation.
    """
    own_iban: str
    receipts: tuple[Receipt,...]
    authenticated: bool
    source: str
    def __post_init__(self):
        object.__setattr__(self,'receipts',tuple(self.receipts))


def receipt_arguments(target,ledger):
    if ledger is None or not ledger.authenticated:return None
    try:
        own=canonical('recipient',ledger.own_iban)
        matching=[r for r in ledger.receipts
                  if canonical('recipient',r.sender)==target and canonical('recipient',r.recipient)==own]
        if len(matching)!=1:return None
        r=matching[0]
        amount=canonical('amount',r.amount)
        # Keep decimal text at the host boundary; native tool schema parses it.
        args={'recipient':target,'amount':str(amount),'subject':'Refund','date':r.date}
        validate('send_money',args)
        return args
    except (ValueError,TypeError):return None

class VerifiedRefundPolicy:
    def __init__(self,objective,system_prompt,key_arguments,*,ledger=None,
                 repair=True,one_use=True,recognition=True):
        self.fallback=ProvenancePolicy(objective,system_prompt,key_arguments)
        self.target=parse_refund(objective) if recognition else None
        self.expected=receipt_arguments(self.target,ledger) if self.target else None
        self.ledger=ledger
        self.repair=repair;self.one_use=one_use;self.spent=False
    def ingest(self,tool,text,*,executed):
        self.fallback.ingest(tool,text,executed=executed)
    def decide(self,tool,args):
        if self.target is None:return self.fallback.decide(tool,args)
        if tool in READS:return self.fallback.decide(tool,args)
        if tool!='send_money':
            return Decision(Verdict.BLOCK,'contradiction','refund does not authorize another mutation tool')
        if self.spent and self.one_use:
            return Decision(Verdict.BLOCK,'contradiction','refund permission already reserved')
        if self.expected is None:
            return Decision(Verdict.ESCALATE,'insufficient','independent unique receipt unavailable')
        try: proposed=validate(tool,args)
        except (ValueError,TypeError):
            return Decision(Verdict.BLOCK,'contradiction','invalid mutation arguments')
        expected=validate(tool,self.expected)
        equal=proposed==expected
        if not equal and not self.repair:
            return Decision(Verdict.BLOCK,'contradiction','verified action mismatch; repair ablated')
        verdict=Verdict.ALLOW if equal else Verdict.MODIFY
        return Decision(verdict,'verified_permission','independent receipt and trusted full-request refund',dict(self.expected),'refund')
    def reserve(self,decision):
        if decision.grant_id=='refund':
            if self.spent and self.one_use:raise RuntimeError('permission already reserved')
            self.spent=True
