from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/inspections.csv")

# TODO: 중복 ID 수를 구하고 고유 검사 행만 남깁니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
