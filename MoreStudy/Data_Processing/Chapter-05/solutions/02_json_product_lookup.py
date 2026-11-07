import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "data" / "products.json"

def categories(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as file:
        document = json.load(file)
    return {product["product_id"]: product["category"] for product in document["products"]}

if __name__ == "__main__":
    print(categories(SOURCE))
