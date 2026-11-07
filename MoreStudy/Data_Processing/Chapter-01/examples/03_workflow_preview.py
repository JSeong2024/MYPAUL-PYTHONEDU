# 원본 데이터는 별도로 유지하고, 검증된 값을 새 목록에 담습니다.
raw_readings = ["23.5", " 25.0 ", "", "error", "22.0"]
valid_readings = []
invalid_count = 0

for item in raw_readings:
    text = item.strip()
    try:
        if not text:
            raise ValueError("빈 값")
        valid_readings.append(float(text))
    except ValueError:
        invalid_count += 1

print("원본:", raw_readings)
print("처리 후:", valid_readings)
print("제외된 값:", invalid_count)
