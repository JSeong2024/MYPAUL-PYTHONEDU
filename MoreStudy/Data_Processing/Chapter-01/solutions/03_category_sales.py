"""Exercise 03 — 분류별 매출 집계 정답."""

orders = [
    {"category": "음료", "quantity": 2, "unit_price": 1500},
    {"category": "문구", "quantity": 3, "unit_price": 1000},
    {"category": "음료", "quantity": 1, "unit_price": 2500},
    {"category": "간식", "quantity": 2, "unit_price": 2000},
]

category_sales = {}
for order in orders:
    category = order["category"]
    amount = order["quantity"] * order["unit_price"]
    category_sales[category] = category_sales.get(category, 0) + amount

for category in sorted(category_sales):
    print(f"{category}: {category_sales[category]}원")
print("전체 매출:", sum(category_sales.values()), "원")
