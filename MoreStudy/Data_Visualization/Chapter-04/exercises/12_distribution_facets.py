"""Coding Practice: 우선순위별 분포를 두 개의 Facet에 배치.

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
# TODO: 우선순위별 분포를 두 개의 Facet에 배치
raise NotImplementedError("TODO: 12_distribution_facets")
g.set_axis_labels("Response (ms)","Requests")
g.figure.savefig(OUT/"12_displot.png",dpi=145,bbox_inches="tight")
plt.close(g.figure)
