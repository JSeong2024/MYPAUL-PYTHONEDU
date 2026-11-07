from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

raw=pd.read_csv(ROOT/'data/support_tickets.csv')
x=raw.first_response_min.dropna()
fig,ax=plt.subplots(figsize=(7,4))
sns.ecdfplot(x=x,ax=ax,color='#397BA8',lw=2)
ax.axvline(60,color='#C45F54',ls='--',label='60 min benchmark')
ax.set(xlim=(0,250),ylim=(0,1.02),xlabel='First response (minutes)',ylabel='Share at or below x',title='Cumulative response distribution')
ax.legend();fig.tight_layout();fig.savefig(ROOT/'figures/08_ecdf_threshold.png',dpi=145);plt.close(fig)
print('<= 60 minutes:',round((x<=60).mean(),3))
