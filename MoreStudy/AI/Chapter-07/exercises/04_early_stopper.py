"""Practice 04 — Validation Loss로 Early Stopping 구현."""
from dataclasses import dataclass

@dataclass
class EarlyStopper:
    patience:int=3
    min_delta:float=0.
    best:float=float('inf')
    best_epoch:int=0
    stale_epochs:int=0

    def update(self,epoch:int,validation_loss:float)->bool:
        # TODO: validation_loss 개선 여부 판단, best_epoch 갱신
        # TODO: 개선 없을 때 stale_epochs 증가, patience에 도달하면 True
        raise NotImplementedError

if __name__=='__main__':
    e=EarlyStopper(patience=2)
    for n,v in enumerate([.8,.6,.61,.62],1):print(e.update(n,v))
