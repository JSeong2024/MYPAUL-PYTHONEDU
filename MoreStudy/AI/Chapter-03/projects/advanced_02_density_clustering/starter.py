"""Advanced 02: 곡선형 군집의 KMeans와 DBSCAN 비교."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data/curved_paths.csv"
FEATURES = ["x_position", "y_position"]


def load_and_validate(path=DATA_PATH):
    """STEP 1: 좌표와 참고 그룹을 확인한다."""
    df = pd.read_csv(path)
    # TODO: 결측값, 식별자, Feature 형식 및 reference_group 값을 검증한다.
    raise NotImplementedError("STEP 1: 데이터 검증")


def compare_methods(df, eps=0.23, min_samples=6):
    """STEP 2~5: 좌표 표준화, KMeans/DBSCAN, 사후 ARI 계산."""
    # TODO: reference_group은 Cluster 계산에서 제외한다.
    # TODO: KMeans(n_clusters=2, n_init=10, random_state=42).
    # TODO: DBSCAN(eps=eps, min_samples=min_samples).
    # TODO: ARI, Cluster 수와 Noise(-1) 수를 각각 계산한다.
    raise NotImplementedError("STEP 2~5: Clustering 결과 비교")


def main():
    df = load_and_validate()
    result = compare_methods(df)
    print(result)
    # TODO STEP 6~7: 산점도와 eps 변경 실험을 수행한다.

if __name__ == "__main__":
    main()
