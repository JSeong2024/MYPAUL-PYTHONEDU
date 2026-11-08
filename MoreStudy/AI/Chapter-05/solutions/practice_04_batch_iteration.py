"""Practice 04 모범 구현."""
import torch
from torch.utils.data import TensorDataset, DataLoader


def batch_sizes(count: int, batch_size: int) -> list[int]:
    if count < 0 or batch_size <= 0:
        raise ValueError('invalid count or batch_size')
    dataset = TensorDataset(torch.arange(count))
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    return [len(features) for (features,) in loader]


if __name__ == '__main__':
    print(batch_sizes(10, 4))
