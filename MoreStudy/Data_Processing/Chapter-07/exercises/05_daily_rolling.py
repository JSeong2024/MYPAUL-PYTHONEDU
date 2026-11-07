"""Exercise 05 — 빈 날짜를 0으로 보완하고 3일 이동합을 계산하세요."""
import pandas as pd


def daily_rolling_sum(frame: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """date, sales_won 입력 → 날짜별 합계 및 rolling_3d_sum. 누락된 날은 0 매출 가정."""
    # TODO: 같은 날짜 중복 합산, 전체 달력 구성, rolling(3, min_periods=1)
    raise NotImplementedError


if __name__ == "__main__":
    data = pd.DataFrame({"date": ["2026-01-01", "2026-01-03", "2026-01-03"], "sales_won": [100, 200, 50]})
    print(daily_rolling_sum(data, "2026-01-01", "2026-01-04").to_string(index=False))
