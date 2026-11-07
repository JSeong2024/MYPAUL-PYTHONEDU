from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'/'server_metrics.csv'
OUTPUT=ROOT/'output'/'mini_03_server'

def build_report(frame:pd.DataFrame):
    fig,axes=plt.subplots(3,1,figsize=(11,9),sharex=True,layout='constrained')
    # TODO: 서비스별 CPU, 메모리, 응답시간 추이를 각각의 Axes에 표현하세요.
    # TODO: 기록이 없는 시간은 0으로 채우지 말고 NaN으로 유지하세요.
    # TODO: CPU 85%, 메모리 90%, 응답시간 450ms 검토선을 그리세요.
    return fig

def main():
    frame=pd.read_csv(DATA,parse_dates=['timestamp'])
    OUTPUT.mkdir(parents=True,exist_ok=True)
    fig=build_report(frame)
    fig.savefig(OUTPUT/'server_performance.png',dpi=150)
    plt.close(fig)
if __name__=='__main__':main()
