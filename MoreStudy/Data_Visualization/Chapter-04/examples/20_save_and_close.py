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
fig,ax=plt.subplots(figsize=(7,4),layout="constrained")
sns.histplot(data=df,x="response_ms",bins=22,color="steelblue",ax=ax)
ax.set(title="Saved Seaborn figure",xlabel="Response (ms)")
fig.savefig(OUT/"20_save_and_close.png",dpi=145,bbox_inches="tight")
fig.savefig(OUT/"20_save_and_close.svg",bbox_inches="tight")
plt.close(fig)
print("PNG/SVG saved")
