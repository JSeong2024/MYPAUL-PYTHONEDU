"""Practice 03 모범 구현: 활성화 함수 적용."""
import torch

def hidden_activation(x,mode='relu'):
    if mode=='relu':return torch.relu(x)
    if mode=='tanh':return torch.tanh(x)
    raise ValueError('mode는 relu 또는 tanh여야 합니다.')

if __name__=='__main__':
    print(hidden_activation(torch.tensor([-2.,1.])))
