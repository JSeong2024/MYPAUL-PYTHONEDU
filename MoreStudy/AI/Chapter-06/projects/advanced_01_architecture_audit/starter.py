"""Advanced 01 — 신경망 설계, 출력 Shape 및 Parameter 감사."""
from torch import nn

class SignalNet(nn.Module):
    def __init__(self, hidden=16, dropout=0.0):
        super().__init__()
        # TODO: 6->hidden->3 네트워크, ReLU/Dropout 포함
        raise NotImplementedError

    def forward(self, x):
        # TODO: (N,6) Shape 검증 후 Logit 반환
        raise NotImplementedError


def count_parameters(model):
    # TODO: 학습 가능한 Parameter 개수 계산
    raise NotImplementedError


def run():
    # TODO: Validation Split과 두 아키텍처 학습·평가
    raise NotImplementedError

if __name__=='__main__':
    run()
