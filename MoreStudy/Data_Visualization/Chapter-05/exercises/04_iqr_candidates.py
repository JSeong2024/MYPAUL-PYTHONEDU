from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

x = pd.read_csv(ROOT / "data/shipments.csv").actual_days.dropna()

# TODO: Q1/Q3를 구하고 IQR 상한 초과 건수를 출력합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
