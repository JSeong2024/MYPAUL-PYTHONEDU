# Chapter 04. Python Data Structures

지난 장에서는 커피와 쿠키의 주문 수량을 각각 입력받아 결제 금액을 계산했습니다. 메뉴가 늘어날 때마다 새로운 변수를 만들면, 주문 목록이나 가격표를 한눈에 파악하기 어려워집니다.

이번 장에서는 여러 값을 한곳에 모아 다루는 **자료구조(Data Structure)** 를 살펴봅니다. 주문 순서는 리스트에, 메뉴 이름과 가격은 딕셔너리에 저장하는 것처럼 데이터의 용도에 맞춰 자료구조를 선택해 봅니다.

## 4.1. List — 순서대로 값 관리하기

리스트는 여러 값을 순서대로 저장합니다. 대괄호 안에 값을 쉼표로 구분해 적습니다. 각 값의 위치를 나타내는 번호를 **인덱스(Index)** 라고 하며, 첫 번째 값의 인덱스는 `0`입니다.

### 예제 4-1. 주문 순서 확인하기

~~~python
orders = ["커피", "쿠키", "커피"]

print(orders[0])
print(orders[1])
print(len(orders))
~~~

**실행 결과**

~~~text
커피
쿠키
3
~~~

같은 메뉴가 두 번 들어 있어도 각각의 주문으로 남습니다. `len(orders)`는 주문 목록에 들어 있는 항목 수를 반환합니다. 이 리스트의 세 항목은 `orders[0]`, `orders[1]`, `orders[2]`로 읽을 수 있습니다. `orders[3]`에 접근하면 `IndexError`가 발생합니다.

### 예제 4-2. 주문 수정하기

~~~python
orders = ["커피", "쿠키"]

orders[1] = "샌드위치"
orders.append("커피")

print(orders)
~~~

**실행 결과**

~~~text
['커피', '샌드위치', '커피']
~~~

`orders[1] = "샌드위치"`는 두 번째 주문을 바꿉니다. `append()`는 리스트 맨 뒤에 항목을 추가합니다. 위치가 정해진 항목을 삭제할 때는 `del orders[1]`처럼 작성합니다. 가운데 항목을 삭제하면 뒤에 있던 항목이 한 칸씩 앞으로 이동합니다.

## 4.2. Tuple — 여러 값을 한 묶음으로 다루기

튜플도 값을 순서대로 저장하며, 인덱스로 값을 읽을 수 있습니다. 상품명과 가격처럼 정해진 자리에 각 값을 담아 한 묶음으로 다룰 때 사용할 수 있습니다.

### 예제 4-3. 메뉴 항목 읽기

~~~python
item = ("커피", 4800)

print(item[0])
print(f"{item[1]:,}원")
~~~

**실행 결과**

~~~text
커피
4,800원
~~~

튜플에 들어 있는 항목은 개별적으로 바꿀 수 없습니다. 위 코드에서 `item[1] = 5000`을 실행하면 `TypeError`가 발생합니다. `item = ("커피", 5000)`처럼 변수에 새 튜플을 대입할 수는 있습니다. 항목이 하나인 튜플을 만들 때는 `("커피",)`처럼 쉼표를 붙입니다.

## 4.3. Dictionary — 키로 값 찾기

딕셔너리는 **키(Key)** 와 **값(Value)** 을 한 쌍으로 저장합니다. 메뉴 이름을 키로, 가격을 값으로 저장하면 메뉴 이름으로 가격을 찾을 수 있습니다.

### 예제 4-4. 가격 조회하고 수정하기

~~~python
menu = {"커피": 4800, "쿠키": 2500}

print(menu["쿠키"])

menu["쿠키"] = 2800
menu["샌드위치"] = 6000

print(f"쿠키: {menu['쿠키']:,}원")
print(f"샌드위치: {menu['샌드위치']:,}원")
~~~

**실행 결과**

~~~text
2500
쿠키: 2,800원
샌드위치: 6,000원
~~~

기존 키에 값을 대입하면 가격이 바뀝니다. 새 키에 값을 대입하면 메뉴가 추가됩니다. `menu["차"]`처럼 등록되지 않은 키를 대괄호로 조회하면 `KeyError`가 발생합니다. 등록 여부만 확인하려면 `"차" in menu`를 사용합니다. 이 식의 결과는 `False`입니다.

## 4.4. Set — 중복 없이 값 모으기

집합은 같은 값을 한 번만 저장합니다. 집합에는 인덱스가 없으므로, 특정 항목의 존재 여부를 확인하거나 중복을 제거할 때 사용합니다.

### 예제 4-5. 주문한 메뉴의 종류 세기

~~~python
orders = ["커피", "쿠키", "커피"]
ordered_items = set(orders)

print(len(ordered_items))
print("쿠키" in ordered_items)
~~~

**실행 결과**

~~~text
2
True
~~~

주문은 세 건이고, 주문한 메뉴는 두 종류입니다. `set(orders)`는 리스트의 값을 읽어 새 집합을 만듭니다. 원래 주문 목록에는 커피 두 건이 그대로 남습니다.

집합은 `{"커피", "쿠키"}`처럼 만들 수도 있습니다. 빈 집합은 `set()`으로 만듭니다. `{}`는 빈 딕셔너리입니다.

## 4.5. Choosing a Data Structure — 자료구조 선택하기

먼저 저장한 정보를 어떻게 사용할지 생각해 봅시다. 첫 번째 주문을 확인해야 한다면 접수 순서가 필요합니다. 쿠키 가격을 찾으려면 메뉴 이름이 기준이 됩니다.

<table align="center">
  <thead>
    <tr>
      <th>자료구조</th>
      <th>선택 기준</th>
      <th>카페 주문 예시</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>리스트 <code>list</code></td>
      <td>순서를 유지하고 항목을 추가하거나 수정합니다.</td>
      <td>접수 순서대로 주문을 기록합니다.</td>
    </tr>
    <tr>
      <td>튜플 <code>tuple</code></td>
      <td>정해진 순서로 값을 묶고 각 항목을 그대로 유지합니다.</td>
      <td>상품명과 가격을 한 쌍으로 다룹니다.</td>
    </tr>
    <tr>
      <td>딕셔너리 <code>dict</code></td>
      <td>키를 기준으로 값을 읽거나 수정합니다.</td>
      <td>메뉴 이름으로 가격을 조회합니다.</td>
    </tr>
    <tr>
      <td>집합 <code>set</code></td>
      <td>중복을 제외하거나 항목의 포함 여부를 확인합니다.</td>
      <td>주문한 메뉴의 종류를 셉니다.</td>
    </tr>
  </tbody>
</table>

## Summary

- 리스트와 튜플은 인덱스로 값을 읽습니다. 첫 번째 항목의 인덱스는 `0`입니다.
- 리스트는 항목을 수정할 수 있습니다. 튜플은 생성 후 각 자리에 있는 항목을 바꿀 수 없습니다.
- 딕셔너리는 키로 값을 조회합니다. 같은 키에 다시 대입하면 값이 갱신됩니다.
- 집합은 중복된 값을 하나로 모읍니다. 항목이 들어 있는지는 `in`으로 확인할 수 있습니다.

## Exercise

1. `["커피", "쿠키"]`에서 첫 항목을 `"차"`로 바꾸고, 목록의 맨 뒤에 `"커피"`를 추가한 뒤 전체 목록을 출력해 보세요.
2. `("샌드위치", 6000)`에서 메뉴 이름과 가격을 읽어 `샌드위치: 6,000원`을 출력해 보세요.
3. `{"커피": 4800, "쿠키": 2500}`에서 쿠키 가격을 2,800원으로 바꾸고, 차를 3,000원으로 추가한 뒤 두 가격을 출력해 보세요.
4. `["커피", "차", "커피", "차", "쿠키"]`에서 전체 주문 건수와 주문한 메뉴 종류 수를 각각 구해 보세요.

<details>
<summary>연습문제 확인</summary>

<table align="center">
  <thead>
    <tr>
      <th>문제</th>
      <th>확인할 결과</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><code>['차', '쿠키', '커피']</code></td>
    </tr>
    <tr>
      <td>2</td>
      <td><code>샌드위치: 6,000원</code></td>
    </tr>
    <tr>
      <td>3</td>
      <td>쿠키 2,800원, 차 3,000원</td>
    </tr>
    <tr>
      <td>4</td>
      <td>전체 5건, 메뉴 3종류</td>
    </tr>
  </tbody>
</table>

</details>

## Mini Project

### 카페 주문 요약표 만들기

메뉴 가격표와 두 건의 주문을 이용해 주문별 금액과 합계를 출력합니다. 같은 메뉴가 두 번 들어올 수도 있습니다. 주문 목록에는 두 건을 모두 남기고, 메뉴 종류 수를 셀 때는 중복을 한 번만 셉니다.

**시작 코드**

~~~python
menu = {"커피": 4800, "쿠키": 2500, "샌드위치": 6000}
orders = ["커피", "쿠키"]
~~~

**요구사항**

1. 인덱스를 사용해 첫 번째와 두 번째 주문의 메뉴 이름을 읽는다.
2. 딕셔너리에서 각 메뉴의 가격을 찾아 주문별 가격과 합계를 구한다.
3. 주문 건수와 주문한 메뉴의 종류 수를 출력한다.
4. 각 금액에 천 단위 구분 기호와 `원`을 표시한다.

**실행 예시**

~~~text
첫 번째 주문: 커피 4,800원
두 번째 주문: 쿠키 2,500원
합계: 7,300원
전체 주문: 2건
메뉴 종류: 2종
~~~

**확인할 사항**

- `orders`를 `["커피", "커피"]`로 바꾸면 전체 주문은 2건, 메뉴 종류는 1종, 합계는 9,600원으로 표시되는가?
- `menu`에서 커피 가격을 5,000원으로 바꾸면 새 가격이 합계에 반영되는가?

주문은 가격표에 등록된 메뉴 두 건으로 가정합니다. 등록 여부에 따라 출력을 바꾸는 기능은 Chapter 05의 조건문으로, 주문 건수에 관계없이 합계를 구하는 기능은 Chapter 06의 반복문으로 확장할 수 있습니다.

<details>
<summary>미니 프로젝트 해설</summary>

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

합계는 주문별 가격으로 계산합니다. 집합은 메뉴의 종류를 셀 때 사용합니다.

</details>

---

## References

- [Python Tutorial — Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python Standard Library — Built-in Types](https://docs.python.org/3/library/stdtypes.html)

---

<p align="center">
  <a href="../Chapter-03/">← Chapter 03</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-05/">Chapter 05 →</a>
</p>

<p align="center">
  <sub>© 2025–2026 Choi Jae-Seong · ONEUL</sub>
  <br>
  <sub>
    Educational Content ·
    <a href="../../LICENSE-CONTENT.md">CC BY-NC 4.0</a>
  </sub>
</p>

<p align="center">
  <img src="../../.github/assets/logo_ONEUL_01.png"
       width="90" alt="ONEUL">
</p>
