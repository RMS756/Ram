"""Check policy composition, live success tracking and audit truthfulness."""
import ast
import inspect
import sys
from pathlib import Path
from types import SimpleNamespace
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/g3_integration'))
sys.path.insert(0,str(ROOT/'experiments/pilot'))
import guard as module
import common
from rem.algorithms.behavior.evidence import BenignReference,FEATURE_ORDER
from rem.core.results import Verdict
from rem.integration.agentdojo_replay import FrozenScorer,GuardConfig,RemGuard

A='ZK52390800003316720548';B='QB71046600002985413307'

def call(recipient=A,amount=50):
    return {'recipient':recipient,'amount':amount,'subject':'payment','date':'2026-11-16'}

def make(objective,verdict=Verdict.ALLOW,mode='strict',predicates=None):
    st=common.make_setup();seen=[]
    cfg=GuardConfig(st.spec,st.detector,BenignReference(frozenset()),st.tier_map,st.restricted,'step_level','no_reviewer')
    scorer=FrozenScorer(tuple(FEATURE_ORDER),-4.0,tuple(0.0 for _ in FEATURE_ORDER),0.0,1.0,tuple(0.0 for _ in FEATURE_ORDER))
    def decide(c):
        seen.append((c.tool,dict(c.args)))
        return verdict,'test_rem',{'risks':{verdict.value:0.1}}
    ep=SimpleNamespace(objective=objective,system_prompt='',injection_task_id=None,episode_id='regression')
    return module.attach_permission_gate(RemGuard(cfg,scorer,decide,st.labeler,ep),mode=mode,predicates=predicates),seen

@pytest.mark.parametrize('args',[call(A,100),call(B,50)])
def test_swapped_amounts_are_denied_even_when_rem_would_allow(args):
    g,seen=make(f'Send 50 to {A} and 100 to {B}.')
    released,_=g.evaluate('send_money',args)
    assert not released and not seen and g.audit[-1]['verdict_source']=='g3_denied'

def test_wrong_payment_effect_is_denied():
    g,seen=make(f'Create a monthly standing order for 50 to {A}.')
    assert not g.evaluate('send_money',call())[0] and not seen

def test_subjective_condition_is_escalated_without_consulting_rem():
    g,seen=make(f'If something looks suspicious, send 50 to {A}.')
    assert not g.evaluate('send_money',call())[0]
    assert g.audit[-1]['verdict']=='escalate' and not seen

def test_false_compound_condition_is_denied():
    g,seen=make(f'If my balance is above 1000 and below 5000, send 50 to {A}.')
    g.evaluate('get_balance',{});g.ingest('get_balance','10000',executed=True);seen.clear()
    assert not g.evaluate('send_money',call())[0] and not seen

@pytest.mark.parametrize('verdict',list(Verdict))
def test_supported_permission_preserves_every_rem_verdict(verdict):
    g,seen=make(f'Send 50 to {A}.',verdict)
    assert g.evaluate('send_money',call())[0] is (verdict is Verdict.ALLOW)
    assert g.audit[-1]['verdict']==verdict.value and len(seen)==1

@pytest.mark.parametrize('success',[True,False])
def test_only_successful_execution_consumes_the_payment(success):
    g,seen=make(f'Send 50 to {A}.')
    assert g.evaluate('send_money',call())[0]
    g.ingest('send_money','sent' if success else 'error',executed=success)
    assert g.evaluate('send_money',call())[0] is (not success)

def test_withheld_call_does_not_consume_permission():
    g,seen=make(f'Send 50 to {A}.',Verdict.BLOCK)
    g.evaluate('send_money',call());g.ingest('send_money','withheld',executed=False)
    g.evaluate('send_money',call())
    assert len(seen)==2

def test_guard_audit_keeps_score_but_does_not_claim_it_caused_rejection():
    g,seen=make(f'Send 50 to {A}.')
    g.evaluate('send_money',call(B))
    a=g.audit[-1]
    assert 0<a['p']<1 and a['phi']
    assert not a['probability_used_for_verdict'] and a['risk_table']=='not_applicable'
    assert not a['details']['rem_consulted'] and a['rem_latency_full_ms']>=a['rem_latency_ms']

def test_unrestricted_read_reaches_rem():
    g,seen=make(f'Send 50 to {A}.')
    assert g.evaluate('get_balance',{})[0] and seen[0][0]=='get_balance'

def test_runtime_adapter_has_no_access_to_ground_truth_fields():
    tree=ast.parse(inspect.getsource(module))
    names={n.attr for n in ast.walk(tree) if isinstance(n,ast.Attribute)}
    assert not names.intersection({'label','utility','security','attacked','injections','user_task_id','injection_task_id'})

def predicates():
    from rem.algorithms.decision.policy import PredicatePolicy
    return PredicatePolicy(frozenset(),3,('x_act1',),frozenset(common.make_setup().restricted),True)

def test_routing_releases_supported_call_without_a_learned_veto():
    g,seen=make(f'Send 50 to {A}.',Verdict.BLOCK,mode='routed',predicates=predicates())
    assert g.evaluate('send_money',call())[0] and not seen
    assert not g.audit[-1]['probability_used_for_verdict']

def test_routing_cannot_override_a_denied_recipient():
    g,seen=make(f'Send 50 to {A}.',mode='routed',predicates=predicates())
    assert not g.evaluate('send_money',call(B))[0] and not seen

def test_routing_sends_only_authorized_value_uncertainty_to_model():
    g,seen=make(f'Send money to {A}.',mode='routed',predicates=predicates())
    ev=g.permission_gate.evidence(g.tracker,'send_money',call(),3)
    assert ev.overall=='unknown' and ev.authority
    assert g.evaluate('send_money',call())[0] and len(seen)==1

def test_routing_does_not_treat_subjective_condition_as_satisfied():
    g,seen=make(f'If something looks suspicious, send 50 to {A}.',mode='routed',predicates=predicates())
    assert not g.evaluate('send_money',call())[0] and not seen

def test_routing_retains_explicit_d1_prohibition():
    from rem.algorithms.decision.policy import PredicatePolicy
    pred=PredicatePolicy(frozenset({'send_money'}),3,('x_act1',),frozenset(common.make_setup().restricted),True)
    g,seen=make(f'Send 50 to {A}.',mode='routed',predicates=pred)
    assert not g.evaluate('send_money',call())[0] and not seen
    assert g.audit[-1]['verdict_source']=='D1'
