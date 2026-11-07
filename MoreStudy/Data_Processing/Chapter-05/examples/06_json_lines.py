import json
from pathlib import Path

source = Path(__file__).resolve().parents[1] / "data" / "readings.jsonl"
records = []
with source.open("r", encoding="utf-8") as file:
    for line_no, line in enumerate(file, start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSONL {line_no}행 오류") from exc

print("Readings:", len(records))
print("Max temp:", max(item["temperature_c"] for item in records))
