"""Daily Coverage: 하루의 유효 관측 수를 계산합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/weather_hourly.csv',parse_dates=['timestamp_local'])
s=df.query('station_id == "W-A"').set_index('timestamp_local')['temperature_c'].sort_index()
# TODO: 하루의 유효 관측 수를 계산합니다.
raise NotImplementedError('Complete the marked line before continuing')
print('Incomplete days:',int((daily['count']<24).sum()))
fig,ax=plt.subplots(figsize=(9,3.5))
ax.bar(daily.index,daily['count'],width=.8)
ax.axhline(24,ls='--',color='#b34743',label='Expected hourly samples')
ax.set(title='Daily measurement coverage',ylabel='Available records',ylim=(0,26));ax.legend()
fig.tight_layout();fig.savefig(ROOT/'figures/08_group_coverage.png',dpi=145);plt.close(fig)
