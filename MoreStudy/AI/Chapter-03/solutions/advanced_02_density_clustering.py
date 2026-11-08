"""Advanced 02: 비구형 군집과 Noise에서 KMeans와 DBSCAN 비교."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["x_position", "y_position"]


def load_data(path=ROOT / "data/curved_paths.csv"):
    df = pd.read_csv(path)
    required = ["point_id", *FEATURES, "reference_group"]
    if any(c not in df for c in required):
        raise ValueError("필수 열이 없습니다.")
    if df[required].isna().any().any() or df.point_id.duplicated().any():
        raise ValueError("결측값 또는 중복 ID가 있습니다.")
    X = df[FEATURES].to_numpy(dtype=float)
    if not np.isfinite(X).all() or not df.reference_group.isin([-1, 0, 1]).all():
        raise ValueError("위치 또는 참고 Group 값이 유효하지 않습니다.")
    return df


def compare_clusters(df, eps=0.23, min_samples=6):
    X = df[FEATURES].to_numpy(dtype=float)
    ref = df.reference_group.to_numpy(dtype=int)
    scaled = StandardScaler().fit_transform(X)
    kmeans = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(scaled)
    dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(scaled)
    n_clusters = len(set(dbscan) - {-1})
    return {
        "X": X, "reference": ref, "kmeans": kmeans, "dbscan": dbscan,
        "kmeans_ari": float(adjusted_rand_score(ref, kmeans)),
        "dbscan_ari": float(adjusted_rand_score(ref, dbscan)),
        "dbscan_noise": int((dbscan == -1).sum()),
        "dbscan_clusters": n_clusters,
    }


def plot_result(result, output=ROOT / "outputs/advanced_02_density_clustering.png"):
    output = Path(output)
    output.parent.mkdir(exist_ok=True, parents=True)
    X = result["X"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    for ax, field, title in zip(axes, ["reference", "kmeans", "dbscan"],
                                ["Reference (evaluation only)", "KMeans", "DBSCAN (-1: noise)"]):
        labels = result[field]
        ax.scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", s=15)
        ax.set(xlabel="x position", ylabel="y position", title=title)
        ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    fig.savefig(output, dpi=140)
    plt.close(fig)
    return output


def main():
    result = compare_clusters(load_data())
    print(f"KMeans ARI: {result['kmeans_ari']:.3f}")
    print(f"DBSCAN ARI: {result['dbscan_ari']:.3f}")
    print(f"DBSCAN cluster count: {result['dbscan_clusters']}, noise points: {result['dbscan_noise']}")
    print("Saved:", plot_result(result))

if __name__ == "__main__":
    main()
