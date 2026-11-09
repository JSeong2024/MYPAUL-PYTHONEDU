"""모범 구현의 실제 실행 결과를 바탕으로 Chapter 07 그림 생성."""
from __future__ import annotations
from pathlib import Path
import sys
import tempfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from solutions import (mini_01_optimizer_comparison as m1,
                       mini_02_learning_rate_scheduler as m2,
                       advanced_01_generalization_clinic as a1,
                       advanced_02_gradient_audit as a2,
                       advanced_03_checkpoint_resume as a3,
                       professional_01_fleet_training as p1)

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures';FIG.mkdir(parents=True,exist_ok=True)
plt.rcParams['font.size']=10
plt.rcParams['figure.dpi']=125

def finish(name,ax):
    ax.grid(alpha=.25);ax.legend(loc='best',fontsize=9)
    ax.figure.tight_layout()
    ax.figure.savefig(FIG/name,bbox_inches='tight',dpi=145)
    plt.close(ax.figure)

def generate():
    _,history,_=m1.run()
    fig,ax=plt.subplots(figsize=(9,4.5))
    for name,group in history.groupby('model'):
        ax.plot(group.epoch,group.validation_loss,label=f'{name} · Validation')
        ax.plot(group.epoch,group.train_loss,linestyle='--',alpha=.7,label=f'{name} · Train')
    ax.set(title='Optimizer Comparison · Scaled MSE',xlabel='Epoch',ylabel='MSE')
    finish('mini_01_optimizer_curves.png',ax)

    _,history=m2.run()
    fig,(ax1,ax2)=plt.subplots(2,1,sharex=True,figsize=(9,6.4))
    for name,group in history.groupby('schedule'):
        ax1.plot(group.epoch,group.validation_loss,label=f'{name} · Validation')
        ax2.step(group.epoch,group.learning_rate,where='mid',label=name)
    ax1.set(title='Fixed Learning Rate vs StepLR',ylabel='Validation BCE')
    ax2.set(xlabel='Epoch',ylabel='Learning Rate')
    ax1.grid(alpha=.25);ax2.grid(alpha=.25)
    ax1.legend();ax2.legend();fig.tight_layout()
    fig.savefig(FIG/'mini_02_scheduler_curves.png',bbox_inches='tight',dpi=145);plt.close(fig)

    _,history,_=a1.run()
    fig,ax=plt.subplots(figsize=(9,4.5))
    for name,group in history.groupby('variant'):
        ax.plot(group.epoch,group.validation_loss,label=f'{name} · Validation')
        ax.plot(group.epoch,group.train_loss,linestyle='--',alpha=.7,label=f'{name} · Train')
    ax.set(title='Generalization Clinic · Learning Curves',xlabel='Epoch',ylabel='Scaled MSE')
    finish('advanced_01_generalization_curves.png',ax)

    report,_=a2.run()
    fig,ax=plt.subplots(figsize=(7,4))
    labels=['Before clipping','After clipping']
    values=[report['gradient_norm_before_clip'],report['gradient_norm_after_clip']]
    ax.bar(labels,values,width=.55)
    ax.axhline(report['clip_max_norm'],color='gray',linestyle='--',label='max_norm=0.3')
    ax.set(title=f'Micro-Batch Difference: {report["max_gradient_difference"]:.2e}',ylabel='Gradient L2 norm')
    finish('advanced_02_gradient_norm.png',ax)

    _,history=a3.run()
    fig,ax=plt.subplots(figsize=(9,4.5))
    for name,group in history.groupby('run'):
        ax.plot(group.epoch,group.validation_loss,'o-',label=name,alpha=.75)
    ax.axvline(5,color='gray',linestyle='--',label='Checkpoint saved at Epoch 5')
    ax.set(title='Uninterrupted vs Resumed Training',xlabel='Epoch',ylabel='Validation MSE')
    finish('advanced_03_resume.png',ax)

    report,candidates,preds=p1.run()
    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(9,6.5))
    ax1.bar(candidates.model,candidates.validation_f2,width=.48)
    ax1.set(title='Fleet Training · Validation Model Selection',ylabel='Validation F2',ylim=(0,1))
    weeks=preds.groupby('week').review_flag.agg(['size','sum'])
    limit=(weeks['size']*.30).apply(lambda n:__import__('math').ceil(n))
    ax2.bar(weeks.index, weeks['sum'],width=.55,label='Test reviews')
    ax2.plot(weeks.index,limit,'--o',label='Weekly capacity')
    ax2.set(xlabel='Week',ylabel='Number of events reviewed',title='Test Review Load (threshold fixed on Validation)')
    ax1.grid(alpha=.22);ax2.grid(alpha=.22);ax2.legend();fig.tight_layout()
    fig.savefig(FIG/'professional_01_fleet_training.png',bbox_inches='tight',dpi=145)
    plt.close(fig)
    return sorted(x.name for x in FIG.glob('*.png'))

if __name__=='__main__':
    for name in generate():print(name)
