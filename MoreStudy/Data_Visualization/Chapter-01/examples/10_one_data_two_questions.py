from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
frame = pd.read_csv(ROOT / "data" / "park_visits.csv", parse_dates=["date"])
summary = frame.groupby(frame["rainfall_mm"].gt(0))["visitors"].mean()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(frame["date"], frame["visitors"], marker="o")
ax1.set(title="When did visits change?", xlabel="Date", ylabel="Visitors (people/day)")
ax2.bar(["Dry", "Rainy"], [summary.loc[False], summary.loc[True]])
ax2.set(title="How do day groups compare?", xlabel="Day type", ylabel="Mean visitors (people/day)")
ax2.set_ylim(bottom=0)
fig.autofmt_xdate()
fig.tight_layout()
out = ROOT / "output" / "10_two_questions.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150)
plt.close(fig)
print("Different questions require different charts")
