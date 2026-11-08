"""한 단계 자동 미분과 gradient accumulation 확인."""
import torch


def main():
    w = torch.tensor(1.0, requires_grad=True)
    b = torch.tensor(0.0, requires_grad=True)
    x = torch.tensor([1.0, 2.0, 3.0])
    y = torch.tensor([3.0, 5.0, 7.0])
    loss = ((w * x + b - y) ** 2).mean()
    print('loss:', loss.item(), 'graph:', type(loss.grad_fn).__name__)
    loss.backward()
    print('gradient:', w.grad.item(), b.grad.item())
    # 동일 계산을 새 그래프로 만들고 backward()하면 기존 grad에 더해집니다.
    ((w * x + b - y) ** 2).mean().backward()
    print('accumulated:', w.grad.item(), b.grad.item())
    w.grad = None
    b.grad = None
    print('after reset:', w.grad, b.grad)
    with torch.no_grad():
        value = w * x + b
    print('tracking disabled:', value.requires_grad)


if __name__ == '__main__':
    main()
