"""소규모 전체 데이터 학습 예시. Optimizer 상세는 Chapter 07."""
import torch
from torch import nn
from torch.utils.data import TensorDataset,DataLoader

torch.manual_seed(9)
torch.set_num_threads(1)
x=torch.linspace(-1,1,80).unsqueeze(1)
y=(0.7*x+0.2)
loader=DataLoader(TensorDataset(x,y),batch_size=16,shuffle=True)
model=nn.Linear(1,1)
optimizer=torch.optim.SGD(model.parameters(),lr=0.15)
loss_fn=nn.MSELoss()
for epoch in range(30):
    model.train()
    total=0.0
    for bx,by in loader:
        optimizer.zero_grad()
        predicted=model(bx)
        loss=loss_fn(predicted,by)
        loss.backward()
        optimizer.step()
        total+=loss.item()*len(bx)
    if epoch in (0,9,29):print(f'epoch {epoch+1:02d}: train MSE={total/len(x):.6f}')
model.eval()
with torch.inference_mode():
    print('prediction at x=0:',round(model(torch.zeros(1,1)).item(),4))
