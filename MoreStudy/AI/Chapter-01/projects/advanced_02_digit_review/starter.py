"""Advanced 02 Starter — 자동 분류와 사람 검토 대상으로 나눕니다."""
from pathlib import Path
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]


def review_decision(max_votes: np.ndarray, threshold: float) -> np.ndarray:
    """TODO: 최대 투표 비율이 기준 미만이면 True(검토 필요)로 반환합니다."""
    raise NotImplementedError("TODO: review_decision")


def run() -> None:
    digits = load_digits()
    # TODO 1: Feature(64차원)와 Label(0~9)을 분리합니다.
    # TODO 2: 80:20 층화 분할하고 KNN(이웃 5개)을 학습합니다.
    # TODO 3: predict_proba()의 최대 이웃 투표 비율을 구합니다.
    # TODO 4: 기준 0.8 미만은 REVIEW, 나머지는 AUTO로 분리합니다.
    # TODO 5: 건수, 자동 처리 정확도, 검토 사례 이미지를 표시합니다.
    print(f"입력: {len(digits.target)}건")
    raise NotImplementedError("TODO 1~5")


if __name__ == "__main__":
    run()
