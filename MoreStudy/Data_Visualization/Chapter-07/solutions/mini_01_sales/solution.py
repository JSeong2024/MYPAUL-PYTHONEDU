"""Reference solution: Mini 01 — Retail Sales Interactive Explorer."""
from pathlib import Path
import pandas as pd
import plotly.express as px
from project_core.io import DATA, ROOT, export_html, export_json


def analyze_sales(path: Path = DATA / "retail_sales.csv") -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(path, parse_dates=["date"])
    needed = {"date", "store", "category", "units", "unit_price_krw", "revenue_krw"}
    if not needed.issubset(raw):
        raise ValueError("필수 판매 열이 없습니다")
    if raw[["date", "store", "category"]].duplicated().any():
        raise ValueError("매장·상품 분류·날짜가 중복됩니다")
    if (raw[["units", "unit_price_krw", "revenue_krw"]] < 0).any().any():
        raise ValueError("음수 수량 또는 금액")
    if not (raw["units"] * raw["unit_price_krw"] == raw["revenue_krw"]).all():
        raise ValueError("매출 계산 결과가 일치하지 않습니다")
    by_store = raw.groupby("store", as_index=False).agg(revenue_krw=("revenue_krw", "sum"))
    by_date = raw.groupby(["date", "store"], as_index=False).agg(revenue_krw=("revenue_krw", "sum"))
    return by_store, by_date


def make_figures(by_store: pd.DataFrame, by_date: pd.DataFrame):
    bar = px.bar(by_store.sort_values("revenue_krw"), x="revenue_krw", y="store", orientation="h", text_auto=True,
                 title="Total Sales by Store", labels={"revenue_krw": "Revenue (KRW)", "store": "Store"})
    bar.update_layout(template="plotly_white")
    line = px.line(by_date.sort_values("date"), x="date", y="revenue_krw", color="store", markers=True,
                   title="Daily Sales by Store", labels={"date": "Date", "revenue_krw": "Revenue (KRW)"})
    line.update_layout(template="plotly_white", hovermode="x unified")
    line.update_xaxes(rangeslider_visible=True)
    return bar, line


def run(output: Path = ROOT / "output/mini_01_sales") -> dict:
    by_store, by_date = analyze_sales()
    bar, line = make_figures(by_store, by_date)
    export_html(bar, output / "store_totals.html")
    export_html(line, output / "daily_trends.html")
    result = {"stores": int(len(by_store)), "days": int(by_date.date.nunique()),
              "total_revenue_krw": int(by_store.revenue_krw.sum())}
    export_json(result, output / "summary.json")
    return result


if __name__ == "__main__":
    print(run())
