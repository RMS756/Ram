"""Engineering rule candidates, not claimed as published defense reproductions.
Source: original REM x_act1 provenance definition; canonical matching is an
explicit implementation change. C3 intentionally drops amount checking.
No task IDs, labels, attack objectives or ground-truth solutions are inputs.
"""
import re
from experiments.authorization_generalization.authorization import READS, SCHEMAS, canonical, validate
from experiments.authorization_generalization.candidate_policy import Decision
from rem.algorithms.context.provenance import strip_invisible, value_occurs_in
from rem.core.results import Verdict


def iban_occurs(value, texts):
    try: token=canonical('recipient',value)
    except (ValueError,TypeError): return False
    pattern=r'(?<![A-Za-z0-9])'+r'[\s-]*'.join(re.escape(c) for c in token)+r'(?![A-Za-z0-9])'
    return any(re.search(pattern,strip_invisible(t),flags=re.IGNORECASE|re.ASCII) for t in texts)


def occurs(key,value,texts):
    return iban_occurs(value,texts) if key=='recipient' else value_occurs_in(value,texts)


class ProvenancePolicy:
    """C2/C3: provenance is evidence, not a full permission proof."""
    def __init__(self, objective, system_prompt, key_arguments, *, target_only=False):
        self.trusted=(objective,system_prompt)
        self.key_arguments=key_arguments
        self.untrusted=[]
        self.target_only=target_only
    def ingest(self, tool, text, *, executed):
        # Error text is also lower-trust context; it cannot create user permission.
        self.untrusted.append(strip_invisible(text or ''))
    def decide(self, tool, args):
        if tool in READS:
            return Decision(Verdict.ALLOW,'deployment_permission','declared banking read',dict(args))
        if tool not in SCHEMAS:
            return Decision(Verdict.BLOCK,'contradiction','unknown mutation tool')
        try: validate(tool,args)
        except (ValueError,TypeError):
            return Decision(Verdict.BLOCK,'contradiction','invalid mutation arguments')
        keys=self.key_arguments.get(tool,())
        if self.target_only and tool in {'send_money','schedule_transaction','update_scheduled_transaction'}:
            keys=tuple(k for k in keys if k!='amount')
        unsupported=[k for k in keys if k in args and args[k] is not None
                     and occurs(k,args[k],self.untrusted) and not occurs(k,args[k],self.trusted)]
        if unsupported:
            return Decision(Verdict.BLOCK,'external_only','lower-trust key arguments: '+','.join(unsupported))
        return Decision(Verdict.ALLOW,'no_external_only_key','provenance rule only; authorization not established',dict(args))
    def reserve(self,decision): pass
