"""Mini Project 01 — 배송 시간 예측."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "delivery_times.csv"


def compare_models(frame: pd.DataFrame) -> dict:
    """Baseline과 Linear Regression의 MAE 및 회귀 계수를 반환합니다."""
    # STEP 1: 필수 열과 수치 범위를 검사합니다.
    # STEP 2: 거리(X)와 배송 시간(y)을 지정하고 Train/Test로 분리합니다.
    # STEP 3: DummyRegressor와 LinearRegression을 동일한 Train Set으로 학습합니다.
    # STEP 4: 두 모델의 MAE를 동일한 Test Set에서 계산합니다.
    raise NotImplementedError


if __name__ == "__main__":
    print(compare_models(pd.read_csv(DATA)))
