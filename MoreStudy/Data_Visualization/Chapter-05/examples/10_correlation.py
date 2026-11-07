from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df=pd.read_csv(ROOT/'data/support_tickets.csv').dropna(subset=['first_response_min','customer_rating'])
pearson=df['first_response_min'].corr(df['customer_rating'])
fig,ax=plt.subplots(figsize=(7,4))
sns.scatterplot(data=df,x='first_response_min',y='customer_rating',alpha=.35,ax=ax)
ax.set(xlim=(0,250),xlabel='Response (minutes)',ylabel='Customer rating',title=f'Response and rating (Pearson r={pearson:.2f})')
fig.tight_layout();fig.savefig(ROOT/'figures/10_correlation.png',dpi=145);plt.close(fig)
print('Pearson r:',round(pearson,3),'paired n:',len(df))
