"""P-01 — Warranty Repair Triage (Starter Code).

입력: historical_claims.csv, incoming_claims.csv
출력: evaluation.json, daily_review_queue.csv, incoming_decisions.csv, invalid_claims.csv, report.md
문제 원문: ../problem.md의 P-01 절
"""
from pathlib import Path
import pandas as pd

from sklearn.linear_model import LogisticRegression

def main() -> None:
    # STEP 1: 날짜·정수형 Feature 및 제품 ID 검증
    # STEP 2: 제품 단위 분할 → Baseline+Logistic Regression
    # STEP 3: Validation F2(동점이면 큰 Threshold) → Test 및 날짜별 3건 큐
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
