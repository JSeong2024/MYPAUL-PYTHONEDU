# Chapter 07. Solutions

## Exercise 01. 안내 문구를 출력하는 함수

**완성 코드**

```python
menu_line = "계산기에서 사용할 연산자: +, -, *, /"


def show_menu():
    print(menu_line)


show_menu()
show_menu()
```

**실행 결과**

```text
계산기에서 사용할 연산자: +, -, *, /
계산기에서 사용할 연산자: +, -, *, /
```

7.2절에서 배운 것처럼 함수는 한 번 정의해 두면 필요한 만큼 호출할 수 있습니다. `show_menu()`를 두 번 호출하므로 함수 내부의 `print()`가 두 번 실행되어 같은 안내 문구가 출력됩니다.

`menu_line`은 함수 외부에 정의된 전역 변수입니다. `show_menu()` 함수 내부에는 같은 이름의 지역 변수가 없으므로 전역 변수 `menu_line`에 저장된 문자열을 참조할 수 있습니다.

> 7.5절에서 살펴본 것처럼 함수 내부에서 전역 변수의 값을 참조할 때는 `global` 키워드를 사용할 필요가 없습니다.

## Exercise 02. 단가와 수량을 인수로 넘기기

**완성 코드**

```python
def print_subtotal(price, quantity):
    print(f"주문 금액: {price * quantity:,}원")


print_subtotal(4800, 3)
print_subtotal(2500, 2)
```

**실행 결과**

```text
주문 금액: 14,400원
주문 금액: 5,000원
```

7.3절에서 배운 위치 인수 전달 방식에 따라 첫 번째 인수는 매개변수 `price`에, 두 번째 인수는 매개변수 `quantity`에 전달됩니다.

함수를 호출할 때마다 단가와 수량을 전달받아 주문 금액을 계산하고 출력합니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">호출 코드</th>
      <th align="center">단가(원)</th>
      <th align="center">수량(개)</th>
      <th align="center">주문 금액(원)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><code>print_subtotal(4800, 3)</code></td>
      <td align="right">4,800</td>
      <td align="right">3</td>
      <td align="right">14,400</td>
    </tr>
    <tr>
      <td align="center"><code>print_subtotal(2500, 2)</code></td>
      <td align="right">2,500</td>
      <td align="right">2</td>
      <td align="right">5,000</td>
    </tr>
  </tbody>
</table>

f-문자열의 `{price * quantity:,}`에서 `price * quantity`는 주문 금액을 계산하는 표현식이며, `:,`는 계산 결과에 천 단위 쉼표를 표시하는 형식 지정자입니다.

> f-문자열에는 변수뿐만 아니라 연산을 포함한 표현식도 작성할 수 있습니다. 형식 지정자는 계산 결과의 출력 형태를 변경할 뿐, 원래 숫자 값에는 영향을 주지 않습니다.

## Exercise 03. 반환값으로 거스름돈 계산하기

**완성 코드**

```python
def calculate_change(paid, price):
    return paid - price


result = calculate_change(15_000, 13_680)
print(f"거스름돈: {result}원")
```

**실행 결과**

```text
거스름돈: 1320원
```

7.4절에서 배운 것처럼 `print()`는 값을 화면에 출력하고, `return`은 값을 호출한 곳으로 반환합니다.

기존 코드에서는 함수 내부에서 계산한 거스름돈을 출력했지만, 값을 반환하지 않았으므로 `result` 변수에는 `None`이 저장되었습니다.

`print(paid - price)`를 `return paid - price`로 변경하면 계산 결과를 함수 외부에서도 사용할 수 있습니다.

수정한 프로그램의 실행 순서는 다음과 같습니다.

1. `calculate_change(15_000, 13_680)`을 호출합니다.
2. 매개변수 `paid`와 `price`에 각각 `15000`과 `13680`이 전달됩니다.
3. `paid - price`를 계산하여 거스름돈인 `1320`을 구합니다.
4. `return`을 통해 계산 결과를 반환합니다.
5. 반환값 `1320`이 `result` 변수에 저장됩니다.
6. 함수 외부의 `print()`를 통해 거스름돈을 출력합니다.

이처럼 계산과 출력을 분리하면 함수에서 반환한 값을 다른 연산에 활용하거나 필요한 형식으로 출력할 수 있습니다.

## Mini Project. 사칙연산 계산기 만들기

### 완성 코드

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

### 코드 해설

이 프로그램은 사용자 입력 및 입력값 검사, 사칙연산 수행, 결과 출력의 세 가지 작업으로 구성됩니다.

**1. 사용자 입력 및 입력값 검사**

함수 외부에서 첫 번째 정수, 연산자, 두 번째 정수를 순서대로 입력받습니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">변수</th>
      <th align="center">자료형</th>
      <th align="center">역할</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><code>left</code></td>
      <td align="center"><code>int</code></td>
      <td align="left">첫 번째 정수를 저장합니다.</td>
    </tr>
    <tr>
      <td align="center"><code>operator</code></td>
      <td align="center"><code>str</code></td>
      <td align="left">사용자가 입력한 연산자를 저장합니다.</td>
    </tr>
    <tr>
      <td align="center"><code>right</code></td>
      <td align="center"><code>int</code></td>
      <td align="left">두 번째 정수를 저장합니다.</td>
    </tr>
    <tr>
      <td align="center"><code>result</code></td>
      <td align="center"><code>int</code> 또는 <code>float</code></td>
      <td align="left">함수가 반환한 계산 결과를 저장합니다.</td>
    </tr>
  </tbody>
</table>

입력받은 값은 다음 조건에 따라 검사합니다.

- `operator not in ["+", "-", "*", "/"]`: 지원하지 않는 연산자인지 확인합니다.
- `operator == "/" and right == 0`: 나눗셈을 수행하면서 나누는 수가 `0`인지 확인합니다.

두 조건에 모두 해당하지 않는 경우에만 `calculate()` 함수를 호출합니다.

> `right == 0`이라는 조건만 검사하면 `12 + 0`이나 `12 * 0`과 같은 정상적인 연산도 수행할 수 없습니다. 따라서 연산자가 `"/"`이고 두 번째 정수가 `0`인 경우에만 나눗셈을 제한해야 합니다.

**2. 사칙연산 수행**

`calculate()` 함수는 두 정수와 연산자를 매개변수로 전달받습니다. `if-elif-else` 문을 사용하여 연산자에 알맞은 계산을 수행하고 결과를 반환합니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">연산자</th>
      <th align="center">실행되는 코드</th>
      <th align="center">반환값의 자료형</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><code>+</code></td>
      <td align="center"><code>return left + right</code></td>
      <td align="center"><code>int</code></td>
    </tr>
    <tr>
      <td align="center"><code>-</code></td>
      <td align="center"><code>return left - right</code></td>
      <td align="center"><code>int</code></td>
    </tr>
    <tr>
      <td align="center"><code>*</code></td>
      <td align="center"><code>return left * right</code></td>
      <td align="center"><code>int</code></td>
    </tr>
    <tr>
      <td align="center"><code>/</code></td>
      <td align="center"><code>return left / right</code></td>
      <td align="center"><code>float</code></td>
    </tr>
  </tbody>
</table>

함수를 호출하기 전에 연산자의 유효성을 검사했으므로 `calculate()` 함수 내부의 마지막 `else` 블록에는 연산자가 `"/"`인 경우에만 도달합니다.

`return` 문이 실행되면 계산 결과를 반환하고 함수의 실행을 종료합니다.

**3. 결과 출력**

함수에서 반환한 계산 결과를 `result` 변수에 저장하고, 함수 외부에서 `print()`를 사용하여 출력합니다.

계산을 수행하는 함수와 입출력을 처리하는 코드를 분리했으므로 `calculate()` 함수는 사용자 입력 없이도 독립적으로 호출할 수 있습니다. 예를 들어 `calculate(12, "*", 3)`을 호출하면 계산 결과인 `36`을 반환합니다.

### 프로그램 검증하기

Practice 문서에서 제시한 입력값으로 프로그램을 검증하면 다음과 같은 결과를 확인할 수 있습니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">번호</th>
      <th align="center">첫 번째 정수</th>
      <th align="center">연산자</th>
      <th align="center">두 번째 정수</th>
      <th align="center">출력 결과</th>
      <th align="center"><code>calculate()</code> 호출 여부</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">1</td>
      <td align="right">12</td>
      <td align="center"><code>+</code></td>
      <td align="right">3</td>
      <td align="left">계산 결과: 15</td>
      <td align="center">예</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td align="right">3</td>
      <td align="center"><code>-</code></td>
      <td align="right">12</td>
      <td align="left">계산 결과: -9</td>
      <td align="center">예</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td align="right">12</td>
      <td align="center"><code>*</code></td>
      <td align="right">3</td>
      <td align="left">계산 결과: 36</td>
      <td align="center">예</td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td align="right">12</td>
      <td align="center"><code>/</code></td>
      <td align="right">3</td>
      <td align="left">계산 결과: 4.0</td>
      <td align="center">예</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td align="right">7</td>
      <td align="center"><code>/</code></td>
      <td align="right">2</td>
      <td align="left">계산 결과: 3.5</td>
      <td align="center">예</td>
    </tr>
    <tr>
      <td align="center">6</td>
      <td align="right">-4</td>
      <td align="center"><code>+</code></td>
      <td align="right">9</td>
      <td align="left">계산 결과: 5</td>
      <td align="center">예</td>
    </tr>
    <tr>
      <td align="center">7</td>
      <td align="right">12</td>
      <td align="center"><code>*</code></td>
      <td align="right">0</td>
      <td align="left">계산 결과: 0</td>
      <td align="center">예</td>
    </tr>
    <tr>
      <td align="center">8</td>
      <td align="right">0</td>
      <td align="center"><code>/</code></td>
      <td align="right">3</td>
      <td align="left">계산 결과: 0.0</td>
      <td align="center">예</td>
    </tr>
    <tr>
      <td align="center">9</td>
      <td align="right">12</td>
      <td align="center"><code>/</code></td>
      <td align="right">0</td>
      <td align="left">0으로 나눌 수 없습니다.</td>
      <td align="center">아니요</td>
    </tr>
    <tr>
      <td align="center">10</td>
      <td align="right">12</td>
      <td align="center"><code>%</code></td>
      <td align="right">3</td>
      <td align="left">지원하지 않는 연산자입니다.</td>
      <td align="center">아니요</td>
    </tr>
    <tr>
      <td align="center">11</td>
      <td align="right">12</td>
      <td align="center"><code>%</code></td>
      <td align="right">0</td>
      <td align="left">지원하지 않는 연산자입니다.</td>
      <td align="center">아니요</td>
    </tr>
    <tr>
      <td align="center">12</td>
      <td align="right">12</td>
      <td align="center">빈 문자열</td>
      <td align="right">3</td>
      <td align="left">지원하지 않는 연산자입니다.</td>
      <td align="center">아니요</td>
    </tr>
  </tbody>
</table>

9번부터 12번까지는 함수 외부의 조건문에서 잘못된 입력을 확인하므로 `calculate()` 함수가 호출되지 않습니다.

11번의 경우 두 번째 정수가 `0`이지만, 지원하지 않는 연산자인지를 먼저 검사하므로 `지원하지 않는 연산자입니다.`가 출력됩니다.

> 이 프로그램은 두 수에 올바른 정수가 입력된다고 가정합니다. 정수로 변환할 수 없는 문자열을 입력하면 `int()`에서 `ValueError`가 발생합니다.

### 응용 풀이

7.6.1절에서 배운 것처럼 함수 내부에서 다른 함수를 호출하고, 그 반환값을 다시 반환할 수 있습니다.

곱셈 연산을 담당하는 `multiply()` 함수를 별도로 정의합니다.

```python
def multiply(left, right):
    return left * right
```

이어서 `calculate()` 함수에서 곱셈을 수행하는 부분을 `return multiply(left, right)`로 변경합니다.

**완성 코드**

```python
def multiply(left, right):
    return left * right


def calculate(left, operator, right):
    if operator == "+":
        return left + right
    elif operator == "-":
        return left - right
    elif operator == "*":
        return multiply(left, right)
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

**실행 예시**

```text
첫 번째 정수: 12
연산자 (+, -, *, /): *
두 번째 정수: 3
계산 결과: 36
```

곱셈을 수행할 때의 실행 순서는 다음과 같습니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">순서</th>
      <th align="center">실행 흐름</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">1</td>
      <td align="left"><code>calculate(12, "*", 3)</code>을 호출합니다.</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td align="left">연산자가 <code>"*"</code>이므로 <code>multiply(12, 3)</code>을 호출합니다.</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td align="left"><code>multiply()</code> 함수가 두 수의 곱인 <code>36</code>을 반환합니다.</td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td align="left"><code>calculate()</code> 함수가 전달받은 값 <code>36</code>을 다시 반환합니다.</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td align="left">반환값 <code>36</code>이 <code>result</code> 변수에 저장됩니다.</td>
    </tr>
    <tr>
      <td align="center">6</td>
      <td align="left">함수 외부에서 계산 결과를 출력합니다.</td>
    </tr>
  </tbody>
</table>

기존 프로그램과 비교하면 곱셈을 수행하는 코드가 별도의 함수로 분리되었을 뿐, 사용자 입력 방식과 출력 결과는 달라지지 않습니다.

`multiply()` 함수는 곱셈을 수행하고, `calculate()` 함수는 연산자에 따라 계산 방법을 선택하는 역할을 담당합니다. 이처럼 기능에 따라 함수를 나누면 각 기능을 독립적으로 관리하고 재사용할 수 있습니다.

> `calculate()` 함수 내부에서 `multiply()`를 호출할 때는 해당 함수가 이미 정의되어 있어야 합니다. 다만 반드시 `calculate()`의 정의보다 위에 작성해야 하는 것은 아니며, 실제로 호출되는 시점까지 정의되어 있으면 됩니다.

<p align="center">
  <a href="../Practice.md">← Exercise &amp; Mini Project</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Chapter 07</a>
</p>
