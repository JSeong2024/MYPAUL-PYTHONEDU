"""Practice 02 모범 구현."""
import torch


def calibrate(readings: torch.Tensor, offsets: torch.Tensor):
    if readings.ndim != 2 or readings.shape[1] != 3:
        raise ValueError('readings must be [N,3]')
    if offsets.shape != (3,):
        raise ValueError('offsets must be [3]')
    valid = readings >= 0
    result = readings.to(torch.float32) + offsets.to(readings.device, dtype=torch.float32)
    return result, valid


if __name__ == '__main__':
    print(calibrate(torch.tensor([[3., -1., 8.]]), torch.tensor([1., 2., 3.])))
