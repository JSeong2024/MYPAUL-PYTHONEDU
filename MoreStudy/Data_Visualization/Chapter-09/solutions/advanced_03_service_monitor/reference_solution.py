"""Advanced 03: strict request-level audit, P95 and server error rate."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import pandas as pd
import numpy as np
import re
from html import escape
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from core.utils import arguments,load,numeric,save,figure_start,finish

def extras(p):
 p.add_argument('--start',default='2026-10-01');p.add_argument('--end',default='2026-10-14')
 p.add_argument('--services',default='',help='comma-separated service IDs; empty=all')

def strict_utc(value):
 try:
  value=str(value).strip()
  if not value.endswith('Z') and not value.endswith('+00:00'):return pd.NaT
  return pd.Timestamp(value).tz_convert('Asia/Seoul')
 except (ValueError,TypeError,OverflowError):return pd.NaT

def run():
 args=arguments('Service Performance Monitoring','advanced_03_service_monitor',extras)
 catalog=load(args.data/'service_catalog.csv',['service_id','service_name'])
 if catalog.service_id.duplicated().any() or not catalog.service_id.str.strip().all():raise ValueError('invalid service_catalog.csv keys')
 df=load(args.data/'requests.csv',['request_id','timestamp_utc','service_id','latency_ms','status_code'])
 duplicates=df.request_id.duplicated(keep=False)|df.request_id.eq('')
 latency=numeric(df.latency_ms)
 codes=numeric(df.status_code)
 times=pd.Series((strict_utc(v) for v in df.timestamp_utc),index=df.index)
 reasons=[]
 for i,row in df.iterrows():
  marks=[]
  if duplicates.iloc[i]:marks.append('duplicate_or_missing_request_id')
  if pd.isna(latency.iloc[i]) or latency.iloc[i]<0:marks.append('invalid_latency')
  c=codes.iloc[i]
  if pd.isna(c) or not re.fullmatch(r'[1-5][0-9]{2}',row.status_code.strip()):marks.append('invalid_status_code')
  if row.service_id not in set(catalog.service_id):marks.append('unknown_service_id')
  if pd.isna(times.iloc[i]):marks.append('invalid_utc_timestamp')
  reasons.append(';'.join(marks))
 audit=pd.DataFrame({'source_row':df.index+2,'request_id':df.request_id,'reason_codes':reasons})
 audit=audit[audit.reason_codes.ne('')];save(audit,args.output/'audit.csv')
 valid=df.loc[[not x for x in reasons]].copy()
 valid['timestamp_kst']=[times.iloc[i] for i in valid.index]
 valid['latency_ms']=latency.loc[valid.index].astype(float);valid['status_code']=codes.loc[valid.index].astype(int)
 valid['local_date']=pd.to_datetime(valid.timestamp_kst).dt.strftime('%Y-%m-%d')
 chosen=set(args.services.split(',')) if args.services else set(catalog.service_id)
 if chosen-set(catalog.service_id):raise ValueError('Unknown --services ID')
 if args.start>args.end:raise ValueError('--start must be <= --end')
 selected=valid[valid.service_id.isin(chosen)&valid.local_date.between(args.start,args.end)].copy()
 selected['local_hour']=pd.to_datetime(selected.timestamp_kst).dt.strftime('%Y-%m-%d %H:00')
 save(selected.drop(columns=['timestamp_kst']),args.output/'valid_requests.csv')
 def calc(part):
  if part.empty:return {'request_count':0,'p95_ms':np.nan,'error_rate_pct':np.nan}
  return {'request_count':len(part),'p95_ms':float(part.latency_ms.quantile(.95,interpolation='linear')),'error_rate_pct':100*float(part.status_code.between(500,599).sum())/len(part)}
 rows=[]
 for sid in sorted(chosen):rows.append({'service_id':sid,**calc(selected[selected.service_id.eq(sid)])})
 summary=pd.DataFrame(rows,columns=['service_id','request_count','p95_ms','error_rate_pct']);save(summary,args.output/'summary.csv')
 display=summary[['service_id','request_count']].copy()
 display['p95_ms']=summary.p95_ms.map(lambda v: '자료 없음' if pd.isna(v) else f'{v:.2f} ms')
 display['error_rate_pct']=summary.error_rate_pct.map(lambda v: '자료 없음' if pd.isna(v) else f'{v:.2f}%')
 save(display,args.output/'kpi_display.csv')
 hourly=[]
 hours=pd.date_range(args.start+' 00:00',args.end+' 23:00',freq='h')
 for sid in sorted(chosen):
  part=selected[selected.service_id.eq(sid)]
  grouped={key:group for key,group in part.groupby('local_hour')}
  for dt in hours:
   key=dt.strftime('%Y-%m-%d %H:00')
   hourly.append({'service_id':sid,'local_hour':key,**calc(grouped.get(key,part.iloc[0:0]))})
 hour_frame=pd.DataFrame(hourly,columns=['service_id','local_hour','request_count','p95_ms','error_rate_pct'])
 save(hour_frame,args.output/'hourly.csv')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(3,1,figsize=(12,9),dpi=125,sharex=True)
 for sid in sorted(chosen):
  g=hour_frame[hour_frame.service_id.eq(sid)]
  axes[0].plot(g.local_hour,g.request_count,label=sid,linewidth=1.5)
  axes[1].plot(g.local_hour,g.p95_ms,label=sid,linewidth=1.5)
  axes[2].plot(g.local_hour,g.error_rate_pct,label=sid,linewidth=1.5)
 axes[0].set_ylabel('Requests');axes[1].set_ylabel('P95 latency (ms)');axes[2].set_ylabel('Server error rate (%)')
 axes[2].set_xlabel('Local hour (Asia/Seoul)')
 for ax in axes:ax.grid(alpha=.2);ax.legend(loc='upper right',ncol=3,fontsize=7)
 axes[2].set_xticks(list(range(0,len(hours),max(1,len(hours)//7))))
 axes[2].tick_params(axis='x',rotation=25)
 axes[0].set_title(f'Service performance (KST {args.start} to {args.end})')
 finish(fig,args.output/'dashboard.png')
 chart=make_subplots(rows=3,cols=1,shared_xaxes=True,subplot_titles=('Request count','P95 latency (ms)','Server error rate (%)'))
 for sid in sorted(chosen):
  g=hour_frame[hour_frame.service_id.eq(sid)]
  chart.add_trace(go.Scatter(x=g.local_hour,y=g.request_count,mode='lines',name=sid,legendgroup=sid,showlegend=True),row=1,col=1)
  chart.add_trace(go.Scatter(x=g.local_hour,y=g.p95_ms,mode='lines',name=sid+' P95',legendgroup=sid,showlegend=False,connectgaps=False),row=2,col=1)
  chart.add_trace(go.Scatter(x=g.local_hour,y=g.error_rate_pct,mode='lines',name=sid+' 5xx',legendgroup=sid,showlegend=False,connectgaps=False),row=3,col=1)
 chart.update_layout(title=f'Service performance (KST {args.start}..{args.end})',height=900)
 html=chart.to_html(include_plotlyjs='cdn',full_html=True,div_id='service-performance')
 # Text KPIs use the same summary as CSV/plots. Empty denominator is not 0%.
 rows_html=''.join('<tr>'+''.join('<td>'+escape(str(v))+'</td>' for v in row)+'</tr>' for row in display.itertuples(index=False,name=None))
 kpi_html='<section style="font:14px Arial,sans-serif;max-width:1100px;margin:16px auto"><h2>Service KPIs (KST)</h2><table border="1" cellpadding="8" cellspacing="0"><thead><tr><th>Service</th><th>Valid requests</th><th>P95</th><th>Server error rate</th></tr></thead><tbody>'+rows_html+'</tbody></table></section>'
 html=html.replace('<body>', '<body>\n'+kpi_html,1)
 (args.output/'dashboard.html').write_text(html,encoding='utf-8')
 print(f'PASS advanced_03: {len(selected)} valid selected / {len(audit)} audited')
if __name__=='__main__':run()
