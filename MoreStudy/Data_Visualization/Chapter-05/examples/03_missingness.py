from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df = pd.read_csv(ROOT/'data/support_tickets.csv')
rate = df.groupby('team')['first_response_min'].apply(lambda s:s.isna().mean()).sort_values()
print('Missing fraction:',rate.round(3).to_dict())
fig,ax=plt.subplots(figsize=(7,3.5))
ax.barh(rate.index,rate,color='#9A80B3')
ax.set(xlim=(0,.15),xlabel='Missing share',title='First-response data missingness')
fig.tight_layout();fig.savefig(ROOT/'figures/03_missingness.png',dpi=145);plt.close(fig)
