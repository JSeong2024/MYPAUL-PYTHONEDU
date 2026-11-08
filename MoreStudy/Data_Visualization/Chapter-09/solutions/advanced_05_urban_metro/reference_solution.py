"""Advanced 05: station-hour completeness and zero vs missing ridership."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import pandas as pd
import numpy as np
import plotly.express as px
from core.utils import arguments,load,numeric,save,figure_start,finish

def extras(p):p.add_argument('--line',default='',help='L1/L2; empty=all')
def run():
 args=arguments('Urban Transportation Dashboard','advanced_05_urban_metro',extras)
 stations=load(args.data/'stations.csv',['station_id','station_name','line'])
 if stations.station_id.duplicated().any():raise ValueError('duplicate stations')
 if args.line and args.line not in set(stations.line):raise ValueError('unknown --line')
 df=load(args.data/'boardings.csv',['record_id','station_id','timestamp_kst','boardings'])
 df['boardings']=numeric(df.boardings);df['time']=pd.to_datetime(df.timestamp_kst,errors='coerce')
 bad=df.record_id.duplicated(keep=False)|df.duplicated(['station_id','timestamp_kst'],keep=False)|~df.station_id.isin(stations.station_id)|df.boardings.isna()|df.boardings.lt(0)|df.time.isna()
 audit=df.loc[bad,['record_id','station_id']].copy();audit['reason']='invalid_or_duplicate_record';save(audit,args.output/'audit.csv')
 df=df.loc[~bad].merge(stations,on='station_id',how='left')
 if args.line:df=df[df.line.eq(args.line)]
 active=stations if not args.line else stations[stations.line.eq(args.line)]
 dates=pd.date_range('2026-10-01','2026-10-10',freq='D')
 hours=[f'{d.date().isoformat()} {h:02d}:00' for d in dates for h in range(6,22)]
 expected=pd.MultiIndex.from_product([active.station_id,hours],names=['station_id','timestamp_kst']).to_frame(index=False)
 expected=expected.merge(df[['station_id','timestamp_kst','boardings']],on=['station_id','timestamp_kst'],how='left',validate='one_to_one')
 expected['observed']=expected.boardings.notna();expected=expected.merge(stations,on='station_id',how='left')
 save(expected,args.output/'hourly_coverage.csv')
 summary=expected.groupby(['line','station_id','station_name'],as_index=False).agg(expected=('observed','size'),observed=('observed','sum'),observed_boardings=('boardings','sum'))
 summary['missing']=summary.expected-summary.observed
 save(summary,args.output/'station_summary.csv')
 fig,ax=figure_start(11,5)
 ax.bar(summary.station_name,summary.observed_boardings);ax.set_ylabel('Recorded boardings (passengers)');ax.set_xlabel('Station')
 ax.set_title('Observed station boarding totals (not corrected for missing slots)')
 finish(fig,args.output/'dashboard.png')
 chart=px.bar(summary,x='station_name',y='observed_boardings',color='line',hover_data=['observed','missing'],title='Metro station ridership (observed slots)')
 (args.output/'dashboard.html').write_text(chart.to_html(include_plotlyjs='cdn',full_html=True,div_id='metro-dashboard'),encoding='utf-8')
 print(f'PASS advanced_05: {int(expected.observed.sum())}/{len(expected)} slots')
if __name__=='__main__':run()
