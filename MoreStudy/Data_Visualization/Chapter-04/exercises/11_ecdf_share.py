"""Coding Practice: 경험 누적분포(ECDF) 만들기.

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

df=pd.read_csv(DATA/"service_requests.csv")
fig,axes=plt.subplots(1,2,figsize=(11,4),layout="constrained")
sns.kdeplot(data=df,x="response_ms",hue="priority",common_norm=False,cut=0,ax=axes[0])
# TODO: 경험 누적분포(ECDF) 만들기
raise NotImplementedError("TODO: 11_ecdf_share")
axes[0].set(title="Smoothed KDE (not exact counts)")
axes[1].set(title="Empirical cumulative share",ylabel="Cumulative proportion")
fig.savefig(OUT/"11_kde_ecdf.png",dpi=145)
plt.close(fig)
