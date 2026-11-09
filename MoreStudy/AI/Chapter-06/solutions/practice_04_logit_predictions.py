"""Practice 04 모범 구현: Logit에서 확률/클래스 계산."""
import torch

def multiclass_predictions(logits):
    if logits.ndim != 2 or logits.shape[1] < 2:
        raise ValueError('Logits Shape는 (N,C), C>=2여야 합니다.')
    probabilities=torch.softmax(logits,dim=1)
    return probabilities,probabilities.argmax(dim=1)

if __name__=='__main__':
    print(multiclass_predictions(torch.tensor([[2.,0.,-1.]])))
