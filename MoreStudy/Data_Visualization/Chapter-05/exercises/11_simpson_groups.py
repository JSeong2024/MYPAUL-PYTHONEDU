from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/simpson_delivery.csv")

# TODO: 전체 비율과 `zone`별 비율을 각각 출력합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
