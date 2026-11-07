"""Coding Practice: 히스토그램 구간 수를 35로 지정.

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
sns.histplot(data=df,x="response_ms",bins=10,color="steelblue",ax=axes[0])
sns.histplot(data=df,x="response_ms",bins=35,color="steelblue",ax=axes[1])
axes[0].set(title="10 bins",xlabel="Response (ms)")
axes[1].set(title="35 bins",xlabel="Response (ms)")
fig.savefig(OUT/"10_histplot_bins.png",dpi=145)
plt.close(fig)
