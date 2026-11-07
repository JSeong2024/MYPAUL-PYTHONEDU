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
g=sns.jointplot(data=df,x="visitors",y="new_members",kind="scatter",height=6,color="teal")
g.figure.suptitle("Visitors and new members",y=1.02)
g.figure.savefig(OUT/"14_jointplot.png",dpi=145,bbox_inches="tight")
plt.close(g.figure)
