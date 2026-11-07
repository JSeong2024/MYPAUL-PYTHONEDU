"""Coding Practice: 상관계수 범위를 -1~1 고정하고 셀 값 표시.

이 파일은 일부 코드가 비어 있습니다. TODO를 완성한 뒤 실행하세요.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", palette="colorblind")

df=pd.read_csv(DATA/"library_visits.csv")
cols=["visitors","new_members","open_hours"]
corr=df[cols].corr(numeric_only=True)
fig,ax=plt.subplots(figsize=(6.5,4.5),layout="constrained")
# TODO: 상관계수 범위를 -1~1 고정하고 셀 값 표시
raise NotImplementedError("TODO: 15_correlation_heatmap")
ax.set(title="Linear correlation (Pearson)")
fig.savefig(OUT/"16_heatmap_corr.png",dpi=145)
plt.close(fig)
