"""Practice 02 모범 구현."""

def binary_scores(tp,fp,fn):
    if any(isinstance(v,bool) or not isinstance(v,int) or v<0 for v in [tp,fp,fn]):
        raise ValueError("건수는 0 이상의 정수여야 합니다.")
    precision=tp/(tp+fp) if tp+fp else 0.
    recall=tp/(tp+fn) if tp+fn else 0.
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.
    return float(precision),float(recall),float(f1)

if __name__=="__main__":print(binary_scores(8,2,4))
