"""주문 데이터 품질 검사: 원본 보존 / 제외·검토 분리 / 결과 및 감사 로그 생성."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = (
    "order_id", "order_date", "customer_id", "region", "category",
    "quantity", "unit_price", "status",
)


def load_policy(path: Path) -> dict:
    policy = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "allowed_regions", "allowed_categories", "allowed_statuses",
        "revenue_status", "max_quantity", "max_unit_price",
        "review_unit_price_over", "earliest_date", "latest_date",
    }
    missing = required - policy.keys()
    if missing:
        raise ValueError(f"Policy keys missing: {sorted(missing)}")
    for key in ("max_quantity", "max_unit_price", "review_unit_price_over"):
        if type(policy[key]) is not int or policy[key] <= 0:
            raise ValueError(f"Invalid positive integer policy: {key}")
    if policy["review_unit_price_over"] > policy["max_unit_price"]:
        raise ValueError("Review threshold exceeds maximum price")
    for key in ("allowed_regions", "allowed_categories", "allowed_statuses"):
        values = policy[key]
        if not isinstance(values, list) or not values or not all(isinstance(v, str) and v for v in values):
            raise ValueError(f"Invalid policy list: {key}")
        if len({v.casefold() for v in values}) != len(values):
            raise ValueError(f"Duplicate case-insensitive values: {key}")
    if policy["revenue_status"] not in policy["allowed_statuses"]:
        raise ValueError("Revenue status must be allowed")
    start = pd.Timestamp(policy["earliest_date"])
    end = pd.Timestamp(policy["latest_date"])
    if start > end:
        raise ValueError("Invalid policy date range")
    return policy


def _canonical(values: pd.Series, allowed: list[str]) -> pd.Series:
    lookup = {item.casefold(): item for item in allowed}
    return values.str.casefold().map(lookup).astype("string")


def clean_orders(source: pd.DataFrame, policy: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """accepted, rejected, review, audit 반환. source를 직접 수정하지 않음."""
    if tuple(source.columns) != COLUMNS:
        raise ValueError(f"Expected columns: {', '.join(COLUMNS)}")
    if not all(pd.api.types.is_string_dtype(dtype) for dtype in source.dtypes):
        raise ValueError("Read raw data with dtype='string' before cleaning")

    values = source.copy(deep=True)
    for name in COLUMNS:
        values[name] = values[name].str.strip().replace("", pd.NA)

    values["region"] = _canonical(values["region"], policy["allowed_regions"])
    values["category"] = _canonical(values["category"], policy["allowed_categories"])
    values["status"] = values["status"].str.casefold()

    numeric_qty = pd.to_numeric(values["quantity"], errors="coerce")
    numeric_price = pd.to_numeric(values["unit_price"], errors="coerce")
    parsed_dates = pd.to_datetime(values["order_date"], format="%Y-%m-%d", errors="coerce")
    date_shape = values["order_date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}").fillna(False)

    rules = {
        "INVALID_ORDER_ID": values["order_id"].str.fullmatch(r"ORD-\d{3}").fillna(False),
        "INVALID_CUSTOMER_ID": values["customer_id"].str.fullmatch(r"C\d{3}").fillna(False),
        "INVALID_DATE": (date_shape & parsed_dates.between(
            pd.Timestamp(policy["earliest_date"]), pd.Timestamp(policy["latest_date"])
        )).fillna(False),
        "INVALID_REGION": values["region"].notna(),
        "INVALID_CATEGORY": values["category"].notna(),
        "INVALID_QUANTITY": (
            numeric_qty.notna() & numeric_qty.ge(1) &
            numeric_qty.le(policy["max_quantity"]) & numeric_qty.mod(1).eq(0)
        ).fillna(False),
        "INVALID_UNIT_PRICE": (
            numeric_price.notna() & numeric_price.ge(1) &
            numeric_price.le(policy["max_unit_price"]) & numeric_price.mod(1).eq(0)
        ).fillna(False),
        "INVALID_STATUS": values["status"].isin(policy["allowed_statuses"]).fillna(False),
        "DUPLICATE_ORDER_ID": (~values["order_id"].duplicated(keep="first")).fillna(False),
    }

    decisions: list[str] = []
    issues: list[str] = []
    audit_rows: list[dict] = []
    for position in range(len(source)):
        failures = [code for code, passing in rules.items() if not bool(passing.iloc[position])]
        if failures:
            decision = "rejected"
        elif bool(numeric_price.iloc[position] > policy["review_unit_price_over"]):
            decision = "review"
            failures = ["HIGH_UNIT_PRICE"]
        else:
            decision = "accepted"
        decisions.append(decision)
        joined = ";".join(failures)
        issues.append(joined)
        audit_rows.append({
            "source_line": position + 2,
            "order_id": source.iloc[position]["order_id"],
            "decision": decision,
            "issues": joined,
        })

    accepted_positions = [i for i, value in enumerate(decisions) if value == "accepted"]
    rejected_positions = [i for i, value in enumerate(decisions) if value == "rejected"]
    review_positions = [i for i, value in enumerate(decisions) if value == "review"]

    accepted = values.iloc[accepted_positions].copy().reset_index(drop=True)
    accepted["order_date"] = parsed_dates.iloc[accepted_positions].dt.strftime("%Y-%m-%d").to_numpy()
    accepted["quantity"] = numeric_qty.iloc[accepted_positions].astype("int64").to_numpy()
    accepted["unit_price"] = numeric_price.iloc[accepted_positions].astype("int64").to_numpy()
    accepted["total_price"] = accepted["quantity"] * accepted["unit_price"]

    def quarantined(positions: list[int]) -> pd.DataFrame:
        result = source.iloc[positions].copy().reset_index(drop=True)
        result.insert(0, "source_line", [p + 2 for p in positions])
        result["issues"] = [issues[p] for p in positions]
        return result

    return accepted, quarantined(rejected_positions), quarantined(review_positions), pd.DataFrame(audit_rows)


def run_pipeline(source_path: Path, policy_path: Path, output_dir: Path) -> dict:
    policy = load_policy(policy_path)
    raw = pd.read_csv(source_path, dtype="string", keep_default_na=False, encoding="utf-8")
    accepted, rejected, review, audit = clean_orders(raw, policy)

    revenue = (
        accepted.loc[accepted["status"] == policy["revenue_status"]]
        .groupby("region", as_index=False)["total_price"]
        .sum()
        .rename(columns={"total_price": "revenue_krw"})
        .sort_values("region")
        .reset_index(drop=True)
    )
    issue_counts = Counter(
        issue for issue_list in audit["issues"]
        for issue in issue_list.split(";") if issue
    )
    report = {
        "source_records": int(len(raw)),
        "accepted_records": int(len(accepted)),
        "rejected_records": int(len(rejected)),
        "review_records": int(len(review)),
        "completed_orders": int(accepted["status"].eq(policy["revenue_status"]).sum()),
        "completed_revenue_krw": int(revenue["revenue_krw"].sum()),
        "issue_counts": dict(sorted(issue_counts.items())),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, frame in (
        ("cleaned_orders.csv", accepted),
        ("rejected_orders.csv", rejected),
        ("review_orders.csv", review),
        ("audit_log.csv", audit),
        ("revenue_by_region.csv", revenue),
    ):
        frame.to_csv(output_dir / name, index=False, encoding="utf-8-sig")
    (output_dir / "quality_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    summary = run_pipeline(
        ROOT / "data/raw_orders.csv",
        ROOT / "data/cleaning_policy.json",
        ROOT / "output",
    )
    for label in (
        "source_records", "accepted_records", "rejected_records",
        "review_records", "completed_orders", "completed_revenue_krw",
    ):
        print(f"{label}: {summary[label]}")
    print("Saved to: output/")
