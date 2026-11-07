from pathlib import Path
import matplotlib.pyplot as plt

OUTPUT = Path(__file__).resolve().parents[2] / "output"
OUTPUT.mkdir(exist_ok=True)
import numpy as np

labels = ["D1", "D2", "D3", "D4", "D5"]
measurements = [7, 10, np.nan, 8, 12]
fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
ax.plot(labels, measurements, marker="o")
ax.set(title="Measurements with a Gap", xlabel="Day", ylabel="Value")
fig.savefig(OUTPUT / "exercise_04.png", dpi=150)
plt.close(fig)
