"""Missing vs Zero: 없는 날짜를 복원하되 임의로 0을 채우지 않습니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
store=df.query('store_id == "ST-C"').set_index('date')['revenue_krw']
expected=pd.date_range('2026-08-20','2026-09-20',freq='D')
# TODO: 없는 날짜를 복원하되 임의로 0을 채우지 않습니다.
raise NotImplementedError('Complete the marked line before continuing')
print('Missing:',int(s.isna().sum()),'Observed zero:',int(s.eq(0).sum()))
fig,ax=plt.subplots(figsize=(8,3.4))
ax.plot(s.index,s.values,marker='o',label='Daily revenue')
ax.scatter(s[s.eq(0)].index,s[s.eq(0)].values,color='#b64b35',s=75,label='Observed zero')
ax.set(title='Missing is not zero',ylabel='Revenue (KRW)');ax.legend()
fig.autofmt_xdate();fig.tight_layout();fig.savefig(ROOT/'figures/05_missing_and_zero.png',dpi=145);plt.close(fig)
