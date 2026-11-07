from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data'/'store_sales.csv'
OUTPUT=ROOT/'output'/'mini_02_sales'

def build_report(frame:pd.DataFrame):
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    # TODO: 날짜별 매출 선 그래프, 매장별 매출 막대그래프,
    #       분류별 매출 가로 막대그래프, 일별 매출 히스토그램을 구현하세요.
    # TODO: 최고 매출일에 주석을 추가하세요.
    return fig

def main():
    frame=pd.read_csv(DATA,parse_dates=['date'])
    OUTPUT.mkdir(parents=True,exist_ok=True)
    fig=build_report(frame)
    fig.savefig(OUTPUT/'store_sales_report.png',dpi=150)
    plt.close(fig)
if __name__=='__main__':main()
