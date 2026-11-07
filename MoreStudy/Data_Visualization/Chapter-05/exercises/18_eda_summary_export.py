from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

import json
df = pd.read_csv(ROOT / "data/inspections.csv")

# TODO: 데이터셋 행 수·중복·불량률을 JSON으로 출력하고 저장합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
