from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df=pd.read_csv(ROOT/'data/inspections.csv').drop_duplicates('inspection_id')
columns=['thickness_mm','temperature_c','is_defective']
corr=df[columns].corr(numeric_only=True)
fig,ax=plt.subplots(figsize=(6.4,4.6));sns.heatmap(corr,annot=True,fmt='.2f',vmin=-1,vmax=1,center=0,cmap='vlag',ax=ax)
ax.set(title='Inspection data correlation matrix')
fig.tight_layout();fig.savefig(ROOT/'figures/12_correlation_heatmap.png',dpi=145);plt.close(fig)
print(corr.round(2).to_string())
