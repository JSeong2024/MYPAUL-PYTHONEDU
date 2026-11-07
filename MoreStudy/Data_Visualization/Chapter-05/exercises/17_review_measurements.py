from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/inspections.csv").drop_duplicates("inspection_id")

# TODO: 8–12mm 범위 외 값과 결측을 review=True로 표시합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
