"""Practice 03 모범 구현."""
import torch


def derivative_at(value: float) -> float:
    x = torch.tensor(value, dtype=torch.float64, requires_grad=True)
    result = 3 * x.square() + 2 * x
    result.backward()
    return x.grad.item()


if __name__ == '__main__':
    print(derivative_at(2.0))
