"""Practice 05 — StepLR의 학습률 변화를 기록."""
import torch

def learning_rate_history(initial_lr:float,step_size:int,gamma:float,epochs:int)->list[float]:
    # TODO: SGD Optimizer와 StepLR을 생성
    # TODO: 각 Epoch에서 실제 사용한 LR 기록
    # TODO: optimizer.step() 후 scheduler.step() 수행
    raise NotImplementedError

if __name__=='__main__':
    print(learning_rate_history(.1,2,.5,5))
