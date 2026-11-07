"""Chapter 07 Mini Project: 검증된 테이블 결합 및 매출 데이터 마트 생성."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"


def load_sources(data_dir: Path = DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    orders = pd.read_csv(data_dir / "order_lines.csv", dtype={
        "line_id": "string", "order_id": "string", "store_id": "string", "product_id": "string",
        "quantity": "int64", "unit_price_won": "int64", "discount_pct": "int64",
    })
    orders["order_date"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="raise")
    products = pd.read_csv(data_dir / "products.csv", dtype={"product_id": "string"})
    stores = pd.read_csv(data_dir / "stores.csv", dtype={"store_id": "string"})
    return orders, products, stores


def validate_sources(orders: pd.DataFrame, products: pd.DataFrame, stores: pd.DataFrame) -> None:
    for frame, key in ((orders, "line_id"), (products, "product_id"), (stores, "store_id")):
        if frame[key].isna().any() or frame[key].duplicated().any():
            raise ValueError(f"Missing or duplicated key: {key}")
    required = ["line_id", "order_id", "order_date", "store_id", "product_id", "quantity", "unit_price_won", "discount_pct"]
    if orders[required].isna().any().any():
        raise ValueError("Missing required order field")
    if (orders["quantity"] < 1).any() or (orders["unit_price_won"] < 0).any():
        raise ValueError("Invalid quantity or unit price")
    if (~orders["discount_pct"].between(0, 100)).any():
        raise ValueError("Discount percentage is outside 0..100")
    if orders["order_date"].isna().any():
        raise ValueError("Invalid order date")


def enrich_orders(orders: pd.DataFrame, products: pd.DataFrame, stores: pd.DataFrame) -> pd.DataFrame:
    result = orders.merge(
        products[["product_id", "product_name", "category"]],
        on="product_id", how="left", validate="many_to_one", indicator="product_match",
    )
    if result["product_match"].ne("both").any():
        raise ValueError("Unknown product_id in orders")
    result = result.drop(columns="product_match").merge(
        stores[["store_id", "store_name", "region"]],
        on="store_id", how="left", validate="many_to_one", indicator="store_match",
    )
    if result["store_match"].ne("both").any():
        raise ValueError("Unknown store_id in orders")
    result = result.drop(columns="store_match")
    gross = result["quantity"] * result["unit_price_won"]
    numerator = gross * (100 - result["discount_pct"])
    if (numerator % 100).ne(0).any():
        raise ValueError("Discount creates fractional KRW: rounding policy required")
    result["net_sales_won"] = numerator // 100
    result["month"] = result["order_date"].dt.strftime("%Y-%m")
    return result.sort_values("line_id").reset_index(drop=True)


def make_summaries(frame: pd.DataFrame, store_ids: pd.Series) -> dict[str, pd.DataFrame]:
    by_store = frame.groupby(["store_id", "store_name", "region"], as_index=False).agg(
        order_lines=("line_id", "size"), orders=("order_id", "nunique"),
        units=("quantity", "sum"), net_sales_won=("net_sales_won", "sum"),
    ).sort_values("store_id").reset_index(drop=True)
    by_category_month = frame.groupby(["month", "category"], as_index=False).agg(
        order_lines=("line_id", "size"), units=("quantity", "sum"),
        net_sales_won=("net_sales_won", "sum"),
    ).sort_values(["month", "category"]).reset_index(drop=True)
    sparse_daily = frame.groupby(["order_date", "store_id"], as_index=False).agg(
        order_lines=("line_id", "size"), net_sales_won=("net_sales_won", "sum"),
    )
    # 예제의 거래 기록은 모든 날짜가 완전히 수집되었다는 전제. 없는 거래일은 0원.
    calendar = pd.date_range(frame["order_date"].min(), frame["order_date"].max(), freq="D")
    full_index = pd.MultiIndex.from_product(
        [calendar, sorted(store_ids.tolist())], names=["order_date", "store_id"],
    )
    daily = (sparse_daily.set_index(["order_date", "store_id"])
             .reindex(full_index, fill_value=0).reset_index())
    daily = daily.sort_values(["store_id", "order_date"]).reset_index(drop=True)
    daily["rolling_7d_avg_won"] = (daily.groupby("store_id")["net_sales_won"]
        .transform(lambda values: values.rolling(window=7, min_periods=1).mean())
        .round(2))
    daily["cumulative_sales_won"] = daily.groupby("store_id")["net_sales_won"].cumsum()
    return {"sales_by_store": by_store, "sales_by_category_month": by_category_month,
            "sales_daily_by_store": daily}


def run_pipeline(data_dir: Path = DATA_DIR, output_dir: Path = OUTPUT_DIR) -> dict[str, object]:
    orders, products, stores = load_sources(data_dir)
    validate_sources(orders, products, stores)
    enriched = enrich_orders(orders, products, stores)
    reports = make_summaries(enriched, stores["store_id"])
    assert len(enriched) == len(orders), "Merge must not multiply source rows"
    assert int(reports["sales_by_store"]["net_sales_won"].sum()) == int(enriched["net_sales_won"].sum())
    assert int(reports["sales_by_category_month"]["net_sales_won"].sum()) == int(enriched["net_sales_won"].sum())
    summary = {
        "source_lines": int(len(orders)),
        "distinct_orders": int(orders["order_id"].nunique()),
        "stores": int(stores["store_id"].nunique()),
        "products": int(products["product_id"].nunique()),
        "net_sales_won": int(enriched["net_sales_won"].sum()),
        "first_date": enriched["order_date"].min().strftime("%Y-%m-%d"),
        "last_date": enriched["order_date"].max().strftime("%Y-%m-%d"),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, report in {"enriched_order_lines": enriched, **reports}.items():
        to_write = report.copy()
        if "order_date" in to_write:
            to_write["order_date"] = to_write["order_date"].dt.strftime("%Y-%m-%d")
        to_write.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8", lineterminator="\n")
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate validated store sales summaries")
    parser.add_argument("--data", type=Path, default=DATA_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    arguments = parser.parse_args()
    print(json.dumps(run_pipeline(arguments.data, arguments.output), ensure_ascii=False, sort_keys=True))
