"""Mini Project 02 — Autograd의 첫 업데이트 구현."""
from pathlib import Path
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[2]


def one_gradient_step(path: Path, learning_rate: float = 0.03):
    frame = pd.read_csv(path)
    x = torch.tensor(frame['input_signal'].to_numpy(), dtype=torch.float64)
    y = torch.tensor(frame['reference_value'].to_numpy(), dtype=torch.float64)
    # TODO: 입력 유한성, x 최소 2개 고유값, learning_rate 검증
    w = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    b = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    # TODO: MSE 계산 후 backward()로 w.grad, b.grad 얻기
    # TODO: no_grad 안에서 w,b 한 단계 갱신
    # TODO: 갱신 전후 Loss와 gradient 반환, grad 초기화
    raise NotImplementedError('Finish one_gradient_step')


if __name__ == '__main__':
    print(one_gradient_step(ROOT / 'data/calibration_pairs.csv'))
