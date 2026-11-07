from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

s = pd.Series([2, 2, 3, 3, 4, 40],dtype=float)
print('all',round(s.mean(),2),'sensitivity',round(s[s<10].mean(),2))
