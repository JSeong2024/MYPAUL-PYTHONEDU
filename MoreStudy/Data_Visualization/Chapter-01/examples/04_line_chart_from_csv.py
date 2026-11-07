from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
frame = pd.read_csv(ROOT / "data" / "park_visits.csv", parse_dates=["date"])
frame = frame.sort_values("date")
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(frame["date"], frame["visitors"], marker="o")
ax.set(title="Daily Park Visits (Synthetic Data)", xlabel="Date", ylabel="Visitors (people/day)")
ax.grid(axis="y", alpha=0.3)
fig.autofmt_xdate()
fig.tight_layout()
out = ROOT / "output" / "04_visitor_trend.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150)
plt.close(fig)
print("Days:", len(frame))
print("Total visitors:", int(frame["visitors"].sum()))
