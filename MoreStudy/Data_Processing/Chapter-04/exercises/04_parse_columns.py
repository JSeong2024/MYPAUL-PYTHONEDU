import pandas as pd


def parse_columns(raw: pd.DataFrame) -> pd.DataFrame:
    """price_text와 date_text를 각각 price(Int64)·date(datetime) 열로 변환하세요."""
    # 가격 쉼표 제거, 잘못된 숫자·날짜는 결측으로 표시
    # 기존 raw DataFrame은 변경하지 않습니다.
    raise NotImplementedError
