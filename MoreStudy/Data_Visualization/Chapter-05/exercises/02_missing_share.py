from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/support_tickets.csv")

# TODO: `team`별 결측률을 0–1 범위로 출력합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
