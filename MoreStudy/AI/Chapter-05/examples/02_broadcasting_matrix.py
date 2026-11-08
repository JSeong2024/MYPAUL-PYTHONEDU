"""Broadcasting, reduction, matrix multiplication, shape error."""
import torch


def main():
    samples = torch.tensor([[40., 30., 20.], [50., 45., 35.]])
    offsets = torch.tensor([2., -1., 3.])
    calibrated = samples + offsets
    print('broadcast result:', calibrated.tolist())
    print('mean(dim=0):', calibrated.mean(dim=0).tolist())
    print('mean(dim=1):', calibrated.mean(dim=1).tolist())
    weights = torch.tensor([[0.2], [0.3], [0.5]])
    score = calibrated @ weights
    print('matrix result shape:', tuple(score.shape))
    try:
        _ = calibrated + torch.ones(2)
    except RuntimeError as exc:
        print('incompatible shapes:', type(exc).__name__)


if __name__ == '__main__':
    main()
