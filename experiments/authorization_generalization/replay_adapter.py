"""Candidate replay executor. Reuses original replay actor and native scorer.
Engineering adaptation: actually execute Decision.args for Modify; no reviewer.
Never supplies task IDs, injection labels, benchmark truth, or outcomes to policy.
"""
import time
from rem.integration.agentdojo_replay import _agentdojo_elements
from rem.core.results import Verdict
from .authorization import Contract
from .candidate_policy import AuthorizationPolicy

OPTIONS={'AA_REM':{},'AA_no_authorization':{'authorization':False},
         'AA_no_provenance':{'provenance':False},'AA_no_behavior':{'behavior':False},
         'AA_no_repair':{'repair':False}}

def replay_candidate(ep,suite,name):
    from agentdojo.agent_pipeline import ToolsExecutor
    from agentdojo.types import ChatToolResultMessage,text_content_block_from_string
    AgentPipeline,SystemMessage,InitQuery,ToolsExecutionLoop,ReplayLLM,_ = _agentdojo_elements()
    policy=AuthorizationPolicy(Contract(),**OPTIONS[name])
    audit=[]
    class Executor(ToolsExecutor):
        def query(self,query,runtime,env,messages=[],extra_args={}):
            if not messages or messages[-1]['role']!='assistant' or not messages[-1]['tool_calls']:
                return query,runtime,env,messages,extra_args
            results=[]
            for call in messages[-1]['tool_calls']:
                start=time.perf_counter_ns()
                d=policy.decide(call.function,call.args)
                release=d.verdict in {Verdict.ALLOW,Verdict.MODIFY}
                if release:
                    policy.reserve(d)
                    res,err=runtime.run_function(env,call.function,dict(d.args))
                    out=self.output_formatter(res)
                else: out,err='',f'AA-REM: {d.verdict.value}: {d.reason}'
                policy.store.ingest(out,executed=release and err is None)
                results.append(ChatToolResultMessage(role='tool',content=[text_content_block_from_string(out)],
                               tool_call_id=call.id,tool_call=call,error=err))
                audit.append({'tool':call.function,'verdict':d.verdict.value,'released':release,
                              'evidence':d.evidence,'latency_ms':(time.perf_counter_ns()-start)/1e6})
            return query,runtime,env,[*messages,*results],extra_args
    actor=ReplayLLM(ep)
    pipe=AgentPipeline([SystemMessage(ep.system_prompt),InitQuery(),actor,ToolsExecutionLoop([Executor(),actor])])
    pipe.name='aa_rem_replay'
    ut=suite.get_user_task_by_id(ep.user_task_id)
    it=suite.get_injection_task_by_id(ep.injection_task_id) if ep.injection_task_id else None
    error=None
    try: utility,security=suite.run_task_with_pipeline(pipe,ut,it,dict(ep.injections))
    except Exception as exc: utility,security,error=False,False,repr(exc)
    return {'utility':bool(utility),'security':bool(security),'error':error,'audit':audit}
