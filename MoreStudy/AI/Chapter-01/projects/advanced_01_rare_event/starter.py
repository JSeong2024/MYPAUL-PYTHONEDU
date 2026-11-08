"""Advanced 01 Starter — 드문 사건을 놓치는 모델의 한계를 점검합니다."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, recall_score, balanced_accuracy_score

ROOT = Path(__file__).resolve().parents[2]


def run() -> None:
    df = pd.read_csv(ROOT / "data" / "rare_events.csv")
    # TODO 1: 결측과 0/1 레이블, 데이터 분포를 검사합니다.
    # TODO 2: 학습/평가 데이터를 층화 분할합니다.
    # TODO 3: 항상 0만 예측하는 비교 기준 모델을 만듭니다.
    # TODO 4: StandardScaler + LogisticRegression을 학습합니다.
    # TODO 5: 정확도, 드문 사건 재현율, 균형 정확도를 비교합니다.
    # TODO 6: 결과 그래프와 해석을 작성합니다.
    print(f"입력: {len(df)}건")
    raise NotImplementedError("TODO 1~6")


if __name__ == "__main__":
    run()
