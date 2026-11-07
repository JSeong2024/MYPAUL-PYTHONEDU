from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

df=pd.read_csv(ROOT/'data/shipments.csv')
x=df.loc[df['status'].eq('delivered'),'actual_days'].dropna()
q1,q3=x.quantile([.25,.75]); iqr=q3-q1
upper=q3+1.5*iqr;lower=q1-1.5*iqr
suspect=x[(x<lower)|(x>upper)]
print('IQR:',round(iqr,2),'bounds:',round(lower,2),round(upper,2),'candidates:',len(suspect))
fig,ax=plt.subplots(figsize=(7,3.3));sns.boxplot(x=x,ax=ax,color='#7AAFC5')
ax.set(title='Delivery duration and outlier candidates',xlabel='Actual days')
fig.tight_layout();fig.savefig(ROOT/'figures/05_outlier_iqr.png',dpi=145);plt.close(fig)
