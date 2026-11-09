"""Dropout은 Train/Eval에서 다르게 작동합니다. Weight Decay는 Optimizer 설정입니다."""
import torch
from torch import nn
torch.manual_seed(4)
model=nn.Sequential(nn.Linear(4,8),nn.ReLU(),nn.Dropout(.3),nn.Linear(8,1))
optimizer=torch.optim.AdamW(model.parameters(),lr=.01,weight_decay=.03)
x=torch.ones(5,4)
model.train();a=model(x);b=model(x)
model.eval()
with torch.inference_mode():
    c=model(x);d=model(x)
print('Train outputs equal:',bool(torch.allclose(a,b)))
print('Eval outputs equal:',bool(torch.allclose(c,d)))
print('Weight decay:',optimizer.param_groups[0]['weight_decay'])
