import sqlite3

def find_devices(minimum: float) -> list[str]:
    conn = sqlite3.connect(":memory:")
    try:
        with conn:
            conn.execute("CREATE TABLE sensors (sensor_id TEXT PRIMARY KEY, temperature REAL)")
            conn.executemany("INSERT INTO sensors VALUES (?, ?)", [
                ("ST-01", 22.5), ("ST-02", 26.0), ("ST-03", 20.5),
            ])
            rows = conn.execute(
                "SELECT sensor_id FROM sensors WHERE temperature >= ? ORDER BY sensor_id", (minimum,)
            ).fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()

if __name__ == "__main__":
    print(find_devices(22.0))
