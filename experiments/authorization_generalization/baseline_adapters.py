"""Reuse the original pilot policies and fold states without altering their code."""
import sys
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'experiments/pilot'))
import run_main as original
from rem.core.results import Verdict
from rem.integration.agentdojo_replay import RemGuard, GuardConfig

class ProvenanceGuard(RemGuard):
    def evaluate(self,tool,args):
        # Extract before parent records the proposal; label is never read.
        feats,_=self.tracker.features(tool,args)
        value=feats['x_act1']
        self.decide=lambda ctx: (Verdict.BLOCK if value else Verdict.ALLOW,'x_act1_rule',{})
        return super().evaluate(tool,args)

def make_baseline(name, ep, data, fits, policies, setup, refs):
    fold=data.episode_fold[ep.episode_id]
    gc=GuardConfig(setup.spec,setup.detector,refs[fold],setup.tier_map,setup.restricted,'step_level','no_reviewer')
    if name=='B0':
        return RemGuard(gc,None,lambda ctx:(Verdict.ALLOW,'allow_all',{}),setup.labeler,ep)
    if name=='x_act1':
        return ProvenanceGuard(gc,None,lambda ctx:None,setup.labeler,ep)
    policy=policies[fold]['B1' if name=='B1' else 'A3_step_level']
    def decide(ctx):
        d=policy.decide(ctx.p,ctx.tier,ctx.tool,ctx.available)
        return d.verdict,d.source,{'tie':getattr(d,'tie',False)}
    scorer=original.scorer_of(fits['label_nll_primary'].fits[fold],original.FEATURE_ORDER)
    return RemGuard(gc,scorer,decide,setup.labeler,ep)
