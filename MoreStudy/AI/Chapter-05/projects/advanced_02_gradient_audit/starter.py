"""Advanced Project 02 — Gradient Audit."""
from pathlib import Path
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[2]


def audit_gradients(path: Path, epsilon: float = 1e-6):
    frame = pd.read_csv(path)
    x = torch.tensor(frame['input_signal'].to_numpy(), dtype=torch.float64)
    y = torch.tensor(frame['target_value'].to_numpy(), dtype=torch.float64)
    # TODO: 입력 유효성 검증
    w = torch.tensor(0.45, dtype=torch.float64, requires_grad=True)
    b = torch.tensor(-0.15, dtype=torch.float64, requires_grad=True)

    def loss_fn(weight, bias):
        prediction = torch.tanh(weight * x + bias)
        return (prediction - y).square().mean() + 0.05 * weight.square()

    # TODO: backward()로 Autograd gradient 산출
    # TODO: (f(theta+epsilon)-f(theta-epsilon))/(2*epsilon) 구현
    # TODO: 상대오차 및 1e-5 미만 여부를 DataFrame에 기록
    raise NotImplementedError('Finish audit_gradients')


if __name__ == '__main__':
    print(audit_gradients(ROOT / 'data/gradient_audit.csv'))
