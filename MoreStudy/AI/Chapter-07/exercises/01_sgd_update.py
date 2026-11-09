"""Practice 01 — SGD Parameter 갱신."""
import torch

def sgd_update(weight:torch.Tensor,gradient:torch.Tensor,learning_rate:float)->torch.Tensor:
    # TODO: learning_rate 검증과 Shape 검사
    # TODO: weight - learning_rate * gradient 반환
    raise NotImplementedError

if __name__=='__main__':
    print(sgd_update(torch.tensor([2.,-1.]),torch.tensor([.5,-.2]),.1))
