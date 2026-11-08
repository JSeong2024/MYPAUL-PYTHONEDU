"""Mini Project 01 — 완성된 함수가 아니며 TODO를 구현해야 합니다."""
from pathlib import Path
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[2]
COLUMNS = ['sensor_01', 'sensor_02', 'sensor_03', 'sensor_04']
FACTORS = [1.00, 0.98, 1.03, 1.01]


def analyze_sensor_file(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    # TODO: 필수 열·중복 day·숫자 범위·-1 결측 표시 검사
    readings = torch.tensor(frame[COLUMNS].to_numpy(dtype='float32'))
    factors = torch.tensor(FACTORS, dtype=torch.float32)
    # TODO: [N,4] * [4] Broadcasting으로 교정값 계산
    # TODO: -1은 평균과 최대값에서 제외, 모든 행이 -1인 센서는 오류
    # TODO: valid_count, mean_calibrated, max_calibrated, high_count(>=65) 집계
    raise NotImplementedError('Finish analyze_sensor_file')


if __name__ == '__main__':
    result = analyze_sensor_file(ROOT / 'data/sensor_readings.csv')
    out = ROOT / 'outputs/mini_01'
    out.mkdir(parents=True, exist_ok=True)
    result.to_csv(out / 'sensor_summary.csv', index=False)
