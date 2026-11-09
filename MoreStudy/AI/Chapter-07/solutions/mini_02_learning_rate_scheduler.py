"""Mini 02 — 고정 LR과 StepLR의 학습 기록 비교."""
from __future__ import annotations
from pathlib import Path
import copy
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.metrics import f1_score
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.common import (alert_data,binary_model,seed_everything,make_loader,
                              train_epoch,eval_loss)


def run(data_path=None,output_dir=None,epochs:int=28):
    if epochs<2:raise ValueError('epochs must be >= 2')
    seed_everything(123)
    d=alert_data(data_path);init=binary_model().state_dict();initial=copy.deepcopy(init)
    history=[];report=[]
    for mode in ['fixed_lr','step_lr']:
        model=binary_model();model.load_state_dict(initial)
        optimizer=torch.optim.SGD(model.parameters(),lr=.085,momentum=.85)
        scheduler=(torch.optim.lr_scheduler.StepLR(optimizer,step_size=8,gamma=.5)
                   if mode=='step_lr' else None)
        loss_fn=nn.BCEWithLogitsLoss()
        train_x,train_y=d['train'];val_x,val_y=d['validation'];test_x,test_y=d['test']
        loader=make_loader(train_x,train_y,batch_size=30,shuffle=True,seed=99)
        best_loss=float('inf');best_epoch=0;best_state=None
        for epoch in range(1,epochs+1):
            used_lr=optimizer.param_groups[0]['lr']
            train_loss=train_epoch(model,loader,optimizer,loss_fn)
            val_loss=eval_loss(model,val_x,val_y,loss_fn)
            history.append({'schedule':mode,'epoch':epoch,'learning_rate':used_lr,
                            'train_loss':train_loss,'validation_loss':val_loss})
            if val_loss<best_loss:
                best_loss=val_loss;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
            if scheduler is not None:scheduler.step()
        model.load_state_dict(best_state)
        model.eval()
        with torch.inference_mode():
            prob=torch.sigmoid(model(test_x)).numpy().flatten()
        pred=(prob>=.5).astype(int);actual=test_y.numpy().flatten().astype(int)
        report.append({'schedule':mode,'best_epoch':best_epoch,
                       'best_validation_loss':best_loss,
                       'test_accuracy':float((pred==actual).mean()),
                       'test_f1':float(f1_score(actual,pred,zero_division=0))})
    result=pd.DataFrame(report);hist=pd.DataFrame(history)
    if output_dir is not None:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        result.to_csv(out/'scheduler_comparison.csv',index=False)
        hist.to_csv(out/'learning_rate_history.csv',index=False)
    return result,hist

if __name__=='__main__':
    a,_=run(output_dir=Path(__file__).resolve().parents[1]/'outputs'/'mini_02')
    print(a.to_string(index=False))
