"""Exercise 01 solution: zero-based ranked bar chart."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def solve(output: Path | None = None) -> pd.Series:
    df=pd.read_csv(ROOT/"data"/"library_visits.csv")
    totals=df.groupby("branch")["visitors"].sum().sort_values(ascending=False)
    fig,ax=plt.subplots(figsize=(8,4))
    bars=ax.barh(totals.index, totals.values)
    ax.invert_yaxis();ax.set_xlim(0,totals.max()*1.22)
    ax.bar_label(bars,padding=3)
    ax.set(xlabel="Visitors (people)",title="Observed Visits by Branch")
    fig.tight_layout()
    path=output or ROOT/"output"/"exercise_01.png"
    path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,dpi=150);plt.close(fig)
    return totals

if __name__=="__main__":print(solve().to_string())
