import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
raw=pd.read_csv(ROOT/'data/server_metrics.csv')
raw['utc']=pd.to_datetime(raw['timestamp_utc'],utc=True)
raw['kst']=raw['utc'].dt.tz_convert('Asia/Seoul')
print('UTC first:',raw.iloc[0]['utc'])
print('KST first:',raw.iloc[0]['kst'])
fig,ax=plt.subplots(figsize=(8,3.1))
ax.plot(raw['kst'],raw['cpu_pct'],lw=.8)
ax.set(title='Same measurements, KST date axis',xlabel='Time (Asia/Seoul)',ylabel='CPU (%)')
fig.tight_layout();fig.savefig(ROOT/'figures/19_timezone.png',dpi=145);plt.close(fig)
