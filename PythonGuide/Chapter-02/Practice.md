# Chapter 02. Practice

## Exercise

**Q-01.** 다음 중 Python 변수 이름으로 사용할 수 있는 것은 무엇입니까?

① `2nd_score`  
② `total-price`  
③ `total_price`  
④ `class`

**Q-02.** `price = 1800`의 의미로 올바른 것은 무엇입니까?

① `price`와 `1800`이 같은지 비교한다.  
② `1800`을 `price`라는 이름으로 사용할 수 있게 한다.  
③ `price`를 화면에 출력한다.  
④ `price`를 문자열로 변환한다.

**Q-03.** 다음 코드의 `value`가 가리키는 값의 자료형은 무엇입니까?

```python
value = "12"
```

① `int`　② `float`　③ `str`　④ `bool`


**Q-04.** `17 // 5`의 결과는 무엇입니까?

① `2`　② `3`　③ `3.4`　④ `4`


**Q-05.** Python에서 `=`과 `==`의 차이를 설명하십시오.


**Q-06.** `7 + 3`과 `"7" + "3"`은 각각 어떤 결과를 만드는지 쓰고, 결과가 다른 이유를 설명하십시오.


**Q-07.** 다음 코드의 출력 결과를 작성하십시오.

```python
count = 2
count = count + 3
count *= 2

print(count)
```


**Q-08.** 다음 두 출력 결과를 순서대로 작성하십시오.

```python
print(4 + 2 * 3)
print((4 + 2) * 3)
```


**Q-09.** 다음 코드의 출력 결과를 순서대로 작성하십시오.

```python
stock = 5
requested = 3
is_open = False

print(stock >= requested and is_open)
print(stock >= requested or is_open)
```


**Q-10.** 다음 코드는 상품 가격과 수량을 곱하려고 작성했지만 실행할 수 없습니다. 잘못된 부분을 찾아 수정하십시오.

```python
unit_price = 2500
quantity = 4

total = unit_price x quantity
print(total)
```

## Mini Project

### Basic
#### 1. 상품 구매 금액 계산

상품을 구매할 때 할인 전 금액과 최종 결제 금액을 계산하는 프로그램을 작성합니다.

**주어진 정보**

<table align="center">
  <thead>
    <tr>
      <th align="center">항목</th>
      <th align="center">값</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">상품명</td>
      <td align="center">사과</td>
    </tr>
    <tr>
      <td align="center">단가</td>
      <td align="center">1,800원</td>
    </tr>
    <tr>
      <td align="center">수량</td>
      <td align="center">4개</td>
    </tr>
    <tr>
      <td align="center">할인 금액</td>
      <td align="center">1,000원</td>
    </tr>
  </tbody>
</table>

**요구사항**

1. 상품명, 단가, 수량, 할인 금액을 각각 변수에 저장한다.
2. 할인 전 금액을 `단가 × 수량`으로 계산한다.
3. 최종 결제 금액을 `할인 전 금액 - 할인 금액`으로 계산한다.
4. 상품명, 수량, 할인 전 금액, 할인 금액, 최종 결제 금액을 출력한다.

**예상 출력**

```text
상품: 사과
수량: 4
할인 전 금액: 7200
할인 금액: 1000
결제 금액: 6200
```

**확인할 사항**

- 단가나 수량을 변경하면 계산 결과도 달라지는가?
- 할인 금액을 0으로 바꾸면 결제 금액은 할인 전 금액과 같아지는가?
- 금액 계산에 필요한 숫자를 출력문마다 직접 반복하지 않고 변수를 사용했는가?

### Advanced 
#### 2. 카페 주문 및 결제 가능 여부 확인

카페에서 여러 상품을 주문했습니다. 주문 금액과 할인 적용 후 금액을 계산하고, 보유한 잔액으로 결제할 수 있는지 확인하는 프로그램을 작성합니다.

**주어진 정보**

<table align="center">
  <thead>
    <tr>
      <th align="center">항목</th>
      <th align="center">값</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">커피 단가</td>
      <td align="center">4,500원</td>
    </tr>
    <tr>
      <td align="center">커피 수량</td>
      <td align="center">2잔</td>
    </tr>
    <tr>
      <td align="center">샌드위치 단가</td>
      <td align="center">6,200원</td>
    </tr>
    <tr>
      <td align="center">샌드위치 수량</td>
      <td align="center">1개</td>
    </tr>
    <tr>
      <td align="center">할인 금액</td>
      <td align="center">1,000원</td>
    </tr>
    <tr>
      <td align="center">보유 잔액</td>
      <td align="center">14,000원</td>
    </tr>
    <tr>
      <td align="center">회원 여부</td>
      <td align="center"><code>True</code></td>
    </tr>
    <tr>
      <td align="center">회원 혜택 최소 주문 금액</td>
      <td align="center">15,000원</td>
    </tr>
  </tbody>
</table>

**요구사항**

1. 모든 정보를 변수에 저장한다.
2. 상품별 금액을 계산한 뒤 주문 금액을 구한다.
3. 주문 금액에서 할인 금액을 빼 결제 예정 금액을 구한다.
4. 보유 잔액이 결제 예정 금액 이상인지 비교한다.
5. 회원이면서 **할인 전 주문 금액이 15,000원 이상**인지 논리 연산자로 확인한다.
6. 주문 금액, 할인 금액, 결제 예정 금액, 결제 가능 여부, 회원 혜택 대상 여부를 출력한다.

**예상 출력**

```text
주문 금액: 15200
할인 금액: 1000
결제 예정 금액: 14200
결제 가능: False
회원 혜택 대상: True
```

회원 혜택 대상인지는 확인만 합니다. 혜택에 따라 할인 금액을 바꾸거나 결제를 진행하는 기능은 구현하지 않습니다. 이러한 분기 처리는 Chapter 05의 조건문에서 다룹니다.

**확인할 사항**

- 주문 수량을 변경하면 주문 금액과 결제 예정 금액이 함께 바뀌는가?
- 보유 잔액을 15,000원으로 변경하면 결제 가능 여부가 `True`로 바뀌는가?
- 회원 여부를 `False`로 변경하면 회원 혜택 대상 여부가 `False`로 바뀌는가?
- 비교 연산자와 논리 연산자를 사용해 참·거짓을 판단했는가?


해설은 [Solutions](./solutions/README.md)에서 확인할 수 있습니다.

<p align="center">
  <a href="./2.5.Assignment-Operators-and-Expressions.md">← 2.5. Assignment Operators &amp; Expressions</a>
  &nbsp;·&nbsp;
  <a href="./README.md">Chapter 02</a>
  &nbsp;·&nbsp;
  <a href="./solutions/README.md">Solutions →</a>
</p>
