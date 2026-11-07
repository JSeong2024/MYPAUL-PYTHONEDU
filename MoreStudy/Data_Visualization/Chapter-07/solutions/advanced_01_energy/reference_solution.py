"""Reference solution: Advanced 01 — Regional Electricity Demand Explorer.
The input contains deliberately invalid rows. The validator keeps an audit trail
and never silently treats missing timestamps as demand=0.
"""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from project_core.io import ROOT, DATA, export_html, export_json

VALID_REGIONS=('East','North','South','West')
LOCAL_TZ='Asia/Seoul'
START=pd.Timestamp('2026-09-01 00:00',tz=LOCAL_TZ)
END=pd.Timestamp('2026-10-05 23:00',tz=LOCAL_TZ)


def validate_energy(path:Path=DATA/'regional_energy_hourly.csv') -> tuple[pd.DataFrame,pd.DataFrame]:
    raw=pd.read_csv(path,dtype=str,keep_default_na=False)
    required={'timestamp_utc','region','demand_kw'}
    if not required.issubset(raw):raise ValueError('필수 열 누락')
    work=raw.copy()
    work['time']=pd.to_datetime(work.timestamp_utc,utc=True,errors='coerce')
    work['kw']=pd.to_numeric(work.demand_kw,errors='coerce')
    invalid_time=work.time.isna()
    invalid_region=~work.region.isin(VALID_REGIONS)
    invalid_value=work.kw.isna() | (work.kw<0) | ~pd.Series(__import__('numpy').isfinite(work.kw.to_numpy()),index=work.index)
    time_local=work.time.dt.tz_convert(LOCAL_TZ)
    invalid_range=work.time.notna() & ~time_local.between(START,END)
    # Duplicates marked on BOTH rows: refuse ambiguous evidence, not silently keep first.
    duplicated=work.duplicated(subset=['timestamp_utc','region'],keep=False)
    reasons=[]
    for i in work.index:
        flags=[]
        for name,mask in [('invalid_time',invalid_time),('unknown_region',invalid_region),
                          ('invalid_kw',invalid_value),('out_of_range',invalid_range),('duplicate_slot',duplicated)]:
            if bool(mask.loc[i]):flags.append(name)
        reasons.append('|'.join(flags))
    work['reason']=reasons
    bad=work[work.reason.ne('')].copy()
    valid=work[work.reason.eq('')][['region','time','kw']].copy()
    valid['timestamp_local']=valid.time.dt.tz_convert(LOCAL_TZ)
    return valid.sort_values(['region','timestamp_local']),bad


def make_expected_grid(valid:pd.DataFrame,regions:tuple[str,...]=VALID_REGIONS)->pd.DataFrame:
    if not regions or len(set(regions))!=len(regions) or any(r not in VALID_REGIONS for r in regions):
        raise ValueError('유효한 지역을 중복 없이 하나 이상 선택')
    grid=pd.MultiIndex.from_product([regions,pd.date_range(START,END,freq='h')],names=['region','timestamp_local']).to_frame(index=False)
    grid=grid.merge(valid[['region','timestamp_local','kw']],on=['region','timestamp_local'],how='left',validate='one_to_one',indicator=True)
    grid['observed']=grid['_merge'].eq('both')
    return grid.drop(columns='_merge').sort_values(['region','timestamp_local']).reset_index(drop=True)


def make_figure(grid:pd.DataFrame,regions:tuple[str,...]=VALID_REGIONS)->go.Figure:
    if not regions:raise ValueError('지역을 선택하세요')
    fig=make_subplots(rows=2,cols=1,shared_xaxes=False,vertical_spacing=.17,
                      subplot_titles=('Hourly Demand — Missing Hours Are Gaps','24-Hour Average Profile'))
    trace_indices=[]
    for region in regions:
        g=grid[grid.region==region].sort_values('timestamp_local')
        if g.empty:raise ValueError('해당 지역 데이터 없음')
        idx=[]
        idx.append(len(fig.data));fig.add_trace(go.Scatter(x=g.timestamp_local,y=g.kw,mode='lines',name=region,
                               legendgroup=region,connectgaps=False),row=1,col=1)
        profile=g.assign(hour=g.timestamp_local.dt.hour).groupby('hour',as_index=False).agg(mean_kw=('kw','mean'))
        idx.append(len(fig.data));fig.add_trace(go.Scatter(x=profile.hour,y=profile.mean_kw,mode='lines+markers',name=region,
                              legendgroup=region,showlegend=False),row=2,col=1)
        trace_indices.append((region,idx))
    buttons=[dict(label='All Regions',method='update',args=[{'visible':[True]*len(fig.data)},{'title':'Hourly Electricity Demand — All Regions'}])]
    for region,ids in trace_indices:
        buttons.append(dict(label=region,method='update',args=[{'visible':[i in ids for i in range(len(fig.data))]},
                           {'title':f'Hourly Electricity Demand — {region}'}]))
    fig.update_layout(updatemenus=[dict(buttons=buttons,x=1.0,y=1.23,xanchor='right',yanchor='top')],
                      title='Hourly Electricity Demand — All Regions',template='plotly_white',height=750,
                      margin=dict(t=140,b=60),hovermode='x unified')
    # Only time-series top panel gets a date-range slider; bottom panel uses hour of day.
    fig.update_xaxes(rangeslider_visible=True,row=1,col=1)
    fig.update_xaxes(title_text='Hour of Day (KST)',row=2,col=1)
    fig.update_yaxes(title_text='Demand (kW)',row=1,col=1)
    fig.update_yaxes(title_text='Average kW',row=2,col=1)
    return fig


def summarize_grid(grid:pd.DataFrame)->dict:
    totals=grid.groupby('region',as_index=False).agg(expected=('observed','size'),observed=('observed','sum'),peak_kw=('kw','max'))
    totals['coverage_pct']=(100*totals.observed/totals.expected).round(2)
    return {'regions':totals.to_dict(orient='records'),
            'expected_slots':int(totals.expected.sum()),'observed_slots':int(totals.observed.sum())}


def run(output:Path=ROOT/'output/advanced_01_energy',regions:tuple[str,...]=VALID_REGIONS)->dict:
    valid,bad=validate_energy()
    grid=make_expected_grid(valid,regions)
    fig=make_figure(grid,regions)
    export_html(fig,output/'energy_explorer.html')
    bad[['timestamp_utc','region','demand_kw','reason']].to_csv(output/'invalid_rows.csv',index=False)
    grid.to_csv(output/'hourly_coverage.csv',index=False)
    summary=summarize_grid(grid)
    summary['rejected_rows']=len(bad)
    export_json(summary,output/'summary.json')
    return summary


if __name__=='__main__':print(run())
