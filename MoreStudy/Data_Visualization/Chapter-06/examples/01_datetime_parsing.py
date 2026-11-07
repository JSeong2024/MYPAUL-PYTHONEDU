import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
raw = pd.Series(['2026-10-01','2026-10-03','not-a-date','2026-10-02'])
dates = pd.to_datetime(raw,format='%Y-%m-%d',errors='coerce')
print('Valid:', int(dates.notna().sum()), 'Invalid:', int(dates.isna().sum()))
valid = dates.dropna().sort_values().reset_index(drop=True)
fig, ax = plt.subplots(figsize=(7,2.8))
ax.scatter(valid,range(1,len(valid)+1),s=70)
ax.set(title='Parsed chronological dates',ylabel='Order')
fig.autofmt_xdate();fig.tight_layout()
fig.savefig(ROOT/'figures/01_datetime_parsing.png',dpi=145);plt.close(fig)
