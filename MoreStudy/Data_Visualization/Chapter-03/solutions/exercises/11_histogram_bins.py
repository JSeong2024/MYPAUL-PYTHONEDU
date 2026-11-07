from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
minutes=[4,8,11,12,19,24,27,32,37,39,43,48,55]
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
ax.hist(minutes,bins=[0,20,40,60],edgecolor='white')
ax.set(title='Delivery Time Distribution',xlabel='Minutes',ylabel='Deliveries')
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_11.png',dpi=145)
plt.close(fig)
