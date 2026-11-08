"""Tensor 생성, dtype, shape, reshape."""
import numpy as np
import torch


def main():
    readings = torch.tensor([[20, 22, 21], [23, 24, 22]], dtype=torch.float32)
    print('shape:', tuple(readings.shape))
    print('dtype:', readings.dtype, 'device:', readings.device)
    print('column:', readings[:, 1].tolist())
    print('mean by sensor:', readings.mean(dim=0).tolist())
    print('flatten:', readings.reshape(-1).tolist())

    array = np.array([10.0, 20.0], dtype=np.float32)
    shared = torch.from_numpy(array)
    array[0] = 99.0
    print('shared NumPy view:', shared.tolist())
    copied = torch.tensor(array)
    array[1] = 77.0
    print('copied tensor:', copied.tolist())


if __name__ == '__main__':
    main()
