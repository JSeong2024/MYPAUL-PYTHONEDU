"""Exercise 02 — 센서 측정값 검증 정답."""

raw_values = ["21.5", "", "-5", "20.0", "error", "18.5"]
floats = []
invalid = 0

for item in raw_values:
    try:
        value = float(item)
    except ValueError:
        invalid += 1
        continue
    if 0 <= value <= 50:
        floats.append(value)
    else:
        invalid += 1

print("유효:", len(floats), "건")
print("제외:", invalid, "건")
if floats:
    print(f"유효값 평균: {sum(floats) / len(floats):.1f}")
else:
    print("유효값 평균: 계산 불가")
