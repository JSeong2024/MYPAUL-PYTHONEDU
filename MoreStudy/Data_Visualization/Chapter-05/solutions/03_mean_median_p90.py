from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

s = pd.read_csv(ROOT / "data/support_tickets.csv").first_response_min.dropna()
print('mean',round(s.mean(),1),'median',round(s.median(),1),'P90',round(s.quantile(.9),1))
