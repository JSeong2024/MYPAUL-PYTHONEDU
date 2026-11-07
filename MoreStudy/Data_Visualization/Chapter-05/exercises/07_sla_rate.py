from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

x = pd.read_csv(ROOT / "data/support_tickets.csv").first_response_min.dropna()

# TODO: 기록된 응답시간 중 60분 이하 비율을 계산합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
