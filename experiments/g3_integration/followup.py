"""Fixed post-scoring value-guard follow-up; earlier outputs are never overwritten."""
import collections,gzip,json,multiprocessing as mp,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import run as J
from value_guard import attach_direct_value_guard

def make_guard(arm,cell,ep,st):
    assert arm=='HV'
    return attach_direct_value_guard(J.V3.make_guard_v3('L4',cell,ep,st))

def replay():
    d=J.data();a=J.load('prepared');st=J.common.make_setup()
    probe={e:J.dataclasses.replace(d.episodes[e],injections={k:v.replace(J.S.ATTACKER_IBAN,J.S.spaced(J.S.ATTACKER_IBAN)) for k,v in d.episodes[e].injections.items()}) for e in a['valid'] if d.episodes[e].attacked and any(J.S.ATTACKER_IBAN in v for v in d.episodes[e].injections.values())}
    eps={'primary':{e:d.episodes[e] for e in a['valid']},'dev2':a['fresh'],'probe':probe}
    fold={'primary':d.episode_fold,'dev2':{e:m['fold'] for e,m in a['meta'].items()},'probe':d.episode_fold}
    J.W.update(setup=st,cells=J.load('cells'),eps=eps,fold=fold);J.guard=make_guard
    jobs=[('S1',r,e,'HV') for r,pop in eps.items() for e in sorted(pop)]+[('S2','primary',e,'HV') for e in a['valid']]
    t=time.time()
    with mp.get_context('fork').Pool(4) as p:rows=p.map(J.replay_job,jobs,chunksize=32)
    J.save('value_replays',rows);print('HV replays',len(rows),'seconds',round(time.time()-t),flush=True)

def report():
    d=J.data();aux=J.load('prepared');by=collections.defaultdict(lambda:collections.defaultdict(dict))
    new=J.load('value_replays')
    for s,r,e,a,u,atk,err,aud in J.load('replays')+new:by[(s,r)][e][a]=(int(u),int(atk),err,aud)
    fresh=aux['fresh'];fv=sorted(e for e,v in by[('S1','dev2')].items() if v['B0'][2] is None and v['B0'][:2]==(fresh[e].utility,fresh[e].security))
    out={'status':'POST-SCORING DEVELOPMENT FOLLOW-UP; known failure-driven repair; no independent validation','protocol_commit':'370cc55','populations':{}}
    for name,scheme,role,ids in [('primary_S1','S1','primary',aux['valid']),('primary_S2','S2','primary',aux['valid']),('dev2','S1','dev2',fv)]:
        B=by[(scheme,role)];episodes=d.episodes if role=='primary' else fresh
        if scheme=='S2':
            for e in ids:B[e]['G3']=by[('S1','primary')][e]['G3'];B[e]['PG']=by[('S1','primary')][e]['PG']
        att=[e for e in ids if episodes[e].attacked];ben=[e for e in ids if not episodes[e].attacked]
        usr=lambda e:episodes[e].user_task_id;inj=lambda e:episodes[e].injection_task_id
        out['populations'][name]={'n_attacked':len(att),'n_benign':len(ben),'arms':J.R.block(B,att,ben,['HV','L4','PG','G3','REM11'],set(J.common.make_setup().restricted)),'contrasts':{'HV minus '+a:J.R.paired(B,att,ben,usr,inj,'HV',a) for a in ['L4','PG','G3','REM11']}}
        print(name,{a:(v['all_tasks_completed'],v['attacks_successful'],v['benign_completed']) for a,v in out['populations'][name]['arms'].items()},flush=True)
    probe=by[('S1','probe')]
    out['probe']={'n':len(probe),'attacks':sum(v['HV'][1] for v in probe.values()),'errors':sum(v['HV'][2] is not None for v in probe.values())}
    J.guard=make_guard;J.ARMS=['HV'];out['fixtures']=J.fixtures(J.load('cells'))
    J.write('value_guard_results.json',out)
    with gzip.open(J.OUT/'value_guard_episode_outcomes.jsonl.gz','wt',encoding='utf-8') as f:
        for s,r,e,a,u,atk,err,aud in new:f.write(json.dumps({'scheme':s,'population':r,'episode_id':e,'arm':a,'utility':u,'security':atk,'error':err})+'\n')
    print('unsafe fixtures',{n:[r['fixture'] for r in a['HV']['rows'] if r['unsafe']] for n,a in out['fixtures'].items()},flush=True)

if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ['replay','report']:raise SystemExit('followup.py replay|report')
    globals()[sys.argv[1]]()
