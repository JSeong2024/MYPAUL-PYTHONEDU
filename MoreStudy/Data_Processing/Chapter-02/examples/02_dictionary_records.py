"""딕셔너리로 상품 정보를 관리하고 안전하게 조회."""

product = {"product_id": "P-001", "name": "노트", "stock": 12}
product["stock"] -= 3
product["category"] = "문구"

print("상품:", product["name"])
print("재고:", product["stock"])
print("할인율:", product.get("discount_rate", 0))
print("품목:", list(product))

if "category" in product:
    print("분류:", product["category"])

# Key가 없을 수 있다면 `dict.get()`이나 멤버십 검사를 고려합니다.
