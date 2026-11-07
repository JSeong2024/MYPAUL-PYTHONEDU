from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/support_tickets.csv")
pairs=df.dropna(subset=['first_response_min','customer_rating'])
print('paired n',len(pairs))
