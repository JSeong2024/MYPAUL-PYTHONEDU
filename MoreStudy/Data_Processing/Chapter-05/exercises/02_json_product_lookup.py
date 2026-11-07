"""Exercise 02: JSON 상품 목록을 상품 ID -> 카테고리 사전으로 바꾸세요."""
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "data" / "products.json"

def categories(path: Path) -> dict[str, str]:
    # TODO: JSON 파일을 UTF-8로 로드합니다.
    # TODO: 각 상품의 product_id를 키, category를 값으로 반환합니다.
    raise NotImplementedError

if __name__ == "__main__":
    print(categories(SOURCE))
