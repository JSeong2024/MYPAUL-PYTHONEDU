# 한 행(Record)이 어떤 필드로 구성되는지 확인합니다.
record = {"station_id": "ST-01", "temperature_c": 23.5, "measured_at": "2026-11-01"}

print("필드:", ", ".join(record.keys()))
print("관측소:", record["station_id"])
print("기온:", record["temperature_c"], "°C")
print("날짜:", record["measured_at"])
