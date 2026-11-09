"""Practice 03 — 전체 Gradient norm을 계산하고 Clip합니다."""
import torch
from torch import nn

def clip_gradients(model:nn.Module,max_norm:float)->tuple[float,float]:
    if max_norm<=0:raise ValueError('max_norm must be positive')
    params=[p for p in model.parameters() if p.grad is not None]
    if not params:raise ValueError('No gradient found')
    before=float(torch.linalg.vector_norm(torch.cat([p.grad.reshape(-1) for p in params])))
    nn.utils.clip_grad_norm_(params,max_norm=max_norm,error_if_nonfinite=True)
    after=float(torch.linalg.vector_norm(torch.cat([p.grad.reshape(-1) for p in params])))
    return before,after

if __name__=='__main__':
    model=nn.Linear(2,1);model(torch.ones(1,2)).sum().backward()
    print(clip_gradients(model,.5))
