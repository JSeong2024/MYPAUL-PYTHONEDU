"""Challenge 01: flight cancellations and arrival performance with explicit denominators."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import pandas as pd
import numpy as np
import json
from core.utils import arguments,load,numeric,save,figure_start,finish

def extras(p):
 p.add_argument('--airport',default='',help='Airport ID, empty = all')
 p.add_argument('--start',default='2026-10-01');p.add_argument('--end',default='2026-10-14')
def run():
 args=arguments('Airport Operations Analysis','challenge_01_airport_operations',extras)
 airports=load(args.data/'airports.csv',['airport_id','airport_name'])
 if airports.airport_id.duplicated().any():raise ValueError('duplicate airport reference')
 if args.airport and args.airport not in set(airports.airport_id):raise ValueError('unknown airport filter')
 df=load(args.data/'flights.csv',['flight_id','flight_date','airport_id','airline','status','arrival_delay_min'])
 df['delay']=numeric(df.arrival_delay_min)
 times=pd.to_datetime(df.flight_date,errors='coerce')
 operated=df.status.eq('operated');cancelled=df.status.eq('cancelled')
 bad=df.flight_id.duplicated(keep=False)|df.flight_id.eq('')|~df.airport_id.isin(airports.airport_id)|times.isna()|~(operated|cancelled)|(operated & df.delay.isna())|(cancelled & df.arrival_delay_min.ne(''))
 reasons=[]
 for i,row in df.iterrows():
  codes=[]
  if df.flight_id.eq(row.flight_id).sum()>1 or not row.flight_id:codes.append('duplicate_or_missing_id')
  if row.airport_id not in set(airports.airport_id):codes.append('unknown_airport')
  if pd.isna(times.iloc[i]):codes.append('invalid_date')
  if row.status not in ('operated','cancelled'):codes.append('invalid_status')
  if row.status=='operated' and pd.isna(df.delay.iloc[i]):codes.append('invalid_delay')
  if row.status=='cancelled' and row.arrival_delay_min!='':codes.append('cancelled_delay_not_empty')
  reasons.append(';'.join(codes))
 audit=df.loc[bad,['flight_id','airport_id']].copy();audit.insert(0,'source_row',df.loc[bad].index+2);audit['reason_codes']=[reasons[i] for i in df.loc[bad].index]
 save(audit,args.output/'audit.csv')
 valid=df.loc[~bad].copy()
 valid=valid[valid.flight_date.between(args.start,args.end)]
 if args.airport:valid=valid[valid.airport_id.eq(args.airport)]
 def group(part):
  n=len(part);op=part[part.status.eq('operated')];cancel=n-len(op)
  late=int(op.delay.ge(15).sum())
  return pd.Series({'scheduled':n,'operated':len(op),'cancelled':cancel,'on_time':len(op)-late,'delayed_15plus':late,'cancellation_pct':100*cancel/n if n else np.nan,'on_time_pct':100*(len(op)-late)/len(op) if len(op) else np.nan,'mean_delay_min':float(op.delay.mean()) if len(op) else np.nan})
 summary=valid.groupby('airport_id').apply(group,include_groups=False).reset_index() if len(valid) else pd.DataFrame(columns=['airport_id','scheduled','operated','cancelled','on_time','delayed_15plus','cancellation_pct','on_time_pct','mean_delay_min'])
 save(summary,args.output/'airport_summary.csv')
 daily=valid.groupby(['flight_date','airport_id']).apply(group,include_groups=False).reset_index() if len(valid) else pd.DataFrame()
 save(daily,args.output/'daily_summary.csv')
 fig,ax=figure_start(10,5)
 if len(summary):ax.bar(summary.airport_id,summary.on_time_pct)
 ax.set_ylim(0,100);ax.set_ylabel('On-time arrivals / operated flights (%)');ax.set_xlabel('Airport')
 ax.set_title('Arrival punctuality, cancellations excluded from on-time denominator')
 finish(fig,args.output/'report.png')
 (args.output/'summary.json').write_text(json.dumps({'valid_flights':len(valid),'excluded_raw_rows':len(audit),'filter':{'airport':args.airport,'start':args.start,'end':args.end}},ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
 print(f'PASS challenge_01: {len(valid)} scheduled / {len(audit)} audit rows')
if __name__=='__main__':run()
