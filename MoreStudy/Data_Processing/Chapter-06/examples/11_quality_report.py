import pandas as pd

records = pd.DataFrame({
    "decision": ["accepted", "rejected", "review", "accepted", "rejected"]
})
counts = records["decision"].value_counts()
for state in ("accepted", "rejected", "review"):
    print(f"{state}: {int(counts.get(state, 0))}")
print("Total:", len(records))
