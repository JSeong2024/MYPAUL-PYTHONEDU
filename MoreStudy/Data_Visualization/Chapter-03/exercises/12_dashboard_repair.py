from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(2,2,figsize=(9,6),layout='constrained')
axes[0,0].plot([1,2,3],[4,6,5]);axes[0,0].set_title('Daily')
axes[0,1].bar(['A','B'],[5,7]);axes[0,1].set_title('Category')
# TODO: 오른쪽 아래가 아니라 왼쪽 아래 axes[1,0]에 분포 그래프를 추가하세요.
# TODO: 오른쪽 아래 axes[1,1]에는 누적 데이터 선 그래프를 그리세요.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_12.png',dpi=145)
plt.close(fig)
