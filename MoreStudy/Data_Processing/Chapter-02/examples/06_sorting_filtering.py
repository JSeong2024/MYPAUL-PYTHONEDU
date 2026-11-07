"""조건 필터링과 복수 기준의 안정적 정렬."""

products = [
    {"name": "노트", "category": "문구", "price": 2500, "stock": 7},
    {"name": "연필", "category": "문구", "price": 800, "stock": 12},
    {"name": "커피", "category": "음료", "price": 2500, "stock": 4},
    {"name": "파일", "category": "문구", "price": 1500, "stock": 9},
]

available = [item for item in products if item["stock"] >= 5]
ranked = sorted(available, key=lambda item: (-item["price"], item["name"]))

print("재고 5개 이상:", len(available), "종")
for item in ranked:
    print(f"{item['name']}: {item['price']:,}원 / {item['stock']}개")

print("원본 첫 번째:", products[0]["name"])
