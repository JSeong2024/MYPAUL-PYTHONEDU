from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

x = np.arange(1, 31)
y = x ** 2
frame=pd.DataFrame({'x':x,'y':y})
print('Pearson',round(frame.x.corr(frame.y),3))
print('Spearman',round(frame.x.corr(frame.y,method='spearman'),3))
