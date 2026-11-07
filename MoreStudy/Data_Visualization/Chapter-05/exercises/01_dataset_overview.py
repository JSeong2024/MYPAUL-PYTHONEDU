from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/shipments.csv")

# TODO: 전체 행·고유 ID·상태별 건수를 출력합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
