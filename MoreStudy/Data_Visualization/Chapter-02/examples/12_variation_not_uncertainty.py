from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)
import numpy as np

samples = {"Method A": [10.0, 10.5, 9.8, 11.0, 10.2], "Method B": [12.2, 11.5, 12.0, 13.1, 11.2]}
labels = list(samples)
means = [np.mean(samples[name]) for name in labels]
stds = [np.std(samples[name], ddof=1) for name in labels]
fig, ax = plt.subplots(figsize=(7.4, 3.8))
ax.errorbar(labels, means, yerr=stds, fmt="o", capsize=6)
ax.set(title="Mean ± Sample SD (Not a Confidence Interval)", ylabel="Measurement units", ylim=(8.8, 14.0))
ax.grid(axis="y", alpha=.2)
fig.tight_layout()
fig.savefig(OUTPUT / "12_variation_not_uncertainty.png", dpi=150)
plt.close(fig)
for label, mean, sd in zip(labels, means, stds): print(f"{label}: mean={mean:.2f}, sample SD={sd:.2f}")
