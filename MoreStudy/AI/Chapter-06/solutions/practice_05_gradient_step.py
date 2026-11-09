"""Practice 05 모범 구현: 단일 Gradient Step."""
import torch

def one_step(model,x,y,lr=0.1):
    if lr<=0:raise ValueError('lr는 양수여야 합니다.')
    loss_fn=torch.nn.MSELoss()
    for p in model.parameters():
        p.grad=None
    before=loss_fn(model(x),y)
    before.backward()
    with torch.no_grad():
        for p in model.parameters():
            p -= lr*p.grad
    after=loss_fn(model(x),y)
    return float(before.item()),float(after.item())

if __name__=='__main__':
    model=torch.nn.Linear(1,1)
    print(one_step(model,torch.tensor([[1.]]),torch.tensor([[2.]])))
