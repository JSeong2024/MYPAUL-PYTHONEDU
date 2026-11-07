"""Counter와 defaultdict를 이용한 빈도와 그룹 집계."""

from collections import Counter, defaultdict

orders = [
    ("문구", 3500),
    ("음료", 2500),
    ("문구", 1200),
    ("간식", 1800),
    ("음료", 2200),
]

counts = Counter(category for category, _ in orders)
revenue = defaultdict(int)
for category, price in orders:
    revenue[category] += price

for category in sorted(counts):
    print(f"{category}: {counts[category]}건 / {revenue[category]:,}원")
print("최다 주문 수:", max(counts.values()))
