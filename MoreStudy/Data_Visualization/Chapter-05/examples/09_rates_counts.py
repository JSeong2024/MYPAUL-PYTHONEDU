from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sns.set_theme(style='whitegrid')

raw=pd.read_csv(ROOT/'data/inspections.csv').drop_duplicates('inspection_id')
g=raw.groupby('line',as_index=False).agg(n=('is_defective','size'),defects=('is_defective','sum'))
g['rate']=g.defects/g.n
fig,axes=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
axes[0].bar(g.line,g.defects,color='#4E86B0');axes[0].set(title='Defect count',ylabel='Cases')
axes[1].bar(g.line,g.rate,color='#60A092');axes[1].set(title='Defect share',ylabel='Rate',ylim=(0,.3))
fig.savefig(ROOT/'figures/09_rates_counts.png',dpi=145);plt.close(fig)
print(g[['line','n','defects','rate']].round(3).to_string(index=False))
