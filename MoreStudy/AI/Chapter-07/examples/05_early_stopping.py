"""Validation 지표로 최선의 Weight를 선택합니다."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import copy
from torch import nn
import torch
from solutions.common import energy_data,regression_model,seed_everything,make_loader,train_epoch,eval_loss
seed_everything(26)
d=energy_data();model=regression_model(hidden=24);optimizer=torch.optim.AdamW(model.parameters(),lr=.02)
loss_fn=nn.MSELoss();x,y=d['train'];vx,vy=d['validation']
best=float('inf');best_epoch=0;best_state=None;stale=0
for epoch in range(1,31):
    train_epoch(model,make_loader(x,y,32,shuffle=True,seed=epoch),optimizer,loss_fn)
    v=eval_loss(model,vx,vy,loss_fn)
    if v<best-1e-6:
        best=v;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict());stale=0
    else:
        stale+=1
        if stale>=5:break
model.load_state_dict(best_state)
print(f'Best epoch={best_epoch}, validation MSE={best:.4f}, stopped after={epoch}')
