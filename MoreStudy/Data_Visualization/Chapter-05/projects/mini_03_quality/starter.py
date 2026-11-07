from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'inspections.csv'


def run():
    raw = pd.read_csv(DATA)
    print('Input rows:', len(raw))
    # TODO: 중복 제거, 측정 검토 상태 기록, 라인별 불량률과 분포 그래프 구현
    raise NotImplementedError('README의 요구사항에 따라 구현하세요.')


if __name__ == '__main__':
    run()
