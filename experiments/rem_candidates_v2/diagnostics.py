"""Post-hoc descriptive diagnostics; no new confidence cutoff or policy tuning.
The exact historical password counts refer to the separately reproduced R4 run.
"""
import sys,json,gzip,pickle,collections
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/pilot'))
ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,required=True);ap.add_argument('--results',type=Path,required=True);ap.add_argument('--historical-rmod',type=Path);args=ap.parse_args()
from data import build
from experiments.authorization_generalization.evaluate import prepare
from rem.evaluation.probabilistic import roc_auc,average_precision,brier_binary,expected_calibration_error
import numpy as np
raw=pickle.load(args.raw.open('rb'));filtered,_=prepare(raw,'v1.2.1');d=build(raw=filtered)
steps=collections.defaultdict(list)
for s in d.steps:steps[s.episode_id].append(s)
aud=json.loads(gzip.decompress((args.results/'decision_audits.json.gz').read_bytes()))
by=collections.defaultdict(list);coverage=collections.Counter();truncated=[]
for record in aud:
 if record['grouping']!='injection_task':continue
 if record['policy']=='C4_verified_refund':
  coverage['backend_accesses']+=record['backend_accesses'];coverage['verified_repairs']+=record['verified_repairs']
 if record['policy'] not in {'REM_R4','C1_action_model'}:continue
 ss=steps[record['episode_id']]
 assert len(record['audit'])<=len(ss)
 if len(record['audit'])<len(ss):truncated.append({'episode':record['episode_id'],'policy':record['policy'],'recorded_proposals':len(ss),'evaluated_proposals':len(record['audit'])})
 for s,a in zip(ss,record['audit']):
  assert s.tool==a['tool']
  by[(record['policy'],s.injection_task_id)].append((s.label,a['model_probability'],a['released'],s.tool))
result={}
for (policy,objective),records in by.items():
 y=np.asarray([r[0] for r in records]);p=np.asarray([r[1] for r in records]);wrong=[r[1] for r in records if r[0] and r[2]]
 result.setdefault(policy,{})[str(objective)]={
  'n_steps':len(records),'positive_attempts':int(y.sum()),'positive_attempts_released':len(wrong),
  'released_positive_probability_range':([min(wrong),max(wrong)] if wrong else None),
  'released_positive_probability_median':float(np.median(wrong)) if wrong else None,
  'binary_brier':brier_binary(y,p),'ece_M10':expected_calibration_error(y,p,10),
  'note':'Within-objective prediction diagnostics, not a fitted per-objective calibrator or a human authorization audit.'}
for ep in d.episodes.values():
 from experiments.rem_candidates_v2.refund_policy import parse_refund
 if parse_refund(ep.objective):
  coverage['recognized_episodes']+=1
  coverage['recognized_episodes_with_proposals']+=bool(steps[ep.episode_id])
  coverage['recognized_no_proposal_episodes']+=not bool(steps[ep.episode_id])
result['C4_coverage']=dict(coverage)
result['truncated_native_prefixes']=truncated

if args.historical_rmod:
 historical=pickle.load(args.historical_rmod.open('rb'))
 password_steps=[s for role,eid,ss in raw['steps'] if role=='primary' for s in ss if s.label and s.tool=='update_password']
 result['historical_password_count_verification']={'all_primary_positive_attempts':len(password_steps),'replay_valid_positive_attempts':sum(bool(historical['agree'].get(s.episode_id)) for s in password_steps)}
(args.results/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2)[-800:])
