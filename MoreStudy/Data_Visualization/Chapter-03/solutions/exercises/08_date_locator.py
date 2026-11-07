from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
dates=pd.date_range('2026-10-01',periods=30,freq='D');values=[20+(i%6)*2 for i in range(30)]
fig,ax=plt.subplots(figsize=(8.5,4),layout='constrained')
ax.plot(dates,values)
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax.set(title='Daily Measurements',xlabel='Date',ylabel='Value')
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_08.png',dpi=145)
plt.close(fig)
