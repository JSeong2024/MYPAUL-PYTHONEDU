from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/support_tickets.csv")
print('all',round(df.first_response_min.median(),2))
print('resolved',round(df.loc[df.resolved.eq(1),'first_response_min'].median(),2))
