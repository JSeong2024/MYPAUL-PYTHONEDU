import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/server_metrics.csv')
df['time']=pd.to_datetime(df['timestamp_utc'],utc=True)
fig,ax=plt.subplots(figsize=(10,3.5))
ax.plot(df['time'],df['latency_ms'],lw=1)
start=pd.Timestamp('2026-10-27 02:15',tz='UTC');end=pd.Timestamp('2026-10-27 03:30',tz='UTC')
ax.axvspan(start,end,color='#f0ae4f',alpha=.28,label='Review window')
ax.set(title='Latency and marked review window',ylabel='Latency (ms)',xlabel='Time (UTC)');ax.legend()
fig.tight_layout();fig.savefig(ROOT/'figures/17_event_window.png',dpi=145);plt.close(fig)
print('Window length (minutes):',int((end-start).total_seconds()/60))
