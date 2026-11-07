"""Exercise 04 정답 — 그룹 집계, 정렬 및 필터링."""

from collections import defaultdict

items = [
    {"category": "문구", "amount": 3000},
    {"category": "음료", "amount": 2500},
    {"category": "문구", "amount": 1200},
    {"category": "간식", "amount": 4200},
    {"category": "음료", "amount": 1900},
    {"category": "기타", "amount": 700},
]

total = defaultdict(int)
for item in items:
    total[item["category"]] += item["amount"]

ranking = sorted(total.items(), key=lambda pair: (-pair[1], pair[0]))
for rank, (category, amount) in enumerate(ranking, start=1):
    print(f"{rank}위 {category}: {amount:,}원")

above_threshold = [category for category, amount in ranking if amount >= 4000]
print("4,000원 이상:", above_threshold)
