"""Sequential과 nn.Module로 만든 신경망의 출력 Shape."""
import torch
from torch import nn

class SmallNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.network=nn.Sequential(nn.Linear(4,8),nn.ReLU(),nn.Linear(8,3))
    def forward(self,x):
        return self.network(x)

torch.manual_seed(4)
model=SmallNetwork()
batch=torch.randn(5,4)
logits=model(batch)
print(model)
print('logits shape:',tuple(logits.shape))
print('trainable parameters:',sum(p.numel() for p in model.parameters()))
