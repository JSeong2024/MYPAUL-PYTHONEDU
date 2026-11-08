"""Practice 04: Decision Threshold에서 이진 예측 생성."""
import numpy as np

def threshold_predictions(scores,threshold=.5):
    """[0,1] 확률 추정치에서 threshold 이상이면 1을 반환한다."""
    # TODO: 0~1 범위 검증, >= threshold 적용
    raise NotImplementedError

if __name__=="__main__":
    print(threshold_predictions([.2,.5,.8],.5))
