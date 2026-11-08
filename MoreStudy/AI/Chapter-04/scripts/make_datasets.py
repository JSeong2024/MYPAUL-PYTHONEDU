"""Chapter 04: 재현 가능한 실습용 합성 데이터 생성."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def generate_alerts():
    rng = np.random.default_rng(404)
    n = 720
    temperature = rng.normal(66, 14, n).clip(20, 110)
    vibration = rng.gamma(shape=2.4, scale=1.5, size=n).clip(0, 18)
    current = rng.normal(12.5, 3.2, n).clip(2, 26)
    operation_hours = rng.uniform(10, 1600, n)
    score = (-7.6 + .037 * temperature + .40 * vibration + .095 * current
             + .00032 * operation_hours + rng.normal(0, .75, n))
    p = 1 / (1 + np.exp(-score))
    flagged = rng.binomial(1, p)
    return pd.DataFrame({
        "alert_id": [f"AL{i:04d}" for i in range(1, n + 1)],
        "temperature_c": np.round(temperature, 3),
        "vibration_mm_s": np.round(vibration, 3),
        "current_a": np.round(current, 3),
        "operation_hours": np.round(operation_hours, 2),
        "flagged": flagged,
    })


def generate_delivery():
    rng = np.random.default_rng(405)
    n = 560
    distance = rng.uniform(1, 22, n)
    stops = rng.integers(0, 7, n)
    traffic = rng.uniform(.1, 1., n)
    predicted = 6 + 2.85 * distance + 3.1 * stops + 17 * traffic
    minutes = np.maximum(1., predicted + rng.normal(0, 5., n))
    return pd.DataFrame({
        "delivery_id": [f"DL{i:04d}" for i in range(1, n + 1)],
        "distance_km": np.round(distance, 3),
        "stop_count": stops,
        "traffic_index": np.round(traffic, 3),
        "actual_minutes": np.round(minutes, 2),
    })


def generate_curve():
    rng = np.random.default_rng(406)
    x = rng.uniform(-3, 3, 80)
    y = np.sin(1.3 * x) + .17 * x + rng.normal(0, .33, len(x))
    return pd.DataFrame({
        "sample_id": [f"CV{i:04d}" for i in range(1, len(x) + 1)],
        "input_x": np.round(x, 6),
        "target_y": np.round(y, 6),
    })


def generate_devices():
    rng = np.random.default_rng(407)
    n_devices, per_device = 100, 6
    # 실제 예측에 투입해서는 안 되는 기기별 식별 신호를 일부러 포함한다.
    fingerprints = np.sort(rng.uniform(0, 10000, n_devices))
    labels = rng.integers(0, 2, n_devices)
    records = []
    for i in range(n_devices):
        for cycle in range(per_device):
            records.append({
                "device_id": f"DV{i + 1:03d}",
                "cycle_no": cycle + 1,
                "fingerprint_signal": round(float(fingerprints[i]), 5),
                "temperature_c": round(float(rng.normal(65, 9)), 3),
                "maintenance_flag": int(labels[i]),
            })
    return pd.DataFrame(records)


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    generate_alerts().to_csv(DATA / "incident_alerts.csv", index=False)
    generate_delivery().to_csv(DATA / "delivery_times.csv", index=False)
    generate_curve().to_csv(DATA / "curve_measurements.csv", index=False)
    generate_devices().to_csv(DATA / "device_cycles.csv", index=False)
    print("Created 4 synthetic datasets")


if __name__ == "__main__":
    main()
