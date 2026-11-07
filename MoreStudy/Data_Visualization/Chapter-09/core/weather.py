"""Chapter 09 capstone: figures and independent dashboard input model."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from .analytics import DATA, require_columns

WEATHER = DATA / 'weather'

def load_weather(path:Path|None=None):
    folder=Path(path) if path is not None else WEATHER
    daily=pd.read_csv(folder/'daily_station_summary.csv')
    coverage=pd.read_csv(folder/'coverage.csv')
    with (folder/'quality_report.json').open(encoding='utf-8') as f:quality=json.load(f)
    require_columns(daily,['station_id','region','date','readings','avg_temperature_c','total_precipitation_mm','complete_day'])
    require_columns(coverage,['station_id','date','observed_readings','expected_readings','status'])
    if daily.duplicated(['station_id','date']).any() or coverage.duplicated(['station_id','date']).any():raise ValueError('Duplicated station-day keys')
    return daily,coverage,quality

def filter_weather(daily,coverage,stations=None,start=None,end=None):
    d=daily.copy();c=coverage.copy()
    if stations is not None:
        d=d[d.station_id.isin(stations)];c=c[c.station_id.isin(stations)]
    for field,value,operator in [('date',start,'ge'),('date',end,'le')]:
        if value is not None:
            d=d.loc[getattr(d[field],operator)(str(value))].copy();c=c.loc[getattr(c[field],operator)(str(value))].copy()
    return d,c

def weather_kpis(daily:pd.DataFrame,coverage:pd.DataFrame)->dict:
    expected=int(coverage['expected_readings'].sum());observed=int(coverage['observed_readings'].sum());readings=int(daily['readings'].sum())
    if observed!=readings:raise ValueError('Daily and coverage counts disagree')
    # Weighted by accepted readings, not naive average of station/day means.
    avg=float(np.average(daily['avg_temperature_c'],weights=daily['readings'])) if readings else None
    return {'accepted_readings':readings,'expected_readings':expected,'coverage_pct':round(100*observed/expected,2) if expected else None,'weighted_avg_temperature_c':round(avg,2) if avg is not None else None,'incomplete_station_days':int(coverage['status'].ne('complete').sum())}

def weather_static_report(daily:pd.DataFrame,coverage:pd.DataFrame,path:Path)->dict:
    kpis=weather_kpis(daily,coverage)
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    colors=plt.get_cmap('tab10')
    for i,(station,grp) in enumerate(daily.groupby('station_id',sort=True)):
        grp=grp.sort_values('date')
        axes[0,0].plot(pd.to_datetime(grp['date']),grp['avg_temperature_c'],marker='o',label=station,color=colors(i))
    axes[0,0].set(title='Daily temperature by station',ylabel='Temperature (°C)')
    axes[0,0].legend(fontsize=8)
    byregion=daily.groupby('region',as_index=False)['total_precipitation_mm'].sum()
    axes[0,1].bar(byregion['region'],byregion['total_precipitation_mm'])
    axes[0,1].set(title='Recorded precipitation',ylabel='Precipitation (mm)')
    cv=coverage.assign(date=pd.to_datetime(coverage['date'])).pivot(index='station_id',columns='date',values='observed_readings')
    sns.heatmap(cv,ax=axes[1,0],annot=True,fmt='.0f',cmap='Blues',cbar=False,vmin=0,vmax=2)
    axes[1,0].set(title='Valid readings by station and date',xlabel='Date',ylabel='Station')
    axes[1,0].tick_params(axis='x',labelrotation=70)
    counts=coverage['status'].value_counts().reindex(['complete','partial','missing'],fill_value=0)
    axes[1,1].bar(counts.index,counts.values)
    axes[1,1].set(title='Coverage status of station-days',ylabel='Days')
    fig.suptitle(f"Weather Data Visualization Capstone | coverage {kpis['coverage_pct']}%",fontsize=14)
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);fig.savefig(path,dpi=130,bbox_inches='tight');plt.close(fig)
    return kpis

def weather_html(daily,path:Path):
    fig=px.line(daily.assign(date=pd.to_datetime(daily['date'])),x='date',y='avg_temperature_c',color='station_id',markers=True,title='Daily station temperature',labels={'avg_temperature_c':'Temperature (°C)','date':'Date','station_id':'Station'})
    fig.update_layout(hovermode='x unified')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);fig.write_html(str(path),include_plotlyjs=True,full_html=True)
