from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/shipments.csv")
df = df.loc[df.status.eq("delivered") & df.actual_days.notna()]
out=df.groupby('zone').actual_days.agg(['size','median'])
print(out.round(2).to_string())
