from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

x = pd.read_csv(ROOT / "data/shipments.csv").actual_days.dropna()
q1,q3=x.quantile([.25,.75]);upper=q3+1.5*(q3-q1)
print('upper',round(upper,2),'candidates',int((x>upper).sum()))
