import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
s=df.query('store_id == "ST-B"').set_index('date')['revenue_krw'].sort_index()
s=s.reindex(pd.date_range(s.index.min(),s.index.max(),freq='D'))
mean7=s.rolling(7,min_periods=7).mean()
print('Rolling valid:',int(mean7.notna().sum()),'Missing daily:',int(s.isna().sum()))
fig,ax=plt.subplots(figsize=(9,3.4))
ax.plot(s.index,s.values,alpha=.35,label='Daily')
ax.plot(mean7.index,mean7.values,lw=2,label='7-day mean (complete window)')
ax.set(title='Rolling seven-day average',ylabel='KRW');ax.legend()
fig.tight_layout();fig.savefig(ROOT/'figures/09_rolling_count.png',dpi=145);plt.close(fig)
