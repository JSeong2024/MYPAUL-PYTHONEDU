"""nn.Linear의 Weight 방향과 Batch 차원."""
import torch
from torch import nn

torch.manual_seed(6)
layer=nn.Linear(3,2)
x=torch.tensor([[1.,2.,3.],[4.,5.,6.]],dtype=torch.float32)
y=layer(x)
print('input:',tuple(x.shape),'weight:',tuple(layer.weight.shape),'bias:',tuple(layer.bias.shape))
print('output:',tuple(y.shape))
print('same as x @ W.T + b:',torch.allclose(y,x @ layer.weight.T + layer.bias))
