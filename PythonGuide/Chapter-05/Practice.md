# Chapter 05. Practice

## Exercise 01. 결제 가능 여부 확인하기

손님에게 받은 돈이 결제 금액 이상인지 확인하는 프로그램을 작성하세요. 받은 돈이 충분하면 결제가 가능하다는 안내 문구를 출력하고, 부족하면 결제에 필요한 금액이 얼마나 부족한지 출력합니다.

**시작 코드**

```python
price = 7_300
paid = 7_299
```

**요구사항**

1. 비교 연산자를 사용하여 받은 돈(`paid`)이 결제 금액(`price`) 이상인지 확인합니다.
2. 받은 돈이 충분하면 `결제할 수 있습니다.`를 출력합니다.
3. 받은 돈이 부족하면 결제 금액에서 받은 돈을 빼 부족한 금액을 출력합니다.

**실행 예시 1 — 받은 돈이 7,299원인 경우**

```text
1원이 부족합니다.
```

**실행 예시 2 — 받은 돈이 7,300원인 경우**

```text
결제할 수 있습니다.
```

`paid`의 값을 변경하면서 다음과 같은 결과가 출력되는지 확인하세요.

<table align="center">
  <thead>
    <tr>
      <th align="center">결제 금액(원)</th>
      <th align="center">받은 돈(원)</th>
      <th align="center">실행 결과</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">7,300</td>
      <td align="right">7,299</td>
      <td align="left">1원이 부족합니다.</td>
    </tr>
    <tr>
      <td align="right">7,300</td>
      <td align="right">7,300</td>
      <td align="left">결제할 수 있습니다.</td>
    </tr>
    <tr>
      <td align="right">7,300</td>
      <td align="right">8,000</td>
      <td align="left">결제할 수 있습니다.</td>
    </tr>
  </tbody>
</table>

> 받은 돈과 결제 금액이 같은 경우에도 결제할 수 있습니다. 두 값이 같은 경우를 포함할 수 있도록 적절한 비교 연산자를 사용하세요.

## Exercise 02. 주문 금액에 따라 할인율 정하기

카페에서는 손님의 주문 금액에 따라 서로 다른 할인율을 적용합니다. 주문 금액을 확인하고, 다음 할인 기준에 따라 적용할 할인율을 출력하는 프로그램을 작성하세요.

<table align="center">
  <thead>
    <tr>
      <th align="center">주문 금액</th>
      <th align="center">할인율</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left">30,000원 이상</td>
      <td align="right">10%</td>
    </tr>
    <tr>
      <td align="left">10,000원 이상 30,000원 미만</td>
      <td align="right">5%</td>
    </tr>
    <tr>
      <td align="left">10,000원 미만</td>
      <td align="right">0%</td>
    </tr>
  </tbody>
</table>

**시작 코드**

```python
total = 30_000
```

**요구사항**

1. `if`, `elif`, `else`를 사용하여 주문 금액에 따라 할인율을 구분합니다.
2. 주문 금액이 30,000원 이상이면 10%의 할인율을 적용합니다.
3. 주문 금액이 10,000원 이상 30,000원 미만이면 5%의 할인율을 적용합니다.
4. 주문 금액이 10,000원 미만이면 0%의 할인율을 적용합니다.
5. 결정된 할인율을 출력합니다.

**실행 결과**

```text
10%
```

`total`의 값을 변경하면서 할인율이 올바르게 출력되는지 확인하세요.

<table align="center">
  <thead>
    <tr>
      <th align="center">주문 금액(원)</th>
      <th align="center">예상 할인율</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">9,999</td>
      <td align="right">0%</td>
    </tr>
    <tr>
      <td align="right">10,000</td>
      <td align="right">5%</td>
    </tr>
    <tr>
      <td align="right">29,999</td>
      <td align="right">5%</td>
    </tr>
    <tr>
      <td align="right">30,000</td>
      <td align="right">10%</td>
    </tr>
  </tbody>
</table>

> 조건에 따라 결과가 달라지는 기준값을 **경계값**(**Boundary Value**)이라고 합니다. 이 예제에서는 10,000원과 30,000원이 할인율을 결정하는 경계값입니다. 경계값과 그 주변의 값을 함께 확인하면 비교 연산자나 조건식이 올바르게 작성되었는지 판단하는 데 도움이 됩니다.

## Exercise 03. 회원 할인 확인하기

카페에서는 회원이면서 주문 금액이 10,000원 이상인 손님에게만 회원 할인을 적용합니다. 회원 여부와 주문 금액을 함께 확인하여 할인 적용 여부를 출력하는 프로그램을 작성하세요.

**시작 코드**

```python
is_member = False
total = 12_000
```

**요구사항**

1. `is_member`를 사용하여 손님의 회원 여부를 확인합니다.
2. 주문 금액(`total`)이 10,000원 이상인지 확인합니다.
3. 논리 연산자 `and`를 사용하여 두 조건을 모두 만족하는지 확인합니다.
4. 두 조건을 모두 만족하면 `회원 할인을 적용합니다.`를 출력합니다.
5. 두 조건 중 하나라도 만족하지 않으면 `회원 할인을 적용하지 않습니다.`를 출력합니다.

**실행 결과**

```text
회원 할인을 적용하지 않습니다.
```

`is_member`와 `total`의 값을 변경하면서 다음 네 가지 상황을 모두 확인하세요.

<table align="center">
  <thead>
    <tr>
      <th align="center">회원 여부</th>
      <th align="center">주문 금액(원)</th>
      <th align="center">회원 할인 적용 여부</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><code>True</code></td>
      <td align="right">12,000</td>
      <td align="center">적용</td>
    </tr>
    <tr>
      <td align="center"><code>True</code></td>
      <td align="right">8,000</td>
      <td align="center">미적용</td>
    </tr>
    <tr>
      <td align="center"><code>False</code></td>
      <td align="right">12,000</td>
      <td align="center">미적용</td>
    </tr>
    <tr>
      <td align="center"><code>False</code></td>
      <td align="right">8,000</td>
      <td align="center">미적용</td>
    </tr>
  </tbody>
</table>

> 논리 연산자 `and`는 두 조건이 모두 참일 때만 참으로 평가됩니다. 따라서 주문 금액이 충분하더라도 회원이 아니라면 회원 할인을 적용하지 않습니다.

---

## Mini Project. 카페 주문 접수하기

카페에서 손님의 주문을 접수하고 결제까지 처리하는 프로그램을 만들어 봅시다.

손님에게 메뉴 이름과 주문 수량, 받은 돈을 차례로 입력받습니다. 입력받은 메뉴와 수량이 유효한지 확인하고, 주문 금액에 따른 할인율을 적용하여 최종 결제 금액을 계산합니다. 이후 받은 돈이 충분한지 확인하여 결제 결과를 안내합니다.

이번 프로젝트에서는 한 번에 한 종류의 메뉴만 주문하며, 수량과 받은 돈은 정수로 입력한다고 가정합니다. 받은 돈은 0 이상으로 제한합니다.

### 메뉴 가격표

<table align="center">
  <thead>
    <tr>
      <th align="center">메뉴</th>
      <th align="center">가격(원)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left">커피</td>
      <td align="right">4,800</td>
    </tr>
    <tr>
      <td align="left">쿠키</td>
      <td align="right">2,500</td>
    </tr>
    <tr>
      <td align="left">차</td>
      <td align="right">3,000</td>
    </tr>
  </tbody>
</table>

### 시작 코드

```python
menu = {"커피": 4800, "쿠키": 2500, "차": 3000}

item = input("메뉴: ")
quantity = int(input("수량: "))
paid = int(input("받은 돈: "))
```

각 변수에 저장되는 정보는 다음과 같습니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">변수</th>
      <th align="center">자료형</th>
      <th align="center">저장하는 정보</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><code>menu</code></td>
      <td align="center"><code>dict</code></td>
      <td align="left">메뉴 이름과 가격</td>
    </tr>
    <tr>
      <td align="center"><code>item</code></td>
      <td align="center"><code>str</code></td>
      <td align="left">손님이 주문한 메뉴 이름</td>
    </tr>
    <tr>
      <td align="center"><code>quantity</code></td>
      <td align="center"><code>int</code></td>
      <td align="left">주문 수량</td>
    </tr>
    <tr>
      <td align="center"><code>paid</code></td>
      <td align="center"><code>int</code></td>
      <td align="left">손님에게 받은 돈</td>
    </tr>
  </tbody>
</table>

### 요구사항

**1. 메뉴 확인하기**

- `in` 또는 `not in` 연산자를 사용하여 입력받은 메뉴 이름이 딕셔너리 `menu`에 등록되어 있는지 확인합니다.
- 등록되지 않은 메뉴라면 `판매하지 않는 메뉴입니다.`를 출력합니다.
- 등록되지 않은 메뉴에 대해서는 이후 주문 금액 계산과 결제 처리를 진행하지 않습니다.

**2. 주문 수량 확인하기**

- 메뉴가 등록되어 있다면 주문 수량이 1 이상인지 확인합니다.
- 수량이 1보다 작으면 `수량은 1 이상이어야 합니다.`를 출력합니다.
- 메뉴와 수량이 모두 유효한 경우에만 주문 금액을 계산합니다.

**3. 주문 금액 계산하기**

- 딕셔너리에서 주문한 메뉴의 가격을 가져옵니다.
- 메뉴의 단가에 주문 수량을 곱하여 할인 전 주문 금액을 계산합니다.
- 계산한 주문 금액은 `total` 변수에 저장합니다.

**4. 할인율 적용하기**

주문 금액에 따라 다음 할인율을 적용합니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">주문 금액</th>
      <th align="center">할인율</th>
      <th align="center"><code>rate</code></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left">30,000원 이상</td>
      <td align="right">10%</td>
      <td align="right">10</td>
    </tr>
    <tr>
      <td align="left">10,000원 이상 30,000원 미만</td>
      <td align="right">5%</td>
      <td align="right">5</td>
    </tr>
    <tr>
      <td align="left">10,000원 미만</td>
      <td align="right">0%</td>
      <td align="right">0</td>
    </tr>
  </tbody>
</table>

- 적용할 할인율을 `rate` 변수에 저장합니다.
- 할인액은 `total * rate // 100`을 사용하여 계산합니다.
- 주문 금액에서 할인액을 빼 최종 결제 금액을 구합니다.

> 이 프로젝트에서는 금액을 정수 단위로 처리합니다. 할인액을 계산할 때 `//` 연산자를 사용하면 1원 미만의 금액을 버릴 수 있습니다.

**5. 결제 처리하기**

- 최종 결제 금액을 출력합니다.
- 받은 돈이 결제 금액 이상이면 거스름돈을 계산하고 결제 완료 문구와 함께 출력합니다.
- 받은 돈이 결제 금액보다 적으면 부족한 금액을 계산하여 출력합니다.
- 금액을 출력할 때는 f-문자열을 사용하여 천 단위 구분 기호를 표시합니다.

### 실행 예시

**실행 예시 1 — 정상적인 주문 및 결제**

```text
메뉴: 커피
수량: 3
받은 돈: 15000
결제 금액: 13,680원
결제 완료. 거스름돈: 1,320원
```

커피의 가격은 4,800원이고 주문 수량은 3잔이므로 주문 금액은 14,400원입니다. 주문 금액이 10,000원 이상 30,000원 미만이므로 5%의 할인율을 적용합니다.

<table align="center">
  <thead>
    <tr>
      <th align="center">구분</th>
      <th align="center">계산 과정</th>
      <th align="center">금액(원)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left">주문 금액</td>
      <td align="right">4,800 × 3</td>
      <td align="right">14,400</td>
    </tr>
    <tr>
      <td align="left">할인액</td>
      <td align="right">14,400 × 5 ÷ 100</td>
      <td align="right">720</td>
    </tr>
    <tr>
      <td align="left">결제 금액</td>
      <td align="right">14,400 - 720</td>
      <td align="right">13,680</td>
    </tr>
    <tr>
      <td align="left">받은 돈</td>
      <td align="center">-</td>
      <td align="right">15,000</td>
    </tr>
    <tr>
      <td align="left">거스름돈</td>
      <td align="right">15,000 - 13,680</td>
      <td align="right">1,320</td>
    </tr>
  </tbody>
</table>

**실행 예시 2 — 판매하지 않는 메뉴를 주문한 경우**

```text
메뉴: 주스
수량: 2
받은 돈: 10000
판매하지 않는 메뉴입니다.
```

가격표에 등록되지 않은 메뉴이므로 주문 금액 계산과 결제 처리를 진행하지 않습니다.

**실행 예시 3 — 주문 수량이 올바르지 않은 경우**

```text
메뉴: 커피
수량: 0
받은 돈: 10000
수량은 1 이상이어야 합니다.
```

메뉴는 등록되어 있지만 주문 수량이 1보다 작으므로 결제를 진행하지 않습니다.

**실행 예시 4 — 받은 돈이 부족한 경우**

```text
메뉴: 커피
수량: 3
받은 돈: 13000
결제 금액: 13,680원
680원이 부족합니다.
```

결제 금액은 13,680원이지만 받은 돈은 13,000원이므로 결제에 필요한 금액이 680원 부족합니다.

**실행 예시 5 — 받은 돈과 결제 금액이 같은 경우**

```text
메뉴: 커피
수량: 3
받은 돈: 13680
결제 금액: 13,680원
결제 완료. 거스름돈: 0원
```

받은 돈과 결제 금액이 같으므로 정상적으로 결제를 완료하고, 거스름돈은 0원으로 출력합니다.

### 프로그램 검증하기

프로그램을 완성했다면 메뉴, 수량, 받은 돈을 다양하게 변경하면서 요구사항을 모두 만족하는지 확인하세요.

<table align="center">
  <thead>
    <tr>
      <th align="center">번호</th>
      <th align="center">메뉴</th>
      <th align="center">수량</th>
      <th align="center">받은 돈(원)</th>
      <th align="center">결제 금액(원)</th>
      <th align="center">예상 결과</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">1</td>
      <td align="left">커피</td>
      <td align="right">1</td>
      <td align="right">5,000</td>
      <td align="right">4,800</td>
      <td align="left">거스름돈 200원</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td align="left">쿠키</td>
      <td align="right">4</td>
      <td align="right">10,000</td>
      <td align="right">9,500</td>
      <td align="left">거스름돈 500원</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td align="left">차</td>
      <td align="right">10</td>
      <td align="right">30,000</td>
      <td align="right">27,000</td>
      <td align="left">거스름돈 3,000원</td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td align="left">커피</td>
      <td align="right">3</td>
      <td align="right">13,000</td>
      <td align="right">13,680</td>
      <td align="left">680원 부족</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td align="left">커피</td>
      <td align="right">3</td>
      <td align="right">13,680</td>
      <td align="right">13,680</td>
      <td align="left">거스름돈 0원</td>
    </tr>
    <tr>
      <td align="center">6</td>
      <td align="left">주스</td>
      <td align="right">2</td>
      <td align="right">10,000</td>
      <td align="center">-</td>
      <td align="left">판매하지 않는 메뉴</td>
    </tr>
    <tr>
      <td align="center">7</td>
      <td align="left">커피</td>
      <td align="right">0</td>
      <td align="right">10,000</td>
      <td align="center">-</td>
      <td align="left">올바르지 않은 수량</td>
    </tr>
    <tr>
      <td align="center">8</td>
      <td align="left">차</td>
      <td align="right">-1</td>
      <td align="right">5,000</td>
      <td align="center">-</td>
      <td align="left">올바르지 않은 수량</td>
    </tr>
  </tbody>
</table>

> 정상적인 입력뿐만 아니라 잘못된 입력이나 조건이 바뀌는 경계값에서도 프로그램이 올바르게 동작하는지 확인해야 합니다. 특히 조건문을 사용하는 프로그램에서는 각각의 조건에 해당하는 입력값을 준비하여 모든 실행 경로를 확인하는 습관을 들이세요.

---

모든 실습을 마친 뒤 [Solutions](./solutions/README.md)에서 예제 풀이와 해설을 확인하세요. 자신이 작성한 코드와 예제 풀이를 비교하면서 조건문의 구성 방법과 실행 흐름을 살펴보세요.

<p align="center">
  <a href="./5.5.Nested-Conditions.md">← 5.5. Nested Conditions</a>
  &nbsp;·&nbsp;
  <a href="./README.md">Chapter 05</a>
  &nbsp;·&nbsp;
  <a href="./solutions/README.md">Solutions →</a>
</p>
