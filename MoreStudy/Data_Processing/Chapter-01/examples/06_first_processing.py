# 상품별 매출 계산: 수량 × 단가 (원)
orders = [
    {"category": "음료", "quantity": 2, "unit_price": 1800},
    {"category": "문구", "quantity": 3, "unit_price": 1200},
    {"category": "음료", "quantity": 1, "unit_price": 2500},
]

revenue_by_category = {}
for order in orders:
    category = order["category"]
    amount = order["quantity"] * order["unit_price"]
    revenue_by_category[category] = revenue_by_category.get(category, 0) + amount

print("전체 주문:", len(orders), "건")
print("전체 매출:", sum(revenue_by_category.values()), "원")
for category in sorted(revenue_by_category):
    print(f"{category}: {revenue_by_category[category]}원")
