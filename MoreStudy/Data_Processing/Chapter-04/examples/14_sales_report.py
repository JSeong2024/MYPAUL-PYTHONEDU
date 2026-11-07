"""Mini Project: 주문 데이터 읽기 → 기본 검증 → 집계 → CSV 저장."""
from pathlib import Path
import pandas as pd

CHAPTER = Path(__file__).resolve().parents[1]
REQUIRED = {"order_id", "order_date", "region", "category", "product", "quantity", "unit_price", "status"}


def load_orders(path: Path) -> pd.DataFrame:
    orders = pd.read_csv(path)
    missing_columns = REQUIRED.difference(orders.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing_columns))}")
    if orders.empty or orders["order_id"].isna().any() or orders["order_id"].duplicated().any():
        raise ValueError("Order IDs must be present and unique")
    if orders[list(REQUIRED)].isna().any().any():
        raise ValueError("Required fields contain missing values")
    if not orders["status"].isin(["completed", "canceled"]).all():
        raise ValueError("Unexpected order status")
    for column in ("quantity", "unit_price"):
        values = pd.to_numeric(orders[column], errors="coerce")
        if values.isna().any() or (values < (1 if column == "quantity" else 0)).any() or (values % 1 != 0).any():
            raise ValueError(f"Invalid numeric column: {column}")
        orders[column] = values.astype("int64")
    parsed_dates = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="coerce")
    if parsed_dates.isna().any():
        raise ValueError("Invalid order date")
    orders["order_date"] = parsed_dates
    return orders


def make_reports(orders: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    completed = orders.loc[orders["status"] == "completed"].copy()
    completed["amount"] = completed["quantity"] * completed["unit_price"]
    by_region = completed.groupby("region", as_index=False).agg(
        orders=("order_id", "size"), revenue=("amount", "sum")
    ).sort_values("region").reset_index(drop=True)
    by_category = completed.groupby("category", as_index=False).agg(
        orders=("order_id", "size"), revenue=("amount", "sum")
    ).sort_values("category").reset_index(drop=True)
    by_day = completed.groupby("order_date", as_index=False).agg(
        orders=("order_id", "size"), revenue=("amount", "sum")
    ).sort_values("order_date").reset_index(drop=True)
    return by_region, by_category, by_day


def export_reports(reports: tuple[pd.DataFrame, ...], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, frame in zip(("sales_by_region.csv", "sales_by_category.csv", "sales_by_day.csv"), reports):
        frame.to_csv(output_dir / filename, index=False, encoding="utf-8")


def main() -> None:
    orders = load_orders(CHAPTER / "data" / "orders.csv")
    reports = make_reports(orders)
    export_reports(reports, CHAPTER / "output")
    valid_count = int(orders["status"].eq("completed").sum())
    total_sales = int(reports[0]["revenue"].sum())
    print(f"Orders: {len(orders)} (completed {valid_count}, canceled {len(orders) - valid_count})")
    print(f"Revenue: {total_sales:,} KRW")
    print("Sales by region:")
    print(reports[0].to_string(index=False))
    print("Saved: sales_by_region.csv, sales_by_category.csv, sales_by_day.csv")


if __name__ == "__main__":
    main()
