"""Practice 01 모범 구현: 가중합 한 단계."""
import torch

def linear_forward(x,weights,bias):
    if x.ndim!=2 or weights.ndim!=2 or x.shape[1]!=weights.shape[1] or bias.ndim!=1 or bias.shape[0]!=weights.shape[0]:
        raise ValueError('x=(N,D), weights=(O,D), bias=(O,)를 확인하세요.')
    return x@weights.T+bias

if __name__=='__main__':
    print(linear_forward(torch.tensor([[1.,2.]]),torch.tensor([[2.,3.],[-1.,1.]]),torch.tensor([0.5,1.])))
