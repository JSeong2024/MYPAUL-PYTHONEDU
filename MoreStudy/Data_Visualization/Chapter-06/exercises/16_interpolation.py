"""Limited Interpolation: 누락 추정값을 최대 3개 연속 내부 공백에 한정합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/weather_hourly.csv',parse_dates=['timestamp_local'])
s=df.query('station_id == "W-C"').set_index('timestamp_local')['temperature_c'].sort_index()
expected=pd.date_range('2026-10-03','2026-10-04 23:00',freq='h')
# TODO: 누락 추정값을 최대 3개 연속 내부 공백에 한정합니다.
raise NotImplementedError('Complete the marked line before continuing')
print('Missing:',int(s.isna().sum()),'Estimated:',int((s.isna() & filled.notna()).sum()))
fig,ax=plt.subplots(figsize=(9,3.5))
ax.plot(s.index,s,label='Observed',lw=1.7)
ax.plot(filled.index,filled,ls='--',alpha=.7,label='Estimated (interpolation)')
ax.set(title='Measured vs estimated temperatures',ylabel='°C');ax.legend()
fig.tight_layout();fig.savefig(ROOT/'figures/18_interpolation.png',dpi=145);plt.close(fig)
