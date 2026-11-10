coffee_price = 4500
coffee_count = 2
sandwich_price = 6200
sandwich_count = 1
discount = 1000
balance = 14000
is_member = True
benefit_threshold = 15000

coffee_amount = coffee_price * coffee_count
sandwich_amount = sandwich_price * sandwich_count
subtotal = coffee_amount + sandwich_amount
payment = subtotal - discount

can_pay = balance >= payment
eligible_for_benefit = is_member and subtotal >= benefit_threshold

print("주문 금액:", subtotal)
print("할인 금액:", discount)
print("결제 예정 금액:", payment)
print("결제 가능:", can_pay)
print("회원 혜택 대상:", eligible_for_benefit)
