"""컴프리헨션으로 데이터 추출과 간단한 변환."""

readings = [18, 21, 27, 19, 30]
hot = [value for value in readings if value >= 25]
celsius_to_fahrenheit = [round(value * 9 / 5 + 32, 1) for value in hot]

products = [
    {"name": "노트", "price": 2500},
    {"name": "연필", "price": 800},
    {"name": "파일", "price": 1500},
]
price_by_name = {item["name"]: item["price"] for item in products}

print("고온 측정값:", hot)
print("화씨 변환:", celsius_to_fahrenheit)
print("상품 가격:", price_by_name)
