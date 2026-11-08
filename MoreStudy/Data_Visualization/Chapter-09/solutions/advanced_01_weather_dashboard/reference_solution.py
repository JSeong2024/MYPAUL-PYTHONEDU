"""Advanced 01: cross-station daily coverage and normalized temperature comparison."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import pandas as pd
import numpy as np
from core.utils import arguments,load,numeric,save,figure_start,finish,iso_day

def extras(p):
 p.add_argument('--start',default='2026-10-01');p.add_argument('--end',default='2026-10-21')
 p.add_argument('--stations',default='',help='comma-separated station IDs; empty=all')
def run():
 args=arguments('Weather Monitoring Dashboard','advanced_01_weather_dashboard',extras)
 stations=load(args.data/'stations.csv',['station_id','station_name','zone'])
 if stations.station_id.duplicated().any():raise ValueError('duplicate station ID')
 df=load(args.data/'observations.csv',['observation_id','station_id','local_date','temperature_c','rain_mm'])
 df['temperature_c']=numeric(df.temperature_c);df['rain_mm']=numeric(df.rain_mm)
 duplicate=df.observation_id.duplicated(keep=False)
 bad=duplicate|~df.station_id.isin(stations.station_id)|df.temperature_c.isna()|df.rain_mm.isna()|df.rain_mm.lt(0)|pd.to_datetime(df.local_date,errors='coerce').isna()
 audit=df.loc[bad,['observation_id','station_id','local_date']].copy();audit['reason']='duplicate_or_invalid_record';save(audit,args.output/'audit.csv')
 valid=df.loc[~bad].copy()
 ids=set(args.stations.split(',')) if args.stations else set(stations.station_id)
 if ids-set(stations.station_id):raise ValueError('unknown station filter')
 filtered=iso_day(valid[valid.station_id.isin(ids)],start=args.start,end=args.end)
 dates=pd.date_range(args.start,args.end,freq='D').strftime('%Y-%m-%d')
 grid=pd.MultiIndex.from_product([sorted(ids),dates],names=['station_id','local_date']).to_frame(index=False)
 grid=grid.merge(filtered[['station_id','local_date','temperature_c','rain_mm']],how='left',on=['station_id','local_date'],validate='one_to_one')
 grid['observed']=grid.temperature_c.notna();save(grid,args.output/'coverage.csv')
 summary=grid.groupby('station_id',as_index=False).agg(expected=('observed','size'),observed=('observed','sum'),mean_temperature_c=('temperature_c','mean'),total_rain_mm=('rain_mm','sum'))
 summary['coverage_pct']=100*summary.observed/summary.expected;save(summary,args.output/'station_summary.csv')
 fig,ax=figure_start(11,5)
 for sid,part in grid.groupby('station_id'):
  ax.plot(part.local_date,part.temperature_c,marker='.',label=sid)
 ax.set_xticks(list(range(0,len(dates),max(1,len(dates)//7))));ax.tick_params(axis='x',rotation=25)
 ax.set_ylabel('Temperature (°C)');ax.set_xlabel('Local date (KST)');ax.set_title('Multi-station temperature (gaps remain missing)');ax.legend()
 finish(fig,args.output/'dashboard.png');print(f'PASS advanced_01: {len(ids)} stations, {int(grid.observed.sum())} observations')
if __name__=='__main__':run()
