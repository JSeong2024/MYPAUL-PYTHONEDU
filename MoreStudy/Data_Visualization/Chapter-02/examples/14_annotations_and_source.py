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
fig, ax = plt.subplots(figsize=(8.5, 4.2))
bars = ax.barh(summary["branch"], summary["visitors"])
ax.invert_yaxis()
ax.set(xlim=(0, summary["visitors"].max()*1.2),
       xlabel="Visitors (people)", title="Total Visits by Branch")
ax.bar_label(bars, padding=3)
ax.text(0, -0.23, "Source: Synthetic library visits, 2026-10-01 to 2026-10-14",
        transform=ax.transAxes, fontsize=8)
ax.text(0, -0.32, "Note: Eastgate has one missing date; totals are observed only.",
        transform=ax.transAxes, fontsize=8)
fig.subplots_adjust(bottom=.34)
fig.savefig(OUTPUT / "14_annotations_and_source.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Annotated chart saved")
