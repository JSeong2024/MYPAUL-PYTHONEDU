"""C-01 — Equipment Failure Model Audit (Starter Code).

입력: equipment_history.csv
출력: data_audit.csv, split_audit.json, metric_comparison.csv, error_by_device.csv, root_cause_report.md
문제 원문: ../problem.md의 C-01 절
"""
from pathlib import Path
import pandas as pd

from sklearn.linear_model import LogisticRegression

def main() -> None:
    # STEP 1: 금지된 최종 수리 코드를 입력 특성에서 제거
    # STEP 2: Random vs Group Split 차이 분석; GroupKFold 선택
    # STEP 3: Train-only Imputer/Scaler, 설비별 FP/FN 및 테스트
    raise NotImplementedError("TODO: main() 구현")


if __name__ == "__main__":
    main()
