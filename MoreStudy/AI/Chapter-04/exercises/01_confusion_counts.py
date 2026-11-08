"""Practice 01: Confusion Matrix 네 값 계산."""
import numpy as np

def confusion_counts(y_true, y_pred):
    """TN, FP, FN, TP 순서의 정수 tuple을 반환한다."""
    actual=np.asarray(y_true)
    predicted=np.asarray(y_pred)
    # TODO: 배열 길이, 0/1 레이블 검사 후 TN, FP, FN, TP 계산
    raise NotImplementedError

if __name__=="__main__":
    print(confusion_counts([0,0,1,1,1],[0,1,0,1,1]))
