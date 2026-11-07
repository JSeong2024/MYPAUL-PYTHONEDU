"""Mini Project: 온도 센서 행렬의 품질 검사와 집계 및 CSV 출력."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "weekly_temperatures.csv"
OUTPUT = ROOT / "output" / "sensor_summary.csv"
SENSOR_NAMES = ("ST-01", "ST-02", "ST-03", "ST-04")

def analyze_measurements(raw: np.ndarray) -> dict:
    """행=날짜, 열=센서인 2차원 측정값을 검사합니다."""
    readings = np.asarray(raw, dtype=np.float64)
    if readings.ndim != 2 or readings.shape[1] != len(SENSOR_NAMES):
        raise ValueError("(날짜 수, 4) 형태의 입력이 필요합니다.")
    if readings.shape[0] == 0:
        raise ValueError("측정 날짜가 하나 이상 필요합니다.")

    missing = readings == -999.0
    out_of_range = (~np.isfinite(readings) | (readings < 0) | (readings > 45)) & ~missing
    valid = ~missing & ~out_of_range
    if not np.all(valid.any(axis=0)) or not np.all(valid.any(axis=1)):
        raise ValueError("각 날짜와 센서에 유효한 값이 하나 이상 필요합니다.")

    clean = np.where(valid, readings, np.nan)
    alarms = valid & (readings > 30)
    return {
        "raw_count": readings.size,
        "missing_count": int(np.count_nonzero(missing)),
        "range_error_count": int(np.count_nonzero(out_of_range)),
        "valid_count": int(np.count_nonzero(valid)),
        "alarm_count": int(np.count_nonzero(alarms)),
        "daily_mean": np.nanmean(clean, axis=1),
        "sensor_mean": np.nanmean(clean, axis=0),
        "sensor_alarm_count": np.count_nonzero(alarms, axis=0),
    }

def load_data(path: Path = INPUT) -> np.ndarray:
    return np.loadtxt(path, delimiter=",", skiprows=1, usecols=(1, 2, 3, 4))

def save_report(stats: dict, path: Path = OUTPUT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    report = np.column_stack((
        np.arange(1, len(SENSOR_NAMES) + 1),
        stats["sensor_mean"],
        stats["sensor_alarm_count"],
    ))
    np.savetxt(
        path, report, delimiter=",", fmt=["%d", "%.2f", "%d"],
        header="sensor_number,mean_temperature_c,alarm_count", comments="",
        encoding="utf-8",
    )

def main() -> None:
    raw = load_data()
    stats = analyze_measurements(raw)
    save_report(stats)
    print("원본 측정값:", stats["raw_count"])
    print("결측(-999):", stats["missing_count"])
    print("범위 오류:", stats["range_error_count"])
    print("유효 측정값:", stats["valid_count"])
    print("30°C 초과 경보:", stats["alarm_count"])
    print("일별 평균(°C):", np.round(stats["daily_mean"], 2))
    print("센서별 평균(°C):", np.round(stats["sensor_mean"], 2))
    print("센서별 경보 횟수:", stats["sensor_alarm_count"])
    print("저장:", OUTPUT.relative_to(ROOT).as_posix())

if __name__ == "__main__":
    main()
