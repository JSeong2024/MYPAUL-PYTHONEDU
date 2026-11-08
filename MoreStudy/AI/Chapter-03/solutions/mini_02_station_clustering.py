"""Mini 02: Label이 없는 대여소 이용 패턴 군집화."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["morning_trips", "evening_trips", "weekend_trips"]


def load_data(path=ROOT / "data/station_patterns.csv"):
    df = pd.read_csv(path)
    required = ["station_id", *FEATURES]
    if any(c not in df for c in required):
        raise ValueError("필수 열이 없습니다.")
    if df[required].isna().any().any() or df.station_id.duplicated().any():
        raise ValueError("결측값 또는 중복 ID가 있습니다.")
    values = df[FEATURES].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("이용 횟수는 0 이상의 유한한 수여야 합니다.")
    if len(df) < 3:
        raise ValueError("3개 이상의 샘플이 필요합니다.")
    return df


def cluster_stations(df, n_clusters=3):
    X = df[FEATURES].to_numpy(dtype=float)
    model = make_pipeline(StandardScaler(), KMeans(n_clusters=n_clusters, n_init=10, random_state=42))
    labels = model.fit_predict(X)
    table = df.copy()
    table["cluster"] = labels
    profile = table.groupby("cluster")[FEATURES].mean().round(1)
    counts = table.cluster.value_counts().sort_index()
    return {"model": model, "labels": labels, "profile": profile, "counts": counts, "table": table}


def plot_result(result, output=ROOT / "outputs/mini_02_station_clustering.png"):
    output = Path(output)
    output.parent.mkdir(exist_ok=True, parents=True)
    df = result["table"]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    scatter = ax.scatter(df.morning_trips, df.weekend_trips, c=df.cluster, cmap="viridis", alpha=0.8)
    ax.set(xlabel="Morning trips", ylabel="Weekend trips", title="Station use patterns (KMeans)")
    fig.colorbar(scatter, ax=ax, label="Cluster ID")
    fig.tight_layout()
    fig.savefig(output, dpi=140)
    plt.close(fig)
    return output


def main():
    result = cluster_stations(load_data())
    print("Cluster counts:\n", result["counts"].to_string())
    print("Cluster profile (original unit):\n", result["profile"].to_string())
    print("Saved:", plot_result(result))

if __name__ == "__main__":
    main()
