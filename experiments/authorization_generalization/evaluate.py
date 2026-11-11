"""Executable study: consistent-version cohort, original adapters, native replay.
Run as a module from repo root. Output directory MUST be outside baseline paths.
"""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import pickle
import platform
import subprocess
import sys
import time
import tracemalloc
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def dump(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,indent=2,default=lambda o:o.tolist() if isinstance(o,np.ndarray) else str(o),allow_nan=False)+'\n')

def clean(obj):
 if isinstance(obj,dict):return {str(k):clean(v) for k,v in obj.items()}
 if isinstance(obj,(list,tuple)):return [clean(v) for v in obj]
 if isinstance(obj,(float,np.floating)) and not np.isfinite(obj):return None
 if isinstance(obj,np.integer):return int(obj)
 if isinstance(obj,np.ndarray):return clean(obj.tolist())
 return obj

def prepare(raw, version):
 from agentdojo.task_suite.load_suites import get_suites
 suite=get_suites(version)['banking']
 keep=[]; excluded=collections.Counter(); versions=collections.Counter()
 for entry in raw['episodes']:
  ep=entry['episode'];versions[str(ep.benchmark_version)]+=1
  if ep.user_task_id=='user_task_15':excluded['user_task_15_collision']+=1;continue
  if ep.benchmark_version!=version:excluded['unverified_or_other_version']+=1;continue
  if ep.objective != suite.get_user_task_by_id(ep.user_task_id).PROMPT:
   excluded['prompt_version_conflict']+=1;continue
  keep.append(entry)
 ids={e['episode'].episode_id for e in keep}
 return {'episodes':keep,'steps':[x for x in raw['steps'] if x[1] in ids]}, {'versions':dict(versions),'excluded':dict(excluded),'retained':len(keep)}

def cluster_ci(values,groups,seed,resamples=2000):
 from rem.evaluation.bootstrap import grouped_bootstrap
 return grouped_bootstrap(list(range(len(values))),lambda i:groups[i],lambda ii:float(np.mean(np.asarray(values)[list(ii)])),resamples=resamples,seed=seed)

def summarize(rows,seed):
 names=sorted({r['policy'] for r in rows}); out={}; paired={}
 for name in names:
  rr=[r for r in rows if r['policy']==name]
  ent={}
  for metric,att,group in [('ASR',True,'objective'),('benign_task_success',False,'task'),('utility_under_attack',True,'objective')]:
   xs=[r for r in rr if r['attacked']==att]
   field='security' if metric=='ASR' else 'utility'
   ent[metric]={'n':len(xs),'events':sum(r[field] for r in xs),
      'estimate_ci95':cluster_ci([r[field] for r in xs],[r[group] for r in xs],seed) if xs else None}
  out[name]=ent
 for ref in ['B0','B1','REM_R4','x_act1']:
  lookup={r['episode_id']:r for r in rows if r['policy']==ref}
  pair={}
  for metric,att,field,group in [('ASR',True,'security','objective'),('benign_task_success',False,'utility','task')]:
   xs=[r for r in rows if r['policy']=='AA_REM' and r['attacked']==att]
   values=[int(r[field])-int(lookup[r['episode_id']][field]) for r in xs]
   pair[metric]=cluster_ci(values,[r[group] for r in xs],seed) if xs else None
   if metric=='ASR' and xs:
    pair['ASR_user_task_cluster_sensitivity']=cluster_ci(values,[r['task'] for r in xs],seed)
  paired['AA_REM_minus_'+ref]=pair
 return {'policies':out,'paired_differences':paired}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True,type=Path);ap.add_argument('--out',required=True,type=Path)
 a=ap.parse_args();out=a.out.resolve()
 if out==ROOT/'results' or ROOT/'results' in out.parents:raise ValueError('baseline results protected')
 out.mkdir(parents=True,exist_ok=True)
 os.environ['PILOT_RESULTS_DIR']=str(out/'fit')
 from .baseline_adapters import original,make_baseline
 from .replay_adapter import replay_candidate,OPTIONS
 from .candidate_policy import AuthorizationPolicy
 from .authorization import Contract
 from rem.integration.agentdojo_replay import replay_episode
 from rem.integration.steps import design_matrix
 from rem.algorithms.calibration.logit_nll import LabelNLLLogitCalibrator
 from agentdojo.task_suite.load_suites import get_suites
 protocol=json.loads((HERE/'protocol.json').read_text());seed=protocol['seed']
 raw=pickle.load(a.raw.open('rb'))  # only the locally generated artifact, never arbitrary uploads
 filtered,audit=prepare(raw,'v1.2.1');dump(out/'dataset_audit.json',audit)
 fitdir=out/'fit';fitdir.mkdir(exist_ok=True)
 pickle.dump(filtered,(fitdir/'steps.pkl').open('wb'))
 data=original.build('primary',raw=filtered)
 dump(out/'splits.json',{'task_ids':sorted({s.user_task_id for s in data.steps}),
  'objective_folds':{f:sorted({s.episode_id for s in data.steps if data.episode_fold[s.episode_id]==f}) for f in set(data.fold)},
  'n_steps':len(data.steps),'positives':int(sum(data.y)),
  'no_injection_objective_overlap':all(not (set(data.fold[data.fold==f]) & set(data.fold[data.fold!=f])) for f in set(data.fold))})
 # Same fixed estimator/features/grid/OOF calibration as original; refit only on this version.
 fits={};prob={}
 for name,order in [('label_nll_primary',original.FEATURE_ORDER),('no_ctx',original.features_without(['ctx'])),
                    ('no_beh',original.features_without(['beh'])),('no_act',original.features_without(['act']))]:
  res=original.run_crossfit(data,order,LabelNLLLogitCalibrator)
  fits[name]=res;ok=~np.isnan(res.p_cal)
  prob[name]=clean({'calibrated':original.prob_metrics(data.y[ok],res.p_cal[ok]),
     'raw':original.prob_metrics(data.y,res.p_raw),'calibration_failures':[f for f,ff in res.fits.items() if ff.calibration_failed]})
 original.save_state('crossfit',fits)
 setup=original.make_setup()
 from dataclasses import replace
 setup=replace(setup,suite=get_suites('v1.2.1')['banking'])
 # original helper uses v1 config; explicitly override native replay suite in this adapter.
 original.make_setup=lambda *args,**kwargs:setup
 original.stage_rmod()
 rstate=original.load_state('rmod');rmod=rstate['rmod']
 policies=original.build_policies(fits,rmod)
 refs={f:original.reference_from_mask(data,data.fold!=f) for f in set(data.fold)}
 rows=[];all_details=[];valid=[];invalid=[]
 names=['B0','B1','REM_R4','x_act1',*OPTIONS]
 for eid,ep in data.episodes.items():
  baseline=make_baseline('B0',ep,data,fits,policies,setup,refs)
  b0=replay_episode(ep,setup.suite,baseline)
  if b0.error or (b0.utility,b0.security)!=(ep.utility,ep.security):
   invalid.append({'episode_id':eid,'error':b0.error,'record':[ep.utility,ep.security],'replay':[b0.utility,b0.security]});continue
  valid.append(eid)
  for name in names:
   if name in OPTIONS:result=replay_candidate(ep,setup.suite,name)
   else:
    g=make_baseline(name,ep,data,fits,policies,setup,refs)
    r=replay_episode(ep,setup.suite,g)
    result={'utility':r.utility,'security':r.security,'error':r.error,'audit':r.audit}
   rec={'episode_id':eid,'task':ep.user_task_id,'objective':ep.injection_task_id,'attacked':ep.attacked,
        'policy':name,**{k:result[k] for k in ['utility','security','error']}}
   rows.append(rec);all_details.append({**rec,'audit':result['audit']})
 dump(out/'replay_agreement.json',{'valid':valid,'invalid':invalid,'n':len(data.episodes)})
 dump(out/'episode_outcomes.json',rows);dump(out/'decision_audits.json',clean(all_details))
 dump(out/'replay_metrics.json',clean(summarize(rows,seed)))
 # Offline classifications are interception proxies on legacy attempt labels.
 decisions={n:[] for n in names}; evid=collections.Counter()
 for eid,ep in data.episodes.items():
  pp={n:AuthorizationPolicy(Contract(),**opts) for n,opts in OPTIONS.items()}
  for s in [s for s in data.steps if s.episode_id==eid]:
   fold=data.episode_fold[eid];fit=fits['label_nll_primary']
   i=next(i for i,x in enumerate(data.steps) if x is s)
   for n in names:
    if n in OPTIONS:
     d=pp[n].decide(s.tool,s.args);v=d.verdict.value
     if n=='AA_REM':evid[d.evidence]+=1
    elif n=='B0':v='allow'
    elif n=='x_act1':v='block' if s.features['x_act1'] else 'allow'
    else:
     key='B1' if n=='B1' else 'A3_step_level'
     v=policies[fold][key].decide(float(fit.p_cal[i]),s.tier,s.tool,s.available).verdict.value
    decisions[n].append({'episode':eid,'label':s.label,'verdict':v,'task':s.user_task_id,'objective':s.injection_task_id,'benign':not ep.attacked})
 offline={}
 for n,dd in decisions.items():
  tp=sum(d['label']==1 and d['verdict']!='allow' for d in dd);fn=sum(d['label']==1 and d['verdict']=='allow' for d in dd)
  fp=sum(d['label']==0 and d['verdict']!='allow' for d in dd);tn=sum(d['label']==0 and d['verdict']=='allow' for d in dd)
  ben=[d for d in dd if d['benign']]
  offline[n]={'tp':tp,'fp':fp,'fn':fn,'tn':tn,'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None,
    'false_negative_rate':fn/(tp+fn) if tp+fn else None,'y0_withheld_proxy':fp/(fp+tn) if fp+tn else None,
    'benign_action_approval_proxy':sum(d['verdict']=='allow' for d in ben)/len(ben) if ben else None,
    'benign_explicit_block_proxy':sum(d['verdict']=='block' for d in ben)/len(ben) if ben else None,
    'benign_escalation_proxy':sum(d['verdict']=='escalate' for d in ben)/len(ben) if ben else None,
    'verdicts':dict(collections.Counter(d['verdict'] for d in dd))}
 dump(out/'offline_metrics.json',offline)
 dump(out/'authorization_coverage.json',{'legacy_structured_grants':0,'steps':len(data.steps),'evidence_states':dict(evid),
  'authorization_ground_truth':'unavailable; no true unauthorized-action rate or true authorized-action approval claimed'})
 dump(out/'model_metrics.json',prob)
 # Fixed-rule per-task/objective strata; no training claim for candidate.
 strata={}
 for key in ['task','objective']:
  strata[key]={str(g):clean(summarize([r for r in rows if r[key]==g],seed)) for g in sorted({r[key] for r in rows},key=str)}
 dump(out/'generalization_strata.json',strata)
 # Cost/calibration policy sensitivities on held-out predictions; not efficacy.
 sensitivity={}
 for mult in original.CFG['grid']['C_miss_multiplier']:
  for esc in original.CFG['grid']['C_esc']:
   vv=[]
   for i,s in enumerate(data.steps):
    f=data.fold[i]
    grid=original.build_loss_grid(original.loss_spec(rmod['step_level'][f],mult,esc),'isolated sensitivity')
    p=original.A3Policy(grid,original.predicates(),tie_mode='record_chapter3_order')
    vv.append(p.decide(float(fits['label_nll_primary'].p_cal[i]),s.tier,s.tool,s.available).verdict.value)
   sensitivity[f'miss={mult},escalate={esc}']=dict(collections.Counter(vv))
 for name,pp in [('raw',fits['label_nll_primary'].p_raw),*[(n,fits[n].p_cal) for n in ['no_ctx','no_beh','no_act']]]:
  sensitivity[name]=dict(collections.Counter(policies[data.fold[i]]['A3_step_level'].decide(float(pp[i]),s.tier,s.tool,s.available).verdict.value for i,s in enumerate(data.steps)))
 dump(out/'sensitivity.json',sensitivity)
 # Decision-only microbenchmark: includes policy call, excludes native tools.
 example=data.steps[:min(len(data.steps),300)];lat=[]
 tracemalloc.start();policy=AuthorizationPolicy(Contract())
 for s in example:
  start=time.perf_counter_ns();policy.decide(s.tool,s.args);lat.append((time.perf_counter_ns()-start)/1e6)
 _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 dump(out/'overhead.json',{'calls':len(lat),'latency_instrumented_ms_median':float(np.median(lat)),'latency_instrumented_ms_p95':float(np.quantile(lat,.95)),
   'python_traced_peak_batch_bytes':peak,'scope':'decision-only under tracemalloc; excludes agent/tool execution; not comparable to full original pipeline latency'})
 dump(out/'manifest.json',{'protocol_sha256':hashlib.sha256((HERE/'protocol.json').read_bytes()).hexdigest(),'baseline':protocol['baseline_commit'],
  'python':platform.python_version(),'numpy':np.__version__,'actual_native_suite':'v1.2.1','seed':seed,'evaluation':'NO-ADAPT simulated bank; no live LLM',
  'candidate_source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('*.py')}})
 print(json.dumps(clean(summarize(rows,seed)),indent=2),flush=True)
if __name__=='__main__':main()
