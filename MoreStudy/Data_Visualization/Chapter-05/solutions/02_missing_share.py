from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/support_tickets.csv")
share=df.groupby('team').first_response_min.apply(lambda x:x.isna().mean())
print(share.round(3).to_dict())
