from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df=pd.read_csv(ROOT/'data/support_tickets.csv').dropna(subset=['first_response_min'])
fig,axes=plt.subplots(1,3,figsize=(12,3.7),sharey=True,layout='constrained')
for ax,priority in zip(axes,['High','Normal','Low']):
    part=df.loc[df.priority.eq(priority)]
    sns.scatterplot(data=part,x='first_response_min',y='customer_rating',alpha=.5,ax=ax,color='#4B84A6')
    ax.set(xlim=(0,250),title=f'{priority} (n={len(part)})',xlabel='Response min')
axes[0].set_ylabel('Rating');fig.savefig(ROOT/'figures/19_scatter_facets.png',dpi=145);plt.close(fig)
