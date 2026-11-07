from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/support_tickets.csv")

# TODO: 전체와 해결된 문의의 첫 응답시간 중앙값을 비교합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
