"""Last 60 Minutes: 최근 60분 관측 중 8개 이상이 존재할 때만 평균을 계산합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/server_metrics.csv')
df['time']=pd.to_datetime(df['timestamp_utc'],utc=True)
s=df.set_index('time')['latency_ms'].sort_index()
count=s.rolling('60min').count()
# TODO: 최근 60분 관측 중 8개 이상이 존재할 때만 평균을 계산합니다.
raise NotImplementedError('Complete the marked line before continuing')
print('Rolling sample count range:',int(count.min()),int(count.max()))
fig,ax=plt.subplots(figsize=(9,3.5))
ax.plot(s.index,s,alpha=.25,label='Observed')
ax.plot(mean.index,mean,label='Last 60 minutes (min 8)',lw=1.8)
ax.set(title='Time-based rolling mean',ylabel='Latency (ms)');ax.legend()
fig.tight_layout();fig.savefig(ROOT/'figures/10_rolling_time.png',dpi=145);plt.close(fig)
