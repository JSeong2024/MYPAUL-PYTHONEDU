from pathlib import Path
import json, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from project_utils.eda import valid_deliveries

def run(output=None, source=None):
    data=pd.read_csv(source or ROOT/'data/shipments.csv')
    valid=valid_deliveries(data)
    out=Path(output or ROOT/'output/mini_01_delivery');out.mkdir(parents=True,exist_ok=True)
    by_zone=valid.groupby('zone',as_index=False).agg(n=('on_time','size'), rate=('on_time','mean'),average_days=('actual_days','mean'))
    by_carrier=valid.groupby('carrier',as_index=False).agg(n=('on_time','size'),rate=('on_time','mean'))
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    sns.histplot(data=valid,x='actual_days',bins=20,ax=axes[0,0],color='#3475B5')
    axes[0,0].set(xlabel='Actual days',title='Delivery duration')
    sns.boxplot(data=valid,x='zone',y='actual_days',order=['Urban','Suburban','Remote'],ax=axes[0,1],color='#71A6D2')
    axes[0,1].set(xlabel='Zone',ylabel='Actual days',title='Delivery days by zone')
    sns.barplot(data=by_zone,x='zone',y='rate',order=['Urban','Suburban','Remote'],ax=axes[1,0],color='#4F9889',errorbar=None)
    axes[1,0].set(ylim=(0,1),ylabel='On-time rate',title='On-time rate by zone')
    sns.barplot(data=by_carrier,x='carrier',y='rate',ax=axes[1,1],color='#BB8D67',errorbar=None)
    axes[1,1].set(ylim=(0,1),ylabel='On-time rate',title='On-time rate by carrier')
    fig.suptitle('Delivery Reliability Review')
    fig.savefig(out/'report.png',dpi=140);plt.close(fig)
    by_zone.to_csv(out/'zone_summary.csv',index=False)
    by_carrier.to_csv(out/'carrier_summary.csv',index=False)
    summary={'raw_count':int(len(data)),'valid_count':int(len(valid)), 'excluded_count':int(len(data)-len(valid)), 'on_time_rate':float(valid.on_time.mean())}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    return summary

if __name__=='__main__': print(run())
