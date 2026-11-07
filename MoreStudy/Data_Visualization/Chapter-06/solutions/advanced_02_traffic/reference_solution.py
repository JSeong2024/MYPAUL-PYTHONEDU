from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
LOCAL_TZ = 'Asia/Seoul'
START = pd.Timestamp('2026-10-01 00:00',tz=LOCAL_TZ)
END = pd.Timestamp('2026-10-28 23:00',tz=LOCAL_TZ)


def validate_traffic(raw, corridors):
    required = {'timestamp_utc','corridor_id','vehicle_count'}
    if not required.issubset(raw.columns): raise ValueError('Missing required columns')
    df=raw.copy()
    df['utc_time']=pd.to_datetime(df['timestamp_utc'],utc=True,errors='coerce')
    df['local_time']=df['utc_time'].dt.tz_convert(LOCAL_TZ)
    df['count']=pd.to_numeric(df['vehicle_count'],errors='coerce')
    bad_time=df['local_time'].isna()|df['local_time'].lt(START)|df['local_time'].gt(END)|(df['local_time'].dt.minute!=0)
    bad_corridor=~df['corridor_id'].isin(corridors)
    bad_count=df['count'].isna()|~np.isfinite(df['count'])|df['count'].lt(0)|(df['count']%1!=0)
    dup=df.duplicated(['corridor_id','utc_time'],keep=False)&~bad_time
    bad=bad_time|bad_corridor|bad_count|dup
    audit=df.assign(invalid_time=bad_time,unknown_corridor=bad_corridor,invalid_count=bad_count,duplicate=dup,accepted=~bad)
    return df.loc[~bad].copy(),audit


def make_time_grid(accepted, selected):
    times=pd.date_range(START,END,freq='h')
    frame=(accepted.loc[accepted['corridor_id'].isin(selected)]
        .pivot(index='local_time',columns='corridor_id',values='count')
        .reindex(index=times,columns=selected))
    return frame


def build_report(corridors=None,output_dir=None):
    out=Path(output_dir) if output_dir is not None else ROOT/'output/advanced_02_traffic'
    out.mkdir(parents=True,exist_ok=True)
    catalog=json.loads((ROOT/'data/traffic_corridors.json').read_text(encoding='utf-8'))
    names={r['corridor_id']:r['name'] for r in catalog}
    selected=list(names) if corridors is None else list(corridors)
    if not selected or len(set(selected))!=len(selected) or any(c not in names for c in selected):
        raise ValueError('Select unique, registered corridors')
    raw=pd.read_csv(ROOT/'data/traffic_hourly.csv',dtype=str,keep_default_na=False)
    valid,audit=validate_traffic(raw,set(names))
    grid=make_time_grid(valid,selected)
    # Sum only complete days; partial days stay NA to avoid undercounting.
    by_day=grid.resample('D').agg(['sum','count'])
    days=grid.resample('D').sum(min_count=24)
    completeness=grid.notna().resample('D').sum().astype(int)
    daily=days.copy();daily.index.name='date_local';daily.to_csv(out/'complete_daily_totals.csv')
    completeness.index.name='date_local';completeness.to_csv(out/'daily_sample_counts.csv')
    audit.to_csv(out/'audit.csv',index=False)
    summary=[]
    for corridor in selected:
        s=grid[corridor]
        summary.append({'corridor_id':corridor,'name':names[corridor], 'observed_hours':int(s.notna().sum()),'expected_hours':len(s), 'coverage_pct':round(float(100*s.notna().mean()),2), 'complete_days':int((completeness[corridor]==24).sum())})
    pd.DataFrame(summary).to_csv(out/'corridor_summary.csv',index=False)
    n=len(selected)
    fig,axes=plt.subplots(2,2,figsize=(13,9),layout='constrained')
    ax=axes[0,0]
    for c in selected: ax.plot(days.index,days[c],marker='.',ms=3,lw=1,label=c)
    ax.set(title='Complete-day vehicle totals',ylabel='Vehicles / day');ax.legend(ncol=3,fontsize=8)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7, tz=ZoneInfo('Asia/Seoul')))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d', tz=ZoneInfo('Asia/Seoul')))
    ax=axes[0,1]
    covers=[r['coverage_pct'] for r in summary]
    ax.barh(selected,covers)
    ax.set(xlim=(0,100),xlabel='Coverage (%)',title='Observed time slots')
    ax=axes[1,0]
    profiles=[]
    for c in selected:
        for kind in ['Weekday','Weekend']:
            mask=(grid.index.dayofweek>=5) if kind=='Weekend' else (grid.index.dayofweek<5)
            profile=grid.loc[mask,c].groupby(grid.index[mask].hour).mean().reindex(range(24))
            profiles.append(profile.to_numpy())
            if c==selected[0]:ax.plot(profile.index,profile.values,label=kind)
    ax.set(title=f'Time-of-day pattern — {selected[0]}',xlabel='Hour (KST)',ylabel='Mean vehicles / observed hour');ax.legend()
    ax=axes[1,1]
    matrix=np.array([grid[c].groupby(grid.index.hour).mean().reindex(range(24)).to_numpy() for c in selected])
    image=ax.imshow(matrix,aspect='auto',cmap='viridis',origin='upper')
    ax.set(title='Typical hourly volume (mean of observed hours)',xlabel='Hour (KST)',yticks=range(n),yticklabels=selected,xticks=range(0,24,3))
    fig.colorbar(image,ax=ax,label='Vehicles / hour')
    for ax in (axes[0,0],axes[1,0]):ax.grid(alpha=.2)
    fig.savefig(out/'traffic_overview.png',dpi=145)
    plt.close(fig)
    # Individual detail report, dynamic number of corridors.
    fig, axs=plt.subplots(n,1,figsize=(12,max(3.3,n*2.7)),sharex=True,squeeze=False,layout='constrained')
    for ax,c in zip(axs.flat,selected):
        ax.plot(grid.index,grid[c],lw=.7,alpha=.42,label='hourly traffic')
        ax.plot(grid.index,grid[c].rolling(24,min_periods=24).mean(),lw=1.5,label='24-sample mean')
        ax.set(ylabel='Vehicles',title=f'{names[c]} ({c})');ax.grid(alpha=.2)
    axs.flat[0].legend(ncol=2,fontsize=8)
    axs.flat[-1].set_xlabel('Local time — Asia/Seoul')
    fig.savefig(out/'traffic_details.png',dpi=140)
    plt.close(fig)
    return {'raw':len(raw),'accepted':len(valid),'invalid':int((~audit['accepted']).sum()),'selected':n,'missing_slots':int(grid.isna().sum().sum()),'complete_days':int((completeness==24).sum().sum())}

if __name__=='__main__':
    print(build_report())
