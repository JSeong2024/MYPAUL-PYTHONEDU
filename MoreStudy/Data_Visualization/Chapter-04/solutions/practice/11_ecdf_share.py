"""Coding Practice: 경험 누적분포(ECDF) 만들기.

이 파일은 완성된 참조 구현입니다.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", palette="colorblind")

df=pd.read_csv(DATA/"service_requests.csv")
fig,axes=plt.subplots(1,2,figsize=(11,4),layout="constrained")
sns.kdeplot(data=df,x="response_ms",hue="priority",common_norm=False,cut=0,ax=axes[0])
sns.ecdfplot(data=df,x="response_ms",hue="priority",ax=axes[1])
axes[0].set(title="Smoothed KDE (not exact counts)")
axes[1].set(title="Empirical cumulative share",ylabel="Cumulative proportion")
fig.savefig(OUT/"11_kde_ecdf.png",dpi=145)
plt.close(fig)
