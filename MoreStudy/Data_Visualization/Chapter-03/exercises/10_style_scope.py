from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
x=[1,2,3,4];y=[15,20,17,26]
fig,ax=plt.subplots(figsize=(7,4),layout='constrained')
ax.plot(x,y,marker='o')
# TODO: 이번 Axes의 top/right spine을 숨기고 y축 격자만 표시하세요.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_10.png',dpi=145)
plt.close(fig)
