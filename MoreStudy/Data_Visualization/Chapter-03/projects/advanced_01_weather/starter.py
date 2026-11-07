from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'/'weather_stations.csv'

def validate(frame:pd.DataFrame)->pd.DataFrame:
    # TODO 1: 필수 열, 중복 관측, 유효 범위를 검사하세요.
    return frame

def generate_report(frame:pd.DataFrame,selected:list[str],output:Path)->dict:
    # TODO 2: 선택한 관측소 수에 따라 subplot 행/열을 자동 계산하세요.
    # TODO 3: 관측 없는 날짜를 NaN으로 유지하고 모든 기온 그래프에 동일한 y축을 사용하세요.
    # TODO 4: 관측소별 커버리지 보고서, PNG 및 JSON을 저장하세요.
    raise NotImplementedError('Implement the multi-station weather report')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stations',nargs='*')
    parser.add_argument('--output',type=Path,default=ROOT/'output'/'advanced_01_weather')
    args=parser.parse_args()
    frame=validate(pd.read_csv(DATA,parse_dates=['date']))
    print(generate_report(frame,args.stations or sorted(frame['site_id'].unique()),args.output))
if __name__=='__main__':main()
