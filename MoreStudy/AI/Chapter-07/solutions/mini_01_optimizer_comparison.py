"""Mini 01 — 같은 출발점에서 SGD Momentum과 AdamW 비교."""
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


def run(data_path=None,output_dir=None,epochs:int=36):
    if epochs<2:raise ValueError('epochs must be >= 2')
    seed_everything(42)
    d=energy_data(data_path)
    template=regression_model()
    initial=copy.deepcopy(template.state_dict())
    report=[];history=[];predictions=pd.DataFrame({
        'observation_id':d['df'].iloc[d['test_indices']]['observation_id'].to_numpy(),
    })
    for name in ['sgd_momentum','adamw']:
        model=regression_model();model.load_state_dict(initial)
        opt=(torch.optim.SGD(model.parameters(),lr=.045,momentum=.85)
             if name=='sgd_momentum' else torch.optim.AdamW(model.parameters(),lr=.012,weight_decay=0.))
        loss_fn=nn.MSELoss();best_loss=float('inf');best_state=None;best_epoch=0
        xtr,ytr=d['train'];xva,yva=d['validation'];xte,yte=d['test']
        loader=make_loader(xtr,ytr,batch_size=32,shuffle=True,seed=71)
        for epoch in range(1,epochs+1):
            train_loss=train_epoch(model,loader,opt,loss_fn)
            val_loss=eval_loss(model,xva,yva,loss_fn)
            history.append({'model':name,'epoch':epoch,'train_loss':train_loss,
                            'validation_loss':val_loss,'learning_rate':opt.param_groups[0]['lr']})
            if val_loss<best_loss:
                best_loss=val_loss;best_state=copy.deepcopy(model.state_dict());best_epoch=epoch
        model.load_state_dict(best_state)
        metric=eval_regression(model,xte,yte,d['ymean'],d['ystd'])
        predictions['actual_kwh']=metric['truth'].round(5)
        predictions[f'{name}_predicted_kwh']=metric['pred'].round(5)
        report.append({'optimizer':name,'best_epoch':best_epoch,'validation_mse_scaled':best_loss,
                       'test_mae_kwh':metric['mae'],'test_rmse_kwh':metric['rmse']})
    report_df=pd.DataFrame(report);history_df=pd.DataFrame(history)
    if output_dir is not None:
        out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
        report_df.to_csv(out/'optimizer_comparison.csv',index=False)
        history_df.to_csv(out/'training_history.csv',index=False)
        predictions.to_csv(out/'test_predictions.csv',index=False)
    return report_df,history_df,predictions

if __name__=='__main__':
    result,_,_=run(output_dir=Path(__file__).resolve().parents[1]/'outputs'/'mini_01')
    print(result.to_string(index=False))
