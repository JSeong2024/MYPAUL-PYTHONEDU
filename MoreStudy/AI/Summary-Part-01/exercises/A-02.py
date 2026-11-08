"""A-02 — Water Consumption Prediction (Starter Code).

입력: daily_water.csv
출력: model_comparison.csv, test_predictions.csv, report.txt
문제 원문: ../problem.md의 A-02 절
"""
from pathlib import Path
import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def main() -> None:
    # STEP 1: 날짜 정렬 후 60/20/잔여 Test로 분할
    # STEP 2: Train에만 Scaler fit, Validation MAE로 alpha 선택
    # STEP 3: Test 예측·Baseline 비교·잔차 출력
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
