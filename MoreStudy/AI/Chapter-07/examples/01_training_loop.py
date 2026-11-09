"""Training Loop — Batch 처리, backward, step, 모드 전환."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from torch import nn
from solutions.common import alert_data,make_loader,binary_model,seed_everything,train_epoch,eval_loss
seed_everything(17)
d=alert_data();model=binary_model();optimizer=torch.optim.AdamW(model.parameters(),lr=.015)
loss_fn=nn.BCEWithLogitsLoss()
x,y=d['train'];val_x,val_y=d['validation']
loader=make_loader(x,y,32,shuffle=True,seed=17)
for epoch in range(1,6):
    train_loss=train_epoch(model,loader,optimizer,loss_fn)
    val_loss=eval_loss(model,val_x,val_y,loss_fn)
    print(f'Epoch {epoch:02d}: train={train_loss:.4f}, val={val_loss:.4f}')
