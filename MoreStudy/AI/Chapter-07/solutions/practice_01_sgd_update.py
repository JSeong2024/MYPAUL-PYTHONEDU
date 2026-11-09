"""Practice 01 — Parameter 업데이트를 수식으로 확인합니다."""
import torch

def sgd_update(weight:torch.Tensor,gradient:torch.Tensor,learning_rate:float)->torch.Tensor:
    if learning_rate<=0:raise ValueError('learning_rate must be positive')
    if weight.shape!=gradient.shape:raise ValueError('Shape mismatch')
    return weight-learning_rate*gradient

if __name__=='__main__':
    print(sgd_update(torch.tensor([2.,-1.]),torch.tensor([.5,-.2]),.1))
