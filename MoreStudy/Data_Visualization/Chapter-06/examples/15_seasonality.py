import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/weather_hourly.csv',parse_dates=['timestamp_local'])
s=df.query('station_id == "W-B"').set_index('timestamp_local')['temperature_c'].sort_index()
s=s.reindex(pd.date_range('2026-10-01','2026-10-14 23:00',freq='h'))
mean=s.groupby(s.index.hour).mean()
print('Daily cycle amplitude:',round(float(mean.max()-mean.min()),2))
fig,axes=plt.subplots(2,1,figsize=(9,5.5),layout='constrained')
axes[0].plot(s.index,s);axes[0].set(title='Hourly weather observations',ylabel='Temperature (°C)')
axes[1].plot(mean.index,mean,marker='o');axes[1].set(title='Mean diurnal profile',ylabel='Temperature (°C)',xlabel='Hour')
fig.savefig(ROOT/'figures/15_seasonality.png',dpi=145);plt.close(fig)
