"""Pure analytics functions for the final visualization projects.

All bundled datasets are synthetic and for education only.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np

DATA = Path(__file__).resolve().parents[1] / 'data'


def read_csv(name: str, data_dir: Path = DATA) -> pd.DataFrame:
    return pd.read_csv(Path(data_dir) / name)


def verify_unique_reference(frame: pd.DataFrame, key: str) -> None:
    if frame[key].isna().any() or frame[key].duplicated().any():
        raise ValueError(f'Reference key {key} must be non-null and unique')


def classify_slots(raw: pd.DataFrame, *, entity_col: str, timestamp_col: str,
                   measures: dict[str, tuple[float, float]], valid_entities: set[str],
                   expected_times: set[int] | None = None, utc: bool = False) -> tuple[pd.DataFrame,pd.DataFrame]:
    """Accept exact, valid unique slots; reject *all* ambiguous duplicates.

    Returns accepted and excluded records with machine-readable reason strings.
    """
    required = {entity_col,timestamp_col,*measures}
    if not required.issubset(raw.columns):
        raise ValueError(f'Missing required columns: {sorted(required-set(raw.columns))}')
    f = raw.copy()
    f['_parsed'] = pd.to_datetime(f[timestamp_col],errors='coerce',utc=utc,format='mixed')
    f['_entity'] = f[entity_col].astype('string')
    f['_reason'] = ''
    invalid_entity = ~f['_entity'].isin(valid_entities)
    invalid_ts = f['_parsed'].isna()
    f.loc[invalid_entity,'_reason'] += 'unknown_entity|'
    f.loc[invalid_ts,'_reason'] += 'invalid_timestamp|'
    for key,(lo,hi) in measures.items():
        numeric = pd.to_numeric(f[key],errors='coerce')
        bad = numeric.isna() | (~np.isfinite(numeric)) | (numeric<lo) | (numeric>hi)
        f.loc[bad,'_reason'] += f'invalid_{key}|'
        f[key]=numeric
    if expected_times is not None:
        f.loc[f['_parsed'].notna() & ~f['_parsed'].dt.hour.isin(expected_times),'_reason'] += 'unexpected_hour|'
    # Ignore invalid timestamps when comparing duplicates, but never silently keep one candidate.
    duplicated = f['_parsed'].notna() & f.duplicated([entity_col,'_parsed'],keep=False)
    f.loc[duplicated,'_reason'] += 'duplicate_slot|'
    f['_reason']=f['_reason'].str.rstrip('|')
    return f[f['_reason'].eq('')].copy(), f[f['_reason'].ne('')].copy()


def expected_coverage(accepted: pd.DataFrame, *, entities: list[str],
                      first_day: str, last_day: str, hours: list[int],
                      entity_col: str, parsed_col: str='_parsed') -> pd.DataFrame:
    """One record per expected slot, retaining missing as missing—not zero."""
    days=pd.date_range(first_day,last_day,freq='D')
    if not len(days) or not entities or not hours:
        raise ValueError('Coverage requires days, entities and hours')
    keys=pd.MultiIndex.from_product([entities,days,hours],names=[entity_col,'date','hour'])
    expected=keys.to_frame(index=False)
    a=accepted.copy()
    a['date']=a[parsed_col].dt.tz_localize(None).dt.normalize()
    a['hour']=a[parsed_col].dt.hour
    count=a.groupby([entity_col,'date','hour']).size().rename('observed').reset_index()
    if (count['observed']>1).any():raise ValueError('Accepted frame contains duplicate slots')
    result=expected.merge(count,on=[entity_col,'date','hour'],how='left',validate='one_to_one')
    result['observed']=result['observed'].fillna(0).astype(int)
    result['available']=result['observed'].eq(1)
    return result


def weather_summary(data_dir: Path=DATA):
    s=read_csv('stations.csv',data_dir);verify_unique_reference(s,'station_id')
    w=read_csv('weather_observations.csv',data_dir)
    good,bad=classify_slots(w,entity_col='station_id',timestamp_col='observed_at',
                measures={'temperature_c':(-40,55),'precipitation_mm':(0,600)},
                valid_entities=set(s.station_id),expected_times={9,18})
    good=good.merge(s,on='station_id',validate='many_to_one')
    good['date']=good['_parsed'].dt.normalize()
    daily=good.groupby(['station_id','region','date'],as_index=False).agg(
        temperature_c=('temperature_c','mean'), precipitation_mm=('precipitation_mm','sum'),readings=('observation_id','size'))
    slots=expected_coverage(good,entities=s.station_id.tolist(),first_day='2026-09-01',last_day='2026-09-30',hours=[9,18],entity_col='station_id')
    return good,bad,daily,slots


def retail_summary(data_dir: Path=DATA):
    f=read_csv('retail_orders.csv',data_dir)
    if f.transaction_id.duplicated().any():raise ValueError('duplicate transactions')
    f=f[f.status.eq('completed')].copy()
    f['revenue_krw']=f.quantity*f.unit_price_krw
    daily=f.groupby(['date','store_id'],as_index=False).agg(revenue_krw=('revenue_krw','sum'),orders=('transaction_id','size'))
    return f,daily


def latency_summary(data_dir: Path=DATA):
    f=read_csv('service_latency.csv',data_dir)
    if f.trace_id.duplicated().any():raise ValueError('duplicate traces')
    f=f[f.latency_ms.ge(0) & f.is_error.isin([0,1])].copy()
    agg=f.groupby('service').agg(requests=('trace_id','size'),median_ms=('latency_ms','median'),p95_ms=('latency_ms',lambda x:x.quantile(.95)),error_rate=('is_error','mean'))
    return f,agg.reset_index()


def electricity_summary(data_dir: Path=DATA):
    raw=read_csv('electricity_demand.csv',data_dir)
    good,bad=classify_slots(raw,entity_col='region',timestamp_col='timestamp_utc',
        measures={'demand_mw':(0,1e6)},valid_entities={'North','South','East','West'},utc=True)
    good['timestamp_kst']=good['_parsed'].dt.tz_convert('Asia/Seoul')
    good['date_kst']=good['timestamp_kst'].dt.date.astype(str)
    daily=good.groupby(['region','date_kst'],as_index=False).agg(mean_demand_mw=('demand_mw','mean'),peak_demand_mw=('demand_mw','max'),samples=('reading_id','size'))
    return good,bad,daily


def metro_summary(data_dir: Path=DATA):
    stations=read_csv('metro_stations.csv',data_dir);verify_unique_reference(stations,'station_id')
    raw=read_csv('metro_boardings.csv',data_dir)
    good,bad=classify_slots(raw,entity_col='station_id',timestamp_col='timestamp_kst',
        measures={'boardings':(0,1e7)},valid_entities=set(stations.station_id),expected_times=set(range(5,23)))
    good=good.merge(stations,on='station_id',validate='many_to_one')
    slots=expected_coverage(good,entities=stations.station_id.tolist(),first_day='2026-09-01',last_day='2026-09-30',hours=list(range(5,23)),entity_col='station_id')
    daily=good.assign(date=good['_parsed'].dt.normalize()).groupby(['station_id','station_name','date'],as_index=False).agg(boardings=('boardings','sum'),hours_observed=('record_id','size'))
    daily['complete']=daily.hours_observed.eq(18)
    return good,bad,daily,slots


def flight_summary(data_dir: Path=DATA):
    f=read_csv('flights.csv',data_dir)
    if f.flight_id.duplicated().any():raise ValueError('Duplicate flight_id')
    if f.delay_min.isna().any() or (f.delay_min < -120).any():raise ValueError('Invalid flight delays')
    f['late_flag']=(f.delay_min>15).astype(int)
    daily=f.groupby(['airport','date'],as_index=False).agg(flights=('flight_id','size'),late_rate=('late_flag','mean'),p90_delay=('delay_min',lambda x:x.quantile(.9)))
    return f,daily


def transit_summary(data_dir: Path=DATA):
    stops=read_csv('transit_stops.csv',data_dir);verify_unique_reference(stops,'stop_id')
    raw=read_csv('transit_operations.csv',data_dir)
    good,bad=classify_slots(raw,entity_col='stop_id',timestamp_col='timestamp_kst',
        measures={'boardings':(0,1e7),'delay_min':(0,360)},valid_entities=set(stops.stop_id),expected_times=set(range(6,23)))
    good=good.merge(stops,on='stop_id',validate='many_to_one')
    slots=expected_coverage(good,entities=stops.stop_id.tolist(),first_day='2026-09-01',last_day='2026-09-30',hours=list(range(6,23)),entity_col='stop_id')
    incidents=read_csv('transit_incidents.csv',data_dir)
    if incidents.incident_id.duplicated().any():raise ValueError('duplicate incidents')
    if not incidents.stop_id.isin(stops.stop_id).all():raise ValueError('unknown incident stop')
    daily=good.assign(date=good['_parsed'].dt.normalize()).groupby(['stop_id','line','zone','date'],as_index=False).agg(
        boardings=('boardings','sum'),mean_delay_min=('delay_min','mean'),samples=('event_id','size'))
    daily['complete']=daily.samples.eq(17)
    return good,bad,daily,slots,incidents
