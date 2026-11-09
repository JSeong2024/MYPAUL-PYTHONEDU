"""Practice 03 — Gradient Norm과 Clipping."""
import torch
from torch import nn

def clip_gradients(model:nn.Module,max_norm:float)->tuple[float,float]:
    # TODO: None이 아닌 Gradient만 수집하고, max_norm 검증
    # TODO: Clipping 전·후 Norm을 계산
    raise NotImplementedError

if __name__=='__main__':
    m=nn.Linear(2,1);m(torch.ones(1,2)).sum().backward()
    print(clip_gradients(m,.5))
