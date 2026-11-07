from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import matplotlib.pyplot as plt
import numpy as np

# 2026-10-04는 관측되지 않은 날이며 0°C가 아님
labels = ["Oct 01", "Oct 02", "Oct 03", "Oct 04", "Oct 05", "Oct 06"]
temperatures = [19.2, 20.1, 20.5, np.nan, 18.1, 17.8]

fig, ax = plt.subplots(figsize=(8, 4.2), layout="constrained")
ax.plot(labels, temperatures, marker="o")
ax.set(title="Temperature with Missing Observation", xlabel="Date", ylabel="°C")
ax.grid(axis="y", alpha=0.25)
fig.savefig(ROOT / "figures" / "08_missing_dates.png", dpi=150)
plt.close(fig)
