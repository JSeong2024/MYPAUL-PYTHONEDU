from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(2,2,figsize=(9,6),layout='constrained')
axes[0,0].plot([1,2,3],[4,6,5]);axes[0,0].set_title('Daily')
axes[0,1].bar(['A','B'],[5,7]);axes[0,1].set_title('Category')
axes[1,0].hist([2,3,3,4,5,6,6],bins=4)
axes[1,0].set(title='Distribution',xlabel='Value')
axes[1,1].plot([1,2,3],[4,10,15],marker='o')
axes[1,1].set(title='Cumulative',xlabel='Day')
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_12.png',dpi=145)
plt.close(fig)
