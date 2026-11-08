"""Mini 01 — Sensor Tensor Quality Report."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
SENSORS = ['sensor_01', 'sensor_02', 'sensor_03', 'sensor_04']
FACTORS = [1.00, 0.98, 1.03, 1.01]


def analyze_sensor_file(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if list(frame.columns) != ['day', *SENSORS]:
        raise ValueError('Expected day and sensor_01..sensor_04 columns in order')
    if frame.empty or frame['day'].isna().any() or frame['day'].duplicated().any():
        raise ValueError('day must be present and unique')
    try:
        values = frame[SENSORS].apply(pd.to_numeric, errors='raise').to_numpy(dtype='float32')
    except (ValueError, TypeError) as exc:
        raise ValueError('Sensor readings must be numeric') from exc
    readings = torch.from_numpy(values.copy())
    if not bool(torch.isfinite(readings).all()):
        raise ValueError('Sensor readings must be finite')
    if bool(((readings < 0) & (readings != -1)).any()):
        raise ValueError('Only -1 may indicate a missing sensor reading')
    valid = readings >= 0
    counts = valid.sum(dim=0)
    if bool((counts == 0).any()):
        raise ValueError('Every sensor requires at least one valid reading')
    calibrated = readings * torch.tensor(FACTORS, dtype=readings.dtype)
    zeroed = torch.where(valid, calibrated, torch.zeros_like(calibrated))
    averages = zeroed.sum(dim=0) / counts
    highest = torch.where(valid, calibrated, torch.full_like(calibrated, -torch.inf)).max(dim=0).values
    high_count = (valid & (calibrated >= 65)).sum(dim=0)
    rows = []
    for i, sensor in enumerate(SENSORS):
        rows.append({
            'sensor_id': sensor,
            'valid_count': int(counts[i]),
            'mean_calibrated': round(float(averages[i]), 3),
            'max_calibrated': round(float(highest[i]), 3),
            'high_count': int(high_count[i]),
        })
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description='Sensor readings tensor report')
    parser.add_argument('--input', type=Path, default=ROOT / 'data/sensor_readings.csv')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'outputs/mini_01')
    args = parser.parse_args()
    result = analyze_sensor_file(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output_dir / 'sensor_summary.csv', index=False)
    print(result.to_string(index=False))


if __name__ == '__main__':
    main()
