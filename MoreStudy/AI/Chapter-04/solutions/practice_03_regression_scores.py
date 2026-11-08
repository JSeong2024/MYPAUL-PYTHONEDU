"""Practice 03 모범 구현."""
import numpy as np

def regression_scores(y_true,y_pred):
    actual=np.asarray(y_true,dtype=float)
    predicted=np.asarray(y_pred,dtype=float)
    if actual.ndim!=1 or predicted.ndim!=1 or len(actual)==0 or len(actual)!=len(predicted):
        raise ValueError("1차원 비어 있지 않은 동일 길이 배열이 필요합니다.")
    if not np.isfinite(actual).all() or not np.isfinite(predicted).all():
        raise ValueError("유한한 수만 허용합니다.")
    error=actual-predicted
    mae=float(np.abs(error).mean())
    mse=float(np.mean(error**2))
    return mae,mse,float(np.sqrt(mse))

if __name__=="__main__":print(regression_scores([2,5,10],[3,5,8]))
