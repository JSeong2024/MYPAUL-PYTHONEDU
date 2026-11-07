from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/simpson_delivery.csv")

# TODO: 행별 합이 1인 구성비 테이블을 만듭니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
