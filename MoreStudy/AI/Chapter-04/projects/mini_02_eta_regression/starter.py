"""Mini 02: Baseline과 Ridge Regression을 같은 Test Data로 평가한다."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
FEATURES = ["distance_km", "stop_count", "traffic_index"]


def load_data(path=ROOT / "data/delivery_times.csv"):
    """TODO: 필수 열·중복 ID·결측값·유한성·유효 범위 검사."""
    df = pd.read_csv(path)
    raise NotImplementedError


def regression_metrics(y_true, predicted):
    """TODO: MAE, MSE, RMSE, R²를 dict로 반환."""
    raise NotImplementedError


def evaluate(df):
    """TODO: 분할·Median Baseline·Ridge·Training CV 평가."""
    # make_pipeline(StandardScaler(), Ridge(alpha=3.0))
    raise NotImplementedError


def plot_result(result):
    """TODO: Actual vs Predicted, Residual 그래프를 저장."""
    raise NotImplementedError


def main():
    result=evaluate(load_data())
    print(result)
    print(plot_result(result))


if __name__ == "__main__":
    main()
