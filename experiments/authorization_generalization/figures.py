"""Rebuild the standalone security/utility plot from recorded study JSON."""
import argparse
import json
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args()
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 metrics=json.loads(a.results.read_text())['policies'];fig,ax=plt.subplots(figsize=(7,4.5))
 for name,color in [('B0','#64748b'),('B1','#ea580c'),('REM_R4','#2563eb'),('x_act1','#059669'),('AA_REM','#be123c')]:
  d=metrics[name];x=100*d['benign_task_success']['estimate_ci95'][0];y=100*d['ASR']['estimate_ci95'][0]
  ax.scatter(x,y,color=color,s=75);ax.annotate(name,(x,y),xytext=(6,7),textcoords='offset points',fontsize=9)
 ax.set(xlabel='Benign task success (%) — higher is better',ylabel='Native replay ASR (%) — lower is better',
        title='Explicit-version AgentDojo cohort: NO-ADAPT replay',xlim=(20,70),ylim=(-4,65))
 ax.grid(alpha=.2)
 fig.text(.5,.01,'135 attacked / 15 benign episodes; zero structured grants. No live/adaptive security claim.',ha='center',fontsize=8)
 fig.tight_layout(rect=[0,.03,1,1]);a.out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(a.out,dpi=180);plt.close(fig)
if __name__=='__main__':main()
