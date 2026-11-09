"""StepLR는 지정한 Epoch 간격으로 LR을 줄입니다."""
import torch
parameter=torch.nn.Parameter(torch.tensor(2.))
optimizer=torch.optim.SGD([parameter],lr=.1)
scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=2,gamma=.5)
for epoch in range(1,7):
    lr=optimizer.param_groups[0]['lr']
    optimizer.zero_grad(set_to_none=True)
    (parameter-1).square().backward()
    optimizer.step()
    scheduler.step()  # Epoch의 Optimizer 갱신 뒤
    print(f'Epoch {epoch}: LR used={lr:.4f}')
