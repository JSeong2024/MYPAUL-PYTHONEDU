"""Advanced 04: hourly MW and full-day MWh; incomplete days stay partial."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import pandas as pd
import numpy as np
from core.utils import arguments,load,numeric,save,figure_start,finish

def extras(p):p.add_argument('--region',default='',help='region ID, empty=all')
def run():
 args=arguments('Regional Electricity Demand Analysis','advanced_04_electricity_demand',extras)
 ref=load(args.data/'regions.csv',['region_id','region_name'])
 if ref.region_id.duplicated().any():raise ValueError('duplicate region')
 if args.region and args.region not in set(ref.region_id):raise ValueError('unknown region filter')
 raw=load(args.data/'demand.csv',['reading_id','timestamp_utc','region_id','demand_mw'])
 raw['demand_mw']=numeric(raw.demand_mw)
 raw['timestamp_kst']=pd.to_datetime(raw.timestamp_utc,utc=True,errors='coerce').dt.tz_convert('Asia/Seoul')
 duplicate=raw.reading_id.duplicated(keep=False)|raw.duplicated(['region_id','timestamp_kst'],keep=False)
 bad=duplicate|raw.demand_mw.isna()|raw.demand_mw.lt(0)|~raw.region_id.isin(ref.region_id)|raw.timestamp_kst.isna()
 audit=raw.loc[bad,['reading_id','region_id']].copy();audit['reason']='invalid_or_duplicate_reading';save(audit,args.output/'audit.csv')
 df=raw.loc[~bad].copy();df['local_date']=df.timestamp_kst.dt.strftime('%Y-%m-%d');df['hour']=df.timestamp_kst.dt.hour
 if args.region:df=df[df.region_id.eq(args.region)]
 summary=df.groupby(['region_id','local_date'],as_index=False).agg(hour_count=('hour','nunique'),mean_demand_mw=('demand_mw','mean'),energy_observed_mwh=('demand_mw','sum'))
 summary['status']=np.where(summary.hour_count.eq(24),'complete','partial')
 summary['energy_confirmed_mwh']=summary.energy_observed_mwh.where(summary.status.eq('complete'))
 save(summary,args.output/'daily_energy.csv')
 fig,ax=figure_start(11,5)
 for region,part in df.groupby('region_id'):
  hourly=part.sort_values('timestamp_kst');ax.plot(hourly.timestamp_kst, hourly.demand_mw,label=region,linewidth=1)
 ax.set_ylabel('Demand (MW)');ax.set_xlabel('Observation time (Asia/Seoul)');ax.set_title('Regional hourly demand');ax.legend()
 finish(fig,args.output/'dashboard.png');print(f'PASS advanced_04: {len(df)} valid hourly readings')
if __name__=='__main__':run()
