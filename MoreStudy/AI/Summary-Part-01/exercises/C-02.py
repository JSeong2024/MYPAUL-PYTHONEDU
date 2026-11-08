"""C-02 — Library Demand Forecast Recovery (Starter Code).

입력: history_v1.csv, incoming_v2.csv
출력: results/normalized_incoming.csv, rejected_rows.csv, predictions.csv, recovery_report.md
문제 원문: ../problem.md의 C-02 절
"""
from pathlib import Path
import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def main() -> None:
    # STEP 1: history_v1 섭씨 / incoming_v2 화씨 스키마 명시
    # STEP 2: 무효 행이 날짜를 점유하지 않도록 검증, 화씨 → 섭씨
    # STEP 3: 시계열 경계 Target 누출 차단; 결과 스테이징 후 교체
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
