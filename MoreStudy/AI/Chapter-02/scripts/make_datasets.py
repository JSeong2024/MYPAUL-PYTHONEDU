"""Chapter 02 합성 데이터를 동일한 난수 시드로 재생성합니다."""
from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def generate(seed: int = 20261108) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    n = 180
    distance = rng.uniform(0.5, 15.0, n)
    stops = rng.integers(0, 7, n)
    duration = 4.5 + 3.2 * distance + 1.8 * stops + rng.normal(0, 2.0, n)
    delivery = pd.DataFrame({
        "order_id": [f"D{i + 1:04d}" for i in range(n)],
        "distance_km": np.round(distance, 3),
        "stops": stops,
        "duration_min": np.round(duration, 2),
    })

    n = 240
    vibration = rng.uniform(0, 4, n)
    ambient = rng.uniform(100, 12000, n)
    fault = (vibration + rng.normal(0, 0.22, n) >= 2.0).astype(int)
    sensor = pd.DataFrame({
        "sample_id": [f"S{i + 1:04d}" for i in range(n)],
        "vibration_mm_s": np.round(vibration, 4),
        "ambient_lux": np.round(ambient, 1),
        "fault_label": fault,
    })

    n = 320
    temperature = rng.uniform(9, 33, n)
    floor_area = rng.uniform(40, 250, n)
    occupancy = rng.integers(1, 13, n)
    usage = (
        1.1 * floor_area + 2.5 * np.abs(temperature - 21)
        + 8 * occupancy + rng.normal(0, 10, n)
    )
    # 측정 종료 후 확정된 수치이므로 예측 시점에는 사용할 수 없습니다.
    finalized = usage + rng.normal(0, 0.12, n)
    energy = pd.DataFrame({
        "record_id": [f"E{i + 1:04d}" for i in range(n)],
        "temperature_c": np.round(temperature, 3),
        "floor_area_m2": np.round(floor_area, 2),
        "occupancy": occupancy,
        "energy_kwh": np.round(usage, 2),
        "meter_finalized_kwh": np.round(finalized, 2),
    })
    return {
        "delivery_times.csv": delivery,
        "sensor_signals.csv": sensor,
        "energy_usage.csv": energy,
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, frame in generate().items():
        destination = DATA_DIR / filename
        frame.to_csv(destination, index=False)
        print(f"{filename}: {len(frame)} rows")


if __name__ == "__main__":
    main()
