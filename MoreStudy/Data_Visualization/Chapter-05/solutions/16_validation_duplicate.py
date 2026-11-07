from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/inspections.csv")
duplicates=int(df.inspection_id.duplicated().sum())
unique=df.drop_duplicates('inspection_id')
print('duplicates',duplicates,'unique',len(unique))
