"""Advanced 01 — Custom Dataset + DataLoader로 시설 이벤트 집계."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ['hour', 'temperature_c', 'vibration_mm_s']
COLUMNS = ['event_id', 'zone', *FEATURES, 'alert_label']


class FacilityEventDataset(Dataset):
    def __init__(self, csv_path: Path):
        frame = pd.read_csv(csv_path)
        if list(frame.columns) != COLUMNS:
            raise ValueError('Unexpected CSV columns')
        if frame.empty or frame['event_id'].isna().any() or frame['event_id'].duplicated().any():
            raise ValueError('event_id must be present and unique')
        if frame['zone'].isna().any() or (frame['zone'].astype(str).str.strip() == '').any():
            raise ValueError('zone is required')
        try:
            data = torch.tensor(frame[FEATURES].to_numpy(dtype='float32').copy(), dtype=torch.float32)
            labels = torch.tensor(frame['alert_label'].to_numpy(dtype='float64').copy(), dtype=torch.float64)
        except (ValueError, TypeError) as exc:
            raise ValueError('Non-numeric data') from exc
        if not bool(torch.isfinite(data).all() & torch.isfinite(labels).all()):
            raise ValueError('Non-finite feature or label')
        if bool(((data[:, 0] < 0) | (data[:, 0] > 23) | (data[:, 0] != data[:, 0].floor())).any()):
            raise ValueError('hour must be an integer between 0 and 23')
        if bool(((data[:, 1] < -20) | (data[:, 1] > 80) | (data[:, 2] < 0) | (data[:, 2] > 40)).any()):
            raise ValueError('Feature out of range')
        if not bool(((labels == 0) | (labels == 1)).all()):
            raise ValueError('alert_label must be 0 or 1')
        self.features = data
        self.labels = labels.to(torch.int64)
        self.event_ids = frame['event_id'].astype(str).tolist()

    def __len__(self) -> int:
        return len(self.event_ids)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx], self.event_ids[idx]


def summarize_batches(path: Path, batch_size: int = 7) -> tuple[pd.DataFrame, pd.DataFrame]:
    if batch_size < 1:
        raise ValueError('batch_size must be positive')
    dataset = FacilityEventDataset(path)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    rows, events = [], []
    for index, (features, labels, event_ids) in enumerate(loader, start=1):
        rows.append({
            'batch_no': index, 'sample_count': len(features),
            'mean_temperature': round(float(features[:, 1].mean()), 3),
            'mean_vibration': round(float(features[:, 2].mean()), 3),
            'alert_count': int(labels.sum()),
        })
        events.extend({'event_id': eid, 'batch_no': index, 'alert_label': int(label)}
                      for eid, label in zip(event_ids, labels.tolist()))
    return pd.DataFrame(rows), pd.DataFrame(events)


def main():
    parser = argparse.ArgumentParser(description='Facility data loading pipeline')
    parser.add_argument('--input', type=Path, default=ROOT / 'data/facility_events.csv')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'outputs/advanced_01')
    parser.add_argument('--batch-size', type=int, default=7)
    args = parser.parse_args()
    summary, assignments = summarize_batches(args.input, args.batch_size)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output_dir / 'batch_summary.csv', index=False)
    assignments.to_csv(args.output_dir / 'event_assignments.csv', index=False)
    print(summary.to_string(index=False))


if __name__ == '__main__':
    main()
