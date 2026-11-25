# Chapter 05. Solutions

**조건문 종합 실습 풀이**

## Exercise 01. 결제 가능 여부 확인하기

```python
price = 7_300
paid = 7_299

if paid >= price:
    print("결제할 수 있습니다.")
else:
    print(f"{price - paid:,}원이 부족합니다.")
```

받은 돈이 결제 금액과 같을 때도 결제할 수 있으므로 `>=`를 사용합니다.

## Exercise 02. 주문 금액에 따라 할인율 정하기

```python
total = 30_000

if total >= 30_000:
    rate = 10
elif total >= 10_000:
    rate = 5
else:
    rate = 0

print(f"할인율: {rate}%")
```

9,999원, 10,000원, 29,999원, 30,000원을 넣으면 각각 0%, 5%, 5%, 10%가 출력됩니다. 30,000원은 두 조건을 모두 만족하므로 높은 할인율을 먼저 검사합니다.

## Exercise 03. 회원 할인 확인하기

```python
is_member = False
total = 12_000

if is_member and total >= 10_000:
    print("회원 할인을 적용합니다.")
else:
    print("회원 할인을 적용하지 않습니다.")
```

금액 조건은 참이지만 회원 조건은 거짓입니다. 두 조건이 모두 참일 때만 할인을 적용합니다.

## Mini Project. 카페 주문 접수하기

```python
menu = {"커피": 4800, "쿠키": 2500, "차": 3000}

item = input("메뉴: ")
quantity = int(input("수량: "))
paid = int(input("받은 돈: "))

if item not in menu:
    print("판매하지 않는 메뉴입니다.")
elif quantity < 1:
    print("수량은 1 이상이어야 합니다.")
else:
    total = menu[item] * quantity

    if total >= 30_000:
        rate = 10
    elif total >= 10_000:
        rate = 5
    else:
        rate = 0

    discount = total * rate // 100
    price = total - discount
    print(f"결제 금액: {price:,}원")

    if paid >= price:
        print(f"결제 완료. 거스름돈: {paid - price:,}원")
    else:
        print(f"{price - paid:,}원이 부족합니다.")
```

메뉴와 수량을 확인한 뒤에만 가격을 조회합니다. 커피 3잔의 주문 금액은 14,400원이고 5% 할인액은 720원입니다. 결제 금액은 13,680원이므로 15,000원을 받으면 1,320원을 돌려줍니다.

<p align="center">
  <a href="../Practice.md">← Exercise &amp; Mini Project</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Chapter 05</a>
</p>
