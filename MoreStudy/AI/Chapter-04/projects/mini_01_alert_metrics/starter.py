"""Mini 01: Accuracy만으로 놓칠 수 있는 사건을 평가한다."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
FEATURES = ["temperature_c", "vibration_mm_s", "current_a", "operation_hours"]


def load_data(path=ROOT / "data/incident_alerts.csv"):
    """TODO: 필수 열·식별자 중복·결측값·음수·Label 검증."""
    df = pd.read_csv(path)
    raise NotImplementedError


def measure(y_true, y_pred):
    """TODO: TN, FP, FN, TP와 여섯 평가 지표를 반환."""
    raise NotImplementedError


def evaluate(df):
    """TODO: 동일한 Test Data에서 Dummy/Logistic 모델을 비교."""
    # train_test_split(..., stratify=y, test_size=.25, random_state=42)
    # make_pipeline(StandardScaler(), LogisticRegression(...))
    raise NotImplementedError


def plot_result(result):
    """TODO: 지표 그래프·Confusion Matrix를 outputs/에 저장."""
    raise NotImplementedError


def main():
    result = evaluate(load_data())
    print(result)
    print(plot_result(result))


if __name__ == "__main__":
    main()
