"""Mini 01 Starter — 규칙 기반과 학습 기반 날씨 판단을 비교합니다."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]


def rule_predict(rain_probability: np.ndarray) -> np.ndarray:
    """TODO 1: 강수 확률이 60 이상이면 1, 아니면 0을 반환합니다."""
    raise NotImplementedError("TODO 1")


def run() -> None:
    df = pd.read_csv(ROOT / "data" / "weather_choices.csv")
    features = ["rain_probability_pct", "wind_speed_kmh"]
    # TODO 2: X(특징)와 y(정답)를 구분하고 75:25로 분리합니다.
    # TODO 3: 규칙 기반 예측과 KNN(이웃 5개) 예측을 각각 계산합니다.
    # TODO 4: 동일한 평가 데이터에서 정답 비율을 비교합니다.
    # TODO 5: 결과를 산점도로 저장합니다.
    print(f"입력: {len(df)}행 / 특징: {features}")
    raise NotImplementedError("TODO 2~5")


if __name__ == "__main__":
    run()
