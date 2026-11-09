"""선형층 사이에 활성화 함수를 넣는 이유."""
import torch
from torch import nn

x=torch.tensor([[-2.,-1.,0.,1.,2.]],dtype=torch.float32)
print('ReLU',nn.ReLU()(x).tolist())
print('Sigmoid',torch.sigmoid(x).round(decimals=3).tolist())
print('Tanh',torch.tanh(x).round(decimals=3).tolist())

layer1=nn.Linear(2,3)
layer2=nn.Linear(3,1)
with torch.no_grad():
    sample=torch.tensor([[1.,2.]])
    plain=layer2(layer1(sample))
    nonlinear=layer2(torch.relu(layer1(sample)))
print('two-linear and nonlinear output shapes:',tuple(plain.shape),tuple(nonlinear.shape))
