import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "data" / "products.json"
with path.open("r", encoding="utf-8") as file:
    document = json.load(file)

if document.get("schema_version") != 1:
    raise ValueError("지원하지 않는 상품 데이터 버전입니다.")
products = document["products"]
print("Products:", len(products))
print("First:", products[0]["name"])
