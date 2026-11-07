import pandas as pd


def build_dataframe() -> pd.DataFrame:
    """product, quantity, unit_price 순서의 3행 DataFrame을 반환하세요."""
    # 상품: 커피 2개 3500원, 노트 3개 2500원, 펜 5개 1000원
    raise NotImplementedError


if __name__ == "__main__":
    print(build_dataframe().to_string(index=False))
