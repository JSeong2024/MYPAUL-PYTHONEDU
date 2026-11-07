from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
months=['Jan','Feb','Mar','Apr'];means=[12,15,14,18];error=[1.1,1.8,1.4,1.2]
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
# TODO: 각 평균에 error 범위를 수직 오류 막대로 표현하세요.
# TODO: 현재 출력 PNG 외에 practice_14.svg도 저장하세요.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_14.png',dpi=145)
plt.close(fig)
