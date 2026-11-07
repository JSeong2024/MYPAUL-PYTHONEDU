"""Base-100 Index: 매장별 첫날 값으로 나누어 기준 100 지수를 계산합니다."""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
wide=df.pivot(index='date',columns='store_id',values='revenue_krw').sort_index()
base=wide.iloc[0]
assert base.notna().all() and base.gt(0).all()
# TODO: 매장별 첫날 값으로 나누어 기준 100 지수를 계산합니다.
raise NotImplementedError('Complete the marked line before continuing')
print('Base index:',indexed.iloc[0].round().to_dict())
fig,ax=plt.subplots(figsize=(9,3.5))
for c in indexed:ax.plot(indexed.index,indexed[c],lw=1.2,label=c)
ax.axhline(100,color='gray',ls='--',lw=.8)
ax.set(title='Daily revenue indexed to first day = 100',ylabel='Index (base=100)');ax.legend(ncol=3)
fig.tight_layout();fig.savefig(ROOT/'figures/22_normalized_index.png',dpi=145);plt.close(fig)
