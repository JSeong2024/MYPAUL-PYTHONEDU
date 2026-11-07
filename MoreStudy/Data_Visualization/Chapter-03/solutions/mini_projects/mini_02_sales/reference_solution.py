"""Mini Project 02 — store sales chart report (synthetic figures)."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
DATA=ROOT/'data'/'store_sales.csv'

def load_data(path:Path=DATA)->pd.DataFrame:
    frame=pd.read_csv(path,parse_dates=['date'])
    required={'date','store','category','orders','revenue_krw'}
    if not required.issubset(frame.columns):raise ValueError('Missing sales columns')
    if frame[['date','store','category']].duplicated().any():raise ValueError('Duplicate sales key')
    if frame[['orders','revenue_krw']].isna().any().any() or (frame[['orders','revenue_krw']]<0).any().any():
        raise ValueError('Invalid sales numbers')
    return frame

def make_report(frame:pd.DataFrame,output:Path)->dict:
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    by_day=frame.groupby('date')['revenue_krw'].sum().sort_index()
    by_store=frame.groupby('store')['revenue_krw'].sum().sort_values(ascending=False)
    by_cat=frame.groupby('category')['revenue_krw'].sum().sort_values()
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    axes[0,0].plot(by_day.index,by_day.values,marker='.',markersize=4)
    axes[0,0].set(title='Daily Revenue',ylabel='KRW/day')
    axes[0,0].tick_params(axis='x',labelrotation=30)
    bars=axes[0,1].bar(by_store.index,by_store.values)
    axes[0,1].bar_label(bars,fmt='%.0f',padding=3,fontsize=8)
    axes[0,1].set(title='Revenue by Store',ylabel='KRW',ylim=(0,max(by_store)*1.24))
    bars=axes[1,0].barh(by_cat.index,by_cat.values)
    axes[1,0].bar_label(bars,fmt='%.0f',padding=3,fontsize=8)
    axes[1,0].set(title='Revenue by Category',xlabel='KRW',xlim=(0,max(by_cat)*1.3))
    axes[1,1].hist(by_day.values,bins=7,edgecolor='white')
    axes[1,1].set(title='Distribution of Daily Revenue',xlabel='KRW/day',ylabel='Days')
    highest=by_day.idxmax()
    axes[0,0].annotate('Highest',xy=(highest,by_day.loc[highest]),xytext=(0,16),textcoords='offset points',ha='center',arrowprops=dict(arrowstyle='->'))
    fig.suptitle('Store Sales Snapshot — Synthetic Data',fontsize=15)
    fig.savefig(output/'store_sales_report.png',dpi=145)
    plt.close(fig)
    summary={'days':int(by_day.size),'stores':int(by_store.size),'categories':int(by_cat.size),
             'total_revenue_krw':int(frame['revenue_krw'].sum()),'highest_revenue_date':str(highest.date())}
    (output/'sales_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary

def main():
    summary=make_report(load_data(),ROOT/'output'/'mini_02_sales')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
