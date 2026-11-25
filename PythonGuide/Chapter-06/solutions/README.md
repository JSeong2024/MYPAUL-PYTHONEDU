# Chapter 06. Solutions

**반복문 종합 실습 풀이**

## Exercise 01. 짝수의 합과 개수 구하기

```python
numbers = [3, 12, 0, 7, 8, 5]
total = 0
count = 0

for number in numbers:
    if number % 2 == 0:
        total += number
        count += 1

print(f"짝수의 합: {total}")
print(f"짝수의 개수: {count}")
```

짝수는 12, 0, 8입니다. 0을 더해도 합계는 그대로지만 개수는 1 늘어납니다. 따라서 합계는 20이고, 개수는 3입니다.

## Exercise 02. 가운데 정렬 피라미드 그리기

```python
height = int(input("높이: "))

for row in range(1, height + 1):
    spaces = height - row
    stars = 2 * row - 1
    print(" " * spaces + "*" * stars)
```

높이가 3이면 첫 줄에는 공백 2칸과 별 1개, 마지막 줄에는 공백 없이 별 5개를 놓습니다. 끝값을 포함하지 않는 `range()`의 규칙에 맞춰 `height + 1`을 끝값으로 씁니다.

## Exercise 03. 영업 시간에 판매할 메뉴 골라 출력하기

```python
menu = {"커피": 4800, "쿠키": 2500, "차": 3000, "주스": 4000}
sold_out = ["쿠키"]

for item, price in menu.items():
    if item in sold_out:
        continue

    if price <= 4000:
        print(f"{item}: {price:,}원")
```

쿠키는 가격 조건을 만족하지만 품절이므로 건너뜁니다. 커피는 4,000원을 넘습니다. 차와 주스는 품절 목록에 없고 가격이 4,000원 이하이므로 출력합니다.

## Mini Project. 카페 주문 금액 집계하기

```python
total = 0
count = 0

while True:
    amount = int(input("주문 금액 (끝내려면 0): "))

    if amount == 0:
        break

    if amount < 0:
        print("양의 금액을 입력하세요.")
        continue

    total += amount
    count += 1

print(f"합계: {total:,}원")
print(f"주문 건수: {count}건")
```

0에서는 입력을 끝냅니다. 음수에서는 더하는 줄을 건너뛰고 반복문의 첫 줄로 돌아가 새 금액을 받습니다. 양수만 합계와 주문 건수에 반영됩니다.

<table align="center">
  <thead>
    <tr><th align="left">입력 순서</th><th align="right">합계</th><th align="right">주문 건수</th></tr>
  </thead>
  <tbody>
    <tr><td align="left">4800 → -100 → 2500 → 0</td><td align="right">7,300원</td><td align="right">2건</td></tr>
    <tr><td align="left">0</td><td align="right">0원</td><td align="right">0건</td></tr>
    <tr><td align="left">-100 → -50 → 0</td><td align="right">0원</td><td align="right">0건</td></tr>
  </tbody>
</table>

<p align="center">
  <a href="../Practice.md">← Exercise &amp; Mini Project</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Chapter 06</a>
</p>
