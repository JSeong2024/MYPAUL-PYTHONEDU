"""Practice 04 — Validation Loss 기반 Early Stopping 상태 관리."""
from dataclasses import dataclass
import math

@dataclass
class EarlyStopper:
    patience:int=3
    min_delta:float=0.
    best:float=float('inf')
    best_epoch:int=0
    stale_epochs:int=0

    def __post_init__(self):
        if self.patience<=0 or self.min_delta<0:
            raise ValueError('Invalid patience or min_delta')

    def update(self,epoch:int,validation_loss:float)->bool:
        """이번 Epoch 이후 중단해야 하면 True를 반환합니다."""
        if epoch<=0 or not math.isfinite(validation_loss):
            raise ValueError('Invalid epoch or loss')
        if validation_loss < self.best-self.min_delta:
            self.best=float(validation_loss);self.best_epoch=epoch;self.stale_epochs=0
        else:
            self.stale_epochs+=1
        return self.stale_epochs>=self.patience

if __name__=='__main__':
    stopper=EarlyStopper(patience=2)
    for epoch,val in enumerate([.8,.6,.61,.62],1):
        print(epoch,val,stopper.update(epoch,val))
