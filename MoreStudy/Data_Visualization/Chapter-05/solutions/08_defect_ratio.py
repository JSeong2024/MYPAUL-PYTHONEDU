from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/inspections.csv")
df=df.drop_duplicates('inspection_id')
g=df.groupby('line').is_defective.agg(n='size',defects='sum')
g['rate']=g.defects/g.n
print(g.round(3).to_string())
