"""Advanced Project 01 — Custom Dataset과 DataLoader 구현."""
from pathlib import Path
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

ROOT = Path(__file__).resolve().parents[2]
FEATURES = ['hour', 'temperature_c', 'vibration_mm_s']


class FacilityEventDataset(Dataset):
    def __init__(self, csv_path: Path):
        frame = pd.read_csv(csv_path)
        # TODO: 필수 열, 중복 event_id, NaN/inf, Feature 범위, Label(0/1) 검증
        self.features = torch.tensor(frame[FEATURES].to_numpy(dtype='float32'))
        self.labels = torch.tensor(frame['alert_label'].to_numpy(dtype='int64'))
        self.event_ids = frame['event_id'].tolist()

    def __len__(self):
        # TODO: 전체 샘플 수
        raise NotImplementedError

    def __getitem__(self, idx):
        # TODO: 특징 텐서, 레이블, 원본 ID 반환
        raise NotImplementedError


def summarize_batches(path: Path, batch_size: int = 7):
    dataset = FacilityEventDataset(path)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    # TODO: 배치별 sample_count, mean_temperature, mean_vibration, alert_count
    # TODO: 원본 event_id와 batch_no를 보존하는 결과 생성
    raise NotImplementedError


if __name__ == '__main__':
    print(summarize_batches(ROOT / 'data/facility_events.csv'))
