"""Advanced: 시간 단위 승차 기록 검증, 누락 슬롯 탐지 및 보고서 계산."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
import plotly.express as px
from .analytics import as_csv_bytes
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['timestamp_kst','station_id','boardings','avg_delay_min','trips_observed']


def load_reference(data_dir=ROOT/'data'):
    d=Path(data_dir)
    stations=pd.DataFrame(json.loads((d/'stations.json').read_text(encoding='utf-8')))
    policy=json.loads((d/'rail_policy.json').read_text(encoding='utf-8'))
    if stations['station_id'].duplicated().any():raise ValueError('중복 역사 ID')
    if policy.get('timezone')!='Asia/Seoul':raise ValueError('이 예제는 KST 입력을 가정합니다.')
    return stations,policy


def load_raw(path=ROOT/'data'/'metro_hourly_raw.csv'):
    return pd.read_csv(path,dtype=str,keep_default_na=False,encoding='utf-8-sig')


def validate_metro(raw,stations,policy):
    """원본 유지. 중복 슬롯에 속한 모든 행을 제외. accepted, issues, coverage 반환."""
    if not set(REQUIRED).issubset(raw.columns):raise ValueError(f'필수 열 누락: {set(REQUIRED)-set(raw.columns)}')
    work=raw.copy().reset_index(drop=True)
    work['source_row']=work.index+2  # CSV header at line1
    work['station_id']=work['station_id'].astype(str).str.strip()
    work['timestamp_parsed']=pd.to_datetime(work['timestamp_kst'],format='%Y-%m-%d %H:%M',errors='coerce')
    for col in ['boardings','avg_delay_min','trips_observed']:
        work[col+'_number']=pd.to_numeric(work[col],errors='coerce')
    known=set(stations['station_id'])
    begin=pd.Timestamp(policy['start_date']);stop=pd.Timestamp(policy['end_date'])+pd.Timedelta(days=1)
    date_ok=work['timestamp_parsed'].between(begin,stop,inclusive='left')
    clock_ok=work['timestamp_parsed'].dt.minute.eq(0)
    dup=work.duplicated(['station_id','timestamp_parsed'],keep=False)
    reasons=[]
    for i,row in work.iterrows():
        flags=[]
        if row['station_id'] not in known:flags.append('unknown_station')
        if pd.isna(row['timestamp_parsed']) or not bool(date_ok.iloc[i]) or not bool(clock_ok.iloc[i]):flags.append('invalid_time')
        if bool(dup.iloc[i]):flags.append('duplicate_slot')
        for c in ['boardings','avg_delay_min','trips_observed']:
            v=row[c+'_number']
            if not np.isfinite(v) or v < (1 if c=='trips_observed' else 0):flags.append('invalid_'+c)
        if pd.notna(row['boardings_number']) and row['boardings_number']%1:flags.append('boardings_not_integer')
        if pd.notna(row['trips_observed_number']) and row['trips_observed_number']%1:flags.append('trips_not_integer')
        reasons.append('|'.join(flags))
    work['reason_codes']=reasons
    bad=work.loc[work['reason_codes'].ne('')].copy()
    good=work.loc[work['reason_codes'].eq('')].copy()
    good=good.rename(columns={'timestamp_parsed':'timestamp','boardings_number':'boardings_valid','avg_delay_min_number':'delay_valid','trips_observed_number':'trips_valid'})
    good=good[['timestamp','station_id','boardings_valid','delay_valid','trips_valid','source_row']].sort_values(['station_id','timestamp']).reset_index(drop=True)
    good['date']=good['timestamp'].dt.date
    bad=bad[['source_row']+REQUIRED+['reason_codes']]
    dates=pd.date_range(policy['start_date'],policy['end_date'],freq='D')
    hours=pd.date_range(dates[0],dates[-1]+pd.Timedelta(hours=23),freq='h')
    grid=pd.MultiIndex.from_product([stations['station_id'],hours],names=['station_id','timestamp']).to_frame(index=False)
    grid=grid.merge(good[['station_id','timestamp','boardings_valid']],on=['station_id','timestamp'],how='left',validate='one_to_one',indicator=True)
    grid['observed']=grid['_merge'].eq('both')
    grid['date']=grid['timestamp'].dt.date
    coverage=grid[['station_id','timestamp','date','observed','boardings_valid']].copy()
    return good,bad,coverage


def filter_metro(good,coverage,stations,start,end):
    lo=pd.Timestamp(start).date();hi=pd.Timestamp(end).date()
    if lo>hi:raise ValueError('기간 시작일이 종료일보다 늦습니다.')
    names=set(stations)
    accepted=good.loc[good['station_id'].isin(names) & good['date'].between(lo,hi)].copy()
    expected=coverage.loc[coverage['station_id'].isin(names) & coverage['date'].between(lo,hi)].copy()
    return accepted,expected


def metro_summary(good,coverage):
    exp=len(coverage);obs=int(coverage['observed'].sum())
    return {'boardings':int(good['boardings_valid'].sum()),'expected_slots':exp,'accepted_slots':obs,
            'coverage_pct':100*obs/exp if exp else None,
            'missing_slots':exp-obs,
            'mean_hourly_delay_min':float(good['delay_valid'].mean()) if len(good) else None}


def metro_charts(good,coverage,stations):
    if good.empty:return None,None,None
    daily=good.groupby('date',as_index=False)['boardings_valid'].sum()
    daily_line=px.line(daily,x='date',y='boardings_valid',markers=True,title='Daily Boardings (Valid Slots Only)')
    daily_line.update_layout(yaxis_title='Boardings',xaxis_title='Date')
    by_station=good.groupby('station_id',as_index=False)['boardings_valid'].sum().sort_values('boardings_valid',ascending=False)
    rank=px.bar(by_station,x='station_id',y='boardings_valid',title='Boardings by Station')
    rank.update_layout(xaxis_title='Station',yaxis_title='Boardings')
    hour=good.copy();hour['hour']=hour['timestamp'].dt.hour
    pivot=hour.pivot_table(index='station_id',columns='hour',values='boardings_valid',aggfunc='mean')
    matrix=px.imshow(pivot,aspect='auto',title='Average Boardings by Hour and Station',labels={'x':'KST Hour','y':'Station','color':'Boardings'})
    return daily_line,rank,matrix


def missing_dates(coverage):
    daily=coverage.groupby(['station_id','date'],as_index=False).agg(observed=('observed','sum'),expected=('observed','size'))
    daily['status']=np.select([daily['observed'].eq(0),daily['observed'].eq(daily['expected'])],['missing','complete'],default='partial')
    return daily
