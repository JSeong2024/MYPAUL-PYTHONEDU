# Chapter 07. Solutions

## Exercise 01. 안내 문구를 출력하는 함수

```python
menu_line = "계산기에서 사용할 연산자: +, -, *, /"


def show_menu():
    print(menu_line)


show_menu()
show_menu()
```

함수는 한 번 정의하고 두 번 호출합니다. 호출할 때마다 같은 안내 문구가 한 줄씩 출력됩니다.

## Exercise 02. 단가와 수량을 인수로 넘기기

```python
def print_subtotal(price, quantity):
    print(f"주문 금액: {price * quantity:,}원")


print_subtotal(4800, 3)
print_subtotal(2500, 2)
```

호출할 때마다 첫 번째 인수는 `price`, 두 번째 인수는 `quantity`에 들어갑니다.

## Exercise 03. 반환값으로 거스름돈 계산하기

```python
def calculate_change(paid, price):
    return paid - price


result = calculate_change(15_000, 13_680)
print(f"거스름돈: {result}원")
```

`return`으로 돌려준 `1320`이 `result`에 저장됩니다. 화면 출력은 함수 밖의 `print()`에서 한 번만 합니다.

## Mini Project. 사칙연산 계산기 만들기

```python
def calculate(left, operator, right):
    if operator == "+":
        return left + right
    elif operator == "-":
        return left - right
    elif operator == "*":
        return left * right
    else:
        return left / right


left = int(input("첫 번째 정수: "))
operator = input("연산자 (+, -, *, /): ")
right = int(input("두 번째 정수: "))

if operator not in ["+", "-", "*", "/"]:
    print("지원하지 않는 연산자입니다.")
elif operator == "/" and right == 0:
    print("0으로 나눌 수 없습니다.")
else:
    result = calculate(left, operator, right)
    print(f"계산 결과: {result}")
```

지원하는 연산자이고 0으로 나누는 경우도 아닐 때만 `calculate()`를 호출합니다. 함수 안에서 앞의 세 분기를 모두 지나면 남은 연산자는 `/`입니다.

### 응용 풀이

`calculate()`보다 위에 `multiply()`를 정의합니다. 곱셈 분기의 `return left * right`는 `return multiply(left, right)`로 바꿉니다.

```python
def multiply(left, right):
    return left * right
```

`multiply(12, 3)`이 반환한 36을 `calculate()`도 그대로 반환하므로 출력은 `계산 결과: 36`입니다.

<p align="center">
  <a href="../Practice.md">← Exercise &amp; Mini Project</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Chapter 07</a>
</p>
