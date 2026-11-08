"""Practice 01 모범 구현."""
import torch


def summarize(readings: torch.Tensor) -> torch.Tensor:
    if readings.ndim != 2 or readings.shape[1] != 3:
        raise ValueError('readings must have shape [N, 3]')
    if readings.shape[0] == 0:
        raise ValueError('empty readings')
    return readings.to(dtype=torch.float32).mean(dim=0)


if __name__ == '__main__':
    print(summarize(torch.tensor([[1, 2, 3], [3, 4, 5]])))
