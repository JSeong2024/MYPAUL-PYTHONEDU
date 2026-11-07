"""Exercise 04 — Long 데이터를 Wide로 바꾼 뒤 원래 행을 복원하세요."""
import pandas as pd


def pivot_and_restore(long: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """wide(index=store, columns=month), restored(store,month,sales_won), 각각 정렬."""
    # TODO: pivot(), reset_index(), melt()를 사용하세요.
    raise NotImplementedError


if __name__ == "__main__":
    data = pd.DataFrame({"store": ["A", "A", "B", "B"], "month": ["2026-01", "2026-02"] * 2, "sales_won": [10, 20, 30, 40]})
    wide, restored = pivot_and_restore(data)
    print(wide.to_string())
    print(restored.to_string(index=False))
