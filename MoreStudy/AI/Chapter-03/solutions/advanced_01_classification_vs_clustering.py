"""Advanced 01: 같은 Feature에서 Classification과 Clustering이 답하는 질문 비교."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, adjusted_rand_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["morning_activity", "remote_activity", "evening_activity"]


def load_data(path=ROOT / "data/work_modes.csv"):
    df = pd.read_csv(path)
    required = ["record_id", *FEATURES, "work_mode"]
    if any(c not in df for c in required):
        raise ValueError("필수 열이 없습니다.")
    if df[required].isna().any().any() or df.record_id.duplicated().any():
        raise ValueError("결측값 또는 중복 ID가 있습니다.")
    X = df[FEATURES].to_numpy(dtype=float)
    if not np.isfinite(X).all() or not df.work_mode.isin([0, 1, 2]).all():
        raise ValueError("Feature 또는 Target이 유효하지 않습니다.")
    return df


def compare_methods(df):
    X = df[FEATURES].to_numpy(dtype=float)
    y = df.work_mode.to_numpy(dtype=int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42)
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
    clf.fit(X_train, y_train)
    prediction = clf.predict(X_test)
    # Clustering에는 y_test를 제공하지 않는다. Label은 사후 ARI 계산에만 사용한다.
    clusterer = make_pipeline(StandardScaler(), KMeans(n_clusters=3, n_init=10, random_state=42))
    groups = clusterer.fit_predict(X_test)
    return {
        "X_test": X_test, "y_test": y_test, "prediction": prediction,
        "groups": groups, "accuracy": float(accuracy_score(y_test, prediction)),
        "ari": float(adjusted_rand_score(y_test, groups)),
        "classifier": clf, "clusterer": clusterer,
    }


def plot_result(result, output=ROOT / "outputs/advanced_01_classification_vs_clustering.png"):
    output = Path(output)
    output.parent.mkdir(exist_ok=True, parents=True)
    X = result["X_test"]
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.2))
    axes[0].scatter(X[:, 0], X[:, 1], c=result["prediction"], cmap="viridis", s=21)
    axes[0].set(title="Supervised: predicted class", xlabel="Morning activity", ylabel="Remote activity")
    axes[1].scatter(X[:, 0], X[:, 1], c=result["groups"], cmap="viridis", s=21)
    axes[1].set(title="Unsupervised: assigned cluster", xlabel="Morning activity", ylabel="Remote activity")
    fig.tight_layout()
    fig.savefig(output, dpi=140)
    plt.close(fig)
    return output


def main():
    result = compare_methods(load_data())
    print(f"Classification Accuracy: {result['accuracy']:.1%}")
    print(f"Clustering ARI (post-hoc): {result['ari']:.3f}")
    print("Saved:", plot_result(result))

if __name__ == "__main__":
    main()
