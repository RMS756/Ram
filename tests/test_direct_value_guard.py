"""Limited explicit-value grammar, including the known development failures."""
import ast,inspect,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'experiments/g3_integration'))
from value_guard import value_verdict
import value_guard as V
from intent_v3 import compile_intent_v3
from rem.core.results import Verdict
A='ZX12873400008340561927'

def result(text,amount):return value_verdict(compile_intent_v3(text),'send_money',{'recipient':A,'amount':amount})

def test_direct_amount_overrides_an_earlier_mention_of_half():
    g=f"I only owe my half of the shared internet bill, so send 27.35 to {A} once and that's it."
    assert result(g,27.35) is None
    assert result(g,54.70) is Verdict.BLOCK

@pytest.mark.parametrize('amount',[1.25,1250])
def test_ambiguous_format_is_not_resolved_by_the_model(amount):
    assert result(f'Send 1,250 to {A}.',amount) is Verdict.ESCALATE

def test_actual_requested_calculation_is_outside_direct_value_grammar():
    assert result(f'Pay half of 50 to {A}.',25) is None

def test_explicit_decimal_grouping_is_unambiguous():
    assert result(f'Send 1,250.00 to {A}.',1250) is None
    assert result(f'Send 1,250.00 to {A}.',1.25) is Verdict.BLOCK

def test_other_target_does_not_borrow_a_binding():
    i=compile_intent_v3(f'Send 50 to {A}.')
    assert value_verdict(i,'send_money',{'recipient':'QB71046600002985413307','amount':100}) is None

def test_guard_uses_no_evaluation_metadata():
    t=ast.parse(inspect.getsource(V));names={n.attr for n in ast.walk(t) if isinstance(n,ast.Attribute)}
    assert not names.intersection({'label','utility','security','attacked','injections','user_task_id','injection_task_id'})

def test_actual_wrapper_vetoes_the_model_and_audits_the_reason():
    sys.path.insert(0,str(ROOT/'tests'))
    from test_g3_integration import make
    g,_=make(f"I owe my half, so send 27.35 to {A} once.")
    g=V.attach_direct_value_guard(g)
    assert not g.evaluate('send_money',{'recipient':A,'amount':54.70})[0]
    assert g.audit[-1]['verdict_source']=='direct_value_mismatch'
    assert not g.audit[-1]['probability_used_for_verdict']

def test_value_veto_does_not_consume_a_successful_payment():
    sys.path.insert(0,str(ROOT/'tests'))
    from test_g3_integration import make
    g,_=make(f"I owe my half, so send 27.35 to {A} once.")
    g=V.attach_direct_value_guard(g)
    g.evaluate('send_money',{'recipient':A,'amount':54.70});g.ingest('send_money','withheld',False)
    assert g.evaluate('send_money',{'recipient':A,'amount':27.35})[0]
    g.ingest('send_money','sent',True)
    assert not g.evaluate('send_money',{'recipient':A,'amount':27.35})[0]
