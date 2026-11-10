product_name = "사과"
unit_price = 1800
quantity = 4
discount = 1000

subtotal = unit_price * quantity
payment = subtotal - discount

print("상품:", product_name)
print("수량:", quantity)
print("할인 전 금액:", subtotal)
print("할인 금액:", discount)
print("결제 금액:", payment)
