from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/inspections.csv")

# TODO: 중복 검사 ID를 제거하고 n, defects, rate를 계산합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
