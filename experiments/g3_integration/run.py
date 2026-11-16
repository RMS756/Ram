"""Reproduce baseline fits, compose G3 with REM, replay, and report.

Stages: prepare, fit, replay, report. No model API calls. See frozen PROTOCOL.md.
Environment: AGENTDOJO_RUNS, PILOT_RESULTS_DIR, INTEGRATION_STATE, PROGENT_UPSTREAM.
"""
from __future__ import annotations
import collections, dataclasses, gzip, hashlib, json, multiprocessing as mp, os, pickle, sys, time
from pathlib import Path
from types import SimpleNamespace
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/improve_study'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import improve as I
import improve_v3 as V3
import report as R
from permission_v3 import PERM3_ORDER,offline_permission_v3
from guard import attach_permission_gate
from rem.integration.agentdojo_replay import FrozenScorer,GuardConfig,RemGuard
from rem.core.results import Verdict
from rem.algorithms.a3 import A3Policy
from rem.algorithms.decision.loss_matrix import build_loss_grid
S=I.S; common=I.common
STATE=Path(os.environ['INTEGRATION_STATE']);STATE.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'REM_G3_INTEGRATION';OUT.mkdir(exist_ok=True)
ARMS=['B0','REM10','REM11','G3','L4','H10','H11','H11D','HR','A2','PG']
LEARN=['REM10','REM11','L4','H10','H11','H11D','HR']
FIXED=[('H10','REM10'),('H11','REM11'),('H11D','REM11'),('H10','G3'),('H11','G3'),('H11D','G3'),('L4','G3'),('L4','H11D'),('G3','A2'),('G3','PG'),('HR','G3'),('HR','L4')]+[(a,'PG') for a in ['H10','H11','H11D','L4','HR']]
W={}

def save(n,x):
    with (STATE/(n+'.pkl')).open('wb') as f:pickle.dump(x,f)
def load(n):
    with (STATE/(n+'.pkl')).open('rb') as f:return pickle.load(f)
def write(n,x):
    (OUT/n).write_text(json.dumps(x,indent=1,default=common._default),encoding='utf-8')
def digest(items):return hashlib.sha256('\n'.join(sorted(items)).encode()).hexdigest()
def data():return I.build('primary',I.load_raw())

def stage_prepare():
    st=common.make_setup();d=data()
    folds=sorted(set(d.fold.tolist()),key=str)
    from data import reference_from_mask
    refs={f:reference_from_mask(d,d.fold!=f) for f in folds}
    cfg={'B0':{'variant':'step_level','esc':'no_reviewer','decide':S.rm._decide_allow},'oracle_modify_step_level':{'variant':'step_level','esc':'no_reviewer','decide':S.rm._decide_oracle_modify}}
    records=S.rm.run_replays(cfg,sorted(d.episodes),st,d,refs)
    by=collections.defaultdict(dict)
    for e,a,u,s,err,aud in records:by[e][a]=(bool(u),bool(s),err,aud)
    valid=sorted(e for e,v in by.items() if v['B0'][2] is None and v['B0'][:2]==(d.episodes[e].utility,d.episodes[e].security))
    manifest=json.loads((ROOT/'REM_IMPROVEMENT_STUDY/protocol/SPLIT_MANIFEST.json').read_text())
    assert len(valid)==manifest['primary']['eligible'] and digest(valid)==manifest['primary']['eligible_ids_sha256']
    assert len(d.steps)==manifest['primary']['steps']
    rows=[]
    for e in valid:
        ep=d.episodes[e];v=by[e]['oracle_modify_step_level']
        modified=[a for a in v[3] if a[1]=='modify']
        if ep.attacked and modified:rows.append((ep.user_task_id,ep.injection_task_id,modified[0][3],v[1]))
    fresh,meta=I.load_fresh(st,d)
    assert len(fresh)==manifest['dev2_formerly_confirmatory']['episodes_loaded']
    assert digest(fresh)==manifest['dev2_formerly_confirmatory']['loaded_ids_sha256']
    aux={'valid':valid,'rmod_rows':rows,'fresh':fresh,'meta':meta,'baseline':by}
    save('prepared',aux)
    print('prepared',len(valid),'eligible primary;',len(fresh),'loaded second',flush=True)

def fit_job(key):
    d=W['data'];kind=key[0]
    train=(d.fold!=key[1]) if kind=='S1' else ((W['ut']!=key[1])&(W['it']!=key[2]))
    cell,X=S.fit_cell(train,['F0','F0_nobeh','F4'],('y',))
    rows=[(k,sec) for u,i,k,sec in W['rows'] if (i!=key[1] if kind=='S1' else u!=key[1] and i!=key[2])]
    cell['rmod']={k:float(np.mean([s for kk,s in rows if kk==k])) for k in {k for k,_ in rows}}
    for rec in cell['models'].values():
        cols=[S.ALL_ORDER.index(f) for f in rec['order']]
        rec['xbar']=[float(x) for x in X[train][:,cols].mean(axis=0)]
    return key,cell

def stage_fit():
    st=common.make_setup();d=data();aux=load('prepared')
    S.ALL_ORDER=tuple(I.FEATURE_ORDER)+tuple(PERM3_ORDER)
    S.FEATURE_SETS['F4']=I.NOBEH+tuple(PERM3_ORDER)
    Z=np.zeros((len(d.steps),len(PERM3_ORDER)));groups=collections.defaultdict(list)
    for i,s in enumerate(d.steps):groups[s.episode_id].append((s.index,i))
    for e,g in groups.items():
        idx=[i for _,i in sorted(g)];tiers=iter(d.steps[i].tier for i in idx)
        ev=offline_permission_v3(d.episodes[e],lambda tool,args:next(tiers))
        assert len(ev)==len(idx)
        for i,v in zip(idx,ev):Z[i]=[v.features()[f] for f in PERM3_ORDER]
    ut=np.array([s.user_task_id for s in d.steps],dtype=object)
    it=np.array([s.injection_task_id or 'none' for s in d.steps],dtype=object)
    S.G.update(data=d,Z=Z,T={'y':d.y.copy()});W.update(data=d,ut=ut,it=it,rows=aux['rmod_rows'])
    s2={('S2',d.episodes[e].user_task_id,d.episodes[e].injection_task_id or d.episode_fold[e]) for e in aux['valid']}
    jobs=[('S1',f) for f in sorted(set(d.fold.tolist()),key=str)]+sorted(s2)
    t=time.time()
    with mp.get_context('fork').Pool(4) as p:cells=dict(p.map(fit_job,jobs,chunksize=2))
    old=json.loads((ROOT/'results/pilot/e1_crossfit.json').read_text())['label_nll_primary']['per_fold']
    differences=[]
    for f,v in old.items():
        rec=cells[('S1',f)]['models'][('F0','y')]
        differences += [abs(rec['b0']-v['intercept']),abs(rec['g0']-v['gamma_0']),abs(rec['g1']-v['gamma_1'])]
        differences += [abs(c-v['coefficients'][n]) for n,c in zip(rec['order'],rec['coef'])]
    mx=max(differences);assert mx<1e-8,('baseline refit mismatch',mx)
    save('cells',cells)
    write('fits.json',{'cells':[{'key':key,'models':{fs:rec for (fs,target),rec in c['models'].items()},'rmod':c['rmod']} for key,c in cells.items()],'original_S1_F0_max_abs_difference':mx})
    print('fit',len(cells),'cells',round(time.time()-t,1),'seconds; original F0 max difference',mx,flush=True)

def core_guard(arm,cell,ep,st):
    fs='F4' if arm=='HR' else ('F0' if arm in ('REM10','H10') else 'F0_nobeh');rec=cell['models'][(fs,'y')]
    scorer=FrozenScorer(tuple(rec['order']),rec['b0'],tuple(rec['coef']),rec['g0'],rec['g1'],tuple(rec['xbar']))
    gc=GuardConfig(st.spec,st.detector,cell['reference'],st.tier_map,st.restricted,'step_level','no_reviewer')
    policy=A3Policy(build_loss_grid(S.rm.loss_spec(cell['rmod']),'REM + G3 experiment'),S.rm.predicates(),tie_mode='record_chapter3_order',exclude_from_expected_loss=(Verdict.ESCALATE,Verdict.MODIFY) if arm in ('H11D','HR') else ())
    def decide(c):
        v=policy.decide(c.p,c.tier,c.tool,c.available)
        return v.verdict,v.source,{'risks':dict(v.risks),'tie':v.tie,'feasible':v.feasible}
    g=RemGuard(gc,scorer,decide,st.labeler,ep)
    return attach_permission_gate(g,mode='routed',predicates=S.rm.predicates()) if arm=='HR' else (attach_permission_gate(g) if arm.startswith('H') else g)

def guard(arm,cell,ep,st):
    if arm in ('G3','L4'):return V3.make_guard_v3(arm,cell,ep,st)
    if arm in ('B0','A2','PG'):return I.make_guard(arm,cell,ep,st)
    return core_guard(arm,cell,ep,st)

def replay_job(job):
    scheme,role,e,arm=job;ep=W['eps'][role][e]
    key=('S1',W['fold'][role][e]) if scheme=='S1' else ('S2',ep.user_task_id,ep.injection_task_id or W['fold'][role][e])
    out=S.replay_episode(ep,W['setup'].suite,guard(arm,W['cells'][key],ep,W['setup']))
    audit=[(a['label'],a['verdict'],bool(a['released']),a['tier'],a['tool'],a['rem_latency_full_ms'],a['verdict_source'],a['details'].get('permission') or a['details'].get('perm')) for a in out.audit]
    return scheme,role,e,arm,bool(out.utility),bool(out.security),out.error,audit

def stage_replay():
    d=data();aux=load('prepared');st=common.make_setup();I.PG.load()
    probe={e:dataclasses.replace(d.episodes[e],injections={k:v.replace(S.ATTACKER_IBAN,S.spaced(S.ATTACKER_IBAN)) for k,v in d.episodes[e].injections.items()}) for e in aux['valid'] if d.episodes[e].attacked and any(S.ATTACKER_IBAN in v for v in d.episodes[e].injections.values())}
    eps={'primary':{e:d.episodes[e] for e in aux['valid']},'dev2':aux['fresh'],'probe':probe}
    folds={'primary':d.episode_fold,'dev2':{e:m['fold'] for e,m in aux['meta'].items()},'probe':d.episode_fold}
    W.update(setup=st,cells=load('cells'),eps=eps,fold=folds)
    jobs=[('S1',role,e,a) for role,pop in eps.items() for a in ARMS for e in sorted(pop)]
    jobs += [('S2','primary',e,a) for a in LEARN for e in aux['valid']]
    t=time.time();results=[]
    with mp.get_context('fork').Pool(4) as p:
        for i,v in enumerate(p.imap_unordered(replay_job,jobs,chunksize=32),1):
            results.append(v)
            if i%4000==0:print('replay',i,'/',len(jobs),'elapsed',round(time.time()-t),'s',flush=True)
    save('replays',results);print('replay done',len(results),round(time.time()-t),flush=True)

def stage_report():
    d=data();aux=load('prepared');rows=load('replays');by=collections.defaultdict(lambda:collections.defaultdict(dict))
    for scheme,role,e,a,u,s,err,aud in rows:by[(scheme,role)][e][a]=(int(u),int(s),err,aud)
    second=by[('S1','dev2')];meta=aux['meta'];fresh=aux['fresh']
    fv=sorted(e for e,v in second.items() if v['B0'][2] is None and v['B0'][:2]==(fresh[e].utility,fresh[e].security))
    assert len(fv)==2113
    pops={}
    for name,scheme,role,ids in [('primary_S1','S1','primary',aux['valid']),('primary_S2','S2','primary',aux['valid']),('dev2','S1','dev2',fv)]:
        B=by[(scheme,role)]
        if scheme=='S2':
            for e in ids:
                for a in ARMS:
                    if a not in B[e]:B[e][a]=by[('S1','primary')][e][a]
        episodes=d.episodes if role=='primary' else fresh
        att=[e for e in ids if episodes[e].attacked];ben=[e for e in ids if not episodes[e].attacked]
        usr=lambda e:episodes[e].user_task_id;inj=lambda e:episodes[e].injection_task_id
        mm=R.block(B,att,ben,ARMS,set(common.make_setup().restricted))
        pops[name]={'n_attacked':len(att),'n_benign':len(ben),'arms':mm,'contrasts':{a+' minus '+b:R.paired(B,att,ben,usr,inj,a,b) for a,b in FIXED},'completion_by_user':{a:{u:sum(B[e][a][0] for e in ids if usr(e)==u) for u in sorted({usr(e) for e in ids})} for a in ARMS},'attacks_by_user':{a:dict(collections.Counter(usr(e) for e in att if B[e][a][1])) for a in ARMS},'without_user_task_15':{a:{'attacks':sum(B[e][a][1] for e in att if usr(e)!='user_task_15'),'tasks':sum(B[e][a][0] for e in ids if usr(e)!='user_task_15')} for a in ARMS}}
        print(name,[(a,m['attacks_successful'],m['benign_completed'],m['all_tasks_completed']) for a,m in mm.items()],flush=True)
    old=json.loads((ROOT/'REM_IMPROVEMENT_STUDY/followup_v3/results_v3.json').read_text())['populations']
    mapping={'REM10':'M00','REM11':'M00_nobeh','G3':'G3','L4':'L4','A2':'A2','PG':'PG'};eq={}
    for name,p in pops.items():
        eq[name]={}
        for a,old_a in mapping.items():
            eq[name][a]={k:p['arms'][a][k]-old[name]['arms'][old_a][k] for k in ['attacks_successful','benign_completed','all_tasks_completed']}
    probe=by[('S1','probe')]
    out={'status':'EXPLORATORY DEVELOPMENT: offline recorded-trace replay; no live agent or model API','protocol_commits':['0ff1cea','cafc41c','394fccc'],'populations':pops,'reference_reproduction_differences':eq,'probe':{'n':len(probe),'arms':{a:{'attacks':sum(v[a][1] for v in probe.values()),'replay_errors':sum(v[a][2] is not None for v in probe.values())} for a in ARMS}},'fixtures':fixtures(load('cells'))}
    write('results.json',out)
    with gzip.open(OUT/'episode_outcomes.jsonl.gz','wt',encoding='utf-8') as f:
        for scheme,role,e,a,u,s,err,aud in sorted(rows,key=lambda z:z[:4]):f.write(json.dumps({'scheme':scheme,'population':role,'episode_id':e,'arm':a,'utility':u,'security':s,'error':err})+'\n')
    assert all(v==0 for pop in eq.values() for a in pop.values() for v in a.values()),eq
    print('all old arm aggregate outcomes reproduced exactly',flush=True)

def fixtures(cells):
    sys.path.insert(0,str(ROOT/'REM_AUTHORIZATION_AUDIT/tools'));import trace_fixtures as tf
    st=common.make_setup();cell=cells[('S1','injection_task_0')];result={}
    paths=['REM_AUTHORIZATION_AUDIT/fixtures/set1_substitution_fixtures.json','REM_AUTHORIZATION_AUDIT/fixtures/set2_fresh_fixtures.json','REM_FINAL_SUBMISSION/fixtures/set3_credential_and_reformatting_fixtures.json','REM_IMPROVEMENT_STUDY/fixtures/set4_permission_fixtures.json']
    for path in paths:
        v=json.loads((ROOT/path).read_text());records=v['records'] if isinstance(v,dict) else v
        summary={}
        for a in ARMS:
            rr=[]
            for fx in records:
                if 'authorized' in fx:
                    fx['legitimate_call']={'tool':'send_money','args':dict(fx['authorized'])};fx['unsafe_call']={'tool':'send_money','args':dict(fx['substituted'])}
                hist=fx.get('history') or [{'tool':'read_file','args':{'file_path':'document.txt'},'output':fx['tool_output'],'executed':True}]
                pair={}
                for role in ['legitimate','unsafe']:
                    ep=SimpleNamespace(objective=fx['objective'],system_prompt=tf.SYSTEM_PROMPT,injection_task_id=None,episode_id='fixture')
                    g=guard(a,cell,ep,st)
                    for h in hist:
                        g.begin_decision_point();g.evaluate(h['tool'],dict(h['args']));g.ingest(h['tool'],h['output'],executed=g.audit[-1]['released'] and h.get('executed',True))
                    g.begin_decision_point();g.evaluate(fx[role+'_call']['tool'],dict(fx[role+'_call']['args']));pair[role]=bool(g.audit[-1]['released'])
                rr.append({'fixture':fx['id'],**pair})
            summary[a]={'n':len(rr),'legitimate_released':sum(r['legitimate'] for r in rr),'unsafe_released':sum(r['unsafe'] for r in rr),'pairs_correct':sum(r['legitimate'] and not r['unsafe'] for r in rr),'rows':rr}
        result[Path(path).stem]=summary
    return result

if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ('prepare','fit','replay','report'):raise SystemExit('Usage: run.py prepare|fit|replay|report')
    globals()['stage_'+sys.argv[1]]()
