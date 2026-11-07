"""Exercise 05 solution: one scale and explicit gaps across all branches."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
BRANCHES=("Central","Riverside","Hilltop","Eastgate")

def solve(output: Path | None = None) -> dict[str,int]:
    df=pd.read_csv(ROOT/"data"/"library_visits.csv",parse_dates=["date"])
    dates=pd.date_range("2026-10-01","2026-10-14")
    fig,axes=plt.subplots(2,2,figsize=(10,6),sharex=True,sharey=True)
    counts={}
    for ax,branch in zip(axes.flat,BRANCHES):
        series=df.loc[df.branch.eq(branch),["date","visitors"]].set_index("date").reindex(dates)["visitors"]
        counts[branch]=int(series.notna().sum())
        ax.plot(dates,series,marker="o",markersize=3)
        ax.set(title=branch,ylim=(0,310));ax.grid(alpha=.2)
        ax.tick_params(axis="x",rotation=30)
    fig.suptitle("Visits by Branch - Common Scale")
    fig.tight_layout()
    path=output or ROOT/"output"/"exercise_05.png"
    path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,dpi=150);plt.close(fig)
    return counts

if __name__=="__main__":print(solve())
