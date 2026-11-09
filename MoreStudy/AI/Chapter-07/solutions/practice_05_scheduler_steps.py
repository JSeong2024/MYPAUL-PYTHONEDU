"""Practice 05 — LR Scheduler는 Optimizer update 이후 호출합니다."""
import torch

def learning_rate_history(initial_lr:float,step_size:int,gamma:float,epochs:int)->list[float]:
    if initial_lr<=0 or step_size<=0 or epochs<=0 or not 0<gamma<=1:
        raise ValueError('Invalid schedule configuration')
    param=torch.nn.Parameter(torch.tensor(0.))
    optimizer=torch.optim.SGD([param],lr=initial_lr)
    scheduler=torch.optim.lr_scheduler.StepLR(optimizer,step_size=step_size,gamma=gamma)
    history=[]
    for _ in range(epochs):
        history.append(optimizer.param_groups[0]['lr'])
        optimizer.zero_grad(set_to_none=True)
        (param-1).square().backward()
        optimizer.step()
        scheduler.step()
    return history

if __name__=='__main__':
    print(learning_rate_history(.1,2,.5,5))
