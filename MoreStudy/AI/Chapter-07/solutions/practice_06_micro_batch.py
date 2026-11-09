"""Practice 06 — 평균 Loss를 배치 크기에 비례해 누적합니다."""
import torch
from torch import nn

def accumulate_gradient(model:nn.Module,x:torch.Tensor,y:torch.Tensor,micro_batch_size:int)->torch.Tensor:
    if micro_batch_size<=0 or len(x)==0 or len(x)!=len(y):
        raise ValueError('Invalid batch size or dataset')
    model.zero_grad(set_to_none=True)
    loss_fn=nn.MSELoss(reduction='mean')
    for start in range(0,len(x),micro_batch_size):
        xm=x[start:start+micro_batch_size];ym=y[start:start+micro_batch_size]
        loss=loss_fn(model(xm),ym)
        (loss*(len(xm)/len(x))).backward()
    return torch.cat([p.grad.detach().flatten() for p in model.parameters()])

if __name__=='__main__':
    m=nn.Linear(2,1)
    print(accumulate_gradient(m,torch.ones(5,2),torch.zeros(5,1),2))
