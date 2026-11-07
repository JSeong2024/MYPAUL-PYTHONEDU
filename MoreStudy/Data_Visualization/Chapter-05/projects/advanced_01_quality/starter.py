from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'inspections.csv'


def run():
    raw = pd.read_csv(DATA)
    print('Input rows:', len(raw))
    # TODO: 가변 Plant 목록과 예외를 처리하며 자동 보고서 생성
    raise NotImplementedError('README의 요구사항에 따라 구현하세요.')


if __name__ == '__main__':
    run()
