from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'shipments.csv'


def run():
    raw = pd.read_csv(DATA)
    print('Input rows:', len(raw))
    # TODO: 정상 배송 추출, 정시 비율 계산, 운송사·지역별 2×2 그래프를 구현
    raise NotImplementedError('README의 요구사항에 따라 구현하세요.')


if __name__ == '__main__':
    run()
