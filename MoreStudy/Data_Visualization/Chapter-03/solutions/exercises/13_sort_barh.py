from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
stores={'North':70,'South':35,'East':52,'West':86}
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
items=sorted(stores.items(),key=lambda item:item[1])
ax.barh([k for k,v in items],[v for k,v in items])
ax.set(title='Orders by Store',xlabel='Orders')
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_13.png',dpi=145)
plt.close(fig)
