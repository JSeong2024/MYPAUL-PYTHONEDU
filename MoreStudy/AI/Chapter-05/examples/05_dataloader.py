"""TensorDataset, DataLoader, mini-batch와 마지막 배치 확인."""
import torch
from torch.utils.data import TensorDataset, DataLoader


def main():
    x = torch.arange(30, dtype=torch.float32).reshape(10, 3)
    y = (x[:, 0] > 12).to(torch.int64)
    dataset = TensorDataset(x, y)
    loader = DataLoader(dataset, batch_size=4, shuffle=False, num_workers=0)
    print('samples:', len(dataset), 'batches:', len(loader))
    for index, (features, labels) in enumerate(loader, start=1):
        print(f'batch {index}:', tuple(features.shape), tuple(labels.shape))
    shuffled = DataLoader(dataset, batch_size=4, shuffle=True,
                          generator=torch.Generator().manual_seed(42), num_workers=0)
    print('first shuffled IDs:', next(iter(shuffled))[0][:, 0].tolist())


if __name__ == '__main__':
    main()
