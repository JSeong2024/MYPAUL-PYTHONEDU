from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
load=[30,45,57,68,80];time=[80,98,110,180,240];temp=[22,24,27,29,31]
fig,ax=plt.subplots(figsize=(7.5,4),layout='constrained')
# TODO: 점 크기 100, color mapping은 temp, cmap='viridis'를 사용하세요.
# TODO: Figure의 colorbar에 'Device temp (°C)'를 표시하세요.
(ROOT/'output').mkdir(exist_ok=True)
fig.savefig(ROOT/'output'/'practice_09.png',dpi=145)
plt.close(fig)
