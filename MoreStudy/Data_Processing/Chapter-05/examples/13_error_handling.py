import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def load_products(path: Path):
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise ValueError("상품 파일을 찾을 수 없습니다.") from exc
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("상품 파일의 인코딩 또는 JSON 형식을 확인하세요.") from exc
    if not isinstance(data, dict) or not isinstance(data.get("products"), list):
        raise ValueError("상품 목록(products)이 필요합니다.")
    return data["products"]

products = load_products(root / "data" / "products.json")
print("Valid products:", len(products))
