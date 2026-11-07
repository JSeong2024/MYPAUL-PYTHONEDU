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
table=pd.crosstab(df.carrier,df.zone,normalize='index')
fig,ax=plt.subplots(figsize=(6.7,4))
table[['Urban','Remote']].plot.bar(stacked=True,ax=ax,color=['#77ADCC','#C7A077'],rot=0)
ax.set(title='Order mix by carrier',ylabel='Share of orders',ylim=(0,1))
fig.tight_layout();fig.savefig(ROOT/'figures/14_composition_counts.png',dpi=145);plt.close(fig)
print(table.round(3).to_string())
