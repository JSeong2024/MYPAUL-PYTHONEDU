from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)
import pandas as pd

frame = pd.read_csv(ROOT / "data" / "library_visits.csv")
counts = frame["visitors"]
fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.8), sharey=True)
axes[0].hist(counts, bins=4, edgecolor="white")
axes[0].set(title="4 Bins", xlabel="Visitors / day", ylabel="Days")
axes[1].hist(counts, bins=12, edgecolor="white")
axes[1].set(title="12 Bins", xlabel="Visitors / day")
fig.tight_layout()
fig.savefig(OUTPUT / "11_histogram_bin_choice.png", dpi=150)
plt.close(fig)
print("Observations:", len(counts))
