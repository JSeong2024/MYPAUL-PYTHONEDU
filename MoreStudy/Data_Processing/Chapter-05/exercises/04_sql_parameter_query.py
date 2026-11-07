"""Exercise 04: SQLite 바인딩 매개변수로 조건에 맞는 행을 조회하세요."""
import sqlite3

def find_devices(minimum: float) -> list[str]:
    # TODO: 메모리 DB에 센서 3개를 저장합니다.
    # ST-01: 22.5, ST-02: 26.0, ST-03: 20.5
    # TODO: temperature >= minimum을 매개변수 바인딩으로 조회합니다.
    # TODO: sensor_id 오름차순 목록을 반환합니다.
    raise NotImplementedError

if __name__ == "__main__":
    print(find_devices(22.0))
