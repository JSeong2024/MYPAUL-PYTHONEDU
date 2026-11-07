from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

raw=pd.read_csv(ROOT/'data/shipments.csv')
valid=raw.loc[raw.status.eq('delivered') & raw.actual_days.notna()].copy()
counts=valid.groupby('zone').size()
print('Group n:',counts.to_dict())
fig,ax=plt.subplots(figsize=(7,4))
sns.boxplot(data=valid,x='zone',y='actual_days',order=['Urban','Suburban','Remote'],ax=ax)
ax.set(title='Delivery duration by zone',ylabel='Days')
for i,z in enumerate(['Urban','Suburban','Remote']):ax.text(i,ax.get_ylim()[1]*.92,f'n={counts[z]}',ha='center',fontsize=9)
fig.tight_layout();fig.savefig(ROOT/'figures/07_group_comparison.png',dpi=145);plt.close(fig)
