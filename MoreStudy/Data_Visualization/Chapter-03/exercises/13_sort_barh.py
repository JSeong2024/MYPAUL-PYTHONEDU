from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
stores={'North':70,'South':35,'East':52,'West':86}
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
# TODO: 값으로 정렬하고, y축이 오름차순인 가로 막대그래프로 구현하세요.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_13.png',dpi=145)
plt.close(fig)
