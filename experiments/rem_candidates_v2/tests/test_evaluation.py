"""Integration checks on actual generated study artifacts; no invented scores."""
import json
import os
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[3]
RESULTS=Path(os.environ.get('REM_V2_RESULTS','/workspace/work/v2_eval_final'))

def result(name):
 p=RESULTS/name
 if not p.exists():pytest.skip('run v2 evaluation to generate integration artifacts')
 return json.loads(p.read_text())

def test_actual_split_membership_excludes_episode_and_task_or_objective():
 splits=result('splits.json')
 for grouping,folds in splits.items():
  for name,fold in folds.items():
   train=set(fold['fit_episodes']);test=set(fold['test_episodes'])
   assert not train&test
   assert not set(fold['residual_fit_episodes'])&test
   field=1 if grouping=='user_task' else 2
   tr={e.split('|')[field] for e in train};te={e.split('|')[field] for e in test}
   if grouping=='injection_task':tr.discard('none');te.discard('none')
   assert not tr&te

def test_all_replay_rows_have_outcomes_and_reused_runs_not_new_samples():
 rows=result('episode_outcomes.json');manifest=result('manifest.json')
 assert len(rows)==3900
 assert len({r['episode_id'] for r in rows})==150
 assert not any(r['error'] for r in rows)
 assert sum(not r['reused_fixed_policy_run'] for r in rows)==manifest['native_replays_executed']==2400
 assert sum(r['reused_fixed_policy_run'] for r in rows)==1500
 for g in ('injection_task','user_task'):
  for policy in {r['policy'] for r in rows}:
   subset=[r for r in rows if r['grouping']==g and r['policy']==policy]
   assert len(subset)==150 and sum(r['attacked'] for r in subset)==135

def test_unchanged_primary_controls_reproduce_previous_native_outcomes():
 rows=result('episode_outcomes.json')
 prior=json.loads((ROOT/'REM_ALGORITHM_IMPROVEMENT_STUDY/artifacts/episode_outcomes.json').read_text())
 old={(r['episode_id'],r['policy']):(r['utility'],r['security']) for r in prior}
 for r in rows:
  if r['grouping']!='injection_task' or r['policy'] not in {'B0','B1','REM_R4','x_act1','AA_REM_previous'}:continue
  name='AA_REM' if r['policy']=='AA_REM_previous' else r['policy']
  assert (r['utility'],r['security'])==old[(r['episode_id'],name)]

def test_reported_events_recomputed_from_raw_outcomes():
 rows=result('episode_outcomes.json');metrics=result('metrics.json')
 for g,entry in metrics.items():
  for p,values in entry['policies'].items():
   for name,attack,key in [('ASR',True,'security'),('benign_task_success',False,'utility'),('utility_under_attack',True,'utility')]:
    xs=[r for r in rows if r['grouping']==g and r['policy']==p and r['attacked']==attack]
    assert values[name]['n']==len(xs)
    assert values[name]['events']==sum(r[key] for r in xs)
