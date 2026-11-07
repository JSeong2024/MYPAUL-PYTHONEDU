# Chapter 02. Python Data Structures

데이터 처리에 사용하는 Python의 핵심 자료구조인 **List, Tuple, Dictionary, Set**을 학습합니다. 단순한 문법 암기를 넘어 데이터의 순서·중복·고유성·조회 방식을 고려하여 적절한 자료구조를 선택하고, 중첩 레코드의 탐색·필터링·정렬·집계로 연결하는 방법을 다룹니다.

본 자료는 **Python 3.13 이상** 환경을 권장하며, 예제는 **Python 3.10 이상**에서 사용할 수 있는 표준 라이브러리만 활용합니다. NumPy 배열과 Pandas DataFrame은 Chapter 03~04에서 다룹니다.

**선행 학습:** [Chapter 01 — Introduction to Data Processing](../Chapter-01/) · Python 변수·조건문·반복문·함수의 기본 사용법

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [2.1](#section-2-1) | List & Tuple — 순서가 있는 데이터 |
| [2.2](#section-2-2) | Dictionary — Key-Value 기반 데이터 |
| [2.3](#section-2-3) | Set — 중복 제거와 집합 연산 |
| [2.4](#section-2-4) | Nested Data Structures — 중첩 레코드 |
| [2.5](#section-2-5) | Iteration & Comprehension — 데이터 반복 처리 |
| [2.6](#section-2-6) | Sorting & Filtering — 정렬과 조건별 선택 |
| [2.7](#section-2-7) | `collections` — Counter와 defaultdict |
| [2.8](#section-2-8) | Mutability, Copy & Structure Selection — 자료구조 선택과 주의 사항 |
| [2.9](#section-2-9) | Mini Project — Library Loan Report |
| [2.10](#section-2-10) | Coding Practice |
| [2.11](#section-2-11) | Quiz & Summary |

---

<a id="section-2-1"></a>
## 2.1. List & Tuple — 순서가 있는 데이터

**List(리스트)**와 **Tuple(튜플)**은 여러 값을 일정한 순서로 보관하는 시퀀스(Sequence)입니다. 두 자료구조 모두 인덱스로 값에 접근하고, 동일한 값이 여러 번 등장할 수 있습니다. 가장 중요한 차이는 **생성 후 요소의 변경 가능 여부**입니다.

| 비교 | `list` | `tuple` |
|---|---|---|
| 생성 | `[10, 20, 30]` | `(10, 20, 30)` |
| 순서 | 유지 | 유지 |
| 중복 | 허용 | 허용 |
| 인덱싱 / 슬라이싱 | 지원 | 지원 |
| 요소 변경·추가·삭제 | 가능 | 불가능 |
| 적합한 예 | 갱신되는 센서 측정값 | `(위도, 경도)`, 고정 레코드 구조 |

### 2.1.1. 인덱싱, 슬라이싱과 갱신

- `values[0]`: 첫 번째 원소에 접근합니다. 인덱스는 0부터 시작합니다.
- `values[-1]`: 마지막 원소에 접근합니다.
- `values[start:stop]`: `start`부터 `stop` **직전**까지 선택합니다.
- `values.append(x)`: 리스트의 마지막에 원소를 추가합니다.
- `len(values)`: 원소의 개수를 구합니다.

리스트의 슬라이스는 새로운 리스트를 반환하지만, 그 안에 **가변 객체가 들어 있다면 내부 객체의 참조는 공유**할 수 있습니다. 이 차이는 Section 2.8에서 다시 살펴봅니다.

### 2.1.2. Tuple Packing & Unpacking

튜플을 활용하면 관련된 값을 일정한 위치에 보관하고 변수에 한 번에 분리할 수 있습니다.

```python
sensor = ("ST-01", 23.5)
sensor_id, temperature_c = sensor  # Unpacking
print(sensor_id, temperature_c)
```

```text
ST-01 23.5
```

`(42,)`처럼 원소 하나로 구성된 튜플에는 쉼표가 필요합니다. `(42)`는 정수 `42`를 괄호로 감싼 표현식입니다.

**예제 코드 — [01_list_tuple.py](./examples/01_list_tuple.py)**

```python
"""리스트와 튜플을 이용한 측정값 관리."""

readings = [21, 24, 23, 26]
readings.append(25)
readings[0] = 22

print("측정값:", readings)
print("최근 3개:", readings[-3:])
print("측정 개수:", len(readings))

sensor = ("ST-01", "광주", "temperature_c")
sensor_id, region, field = sensor
print(f"센서: {sensor_id} / {region} / {field}")

# 리스트의 슬라이스는 바깥쪽 리스트를 새로 만듭니다.
recent = readings[-3:]
recent[0] = 0
print("원본의 마지막 3개:", readings[-3:])
```

**실행 결과**

```text
측정값: [22, 24, 23, 26, 25]
최근 3개: [23, 26, 25]
측정 개수: 5
센서: ST-01 / 광주 / temperature_c
원본의 마지막 3개: [23, 26, 25]
```

**주의 사항:** 튜플의 원소 위치는 그 자체로 의미를 알려 주지 않습니다. `(23.5, "ST-01")`과 `("ST-01", 23.5)`를 혼동할 수 있으므로 필드의 의미가 많은 레코드는 Dictionary나 이름이 있는 데이터 구조로 표현하는 편이 명확합니다. 또한 튜플이 불변이어도 튜플 내부의 리스트 같은 객체까지 불변이 되는 것은 아닙니다.

---

<a id="section-2-2"></a>
## 2.2. Dictionary — Key-Value 기반 데이터

**Dictionary(딕셔너리)**는 Key(키)와 Value(값)를 연결한 Mapping 자료구조입니다. 데이터 처리에서는 한 개의 레코드를 필드 이름으로 표현하거나, ID별 데이터를 빠르게 조회하는 데 자주 사용합니다.

```python
record = {"student_id": "S-001", "score": 95}
print(record["student_id"])  # S-001
```

### 2.2.1. Key 조회·추가·수정

| 코드 | 역할 | 반환·결과 |
|---|---|---|
| `record["score"]` | 필수 Key 값 조회 | Key가 없으면 `KeyError` |
| `record.get("score")` | Key 조회 | 없으면 `None` |
| `record.get("discount", 0)` | 기본값과 함께 조회 | 없으면 `0` |
| `"score" in record` | Key 존재 여부 | `bool` |
| `record["score"] = 90` | 값 추가 또는 수정 | 원본 수정 |
| `record.keys()` | Key 뷰 조회 | Key 집합에 해당하는 뷰 |
| `record.items()` | (Key, Value) 쌍 조회 | 항목 뷰 |

`record.get("value")`의 결과가 `None`이라고 해서 반드시 **Key가 없는 것**은 아닙니다. Key는 존재하지만 저장된 값이 `None`일 수도 있습니다. 두 상태를 구분해야 한다면 `"value" in record`를 확인합니다.

### 2.2.2. Dictionary의 순서와 Key 조건

Python 3.7부터 일반 Dictionary는 **삽입 순서를 보장**합니다. 기존 Key의 값을 변경해도 위치는 변하지 않지만, 삭제 후 다시 삽입하면 마지막에 들어갑니다. 키에는 문자열·정수·튜플처럼 **해시 가능한(Hashable)** 객체를 사용할 수 있습니다. 가변 List나 Dictionary는 키로 사용할 수 없습니다. 다만 튜플 안에 비해시 객체가 들어 있다면 그 튜플도 키로 사용할 수 없습니다.

**예제 코드 — [02_dictionary_records.py](./examples/02_dictionary_records.py)**

```python
"""딕셔너리로 상품 정보를 관리하고 안전하게 조회."""

product = {"product_id": "P-001", "name": "노트", "stock": 12}
product["stock"] -= 3
product["category"] = "문구"

print("상품:", product["name"])
print("재고:", product["stock"])
print("할인율:", product.get("discount_rate", 0))
print("품목:", list(product))

if "category" in product:
    print("분류:", product["category"])

# Key가 없을 수 있다면 `dict.get()`이나 멤버십 검사를 고려합니다.
```

**실행 결과**

```text
상품: 노트
재고: 9
할인율: 0
품목: ['product_id', 'name', 'stock', 'category']
분류: 문구
```

**데이터 처리에서의 사용:** `product_id`를 Key로 사용하면 상품 번호로 레코드를 찾을 수 있습니다. 반대로 동명이인이 있는 사람의 이름을 고유 Key로 사용하면 자료를 잘못 덮어쓸 위험이 있으므로, 자료의 고유성 규칙을 먼저 정해야 합니다.

---

<a id="section-2-3"></a>
## 2.3. Set — 중복 제거와 집합 연산

**Set(집합)**은 중복을 허용하지 않는 원소들의 모음입니다. 방문자 ID와 같이 고유한 값만 남기거나, 서로 다른 데이터셋의 공통 ID를 찾을 때 유용합니다.

| 연산 | 구문 | 의미 |
|---|---|---|
| 합집합 | `a \| b` | 둘 중 한쪽 이상에 존재 |
| 교집합 | `a & b` | 양쪽 모두에 존재 |
| 차집합 | `a - b` | a에만 존재 |
| 대칭차집합 | `a ^ b` | 한쪽에만 존재 |
| 포함 검사 | `x in a` | x가 a에 존재하는지 확인 |

Set은 데이터가 입력된 순서를 **보장하지 않습니다.** 재현 가능한 정렬 결과가 필요하다면 `sorted()`로 List를 만든 다음 출력합니다. 또한 집합의 원소도 해시 가능해야 합니다.

**예제 코드 — [03_set_operations.py](./examples/03_set_operations.py)**

```python
"""집합을 이용한 중복 제거와 두 집단의 비교."""

monday = ["S-01", "S-02", "S-02", "S-03"]
tuesday = ["S-02", "S-04", "S-03"]
mon_ids = set(monday)
tue_ids = set(tuesday)

print("월요일 방문자:", sorted(mon_ids))
print("공통 방문자:", sorted(mon_ids & tue_ids))
print("월요일에만:", sorted(mon_ids - tue_ids))
print("전체 고유 방문자:", len(mon_ids | tue_ids))

# set의 순회 순서는 보장되지 않으므로 출력에서는 sorted()를 사용합니다.
```

**실행 결과**

```text
월요일 방문자: ['S-01', 'S-02', 'S-03']
공통 방문자: ['S-02', 'S-03']
월요일에만: ['S-01']
전체 고유 방문자: 4
```

**주의:** `list(set(records))`는 중복을 제거할 수 있지만 원래 입력 순서는 보장하지 않습니다. **첫 등장 순서까지 보존**해야 한다면 Dictionary의 삽입 순서를 활용하는 `list(dict.fromkeys(records))`를 고려할 수 있습니다(원소가 Key로 사용 가능한 경우). 또한 ID의 대소문자·공백 등이 정규화되지 않았다면 서로 다른 값으로 취급합니다.

---

<a id="section-2-4"></a>
## 2.4. Nested Data Structures — 중첩 레코드

하나의 학생에게 여러 과목 점수가 있거나, 하나의 주문에 여러 상품이 포함되는 등 실제 데이터는 단순한 일차원 목록만으로 표현하기 어렵습니다. 이러한 경우 List, Tuple, Dictionary를 **중첩(Nested)**하여 표현합니다.

```python
order = {
    "order_id": "O-1001",
    "customer": {"id": "C-01", "region": "광주"},
    "items": [
        {"product": "노트", "quantity": 2},
        {"product": "연필", "quantity": 3},
    ],
}
print(order["customer"]["region"])  # 광주
print(order["items"][0]["product"])  # 노트
```

| 표현 | 의미 | 예시 |
|---|---|---|
| `list[int]` | 수치 목록 | 점수 5개 |
| `dict[str, int]` | 이름과 수치 매핑 | 분류별 주문 수 |
| `list[dict]` | 여러 레코드 | 학생·상품 정보 |
| `dict[str, list]` | 그룹별 목록 | 지역별 측정값 |
| `dict[str, dict]` | ID별 상세 정보 | 사용자별 프로필 |

### 누락 필드 처리

데이터를 탐색할 때 키가 존재하지 않는 경우와 값이 없는 경우는 구분해야 합니다. 아래 예제의 `Math` 성적이 없는 학생은 성적이 0점인 학생과 다르게 표시됩니다.

**예제 코드 — [04_nested_records.py](./examples/04_nested_records.py)**

```python
"""중첩된 레코드에서 과목별 점수를 조회."""

students = [
    {"id": "S-01", "name": "민지", "scores": {"Python": 90, "Math": 82}},
    {"id": "S-02", "name": "도윤", "scores": {"Python": 76, "Math": 91}},
    {"id": "S-03", "name": "서아", "scores": {"Python": 88}},
]

for student in students:
    python_score = student["scores"].get("Python")
    math_score = student["scores"].get("Math")
    math_text = str(math_score) if math_score is not None else "미응시"
    print(f"{student['id']} {student['name']}: Python {python_score}, Math {math_text}")

print("학생 수:", len(students))
```

**실행 결과**

```text
S-01 민지: Python 90, Math 82
S-02 도윤: Python 76, Math 91
S-03 서아: Python 88, Math 미응시
학생 수: 3
```

**주의:** 모든 레코드가 동일한 구조를 가진다고 단정하면 `KeyError`, `TypeError` 등이 발생할 수 있습니다. 파일에서 받은 외부 데이터의 구조와 허용 범위를 검증하는 방법은 Chapter 06에서 자세히 학습합니다.

---

<a id="section-2-5"></a>
## 2.5. Iteration & Comprehension — 데이터 반복 처리

많은 데이터를 하나씩 처리할 때는 `for` 반복문을 사용합니다. **Comprehension(컴프리헨션)**은 List·Dictionary·Set 등을 간결하게 생성할 수 있는 구문입니다.

| 구문 | 생성 결과 | 예시 |
|---|---|---|
| `[f(x) for x in xs]` | List | 값 변환 |
| `[x for x in xs if cond]` | List | 조건에 맞는 값 추출 |
| `{x for x in xs}` | Set | 중복 없는 값 추출 |
| `{k: v for k, v in pairs}` | Dictionary | 키-값 매핑 생성 |
| `(f(x) for x in xs)` | Generator Expression | 필요할 때 순차 계산 |

일회성 합계처럼 중간 List가 필요하지 않으면 `sum(x for x in values if x > 0)`과 같이 Generator Expression을 사용할 수 있습니다. 단, 작은 데이터에서는 반복문과 Comprehension 모두 읽기 쉬운 방식을 선택하면 됩니다.

**예제 코드 — [05_comprehensions.py](./examples/05_comprehensions.py)**

```python
"""컴프리헨션으로 데이터 추출과 간단한 변환."""

readings = [18, 21, 27, 19, 30]
hot = [value for value in readings if value >= 25]
celsius_to_fahrenheit = [round(value * 9 / 5 + 32, 1) for value in hot]

products = [
    {"name": "노트", "price": 2500},
    {"name": "연필", "price": 800},
    {"name": "파일", "price": 1500},
]
price_by_name = {item["name"]: item["price"] for item in products}

print("고온 측정값:", hot)
print("화씨 변환:", celsius_to_fahrenheit)
print("상품 가격:", price_by_name)
```

**실행 결과**

```text
고온 측정값: [27, 30]
화씨 변환: [80.6, 86.0]
상품 가격: {'노트': 2500, '연필': 800, '파일': 1500}
```

**가독성 기준:** 여러 단계의 예외 처리나 상태를 갱신하는 로직은 컴프리헨션 한 줄에 억지로 넣지 않는 것이 좋습니다. 복잡한 조건이 들어가면 일반 `for`문이나 별도의 함수로 나누면 오류를 찾기 쉽습니다.

**주의:** Dictionary Comprehension에서 **동일한 Key가 여러 번 등장하면 마지막 값이 이전 값을 덮어씁니다.** 중복 기록을 모두 보존해야 한다면 값으로 List를 보관하거나 `defaultdict(list)`로 묶어야 합니다.

---

<a id="section-2-6"></a>
## 2.6. Sorting & Filtering — 정렬과 조건별 선택

조건별 추출(Filtering)은 필요한 레코드만 선택하는 과정이며, 정렬(Sorting)은 비교 기준에 따라 순서를 지정하는 과정입니다.

### 2.6.1. `sorted()`와 `list.sort()`

| 구문 | 동작 | 원본 List |
|---|---|---|
| `sorted(values)` | 정렬된 새 List 반환 | 변경하지 않음 |
| `values.sort()` | List 자체를 정렬 | 변경함 |
| `sorted(values, reverse=True)` | 내림차순 정렬 | 변경하지 않음 |
| `sorted(records, key=...)` | 특정 필드를 기준으로 정렬 | 변경하지 않음 |

Python의 정렬은 **안정 정렬(Stable Sort)**입니다. 비교 기준이 같은 원소는 정렬 전에 서로 가지고 있던 상대적 순서를 유지합니다. 여러 기준으로 정렬할 때는 튜플을 Key로 전달하면 명확합니다.

```python
sorted(records, key=lambda x: (-x["score"], x["name"]))
```

위 코드의 첫 번째 기준은 점수 **내림차순**, 두 번째 기준은 이름 **오름차순**입니다. 점수가 동일하면 이름으로 순서를 결정합니다. 단순히 `reverse=True`를 설정하면 튜플 안의 모든 정렬 기준이 한꺼번에 뒤집힐 수 있으므로 주의해야 합니다.

### 2.6.2. 조건별 필터링

`[row for row in rows if row["stock"] >= 5]`처럼 필요한 조건을 만족하는 레코드만 새 List에 모을 수 있습니다. 이때 `stock` 필드가 모든 레코드에 존재하고 숫자형이라는 전제가 필요합니다.

**예제 코드 — [06_sorting_filtering.py](./examples/06_sorting_filtering.py)**

```python
"""조건 필터링과 복수 기준의 안정적 정렬."""

products = [
    {"name": "노트", "category": "문구", "price": 2500, "stock": 7},
    {"name": "연필", "category": "문구", "price": 800, "stock": 12},
    {"name": "커피", "category": "음료", "price": 2500, "stock": 4},
    {"name": "파일", "category": "문구", "price": 1500, "stock": 9},
]

available = [item for item in products if item["stock"] >= 5]
ranked = sorted(available, key=lambda item: (-item["price"], item["name"]))

print("재고 5개 이상:", len(available), "종")
for item in ranked:
    print(f"{item['name']}: {item['price']:,}원 / {item['stock']}개")

print("원본 첫 번째:", products[0]["name"])
```

**실행 결과**

```text
재고 5개 이상: 3 종
노트: 2,500원 / 7개
파일: 1,500원 / 9개
연필: 800원 / 12개
원본 첫 번째: 노트
```

**데이터 해석:** 이 예제는 재고 5개 이상인 상품만 선택한 다음 가격이 높은 순서로 나열합니다. `sorted()`는 상품 정보를 새로 정렬한 목록으로 반환하므로 원본 `products`의 순서는 바뀌지 않습니다.

---

<a id="section-2-7"></a>
## 2.7. `collections` — Counter와 defaultdict

Python 표준 라이브러리의 `collections`는 데이터 처리에 유용한 자료구조를 제공합니다. 이 Chapter에서는 **빈도 계산(Frequency Counting)**과 **그룹별 누적(Group Aggregation)**에 활용되는 `Counter`, `defaultdict`를 학습합니다.

### 2.7.1. Counter — 데이터 빈도 계산

`Counter`는 원소가 몇 번 나타났는지 계산하는 Dictionary 하위 클래스입니다.

```python
from collections import Counter

counts = Counter(["음료", "문구", "음료", "간식"])
print(counts["음료"])     # 2
print(counts["미등록"])   # 0
```

`counts.most_common()`은 빈도가 큰 순서대로 `(항목, 개수)`를 반환합니다. 빈도가 같을 경우 처음 등장한 순서가 영향을 줄 수 있으므로 **동점에 대한 고정된 정렬 규칙**이 필요하다면 `sorted(counts.items(), key=lambda x: (-x[1], x[0]))`을 사용합니다.

### 2.7.2. defaultdict — 기본값이 있는 그룹 누적

```python
from collections import defaultdict

revenue = defaultdict(int)
revenue["문구"] += 1200  # Key가 없으면 0으로 시작
```

`defaultdict(int)`는 없는 Key를 `[]`로 조회하면 `int()`가 반환하는 0을 생성해 저장합니다. `defaultdict(list)`는 없는 Key를 조회하면 빈 List를 생성하므로, 그룹별 레코드 묶기에 활용할 수 있습니다.

**예제 코드 — [07_counter_defaultdict.py](./examples/07_counter_defaultdict.py)**

```python
"""Counter와 defaultdict를 이용한 빈도와 그룹 집계."""

from collections import Counter, defaultdict

orders = [
    ("문구", 3500),
    ("음료", 2500),
    ("문구", 1200),
    ("간식", 1800),
    ("음료", 2200),
]

counts = Counter(category for category, _ in orders)
revenue = defaultdict(int)
for category, price in orders:
    revenue[category] += price

for category in sorted(counts):
    print(f"{category}: {counts[category]}건 / {revenue[category]:,}원")
print("최다 주문 수:", max(counts.values()))
```

**실행 결과**

```text
간식: 1건 / 1,800원
문구: 2건 / 4,700원
음료: 2건 / 4,700원
최다 주문 수: 2
```

**선택 기준**

- **개수 계산:** `Counter`가 간결합니다.
- **합계 계산:** `defaultdict(int)` 또는 일반 Dictionary의 `get()`이 적절합니다.
- **그룹별 레코드 보관:** `defaultdict(list)`가 편리합니다.
- **한 번 조회만 필요한 Key:** `defaultdict`의 `[]` 조회는 새로운 Key를 생성할 수 있으므로 `.get()`과 구분합니다.

---

<a id="section-2-8"></a>
## 2.8. Mutability, Copy & Structure Selection — 자료구조 선택과 주의 사항

### 2.8.1. 가변성과 객체 공유

리스트와 딕셔너리는 **가변(Mutable)** 객체입니다. 같은 객체를 두 변수가 참조한다면 한쪽에서 값을 변경할 때 다른 쪽에서도 변경된 상태를 보게 됩니다.

```python
original = [1, 2]
alias = original
alias.append(3)
print(original)  # [1, 2, 3]
```

`original.copy()`는 새로운 바깥 List를 만들지만 안쪽의 가변 객체는 계속 공유할 수 있습니다. 이는 외부 데이터에서 일부만 수정하려다 원본까지 바꾸는 오류로 이어질 수 있습니다. 내부 객체까지 별도로 복사해야 할 때는 `copy.deepcopy()`를 검토합니다. 다만 복사가 항상 최선은 아니며, 데이터 크기와 필요한 변경 범위를 고려해야 합니다.

**예제 코드 — [08_copy_identity.py](./examples/08_copy_identity.py)**

```python
"""얕은 복사와 중첩 객체의 공유를 확인."""

from copy import deepcopy

original = [{"id": "S-01", "scores": [80, 90]}]
shallow = original.copy()
deep = deepcopy(original)

shallow[0]["scores"][0] = 60
print("원본 점수:", original[0]["scores"])
print("얕은 복사 점수:", shallow[0]["scores"])
print("깊은 복사 점수:", deep[0]["scores"])
print("바깥 리스트는 같은 객체?:", original is shallow)
```

**실행 결과**

```text
원본 점수: [60, 90]
얕은 복사 점수: [60, 90]
깊은 복사 점수: [80, 90]
바깥 리스트는 같은 객체?: False
```

### 2.8.2. 목적에 따른 자료구조 선택

| 필요한 동작 | 우선 고려할 자료구조 | 이유 |
|---|---|---|
| 순서를 유지하며 데이터를 추가 | List | 인덱스 접근과 순차 처리 |
| 고정된 위치의 값 묶음 | Tuple | 원소 변경을 허용하지 않음 |
| ID로 값 조회 | Dictionary | Key 기반 접근 |
| 중복 제거·멤버십 검사 | Set | 고유한 원소 관리 |
| 항목별 발생 횟수 | Counter | 빈도 계산 전용 기능 |
| 그룹별 값 누적·목록화 | defaultdict | 누락 Key의 기본값 생성 |

Dictionary와 Set은 일반적으로 Key의 해시를 이용한 효율적인 조회를 제공하지만, 모든 상황에 항상 일정한 성능을 보장하는 것은 아닙니다. 단순히 원소 개수가 적고 순서가 중요한 상황이라면 List도 충분할 수 있습니다.

**예제 코드 — [09_data_structure_selection.py](./examples/09_data_structure_selection.py)**

```python
"""자료구조 선택의 의미: 순서, 키 조회, 중복 제거."""

raw_ids = ["A-02", "A-01", "A-02", "A-03"]
unique_ids = list(dict.fromkeys(raw_ids))

scores = {"A-01": 84, "A-02": 92, "A-03": 77}
missing = "A-04"
print("원본 순서 유지 + 중복 제거:", unique_ids)
print("A-02 점수:", scores["A-02"])
print("미등록 학생 존재?:", missing in scores)

# 순서만 중요하면 list, Key 조회가 중요하면 dict,
# 순서 없는 고유값 집합이 필요하면 set을 고려합니다.
```

**실행 결과**

```text
원본 순서 유지 + 중복 제거: ['A-02', 'A-01', 'A-03']
A-02 점수: 92
미등록 학생 존재?: False
```

**주의할 점**

- 원본을 수정하는 메서드(`append`, `sort`, `update` 등)와 새 객체를 만드는 함수(`sorted`, 슬라이싱 등)를 구분합니다.
- `list.sort()`는 정렬된 List를 반환하지 않고 `None`을 반환합니다.
- `sum`, `list`, `dict`, `set`처럼 내장 함수·자료형 이름을 변수 이름으로 사용하지 않습니다.
- 값을 임의로 변환하거나 중복을 제거하기 전에 **중복이 실제 오류인지** 확인합니다. 동일한 도서가 여러 번 대출되거나 같은 상품이 여러 번 주문되는 기록은 정상일 수 있습니다.

---

<a id="section-2-9"></a>
## 2.9. Mini Project — Library Loan Report

이 Chapter의 자료구조를 함께 활용해 **도서관 대출 기록을 검증하고 분관별·분류별 통계를 요약하는 프로그램**을 작성합니다. 모든 데이터는 학습용 가상 기록입니다.

**입력 자료:** [library_loans.json](./data/library_loans.json) · [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)

| 처리 단계 | 사용 자료구조·도구 | 주요 작업 |
|---|---|---|
| 불러오기 | `list[dict]` | JSON 배열을 레코드 목록으로 해석 |
| 검증 | Dictionary, Set | 필수 필드와 고유 대출 번호 확인 |
| 정제 | `.copy()`, `.strip()` | 공백 제거, 원본 보존 |
| 빈도 집계 | Counter | 분류별 대출 건수 |
| 그룹 집계 | defaultdict | 분관별 대출 건수 |
| 고유값 | Set | 서로 다른 도서 수 계산 |
| 결과 정렬 | `sorted()`, Tuple Key | 분류 건수 내림차순, 동점 시 이름 오름차순 |

### 데이터 검증 규칙

- `loan_id`, `branch`, `book_id`, `category`, `status`는 비어 있지 않은 문자열이어야 합니다.
- `loan_id`는 공백 정리 후 **유효한 레코드 사이에서만 고유**해야 합니다. `book_id`는 여러 건에 다시 등장할 수 있습니다.
- `status`는 `borrowed` 또는 `returned`만 허용합니다.
- `days_overdue`는 0 이상의 정수여야 합니다. Python에서 `bool`은 `int`의 하위 클래스이므로 `type(days) is int`로 구분합니다.
- **현재 연체 건수**는 상태가 `borrowed`이고 연체 일수가 0보다 큰 기록만 계산합니다. 이 기준은 교육용 가정입니다.
- 검증 실패한 레코드는 집계에서 제외하고 오류 사유별 건수를 보관합니다.

### 실행 예제

입력 JSON을 읽을 때 `json.loads()`와 `Path.read_text()`를 사용합니다. 파일 입출력 자체는 Chapter 05에서 자세히 학습합니다. 이 Chapter에서는 읽어 들인 이후의 **List·Dictionary·Set 기반 데이터 구조와 처리 흐름**에 집중합니다.

**예제 코드 — [10_library_loan_report.py](./examples/10_library_loan_report.py)**

```python
"""Chapter 02 Mini Project: 도서관 대출 데이터 구조화 및 집계."""

import json
from collections import Counter, defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "library_loans.json"
REQUIRED_TEXT = ("loan_id", "branch", "book_id", "category", "status")


def validate_loan(row: object, seen: set[str]) -> tuple[dict | None, str | None]:
    """유효 레코드만 반환합니다. 원본 딕셔너리는 변경하지 않습니다."""
    if not isinstance(row, dict):
        return None, "레코드 형식 오류"
    if any(not isinstance(row.get(key), str) or not row[key].strip() for key in REQUIRED_TEXT):
        return None, "필수 문자열 오류"
    if row["status"] not in {"borrowed", "returned"}:
        return None, "대출 상태 오류"
    days = row.get("days_overdue")
    if type(days) is not int or days < 0:
        return None, "연체 일수 오류"

    cleaned = row.copy()
    for key in REQUIRED_TEXT:
        cleaned[key] = row[key].strip()
    if cleaned["loan_id"] in seen:
        return None, "대출 번호 중복"
    seen.add(cleaned["loan_id"])
    return cleaned, None


def summarize(records: list[object]) -> dict:
    """데이터 구조를 학습하기 위한 메모리 내 요약 기능."""
    seen: set[str] = set()
    valid: list[dict] = []
    errors: Counter[str] = Counter()

    for record in records:
        cleaned, reason = validate_loan(record, seen)
        if reason is not None:
            errors[reason] += 1
        else:
            valid.append(cleaned)

    categories = Counter(row["category"] for row in valid)
    by_branch: dict[str, int] = defaultdict(int)
    overdue_by_branch: Counter[str] = Counter()
    book_ids = set()

    for row in valid:
        branch = row["branch"]
        by_branch[branch] += 1
        book_ids.add(row["book_id"])
        if row["status"] == "borrowed" and row["days_overdue"] > 0:
            overdue_by_branch[branch] += 1

    return {
        "input_count": len(records),
        "valid_count": len(valid),
        "errors": errors,
        "unique_books": len(book_ids),
        "categories": categories,
        "by_branch": dict(by_branch),
        "overdue_by_branch": overdue_by_branch,
    }


def main() -> None:
    records = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("최상위 JSON 데이터는 배열이어야 합니다.")
    report = summarize(records)

    print("도서관 대출 현황")
    print(f"원본: {report['input_count']}건 | 유효: {report['valid_count']}건 | 제외: {sum(report['errors'].values())}건")
    print(f"고유 도서: {report['unique_books']}종")
    print("분류별 대출:")
    for category, count in sorted(report["categories"].items(), key=lambda item: (-item[1], item[0])):
        print(f"  {category}: {count}건")
    print("분관별 대출 / 현재 연체:")
    for branch in sorted(report["by_branch"]):
        print(f"  {branch}: {report['by_branch'][branch]}건 / {report['overdue_by_branch'][branch]}건")
    print("제외 사유:")
    for reason in sorted(report["errors"]):
        print(f"  {reason}: {report['errors'][reason]}건")


if __name__ == "__main__":
    main()
```

**실행 결과**

```text
도서관 대출 현황
원본: 15건 | 유효: 12건 | 제외: 3건
고유 도서: 10종
분류별 대출:
  과학: 5건
  문학: 4건
  역사: 3건
분관별 대출 / 현재 연체:
  동부: 4건 / 2건
  서부: 3건 / 2건
  중앙: 5건 / 1건
제외 사유:
  대출 번호 중복: 1건
  연체 일수 오류: 1건
  필수 문자열 오류: 1건
```

**핵심 코드 해설**

1. `validate_loan()`은 한 레코드의 필드·자료형·허용 범위·중복을 검사하고, 유효하면 정제된 Dictionary를 반환합니다.
2. `seen: set[str]`는 이미 통과한 `loan_id`의 고유성을 검사합니다. 잘못된 레코드의 ID는 Set에 추가하지 않습니다.
3. `Counter`로 분류별 건수를 계산하고, `defaultdict(int)`로 분관별 대출 수를 누적합니다.
4. `set()`으로 서로 다른 `book_id`의 개수를 구합니다. 같은 도서가 여러 번 대출된 기록은 삭제하지 않습니다.
5. 분류별 출력을 건수 내림차순·이름 오름차순으로 정렬해 실행마다 일정한 결과를 제공합니다.
6. 집계 결과는 새로운 자료구조에 보관하고, 입력 List와 개별 원본 Dictionary를 직접 수정하지 않습니다.

**실행 방법** — `Chapter-02/` 기준

```bash
python examples/10_library_loan_report.py
```

**기본 검증 테스트**

```bash
python tests/test_library_loan_report.py
```

위 테스트는 샘플 데이터 15건 중 정상 기록 12건, 오류 기록 3건, 고유 도서 10종, 분관별 집계 및 원본 데이터 보존 여부를 확인합니다. 비어 있는 입력과 `bool` 자료형을 잘못 사용한 경우도 점검합니다.

**확장 과제:** 가장 많이 이용된 분류를 하나만 출력하기, 연체 대출 비율 계산하기, 분관별 대출 빈도 정렬하기, 사용자 지정 분관만 집계하기 등을 추가해 보세요.

---

<a id="section-2-10"></a>
## 2.10. Coding Practice

다음 연습문제는 `exercises/` 폴더의 TODO를 직접 구현한 뒤 `solutions/`의 정답 코드와 비교하도록 구성했습니다. 모두 Python 표준 라이브러리만 사용합니다.

| 번호 | 실습 | 문제 파일 | 정답 코드 |
|:---:|---|---|---|
| 01 | Unique Visitors | [01_unique_visitors.py](./exercises/01_unique_visitors.py) | [01_unique_visitors.py](./solutions/01_unique_visitors.py) |
| 02 | Student Ranking | [02_student_ranking.py](./exercises/02_student_ranking.py) | [02_student_ranking.py](./solutions/02_student_ranking.py) |
| 03 | Inventory Summary | [03_inventory_summary.py](./exercises/03_inventory_summary.py) | [03_inventory_summary.py](./solutions/03_inventory_summary.py) |
| 04 | Top Categories | [04_top_categories.py](./exercises/04_top_categories.py) | [04_top_categories.py](./solutions/04_top_categories.py) |

### Exercise 01 — Unique Visitors

월요일과 화요일의 방문자 ID 목록에서 전체 고유 방문자 수와 양일 공통 방문자 ID를 계산합니다.

**구현 조건**

- 중복된 방문자 ID는 한 명으로 계산합니다.
- 공통 방문자 ID는 **오름차순**으로 출력합니다.
- 월요일 목록에서는 **첫 등장 순서를 유지하면서 중복을 제거**합니다.

**정답 실행 결과**

```text
전체 고유 방문자: 4
공통 방문자: ['U-02', 'U-03']
월요일 최초 방문 순서: ['U-01', 'U-02', 'U-03']
```

### Exercise 02 — Student Ranking

중첩 Dictionary에 보관된 학생별 과목 점수로 평균을 계산하고 성적 순위를 출력합니다.

**구현 조건**

- 두 과목의 산술평균을 사용합니다.
- 평균은 내림차순, 동일 점수이면 이름 오름차순으로 정렬합니다.
- 평균은 소수 첫째 자리까지 출력합니다.

**정답 실행 결과**

```text
1위 서아: 95.0점
2위 민지: 90.0점
3위 하준: 90.0점
4위 도윤: 85.0점
```

### Exercise 03 — Inventory Summary

품목별 재고 변동 기록을 누적하고 기록 건수를 함께 계산합니다.

**구현 조건**

- 양수는 입고, 음수는 출고로 간주하여 **순변동량**을 계산합니다.
- `defaultdict(int)` 또는 일반 Dictionary를 활용합니다.
- `Counter`로 기록 건수를 계산하고 품목명을 오름차순으로 출력합니다.

**정답 실행 결과**

```text
노트: 순변동 6개 / 기록 3건
연필: 순변동 9개 / 기록 2건
파일: 순변동 4개 / 기록 1건
```

### Exercise 04 — Top Categories

상품 분류별 금액 합계를 계산하고, 합계 순위를 출력한 다음 금액이 4,000원 이상인 분류만 추출합니다.

**구현 조건**

- 분류별 합계를 Dictionary에 누적합니다.
- 합계가 큰 순서대로, 동점이면 분류 이름 오름차순으로 정렬합니다.
- **4,000원 이상**인 분류만 별도 목록으로 출력합니다.

**정답 실행 결과**

```text
1위 음료: 4,400원
2위 간식: 4,200원
3위 문구: 4,200원
4위 기타: 700원
4,000원 이상: ['음료', '간식', '문구']
```

---

<a id="section-2-11"></a>
## 2.11. Quiz & Summary

### Quiz

1. List와 Tuple의 핵심 차이는 무엇인가요?
2. `record.get("age")`가 `None`을 반환할 때 반드시 `age` Key가 없다고 판단할 수 있나요?
3. Set을 순회하여 출력했을 때 원래 입력 순서를 항상 유지하나요?
4. 여러 학생의 이름·성적을 레코드 형태로 보관하려면 어떤 중첩 자료구조가 자연스러운가요?
5. `sorted(items)`와 `items.sort()`의 원본 수정 여부는 어떻게 다른가요?
6. 그룹별 발생 횟수와 그룹별 합계를 계산하려면 `Counter`와 `defaultdict(int)` 중 무엇을 선택하면 편리한가요?
7. `original.copy()`로 중첩된 List를 복사하면 내부 List도 모두 독립적으로 복사되나요?
8. 동일한 책(`book_id`)의 대출 기록이 두 건 있다면 중복 오류로 무조건 삭제해야 할까요?
9. `[x for x in values if x > 0]`은 어떤 자료구조를 반환하나요?
10. `sorted(records, key=lambda x: (-x["score"], x["name"]))`의 두 정렬 기준은 무엇인가요?

<details>
<summary><strong>Quiz 정답 확인</strong></summary>

1. List는 가변이며 Tuple은 원소의 추가·삭제·교체가 불가능합니다.
2. 아닙니다. Key가 있어도 저장된 값 자체가 `None`일 수 있습니다.
3. 아닙니다. Set은 순서를 보장하지 않으므로 `sorted()`를 사용합니다.
4. `list[dict]`처럼 여러 Dictionary를 List에 보관할 수 있습니다.
5. `sorted()`는 새 List를 반환하고 `list.sort()`는 원본을 수정합니다.
6. 횟수에는 `Counter`, 합계에는 `defaultdict(int)`가 편리합니다.
7. 아닙니다. 얕은 복사는 안쪽 가변 객체를 공유할 수 있습니다.
8. 아닙니다. 서로 다른 대출 거래라면 같은 도서가 재등장하는 것이 정상일 수 있습니다.
9. List를 반환합니다.
10. 점수 내림차순, 점수가 같으면 이름 오름차순입니다.

</details>

### Summary

- **List:** 순서가 있고 변경 가능한 데이터 목록
- **Tuple:** 위치와 구조가 고정된 시퀀스
- **Dictionary:** Key-Value를 사용한 레코드·조회·집계 표현
- **Set:** 고유값 관리, 합집합·교집합·차집합 처리
- **Nested Structures:** List와 Dictionary를 결합한 복합 레코드 표현
- **Comprehension:** 간결한 데이터 추출·변환·자료구조 생성
- **Sorting & Filtering:** `sorted()`와 조건식을 이용한 데이터 순서 및 범위 선택
- **`collections`:** `Counter`로 빈도 계산, `defaultdict`로 그룹별 누적
- **Copy & Mutation:** 원본 수정 여부와 얕은 복사·깊은 복사 차이 확인
- **Data Integrity:** 고유 Key, 중복 허용 여부, 누락 필드와 유효 범위 확인

다음 Chapter에서는 NumPy의 `ndarray`를 이용해 숫자 데이터를 하나의 배열로 관리하고, 인덱싱·브로드캐스팅·벡터화 연산을 학습합니다. 일반 Python 자료구조와 NumPy 배열의 특성을 비교하면서 **수치 데이터 처리**로 확장합니다.

## References

- [Python — Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python — Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [Python — Sorting HOWTO](https://docs.python.org/3/howto/sorting.html)
- [Python — `collections`](https://docs.python.org/3/library/collections.html)
- [Python — `copy`](https://docs.python.org/3/library/copy.html)
- [Python — `json`](https://docs.python.org/3/library/json.html)
- [Python — Built-in Functions](https://docs.python.org/3/library/functions.html)

---

[← Data Processing 목차](../README.md) · [Chapter 01](../Chapter-01/)
