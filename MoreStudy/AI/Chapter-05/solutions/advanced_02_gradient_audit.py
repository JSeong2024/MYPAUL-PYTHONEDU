"""Advanced 02 — Autograd와 중심 차분 수치 미분을 비교하는 Gradient Audit."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]


def audit_gradients(path: Path, epsilon: float = 1e-6) -> pd.DataFrame:
    if not 0 < epsilon < 1e-2:
        raise ValueError('epsilon must be between 0 and 1e-2')
    frame = pd.read_csv(path)
    if list(frame.columns) != ['input_signal', 'target_value'] or len(frame) < 2:
        raise ValueError('At least two input and target pairs are required')
    try:
        x = torch.tensor(frame['input_signal'].to_numpy(dtype='float64').copy())
        y = torch.tensor(frame['target_value'].to_numpy(dtype='float64').copy())
    except (ValueError, TypeError) as exc:
        raise ValueError('Inputs must be numeric') from exc
    if not bool(torch.isfinite(x).all() & torch.isfinite(y).all()):
        raise ValueError('Inputs must be finite')
    # float64 중심 차분의 수치 안정성을 위해 CPU에서 실행합니다.
    w = torch.tensor(0.45, dtype=torch.float64, requires_grad=True)
    b = torch.tensor(-0.15, dtype=torch.float64, requires_grad=True)

    def loss_fn(weight: torch.Tensor, bias: torch.Tensor) -> torch.Tensor:
        prediction = torch.tanh(weight * x + bias)
        return (prediction - y).square().mean() + 0.05 * weight.square()

    loss = loss_fn(w, b)
    loss.backward()
    results = []
    for name, param in [('w', w), ('b', b)]:
        auto_value = float(param.grad)
        with torch.no_grad():
            plus_w = w + epsilon if name == 'w' else w
            plus_b = b + epsilon if name == 'b' else b
            minus_w = w - epsilon if name == 'w' else w
            minus_b = b - epsilon if name == 'b' else b
            numerical = float((loss_fn(plus_w, plus_b) - loss_fn(minus_w, minus_b)) / (2 * epsilon))
        absolute_error = abs(auto_value - numerical)
        relative_error = absolute_error / max(1., abs(auto_value), abs(numerical))
        results.append({
            'parameter': name, 'autograd': auto_value, 'finite_difference': numerical,
            'absolute_error': absolute_error, 'relative_error': relative_error,
            'pass': relative_error < 1e-5,
        })
    w.grad = None
    b.grad = None
    return pd.DataFrame(results)


def main():
    parser = argparse.ArgumentParser(description='Autograd numerical gradient audit')
    parser.add_argument('--input', type=Path, default=ROOT / 'data/gradient_audit.csv')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'outputs/advanced_02')
    parser.add_argument('--epsilon', type=float, default=1e-6)
    args = parser.parse_args()
    result = audit_gradients(args.input, args.epsilon)
    if not bool(result['pass'].all()):
        raise RuntimeError('Gradient audit failed')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_dir / 'gradient_audit_report.csv', index=False)
    print(result.to_string(index=False))


if __name__ == '__main__':
    main()
