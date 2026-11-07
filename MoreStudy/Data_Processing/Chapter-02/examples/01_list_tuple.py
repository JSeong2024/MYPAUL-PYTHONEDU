"""리스트와 튜플을 이용한 측정값 관리."""

readings = [21, 24, 23, 26]
readings.append(25)
readings[0] = 22

print("측정값:", readings)
print("최근 3개:", readings[-3:])
print("측정 개수:", len(readings))

sensor = ("ST-01", "광주", "temperature_c")
sensor_id, region, field = sensor
print(f"센서: {sensor_id} / {region} / {field}")

# 리스트의 슬라이스는 바깥쪽 리스트를 새로 만듭니다.
recent = readings[-3:]
recent[0] = 0
print("원본의 마지막 3개:", readings[-3:])
