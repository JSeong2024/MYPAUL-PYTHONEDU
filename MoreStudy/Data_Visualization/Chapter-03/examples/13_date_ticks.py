from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
dates=pd.date_range('2026-10-01',periods=35,freq='D')
values=[100+(i%7)*4+i*.6 for i in range(len(dates))]
fig,ax=plt.subplots(figsize=(9,4),layout='constrained')
ax.plot(dates,values,marker='.',markersize=4)
locator=mdates.WeekdayLocator(byweekday=mdates.MO)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax.set(title='Daily Sensor Readings',xlabel='Date (MM-DD)',ylabel='Reading')
ax.grid(alpha=.2)
fig.savefig(ROOT/'figures'/'14_date_ticks.png',dpi=145)
plt.close(fig)
