"""Week Ending Sunday: 일요일로 끝나는 주의 합계와 관측 일수를 계산합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
s=df.query('store_id == "ST-A"').set_index('date')['revenue_krw'].sort_index()
# TODO: 일요일로 끝나는 주의 합계와 관측 일수를 계산합니다.
raise NotImplementedError('Complete the marked line before continuing')
print('First week observed days:',int(weekly.iloc[0]['count']),'Last:',int(weekly.iloc[-1]['count']))
fig,ax=plt.subplots(figsize=(9,3.4))
ax.bar(weekly.index,weekly['sum'],width=5)
ax.set(title='Weeks ending Sunday',xlabel='Week ending date',ylabel='KRW')
fig.tight_layout();fig.savefig(ROOT/'figures/20_weekly_boundaries.png',dpi=145);plt.close(fig)
