from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

import json
df = pd.read_csv(ROOT / "data/inspections.csv")
unique=df.drop_duplicates('inspection_id')
result={'raw_count':len(df),'unique_count':len(unique),'defect_rate':float(unique.is_defective.mean())}
out=ROOT/'output/practice_18';out.mkdir(parents=True,exist_ok=True)
(out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(result)
