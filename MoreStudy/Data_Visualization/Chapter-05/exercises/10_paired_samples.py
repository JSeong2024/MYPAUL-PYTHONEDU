from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/support_tickets.csv")

# TODO: 두 열 모두 결측이 아닌 행 수를 출력합니다.
raise NotImplementedError("TODO: 요구사항에 맞게 완성하세요")
