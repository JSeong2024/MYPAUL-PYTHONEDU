"""Mini 01: 문의 긴급도 Classification."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data/service_tickets.csv"
FEATURES = ["waiting_hours", "failed_attempts", "impacted_users"]


def load_and_validate(path=DATA_PATH):
    """STEP 1: CSV를 읽고 필수 열, NaN, 중복 ID, 값의 범위를 검증한다."""
    df = pd.read_csv(path)
    # TODO: 요구사항을 검증한 다음 DataFrame을 반환한다.
    raise NotImplementedError("STEP 1: 데이터 검증")


def fit_and_evaluate(df):
    """STEP 2~5: Train/Test 분리, Pipeline 학습, 예측과 지표 계산."""
    # TODO: X에서는 ticket_id와 urgent 열을 제외한다.
    # TODO: test_size=0.25, random_state=42, stratify=y.
    # TODO: StandardScaler + LogisticRegression을 연결한다.
    # TODO: Accuracy, Confusion Matrix, 클래스 1의 확률 추정치를 계산한다.
    raise NotImplementedError("STEP 2~5: 분류 및 평가")


def main():
    df = load_and_validate()
    result = fit_and_evaluate(df)
    print(result)
    # TODO STEP 6: Confusion Matrix 시각화 후 outputs/에 저장한다.

if __name__ == "__main__":
    main()
