"""Chapter 01 Mini Project: 주간 주문 데이터 검증 및 매출 요약."""

import csv
from collections import Counter
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "weekly_orders.csv"


def validate_order(row: dict[str, str], seen_ids: set[str]) -> tuple[dict | None, str | None]:
    order_id = (row.get("order_id") or "").strip()
    category = (row.get("category") or "").strip()
    if not order_id or not category:
        return None, "필수값 누락"
    if order_id in seen_ids:
        return None, "주문 번호 중복"

    try:
        quantity = int((row.get("quantity") or "").strip())
        unit_price = int((row.get("unit_price") or "").strip())
    except ValueError:
        return None, "수량/단가 변환 실패"

    if quantity < 1 or unit_price < 0:
        return None, "허용 범위 초과"

    seen_ids.add(order_id)
    return {"order_id": order_id, "category": category,
            "quantity": quantity, "unit_price": unit_price}, None


def main() -> None:
    seen_ids: set[str] = set()
    revenue_by_category: dict[str, int] = {}
    errors: Counter[str] = Counter()
    rows = 0
    valid_rows = 0

    with DATA_PATH.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        expected = {"order_id", "category", "quantity", "unit_price"}
        if reader.fieldnames is None or set(reader.fieldnames) != expected:
            raise ValueError("CSV 헤더가 데이터 명세와 다릅니다.")

        for row in reader:
            rows += 1
            order, reason = validate_order(row, seen_ids)
            if reason is not None:
                errors[reason] += 1
                continue

            valid_rows += 1
            category = order["category"]
            amount = order["quantity"] * order["unit_price"]
            revenue_by_category[category] = revenue_by_category.get(category, 0) + amount

    print("주간 주문 처리 결과")
    print(f"원본: {rows}건 | 유효: {valid_rows}건 | 제외: {sum(errors.values())}건")
    for category in sorted(revenue_by_category):
        print(f"{category}: {revenue_by_category[category]:,}원")
    print(f"총매출: {sum(revenue_by_category.values()):,}원")
    for reason in sorted(errors):
        print(f"제외 사유 - {reason}: {errors[reason]}건")


if __name__ == "__main__":
    main()
