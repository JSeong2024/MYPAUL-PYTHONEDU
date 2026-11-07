"""Advanced 02 — subway station ridership report on synthetic passenger counts.

Uses real station labels but all numerical counts are deliberately fictional.
Ridership counts cannot establish train occupancy or platform crowding.
"""
from pathlib import Path
import argparse
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
DATA=ROOT/'data'/'subway_ridership.csv'
CATALOG=ROOT/'data'/'subway_stations.csv'
HOURS=list(range(5,24))

def load_data(path:Path=DATA,catalog_path:Path=CATALOG)->tuple[pd.DataFrame,pd.DataFrame]:
    raw=pd.read_csv(path,dtype=str,keep_default_na=False)
    stations=pd.read_csv(catalog_path,dtype={'station_id':str,'line':str})
    if not {'date','station_id','hour','boardings','alightings'}.issubset(raw.columns):
        raise ValueError('Missing ridership columns')
    if not {'station_id','station_name','line'}.issubset(stations.columns):
        raise ValueError('Missing station catalog columns')
    if stations['station_id'].duplicated().any():raise ValueError('Duplicate station IDs in catalog')
    if not set(raw['station_id']).issubset(set(stations['station_id'])):raise ValueError('Unknown stations')
    return raw,stations

def validate_rows(raw:pd.DataFrame)->tuple[pd.DataFrame,pd.DataFrame]:
    f=raw.copy()
    f['date']=pd.to_datetime(f['date'],errors='coerce',format='%Y-%m-%d')
    f['hour']=pd.to_numeric(f['hour'],errors='coerce')
    for col in ['boardings','alightings']:
        f[col]=pd.to_numeric(f[col],errors='coerce')
    f['reason']=''
    def flag(mask,label):
        f.loc[mask,'reason']=f.loc[mask,'reason'].apply(lambda old:old+'|'+label if old else label)
    flag(f['date'].isna(),'invalid_date')
    flag(f['hour'].isna() | ~f['hour'].isin(HOURS),'invalid_hour')
    # original slot key ensures duplicate input rows do not double the number of passengers.
    flag(raw.duplicated(['date','station_id','hour'],keep='first'),'duplicate_slot')
    flag(f[['boardings','alightings']].isna().any(axis=1),'invalid_count')
    flag((f[['boardings','alightings']]<0).any(axis=1),'negative_count')
    flag((f[['boardings','alightings']]%1!=0).any(axis=1).fillna(False),'non_integer_count')
    valid=f.loc[f['reason'].eq('')].copy()
    rejected=f.loc[f['reason'].ne('')].copy()
    valid[['hour','boardings','alightings']]=valid[['hour','boardings','alightings']].astype('int64')
    return valid,rejected

def build_summaries(valid:pd.DataFrame,stations:pd.DataFrame,
                    start:pd.Timestamp,end:pd.Timestamp):
    if start>end:raise ValueError('start must not exceed end')
    days=pd.date_range(start,end,freq='D')
    grid=pd.MultiIndex.from_product([stations['station_id'],days,HOURS],names=['station_id','date','hour'])
    indexed=valid.set_index(['station_id','date','hour'])
    if indexed.index.has_duplicates:raise ValueError('Duplicate validated slots')
    complete=indexed.reindex(grid).reset_index()
    complete['total']=complete['boardings']+complete['alightings']
    complete['weekend']=complete['date'].dt.dayofweek>=5
    station=complete.groupby('station_id',as_index=False).agg(
        valid_slots=('total','count'),boardings=('boardings','sum'),alightings=('alightings','sum'))
    station['expected_slots']=len(days)*len(HOURS)
    station['coverage_pct']=100*station['valid_slots']/station['expected_slots']
    station=station.merge(stations,on='station_id',validate='one_to_one')
    station['total']=station['boardings']+station['alightings']
    station=station.sort_values('total',ascending=False).reset_index(drop=True)
    return complete,station

def _write(fig:plt.Figure,path:Path):
    fig.savefig(path,dpi=140)
    plt.close(fig)

def make_report(raw:pd.DataFrame,stations:pd.DataFrame,output:Path,
                selected_ids:list[str]|None=None)->dict:
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    valid,rejected=validate_rows(raw)
    dates=valid['date']
    start,end=dates.min(),dates.max()
    if pd.isna(start) or pd.isna(end):raise ValueError('No valid rows')
    complete,summary=build_summaries(valid,stations,start,end)
    # Overview is based on *observed* ridership, with coverage disclosed nearby.
    fig,axes=plt.subplots(2,2,figsize=(13,8.5),layout='constrained')
    ranking=summary.head(8).iloc[::-1]
    axes[0,0].barh(ranking['station_name'],ranking['total'])
    axes[0,0].set(title='Recorded Passenger Movements by Station',xlabel='Boardings + Alightings')
    dtotal=complete.groupby('date')['total'].sum(min_count=1)
    axes[0,1].plot(dtotal.index,dtotal.values,marker='.',markersize=5)
    axes[0,1].set(title='Daily Recorded Passenger Movements',ylabel='Passengers/day')
    axes[0,1].tick_params(axis='x',labelrotation=30)
    axes[1,0].bar(summary['station_name'],summary['coverage_pct'])
    axes[1,0].set(title='Valid Observation Coverage',ylabel='%',ylim=(0,105))
    axes[1,0].tick_params(axis='x',labelrotation=30)
    hourly=complete.groupby('hour')['total'].mean()
    axes[1,1].plot(hourly.index,hourly.values,marker='o',label='Mean observed slot')
    axes[1,1].set(title='Hourly Mean Recorded Movement',xlabel='Hour',ylabel='Passengers/observed slot')
    axes[1,1].xaxis.set_major_locator(mticker.MultipleLocator(2))
    fig.suptitle('Subway Ridership Overview — Synthetic Counts',fontsize=15)
    _write(fig,output/'01_overview.png')
    # Weekday/weekend hour comparison per observed station-hour slot (not totals).
    grouped=complete.groupby(['weekend','hour'])['total'].mean().unstack(0)
    fig,ax=plt.subplots(figsize=(9,4.8),layout='constrained')
    for weekend,label in [(False,'Weekday'),(True,'Weekend')]:
        ax.plot(grouped.index,grouped[weekend],marker='o',label=label)
    ax.set(title='Hourly Profile: Weekday vs Weekend',xlabel='Hour',ylabel='Mean passengers per observed station-hour')
    ax.legend();ax.grid(alpha=.2)
    _write(fig,output/'02_hourly_profile.png')
    # Station x hour: normalized per observed slot; cells without observations remain NaN.
    heat=complete.groupby(['station_id','hour'])['total'].mean().unstack('hour')
    heat=heat.reindex(stations['station_id']).reindex(columns=HOURS)
    fig,ax=plt.subplots(figsize=(13,5),layout='constrained')
    vals=np.ma.masked_invalid(heat.to_numpy(dtype=float))
    im=ax.imshow(vals,aspect='auto',cmap='viridis',interpolation='nearest')
    ax.set(title='Mean Hourly Passenger Movements by Station',xlabel='Hour',ylabel='Station')
    ax.set_xticks(range(len(HOURS)),HOURS)
    labels=stations.set_index('station_id').loc[heat.index,'station_name']
    ax.set_yticks(range(len(heat)),labels)
    fig.colorbar(im,ax=ax,label='Mean passengers / valid slot')
    _write(fig,output/'03_station_hour_heatmap.png')
    # Dynamic panels: support any nonempty subset and keep consistent scale.
    available=set(stations['station_id'])
    selected=list(stations['station_id']) if selected_ids is None else list(dict.fromkeys(selected_ids))
    if not selected or not set(selected).issubset(available):raise ValueError('Invalid station selection')
    profiles=complete.groupby(['station_id','hour'])['total'].mean().unstack('hour').reindex(selected)
    mx=float(profiles.max().max())
    n=len(selected);cols=min(3,n);rows=math.ceil(n/cols)
    fig,axes=plt.subplots(rows,cols,squeeze=False,sharey=True,figsize=(5*cols,3.5*rows),layout='constrained')
    names=stations.set_index('station_id')['station_name']
    for i,sid in enumerate(selected):
        ax=axes.flat[i];ax.plot(HOURS,profiles.loc[sid],marker='.',linewidth=1.5)
        ax.set(title=names[sid],xlabel='Hour',ylabel='Mean passengers',ylim=(0,mx*1.15))
        ax.grid(alpha=.2);ax.xaxis.set_major_locator(mticker.MultipleLocator(4))
    for ax in list(axes.flat)[n:]:ax.set_visible(False)
    fig.suptitle('Station Profiles — Synthetic Counts',fontsize=15)
    _write(fig,output/'04_dynamic_station_panels.png')
    # Identify valid slots separate from absent/invalid slots; no zero imputation.
    coverage=(complete.assign(valid=complete['total'].notna().astype(int))
              .groupby(['station_id','date'])['valid'].sum().unstack('date').reindex(stations['station_id']))
    fig,ax=plt.subplots(figsize=(12,4.5),layout='constrained')
    im=ax.imshow(coverage.to_numpy(),aspect='auto',cmap='Blues',vmin=0,vmax=len(HOURS),interpolation='nearest')
    ax.set(title='Valid Hourly Slots by Station and Date',xlabel='Date',ylabel='Station')
    ax.set_yticks(range(len(stations)),stations['station_name'])
    dateidx=list(coverage.columns)
    ticks=list(range(0,len(dateidx),4))
    ax.set_xticks(ticks,[dateidx[i].strftime('%m-%d') for i in ticks])
    fig.colorbar(im,ax=ax,label=f'Valid slots/day (max {len(HOURS)})')
    _write(fig,output/'05_coverage_map.png')
    summary.to_csv(output/'station_summary.csv',index=False)
    rejected.to_csv(output/'rejected_rows.csv',index=False)
    totals={'source_rows':len(raw),'accepted_rows':len(valid),'rejected_rows':len(rejected),
            'expected_slots':len(complete),'missing_or_invalid_slots':int(complete['total'].isna().sum()),
            'recorded_boardings':int(summary['boardings'].sum()),'recorded_alightings':int(summary['alightings'].sum()),
            'selected_stations_for_panels':selected,
            'warning':'All passenger counts are synthetic; station counts do not represent train occupancy.'}
    (output/'summary.json').write_text(json.dumps(totals,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return totals

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stations',nargs='*',help='Station IDs to include in dynamic panels')
    p.add_argument('--output',type=Path,default=ROOT/'output'/'advanced_02_subway')
    a=p.parse_args()
    raw,stations=load_data()
    print(json.dumps(make_report(raw,stations,a.output,a.stations),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
