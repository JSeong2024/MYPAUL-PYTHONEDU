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
x=df.loc[df.priority.eq('High'),'first_response_min'].dropna().to_numpy()
rng=np.random.default_rng(25)
boot=rng.choice(x,size=(1500,len(x)),replace=True).mean(axis=1)
lo,hi=np.quantile(boot,[.025,.975])
fig,ax=plt.subplots(figsize=(7,4));sns.histplot(boot,bins=25,ax=ax,color='#7F9CC5')
ax.axvline(lo,ls='--',color='#A25E46');ax.axvline(hi,ls='--',color='#A25E46')
ax.set(title='Bootstrap distribution of mean response',xlabel='Resampled mean (min)')
fig.tight_layout();fig.savefig(ROOT/'figures/16_bootstrap_mean.png',dpi=145);plt.close(fig)
print('Mean:',round(x.mean(),2),'percentile interval:',round(lo,2),round(hi,2))
