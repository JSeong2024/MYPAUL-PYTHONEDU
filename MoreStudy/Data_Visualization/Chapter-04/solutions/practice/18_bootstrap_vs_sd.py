"""Coding Practice: 표준편차 범위 표시하기.

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
sns.barplot(data=df,x="service",y="response_ms",estimator="mean",errorbar=("ci",95),seed=7,ax=axes[0],color="steelblue")
sns.barplot(data=df,x="service",y="response_ms",estimator="mean",errorbar="sd",ax=axes[1],color="steelblue")
axes[0].set(title="95% bootstrap CI for mean",ylabel="Response (ms)")
axes[1].set(title="Standard deviation around mean",ylabel="Response (ms)")
fig.savefig(OUT/"22_errorbar_intervals.png",dpi=145)
plt.close(fig)
