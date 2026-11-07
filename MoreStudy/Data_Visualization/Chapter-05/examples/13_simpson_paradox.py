from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df=pd.read_csv(ROOT/'data/simpson_delivery.csv')
pooled=df.groupby('carrier').on_time.mean()
within=df.groupby(['zone','carrier']).on_time.mean().unstack()
fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
pooled.plot.bar(ax=axes[0],color='#6F99B6',rot=0)
axes[0].set(ylim=(0,1),ylabel='On-time share',title='Overall comparison')
within.plot.bar(ax=axes[1],rot=0,color=['#6F99B6','#C78D74'])
axes[1].set(ylim=(0,1),ylabel='On-time share',title='Within each zone')
fig.savefig(ROOT/'figures/13_simpson_paradox.png',dpi=145);plt.close(fig)
print('Overall:',pooled.round(3).to_dict())
print('By zone: ',within.round(3).to_dict())
