"""Challenge 02: expected time grid, robust hourly baseline, reproducible anomaly report."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import pandas as pd
import numpy as np
import json, hashlib
from core.utils import arguments,load,numeric,save,figure_start,finish

def extras(p):
 p.add_argument('--threshold-mw',type=float,default=120.0,help='absolute residual threshold (MW)')
 p.add_argument('--region',default='',help='region ID; empty=all')
def run():
 args=arguments('Energy Demand & Anomaly Detection','challenge_02_energy_anomalies',extras)
 if args.threshold_mw<=0:raise ValueError('threshold must be > 0')
 regions=load(args.data/'regions.csv',['region_id','capacity_mw'])
 if regions.region_id.duplicated().any():raise ValueError('duplicate region')
 if args.region and args.region not in set(regions.region_id):raise ValueError('unknown region')
 df=load(args.data/'readings.csv',['reading_id','region_id','timestamp_utc','demand_mw'])
 df['demand_mw']=numeric(df.demand_mw)
 df['time']=pd.to_datetime(df.timestamp_utc,errors='coerce',utc=True).dt.tz_convert('Asia/Seoul')
 collision=df.duplicated('reading_id',keep=False)|df.duplicated(['region_id','time'],keep=False)
 bad=collision|~df.region_id.isin(regions.region_id)|df.demand_mw.isna()|df.demand_mw.lt(0)|df.time.isna()
 audit=df.loc[bad,['reading_id','region_id','timestamp_utc']].copy();audit.insert(0,'source_row',df.loc[bad].index+2);audit['reason']='invalid_or_conflicting_reading';save(audit,args.output/'audit.csv')
 valid=df.loc[~bad].copy()
 if args.region:valid=valid[valid.region_id.eq(args.region)]
 # fixed reference horizon: 15 days in KST, 24 hours per day, each registered region
 times=pd.date_range('2026-10-01T00:00:00',periods=15*24,freq='h',tz='Asia/Seoul')
 ids=[args.region] if args.region else sorted(regions.region_id)
 expected=pd.MultiIndex.from_product([ids,times],names=['region_id','time']).to_frame(index=False)
 joined=expected.merge(valid[['region_id','time','demand_mw']],on=['region_id','time'],how='left',validate='one_to_one')
 joined['observed']=joined.demand_mw.notna();joined['local_hour']=joined.time.dt.hour;joined['local_date']=joined.time.dt.strftime('%Y-%m-%d')
 save(joined.assign(time=joined.time.dt.strftime('%Y-%m-%dT%H:%M:%S%z')),args.output/'coverage.csv')
 hourly=joined[joined.observed].copy()
 medians=hourly.groupby(['region_id','local_hour'])['demand_mw'].median().rename('hour_median_mw')
 hourly=hourly.join(medians,on=['region_id','local_hour'])
 hourly['residual_mw']=hourly.demand_mw-hourly.hour_median_mw
 hourly['anomaly']=hourly.residual_mw.abs().gt(args.threshold_mw)
 anomalies=hourly.loc[hourly.anomaly,['region_id','time','demand_mw','hour_median_mw','residual_mw']].copy()
 anomalies['time']=anomalies.time.dt.strftime('%Y-%m-%dT%H:%M:%S%z')
 save(anomalies,args.output/'anomalies.csv')
 inc=load(args.data/'incidents.csv',['incident_id','region_id','start_utc','end_utc','type'])
 if inc.incident_id.duplicated().any() or ~inc.region_id.isin(regions.region_id).all():raise ValueError('incident reference violated')
 intervals=[]
 for _,r in inc.iterrows():
  start=pd.to_datetime(r.start_utc,utc=True,errors='coerce');end=pd.to_datetime(r.end_utc,utc=True,errors='coerce')
  if pd.isna(start) or pd.isna(end) or start>=end:raise ValueError('invalid incident interval')
  intervals.append((r.incident_id,r.region_id,start,end))
 comparison=[]
 for iid,rid,start,end in intervals:
  subset=hourly[(hourly.region_id.eq(rid))&(hourly.time>=start)&(hourly.time<end)]
  comparison.append({'incident_id':iid,'region_id':rid,'observed_hours':len(subset),'anomaly_hours':int(subset.anomaly.sum())})
 save(pd.DataFrame(comparison),args.output/'incident_comparison.csv')
 daily=joined.groupby(['region_id','local_date'],as_index=False).agg(expected=('observed','size'),observed=('observed','sum'),observed_energy_mwh=('demand_mw','sum'))
 daily['status']=np.where(daily.expected.eq(daily.observed),'complete','partial');daily['confirmed_mwh']=daily.observed_energy_mwh.where(daily.status.eq('complete'))
 save(daily,args.output/'daily_summary.csv')
 fig,ax=figure_start(11,5)
 for rid,g in hourly.groupby('region_id'):ax.plot(g.time,g.demand_mw,label=rid,linewidth=1)
 for _,r in hourly[hourly.anomaly].iterrows():ax.scatter([r.time],[r.demand_mw],marker='x',s=40)
 ax.set_ylabel('Demand (MW)');ax.set_xlabel('Local time (Asia/Seoul)');ax.set_title('Hourly demand with threshold anomalies');ax.legend()
 finish(fig,args.output/'report.png')
 manifest={'threshold_mw':args.threshold_mw,'region_filter':args.region,'valid_count':len(hourly),'missing_slots':int((~joined.observed).sum()),'anomalies':len(anomalies)}
 (args.output/'summary.json').write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
 print(f'PASS challenge_02: {len(anomalies)} anomalies / {int((~joined.observed).sum())} missing slots')
if __name__=='__main__':run()
