"""Mini Project 03 — server performance trends. Not a fault-diagnosis system."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
DATA=ROOT/'data'/'server_metrics.csv'
SERVICES=('API','Web','Jobs')

def load_data(path:Path=DATA)->pd.DataFrame:
    frame=pd.read_csv(path,parse_dates=['timestamp'])
    if not {'timestamp','service','cpu_pct','memory_pct','response_ms'}.issubset(frame.columns):
        raise ValueError('Missing server columns')
    if frame[['timestamp','service']].duplicated().any():raise ValueError('Duplicate service-time slot')
    if not set(frame['service']).issubset(SERVICES):raise ValueError('Unknown service')
    for col in ['cpu_pct','memory_pct']:
        if frame[col].isna().any() or not frame[col].between(0,100).all():
            raise ValueError('Invalid percentage')
    numeric=pd.to_numeric(frame['response_ms'],errors='coerce')
    if (frame['response_ms'].notna() & numeric.isna()).any():raise ValueError('Invalid response time')
    frame['response_ms']=numeric
    if frame['response_ms'].dropna().lt(0).any():raise ValueError('Invalid response time')
    return frame

def make_report(frame:pd.DataFrame,output:Path)->dict:
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    hours=pd.date_range(frame['timestamp'].min(),frame['timestamp'].max(),freq='h')
    fig,axes=plt.subplots(3,1,figsize=(11,9),sharex=True,layout='constrained')
    for service in SERVICES:
        part=frame.loc[frame['service']==service].set_index('timestamp').sort_index().reindex(hours)
        axes[0].plot(hours,part['cpu_pct'],label=service,linewidth=1.8)
        axes[1].plot(hours,part['memory_pct'],label=service,linewidth=1.8)
        axes[2].plot(hours,part['response_ms'],label=service,linewidth=1.8)
    for ax,name,unit,limit in zip(axes,['CPU Usage','Memory Usage','Response Time'],['%','%','ms'],[85,90,450]):
        ax.axhline(limit,linestyle='--',linewidth=1,color='firebrick',label=f'Review {limit}{unit}')
        ax.set(title=name,ylabel=unit)
        ax.grid(alpha=.2)
    axes[0].legend(ncol=4,fontsize=8)
    axes[-1].set_xlabel('Timestamp')
    axes[-1].tick_params(axis='x',labelrotation=30)
    fig.suptitle('Server Metrics — Synthetic Data',fontsize=15)
    fig.savefig(output/'server_performance.png',dpi=145)
    plt.close(fig)
    expected=len(hours)*len(SERVICES)
    summary={'expected_slots':int(expected),'observed_rows':len(frame),
             'missing_slots':int(expected-len(frame)),
             'missing_response_cells':int(frame['response_ms'].isna().sum()),
             'cpu_over_85_count':int(frame['cpu_pct'].gt(85).sum())}
    (output/'server_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    return summary

def main():print(json.dumps(make_report(load_data(),ROOT/'output'/'mini_03_server'),indent=2))
if __name__=='__main__':main()
