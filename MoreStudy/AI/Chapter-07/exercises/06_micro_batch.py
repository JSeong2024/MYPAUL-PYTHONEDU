"""Practice 06 — Micro-Batch Gradient Accumulation."""
import torch
from torch import nn

def accumulate_gradient(model:nn.Module,x:torch.Tensor,y:torch.Tensor,micro_batch_size:int)->torch.Tensor:
    # TODO: 전체 Gradient 초기화
    # TODO: 불완전한 마지막 Micro-Batch까지 평균 Loss에 (batch_size / total) 반영
    # TODO: 매 Micro-Batch에서 backward 수행하고 Gradient Vector 반환
    raise NotImplementedError

if __name__=='__main__':
    m=nn.Linear(2,1)
    print(accumulate_gradient(m,torch.ones(5,2),torch.zeros(5,1),2))
