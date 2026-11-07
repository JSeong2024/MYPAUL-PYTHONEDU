import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
s=df.query('store_id == "ST-A"').sort_values('date')
fig,ax=plt.subplots(figsize=(9,3.5))
ax.plot(s['date'],s['revenue_krw'],lw=1.3)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.set(title='Monthly date ticks',xlabel='Date',ylabel='Revenue (KRW)')
ax.grid(alpha=.25)
fig.tight_layout();fig.savefig(ROOT/'figures/03_date_axis.png',dpi=145);plt.close(fig)
print('Observations:',len(s),'First:',s['date'].min().date())
