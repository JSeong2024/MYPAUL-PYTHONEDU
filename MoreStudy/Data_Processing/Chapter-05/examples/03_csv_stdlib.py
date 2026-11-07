import csv
import io
from pathlib import Path

source = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
with source.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

assert reader.fieldnames is not None
print("Columns:", len(reader.fieldnames))
print("Records:", len(rows))
print("First order:", rows[0]["order_id"])
print("Region code:", rows[0]["region_code"])

# 쉼표와 큰따옴표가 포함된 필드도 올바르게 읽습니다.
sample = 'name,note\n"sensor, A","says ""hello"""\n'
quoted = list(csv.DictReader(io.StringIO(sample)))
print("Quoted name:", quoted[0]["name"])
print("Quoted note:", quoted[0]["note"])
