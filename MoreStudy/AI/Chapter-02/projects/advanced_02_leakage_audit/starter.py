"""Advanced Project 02 — 예측 시점 기준 Feature 검증."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "energy_usage.csv"


def audit_and_compare(frame: pd.DataFrame) -> dict:
    """사용 가능 Feature와 종료 후 생성된 Feature의 영향 비교."""
    # STEP 1: 열의 의미와 생성 시점을 확인합니다.
    # STEP 2: 예측 시점에 사용 가능한 열만으로 모델을 학습합니다.
    # STEP 3: 종료 후 값까지 포함한 모델을 의도적으로 비교합니다.
    # STEP 4: 동일한 Test Set에서 MAE를 계산합니다.
    # STEP 5: 배포 가능한 모델에 포함할 Feature 목록을 작성합니다.
    raise NotImplementedError


if __name__ == "__main__":
    print(audit_and_compare(pd.read_csv(DATA)))
