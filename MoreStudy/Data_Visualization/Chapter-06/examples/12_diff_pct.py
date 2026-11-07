import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=pd.Series([100,115,120,0,90],index=['W1','W2','W3','W4','W5'],dtype=float)
delta=s.diff();rate=s.pct_change(fill_method=None)*100
rate=rate.replace([np.inf,-np.inf],np.nan)
print('W2 delta:',int(delta.iloc[1]),'W5 rate available:',bool(pd.notna(rate.iloc[-1])))
fig,axes=plt.subplots(1,2,figsize=(9,3.5),layout='constrained')
axes[0].bar(delta.index,delta.values);axes[0].set(title='Absolute change',ylabel='Change (units)')
axes[1].bar(rate.index,rate.values);axes[1].set(title='Relative change',ylabel='Change (%)')
fig.savefig(ROOT/'figures/12_diff_pct.png',dpi=145);plt.close(fig)
