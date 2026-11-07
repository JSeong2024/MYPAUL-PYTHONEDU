import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/weather_hourly.csv',parse_dates=['timestamp_local'])
s=df.query('station_id == "W-A"').set_index('timestamp_local').sort_index()
summary=s.resample('D').agg(temp_mean=('temperature_c','mean'),rain_sum=('precipitation_mm','sum'))
print('Days:',len(summary),'First day mean temp:',round(summary.iloc[0]['temp_mean'],2))
fig,axes=plt.subplots(2,1,figsize=(9,5.5),sharex=True,layout='constrained')
axes[0].plot(summary.index,summary['temp_mean'],marker='o');axes[0].set(ylabel='Mean °C',title='Temperature: mean')
axes[1].bar(summary.index,summary['rain_sum']);axes[1].set(ylabel='Total mm',title='Hourly precipitation: sum',xlabel='Day')
fig.savefig(ROOT/'figures/07_mean_vs_sum.png',dpi=145);plt.close(fig)
