"""기본 CPU/GPU 장치 선택과 안전한 NumPy 변환."""
import torch


def choose_device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return torch.device('mps')
    return torch.device('cpu')


def main():
    device = choose_device()
    x = torch.arange(5, dtype=torch.float32, device=device)
    y = (x * 2).sum()
    result = y.detach().cpu().item()
    print('selected device:', device)
    print('sum:', result)
    print('NumPy:', (x * 2).detach().cpu().numpy().tolist())


if __name__ == '__main__':
    main()
