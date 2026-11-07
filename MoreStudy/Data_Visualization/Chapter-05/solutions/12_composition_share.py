from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/simpson_delivery.csv")
mix=pd.crosstab(df.carrier,df.zone,normalize='index')
assert np.allclose(mix.sum(axis=1),1)
print(mix.round(3).to_string())
