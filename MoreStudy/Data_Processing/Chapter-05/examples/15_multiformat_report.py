"""Mini Project — CSV + JSON + Excel 데이터를 읽어 지역·분류별 보고서를 생성합니다."""
import json
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def load_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    orders = pd.read_csv(
        data_dir / "orders.csv",
        dtype={"order_id": "string", "region_code": "string", "product_id": "string"},
        encoding="utf-8",
    )
    catalog = json.loads((data_dir / "products.json").read_text(encoding="utf-8"))
    if catalog.get("schema_version") != 1 or not isinstance(catalog.get("products"), list):
        raise ValueError("지원하지 않는 상품 데이터 스키마입니다.")
    products = pd.DataFrame(catalog["products"])
    regions = pd.read_excel(data_dir / "regions.xlsx", sheet_name="Regions", engine="openpyxl", dtype={"region_code": "string"})
    return orders, products, regions

def build_report(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    orders, products, regions = load_data(data_dir)
    required = {"order_id", "order_date", "region_code", "product_id", "quantity", "unit_price", "status"}
    if not required.issubset(orders.columns):
        raise ValueError("주문 파일의 필수 열이 누락되었습니다.")
    if orders["order_id"].isna().any() or orders["order_id"].duplicated().any():
        raise ValueError("주문 ID가 누락되었거나 중복되었습니다.")
    if orders[["quantity", "unit_price", "status", "product_id", "region_code"]].isna().any().any():
        raise ValueError("주문 데이터에 필수값이 누락되었습니다.")
    if not orders["status"].isin(["completed", "canceled"]).all():
        raise ValueError("알 수 없는 주문 상태가 있습니다.")
    if (orders["quantity"] <= 0).any() or (orders["unit_price"] < 0).any():
        raise ValueError("수량과 단가 범위를 확인하세요.")
    dates = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="coerce")
    if dates.isna().any():
        raise ValueError("주문 날짜를 확인하세요.")
    if products["product_id"].isna().any() or products["product_id"].duplicated().any():
        raise ValueError("상품 ID에 중복 또는 누락이 있습니다.")
    if regions["region_code"].isna().any() or regions["region_code"].duplicated().any():
        raise ValueError("지역 코드에 중복 또는 누락이 있습니다.")
    completed = orders.loc[orders["status"].eq("completed")].copy()
    joined = completed.merge(products[["product_id", "name", "category"]], on="product_id", how="left", validate="many_to_one")
    joined = joined.merge(regions[["region_code", "region_name"]], on="region_code", how="left", validate="many_to_one")
    if joined[["name", "category", "region_name"]].isna().any().any():
        raise ValueError("상품 또는 지역 참조 데이터에 일치하지 않는 코드가 있습니다.")
    joined["revenue"] = joined["quantity"] * joined["unit_price"]
    by_region = joined.groupby("region_name", as_index=False)["revenue"].sum().sort_values("region_name").reset_index(drop=True)
    by_category = joined.groupby("category", as_index=False)["revenue"].sum().sort_values("category").reset_index(drop=True)
    return joined, by_region, by_category

def export_report(output_dir: Path, completed: pd.DataFrame, by_region: pd.DataFrame, by_category: pd.DataFrame) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    by_region.to_csv(output_dir / "revenue_by_region.csv", index=False, encoding="utf-8-sig")
    (output_dir / "revenue_by_category.json").write_text(
        by_category.to_json(orient="records", force_ascii=False, indent=2), encoding="utf-8"
    )
    db_path = output_dir / "report.sqlite"
    connection = sqlite3.connect(db_path)
    try:
        with connection:
            by_region.to_sql("revenue_by_region", connection, if_exists="replace", index=False)
            by_category.to_sql("revenue_by_category", connection, if_exists="replace", index=False)
    finally:
        connection.close()

def main() -> None:
    completed, by_region, by_category = build_report(ROOT / "data")
    export_report(ROOT / "output", completed, by_region, by_category)
    print("Completed orders:", len(completed))
    print("Total revenue:", int(completed["revenue"].sum()))
    print("Regions:", len(by_region))
    print("Categories:", len(by_category))
    print("Saved: revenue_by_region.csv, revenue_by_category.json, report.sqlite")

if __name__ == "__main__":
    main()
