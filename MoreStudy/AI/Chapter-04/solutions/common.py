"""프로젝트가 공유하는 입력 검증 함수."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ALERT_FEATURES = ["temperature_c", "vibration_mm_s", "current_a", "operation_hours"]
ETA_FEATURES = ["distance_km", "stop_count", "traffic_index"]


def validated_csv(path, required, id_column=None, numeric=(), nonnegative=(), binary=None):
    df = pd.read_csv(path)
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"필수 열 누락: {sorted(missing)}")
    if df[required].isna().any().any() or not len(df):
        raise ValueError("결측값 또는 빈 데이터셋")
    if id_column and df[id_column].duplicated().any():
        raise ValueError("중복 식별자")
    for col in numeric:
        try:
            values = pd.to_numeric(df[col], errors="raise").to_numpy(dtype=float)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"유효하지 않은 수치: {col}") from exc
        if not np.isfinite(values).all():
            raise ValueError(f"무한대 또는 NaN: {col}")
        if col in nonnegative and (values < 0).any():
            raise ValueError(f"음수 값: {col}")
        df[col] = pd.to_numeric(df[col], errors="raise")
    if binary is not None and not df[binary].isin([0, 1]).all():
        raise ValueError(f"레이블은 0과 1만 허용: {binary}")
    return df


def load_alerts(path=ROOT / "data/incident_alerts.csv"):
    required = ["alert_id", *ALERT_FEATURES, "flagged"]
    df = validated_csv(path, required, "alert_id", [*ALERT_FEATURES, "flagged"], ALERT_FEATURES, "flagged")
    if df.flagged.nunique() != 2 or min(df.flagged.value_counts()) < 5:
        raise ValueError("클래스별 샘플이 부족합니다.")
    return df


def load_delivery(path=ROOT / "data/delivery_times.csv"):
    cols = ["delivery_id", *ETA_FEATURES, "actual_minutes"]
    df = validated_csv(path, cols, "delivery_id", [*ETA_FEATURES, "actual_minutes"], cols[1:])
    if (df.actual_minutes <= 0).any():
        raise ValueError("배송 시간은 양수여야 합니다.")
    return df


def load_curve(path=ROOT / "data/curve_measurements.csv"):
    cols = ["sample_id", "input_x", "target_y"]
    return validated_csv(path, cols, "sample_id", cols[1:])


def load_devices(path=ROOT / "data/device_cycles.csv"):
    cols = ["device_id", "cycle_no", "fingerprint_signal", "temperature_c", "maintenance_flag"]
    df = validated_csv(path, cols, numeric=cols[1:], nonnegative=["cycle_no", "fingerprint_signal"], binary="maintenance_flag")
    if df.device_id.nunique() < 10:
        raise ValueError("최소 10개 장비가 필요합니다.")
    # 같은 장비의 Target이 서로 다른 상태라면 이 실험의 가정과 맞지 않는다.
    if (df.groupby("device_id").maintenance_flag.nunique() > 1).any():
        raise ValueError("장비별 Label이 일관되지 않습니다.")
    if df.maintenance_flag.nunique() != 2:
        raise ValueError("두 클래스가 모두 필요합니다.")
    return df
