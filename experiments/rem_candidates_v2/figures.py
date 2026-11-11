"""Standalone figure from archived comparison JSON; no fitted score changes."""
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--metrics',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 metrics=json.loads(a.metrics.read_text())
 names=['B0','B1','REM_R4','x_act1','AA_REM_previous','C1_action_model','C2_canonical_provenance','C3_target_only','C4_verified_refund']
 labels=['B0','B1','REM','x_act1','AA prev.','C1','C2','C3*','C4**'];x=np.arange(len(names));fig,axes=plt.subplots(1,2,figsize=(12,4.8))
 for ax,metric,title in zip(axes,['ASR','benign_task_success'],['Native replay attack success (lower is better)','Benign task success (higher is better)']):
  for delta,g,color,label in [(-.18,'injection_task','#2563eb','Held-out attack objective'),(.18,'user_task','#d97706','Held-out user task')]:
   y=[metrics[g]['policies'][n][metric]['estimate_ci95'][0]*100 for n in names]
   bars=ax.bar(x+delta,y,.34,color=color,label=label)
   ax.bar_label(bars,fmt='%.1f',fontsize=7,padding=2 if delta<0 else 12)
  ax.set_xticks(x,labels,rotation=30,ha='right');ax.set_title(title,fontsize=10);ax.set_ylabel('Percent');ax.set_ylim(0,72);ax.grid(axis='y',alpha=.15)
 axes[0].legend(fontsize=8)
 fig.suptitle('Four REM candidates — previously examined development recordings',fontsize=12)
 fig.text(.5,.01,'Same 135 attacked / 15 benign episodes. * C3 fails amount-only stress. ** C4 verification has zero benchmark coverage. NO-ADAPT.',ha='center',fontsize=8)
 fig.tight_layout(rect=[0,.045,1,.95]);a.out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(a.out,dpi=180);plt.close(fig)
if __name__=='__main__':main()
