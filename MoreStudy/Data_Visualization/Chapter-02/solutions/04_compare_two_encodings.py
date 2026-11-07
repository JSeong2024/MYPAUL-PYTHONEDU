"""Exercise 04 solution: faithful bar baseline vs zoomed dot plot."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]

def solve(output: Path | None = None) -> tuple[int, int]:
    vals=[80,85]
    fig,axes=plt.subplots(1,2,figsize=(9,3.6))
    axes[0].bar(["A","B"],vals)
    axes[0].set(title="Bar - Zero Baseline",ylim=(0,100),ylabel="Score")
    axes[1].scatter(vals,["A","B"],s=95)
    axes[1].set(title="Dot - Zoomed View",xlim=(76,90),xlabel="Score")
    axes[1].grid(axis="x",alpha=.25)
    fig.tight_layout()
    path=output or ROOT/"output"/"exercise_04.png"
    path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,dpi=150);plt.close(fig)
    return tuple(vals)

if __name__=="__main__":print(solve())
