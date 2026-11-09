"""Advanced 03 — 모델뿐 아니라 Optimizer·Scheduler도 복원하는 중단 재개."""
from __future__ import annotations
from pathlib import Path
import copy
import json
import numpy as np
import pandas as pd
import torch
from torch import nn
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.common import energy_data,make_loader,seed_everything,train_epoch,eval_loss


def network():
    return nn.Sequential(nn.Linear(4,20),nn.Tanh(),nn.Linear(20,1))

def setup(initial):
    model=network();model.load_state_dict(initial)
    optimizer=torch.optim.AdamW(model.parameters(),lr=.014,weight_decay=.01)
    scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=4,gamma=.75)
    return model,optimizer,scheduler

def one_epoch(epoch,model,optimizer,scheduler,x,y,xva,yva):
    # Epoch별 Shuffle Seed를 고정해 중단 후에도 동일한 순서를 재구성합니다.
    loader=make_loader(x,y,batch_size=24,shuffle=True,seed=1000+epoch)
    loss=train_epoch(model,loader,optimizer,nn.MSELoss())
    val=eval_loss(model,xva,yva,nn.MSELoss())
    used_lr=optimizer.param_groups[0]['lr']
    scheduler.step()  # 한 Epoch의 optimizer.step() 뒤
    return {'epoch':epoch,'train_loss':loss,'validation_loss':val,'learning_rate':used_lr}


def run(data_path=None,output_dir=None,total_epochs:int=12,split_epoch:int=5):
    if not 1<=split_epoch<total_epochs:raise ValueError('split_epoch must be less than total_epochs')
    seed_everything(99)
    d=energy_data(data_path);x,y=d['train'];xva,yva=d['validation']
    initial=copy.deepcopy(network().state_dict())
    full,opt_full,sch_full=setup(initial);full_rows=[]
    for epoch in range(1,total_epochs+1):
        full_rows.append(one_epoch(epoch,full,opt_full,sch_full,x,y,xva,yva))
    out=Path(output_dir) if output_dir is not None else None
    if out is not None:out.mkdir(parents=True,exist_ok=True)
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        checkpoint=(out/'checkpoint.pt') if out is not None else (Path(tmp)/'checkpoint.pt')
        interrupted,opt_part,sch_part=setup(initial);resume_rows=[]
        for epoch in range(1,split_epoch+1):
            resume_rows.append(one_epoch(epoch,interrupted,opt_part,sch_part,x,y,xva,yva))
        torch.save({'epoch':split_epoch,'shuffle_base_seed':1000,'model':interrupted.state_dict(),
                    'optimizer':opt_part.state_dict(),'scheduler':sch_part.state_dict(),
                    'feature_order':d['df'].columns.tolist(),
                    'train_mean':torch.tensor(d['mean']),
                    'train_std':torch.tensor(d['std'])},checkpoint)
        saved=torch.load(checkpoint,map_location='cpu',weights_only=True)
        restarted,optimizer,scheduler=setup(initial)
        restarted.load_state_dict(saved['model'])
        optimizer.load_state_dict(saved['optimizer'])
        scheduler.load_state_dict(saved['scheduler'])
        for epoch in range(int(saved['epoch'])+1,total_epochs+1):
            resume_rows.append(one_epoch(epoch,restarted,optimizer,scheduler,x,y,xva,yva))
    max_diff=max(float((a-b).abs().max())
                 for a,b in zip(full.state_dict().values(),restarted.state_dict().values()))
    full_val=eval_loss(full,xva,yva,nn.MSELoss())
    resume_val=eval_loss(restarted,xva,yva,nn.MSELoss())
    report={'total_epochs':total_epochs,'split_epoch':split_epoch,
            'max_parameter_difference':max_diff,
            'full_validation_loss':full_val,'resumed_validation_loss':resume_val,
            'max_history_difference':max(abs(a['validation_loss']-b['validation_loss'])
                                        for a,b in zip(full_rows,resume_rows))}
    history=pd.concat([pd.DataFrame(full_rows).assign(run='uninterrupted'),
                       pd.DataFrame(resume_rows).assign(run='resumed')],ignore_index=True)
    if out is not None:
        history.to_csv(out/'resume_history.csv',index=False)
        (out/'resume_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report,history

if __name__=='__main__':
    a,_=run(output_dir=Path(__file__).resolve().parents[1]/'outputs'/'advanced_03')
    print(a)
