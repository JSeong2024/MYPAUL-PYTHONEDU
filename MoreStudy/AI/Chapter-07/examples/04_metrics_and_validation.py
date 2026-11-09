"""Batch 손실은 Sample 수에 비례해 집계합니다."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from torch import nn
from solutions.common import energy_data,make_loader,seed_everything
seed_everything(22)
d=energy_data();x,y=d['validation'];model=nn.Linear(4,1)
loss_fn=nn.MSELoss(reduction='mean')
model.eval();total_loss=0.;total=0;batch_losses=[]
with torch.inference_mode():
    for bx,by in make_loader(x,y,batch_size=17):
        loss=float(loss_fn(model(bx),by));batch_losses.append(loss)
        total_loss+=loss*len(bx);total+=len(bx)
print('Weighted mean:',round(total_loss/total,6))
print('Unweighted batch mean:',round(sum(batch_losses)/len(batch_losses),6))
