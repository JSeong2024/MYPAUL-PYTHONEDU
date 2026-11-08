"""P-03 — Workspace Utilization Strategy (Starter Code).

입력: workspace_usage.csv
출력: cluster_assignments.csv, cluster_profiles.csv, stability.csv, report.md
문제 원문: ../problem.md의 P-03 절
"""
from pathlib import Path
import pandas as pd

from sklearn.cluster import KMeans

def main() -> None:
    # STEP 1: 데이터 정제, 동일 공간·주차 중복 제외
    # STEP 2: KMeans(seed=7,21,42) 및 ARI 비교
    # STEP 3: seed=42 기준 Cluster Profile과 운영 제안 3개
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
