# Chapter 07. Practice

## Exercise 01. 안내 문구를 출력하는 함수

아래 시작 코드에 인수를 받지 않는 `show_menu()`를 정의하세요. 함수 안에서 메뉴 한 줄을 출력하고, 함수 밖에서 두 번 호출하세요.

```python
menu_line = "계산기에서 사용할 연산자: +, -, *, /"

# show_menu()를 정의하고 두 번 호출하세요.
```

**실행 결과**

```text
계산기에서 사용할 연산자: +, -, *, /
계산기에서 사용할 연산자: +, -, *, /
```

## Exercise 02. 단가와 수량을 인수로 넘기기

`print_subtotal()`가 단가와 수량을 매개변수로 받아 금액을 출력하도록 완성하세요. 함수 안에서 값을 다시 입력받을 필요는 없습니다.

```python
def print_subtotal(price, quantity):
    pass


print_subtotal(4800, 3)
print_subtotal(2500, 2)
```

**실행 결과**

```text
주문 금액: 14,400원
주문 금액: 5,000원
```

## Exercise 03. 반환값으로 거스름돈 계산하기

`calculate_change()`를 호출하면 함수 안에서 거스름돈이 먼저 출력되지만, 바깥에 있는 `result`에는 `None`이 들어갑니다. 함수 안에서 거스름돈을 반환하도록 고치세요. 거스름돈 출력은 함수 밖에서 한 번만 해야 합니다. 받은 돈은 결제 금액 이상이라고 가정합니다.

```python
def calculate_change(paid, price):
    print(paid - price)


result = calculate_change(15_000, 13_680)
print(f"거스름돈: {result}원")
```

**수정 후 실행 결과**

```text
거스름돈: 1320원
```

## Mini Project. 사칙연산 계산기 만들기

첫 번째 정수, 연산자, 두 번째 정수를 순서대로 입력받아 계산 결과를 출력하세요. 두 숫자에는 정수가 입력된다고 가정합니다.

**시작 코드**

```python
def calculate(left, operator, right):
    pass


left = int(input("첫 번째 정수: "))
operator = input("연산자 (+, -, *, /): ")
right = int(input("두 번째 정수: "))

# 연산자와 두 번째 정수를 확인한 뒤 calculate()를 호출하세요.
```

1. `calculate(left, operator, right)`에서 `+`, `-`, `*`, `/`에 맞는 계산 결과를 반환한다.
2. 함수 밖에서 연산자를 확인한다. 지원하지 않는 연산자이면 `지원하지 않는 연산자입니다.`를 출력한다.
3. 연산자가 `/`이고 두 번째 정수가 0이면 `0으로 나눌 수 없습니다.`를 출력한다.
4. 계산할 수 있는 경우에만 `calculate()`를 호출하고, 반환값을 화면에 출력한다.

**실행 예시**

```text
첫 번째 정수: 12
연산자 (+, -, *, /): *
두 번째 정수: 3
계산 결과: 36
```

뺄셈은 입력 순서에 따라 결과가 달라집니다. `3 - 12`의 결과는 `-9`입니다. `12 / 3`은 `4.0`으로 출력되며, `12 / 0`에는 오류 안내가 나와야 합니다.

> `pass`는 아무 일도 하지 않는 문장입니다. 함수 내용을 채울 때는 `pass`를 필요한 코드로 바꾸세요.

### 응용. 곱셈을 별도 함수로 나누기

`multiply(left, right)`를 별도로 정의하고, `calculate()`의 곱셈 분기에서 그 함수를 호출하세요. 안쪽 함수가 돌려준 값을 바깥으로 다시 반환하는지 확인하세요.

<p align="center">
  <a href="./7.6.Organizing-Code-with-Functions.md">← 7.6. Organizing Code with Functions</a>
  &nbsp;·&nbsp;
  <a href="./README.md">Chapter 07</a>
  &nbsp;·&nbsp;
  <a href="./solutions/README.md">Solutions →</a>
</p>
