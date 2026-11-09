"""Optimizer와 Scheduler State를 포함한 Checkpoint 저장·복원."""
import tempfile
from pathlib import Path
import torch
model=torch.nn.Linear(1,1)
opt=torch.optim.AdamW(model.parameters(),lr=.01)
scheduler=torch.optim.lr_scheduler.StepLR(opt,step_size=3,gamma=.5)
x=torch.tensor([[1.],[2.]]);y=torch.tensor([[2.],[4.]])
for epoch in range(3):
    opt.zero_grad(set_to_none=True)
    torch.nn.MSELoss()(model(x),y).backward()
    opt.step();scheduler.step()
with tempfile.TemporaryDirectory() as td:
    checkpoint=Path(td)/'checkpoint.pt'
    torch.save({'epoch':3,'model':model.state_dict(),
                'optimizer':opt.state_dict(),'scheduler':scheduler.state_dict()},checkpoint)
    new_model=torch.nn.Linear(1,1)
    new_opt=torch.optim.AdamW(new_model.parameters(),lr=.01)
    new_scheduler=torch.optim.lr_scheduler.StepLR(new_opt,step_size=3,gamma=.5)
    state=torch.load(checkpoint,weights_only=True,map_location='cpu')
    new_model.load_state_dict(state['model'])
    new_opt.load_state_dict(state['optimizer'])
    new_scheduler.load_state_dict(state['scheduler'])
    print('Resumed at epoch',state['epoch'], 'LR',new_opt.param_groups[0]['lr'])
