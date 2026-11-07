from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
frame = pd.read_csv(ROOT / "data" / "park_visits.csv")
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.hist(frame["visitors"], bins=[80, 120, 160, 200, 240, 280], edgecolor="white")
ax.set(title="Distribution of Daily Visits", xlabel="Visitors (people/day)", ylabel="Number of days")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
out = ROOT / "output" / "07_histogram.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150)
plt.close(fig)
print("Days:", len(frame))
print("Mean visits:", round(float(frame["visitors"].mean()), 1))
