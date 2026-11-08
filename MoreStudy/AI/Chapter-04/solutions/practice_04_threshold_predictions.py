"""Practice 04 모범 구현."""
import numpy as np

def threshold_predictions(scores,threshold=.5):
    p=np.asarray(scores,dtype=float)
    if p.ndim!=1 or not len(p) or not np.isfinite(p).all() or (p<0).any() or (p>1).any():
        raise ValueError("Scores는 유한한 1차원 [0,1] 배열이어야 합니다.")
    if not np.isfinite(threshold) or not 0<=threshold<=1:
        raise ValueError("Threshold는 [0,1] 범위여야 합니다.")
    return (p>=threshold).astype(int)

if __name__=="__main__":print(threshold_predictions([.2,.5,.8],.5).tolist())
