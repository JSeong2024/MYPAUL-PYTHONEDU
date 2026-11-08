"""P-02 — Municipal Waste Demand Prediction (Starter Code).

입력: weekly_waste.csv
출력: test_predictions.csv, zone_metrics.csv, underprediction_top5.csv, report.md
문제 원문: ../problem.md의 P-02 절
"""
from pathlib import Path
import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def main() -> None:
    # STEP 1: 주차·구역별 무결성, 고유 주차 Temporal Split
    # STEP 2: StandardScaler + Ridge; Validation MAE로 alpha 선택
    # STEP 3: Test Baseline 비교·구역별 MAE·과소 예측 5건
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
