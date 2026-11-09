"""가중합과 Step Activation으로 논리 게이트 살펴보기."""
import torch


def step(z):
    return (z >= 0).to(torch.int64)

x=torch.tensor([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
and_out=step(x @ torch.tensor([1.,1.]) - 1.5)
or_out=step(x @ torch.tensor([1.,1.]) - 0.5)
print('Input / AND / OR')
for a,b,c in zip(x.tolist(),and_out.tolist(),or_out.tolist()):
    print(a,b,c)
