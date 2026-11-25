# Chapter 04. Solutions

## Exercise

### 1. 리스트 수정

~~~python
orders = ["커피", "쿠키"]
orders[0] = "차"
orders.append("커피")
print(orders)
~~~

`orders[0]`을 바꾸면 첫 주문이 바뀝니다. 새 주문을 맨 뒤에 추가하면 결과는 `['차', '쿠키', '커피']`입니다.

### 2. 튜플 읽기

~~~python
item = ("샌드위치", 6000)
print(f"{item[0]}: {item[1]:,}원")
~~~

인덱스 0은 메뉴 이름이고 1은 가격입니다. 결과는 `샌드위치: 6,000원`입니다.

### 3. 딕셔너리 수정

~~~python
menu = {"커피": 4800, "쿠키": 2500}
menu["쿠키"] = 2800
menu["차"] = 3000
print(f"쿠키: {menu['쿠키']:,}원")
print(f"차: {menu['차']:,}원")
~~~

기존 키에는 새 가격이 저장되고, 새 키에는 메뉴가 추가됩니다.

### 4. 주문 건수와 메뉴 종류

~~~python
orders = ["커피", "차", "커피", "차", "쿠키"]
print(len(orders))
print(len(set(orders)))
~~~

리스트의 길이는 5이고, 중복을 제거한 집합의 길이는 3입니다.

## Mini Project

~~~python
menu = {"커피": 4800, "쿠키": 2500, "샌드위치": 6000}
orders = ["커피", "쿠키"]

first_item = orders[0]
second_item = orders[1]
first_price = menu[first_item]
second_price = menu[second_item]
total_price = first_price + second_price

print(f"첫 번째 주문: {first_item} {first_price:,}원")
print(f"두 번째 주문: {second_item} {second_price:,}원")
print(f"합계: {total_price:,}원")
print(f"전체 주문: {len(orders)}건")
print(f"메뉴 종류: {len(set(orders))}종")
~~~

같은 메뉴를 두 번 주문하면 두 건의 가격을 모두 더합니다. 메뉴 종류를 셀 때는 집합에서 같은 메뉴를 한 번만 셉니다.

주문 목록을 `["커피", "커피"]`로 바꾸면 합계는 9,600원, 주문은 2건, 메뉴는 1종입니다.

<p align="center">
  <a href="../README.md">← Chapter 04</a>
</p>
