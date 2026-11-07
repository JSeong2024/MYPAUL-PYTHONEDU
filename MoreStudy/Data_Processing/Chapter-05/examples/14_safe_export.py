import csv
import os
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
destination = root / "output" / "status_report.csv"
destination.parent.mkdir(parents=True, exist_ok=True)

# 같은 디렉터리에 임시 파일을 만든 뒤 교체합니다.
temp_name = None
try:
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=destination.parent,
        prefix=".status_", suffix=".tmp", delete=False,
    ) as file:
        temp_name = file.name
        writer = csv.writer(file)
        writer.writerow(["state", "count"])
        writer.writerow(["completed", 10])
        writer.writerow(["canceled", 2])
    os.replace(temp_name, destination)
finally:
    if temp_name is not None and os.path.exists(temp_name):
        os.unlink(temp_name)
print("Saved:", destination.name)
