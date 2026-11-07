"""Rolling Threshold: 최근 완전한 12개 관측을 이용해 경고선과 비교합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/server_metrics.csv')
df['time']=pd.to_datetime(df['timestamp_utc'],utc=True)
s=df.set_index('time')['latency_ms'].sort_index().reindex(pd.date_range('2026-10-26','2026-10-27 23:55',freq='5min',tz='UTC'))
# TODO: 최근 완전한 12개 관측을 이용해 경고선과 비교합니다.
raise NotImplementedError('Complete the marked line before continuing')
limit=500
print('Observed exceedances:',int(s.gt(limit).sum()),'Rolling exceedances:',int(avg.gt(limit).sum()))
fig,ax=plt.subplots(figsize=(9,3.5))
ax.plot(s.index,s,alpha=.32,label='Observed');ax.plot(avg.index,avg,lw=2,label='1-hour complete mean')
ax.axhline(limit,color='#b74444',ls='--',label='Illustrative review threshold')
ax.set(title='Momentary vs sustained latency',ylabel='Latency (ms)');ax.legend()
fig.tight_layout();fig.savefig(ROOT/'figures/24_alert_rolling.png',dpi=145);plt.close(fig)
