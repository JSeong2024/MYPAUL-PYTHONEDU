from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
labels=['Food','Drink','Stationery','Household']
west=np.array([45,37,26,19]);east=np.array([38,42,31,24])
x=np.arange(len(labels));width=0.36
fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
a=ax.bar(x-width/2,west,width,label='West')
b=ax.bar(x+width/2,east,width,label='East')
ax.bar_label(a,padding=2);ax.bar_label(b,padding=2)
ax.set_xticks(x,labels)
ax.set(title='Sales Units by Category',ylabel='Items sold',ylim=(0,55))
ax.legend()
fig.savefig(ROOT/'figures'/'11_grouped_bars.png',dpi=145)
plt.close(fig)
