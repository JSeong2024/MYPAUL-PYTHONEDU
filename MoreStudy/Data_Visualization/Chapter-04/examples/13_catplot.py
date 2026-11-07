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
g=sns.catplot(data=df,x="service",y="response_ms",col="priority",kind="box",height=3.2,aspect=1.35,color="lightblue")
g.set_axis_labels("Service","Response (ms)")
g.figure.savefig(OUT/"13_catplot.png",dpi=145,bbox_inches="tight")
plt.close(g.figure)
