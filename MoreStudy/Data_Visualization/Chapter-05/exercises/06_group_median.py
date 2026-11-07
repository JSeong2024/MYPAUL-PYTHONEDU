from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/shipments.csv")
df = df.loc[df.status.eq("delivered") & df.actual_days.notna()]

# TODO: 지역별 n과 중앙값을 DataFrame으로 출력합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
