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
rate=pd.pivot_table(df,index='line',columns='shift',values='is_defective',aggfunc='mean')
count=pd.pivot_table(df,index='line',columns='shift',values='is_defective',aggfunc='size')
fig,axes=plt.subplots(1,2,figsize=(10,5),layout='constrained')
sns.heatmap(count,annot=True,fmt='.0f',cmap='Blues',ax=axes[0]);axes[0].set_title('Inspection count')
sns.heatmap(rate,annot=True,fmt='.1%',vmin=0,vmax=.3,cmap='YlOrBr',ax=axes[1]);axes[1].set_title('Defect share')
fig.savefig(ROOT/'figures/17_crosstab.png',dpi=145);plt.close(fig)
print('Counts:', count.to_dict())
