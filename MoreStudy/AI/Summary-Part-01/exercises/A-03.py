"""A-03 — Unlabeled Usage Pattern Analysis (Starter Code).

입력: space_usage.csv
출력: invalid_rows.csv, cluster_assignments.csv, cluster_profiles.csv, report.md
문제 원문: ../problem.md의 A-03 절
"""
from pathlib import Path
import pandas as pd

from sklearn.cluster import KMeans

def main() -> None:
    # STEP 1: 유효값·중복 ID 검사, CSV 원본 행 번호 보존
    # STEP 2: 정상 데이터 StandardScaler, KMeans 및 DBSCAN
    # STEP 3: 노이즈(-1)까지 원본 단위 평균으로 프로파일링
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
