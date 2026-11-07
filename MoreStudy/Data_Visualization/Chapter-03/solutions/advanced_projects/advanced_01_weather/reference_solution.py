"""Advanced 01 — reusable multi-station weather reporting with dynamic layouts."""
from pathlib import Path
import argparse
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
DATA=ROOT/'data'/'weather_stations.csv'

def load_data(path:Path=DATA)->pd.DataFrame:
    frame=pd.read_csv(path,parse_dates=['date'])
    required=['date','site_id','site_name','temperature_c','precipitation_mm']
    if not set(required).issubset(frame.columns):raise ValueError('Missing weather columns')
    if frame[['date','site_id']].duplicated().any():raise ValueError('Duplicate site date')
    if frame['site_id'].isna().any() or frame['site_name'].isna().any():raise ValueError('Missing site identity')
    if frame['precipitation_mm'].isna().any() or frame['precipitation_mm'].lt(0).any():raise ValueError('Invalid precipitation')
    if not frame['temperature_c'].dropna().between(-40,50).all():raise ValueError('Temperature outside accepted range')
    return frame

def make_report(frame:pd.DataFrame,output:Path,site_ids:list[str]|None=None)->dict:
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    available=sorted(frame['site_id'].unique())
    selected=available if site_ids is None else list(dict.fromkeys(site_ids))
    if not selected:raise ValueError('Select at least one site')
    if not set(selected).issubset(available):raise ValueError('Unknown site ID')
    frame=frame.loc[frame['site_id'].isin(selected)].copy()
    dates=pd.date_range(frame['date'].min(),frame['date'].max(),freq='D')
    summary_rows=[]
    for sid in selected:
        part=frame.loc[frame['site_id']==sid].set_index('date').reindex(dates)
        summary_rows.append({'site_id':sid,'observed_rows':int(part['site_id'].notna().sum()),
                             'valid_temperature_rows':int(part['temperature_c'].notna().sum()),
                             'expected_rows':len(dates),
                             'coverage_pct':round(100*part['temperature_c'].notna().sum()/len(dates),2)})
    sums=pd.DataFrame(summary_rows)
    sums.to_csv(output/'weather_site_quality.csv',index=False)
    # Fixed comparison axes so the same temperature has the same vertical position.
    yvalues=frame['temperature_c'].dropna()
    bounds=(float(yvalues.min()-2),float(yvalues.max()+2))
    n=len(selected);cols=min(3,n);rows=math.ceil(n/cols)
    fig,axes=plt.subplots(rows,cols,figsize=(5*cols,3.3*rows),squeeze=False,sharey=True,layout='constrained')
    for i,sid in enumerate(selected):
        ax=axes.flat[i]
        part=frame.loc[frame['site_id']==sid].set_index('date')['temperature_c'].reindex(dates)
        ax.plot(dates,part,marker='o',markersize=2.8,linewidth=1.4)
        ax.axhline(28,color='firebrick',linestyle='--',linewidth=1,label='Review 28°C')
        ax.set(title=sid,ylabel='Temperature (°C)',ylim=bounds)
        ax.tick_params(axis='x',labelrotation=30)
        ax.grid(alpha=.18)
        if i==0:ax.legend(fontsize=8)
    for ax in list(axes.flat)[n:]:ax.set_visible(False)
    fig.suptitle('Daily Temperature by Station — Synthetic Data',fontsize=15)
    fig.savefig(output/'dynamic_station_panels.png',dpi=140)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
    bars=ax.bar(sums['site_id'],sums['coverage_pct'])
    ax.bar_label(bars,fmt='%.1f%%',padding=3)
    ax.set(title='Valid Temperature Coverage',ylabel='%',ylim=(0,110))
    fig.savefig(output/'coverage_by_station.png',dpi=145)
    plt.close(fig)
    summary={'stations':len(selected),'expected_slots':len(dates)*len(selected),
             'valid_temperature_rows':int(sums['valid_temperature_rows'].sum()),
             'missing_or_invalid_slots':len(dates)*len(selected)-int(sums['valid_temperature_rows'].sum()),
             'images':['dynamic_station_panels.png','coverage_by_station.png']}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stations',nargs='*',help='e.g. WX-01 WX-03; omit to include all')
    p.add_argument('--output',type=Path,default=ROOT/'output'/'advanced_01_weather')
    a=p.parse_args()
    print(json.dumps(make_report(load_data(),a.output,a.stations),indent=2))
if __name__=='__main__':main()
