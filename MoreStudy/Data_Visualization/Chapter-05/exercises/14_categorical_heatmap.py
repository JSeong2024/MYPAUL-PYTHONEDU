from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/inspections.csv").drop_duplicates("inspection_id")

# TODO: `line` 행, `shift` 열로 평균 불량률 피벗테이블을 만듭니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
