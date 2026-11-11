"""Candidate A: explicit three-state authorization rules, no numeric score.
[PROPOSED — SUPERVISOR APPROVAL REQUIRED]
Engineering implementation inspired by PROVISO §3.1 and capability policies;
NOT PROVISO, Task Shield, or an exact reproduction of any published defense.
"""
from dataclasses import dataclass
from typing import Mapping, Any
from rem.core.results import Verdict
from .authorization import Contract, READS, SCHEMAS, validate
from .provenance import EvidenceStore

@dataclass(frozen=True)
class Decision:
    verdict: Verdict
    evidence: str
    reason: str
    args: Mapping[str,Any] | None = None
    grant_id: str | None = None

class AuthorizationPolicy:
    def __init__(self, contract: Contract, *, authorization=True, provenance=True,
                 behavior=True, repair=True):
        self.contract=contract
        self.store=EvidenceStore()
        self.authorization=authorization; self.provenance=provenance
        self.behavior=behavior; self.repair=repair
        self.spent=set()
    def decide(self, tool: str, args: Mapping[str,Any]) -> Decision:
        if tool in READS:
            return Decision(Verdict.ALLOW,'deployment_permission','declared banking read',dict(args))
        if tool not in SCHEMAS:
            return Decision(Verdict.BLOCK,'contradiction','tool outside declared banking interface')
        try: proposed=validate(tool,args)
        except (ValueError,TypeError):
            return Decision(Verdict.BLOCK,'contradiction','invalid or unknown mutation arguments')
        if not self.authorization:
            return Decision(Verdict.ESCALATE,'insufficient','authorization ablated')
        grants=[g for g in self.contract.grants if g.tool==tool]
        if not grants:
            evidence='contradiction' if self.contract.grants else 'insufficient'
            verdict=Verdict.BLOCK if self.contract.grants else Verdict.ESCALATE
            return Decision(verdict,evidence,'no matching operation grant')
        unresolved=False; matches=[]; repairs=[]; spent_match=False
        for g in grants:
            resolved=self.store.resolve(g,enabled=self.provenance)
            if resolved is None: unresolved=True; continue
            expected=validate(tool,resolved)
            if self.behavior and g.id in self.spent:
                if proposed==expected: spent_match=True
                continue
            # Same fields must be authorized, including subject/date/id. No wildcards.
            if proposed==expected:
                matches.append((g,resolved))
            elif proposed.keys()==expected.keys():
                changed={k for k in proposed if proposed[k]!=expected[k]}
                if changed and changed <= {'recipient','amount'}: repairs.append((g,resolved))
        if len(matches)==1:
            g,resolved=matches[0]
            # Deliver exactly the independently authorized representation.
            v=Verdict.ALLOW if dict(args)==resolved else Verdict.MODIFY
            return Decision(v,'positive','exact authorized action',dict(resolved),g.id)
        if matches or unresolved:
            return Decision(Verdict.ESCALATE,'insufficient','ambiguous grant or unavailable bound evidence')
        if spent_match:
            return Decision(Verdict.BLOCK,'contradiction','one-use authorization already committed')
        if self.repair and len(repairs)==1:
            g,resolved=repairs[0]
            return Decision(Verdict.MODIFY,'contradiction','repair from unique complete trusted grant',dict(resolved),g.id)
        return Decision(Verdict.BLOCK,'contradiction','action contradicts resolved grants')
    def reserve(self, decision: Decision):
        """Consume before execution; uncertain execution never creates free retries.
        Single-thread host assumption. Concurrent production execution needs an
        atomic persistent reservation store, which is outside this experiment.
        """
        if decision.grant_id and decision.verdict in {Verdict.ALLOW,Verdict.MODIFY}:
            if self.behavior and decision.grant_id in self.spent: raise RuntimeError('grant already spent')
            self.spent.add(decision.grant_id)
