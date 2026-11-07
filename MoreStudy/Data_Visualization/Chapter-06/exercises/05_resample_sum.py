"""Monthly Revenue: 일별 매출을 월 시작 시각 기준으로 합산합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
a=df.query('store_id == "ST-A"').set_index('date')['revenue_krw'].sort_index()
# TODO: 일별 매출을 월 시작 시각 기준으로 합산합니다.
raise NotImplementedError('Complete the marked line before continuing')
print('Months:',len(monthly),'Totals agree:',int(monthly.sum())==int(a.sum()))
fig,ax=plt.subplots(figsize=(7,3.5))
ax.bar(monthly.index.strftime('%Y-%m'),monthly.values)
ax.set(title='Monthly store revenue',ylabel='Revenue (KRW)',xlabel='Month')
fig.tight_layout();fig.savefig(ROOT/'figures/06_resample_sum.png',dpi=145);plt.close(fig)
