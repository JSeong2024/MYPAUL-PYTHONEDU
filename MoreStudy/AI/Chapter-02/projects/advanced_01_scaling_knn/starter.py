"""Advanced Project 01 — KNN의 Feature Scaling 비교."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "sensor_signals.csv"


def compare_scaling(frame: pd.DataFrame) -> dict:
    """Raw / Scaled Accuracy와 예측 변경 건수를 반환합니다."""
    # STEP 1: 입력 유효성을 확인합니다.
    # STEP 2: vibration_mm_s, ambient_lux를 Feature로 분리합니다.
    # STEP 3: 한 번만 Train/Test로 나누어 동일한 Test Set을 유지합니다.
    # STEP 4: KNN과 StandardScaler + KNN Pipeline을 학습합니다.
    # STEP 5: 두 정확도와 서로 다른 예측 건수를 비교합니다.
    raise NotImplementedError


if __name__ == "__main__":
    print(compare_scaling(pd.read_csv(DATA)))
