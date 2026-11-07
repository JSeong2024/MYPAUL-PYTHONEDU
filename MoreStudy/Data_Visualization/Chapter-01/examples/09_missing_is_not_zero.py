from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
VALUES = [12, 15, math.nan, 18, 17]  # 수요일은 관측 누락
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.plot(DAYS, VALUES, marker="o")
ax.set(title="Missing Observation Is Not Zero", xlabel="Day", ylabel="Visitors (people)")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
out = Path(__file__).resolve().parents[1] / "output" / "09_missing_data.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150)
plt.close(fig)
print("Observed values:", sum(not math.isnan(v) for v in VALUES))
print("Missing values:", sum(math.isnan(v) for v in VALUES))
