"""CrossEntropyLoss와 BCEWithLogitsLoss는 원시 Logit을 입력받습니다."""
import torch
from torch import nn

logits=torch.tensor([[2.0,0.5,-1.0],[0.1,-0.2,1.2]])
labels=torch.tensor([0,2],dtype=torch.int64)
ce=nn.CrossEntropyLoss()(logits,labels)
print('CrossEntropy:',round(ce.item(),4),'classes:',logits.argmax(dim=1).tolist())
print('Softmax probabilities:',torch.softmax(logits,dim=1).round(decimals=3).tolist())

binary_logits=torch.tensor([1.4,-0.8,0.2])
binary_targets=torch.tensor([1.,0.,1.])
bce=nn.BCEWithLogitsLoss()(binary_logits,binary_targets)
print('BCEWithLogits:',round(bce.item(),4))
