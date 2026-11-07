from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)
import sys
sys.path.insert(0, str(ROOT))
from project.chart_design import load_visits, branch_summary

summary = branch_summary(load_visits(ROOT / "data" / "library_visits.csv"))
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4))
axes[0].bar(summary["branch"], summary["new_members"])
axes[0].set(title="New Members (Count)", ylabel="People")
axes[1].bar(summary["branch"], summary["signup_rate_pct"])
axes[1].set(title="New Members / Visitors (Rate)", ylabel="Percent (%)")
for ax in axes: ax.tick_params(axis="x", rotation=20)
fig.tight_layout()
fig.savefig(OUTPUT / "06_counts_vs_rates.png", dpi=150)
plt.close(fig)
print(summary[["branch", "new_members", "signup_rate_pct"]].round(2).to_string(index=False))
