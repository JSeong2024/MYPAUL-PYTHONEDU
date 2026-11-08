"""Advanced 01: Validation F2로 Threshold를 선택하고 Test로 평가한다."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import fbeta_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
FEATURES = ["temperature_c", "vibration_mm_s", "current_a", "operation_hours"]
THRESHOLDS = np.round(np.arange(.05,.951,.05),2)


def load_data(path=ROOT / "data/incident_alerts.csv"):
    """TODO: 데이터 검증."""
    df = pd.read_csv(path)
    raise NotImplementedError


def choose_threshold(y_val, probabilities, thresholds=THRESHOLDS):
    """TODO: Validation F2 최대화. 동률이면 더 큰 Threshold."""
    # fbeta_score(..., beta=2, zero_division=0)
    raise NotImplementedError


def evaluate(df):
    """TODO: Test 분리 -> Train/Validation -> 선택 -> Test 최종 평가."""
    # Test는 Threshold를 선택한 뒤에만 사용해야 합니다.
    raise NotImplementedError


def plot_result(result):
    """TODO: Threshold별 Validation F2와 선택 기준선을 저장."""
    raise NotImplementedError


def main():
    result=evaluate(load_data())
    print(result)
    print(plot_result(result))


if __name__ == "__main__":
    main()
