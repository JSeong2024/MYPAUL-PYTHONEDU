"""Coding Practice: 관측점 겹침을 줄이는 stripplot.

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

df = pd.read_csv(DATA / "service_requests.csv")
sample = df.sample(110,random_state=12)
fig,axes=plt.subplots(1,2,figsize=(11,4),layout="constrained")
sns.violinplot(data=df,x="service",y="response_ms",inner="quart",cut=0,color="lightblue",ax=axes[0])
# TODO: 관측점 겹침을 줄이는 stripplot
raise NotImplementedError("TODO: 09_strip_jitter")
axes[0].set(title="Violin: smoothed distribution")
axes[1].set(title="Strip: 110 observed points")
fig.savefig(OUT/"09_violin_and_strip.png",dpi=145)
plt.close(fig)
