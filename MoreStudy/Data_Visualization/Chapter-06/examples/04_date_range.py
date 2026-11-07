import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/server_metrics.csv')
df['time']=pd.to_datetime(df['timestamp_utc'],utc=True)
expected=pd.date_range('2026-10-26', '2026-10-27 23:55',freq='5min',tz='UTC')
observed=pd.DatetimeIndex(df['time'])
missing=expected.difference(observed)
print('Expected:',len(expected),'Observed:',len(observed),'Missing:',len(missing))
fig,ax=plt.subplots(figsize=(8,2.6))
ax.scatter(df['time'],[1]*len(df),s=3,label='Observed')
ax.scatter(missing,[1.12]*len(missing),s=36,marker='x',color='#b84444',label='Missing')
ax.set(title='Expected vs observed five-minute timestamps',yticks=[])
ax.legend();fig.tight_layout();fig.savefig(ROOT/'figures/04_date_range.png',dpi=145);plt.close(fig)
