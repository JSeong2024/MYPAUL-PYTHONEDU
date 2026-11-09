"""큰 Gradient를 Clip해 갱신 크기가 과도해지는 것을 제한합니다."""
import torch
from torch import nn
model=nn.Linear(2,1)
x=torch.full((8,2),1000.)
y=torch.zeros(8,1)
optimizer=torch.optim.SGD(model.parameters(),lr=.01)
optimizer.zero_grad(set_to_none=True)
loss=nn.MSELoss()(model(x),y)
loss.backward()
before=float(nn.utils.clip_grad_norm_(model.parameters(),max_norm=1.0,error_if_nonfinite=True))
after=float(torch.linalg.vector_norm(torch.cat([p.grad.flatten() for p in model.parameters()])))
optimizer.step()
print(f'Gradient norm: before={before:.3f}, after={after:.3f}')
