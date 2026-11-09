"""CUDA가 있으면 AMP, 그렇지 않으면 기본 Float32 학습을 실행합니다."""
import torch
from torch import nn
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model=nn.Linear(4,1).to(device)
optimizer=torch.optim.AdamW(model.parameters(),lr=.01)
x=torch.randn(32,4,device=device);y=torch.randn(32,1,device=device)
optimizer.zero_grad(set_to_none=True)
if device.type=='cuda':
    scaler=torch.amp.GradScaler('cuda')
    with torch.amp.autocast('cuda',dtype=torch.float16):
        loss=nn.MSELoss()(model(x),y)
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    nn.utils.clip_grad_norm_(model.parameters(),1.0)
    scaler.step(optimizer);scaler.update()
else:
    loss=nn.MSELoss()(model(x),y)
    loss.backward()
    nn.utils.clip_grad_norm_(model.parameters(),1.0)
    optimizer.step()
print(f'device={device.type}, loss={float(loss.detach()):.4f}')
