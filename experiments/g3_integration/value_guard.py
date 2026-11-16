"""Post-scoring follow-up, frozen separately: constrain directly stated payment amounts.

Limited grammar, no learned parameter and no evaluation metadata. See follow-up protocol.
"""
import re
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'experiments/improve_study'))
from intent import canon_iban,amount_of,parse_amount,compile_intent
from intent_v3 import compile_intent_v3,TOOL_EFFECT
from rem.core.results import Verdict

DIRECT=re.compile(r'\b(?:send|transfer|pay)\s+(?:(?:exactly|only|of)\s+)?(?:[$€£]\s*)?(\d[\d.,]*)',re.I)

def direct_values(instruction):
    values=[]
    raw=[]
    for m in DIRECT.finditer(instruction.span.text):
        value,ambiguous=parse_amount(m.group(1).rstrip('.,'))
        if value is not None or ambiguous:raw.append((value,ambiguous))
        if (ambiguous and instruction.amount_ambiguous) or (value is not None and value==instruction.amount):
            values.append((value,ambiguous))
    if not values and instruction.amount is None and not instruction.amount_ambiguous and len(raw)==1:
        # The old compiler may mark a direct amount as a calculation input due
        # to an earlier 'half' phrase. Recover only an unambiguous clause binding.
        targets={m.canonical for m in compile_intent(instruction.span.text).ibans}
        if targets=={instruction.target}:values=raw
    return values

def value_verdict(intent,tool,args):
    effect=TOOL_EFFECT.get(tool);recipient=canon_iban((args or {}).get('recipient'))
    if effect is None or recipient is None or 'amount' not in (args or {}):return None
    matching=[i for i in intent.instructions if effect in i.effects and i.target==recipient]
    if not matching:return None
    bindings=[direct_values(i) for i in matching]
    if any(not b for b in bindings):return None
    values=[v for b in bindings for v in b];amount=amount_of(args['amount'])
    if any(v is not None and not ambiguous and amount==v for v,ambiguous in values):return None
    return Verdict.ESCALATE if any(ambiguous for _,ambiguous in values) else Verdict.BLOCK

def attach_direct_value_guard(guard):
    intent=compile_intent_v3(guard.episode.objective)
    base_decide,base_evaluate=guard.decide,guard.evaluate
    def decide(c):
        verdict,source,details=base_decide(c) # also records every proposal for runtime fulfillment
        constraint=value_verdict(intent,c.tool,c.args)
        if verdict is Verdict.ALLOW and constraint is not None:
            return constraint,'direct_value_ambiguous' if constraint is Verdict.ESCALATE else 'direct_value_mismatch',{**details,'direct_value_veto':True}
        return verdict,source,details
    def evaluate(tool,args):
        start=time.perf_counter();result=base_evaluate(tool,args);row=guard.audit[-1]
        if row['verdict_source'].startswith('direct_value_'):
            row['probability_used_for_verdict']=False;row['risk_table']='not_applicable'
        row['rem_latency_full_ms']=(time.perf_counter()-start)*1000
        guard.full_latencies_ms[-1]=row['rem_latency_full_ms']
        return result
    guard.decide,guard.evaluate=decide,evaluate
    return guard
