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
fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
valid_thickness = df.loc[df.thickness_mm.between(8, 12), 'thickness_mm']
sns.histplot(valid_thickness,bins=20,ax=axes[0,0],color='#6599BB')
axes[0,0].set(xlim=(8,12),title='Thickness distribution (valid 8–12 mm)')
sns.barplot(data=df,x='plant',y='is_defective',errorbar=None,ax=axes[0,1],color='#79A99D')
axes[0,1].set(ylim=(0,.25),title='Observed defect share')
sns.boxplot(data=df,x='shift',y='temperature_c',ax=axes[1,0],color='#B19ABE')
axes[1,0].set(title='Temperature by shift')
missing=df.isna().sum().sort_values(ascending=False)
axes[1,1].barh(missing.index,missing.values,color='#C58F65')
axes[1,1].set(title='Missing values per field',xlabel='Records')
fig.suptitle('Inspection EDA — summary with stated limitations')
fig.savefig(ROOT/'figures/20_eda_report.png',dpi=145);plt.close(fig)
print('Unique inspections:',len(df),'Defect rate:',round(df.is_defective.mean(),3))
