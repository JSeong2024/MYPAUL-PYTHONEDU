"""Mini 02 — autograd로 선형 보정식의 첫 번째 업데이트 계산."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]


def one_gradient_step(path: Path, learning_rate: float = 0.03) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not 0 < learning_rate <= 0.05:
        raise ValueError('learning_rate must be > 0 and <= 0.05')
    frame = pd.read_csv(path)
    if list(frame.columns) != ['input_signal', 'reference_value'] or len(frame) < 2:
        raise ValueError('Two columns and at least two rows are required')
    try:
        x_values = frame['input_signal'].to_numpy(dtype='float64')
        y_values = frame['reference_value'].to_numpy(dtype='float64')
    except (ValueError, TypeError) as exc:
        raise ValueError('Inputs must be numeric') from exc
    x = torch.from_numpy(x_values.copy())
    y = torch.from_numpy(y_values.copy())
    if not bool(torch.isfinite(x).all() & torch.isfinite(y).all()):
        raise ValueError('Inputs must be finite')
    if torch.unique(x).numel() < 2:
        raise ValueError('At least two distinct x values are required')
    w = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    b = torch.tensor(0.0, dtype=torch.float64, requires_grad=True)
    loss_before = ((w * x + b - y).square()).mean()
    loss_before.backward()
    dw, db = float(w.grad), float(b.grad)
    with torch.no_grad():
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad
        loss_after = ((w * x + b - y).square()).mean()
    gradient_table = pd.DataFrame([
        {'parameter': 'w', 'before': 0.0, 'gradient': dw, 'after': w.detach().item()},
        {'parameter': 'b', 'before': 0.0, 'gradient': db, 'after': b.detach().item()},
    ])
    loss_table = pd.DataFrame([{
        'sample_count': len(frame), 'learning_rate': learning_rate,
        'loss_before': loss_before.detach().item(), 'loss_after': loss_after.detach().item(),
    }])
    w.grad = None
    b.grad = None
    return gradient_table, loss_table


def main():
    parser = argparse.ArgumentParser(description='One-step autograd calibration')
    parser.add_argument('--input', type=Path, default=ROOT / 'data/calibration_pairs.csv')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'outputs/mini_02')
    parser.add_argument('--learning-rate', type=float, default=0.03)
    args = parser.parse_args()
    gradients, losses = one_gradient_step(args.input, args.learning_rate)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    gradients.round(6).to_csv(args.output_dir / 'gradient_report.csv', index=False)
    losses.round(6).to_csv(args.output_dir / 'loss_report.csv', index=False)
    print(gradients.round(6).to_string(index=False))
    print(losses.round(6).to_string(index=False))


if __name__ == '__main__':
    main()
