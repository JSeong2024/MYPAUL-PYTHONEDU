from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

s = pd.read_csv(ROOT / "data/support_tickets.csv").first_response_min.dropna()

# TODO: 평균·중앙값·P90을 소수 1자리로 출력합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
