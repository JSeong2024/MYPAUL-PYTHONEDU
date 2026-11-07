from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/simpson_delivery.csv")
print('overall',df.groupby('carrier').on_time.mean().round(3).to_dict())
print('within',df.groupby(['zone','carrier']).on_time.mean().round(3).to_dict())
