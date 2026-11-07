import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
s=df.query('store_id == "ST-B"').set_index('date')['revenue_krw'].sort_index().reindex(pd.date_range('2026-08-01','2026-10-31',freq='D'))
cumulative=s.cumsum()
print('Observed total:',int(s.sum()),'Missing days:',int(s.isna().sum()))
fig,ax=plt.subplots(figsize=(9,3.4))
ax.plot(cumulative.index,cumulative.values)
ax.set(title='Cumulative observed revenue',ylabel='Observed KRW',xlabel='Date')
fig.tight_layout();fig.savefig(ROOT/'figures/21_cumsum.png',dpi=145);plt.close(fig)
