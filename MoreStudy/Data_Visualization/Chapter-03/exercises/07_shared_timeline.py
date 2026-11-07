from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
hours=[8,9,10,11,12];temperature=[21,22,23,25,24];humidity=[47,45,48,51,49]
fig,axes=plt.subplots(2,1,sharex=True,figsize=(8,5),layout='constrained')
# TODO: 위에는 기온, 아래에는 습도 그래프를 그리고 x축 눈금을 공유하세요.
# TODO: 각각의 y축 단위를 표시하세요.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_07.png',dpi=145)
plt.close(fig)
