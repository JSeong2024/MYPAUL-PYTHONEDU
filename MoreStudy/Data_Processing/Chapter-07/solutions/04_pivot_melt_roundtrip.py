"""Exercise 04 — 모범답안."""
import pandas as pd


def pivot_and_restore(long: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    wide = long.pivot(index="store", columns="month", values="sales_won").sort_index()
    restored = (wide.reset_index().melt(id_vars="store", var_name="month", value_name="sales_won")
                .sort_values(["store", "month"]).reset_index(drop=True))
    return wide, restored


if __name__ == "__main__":
    data = pd.DataFrame({"store": ["A", "A", "B", "B"], "month": ["2026-01", "2026-02"] * 2, "sales_won": [10, 20, 30, 40]})
    wide, restored = pivot_and_restore(data)
    print(wide.to_string())
    print(restored.to_string(index=False))
