# 데이터 개수, 필드, 상위 기록, 비어 있는 값을 점검합니다.
records = [
    {"id": "A-01", "region": "서울", "value": 18},
    {"id": "A-02", "region": "광주", "value": None},
    {"id": "A-03", "region": "부산", "value": 25},
]

print("전체 행:", len(records))
print("필드:", ", ".join(records[0].keys()))
print("첫 행:", records[0])
missing = sum(row["value"] is None for row in records)
print("값 누락:", missing)
