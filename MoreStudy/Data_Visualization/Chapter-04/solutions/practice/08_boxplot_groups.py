"""Coding Practice: 서비스별 응답시간 분포의 중앙값과 사분위 표시.

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

df = pd.read_csv(DATA / "service_requests.csv")
fig, ax = plt.subplots(figsize=(7.5,4.2),layout="constrained")
sns.boxplot(data=df,x="service",y="response_ms",color="lightblue",ax=ax)
ax.set(title="Latency spread by service",ylabel="Response time (ms)")
fig.savefig(OUT/"08_boxplot.png",dpi=145)
plt.close(fig)
