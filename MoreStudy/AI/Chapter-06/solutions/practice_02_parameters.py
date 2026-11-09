"""Practice 02 모범 구현: Parameter 개수."""
from torch import nn

def parameter_count(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

if __name__=='__main__':
    model=nn.Sequential(nn.Linear(4,6),nn.ReLU(),nn.Linear(6,2))
    print(parameter_count(model)) # 44
