"""Exercise 01 정답 — 고유 방문자 집계."""

monday = ["U-01", "U-02", "U-01", "U-03"]
tuesday = ["U-02", "U-04", "U-03", "U-04"]

unique_total = len(set(monday) | set(tuesday))
common = sorted(set(monday) & set(tuesday))
monday_unique_ordered = list(dict.fromkeys(monday))

print("전체 고유 방문자:", unique_total)
print("공통 방문자:", common)
print("월요일 최초 방문 순서:", monday_unique_ordered)
