from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
labels=['Food','Drink','Stationery']
a=np.array([22,31,19]);b=np.array([27,26,25]);x=np.arange(len(labels))
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
width=.35
ax.bar(x-width/2,a,width,label='Store A')
ax.bar(x+width/2,b,width,label='Store B')
ax.set_xticks(x,labels)
ax.set(title='Orders by Store',ylabel='Orders')
ax.legend()
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_05.png',dpi=145)
plt.close(fig)
