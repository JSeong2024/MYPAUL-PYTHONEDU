"""Mini 01: 불균형 Classification의 평가 지표 비교."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix,
                             f1_score, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from common import ROOT, ALERT_FEATURES, load_alerts


def measure(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "specificity": float(tn / (tn + fp)) if tn + fp else None,
        "matrix": cm,
    }


def evaluate(df):
    X, y = df[ALERT_FEATURES].to_numpy(), df.flagged.to_numpy(dtype=int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.25, random_state=42, stratify=y)
    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=42))
    model.fit(X_train, y_train)
    return {
        "dummy": measure(y_test, dummy.predict(X_test)),
        "model": measure(y_test, model.predict(X_test)),
        "test_count": len(y_test), "positive_count": int(y_test.sum()),
    }


def plot_result(result, output=ROOT / "outputs/mini_01_alert_metrics.png"):
    output = Path(output); output.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    keys = ["accuracy", "balanced_accuracy", "precision", "recall", "f1"]
    xx = np.arange(len(keys))
    axes[0].bar(xx - .18, [result["dummy"][k] for k in keys], .36, label="Majority baseline")
    axes[0].bar(xx + .18, [result["model"][k] for k in keys], .36, label="Logistic regression")
    axes[0].set(xticks=xx, xticklabels=["Accuracy", "Balanced", "Precision", "Recall", "F1"], ylim=(0, 1.05), title="Binary classification metrics")
    axes[0].tick_params(axis="x", rotation=40)
    axes[0].legend(fontsize=8)
    cm = result["model"]["matrix"]
    axes[1].imshow(cm, cmap="Blues")
    for (i, j), value in np.ndenumerate(cm):
        axes[1].text(j, i, str(value), ha="center", va="center")
    axes[1].set(xticks=[0, 1], yticks=[0, 1], xticklabels=["0", "1"], yticklabels=["0", "1"], xlabel="Predicted", ylabel="Actual", title="Logistic regression: confusion matrix")
    fig.tight_layout(); fig.savefig(output, dpi=150); plt.close(fig)
    return output


def main():
    r=evaluate(load_alerts())
    print(f"Test: {r['test_count']} / positive: {r['positive_count']}")
    for name in ["dummy", "model"]:
        print(name, {k:round(v, 3) if isinstance(v, float) else v for k,v in r[name].items() if k!="matrix"})
        print("Confusion matrix:\n",r[name]["matrix"])
    print("Saved:",plot_result(r))

if __name__=="__main__": main()
