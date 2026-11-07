from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

values=pd.Series([1.5,1.9,2.1,2.3,2.0,2.2,19.0])
mean_all=values.mean();mean_without=values[values<10].mean()
print('Mean all:',round(mean_all,2),'Without flagged value:',round(mean_without,2))
fig,ax=plt.subplots(figsize=(6,3.5))
ax.bar(['All records','Flagged excluded'],[mean_all,mean_without],color=['#B68C68','#6C9EA2'])
ax.set(ylabel='Average days',title='Sensitivity to one extreme observation')
fig.tight_layout();fig.savefig(ROOT/'figures/06_outlier_sensitivity.png',dpi=145);plt.close(fig)
