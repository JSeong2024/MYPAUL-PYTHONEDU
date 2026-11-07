"""Shared Y Axes: 관측소별 서브플롯의 날짜축과 기온축을 공유하도록 설정합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/weather_hourly.csv',parse_dates=['timestamp_local'])
daily=df.groupby([df['timestamp_local'].dt.floor('D'),'station_id'])['temperature_c'].mean().unstack()
# TODO: 관측소별 서브플롯의 날짜축과 기온축을 공유하도록 설정합니다.
raise NotImplementedError('Complete the marked line before continuing')
for ax,station in zip(axes,sorted(daily.columns)):
    ax.plot(daily.index,daily[station],marker='o');ax.set(title=station,ylabel='Mean °C')
axes[-1].set_xlabel('Day')
fig.savefig(ROOT/'figures/16_shared_axis.png',dpi=145);plt.close(fig)
print('Stations:',len(daily.columns),'Shared y:',bool(axes[0].get_shared_y_axes().joined(axes[0],axes[1])))
