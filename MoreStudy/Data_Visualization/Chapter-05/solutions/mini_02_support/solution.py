from pathlib import Path
import json, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from project_utils.eda import valid_response_times

def run(output=None,source=None):
    raw=pd.read_csv(source or ROOT/'data/support_tickets.csv')
    valid=valid_response_times(raw)
    out=Path(output or ROOT/'output/mini_02_support');out.mkdir(parents=True,exist_ok=True)
    grouped=valid.groupby('priority',as_index=False).agg(n=('first_response_min','size'),median=('first_response_min','median'),p90=('first_response_min',lambda s:s.quantile(.9)),sla_60=('first_response_min',lambda s:float((s<=60).mean())))
    order=['High','Normal','Low']
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    sns.histplot(data=valid,x='first_response_min',bins=35,ax=axes[0,0],color='#4B7BB4')
    axes[0,0].set(xlim=(0,250),title='First response time distribution',xlabel='Minutes')
    sns.ecdfplot(data=valid,x='first_response_min',hue='priority',hue_order=order,ax=axes[0,1])
    axes[0,1].set(xlim=(0,250),title='Cumulative share',xlabel='Minutes')
    sns.boxplot(data=valid,x='priority',y='first_response_min',order=order,ax=axes[1,0],color='#93A8D0')
    axes[1,0].set(ylim=(0,250),title='Response by priority',ylabel='Minutes')
    sns.barplot(data=grouped,x='priority',y='sla_60',order=order,ax=axes[1,1],errorbar=None,color='#549E94')
    axes[1,1].set(ylim=(0,1),ylabel='Share answered within 60 min',title='60-minute benchmark')
    fig.suptitle('Support Response Study')
    fig.savefig(out/'report.png',dpi=140);plt.close(fig)
    grouped.to_csv(out/'priority_summary.csv',index=False)
    result={'raw_count':int(len(raw)),'valid_count':int(len(valid)),'median_min':float(valid.first_response_min.median()), 'p90_min':float(valid.first_response_min.quantile(.9))}
    (out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':print(run())
