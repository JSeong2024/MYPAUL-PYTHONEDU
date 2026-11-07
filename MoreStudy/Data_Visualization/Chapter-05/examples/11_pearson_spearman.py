from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

x=np.arange(1,51,dtype=float);y=x**2
frame=pd.DataFrame({'x':x,'y':y})
p=frame.x.corr(frame.y,method='pearson')
s=frame.x.corr(frame.y,method='spearman')
fig,ax=plt.subplots(figsize=(6.5,4));ax.scatter(x,y,s=19,alpha=.7)
ax.set(xlabel='Input',ylabel='Squared response',title=f'Pearson {p:.2f} vs Spearman {s:.2f}')
fig.tight_layout();fig.savefig(ROOT/'figures/11_pearson_spearman.png',dpi=145);plt.close(fig)
print('Pearson:',round(p,3),'Spearman:',round(s,3))
