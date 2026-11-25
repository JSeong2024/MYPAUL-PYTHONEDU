# Chapter 07. Practice

## Exercise 01. 안내 문구를 출력하는 함수

매개변수가 없는 `show_menu()` 함수를 정의하고, 함수를 여러 번 호출하여 같은 안내 문구를 출력하는 프로그램을 작성하세요.

**시작 코드**

```python
menu_line = "계산기에서 사용할 연산자: +, -, *, /"

# show_menu()를 정의하고 두 번 호출하세요.
```

**요구사항**

1. 매개변수가 없는 `show_menu()` 함수를 정의합니다.
2. 함수 내부에서 전역 변수 `menu_line`에 저장된 안내 문구를 출력합니다.
3. 함수 외부에서 `show_menu()`를 두 번 호출합니다.

**실행 결과**

```text
계산기에서 사용할 연산자: +, -, *, /
계산기에서 사용할 연산자: +, -, *, /
```

## Exercise 02. 단가와 수량을 인수로 넘기기

상품의 단가와 주문 수량을 전달받아 주문 금액을 계산하고 출력하는 `print_subtotal()` 함수를 완성하세요.

**시작 코드**

```python
def print_subtotal(price, quantity):
    pass


print_subtotal(4800, 3)
print_subtotal(2500, 2)
```

**요구사항**

1. 매개변수 `price`와 `quantity`를 사용하여 주문 금액을 계산합니다.
2. 계산한 주문 금액을 함수 내부에서 출력합니다.
3. 주문 금액에는 천 단위 쉼표를 표시합니다.

**실행 결과**

```text
주문 금액: 14,400원
주문 금액: 5,000원
```

> 숫자에 천 단위 쉼표를 표시하려면 f-문자열의 형식 지정자 `:,`를 활용하세요. 함수에 필요한 값은 인수로 전달되므로 함수 내부에서 `input()`을 사용할 필요가 없습니다.

> 시작 코드에 작성된 `pass`는 아무런 동작도 수행하지 않는 키워드입니다. 아직 구현하지 않은 함수의 문법적 구조를 유지할 때 사용할 수 있으며, 함수를 완성할 때는 `pass`를 삭제하고 필요한 코드로 대체하세요.

## Exercise 03. 반환값으로 거스름돈 계산하기

다음 프로그램은 받은 돈에서 결제 금액을 빼 거스름돈을 계산합니다. 현재 코드는 함수 내부에서 거스름돈을 출력하지만, 계산 결과를 반환하지 않으므로 `result` 변수에는 `None`이 저장됩니다.

함수에서 계산한 거스름돈을 반환하고, 함수 외부에서 결과를 출력하도록 프로그램을 수정하세요.

받은 돈(`paid`)은 항상 결제 금액(`price`) 이상이라고 가정합니다.

**시작 코드**

```python
def calculate_change(paid, price):
    print(paid - price)


result = calculate_change(15_000, 13_680)
print(f"거스름돈: {result}원")
```

**수정 전 실행 결과**

```text
1320
거스름돈: None원
```

**요구사항**

1. `calculate_change()` 함수가 계산한 거스름돈을 반환하도록 수정합니다.
2. 반환값을 `result` 변수에 저장합니다.
3. 거스름돈은 함수 외부에서 한 번만 출력합니다.

**수정 후 실행 결과**

```text
거스름돈: 1320원
```

## Mini Project. 사칙연산 계산기 만들기

첫 번째 정수, 연산자, 두 번째 정수를 순서대로 입력받아 사칙연산 결과를 출력하는 계산기 프로그램을 작성하세요.

계산 기능은 `calculate()` 함수로 구성하고, 사용자 입력과 입력값 검사, 결과 출력은 함수 외부에서 처리합니다.

두 수에는 항상 올바른 정수가 입력된다고 가정합니다.

### 시작 코드

```python
def calculate(left, operator, right):
    pass


left = int(input("첫 번째 정수: "))
operator = input("연산자 (+, -, *, /): ")
right = int(input("두 번째 정수: "))

# 연산자와 두 번째 정수를 확인한 뒤 calculate()를 호출하세요.
```

### 요구사항

1. `calculate()` 함수는 두 정수와 연산자를 전달받아 해당 연산의 계산 결과를 반환합니다.
2. 다음 네 가지 연산을 지원합니다.

   <table align="center">
     <thead>
       <tr>
         <th align="center">연산자</th>
         <th align="center">연산</th>
         <th align="center">계산식</th>
       </tr>
     </thead>
     <tbody>
       <tr>
         <td align="center"><code>+</code></td>
         <td align="left">덧셈</td>
         <td align="center"><code>left + right</code></td>
       </tr>
       <tr>
         <td align="center"><code>-</code></td>
         <td align="left">뺄셈</td>
         <td align="center"><code>left - right</code></td>
       </tr>
       <tr>
         <td align="center"><code>*</code></td>
         <td align="left">곱셈</td>
         <td align="center"><code>left * right</code></td>
       </tr>
       <tr>
         <td align="center"><code>/</code></td>
         <td align="left">나눗셈</td>
         <td align="center"><code>left / right</code></td>
       </tr>
     </tbody>
   </table>

3. 지원하지 않는 연산자를 입력하면 `지원하지 않는 연산자입니다.`를 출력합니다.
4. 연산자가 `/`이고 두 번째 정수(`right`)가 `0`이면 `0으로 나눌 수 없습니다.`를 출력합니다.
5. 정상적으로 계산할 수 있는 경우에만 `calculate()` 함수를 호출합니다.
6. 함수의 반환값을 사용하여 `계산 결과: 값` 형식으로 출력합니다.

> `calculate()` 함수는 계산 결과를 반환하는 역할만 담당합니다. 사용자 입력, 입력값 검사, 결과 출력은 함수 외부에서 처리하세요.

### 실행 예시

**실행 예시 1 — 정상적인 연산**

```text
첫 번째 정수: 12
연산자 (+, -, *, /): *
두 번째 정수: 3
계산 결과: 36
```

**실행 예시 2 — 지원하지 않는 연산자**

```text
첫 번째 정수: 12
연산자 (+, -, *, /): %
두 번째 정수: 3
지원하지 않는 연산자입니다.
```

**실행 예시 3 — 0으로 나누는 경우**

```text
첫 번째 정수: 12
연산자 (+, -, *, /): /
두 번째 정수: 0
0으로 나눌 수 없습니다.
```

### 프로그램 검증하기

프로그램을 완성한 뒤 다음 입력값을 사용하여 사칙연산이 정상적으로 수행되는지 확인하세요. 지원하지 않는 연산자를 입력하거나 `0`으로 나누려고 할 때도 적절한 안내 문구가 출력되어야 합니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">번호</th>
      <th align="center">첫 번째 정수</th>
      <th align="center">연산자</th>
      <th align="center">두 번째 정수</th>
      <th align="center">예상 출력</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">1</td>
      <td align="right">12</td>
      <td align="center"><code>+</code></td>
      <td align="right">3</td>
      <td align="left">계산 결과: 15</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td align="right">3</td>
      <td align="center"><code>-</code></td>
      <td align="right">12</td>
      <td align="left">계산 결과: -9</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td align="right">12</td>
      <td align="center"><code>*</code></td>
      <td align="right">3</td>
      <td align="left">계산 결과: 36</td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td align="right">12</td>
      <td align="center"><code>/</code></td>
      <td align="right">3</td>
      <td align="left">계산 결과: 4.0</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td align="right">7</td>
      <td align="center"><code>/</code></td>
      <td align="right">2</td>
      <td align="left">계산 결과: 3.5</td>
    </tr>
    <tr>
      <td align="center">6</td>
      <td align="right">-4</td>
      <td align="center"><code>+</code></td>
      <td align="right">9</td>
      <td align="left">계산 결과: 5</td>
    </tr>
    <tr>
      <td align="center">7</td>
      <td align="right">12</td>
      <td align="center"><code>*</code></td>
      <td align="right">0</td>
      <td align="left">계산 결과: 0</td>
    </tr>
    <tr>
      <td align="center">8</td>
      <td align="right">0</td>
      <td align="center"><code>/</code></td>
      <td align="right">3</td>
      <td align="left">계산 결과: 0.0</td>
    </tr>
    <tr>
      <td align="center">9</td>
      <td align="right">12</td>
      <td align="center"><code>/</code></td>
      <td align="right">0</td>
      <td align="left">0으로 나눌 수 없습니다.</td>
    </tr>
    <tr>
      <td align="center">10</td>
      <td align="right">12</td>
      <td align="center"><code>%</code></td>
      <td align="right">3</td>
      <td align="left">지원하지 않는 연산자입니다.</td>
    </tr>
    <tr>
      <td align="center">11</td>
      <td align="right">12</td>
      <td align="center"><code>%</code></td>
      <td align="right">0</td>
      <td align="left">지원하지 않는 연산자입니다.</td>
    </tr>
    <tr>
      <td align="center">12</td>
      <td align="right">12</td>
      <td align="center">빈 문자열</td>
      <td align="right">3</td>
      <td align="left">지원하지 않는 연산자입니다.</td>
    </tr>
  </tbody>
</table>

> 두 정수를 `/` 연산자로 나누면 결과가 정수로 나누어떨어지더라도 실수형(`float`)으로 반환됩니다. 또한 두 번째 정수가 `0`이라고 해서 항상 오류가 발생하는 것은 아닙니다. 나눗셈을 수행할 때만 `0`으로 나누는 상황을 검사해야 합니다.

### 응용. 곱셈을 별도 함수로 나누기

곱셈 연산을 담당하는 `multiply(left, right)` 함수를 별도로 정의하고, `calculate()` 함수에서 곱셈이 필요한 경우 해당 함수를 호출하도록 프로그램을 수정하세요.

**추가 요구사항**

1. 두 수의 곱을 계산하여 반환하는 `multiply()` 함수를 정의합니다.
2. `calculate()` 함수에서 연산자가 `*`이면 `multiply()` 함수를 호출합니다.
3. `multiply()` 함수의 반환값을 `calculate()` 함수에서 다시 반환합니다.
4. 기존 사칙연산 기능과 입력값 검사, 출력 형식은 그대로 유지합니다.

수정한 프로그램을 실행하여 기존 프로그램과 동일한 결과가 출력되는지 확인하세요.

> 함수를 여러 개로 나누더라도 프로그램의 실행 결과는 달라지지 않아야 합니다. 7.6.1절에서 살펴본 것처럼 다른 함수가 반환한 값을 다시 반환하여 함수 간에 계산 결과를 전달할 수 있습니다.

<p align="center">
  <a href="./7.6.Organizing-Code-with-Functions.md">← 7.6. Organizing Code with Functions</a>
  &nbsp;·&nbsp;
  <a href="./README.md">Chapter 07</a>
  &nbsp;·&nbsp;
  <a href="./solutions/README.md">Solutions →</a>
</p>
