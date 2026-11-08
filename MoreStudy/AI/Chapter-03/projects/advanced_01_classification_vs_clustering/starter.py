"""Advanced 01: Supervised와 Unsupervised의 결과 비교."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, adjusted_rand_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data/work_modes.csv"
FEATURES = ["morning_activity", "remote_activity", "evening_activity"]


def load_and_validate(path=DATA_PATH):
    """STEP 1: Feature와 Target을 확인한다."""
    df = pd.read_csv(path)
    # TODO: 결측값, 값의 범위, 중복 ID를 확인한다.
    raise NotImplementedError("STEP 1: 데이터 검증")


def compare_methods(df):
    """STEP 2~5: 별도의 Classification과 Clustering을 실행한다."""
    # TODO: stratify=y, test_size=0.30, random_state=42로 분리한다.
    # TODO: Supervised 모델을 Train Set으로 학습하고 Test Set Accuracy를 계산한다.
    # TODO: Test Set의 Feature만 사용해 KMeans Clustering을 수행한다.
    # TODO: Target은 Clustering 이후 ARI 계산에만 사용한다.
    raise NotImplementedError("STEP 2~5: 두 방식의 결과 비교")


def main():
    df = load_and_validate()
    result = compare_methods(df)
    print(result)
    # TODO STEP 6: 예측 Label과 Cluster ID를 나란히 시각화한다.

if __name__ == "__main__":
    main()
