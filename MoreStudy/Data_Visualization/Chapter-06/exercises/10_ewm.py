"""EWM Smoothing: 최근 관측에 더 큰 가중치를 주는 EWM을 계산합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=pd.read_csv(ROOT/'data/server_metrics.csv')
s['time']=pd.to_datetime(s['timestamp_utc'],utc=True)
s=s.set_index('time')['latency_ms'].sort_index().reindex(pd.date_range('2026-10-26','2026-10-27 23:55',freq='5min',tz='UTC'))
# TODO: 최근 관측에 더 큰 가중치를 주는 EWM을 계산합니다.
raise NotImplementedError('Complete the marked line before continuing')
r=s.rolling(12,min_periods=12).mean()
print('Series length:',len(s),'EWM valid:',int(e.notna().sum()))
fig,ax=plt.subplots(figsize=(9,3.4))
ax.plot(s.index,s,alpha=.23,label='Observed')
ax.plot(e.index,e,label='EWM (span 12)');ax.plot(r.index,r,label='Complete 12-sample mean')
ax.set(title='Smoothing: EWM vs rolling',ylabel='Latency (ms)');ax.legend()
fig.tight_layout();fig.savefig(ROOT/'figures/11_ewm.png',dpi=145);plt.close(fig)
