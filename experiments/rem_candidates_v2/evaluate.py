"""Frozen multi-candidate comparison on reused v1.2.1 development recordings.
This is not an independent final validation set or a live-agent experiment.
"""
import argparse
from collections import Counter,defaultdict
from dataclasses import replace
import gzip
import hashlib
import json
import os
from pathlib import Path
import pickle
import platform
import subprocess
import time
import numpy as np
from experiments.authorization_generalization.evaluate import clean,prepare,cluster_ci
from .runtime import BASELINES,CANDIDATES,ABLATIONS,replay

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def write(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(clean(obj),indent=2,allow_nan=False)+'\n')

def residuals_from_original_replays(data,oracle_replays):
 """Original r_mod estimate, excluding the current test group from outcomes."""
 by=defaultdict(dict)
 for eid,name,u,s,err,aud in oracle_replays:by[eid][name]=(u,s,err,aud)
 result={};membership={}
 for variant in ('step_level','episode_level'):
  pool=[]
  for eid,ep in data.episodes.items():
   b=by[eid]['B0']
   if (b[0],b[1])!=(ep.utility,ep.security) or b[2] is not None:continue
   r=by[eid]['oracle_modify_'+variant]
   if r[2] is not None:raise RuntimeError('oracle replay error')
   mods=[a for a in r[3] if a[1]=='modify']
   if ep.attacked and mods:pool.append((eid,data.episode_fold[eid],mods[0][3],r[1]))
  result[variant]={}
  for f in sorted(set(data.fold),key=str):
   tier_values=defaultdict(list)
   fitting=[]
   for eid,g,k,outcome in pool:
    if g!=f:tier_values[k].append(outcome);fitting.append(eid)
   result[variant][f]={int(k):float(np.mean(v)) for k,v in tier_values.items()}
   membership[variant+'|'+f]=fitting
 return result,membership

def metrics(rows,protocol):
 seed=protocol['bootstrap']['seed'];resamples=protocol['bootstrap']['resamples']
 out={}
 for group in sorted({r['grouping'] for r in rows}):
  rr=[r for r in rows if r['grouping']==group];policies={};paired={}
  for name in sorted({r['policy'] for r in rr}):
   pp=[r for r in rr if r['policy']==name];entry={}
   for metric,att,field,key in [('ASR',True,'security','objective'),('benign_task_success',False,'utility','task'),('utility_under_attack',True,'utility','objective')]:
    xs=[r for r in pp if r['attacked']==att and r['error'] is None]
    entry[metric]={'events':sum(r[field] for r in xs),'n':len(xs),
      'estimate_ci95':cluster_ci([r[field] for r in xs],[r[key] for r in xs],seed,resamples) if xs else None,
      'unavailable':sum(r['attacked']==att and r['error'] is not None for r in pp)}
   policies[name]=entry
  for name in CANDIDATES+ABLATIONS:
   lookup={r['episode_id']:r for r in rr if r['policy']==name}
   if not lookup:continue
   for ref in ('B0','B1','REM_R4','x_act1','AA_REM_previous'):
    pp={r['episode_id']:r for r in rr if r['policy']==ref}
    record={}
    for metric,att,field,key in [('ASR',True,'security','objective'),('benign_task_success',False,'utility','task')]:
     xs=[r for eid,r in lookup.items() if r['attacked']==att and r['error'] is None and pp[eid]['error'] is None]
     values=[int(r[field])-int(pp[r['episode_id']][field]) for r in xs]
     record[metric]={'paired_n':len(xs),'estimate_ci95':cluster_ci(values,[r[key] for r in xs],seed,resamples) if xs else None}
     if att and xs:
      record['ASR_task_cluster_sensitivity']=cluster_ci(values,[r['task'] for r in xs],seed,resamples)
    paired[name+'_minus_'+ref]=record
  # Observed dominance, not a population test or automatic policy selection.
  frontier=[]
  for n,d in policies.items():
   x=d['benign_task_success']['estimate_ci95'];y=d['ASR']['estimate_ci95']
   if x is None or y is None or d['ASR']['unavailable'] or d['benign_task_success']['unavailable']:continue
   dominated=False
   for other,q in policies.items():
    xx=q['benign_task_success']['estimate_ci95'];yy=q['ASR']['estimate_ci95']
    if other==n or xx is None or yy is None:continue
    if xx[0]>=x[0] and yy[0]<=y[0] and (xx[0]>x[0] or yy[0]<y[0]):dominated=True;break
   if not dominated:frontier.append(n)
  out[group]={'policies':policies,'paired_differences':paired,'observed_pareto_frontier':frontier}
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,required=True);ap.add_argument('--oracle-replays',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--complete-trace',action='store_true')
 a=ap.parse_args();out=a.out.resolve()
 if ROOT/'results'==out or ROOT/'results' in out.parents or ROOT/'REM_ALGORITHM_IMPROVEMENT_STUDY'==out or ROOT/'REM_ALGORITHM_IMPROVEMENT_STUDY' in out.parents:
  raise ValueError('original and previous results protected')
 out.mkdir(parents=True,exist_ok=True)
 os.environ['PILOT_RESULTS_DIR']=str(out/'temporary_pilot_state')
 from experiments.authorization_generalization.baseline_adapters import original
 from rem.algorithms.calibration.logit_nll import LabelNLLLogitCalibrator
 from agentdojo.task_suite.load_suites import get_suites
 raw=pickle.load(a.raw.open('rb'));filtered,audit=prepare(raw,'v1.2.1')
 # The public argument expects a locally generated original native-replay artifact.
 oracle=pickle.load(a.oracle_replays.open('rb'))
 protocol=json.loads((HERE/'protocol.json').read_text())
 write(out/'dataset_audit.json',audit)
 setup=replace(original.make_setup(),suite=get_suites('v1.2.1')['banking'])
 rows=[];details=[];fits_manifest={};splits={};agreed=None;fixed_outcomes={};timings={};count_native=0;horizon_mismatches=[]
 names=BASELINES+CANDIDATES+ABLATIONS
 for grouping in ('injection_task','user_task'):
  start=time.perf_counter()
  data=original.build(raw=filtered,grouping=grouping)
  fits={};model_metrics={}
  for model,order in [('full',original.FEATURE_ORDER),('action_only',original.features_without(['ctx','beh']))]:
   result=original.run_crossfit(data,order,LabelNLLLogitCalibrator)
   fits[model]=(result,tuple(order))
   ok=~np.isnan(result.p_cal)
   model_metrics[model]={'available_steps':int(ok.sum()),'total_steps':len(data.steps),
      'calibrated':original.prob_metrics(data.y[ok],result.p_cal[ok]),
      'raw':original.prob_metrics(data.y,result.p_raw),
      'folds':{str(k):{'lambda':v.lam,'calibration_failed':v.calibration_failed,'gamma_0':v.gamma_0,'gamma_1':v.gamma_1,'coefficients':v.coefficients,'intercept':v.intercept,'features':order,'n_train':v.n_train,'n_test':v.n_test} for k,v in result.fits.items()}}
  rmod,membership=residuals_from_original_replays(data,oracle)
  policies=original.build_policies({'label_nll_primary':fits['full'][0]},rmod)
  refs={f:original.reference_from_mask(data,data.fold!=f) for f in set(data.fold)}
  splits[grouping]={}
  for f in sorted(set(data.fold),key=str):
   train=[s for s in data.steps if data.episode_fold[s.episode_id]!=f]
   test=[s for s in data.steps if data.episode_fold[s.episode_id]==f]
   train_eps=sorted({s.episode_id for s in train});test_eps=sorted({s.episode_id for s in test})
   if set(train_eps)&set(test_eps):raise AssertionError('episode leakage')
   if grouping=='user_task' and {s.user_task_id for s in train}&{s.user_task_id for s in test}:raise AssertionError('task leakage')
   if grouping=='injection_task' and ({s.injection_task_id for s in train if s.injection_task_id}&{s.injection_task_id for s in test if s.injection_task_id}):raise AssertionError('objective leakage')
   if set(membership['step_level|'+f])&set(test_eps):raise AssertionError('residual-outcome leakage')
   splits[grouping][f]={'fit_episodes':train_eps,'test_episodes':test_eps,'residual_fit_episodes':membership['step_level|'+f]}
  fits_manifest[grouping]=model_metrics
  for eid,ep in data.episodes.items():
   f=data.episode_fold[eid]
   if agreed is not None and eid not in agreed:continue
   for name in names:
    if grouping=='user_task' and name not in {'B1','REM_R4','C1_action_model'}:
     rec,aud=fixed_outcomes[(eid,name)]
     rows.append({**rec,'grouping':grouping,'reused_fixed_policy_run':True})
     continue
    score=None;dp=None
    if name in {'B1','REM_R4','C1_action_model'}:
     fitted,order=fits['action_only' if name=='C1_action_model' else 'full']
     ff=fitted.fits.get(f)
     if ff is None and not any(m.tool_calls for m in ep.messages):
      # Terminal episodes have no supervised step/fold and never invoke a policy.
      result=replay(ep,setup.suite,name,setup,None,complete_trace=a.complete_trace);count_native+=1
     elif ff is None:
      raise RuntimeError('missing fit for an episode containing proposals')
     elif ff.calibration_failed:
      result={'utility':False,'security':False,'error':'unavailable_calibrated_fold','audit':[],'backend_accesses':0}
     else:
      score=original.scorer_of(ff,order)
      dp=policies[f]['B1' if name=='B1' else 'A3_step_level']
      result=replay(ep,setup.suite,name,setup,refs[f],scorer=score,decision_policy=dp,complete_trace=a.complete_trace);count_native+=1
    else:
     result=replay(ep,setup.suite,name,setup,refs[f],complete_trace=a.complete_trace);count_native+=1
    if grouping=='injection_task' and name=='B0' and (result['error'] or (result['utility'],result['security'])!=(ep.utility,ep.security)):
     if a.complete_trace:
      horizon_mismatches.append({'episode_id':eid,'recorded':[ep.utility,ep.security],'full_trace':[result['utility'],result['security']]})
     else:raise RuntimeError('B0 native outcome mismatch; do not silently change comparison cohort')
    if result['error'] is not None and result['error']!='unavailable_calibrated_fold':
     raise RuntimeError(f'native replay error for {name}: {result["error"]}')
    rec={'grouping':grouping,'policy':name,'episode_id':eid,'task':ep.user_task_id,'objective':ep.injection_task_id,'attacked':ep.attacked,
       **{k:result[k] for k in ('utility','security','error','backend_accesses')},
       'verified_repairs':sum(x['verified_repair'] for x in result['audit']),'reused_fixed_policy_run':False}
    rows.append(rec);details.append({**rec,'audit':result['audit']})
    if grouping=='injection_task':fixed_outcomes[(eid,name)]=(rec,result['audit'])
  if grouping=='injection_task':agreed=set(data.episodes)
  timings[grouping]=time.perf_counter()-start
  print(grouping,'replay complete',len(data.episodes),timings[grouping],flush=True)
  write(out/'episode_outcomes.json',rows)
  write(out/'model_metrics.json',fits_manifest)
 write(out/'splits.json',splits)
 (out/'decision_audits.json.gz').write_bytes(gzip.compress(json.dumps(clean(details)).encode(),mtime=0))
 result_metrics=metrics(rows,protocol)
 write(out/'metrics.json',result_metrics)
 strata={}
 for key in ('task','objective'):
  strata[key]={}
  for g in sorted({r[key] for r in rows},key=str):
   rr=[r for r in rows if r[key]==g and r['grouping']=='injection_task']
   strata[key][str(g)]={n:{'episodes':sum(r['policy']==n for r in rr),'security_events':sum(r['security'] for r in rr if r['policy']==n),'utility_events':sum(r['utility'] for r in rr if r['policy']==n)} for n in names}
 write(out/'strata.json',strata)
 write(out/'manifest.json',{'study_protocol_sha256':hashlib.sha256((HERE/'protocol.json').read_bytes()).hexdigest(),
    'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('*.py')},
    'raw_sha256':hashlib.sha256(a.raw.read_bytes()).hexdigest(),'oracle_replays_sha256':hashlib.sha256(a.oracle_replays.read_bytes()).hexdigest(),
    'python':platform.python_version(),'numpy':np.__version__,'native_replays_executed':count_native,
    'complete_trace':a.complete_trace,'B0_horizon_outcome_mismatches':horizon_mismatches,'distinct_episodes':len(agreed),'timings_seconds':timings,'data_exposure':'previously examined development recordings, no independent final validation',
    'backend_trust_assumption':'C4 receives current native ledger financial fields via narrow independent host adapter; not task solutions or clean pre-injection state'})
 for group,value in result_metrics.items():
  print(group,{n:{k:v['estimate_ci95'][0] if v['estimate_ci95'] else None for k,v in m.items()} for n,m in value['policies'].items()},flush=True)
if __name__=='__main__':main()
