"""Practice 01 모범 구현."""
import numpy as np

def confusion_counts(y_true,y_pred):
    actual=np.asarray(y_true)
    pred=np.asarray(y_pred)
    if actual.ndim!=1 or pred.ndim!=1 or len(actual)==0 or len(actual)!=len(pred):
        raise ValueError("1차원 비어 있지 않은 동일 길이 배열이 필요합니다.")
    if not np.isin(actual,[0,1]).all() or not np.isin(pred,[0,1]).all():
        raise ValueError("0 또는 1만 허용합니다.")
    tn=int(((actual==0)&(pred==0)).sum())
    fp=int(((actual==0)&(pred==1)).sum())
    fn=int(((actual==1)&(pred==0)).sum())
    tp=int(((actual==1)&(pred==1)).sum())
    return tn,fp,fn,tp

if __name__=="__main__":print(confusion_counts([0,0,1,1,1],[0,1,0,1,1]))
