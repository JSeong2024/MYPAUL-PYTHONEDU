"""모범 구현 결과를 이용해 Chapter 06 설명 그림 생성."""
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from solutions import mini_01_xor_network as m1
from solutions import mini_02_nonlinear_regression as m2
from solutions import advanced_01_architecture_audit as a1
from solutions import advanced_02_model_handoff as a2

def save(name):
    plt.tight_layout();plt.savefig(ROOT/'figures'/name,dpi=135,bbox_inches='tight');plt.close()

def main():
    torch.set_num_threads(1)
    (ROOT/'figures').mkdir(exist_ok=True)
    df=pd.read_csv(ROOT/'data/xor_signals.csv')
    x=torch.tensor(df[['signal_x','signal_y']].to_numpy(dtype='float32'))
    y=torch.tensor(df.label.to_numpy(dtype='float32'))
    idx,_=train_test_split(np.arange(len(df)),test_size=.25,stratify=df.label,random_state=17)
    torch.manual_seed(11)
    linear=nn.Linear(2,1)
    mlp=nn.Sequential(nn.Linear(2,8),nn.Tanh(),nn.Linear(8,1))
    m1.fit(linear,x[idx],y[idx]);m1.fit(mlp,x[idx],y[idx])
    u=np.linspace(-2,2,100)
    xx,yy=np.meshgrid(u,u)
    grid=torch.tensor(np.c_[xx.ravel(), yy.ravel()],dtype=torch.float32)
    fig,axs=plt.subplots(1,2,figsize=(9,3.8))
    for ax,model,title in zip(axs,[linear,mlp],['Single Linear Layer','MLP with Tanh']):
        model.eval()
        with torch.inference_mode():z=torch.sigmoid(model(grid).reshape(xx.shape)).numpy()
        ax.contourf(xx,yy,z,levels=[0,.5,1],alpha=.23)
        ax.contour(xx,yy,z,levels=[.5],linewidths=1)
        ax.scatter(df.signal_x,df.signal_y,c=df.label,s=11,cmap='viridis')
        ax.set(title=title,xlabel='signal_x',ylabel='signal_y',xlim=(-2,2),ylim=(-2,2))
    save('mini_01_xor_boundary.png')

    _,pred,_,_=m2.run()
    plt.figure(figsize=(6,4))
    plt.scatter(pred.actual,pred.linear_prediction,s=20,alpha=.7,label='Linear')
    plt.scatter(pred.actual,pred.mlp_prediction,s=20,alpha=.7,label='MLP')
    mn=min(pred.actual.min(),pred.linear_prediction.min(),pred.mlp_prediction.min())
    mx=max(pred.actual.max(),pred.linear_prediction.max(),pred.mlp_prediction.max())
    plt.plot([mn,mx],[mn,mx],linestyle='--',linewidth=1,label='Perfect prediction')
    plt.xlabel('Actual demand');plt.ylabel('Prediction');plt.legend()
    save('mini_02_regression_comparison.png')

    report,_,_=a1.run()
    plt.figure(figsize=(5.8,3.8))
    plt.bar(report.architecture,report.validation_macro_f1)
    plt.ylim(0,1);plt.ylabel('Validation Macro F1')
    for i,n in enumerate(report.parameter_count):plt.text(i, report.validation_macro_f1.iloc[i]+0.02,f'{n} parameters',ha='center')
    save('advanced_01_architectures.png')

    with tempfile.TemporaryDirectory() as tmp:
        a2.run(output_dir=tmp)
        preds=pd.read_csv(Path(tmp)/'predictions.csv')
        correct=preds.true_label==preds.predicted_label
        plt.figure(figsize=(5.8,3.8))
        plt.hist(preds.loc[correct,'confidence'],bins=10,alpha=.7,label='Correct')
        plt.hist(preds.loc[~correct,'confidence'],bins=10,alpha=.7,label='Incorrect')
        plt.xlabel('Max class probability');plt.ylabel('Test sample count');plt.legend()
        save('advanced_02_handoff.png')
    print('Created 4 figures')

if __name__=='__main__':
    main()
