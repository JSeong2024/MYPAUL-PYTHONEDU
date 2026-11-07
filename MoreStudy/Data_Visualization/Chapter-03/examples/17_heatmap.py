from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
values=np.array([[44,61,70,85],[35,49,65,76],[18,30,48,53]],dtype=float)
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
image=ax.imshow(values,aspect='auto',cmap='viridis',interpolation='nearest')
ax.set_xticks(range(4),['09:00','12:00','15:00','18:00'])
ax.set_yticks(range(3),['Terminal A','Terminal B','Terminal C'])
ax.set(title='Hourly Transactions',xlabel='Hour',ylabel='Location')
fig.colorbar(image,ax=ax,label='Transactions')
fig.savefig(ROOT/'figures'/'18_heatmap.png',dpi=145)
plt.close(fig)
