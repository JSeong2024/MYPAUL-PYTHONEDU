"""Advanced 01 — Early Stopping, Dropout, Weight Decay 점검."""
from __future__ import annotations
from pathlib import Path
import copy
import pandas as pd
import torch
from torch import nn
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.common import (energy_data,make_loader,regression_model,seed_everything,
                              train_epoch,eval_loss,eval_regression)


def run(data_path=None,output_dir=None,max_epochs:int=75,patience:int=10):
    if max_epochs<2 or patience<1:raise ValueError('Invalid epochs or patience')
    seed_everything(8)
    d=energy_data(data_path)
    xtr,ytr=d['train'];xtr,ytr=xtr[::4][:60],ytr[::4][:60]
    xva,yva=d['validation'];xte,yte=d['test']
    # 같은 구조를 사용해 학습 안정성에 영향을 주는 설정만 비교합니다.
    init=copy.deepcopy(regression_model(hidden=64).state_dict())
    reports=[];history=[];predictions=pd.DataFrame({'observation_id':d['df'].iloc[d['test_indices']].observation_id})
    for mode in ['unregularized','regularized']:
        model=regression_model(hidden=64,dropout=.15 if mode=='regularized' else 0.)
        model.load_state_dict(init)
        optimizer=torch.optim.AdamW(model.parameters(),lr=.012,
                                     weight_decay=.05 if mode=='regularized' else 0.)
        loss_fn=nn.MSELoss()
        loader=make_loader(xtr,ytr,batch_size=16,shuffle=True,seed=42)
        best=float('inf');best_epoch=0;best_state=None;waiting=0
        for epoch in range(1,max_epochs+1):
            train_loss=train_epoch(model,loader,optimizer,loss_fn)
            val_loss=eval_loss(model,xva,yva,loss_fn)
            history.append({'variant':mode,'epoch':epoch,
                            'train_loss':train_loss,'validation_loss':val_loss})
            if val_loss<best-1e-8:
                best=val_loss;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict());waiting=0
            else:
                waiting+=1
                if waiting>=patience:break
        model.load_state_dict(best_state)
        metric=eval_regression(model,xte,yte,d['ymean'],d['ystd'])
        predictions['actual_kwh']=metric['truth'].round(5)
        predictions[f'{mode}_prediction']=metric['pred'].round(5)
        reports.append({'variant':mode,'best_epoch':best_epoch,'epochs_run':epoch,
                        'best_validation_loss':best,'test_mae_kwh':metric['mae']})
    report=pd.DataFrame(reports);hist=pd.DataFrame(history)
    if output_dir is not None:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        report.to_csv(out/'generalization_summary.csv',index=False)
        hist.to_csv(out/'learning_curves.csv',index=False)
        predictions.to_csv(out/'test_predictions.csv',index=False)
    return report,hist,predictions

if __name__=='__main__':
    a,_,_=run(output_dir=Path(__file__).resolve().parents[1]/'outputs'/'advanced_01')
    print(a.to_string(index=False))
