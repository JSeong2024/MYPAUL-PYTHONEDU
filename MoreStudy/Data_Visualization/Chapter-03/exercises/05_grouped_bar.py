from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
labels=['Food','Drink','Stationery']
a=np.array([22,31,19]);b=np.array([27,26,25]);x=np.arange(len(labels))
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
# TODO: 각 분류마다 A와 B 막대가 겹치지 않도록 배치하고 범례를 추가하세요.
# TODO: x축 눈금을 분류 이름으로 지정하세요.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_05.png',dpi=145)
plt.close(fig)
