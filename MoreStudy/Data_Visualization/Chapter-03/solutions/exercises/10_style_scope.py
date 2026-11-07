from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
x=[1,2,3,4];y=[15,20,17,26]
fig,ax=plt.subplots(figsize=(7,4),layout='constrained')
ax.plot(x,y,marker='o')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y',alpha=.25)
ax.set(title='Weekly Change',xlabel='Week',ylabel='Count')
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_10.png',dpi=145)
plt.close(fig)
