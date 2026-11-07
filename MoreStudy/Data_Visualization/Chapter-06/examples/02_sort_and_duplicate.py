import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
frame=pd.DataFrame({'time':pd.to_datetime(['2026-10-01 10:00','2026-10-01 09:00','2026-10-01 10:00','2026-10-01 11:00']), 'value':[12,10,13,15]})
frame=frame.sort_values('time')
print('Duplicate time rows:',int(frame.duplicated('time',keep=False).sum()))
fig,ax=plt.subplots(figsize=(7,3))
ax.scatter(frame['time'],frame['value'],s=80)
ax.set(title='Two readings at the same timestamp',ylabel='Sensor value')
fig.autofmt_xdate();fig.tight_layout();fig.savefig(ROOT/'figures/02_sort_and_duplicate.png',dpi=145);plt.close(fig)
