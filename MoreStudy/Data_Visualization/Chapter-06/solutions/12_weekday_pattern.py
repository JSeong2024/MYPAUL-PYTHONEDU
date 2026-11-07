import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
df['weekday']=df['date'].dt.dayofweek
mean=df.groupby('weekday')['revenue_krw'].mean().reindex(range(7))
print('Weekend average higher:',bool(mean.iloc[5:].mean()>mean.iloc[:5].mean()))
fig,ax=plt.subplots(figsize=(8,3.4))
ax.bar(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],mean.values)
ax.set(title='Average daily revenue by weekday',ylabel='KRW / observed store-day')
fig.tight_layout();fig.savefig(ROOT/'figures/13_weekday_pattern.png',dpi=145);plt.close(fig)
