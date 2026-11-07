from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'/'subway_ridership.csv'
CATALOG=ROOT/'data'/'subway_stations.csv'
HOURS=list(range(5,24))

def validate(raw:pd.DataFrame,catalog:pd.DataFrame):
    # TODO 1: 중복 역사/날짜/시간대, 비숫자, 음수 관측을 제외 이유와 함께 분리하세요.
    # TODO 2: 올바른 승하차 건수는 정수로 변환하세요.
    raise NotImplementedError('Implement input validation')

def build_reports(valid:pd.DataFrame,rejected:pd.DataFrame,catalog:pd.DataFrame,
                  selected:list[str],output:Path):
    # TODO 3: 역사×날짜×시간대의 예상 관측 슬롯을 생성하고 원본 관측과 결합하세요.
    # TODO 4: 역별 순위, 시간대별 프로필, 히트맵, 동적 다중 그래프를 생성하세요.
    # TODO 5: 누락 커버리지, 제외 행 및 보고서 수치를 CSV/JSON으로 저장하세요.
    raise NotImplementedError('Implement ridership reporting')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stations',nargs='*')
    p.add_argument('--output',type=Path,default=ROOT/'output'/'advanced_02_subway')
    a=p.parse_args()
    raw=pd.read_csv(DATA,dtype=str,keep_default_na=False)
    catalog=pd.read_csv(CATALOG,dtype=str)
    valid,rejected=validate(raw,catalog)
    print(build_reports(valid,rejected,catalog,a.stations or list(catalog['station_id']),a.output))
if __name__=='__main__':main()
