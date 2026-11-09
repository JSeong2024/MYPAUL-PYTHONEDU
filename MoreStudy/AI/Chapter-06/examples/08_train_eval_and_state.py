"""train/eval 모드, 추론, state_dict 복원."""
from pathlib import Path
import tempfile
import torch
from torch import nn

model=nn.Sequential(nn.Linear(3,12),nn.ReLU(),nn.Dropout(0.5),nn.Linear(12,2))
print('model.training initially:',model.training)
model.eval()
print('Dropout module.training in eval:',model[2].training)
x=torch.tensor([[1.,2.,3.]])
with torch.inference_mode():
    logits=model(x)
    probs=logits.softmax(dim=1)
print('probability sum:',round(probs.sum().item(),6))
with tempfile.TemporaryDirectory() as td:
    path=Path(td)/'weights.pt'
    torch.save(model.state_dict(),path)
    restored=nn.Sequential(nn.Linear(3,12),nn.ReLU(),nn.Dropout(0.5),nn.Linear(12,2))
    restored.load_state_dict(torch.load(path,weights_only=True,map_location='cpu'))
    restored.eval()
    with torch.inference_mode():
        print('restoration identical:',torch.allclose(logits,restored(x)))
