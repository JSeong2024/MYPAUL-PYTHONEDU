"""Coding Practice: 세 변수의 Pairplot과 지점별 색상 표시.

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
# TODO: 세 변수의 Pairplot과 지점별 색상 표시
raise NotImplementedError("TODO: 14_pairplot_fields")
g.figure.savefig(OUT/"15_pairplot.png",dpi=145,bbox_inches="tight")
plt.close(g.figure)
