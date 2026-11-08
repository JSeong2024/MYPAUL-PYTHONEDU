"""Advanced 02: 같은 장비의 반복 측정값에 따른 그룹 누출 실험."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split,GroupShuffleSplit,GroupKFold,cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from common import ROOT,load_devices


def evaluate(df):
    X=df[["fingerprint_signal"]].to_numpy()
    y=df.maintenance_flag.to_numpy(dtype=int)
    groups=df.device_id.to_numpy()
    ridx=np.arange(len(y))
    tr,te=train_test_split(ridx,test_size=.25,stratify=y,random_state=42)
    grouped=GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42)
    gtr,gte=next(grouped.split(X,y,groups))
    def train_score(train,test):
        model=KNeighborsClassifier(n_neighbors=1).fit(X[train],y[train])
        pred=model.predict(X[test])
        return {"accuracy":float(accuracy_score(y[test],pred)),
                "balanced_accuracy":float(balanced_accuracy_score(y[test],pred)),
                "group_overlap":len(set(groups[train]) & set(groups[test])),
                "train_groups":len(set(groups[train])),"test_groups":len(set(groups[test]))}
    random_result=train_score(tr,te)
    grouped_result=train_score(gtr,gte)
    cv=GroupKFold(n_splits=5)
    cv_scores=cross_val_score(KNeighborsClassifier(n_neighbors=1),X,y,groups=groups,cv=cv,scoring="balanced_accuracy")
    return {"random":random_result,"grouped":grouped_result,"group_cv_balanced":cv_scores}


def plot_result(r,output=ROOT/"outputs/advanced_02_group_audit.png"):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig,axs=plt.subplots(1,2,figsize=(9.4,4))
    keys=["random","grouped"]
    axs[0].bar(["Random split","Group split"],[r[k]["balanced_accuracy"] for k in keys])
    axs[0].set(ylim=(0,1.05),ylabel="Balanced accuracy",title="Unseen-device generalization")
    axs[1].bar(["Random split","Group split"],[r[k]["group_overlap"] for k in keys])
    axs[1].set(ylabel="Shared device IDs",title="Device overlap across splits")
    fig.tight_layout();fig.savefig(output,dpi=150);plt.close(fig)
    return output


def main():
    r=evaluate(load_devices())
    print("Random:",r["random"])
    print("Group-aware:",r["grouped"])
    print("GroupKFold balanced accuracy:",np.round(r["group_cv_balanced"],3))
    print("Saved:",plot_result(r))

if __name__=="__main__":main()
