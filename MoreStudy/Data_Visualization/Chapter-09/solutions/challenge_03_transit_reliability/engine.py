"""City transit reliability engine: strict contracts, auditable exclusions, deterministic outputs."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
import re
from pathlib import Path
import shutil
import sys
import tempfile
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

REQUIRED={
 'stops.csv':['stop_id','line','stop_name'],
 'schedule.csv':['stop_id','local_date','expected_hour'],
 'operations.csv':['observation_id','stop_id','timestamp_utc','boardings','delay_minutes'],
 'incidents.csv':['incident_id','stop_id','opened_utc','closed_utc','category']
}
OUTPUT_FILES=['audit.csv','coverage.csv','station_summary.csv','daily_summary.csv','incident_comparison.csv','hourly.csv','overview.png','explorer.html','summary.json']

def read_data(data_dir):
 tables={}
 for filename,headers in REQUIRED.items():
  path=data_dir/filename
  if not path.is_file():raise ValueError(f'{filename}: file is missing')
  try:d=pd.read_csv(path,dtype=str,keep_default_na=False)
  except Exception as exc:raise ValueError(f'{filename}: cannot parse CSV: {exc}') from exc
  if not set(headers).issubset(d.columns) or len(d.columns)!=len(set(d.columns)):
   raise ValueError(f'{filename}: missing or duplicate columns')
  if d.empty and filename in ('stops.csv','schedule.csv'):
   raise ValueError(f'{filename}: reference table cannot be empty')
  tables[filename]=d
 return tables

def parse_utc(value):
 value=str(value).strip()
 if not (value.endswith('Z') or value.endswith('+00:00')):return pd.NaT
 try:return pd.Timestamp(value).tz_convert('UTC')
 except (ValueError,TypeError,OverflowError):return pd.NaT

def reference_data(tables):
 stops=tables['stops.csv'];sched=tables['schedule.csv'];inc=tables['incidents.csv']
 if stops.stop_id.duplicated().any() or stops[['stop_id','line','stop_name']].eq('').any().any():
  raise ValueError('stops.csv: duplicate or empty reference value')
 known=set(stops.stop_id)
 if inc.incident_id.duplicated().any() or inc[['incident_id','category']].eq('').any().any() or not inc.stop_id.isin(known).all():
  raise ValueError('incidents.csv: invalid incident identifier or stop reference')
 intervals=[]
 for n,r in inc.iterrows():
  start=parse_utc(r.opened_utc);end=parse_utc(r.closed_utc)
  if pd.isna(start) or pd.isna(end) or start>=end:
   raise ValueError(f'incidents.csv line {n+2}: invalid UTC [start, end)')
  intervals.append({'incident_id':r.incident_id,'stop_id':r.stop_id,'category':r.category,'start':start,'end':end})
 schedule=[];keys=set()
 for n,r in sched.iterrows():
  try:
   day=pd.Timestamp(r.local_date)
   if not r.local_date or day.strftime('%Y-%m-%d')!=r.local_date:raise ValueError('bad date')
   if not str(r.expected_hour).isdigit():raise ValueError('hour must be integer')
   hour=int(r.expected_hour)
   if hour<0 or hour>23:raise ValueError('hour outside 0..23')
   if r.stop_id not in known:raise ValueError('unknown stop')
   key=(r.stop_id,r.local_date,hour)
   if key in keys:raise ValueError('duplicate expected slot')
   keys.add(key);schedule.append(key)
  except (ValueError,TypeError,OverflowError) as exc:
   raise ValueError(f'schedule.csv line {n+2}: {exc}') from exc
 return stops, pd.DataFrame(schedule,columns=['stop_id','local_date','expected_hour']), keys, intervals

def inspect_operations(df,known,expected):
 ids=Counter(df.observation_id)
 prepared=[];slot_counts=Counter()
 for i,r in df.iterrows():
  stamp=parse_utc(r.timestamp_utc)
  key=None
  if not pd.isna(stamp) and r.stop_id in known:
   local=stamp.tz_convert('Asia/Seoul')
   key=(r.stop_id,local.strftime('%Y-%m-%d'),local.hour)
   if key in expected:slot_counts[key]+=1
  prepared.append((stamp,key))
 valid=[];audit=[]
 for i,r in df.iterrows():
  stamp,key=prepared[i]
  reasons=[]
  if not r.observation_id:reasons.append('missing_observation_id')
  elif ids[r.observation_id]>1:reasons.append('duplicate_observation_id')
  if r.stop_id not in known:reasons.append('unknown_stop')
  if pd.isna(stamp):reasons.append('invalid_timestamp_utc')
  elif key not in expected or stamp.tz_convert('Asia/Seoul').minute!=0 or stamp.tz_convert('Asia/Seoul').second!=0 or stamp.tz_convert('Asia/Seoul').microsecond!=0:
   reasons.append('unexpected_slot')
  if key in expected and slot_counts[key]>1:reasons.append('duplicate_slot')
  try:
   board=int(r.boardings)
   if not re.fullmatch(r'[0-9]+',str(r.boardings).strip()) or board<0:raise ValueError('invalid passengers')
  except (ValueError,TypeError,OverflowError):board=None;reasons.append('invalid_boardings')
  try:
   delay=float(r.delay_minutes)
   if not math.isfinite(delay) or delay<0:raise ValueError('invalid delay')
  except (ValueError,TypeError,OverflowError):delay=None;reasons.append('invalid_delay')
  if reasons:
   audit.append({'source_row':i+2,'observation_id':r.observation_id,'stop_id':r.stop_id,'reason_codes':';'.join(reasons)})
  else:
   valid.append({'observation_id':r.observation_id,'stop_id':r.stop_id,'local_date':key[1], 'expected_hour':key[2], 'boardings':board,'delay_minutes':delay,'timestamp_utc':stamp})
 return pd.DataFrame(valid,columns=['observation_id','stop_id','local_date','expected_hour','boardings','delay_minutes','timestamp_utc']), pd.DataFrame(audit,columns=['source_row','observation_id','stop_id','reason_codes'])

def selection(stops,schedule,valid,intervals,args):
 if args.start>args.end:raise ValueError('--start must not exceed --end')
 subset=stops
 if args.line:
  if args.line not in set(stops.line):raise ValueError(f'unknown --line: {args.line}')
  subset=subset[subset.line.eq(args.line)]
 if args.stops:
  ids=set(v.strip() for v in args.stops.split(',') if v.strip())
  if not ids.issubset(set(stops.stop_id)):raise ValueError('unknown --stops ID')
  subset=subset[subset.stop_id.isin(ids)]
 selected_ids=set(subset.stop_id)
 schedule=schedule[schedule.stop_id.isin(selected_ids)&schedule.local_date.between(args.start,args.end)].copy()
 valid=valid[valid.stop_id.isin(selected_ids)&valid.local_date.between(args.start,args.end)].copy()
 intervals=[r for r in intervals if r['stop_id'] in selected_ids]
 return subset,schedule,valid,intervals

def analyze(tables,args):
 stops,scheduled,keys,intervals=reference_data(tables)
 valid,audit=inspect_operations(tables['operations.csv'],set(stops.stop_id),keys)
 stops,scheduled,valid,intervals=selection(stops,scheduled,valid,intervals,args)
 cov=scheduled.merge(valid[['stop_id','local_date','expected_hour','boardings','delay_minutes','timestamp_utc']],on=['stop_id','local_date','expected_hour'],how='left',validate='one_to_one')
 cov=cov.merge(stops[['stop_id','stop_name','line']],on='stop_id',how='left',validate='many_to_one')
 cov['observed']=cov.boardings.notna();cov['missing']=~cov.observed
 cov['slot_status']=np.where(cov.observed,'valid','missing')
 cov=cov.sort_values(['local_date','expected_hour','stop_id']).reset_index(drop=True)
 daily=cov.groupby(['line','stop_id','stop_name','local_date'],as_index=False).agg(expected=('observed','size'),valid=('observed','sum'),observed_boardings=('boardings','sum'),mean_delay_min=('delay_minutes','mean'))
 daily['missing']=daily.expected-daily.valid;daily['status']=np.where(daily.missing.eq(0),'complete','partial')
 daily['confirmed_boardings']=daily.observed_boardings.where(daily.status.eq('complete'))
 station=cov.groupby(['line','stop_id','stop_name'],as_index=False).agg(expected=('observed','size'),valid=('observed','sum'),observed_boardings=('boardings','sum'),mean_delay_min=('delay_minutes','mean'))
 station['missing']=station.expected-station.valid;station['coverage_pct']=np.where(station.expected.gt(0),100*station.valid/station.expected,np.nan)
 station['confirmed_boardings']=station.observed_boardings.where(station.missing.eq(0))
 hourly=cov.groupby(['local_date','expected_hour','line'],as_index=False).agg(expected=('observed','size'),valid=('observed','sum'),observed_boardings=('boardings','sum'),mean_delay_min=('delay_minutes','mean'))
 hourly['missing']=hourly.expected-hourly.valid
 # For missing-only groups, observed_boardings remains blank, not zero.
 hourly['observed_boardings']=hourly.observed_boardings.where(hourly.valid.gt(0))
 comp=[]
 for obj in intervals:
  r=cov[cov.stop_id.eq(obj['stop_id'])].copy()
  if len(r):
   r['slot_start_utc']=pd.to_datetime(r.local_date+' '+r.expected_hour.astype(str).str.zfill(2)+':00').dt.tz_localize('Asia/Seoul').dt.tz_convert('UTC')
   affected=r[(r.slot_start_utc>=obj['start'])&(r.slot_start_utc<obj['end'])]
  else:affected=r
  comp.append({'incident_id':obj['incident_id'],'stop_id':obj['stop_id'],'category':obj['category'],'expected_overlap_slots':len(affected),'valid_overlap_slots':int(affected.observed.sum()),'missing_overlap_slots':int(affected.missing.sum()),'observed_boardings':int(affected.boardings.sum())})
 incident=pd.DataFrame(comp,columns=['incident_id','stop_id','category','expected_overlap_slots','valid_overlap_slots','missing_overlap_slots','observed_boardings'])
 summary={'scheduled_slots':int(len(cov)),'valid_slots':int(cov.observed.sum()),'missing_slots':int(cov.missing.sum()),'excluded_source_rows':int(len(audit)),'observed_boardings':int(cov.boardings.sum()),'partial_station_days':int(daily.status.eq('partial').sum())}
 return {'coverage':cov,'audit':audit,'daily_summary':daily,'station_summary':station,'hourly':hourly,'incident_comparison':incident,'summary':summary}

def plot_outputs(result,folder,args):
 station=result['station_summary']; hourly=result['hourly'];coverage=result['coverage']
 fig,axes=plt.subplots(2,1,figsize=(11,8),dpi=125)
 if len(station):
  axes[0].bar(station.stop_id,station.coverage_pct)
  axes[0].tick_params(axis='x',rotation=45)
 axes[0].set_ylim(0,105);axes[0].set_ylabel('Coverage (%)');axes[0].set_title('Expected slots vs observed slots')
 if len(hourly):
  t=hourly.groupby(['local_date','expected_hour'],as_index=False).agg(expected=('expected','sum'),valid=('valid','sum'),observed_boardings=('observed_boardings','sum'))
  x=t.local_date+' '+t.expected_hour.astype(str).str.zfill(2)+':00'
  axes[1].plot(x,t.observed_boardings,label='Observed boardings')
  axes[1].set_xticks(list(range(0,len(x),max(1,len(x)//8))));axes[1].tick_params(axis='x',rotation=25)
 else:axes[1].text(.5,.5,'No scheduled slots in the selected range',ha='center',transform=axes[1].transAxes)
 axes[1].set_xlabel('Local hour (Asia/Seoul)');axes[1].set_ylabel('Observed passengers');axes[1].grid(alpha=.2)
 fig.suptitle(f'Transit reliability: {args.start} to {args.end} (KST)')
 fig.tight_layout();fig.savefig(folder/'overview.png',dpi=125,metadata={'Software':'Matplotlib'});plt.close(fig)
 chart=make_subplots(rows=2,cols=1,shared_xaxes=False,subplot_titles=('Stop coverage (%)','Hourly observed passengers'))
 if len(station):chart.add_trace(go.Bar(x=station.stop_id,y=station.coverage_pct,customdata=station[['expected','valid','missing']],hovertemplate='Stop=%{x}<br>Coverage=%{y:.1f}%<br>Expected=%{customdata[0]}<br>Valid=%{customdata[1]}<br>Missing=%{customdata[2]}<extra></extra>',name='Coverage'),row=1,col=1)
 if len(hourly):
  time=hourly.local_date+' '+hourly.expected_hour.astype(str).str.zfill(2)+':00'
  for line,g in hourly.assign(time=time).groupby('line'):
   chart.add_trace(go.Scatter(x=g.time,y=g.observed_boardings,mode='lines+markers',name=line,connectgaps=False,customdata=g[['expected','valid','missing']],hovertemplate='Local hour=%{x}<br>Observed passengers=%{y}<br>Expected=%{customdata[0]}<br>Valid=%{customdata[1]}<br>Missing=%{customdata[2]}<extra></extra>'),row=2,col=1)
 chart.update_yaxes(title_text='Coverage (%)',range=[0,105],row=1,col=1)
 chart.update_yaxes(title_text='Boardings (passengers)',row=2,col=1)
 chart.update_layout(height=800,title=f'Transit Reliability | KST {args.start}..{args.end}',meta=result['summary'])
 (folder/'explorer.html').write_text(chart.to_html(include_plotlyjs=True,full_html=True,div_id='transit-reliability'),encoding='utf-8')

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def export(result,args,folder):
 folder.mkdir(parents=True,exist_ok=True)
 for name in ['audit','coverage','station_summary','daily_summary','incident_comparison','hourly']:
  frame=result[name].copy()
  if name=='coverage':
   frame=frame.drop(columns=['timestamp_utc'],errors='ignore')
  frame.to_csv(folder/(name+'.csv'),index=False,float_format='%.4f',na_rep='',encoding='utf-8')
 (folder/'summary.json').write_text(json.dumps(result['summary'],sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 plot_outputs(result,folder,args)
 manifest={'schema_version':2,'timezone':'Asia/Seoul','interval':'[start, end)','filters':{'line':args.line,'stops':sorted(args.stops.split(',')) if args.stops else [],'start':args.start,'end':args.end},'input_sha256':{name:digest(args.data/name) for name in sorted(REQUIRED)},'output_sha256':{name:digest(folder/name) for name in sorted(OUTPUT_FILES)},'metrics':result['summary']}
 (folder/'manifest.json').write_text(json.dumps(manifest,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def run(argv=None):
 parser=argparse.ArgumentParser(description='City Transit Reliability Platform')
 root=Path(__file__).resolve().parents[2]
 parser.add_argument('--data',type=Path,default=root/'projects'/'challenge_03_transit_reliability'/'data')
 parser.add_argument('--output',type=Path,default=root/'output'/'challenge_03_transit_reliability')
 parser.add_argument('--start',default='2026-10-01');parser.add_argument('--end',default='2026-10-07')
 parser.add_argument('--line',default='');parser.add_argument('--stops',default='',help='comma-separated stop IDs')
 args=parser.parse_args(argv)
 stage=None
 try:
  tables=read_data(args.data)
  result=analyze(tables,args)
  args.output.parent.mkdir(parents=True,exist_ok=True)
  stage=Path(tempfile.mkdtemp(prefix='.stage_transit_',dir=str(args.output.parent)))
  export(result,args,stage)
  if args.output.is_dir():shutil.rmtree(args.output)
  stage.rename(args.output);stage=None
  print('PASS: required outputs completed | '+', '.join(f'{k}={v}' for k,v in result['summary'].items()))
  return 0
 except (ValueError,OSError,KeyError) as exc:
  print(f'FAIL: {exc}',file=sys.stderr);return 1
 finally:
  if stage is not None:shutil.rmtree(stage,ignore_errors=True)

if __name__=='__main__':sys.exit(run())
