from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

x = np.array([18.2, 19.5, 20.1, 22.8, 21.0, 19.9])
rng=np.random.default_rng(17)
means=rng.choice(x,size=(1000,len(x)),replace=True).mean(axis=1)
print(np.quantile(means,[.025,.975]).round(2))
