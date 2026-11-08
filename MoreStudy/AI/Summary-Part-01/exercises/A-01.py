"""A-01 — Visitor Congestion Classification (Starter Code).

입력: validation_scores.csv, test_scores.csv
출력: threshold_report.csv, test_report.txt
문제 원문: ../problem.md의 A-01 절
"""
from pathlib import Path
import pandas as pd

def main() -> None:
    # STEP 1: 두 CSV의 스키마·식별자·값 범위 검증
    # STEP 2: Validation F1로 Threshold 선정, 동점 시 더 큰 값
    # STEP 3: 선택된 Threshold로 Test를 한 번만 평가하고 파일 생성
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
