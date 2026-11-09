"""SGD와 AdamW는 같은 초기 Parameter에서 다른 갱신 경로를 만들 수 있습니다."""
import copy
import torch
torch.manual_seed(42)
original=torch.nn.Parameter(torch.tensor([4.,-3.]))
for name in ['sgd','adamw']:
    w=torch.nn.Parameter(original.detach().clone())
    opt=(torch.optim.SGD([w],lr=.12,momentum=.8) if name=='sgd'
         else torch.optim.AdamW([w],lr=.12,weight_decay=0.))
    for step in range(12):
        opt.zero_grad(set_to_none=True)
        loss=(w[0]-1).square()+4*(w[1]+2).square()
        loss.backward();opt.step()
    with torch.inference_mode():
        final_loss=float((w[0]-1).square()+4*(w[1]+2).square())
    print(f'{name}: w={w.detach().tolist()}, loss={final_loss:.4f}')
