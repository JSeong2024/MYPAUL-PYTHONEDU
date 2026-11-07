from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)
import pandas as pd

frame = pd.read_csv(ROOT / "data" / "library_visits.csv", parse_dates=["date"])
east = frame.loc[frame["branch"].eq("Eastgate"), ["date", "visitors"]]
full_dates = pd.date_range("2026-10-01", "2026-10-14", freq="D")
east = east.set_index("date").reindex(full_dates)
assert east["visitors"].isna().sum() == 1
fig, ax = plt.subplots(figsize=(8.4, 3.6))
ax.plot(east.index, east["visitors"], marker="o")
ax.set(title="Eastgate: Missing Observation Remains a Gap", ylabel="Visitors / day")
ax.tick_params(axis="x", rotation=30)
ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig(OUTPUT / "10_missing_dates.png", dpi=150)
plt.close(fig)
print("Missing date:", east.index[east["visitors"].isna()][0].date())
