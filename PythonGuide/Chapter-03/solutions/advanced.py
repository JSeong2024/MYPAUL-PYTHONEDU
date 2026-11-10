coffee_price = 4800
cookie_price = 2500
discount = 1000

coffee_quantity = int(input("커피 수량: "))
cookie_quantity = int(input("쿠키 수량: "))
received = int(input("받은 돈(원): "))

coffee_total = coffee_price * coffee_quantity
cookie_total = cookie_price * cookie_quantity
subtotal = coffee_total + cookie_total
payment = subtotal - discount
change = received - payment

print("--------------------")
print(f"커피: {coffee_total:,}원")
print(f"쿠키: {cookie_total:,}원")
print(f"주문 금액: {subtotal:,}원")
print(f"할인: {discount:,}원")
print(f"결제 금액: {payment:,}원")
print(f"받은 돈: {received:,}원")
print(f"거스름돈: {change:,}원")
