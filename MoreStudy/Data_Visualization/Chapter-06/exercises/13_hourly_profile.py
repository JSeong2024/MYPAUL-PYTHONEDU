"""Hourly Profile: 시간대별 교통량 평균과 사용 관측 수를 함께 계산합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/traffic_hourly.csv')
df['time']=pd.to_datetime(df['timestamp_utc'],utc=True,errors='coerce').dt.tz_convert('Asia/Seoul')
df['count']=pd.to_numeric(df['vehicle_count'],errors='coerce')
s=df[df['corridor_id'].eq('R-01') & df['count'].ge(0)].drop_duplicates(['time'])
# TODO: 시간대별 교통량 평균과 사용 관측 수를 함께 계산합니다.
raise NotImplementedError('Complete the marked line before continuing')
print('Profile hours:',p['count'].notna().sum(),'Min samples:',int(p['count'].min()))
fig,axes=plt.subplots(2,1,figsize=(8,5.3),sharex=True,layout='constrained')
axes[0].plot(p.index,p['mean'],marker='o');axes[0].set(ylabel='Vehicles / hour',title='Typical hourly volume')
axes[1].bar(p.index,p['count']);axes[1].set(ylabel='Days observed',xlabel='Hour (KST)')
fig.savefig(ROOT/'figures/14_hourly_profile.png',dpi=145);plt.close(fig)
