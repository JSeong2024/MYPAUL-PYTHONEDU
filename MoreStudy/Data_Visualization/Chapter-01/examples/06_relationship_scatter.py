from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
frame = pd.read_csv(ROOT / "data" / "park_visits.csv")
fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.scatter(frame["temperature_c"], frame["visitors"], alpha=0.8)
ax.set(title="Temperature vs Park Visits (Synthetic Data)", xlabel="Temperature (°C)", ylabel="Visitors (people/day)")
ax.grid(alpha=0.25)
fig.tight_layout()
out = ROOT / "output" / "06_scatter_chart.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150)
plt.close(fig)
print("Points:", len(frame))
print("Interpretation: association is not causation")
