"""Exercise 03 정답 — 재고 변동 집계."""

from collections import Counter, defaultdict

movements = [
    ("노트", 5),
    ("연필", 12),
    ("노트", -2),
    ("파일", 4),
    ("연필", -3),
    ("노트", 3),
]

net_change = defaultdict(int)
counts = Counter()
for name, quantity in movements:
    net_change[name] += quantity
    counts[name] += 1

for name in sorted(net_change):
    print(f"{name}: 순변동 {net_change[name]}개 / 기록 {counts[name]}건")
