from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
hours=[9,10,11,12,13,14];orders=[13,16,27,31,25,18]
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
ax.plot(hours,orders,marker='o')
# TODO: 가장 많은 주문이 발생한 (시간, 주문량)을 계산하여 화살표로 표시하세요.
# TODO: 축 제목과 그래프 제목을 지정하세요.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_06.png',dpi=145)
plt.close(fig)
