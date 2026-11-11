"""Label-free runtime adapters and native NO-ADAPT replay for the new study.
Native scoring receives task metadata; security policies never receive it.
C1 and original policies retain the original step-level Modify=withhold
semantics; C4 Modify executes independently verified replacement arguments.
"""
import time
from rem.core.results import Verdict
from rem.algorithms.behavior.evidence import EpisodeTracker
from rem.algorithms.detection.ridge_logistic import sigmoid
from rem.integration.agentdojo_replay import _agentdojo_elements
from experiments.authorization_generalization.candidate_policy import Decision
from .refund_policy import Receipt,VerifiedLedger,VerifiedRefundPolicy,parse_refund
from .provenance_policy import ProvenancePolicy

CANDIDATES=('C1_action_model','C2_canonical_provenance','C3_target_only','C4_verified_refund')
ABLATIONS=('C4_no_verifier','C4_no_repair','C4_no_one_use','C4_no_recognition')
BASELINES=('B0','B1','REM_R4','x_act1','AA_REM_previous')

class RiskPolicy:
    def __init__(self,objective,system_prompt,setup,reference,scorer,decision_policy,*,rule=None):
        self.setup=setup
        self.tracker=EpisodeTracker(objective=objective,trusted_texts=[system_prompt],spec=setup.spec,
                                    detector=setup.detector,reference=reference)
        self.scorer=scorer;self.decision_policy=decision_policy;self.rule=rule
        self.last_probability=None
    def begin_decision_point(self):self.tracker.begin_decision_point()
    def ingest(self,tool,text,*,executed):self.tracker.add_tool_result(tool,text,executed=executed)
    def decide(self,tool,args):
        feats,available=self.tracker.features(tool,args)
        if self.rule=='B0':verdict=Verdict.ALLOW
        elif self.rule=='x_act1':verdict=Verdict.BLOCK if feats['x_act1'] else Verdict.ALLOW
        else:
            if self.scorer is None:raise RuntimeError('calibrated fold unavailable; comparison must not run')
            score=self.scorer.logit(feats)
            probability=float(sigmoid(self.scorer.gamma_1*score+self.scorer.gamma_0))
            self.last_probability=probability
            verdict=self.decision_policy.decide(probability,self.setup.tier_map.tier(tool,args),tool,available).verdict
        self.tracker.record_proposal(tool,args)
        # Legacy Modify withholds the current call. It never executes a replacement.
        released_args=dict(args) if verdict==Verdict.ALLOW else None
        return Decision(verdict,'legacy_policy','original step-level mitigation',released_args)
    def reserve(self,decision):pass


def bank_snapshot_from_environment(env):
    """Independent trusted backend adapter; narrow whitelist, no clean-state oracle.
    The actual current native environment may already contain an injected
    transaction subject. That subject, files, profile and all task/attack data
    are deliberately excluded from this interface.
    """
    bank=env.bank_account
    # Native AgentDojo fixtures use the local-account alias 'me'.
    # Resolve it only in this trusted backend adapter, never in agent arguments.
    def account_id(value):return str(bank.iban) if value=='me' else str(value)
    return VerifiedLedger(str(bank.iban),tuple(Receipt(int(t.id),account_id(t.sender),account_id(t.recipient),str(t.amount),str(t.date))
                          for t in bank.transactions),True,'native_banking_backend')


def replay(ep,suite,name,setup,reference,*,scorer=None,decision_policy=None,complete_trace=False):
    from agentdojo.agent_pipeline import ToolsExecutor
    from agentdojo.functions_runtime import FunctionCall
    from agentdojo.types import ChatToolResultMessage,text_content_block_from_string
    from agentdojo.agent_pipeline.tool_execution import is_string_list
    from ast import literal_eval
    from experiments.authorization_generalization.authorization import Contract
    from experiments.authorization_generalization.candidate_policy import AuthorizationPolicy
    AgentPipeline,SystemMessage,InitQuery,ToolsExecutionLoop,ReplayLLM,_ = _agentdojo_elements()
    audit=[];policy=None;backend_accesses=0
    def create(env):
        nonlocal backend_accesses
        if name in {'C2_canonical_provenance','C3_target_only'}:
            return ProvenancePolicy(ep.objective,ep.system_prompt,setup.spec.key_arguments,target_only=name=='C3_target_only')
        if name.startswith('C4_'):
            ledger=None
            if name not in {'C4_no_verifier','C4_no_recognition'} and parse_refund(ep.objective) is not None:
                ledger=bank_snapshot_from_environment(env);backend_accesses+=1
            return VerifiedRefundPolicy(ep.objective,ep.system_prompt,setup.spec.key_arguments,ledger=ledger,
                repair=name!='C4_no_repair',one_use=name!='C4_no_one_use',recognition=name!='C4_no_recognition')
        if name=='AA_REM_previous':return AuthorizationPolicy(Contract())
        return RiskPolicy(ep.objective,ep.system_prompt,setup,reference,scorer,decision_policy,
                          rule=name if name in {'B0','x_act1'} else None)
    class Executor(ToolsExecutor):
        def query(self,query,runtime,env,messages=[],extra_args={}):
            nonlocal policy
            if not messages or messages[-1]['role']!='assistant' or not messages[-1]['tool_calls']:
                return query,runtime,env,messages,extra_args
            if policy is None:policy=create(env)
            if hasattr(policy,'begin_decision_point'):policy.begin_decision_point()
            results=[]
            for call in messages[-1]['tool_calls']:
                for k,v in call.args.items():
                    if isinstance(v,str) and is_string_list(v):call.args[k]=literal_eval(v)
                start=time.perf_counter_ns()
                d=policy.decide(call.function,dict(call.args))
                release=d.verdict in {Verdict.ALLOW,Verdict.MODIFY} and d.args is not None
                if release:
                    policy.reserve(d)
                    result,err=runtime.run_function(env,call.function,dict(d.args))
                    text=self.output_formatter(result)
                else:text,err='',f'REM candidate: {d.verdict.value}: {d.reason}'
                if hasattr(policy,'store'):policy.store.ingest(text,executed=release and err is None)
                else:policy.ingest(call.function,text if err is None else (err or ''),executed=release and err is None)
                results.append(ChatToolResultMessage(role='tool',content=[text_content_block_from_string(text)],
                               tool_call_id=call.id,tool_call=call,error=err))
                audit.append({'tool':call.function,'verdict':d.verdict.value,'released':release,
                              'evidence':d.evidence,'latency_ms_including_tool':(time.perf_counter_ns()-start)/1e6,
                              'verified_repair':d.verdict==Verdict.MODIFY and d.args is not None,
                              'model_probability':getattr(policy,'last_probability',None)})
            return query,runtime,env,[*messages,*results],extra_args
    actor=ReplayLLM(ep)
    # Keep the original 15-round budget for the primary comparison; a
    # separate sensitivity replays every recorded tool-bearing assistant message.
    rounds=sum(m.get('role')=='assistant' and bool(m.get('tool_calls')) for m in ep.raw_messages)
    loop=ToolsExecutionLoop([Executor(),actor],max_iters=max(1,rounds)) if complete_trace else ToolsExecutionLoop([Executor(),actor])
    pipe=AgentPipeline([SystemMessage(ep.system_prompt),InitQuery(),actor,loop])
    pipe.name='rem_candidates_v2_replay'
    ut=suite.get_user_task_by_id(ep.user_task_id)
    it=suite.get_injection_task_by_id(ep.injection_task_id) if ep.injection_task_id else None
    error=None
    try:utility,security=suite.run_task_with_pipeline(pipe,ut,it,dict(ep.injections))
    except Exception as exc:utility,security,error=False,False,repr(exc)
    return {'utility':bool(utility),'security':bool(security),'error':error,'audit':audit,'backend_accesses':backend_accesses}
