"""R-01 — The City That Never Sleeps (Starter Code).

입력: facilities.csv, daily_operations.csv, incoming_operations.csv
출력: results/ (10 analysis outputs)
문제 원문: ../problem.md의 R-01 절
"""
from pathlib import Path
import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.cluster import KMeans

from sklearn.linear_model import LogisticRegression

def main() -> None:
    # STEP 1: 시설 참조 무결성, 일별 행 검증과 중복 처리
    # STEP 2: 7일 Gap + 신규시설 Holdout 평가 A/B
    # STEP 3: F2 Threshold, Ridge alpha, KMeans 3개 분리 학습
    # STEP 4: 운영 점검 한도(지역·날짜 10건) 및 미선택 이유 기록
    # STEP 5: 원자적 결과 디렉터리 교체, 100k행 성능 비교
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
