from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/shipments.csv")
print('rows',len(df))
print('unique_ids',df.shipment_id.nunique())
print(df.status.value_counts().to_dict())
