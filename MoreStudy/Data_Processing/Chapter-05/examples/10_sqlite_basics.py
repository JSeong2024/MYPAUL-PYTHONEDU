import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as conn, conn:
    conn.execute("CREATE TABLE sensors (sensor_id TEXT PRIMARY KEY, temperature REAL)")
    conn.executemany(
        "INSERT INTO sensors VALUES (?, ?)",
        [("ST-01", 22.5), ("ST-02", 26.0), ("ST-03", 20.5)],
    )
    threshold = 23.0
    rows = conn.execute(
        "SELECT sensor_id, temperature FROM sensors WHERE temperature >= ? ORDER BY sensor_id",
        (threshold,),
    ).fetchall()
print("Matched:", len(rows))
print("Sensors:", ", ".join(item[0] for item in rows))
