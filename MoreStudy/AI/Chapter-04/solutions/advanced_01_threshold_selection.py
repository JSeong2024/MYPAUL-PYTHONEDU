"""Advanced 01: 검증 데이터에서만 Threshold를 선택하고 Test로 평가."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import fbeta_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from common import ROOT,ALERT_FEATURES,load_alerts

THRESHOLDS=np.round(np.arange(.05, .951, .05),2)


def choose_threshold(y_val,prob_val,thresholds=THRESHOLDS):
    """검증 F2 최대화. 동률이면 더 큰 Threshold를 선택한다."""
    if len(y_val)!=len(prob_val) or not len(y_val):
        raise ValueError("검증 배열 길이가 다르거나 비었습니다.")
    p=np.asarray(prob_val,dtype=float)
    if not np.isfinite(p).all() or (p<0).any() or (p>1).any():
        raise ValueError("확률 추정치는 0~1 범위여야 합니다.")
    scores=[float(fbeta_score(y_val,(p>=t).astype(int),beta=2,zero_division=0)) for t in thresholds]
    best=max(range(len(thresholds)),key=lambda i:(scores[i],float(thresholds[i])))
    return float(thresholds[best]),np.asarray(scores)


def evaluate(df):
    X,y=df[ALERT_FEATURES].to_numpy(),df.flagged.to_numpy(dtype=int)
    X_dev,X_test,y_dev,y_test=train_test_split(X,y,test_size=.2,stratify=y,random_state=42)
    X_train,X_val,y_train,y_val=train_test_split(X_dev,y_dev,test_size=.25,stratify=y_dev,random_state=43)
    model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,random_state=42))
    model.fit(X_train,y_train)
    p_val=model.predict_proba(X_val)[:,1]
    chosen,scores=choose_threshold(y_val,p_val)
    # 테스트 데이터는 검증 기준이 확정된 뒤 한 번만 사용한다.
    p_test=model.predict_proba(X_test)[:,1]
    def report(threshold):
        pred=(p_test>=threshold).astype(int)
        return {"precision":float(precision_score(y_test,pred,zero_division=0)),
                "recall":float(recall_score(y_test,pred,zero_division=0)),
                "f2":float(fbeta_score(y_test,pred,beta=2,zero_division=0)),
                "matrix":confusion_matrix(y_test,pred,labels=[0,1])}
    return {"chosen":chosen,"validation_f2":scores,"default_test":report(.5),
            "selected_test":report(chosen),"test_size":len(y_test),"val_size":len(y_val)}


def plot_result(r,output=ROOT/"outputs/advanced_01_threshold_selection.png"):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(7.8,4.6))
    ax.plot(THRESHOLDS,r["validation_f2"],marker="o",markersize=3,label="Validation F2")
    ax.axvline(r["chosen"],linestyle="--",color="tab:orange",label=f"Selected: {r['chosen']:.2f}")
    ax.set(xlabel="Decision threshold",ylabel="F2 score",ylim=(0,1.05),title="Threshold selection uses validation data")
    ax.legend();fig.tight_layout();fig.savefig(output,dpi=150);plt.close(fig)
    return output


def main():
    r=evaluate(load_alerts())
    print(f"Chosen validation threshold: {r['chosen']:.2f}")
    for name in ["default_test","selected_test"]:
        print(name,{k:round(v,3) if isinstance(v,float) else v for k,v in r[name].items() if k!="matrix"})
        print(r[name]["matrix"])
    print("Saved:",plot_result(r))

if __name__=="__main__":main()
