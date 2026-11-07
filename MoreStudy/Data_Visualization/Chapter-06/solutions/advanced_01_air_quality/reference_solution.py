from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
START = pd.Timestamp('2026-09-01 00:00')
END = pd.Timestamp('2026-09-21 23:00')


def validate_air_data(raw, station_ids):
    required = {'timestamp_local', 'station_id', 'pm25_ug_m3'}
    if not required.issubset(raw.columns): raise ValueError('Missing required columns')
    raw = raw.copy()
    raw['parsed_time'] = pd.to_datetime(raw['timestamp_local'], format='%Y-%m-%d %H:%M', errors='coerce')
    raw['value'] = pd.to_numeric(raw['pm25_ug_m3'], errors='coerce')
    bad_time = raw['parsed_time'].isna() | raw['parsed_time'].lt(START) | raw['parsed_time'].gt(END) | (raw['parsed_time'].dt.minute != 0)
    bad_id = ~raw['station_id'].isin(station_ids)
    bad_value = raw['value'].isna() | ~np.isfinite(raw['value']) | raw['value'].lt(0) | raw['value'].gt(500)
    duplicate = raw.duplicated(['station_id', 'parsed_time'], keep=False) & ~bad_time
    bad = bad_time | bad_id | bad_value | duplicate
    valid = raw.loc[~bad].copy()
    if valid.duplicated(['station_id','parsed_time']).any(): raise AssertionError('Uniqueness postcondition violated')
    audit = raw.assign(invalid_timestamp=bad_time, unknown_station=bad_id, invalid_measurement=bad_value, duplicate_key=duplicate, accepted=~bad)
    return valid, audit


def build_report(stations=None, output_dir=None):
    out = Path(output_dir) if output_dir is not None else ROOT/'output/advanced_01_air_quality'
    out.mkdir(parents=True, exist_ok=True)
    catalogue = json.loads((ROOT/'data/air_stations.json').read_text(encoding='utf-8'))
    known = {r['station_id']: r['region'] for r in catalogue}
    selected = list(known) if stations is None else list(stations)
    if not selected or len(set(selected))!=len(selected) or any(s not in known for s in selected):
        raise ValueError('Select unique, registered stations')
    raw = pd.read_csv(ROOT/'data/air_quality_hourly.csv',dtype={'station_id':'str','pm25_ug_m3':'str','timestamp_local':'str'},keep_default_na=False)
    valid,audit = validate_air_data(raw,set(known))
    audit.to_csv(out/'audit.csv',index=False)
    expected = pd.date_range(START,END,freq='h')
    fig,axes=plt.subplots(len(selected),1,figsize=(11,max(3.0,2.8*len(selected))),squeeze=False,sharex=True,layout='constrained')
    records=[]
    for ax,station in zip(axes.flat,selected):
        points=valid.loc[valid['station_id'].eq(station)].set_index('parsed_time')['value'].sort_index().reindex(expected)
        rolling=points.rolling(24,min_periods=18).mean()
        ax.plot(expected,points,label='PM2.5 observed',lw=.8,alpha=.45)
        ax.plot(expected,rolling,label='24-sample rolling mean (min 18)',lw=1.8)
        ax.axhline(35,ls=':',color='#ad473d',label='Illustrative marker: 35')
        ax.set(ylabel='µg/m³',title=f'{known[station]} ({station})')
        ax.grid(alpha=.2)
        records.append({'station_id':station,'observed_hours':int(points.notna().sum()),'expected_hours':len(expected),'coverage_pct':round(100*points.notna().mean(),2),'mean_ug_m3':round(float(points.mean()),2)})
    axes.flat[0].legend(fontsize=8,ncol=2)
    axes.flat[-1].set_xlabel('Local time (KST, assumed from source)')
    fig.savefig(out/'air_quality_report.png',dpi=145)
    plt.close(fig)
    pd.DataFrame(records).to_csv(out/'station_summary.csv',index=False)
    return {'accepted':len(valid),'invalid':int((~audit['accepted']).sum()),'selected':len(selected),'coverage':{r['station_id']:r['coverage_pct'] for r in records}}

if __name__=='__main__':
    print(build_report())
