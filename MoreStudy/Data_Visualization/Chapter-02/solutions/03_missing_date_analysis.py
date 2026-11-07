"""Exercise 03 solution: distinguish missing record from recorded zero."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def solve(output: Path | None = None) -> pd.DataFrame:
    df=pd.read_csv(ROOT/"data"/"library_visits.csv",parse_dates=["date"])
    dates=pd.date_range("2026-10-01","2026-10-14")
    grid=pd.MultiIndex.from_product([dates,sorted(df["branch"].unique())],names=["date","branch"])
    completed=df.set_index(["date","branch"])[["visitors"]].reindex(grid)
    missing=completed[completed["visitors"].isna()].reset_index()
    east=completed.xs("Eastgate",level="branch")
    fig,ax=plt.subplots(figsize=(8,4))
    ax.plot(east.index,east["visitors"],marker="o")
    ax.set(title="Eastgate - Missing Date Preserved",ylabel="Visitors / day")
    ax.tick_params(axis="x",rotation=30);fig.tight_layout()
    path=output or ROOT/"output"/"exercise_03.png"
    path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,dpi=150);plt.close(fig)
    return missing

if __name__=="__main__":print(solve().to_string(index=False))
