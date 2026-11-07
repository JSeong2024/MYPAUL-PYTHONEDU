import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
times=pd.to_datetime(['2026-10-01 09:00','2026-10-01 09:05','2026-10-01 09:10','2026-10-01 10:15','2026-10-01 10:20'])
values=[20,22,24,28,27]
fig,axes=plt.subplots(1,2,figsize=(10,3.2),layout='constrained')
axes[0].plot(range(len(values)),values,marker='o');axes[0].set(title='Incorrect: row index',xlabel='Observation number')
axes[1].plot(times,values,marker='o');axes[1].set(title='Correct: elapsed time',xlabel='Actual timestamp')
axes[1].tick_params(axis='x',rotation=35)
fig.savefig(ROOT/'figures/23_irregular_ticks.png',dpi=145);plt.close(fig)
print('Largest interval (minutes):',int(times.to_series().diff().max().total_seconds()/60))
