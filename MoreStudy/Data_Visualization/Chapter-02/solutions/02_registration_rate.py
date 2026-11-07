"""Exercise 02 solution: aggregate numerator and denominator before division."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def solve(output: Path | None = None) -> pd.Series:
    df=pd.read_csv(ROOT/"data"/"library_visits.csv")
    totals=df.groupby("branch")[["new_members","visitors"]].sum()
    rate=100*totals["new_members"].div(totals["visitors"].where(totals["visitors"]>0))
    rate=rate.sort_values(ascending=False)
    fig,ax=plt.subplots(figsize=(8,4))
    bars=ax.barh(rate.index,rate.values)
    ax.invert_yaxis();ax.set_xlim(0,max(25,float(rate.max())*1.3))
    ax.bar_label(bars,fmt="%.1f%%",padding=3)
    ax.set(title="Registrations per Visitor",xlabel="Rate (%)")
    fig.tight_layout()
    path=output or ROOT/"output"/"exercise_02.png"
    path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,dpi=150);plt.close(fig)
    return rate

if __name__=="__main__":print(solve().round(2).to_string())
