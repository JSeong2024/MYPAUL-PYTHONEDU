"""Mini 02: 대여소 이용 패턴 Clustering."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data/station_patterns.csv"
FEATURES = ["morning_trips", "evening_trips", "weekend_trips"]


def load_and_validate(path=DATA_PATH):
    """STEP 1: 데이터 형식과 식별자 중복을 확인한다."""
    df = pd.read_csv(path)
    # TODO: 필수 열과 값의 유효성을 검사한다.
    raise NotImplementedError("STEP 1: 데이터 검증")


def cluster_and_profile(df):
    """STEP 2~4: 표준화, KMeans, 원래 단위의 Cluster 평균 계산."""
    # TODO: station_id를 Feature에서 제외한다.
    # TODO: StandardScaler + KMeans(n_clusters=3, n_init=10, random_state=42).
    # TODO: cluster ID를 추가하고 Feature별 평균과 건수를 구한다.
    raise NotImplementedError("STEP 2~4: Clustering과 Profile")


def main():
    df = load_and_validate()
    result = cluster_and_profile(df)
    print(result)
    # TODO STEP 5: 오전/주말 이용량 산점도를 저장한다.

if __name__ == "__main__":
    main()
