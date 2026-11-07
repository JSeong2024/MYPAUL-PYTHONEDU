from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

x = pd.read_csv(ROOT / "data/support_tickets.csv").first_response_min.dropna()
print('share',round((x<=60).mean(),3),'n',len(x))
