from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/inspections.csv").drop_duplicates("inspection_id")
pivot=pd.pivot_table(df,index='line',columns='shift',values='is_defective',aggfunc='mean')
print(pivot.round(3).to_string())
