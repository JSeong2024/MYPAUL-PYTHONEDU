"""Coding Practice: 우선순위별 분포를 두 개의 Facet에 배치.

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
g=sns.displot(data=df,x="response_ms",col="priority",bins=22,height=3,aspect=1.4,color="steelblue")
g.set_axis_labels("Response (ms)","Requests")
g.figure.savefig(OUT/"12_displot.png",dpi=145,bbox_inches="tight")
plt.close(g.figure)
