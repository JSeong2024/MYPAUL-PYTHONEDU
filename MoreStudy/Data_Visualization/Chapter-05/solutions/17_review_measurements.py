from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/inspections.csv").drop_duplicates("inspection_id")
review=df.thickness_mm.isna() | ~df.thickness_mm.between(8,12)
print('review',int(review.sum()))
