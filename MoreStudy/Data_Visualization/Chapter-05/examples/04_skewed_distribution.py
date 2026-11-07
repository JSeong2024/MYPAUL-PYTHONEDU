from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df=pd.read_csv(ROOT/'data/support_tickets.csv')
x=df['first_response_min'].dropna()
fig,ax=plt.subplots(figsize=(7,4))
sns.histplot(x,bins=35,ax=ax,color='#6598BD')
ax.axvline(x.mean(),color='#B44343',ls='--',label=f'Mean: {x.mean():.1f}')
ax.axvline(x.median(),color='#24866E',ls='-',label=f'Median: {x.median():.1f}')
ax.set(xlabel='Minutes',title='Response time with a long right tail')
ax.legend();fig.tight_layout();fig.savefig(ROOT/'figures/04_skewed_distribution.png',dpi=145);plt.close(fig)
print('Mean:',round(x.mean(),1),'Median:',round(x.median(),1))
