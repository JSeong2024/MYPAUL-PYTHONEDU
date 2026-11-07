from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df=pd.read_csv(ROOT/'data/support_tickets.csv')
all_median=df.first_response_min.median()
resolved_median=df.loc[df.resolved.eq(1),'first_response_min'].median()
fig,ax=plt.subplots(figsize=(7,3.6))
ax.bar(['All recorded','Resolved only'],[all_median,resolved_median],color=['#6A9FC5','#BD9271'])
ax.set(ylabel='Median first response (min)',title='Effect of restricting the analyzed sample')
fig.tight_layout();fig.savefig(ROOT/'figures/18_selection_bias.png',dpi=145);plt.close(fig)
print('All:',round(all_median,1),'Resolved only:',round(resolved_median,1))
