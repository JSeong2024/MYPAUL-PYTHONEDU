"""직접 계산한 Chain Rule와 Autograd 비교."""
import torch

x=torch.tensor(2.0)
w=torch.tensor(0.5,requires_grad=True)
b=torch.tensor(1.0,requires_grad=True)
target=torch.tensor(5.0)
prediction=w*x+b
loss=(prediction-target)**2
loss.backward()
# dL/dw = 2(wx+b-y)x, dL/db = 2(wx+b-y)
manual_dw=2*(prediction.item()-target.item())*x.item()
manual_db=2*(prediction.item()-target.item())
print('prediction:',prediction.item(),'loss:',loss.item())
print('dL/dw:',w.grad.item(),'manual:',manual_dw)
print('dL/db:',b.grad.item(),'manual:',manual_db)
