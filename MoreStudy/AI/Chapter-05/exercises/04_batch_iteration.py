"""Practice 04 — DataLoader 배치 집계."""
import torch
from torch.utils.data import TensorDataset, DataLoader


def batch_sizes(count: int, batch_size: int) -> list[int]:
    """샘플 수와 배치 크기에 따른 실제 배치의 크기를 반환."""
    if count < 0 or batch_size <= 0:
        raise ValueError('invalid count or batch_size')
    dataset = TensorDataset(torch.arange(count))
    # TODO: DataLoader 생성 후 각 배치의 실제 길이를 반환 (drop_last=False)
    raise NotImplementedError
