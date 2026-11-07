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
g=sns.pairplot(data=df,vars=["visitors","new_members","open_hours"],hue="branch",diag_kind="hist",height=1.9,plot_kws={"alpha":.55,"s":20})
g.figure.savefig(OUT/"15_pairplot.png",dpi=145,bbox_inches="tight")
plt.close(g.figure)
