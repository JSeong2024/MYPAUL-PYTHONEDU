"""7-Day Complete Mean: 누락값이 있는 구간을 평균으로 채우지 않는 7일 이동평균을 구합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
s=df.query('store_id == "ST-B"').set_index('date')['revenue_krw'].sort_index()
s=s.reindex(pd.date_range(s.index.min(),s.index.max(),freq='D'))
# TODO: 누락값이 있는 구간을 평균으로 채우지 않는 7일 이동평균을 구합니다.
raise NotImplementedError('Complete the marked line before continuing')
print('Rolling valid:',int(mean7.notna().sum()),'Missing daily:',int(s.isna().sum()))
fig,ax=plt.subplots(figsize=(9,3.4))
ax.plot(s.index,s.values,alpha=.35,label='Daily')
ax.plot(mean7.index,mean7.values,lw=2,label='7-day mean (complete window)')
ax.set(title='Rolling seven-day average',ylabel='KRW');ax.legend()
fig.tight_layout();fig.savefig(ROOT/'figures/09_rolling_count.png',dpi=145);plt.close(fig)
