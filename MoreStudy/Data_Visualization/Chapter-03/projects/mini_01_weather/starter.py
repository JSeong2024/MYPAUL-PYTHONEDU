from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'/'weather_daily.csv'
OUTPUT=ROOT/'output'/'mini_01_weather'

def build_report(data:pd.DataFrame):
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    # TODO 1: 지역별 기온을 날짜별로 연결하고, 관측 누락은 선이 끊기도록 처리하세요.
    # TODO 2: 지역별 강수량 막대그래프를 추가하세요.
    # TODO 3: 기온과 강수량 산점도, 날짜별 유효 관측 개수 그래프를 추가하세요.
    # TODO 4: 제목, 축 단위, 범례를 설정하고 Figure를 반환하세요.
    return fig

def main():
    data=pd.read_csv(DATA,parse_dates=['date'])
    OUTPUT.mkdir(parents=True,exist_ok=True)
    fig=build_report(data)
    fig.savefig(OUTPUT/'weather_dashboard.png',dpi=150)
    plt.close(fig)
if __name__=='__main__':main()
