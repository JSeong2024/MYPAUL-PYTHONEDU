"""Render figures from actual execution outputs, not invented scores."""
from pathlib import Path
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'problems';OUT.mkdir(parents=True,exist_ok=True)
OUTROOT=Path(os.environ.get('PART02_OUT_ROOT',ROOT/'outputs'))

def axbase(title,xlabel,ylabel):
 fig,ax=plt.subplots(figsize=(8,4.3),dpi=150)
 fig.patch.set_facecolor('white');ax.set_title(title,loc='left',fontsize=14,fontweight='bold');ax.set_xlabel(xlabel);ax.set_ylabel(ylabel);ax.grid(alpha=.22)
 return fig,ax

def save(fig,name):
 fig.tight_layout(pad=2);fig.savefig(OUT/name,bbox_inches='tight',facecolor='white');plt.close(fig)

# A-02, validation accuracy and train loss dual axes
h=pd.read_csv(OUTROOT/'A-02'/'training_history.csv');s=json.loads(Path(OUTROOT/'A-02'/'model_selection.json').read_text());fig,ax=axbase('MLP Training History','Epoch','Train Loss');ax.plot(h.epoch,h.train_loss,label='Train Loss');ax2=ax.twinx();ax2.plot(h.epoch,h.validation_accuracy,label='Validation Accuracy',linestyle='--');ax2.set_ylabel('Validation Accuracy');ax.axvline(s['best_epoch'],linestyle=':',alpha=.7,label=f'Best Epoch {s["best_epoch"]}');ax.legend(loc='upper right');ax2.legend(loc='center right');save(fig,'a-02-training-history.png')

h=pd.read_csv(OUTROOT/'A-03'/'training_history.csv');fig,ax=axbase('Optimizer Configuration Comparison','Epoch','Validation RMSE (kWh)')
for name,part in h.groupby('candidate'):ax.plot(part.epoch,part.validation_rmse,label=f'Candidate {name}')
ax.legend();save(fig,'a-03-optimizer-comparison.png')

p=pd.read_csv(OUTROOT/'P-02'/'test_predictions.csv');g=p.grid_id.iloc[0];pts=p[p.grid_id==g];fig,ax=axbase(f'Next-Day Energy Demand · {g}','Date','Energy (kWh)')
ax.plot(pts.date,pts.actual,marker='o',markersize=3,label='Actual');ax.plot(pts.date,pts.baseline_prediction,label='Persistence Baseline',linestyle='--');ax.plot(pts.date,pts.model_prediction,label='MLP Prediction');ax.tick_params(axis='x',rotation=55,labelsize=8);ax.legend();save(fig,'p-02-demand-forecast.png')

p=pd.read_csv(OUTROOT/'P-03'/'comparison.csv');labels=(p.architecture+'/'+p.batch_strategy).tolist();fig,ax=axbase('Validation Performance & Training Time','Configuration','Validation Accuracy')
ax.bar(labels,p.mean_validation_accuracy,width=.52,alpha=.8,label='Mean Validation Accuracy');ax2=ax.twinx();ax2.plot(labels,p.median_seconds,marker='o',label='Median Training Time');ax2.set_ylabel('Median Seconds');ax.set_ylim(0,1);ax.legend(loc='upper left');ax2.legend(loc='upper right');save(fig,'p-03-resource-comparison.png')

h1=pd.read_csv(OUTROOT/'C-01'/'continuous_history.csv');h2=pd.read_csv(OUTROOT/'C-01'/'resumed_history.csv');fig,ax=axbase('Checkpoint Resume Audit','Epoch','Train Loss');ax.plot(h1.epoch,h1.train_loss,label='Continuous',linewidth=2.5);ax.plot(h2.epoch,h2.train_loss,linestyle='--',label='Interrupted + Resumed');ax.axvline(8,linestyle=':',label='Interruption after Epoch 8');ax.legend();save(fig,'c-01-resume-comparison.png')

m=json.loads(Path(OUTROOT/'R-01'/'validation_selection.json').read_text());fig,ax=plt.subplots(figsize=(8,4.3),dpi=150);fig.patch.set_facecolor('white');ax.set_title('Validation-Gated Model Selection',fontsize=14,loc='left',fontweight='bold')
vers=['v1','v2'];xx=np.arange(2);w=.3;f2=[m[v]['classification_f2'] for v in vers];rmse=[m[v]['regression_rmse'] for v in vers]
ax.bar(xx-w/2,f2,w,label='Classification F2');ax.set_ylabel('F2 (higher is better)');ax.set_ylim(0,max(.9,max(f2)*1.22));ax2=ax.twinx();ax2.bar(xx+w/2,rmse,w,alpha=.45,label='Regression RMSE');ax2.set_ylabel('RMSE (kWh, lower is better)');ax.set_xticks(xx,vers);ax.grid(axis='y',alpha=.2);ax.text(.03,.98,'Selected: '+m['selected_version'],transform=ax.transAxes,va='top');ax.legend(loc='upper left',bbox_to_anchor=(0,.89));ax2.legend(loc='upper right',bbox_to_anchor=(1,.89));save(fig,'r-01-deployment-evaluation.png')
print('Created',len(list(OUT.glob('*.png'))),'figures')
