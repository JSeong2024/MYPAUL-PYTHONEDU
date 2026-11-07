# Chapter 03. NumPy Fundamentals

NumPy의 **ndarray(다차원 배열)**를 중심으로 배열 생성, 자료형, 인덱싱, 수치 연산, 집계, Broadcasting, 난수 생성 및 벡터화를 학습합니다. Chapter 02의 Python 자료구조를 확장하여, 여러 측정값을 일정한 형태로 표현하고 효율적으로 계산하는 방법을 다룹니다.

본 자료는 **Python 3.13 이상과 NumPy 2.x**를 기준으로 작성하였으며, 예제는 NumPy 2.3.5 환경에서 실행 검증했습니다. NumPy 공식 문서의 2.5 버전 기능 설명도 참고했습니다. 운영체제와 패키지 버전에 따라 일부 출력 형식 및 난수 결과, 실행 시간은 달라질 수 있습니다.

**선행 학습:** [Chapter 01 — Introduction to Data Processing](../Chapter-01/) · [Chapter 02 — Python Data Structures](../Chapter-02/) · Python 조건문·반복문·함수 기초

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [3.1](#section-3-1) | Introduction to NumPy — 개념과 설치 |
| [3.2](#section-3-2) | ndarray & Array Metadata — shape, ndim, size, dtype |
| [3.3](#section-3-3) | Array Creation — 배열 생성 함수 |
| [3.4](#section-3-4) | Indexing, Slicing, Views & Copies |
| [3.5](#section-3-5) | Element-wise Operations & Universal Functions |
| [3.6](#section-3-6) | Aggregation & Axis — 배열 집계와 차원 |
| [3.7](#section-3-7) | Broadcasting — 서로 다른 배열 크기의 연산 |
| [3.8](#section-3-8) | Reshaping & Combining — 형태 변경과 결합 |
| [3.9](#section-3-9) | Boolean Masking & Conditional Selection |
| [3.10](#section-3-10) | Random Number Generation — Generator API |
| [3.11](#section-3-11) | Data Types, Memory & Numerical Precision |
| [3.12](#section-3-12) | Vectorization & Performance — 반복문과 비교 |
| [3.13](#section-3-13) | Mini Project — Sensor Temperature Quality Report |
| [3.14](#section-3-14) | Coding Practice |
| [3.15](#section-3-15) | Quiz & Summary |

## Getting Started

**가상환경에서 NumPy 설치** — Python 실행 명령은 환경에 따라 `py` 또는 `python3`일 수 있습니다.

```bash
python -m pip install --upgrade pip
python -m pip install numpy
python -c "import numpy as np; print(np.__version__)"
```

저장소의 `Data_Processing/Chapter-03/` 디렉터리를 기준으로 예제를 실행합니다.

```bash
python examples/01_array_creation.py
python examples/13_sensor_quality_report.py
python -m unittest discover -s tests -v
```

- Chapter 03의 예제는 **NumPy 외에 별도의 패키지가 필요하지 않습니다.**
- `examples/`는 완성된 설명용 코드, `exercises/`는 직접 완성할 코드, `solutions/`는 모범 정답입니다.
- `data/`에는 교육용 가상 데이터가 있으며, 원본을 수정하지 않습니다.
- Mini Project의 결과는 실행 후 `output/`에 생성되며 Git에는 포함하지 않습니다.


---

<a id="section-3-1"></a>
## 3.1. Introduction to NumPy — 개념과 설치

**NumPy(Numerical Python)**는 다차원 배열과 배열 기반 수치 연산을 지원하는 Python 라이브러리입니다. 중심 자료구조인 `numpy.ndarray`는 하나의 배열 안에 일정한 데이터 타입을 사용하며, 배열 전체에 수행할 연산을 간결하게 표현할 수 있습니다.

| 항목 | Python `list` | NumPy `ndarray` |
|---|---|---|
| 원소 자료형 | 서로 다른 타입을 함께 보관 가능 | 일반적인 배열은 공통 `dtype` 사용 |
| 주된 용도 | 범용 데이터 모음 | 수치 및 동종 데이터 연산 |
| `+` 연산 | 리스트 이어 붙이기 | 원소별 덧셈(호환 가능한 shape) |
| 반복 계산 | 직접 순회하는 경우가 많음 | 배열 연산·ufunc로 표현 가능 |
| 메모리 | Python 객체 참조 등의 관리 비용 | 동종 수치 데이터의 연속 버퍼 활용 가능 |

`ndarray`가 언제나 리스트보다 빠르거나 메모리를 적게 사용한다고 단정할 수는 없습니다. 배열의 크기, 자료형, 연산 방식, 중간 배열 생성 여부에 따라 달라집니다.

다음 코드는 같은 `+` 기호라도 두 자료구조에서 의미가 다르다는 점을 보여줍니다.

```python
import numpy as np

print([1, 2] + [3, 4])                  # [1, 2, 3, 4]
print(np.array([1, 2]) + np.array([3, 4]))  # [4 6]
```

`import numpy as np`는 널리 사용되는 별칭 규칙입니다. `np`를 강제하는 언어 규칙은 아니지만, 본 자료에서는 이를 통일하여 사용합니다.


---

<a id="section-3-2"></a>
## 3.2. ndarray & Array Metadata — shape, ndim, size, dtype

NumPy 배열의 **축(Axis)**은 데이터의 각 차원을 나타냅니다. 1차원 배열은 축이 하나이고, 일반적인 표 형태의 2차원 배열은 행과 열 두 축을 갖습니다. `shape`는 각 축의 길이를 나타내는 튜플입니다.

```text
1차원: [10, 20, 30]              shape=(3,)
2차원: [[1, 2, 3], [4, 5, 6]]    shape=(2, 3)
3차원: 두 개의 2×3 행렬          shape=(2, 2, 3)
```

| 속성 | 의미 | `(2, 3)` 실수 배열의 예 |
|---|---|---|
| `ndim` | 배열의 차원 수 | `2` |
| `shape` | 축별 크기 | `(2, 3)` |
| `size` | 전체 원소 수 | `6` |
| `dtype` | 배열의 원소 자료형 | `float64` |
| `itemsize` | 원소 하나의 바이트 수 | `8` |
| `nbytes` | 배열 데이터 버퍼의 바이트 수 | `48` |

`nbytes`는 원소 데이터의 총 크기로, Python 객체 전체의 메모리 사용량과는 구분됩니다. 같은 원소 수여도 `float32`, `float64`처럼 자료형에 따라 달라집니다.

**예제 코드 — [02_shape_dtype.py](./examples/02_shape_dtype.py)**

```python
"""ndarray의 크기, 차원, 원소 수 및 자료형 확인."""
import numpy as np

readings = np.array([[21.5, 23.0, 22.8], [24.1, 23.7, 22.0]])
print("배열:\n", readings, sep="")
print("shape:", readings.shape)
print("ndim:", readings.ndim)
print("size:", readings.size)
print("dtype:", readings.dtype)
print("itemsize:", readings.itemsize)
print("nbytes:", readings.nbytes)
```

**실행 결과**

```text
배열:
[[21.5 23.  22.8]
 [24.1 23.7 22. ]]
shape: (2, 3)
ndim: 2
size: 6
dtype: float64
itemsize: 8
nbytes: 48
```

배열의 크기를 점검하는 습관은 이후 Broadcasting, Reshaping 및 Pandas 데이터 변환을 이해하는 데 중요합니다.


---

<a id="section-3-3"></a>
## 3.3. Array Creation — 배열 생성 함수

배열은 Python의 List나 Tuple로 만들거나, NumPy의 생성 함수를 이용할 수 있습니다.

| 함수 | 기능 | 예 |
|---|---|---|
| `np.array()` | Python 시퀀스로 배열 생성 | `np.array([1, 2, 3])` |
| `np.zeros()` | 0으로 초기화 | `np.zeros((2, 3))` |
| `np.ones()` | 1로 초기화 | `np.ones(4)` |
| `np.full()` | 지정한 값으로 초기화 | `np.full((2, 2), 7)` |
| `np.arange()` | 일정 간격의 값 생성, 끝값 제외 | `np.arange(0, 10, 2)` |
| `np.linspace()` | 구간을 지정 개수로 등분 | `np.linspace(0, 1, 5)` |
| `np.eye()` | 대각 원소가 1인 2차원 배열 | `np.eye(3)` |
| `np.empty()` | 원소 값을 초기화하지 않은 배열 생성 | `np.empty(3)` |

`np.empty()`의 원소는 예측 가능한 기본값이 아닙니다. 값을 모두 다시 대입할 계획이 없으면 초기화된 배열을 사용하는 것이 안전합니다. 부동소수점 `np.arange()`는 누적 오차로 예상치 못한 원소 수가 될 수 있어, 구간 내 개수가 중요한 경우 `np.linspace()`를 고려합니다.

**예제 코드 — [01_array_creation.py](./examples/01_array_creation.py)**

```python
"""Python 시퀀스와 NumPy 생성 함수를 이용한 배열 만들기."""
import numpy as np

integers = np.array([10, 20, 30], dtype=np.int64)
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print("정수 배열:", integers)
print("2차원 배열:\n", matrix, sep="")
print("영행렬:\n", np.zeros((2, 3), dtype=int), sep="")
print("연속 값:", np.arange(0, 10, 2))
print("균등 간격:", np.linspace(0, 1, 5))
```

**실행 결과**

```text
정수 배열: [10 20 30]
2차원 배열:
[[1 2 3]
 [4 5 6]]
영행렬:
[[0 0 0]
 [0 0 0]]
연속 값: [0 2 4 6 8]
균등 간격: [0.   0.25 0.5  0.75 1.  ]
```

**예제의 `np.arange(0, 10, 2)`는 10을 포함하지 않고** `[0, 2, 4, 6, 8]`을 생성합니다. 생성 함수의 기본 `dtype`은 함수와 입력에 따라 달라질 수 있으므로 데이터 타입이 중요하면 명시적으로 지정합니다.


---

<a id="section-3-4"></a>
## 3.4. Indexing, Slicing, Views & Copies

인덱싱(Indexing)은 위치로 배열 값을 찾는 작업이며, 슬라이싱(Slicing)은 연속 구간을 선택하는 작업입니다. 2차원 배열에서는 `array[행, 열]`로 표현합니다.

| 표현 | 설명 |
|---|---|
| `a[0]` | 첫 번째 행 또는 첫 번째 원소 |
| `a[1, 2]` | 두 번째 행, 세 번째 열 |
| `a[:, 1]` | 모든 행의 두 번째 열 |
| `a[1:, :2]` | 두 번째 행부터, 처음 두 열 |
| `a[[0, 2]]` | 첫 번째·세 번째 행을 고급 인덱싱으로 선택 |

**예제 코드 — [03_indexing_slicing.py](./examples/03_indexing_slicing.py)**

```python
"""2차원 배열의 인덱싱과 슬라이싱."""
import numpy as np

scores = np.array([[80, 90, 70, 100],
                   [75, 85, 95,  90],
                   [88, 92, 84,  96]])
print("두 번째 학생:", scores[1])
print("세 번째 과목:", scores[:, 2])
print("앞의 두 학생 / 두 과목:\n", scores[:2, :2], sep="")
print("선택된 두 값:", scores[[0, 2], [1, 3]])
```

**실행 결과**

```text
두 번째 학생: [75 85 95 90]
세 번째 과목: [70 95 84]
앞의 두 학생 / 두 과목:
[[80 90]
 [75 85]]
선택된 두 값: [90 96]
```

### 3.4.1. View와 Copy의 차이

- **View:** 원본과 같은 데이터 버퍼를 참조합니다. 값을 수정하면 원본에도 영향을 줄 수 있습니다.
- **Copy:** 독립된 데이터 버퍼를 생성합니다. 복사본을 수정해도 원본이 직접 변경되지 않습니다.
- **기본 슬라이싱:** 일반적으로 View를 반환합니다.
- **정수 배열·Boolean 고급 인덱싱:** 결과를 선택할 때 Copy를 반환합니다.
- **`copy()`**: 명시적으로 독립된 배열을 만듭니다.

**예제 코드 — [04_views_and_copies.py](./examples/04_views_and_copies.py)**

```python
"""슬라이싱 View와 정수 배열 인덱싱 Copy의 차이."""
import numpy as np

original = np.array([10, 20, 30, 40, 50])
view = original[1:4]
view[0] = 99
print("View 변경 후 원본:", original)
print("View 공유 여부:", np.shares_memory(original, view))

selected = original[[1, 3]]  # 고급 인덱싱: 새로운 배열
selected[0] = -1
print("고급 인덱싱 변경 후 원본:", original)
print("고급 인덱싱 공유 여부:", np.shares_memory(original, selected))

independent = original.copy()
independent[0] = -100
print("copy() 변경 후 원본:", original)
```

**실행 결과**

```text
View 변경 후 원본: [10 99 30 40 50]
View 공유 여부: True
고급 인덱싱 변경 후 원본: [10 99 30 40 50]
고급 인덱싱 공유 여부: False
copy() 변경 후 원본: [10 99 30 40 50]
```

`np.shares_memory()`는 두 배열이 메모리를 공유하는지를 확인하는 도구입니다. `reshape()`나 `ravel()`과 같은 변환은 입력 메모리 배치에 따라 View 또는 Copy가 될 수 있으므로 일률적으로 가정하지 않습니다.


---

<a id="section-3-5"></a>
## 3.5. Element-wise Operations & Universal Functions

NumPy 배열에서는 사칙연산과 비교 연산을 **원소별(Element-wise)**로 적용할 수 있습니다. 반복문 대신 계산 규칙을 배열 단위로 표현하는 방식을 **벡터화(Vectorization)**라고 부릅니다.

| 연산 | 설명 |
|---|---|
| `a + b`, `a - b` | 원소별 덧셈·뺄셈 |
| `a * b`, `a / b` | 원소별 곱셈·나눗셈 |
| `a ** 2` | 원소별 제곱 |
| `np.sqrt(a)` | 원소별 제곱근 |
| `np.abs(a)` | 원소별 절댓값 |
| `np.round(a, 2)` | 소수점 자리 반올림 |
| `a @ b` | 행렬 곱(규칙에 맞는 차원 필요) |

**Universal Function(ufunc)**은 배열 원소에 연산을 적용하도록 구현된 NumPy의 함수 체계입니다. `np.sqrt()`, `np.add()`, `np.maximum()` 등이 대표적인 예입니다.

**예제 코드 — [05_elementwise_operations.py](./examples/05_elementwise_operations.py)**

```python
"""원소별 연산과 범용 함수(ufunc)."""
import numpy as np

quantity = np.array([2, 3, 1])
unit_price = np.array([1500, 2000, 5000])
sales = quantity * unit_price
print("판매액:", sales)
print("총판매액:", sales.sum())

celsius = np.array([0.0, 20.0, 35.0])
fahrenheit = celsius * 9 / 5 + 32
print("화씨:", fahrenheit)
print("제곱근:", np.sqrt(np.array([1, 4, 9])))
```

**실행 결과**

```text
판매액: [3000 6000 5000]
총판매액: 14000
화씨: [32. 68. 95.]
제곱근: [1. 2. 3.]
```

이 예제는 각 상품의 `수량 × 단가`를 배열 연산으로 한 번에 계산합니다. 다만 `np.array([1, 2]) * np.array([3, 4])`는 `[3, 8]`로 계산되며 행렬 곱과 다릅니다. 행렬 곱은 차원 조건을 만족하는 경우 `@` 또는 `np.matmul()`을 사용합니다.


---

<a id="section-3-6"></a>
## 3.6. Aggregation & Axis — 배열 집계와 차원

집계(Aggregation)는 여러 원소를 하나의 요약값 또는 축별 요약값으로 만드는 작업입니다. `sum()`, `mean()`, `min()`, `max()`, `std()` 등을 활용합니다.

2차원 배열에서 `axis`는 **집계할 때 줄어드는 축**을 의미합니다.

```text
            과목1 과목2 과목3
학생1        80    90    70
학생2        85    75    95

axis=0 → 학생(행) 방향으로 합치므로 과목(열)별 결과
axis=1 → 과목(열) 방향으로 합치므로 학생(행)별 결과
```

| 코드 | 결과 크기 | 의미 |
|---|---|---|
| `a.mean()` | 스칼라 | 전체 평균 |
| `a.mean(axis=0)` | `(열 수,)` | 열별 평균 |
| `a.mean(axis=1)` | `(행 수,)` | 행별 평균 |
| `a.mean(axis=1, keepdims=True)` | `(행 수, 1)` | 축을 길이 1로 유지 |

산술평균은 다음과 같이 계산합니다.

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

`np.nan`이 포함된 배열에 일반 `mean()`을 호출하면 결과에 `nan`이 전파될 수 있습니다. `np.nanmean()`은 NaN 값을 계산에서 제외하지만 **행이나 열의 값이 전부 NaN인 경우** 경고와 함께 NaN을 반환할 수 있으므로, 입력 검증이 필요합니다.

**예제 코드 — [06_aggregation_axis.py](./examples/06_aggregation_axis.py)**

```python
"""axis별 평균·합계 및 NaN을 제외한 집계."""
import numpy as np

scores = np.array([[80.0, 90.0, 70.0],
                   [85.0, 75.0, 95.0]])
print("전체 평균:", scores.mean())
print("열별 평균(axis=0):", scores.mean(axis=0))
print("행별 평균(axis=1):", scores.mean(axis=1))
print("열별 합계:", scores.sum(axis=0))

with_missing = np.array([21.0, np.nan, 25.0])
print("NaN 제외 평균:", np.nanmean(with_missing))
print("행 평균 유지 차원:", scores.mean(axis=1, keepdims=True).shape)
```

**실행 결과**

```text
전체 평균: 82.5
열별 평균(axis=0): [82.5 82.5 82.5]
행별 평균(axis=1): [80. 85.]
열별 합계: [165. 165. 165.]
NaN 제외 평균: 23.0
행 평균 유지 차원: (2, 1)
```

`np.std()`는 기본적으로 모집단 표준편차(`ddof=0`)를 계산합니다. 통계적으로 표본 표준편차가 필요한 경우에는 `ddof=1`이 적절한지 별도로 판단해야 합니다. 데이터 개수가 0인 경우의 집계도 무조건 유효한 값이 나오지는 않습니다.


---

<a id="section-3-7"></a>
## 3.7. Broadcasting — 서로 다른 배열 크기의 연산

**Broadcasting**은 배열의 차원 크기가 달라도 일정한 규칙을 만족하면 원소별 연산이 가능하도록 하는 기능입니다. 주로 각 열에 보정값을 더하거나, 모든 원소에 같은 상수를 적용할 때 사용합니다.

### 3.7.1. Broadcasting 규칙

두 배열의 `shape`를 **오른쪽 끝 차원부터 비교**합니다. 각 차원에서 크기가 같거나, 둘 중 하나가 `1`이면 호환됩니다. 짧은 `shape`의 왼쪽에는 크기가 1인 차원이 있는 것처럼 비교합니다.

| A의 shape | B의 shape | 결과 |
|---|---|---|
| `(2, 3)` | `(3,)` | `(2, 3)` |
| `(2, 3)` | `(2, 1)` | `(2, 3)` |
| `(3, 1)` | `(1, 4)` | `(3, 4)` |
| `(2, 3)` | `(4,)` | **불가능** |

### 3.7.2. 수치 예제

**예제 코드 — [07_broadcasting.py](./examples/07_broadcasting.py)**

```python
"""서로 다른 shape의 배열을 호환 가능한 차원으로 계산."""
import numpy as np

readings = np.array([[20.0, 22.0, 24.0],
                     [19.0, 21.0, 25.0]])   # (2, 3)
offsets = np.array([0.5, -0.5, 1.0])       # (3,)
corrected = readings + offsets
print("센서별 보정:\n", corrected, sep="")

row_offsets = np.array([[0.0], [2.0]])    # (2, 1)
print("행별 추가 보정:\n", corrected + row_offsets, sep="")
print("계산 결과 shape:", np.broadcast_shapes((2, 3), (3,)))

try:
    np.broadcast_shapes((2, 3), (4,))
except ValueError:
    print("(2, 3)과 (4,)는 Broadcasting 불가")
```

**실행 결과**

```text
센서별 보정:
[[20.5 21.5 25. ]
 [19.5 20.5 26. ]]
행별 추가 보정:
[[20.5 21.5 25. ]
 [21.5 22.5 28. ]]
계산 결과 shape: (2, 3)
(2, 3)과 (4,)는 Broadcasting 불가
```

`offsets`의 `shape=(3,)`이므로 각 행의 세 센서에 동일한 순서로 적용합니다. 반면 `row_offsets`는 `(2, 1)`이므로 각 행의 모든 열에 해당 행의 보정값을 더합니다.

**주의:** Broadcasting은 큰 중간 결과 배열을 생성하는 식으로 사용하면 메모리 사용량이 증가할 수 있습니다. 형태가 맞는다는 이유만으로 항상 효율적인 것은 아닙니다.


---

<a id="section-3-8"></a>
## 3.8. Reshaping & Combining — 형태 변경과 결합

데이터는 원소 개수를 유지하면서 새로운 차원으로 배열하거나, 여러 배열을 하나로 연결할 수 있습니다.

| 도구 | 역할 | 주의 |
|---|---|---|
| `reshape()` | 원소를 다른 차원 배치로 표현 | 전체 원소 수 동일 필요 |
| `.T` | 축 순서를 뒤집는 Transpose | 2차원에서는 행·열 전환 |
| `np.concatenate()` | 기존 축을 따라 이어 붙임 | 나머지 축 크기 호환 필요 |
| `np.stack()` | 새 축을 추가해 배열을 쌓음 | 입력 배열의 shape 동일 필요 |
| `np.ravel()` | 1차원 배열로 펼침 | View/Copy 여부에 주의 |

예를 들어 `(6,)` 배열은 `(2, 3)`으로 바꿀 수 있지만 `(2, 4)`로 바꾸면 원소가 부족하여 오류가 발생합니다.

**예제 코드 — [08_reshape_stack.py](./examples/08_reshape_stack.py)**

```python
"""형태 변경, 축 교환, 배열 이어 붙이기 및 쌓기."""
import numpy as np

values = np.arange(1, 7)
matrix = values.reshape(2, 3)
print("reshape:\n", matrix, sep="")
print("transpose:\n", matrix.T, sep="")

first = np.array([10, 20])
second = np.array([30, 40])
print("concatenate:", np.concatenate([first, second]))
print("stack:\n", np.stack([first, second]), sep="")
```

**실행 결과**

```text
reshape:
[[1 2 3]
 [4 5 6]]
transpose:
[[1 4]
 [2 5]
 [3 6]]
concatenate: [10 20 30 40]
stack:
[[10 20]
 [30 40]]
```

`np.concatenate([first, second])`는 두 개의 1차원 배열을 길게 연결하고, `np.stack([first, second])`는 **새로운 축**을 만들어 2차원 배열로 결합한다는 차이가 있습니다.


---

<a id="section-3-9"></a>
## 3.9. Boolean Masking & Conditional Selection

조건식의 결과인 Boolean 배열을 **Mask(마스크)**로 이용하면 필요한 데이터만 선택할 수 있습니다.

```python
import numpy as np
values = np.array([10, 20, 30, 40])
selected = values[values >= 25]  # [30 40]
```

| 구문 | 의미 |
|---|---|
| `a > 30` | 조건별 참·거짓 배열 |
| `a[(a >= 0) & (a <= 45)]` | 여러 조건을 만족하는 값 선택 |
| `~mask` | Boolean 조건 반전 |
| `np.where(mask, x, y)` | 조건에 따라 x 또는 y 선택 |
| `np.count_nonzero(mask)` | 참인 원소 개수 세기 |

NumPy 배열 조건에서는 Python의 `and`/`or` 대신 `&`/`|`를 사용하고, **각 조건식을 괄호로 감싸는 습관**이 필요합니다.

**예제 코드 — [09_boolean_masking.py](./examples/09_boolean_masking.py)**

```python
"""조건부 선택, 결측 표식 처리, np.where()."""
import numpy as np

temperatures = np.array([22.5, -999.0, 31.2, 47.0, 25.0])
missing = temperatures == -999.0
in_range = (temperatures >= 0) & (temperatures <= 45)
valid = ~missing & in_range

cleaned = np.where(valid, temperatures, np.nan)
print("유효 데이터:", temperatures[valid])
print("제외 개수:", np.count_nonzero(~valid))
print("정제 배열:", cleaned)
print("유효 데이터 평균:", round(float(np.nanmean(cleaned)), 2))
print("30도 초과:", temperatures[valid & (temperatures > 30)])
```

**실행 결과**

```text
유효 데이터: [22.5 31.2 25. ]
제외 개수: 2
정제 배열: [22.5  nan 31.2  nan 25. ]
유효 데이터 평균: 26.23
30도 초과: [31.2]
```

이 예제의 `-999`는 교육용 데이터셋에서 **누락을 뜻하는 약속된 표식**입니다. 모든 실제 데이터에 통용되는 결측치 규칙은 아닙니다. `np.nan`은 부동소수점 배열에서 누락 또는 유효하지 않은 값을 표시할 때 사용할 수 있으며, 데이터 의미를 확인한 뒤 변환해야 합니다.


---

<a id="section-3-10"></a>
## 3.10. Random Number Generation — Generator API

난수는 모의 실험, 임의 샘플링, 테스트 데이터 생성 등에 활용할 수 있습니다. 새로운 코드에서는 `np.random.default_rng()`로 **Generator 객체**를 만드는 방식을 권장합니다.

| 메서드 | 용도 | 예 |
|---|---|---|
| `rng.integers(low, high, size)` | 정수 난수, 상한 제외 | `rng.integers(1, 7, 10)` |
| `rng.random(size)` | `[0, 1)`의 실수 난수 | `rng.random(5)` |
| `rng.normal(loc, scale, size)` | 정규분포 난수 | `rng.normal(0, 1, 10)` |
| `rng.choice(values, size)` | 값 샘플링 | `rng.choice(["A", "B"], 3)` |
| `rng.shuffle(a)` | 배열을 제자리에서 섞음 | `rng.shuffle(a)` |

**Seed(시드)**는 난수 Generator 초기화에 사용하는 값입니다. 같은 Generator 구현과 환경에서 같은 Seed와 동일한 호출 순서를 사용하면 결과를 재현할 수 있습니다. NumPy는 모든 버전과 Generator 구현에 걸쳐 난수열의 동일성을 보장하지는 않습니다.

**예제 코드 — [10_random_generator.py](./examples/10_random_generator.py)**

```python
"""새 Generator와 seed로 재현 가능한 수치 실험 만들기."""
import numpy as np

rng = np.random.default_rng(2026)
dice = rng.integers(1, 7, size=8)  # 1~6 정수. upper bound는 제외
noise = rng.normal(loc=0.0, scale=1.0, size=4)
print("주사위:", dice)
print("표준정규 난수:", np.round(noise, 2))

repeated = np.random.default_rng(2026).integers(1, 7, size=8)
print("같은 초기 조건:", np.array_equal(dice, repeated))
```

**실행 결과**

```text
주사위: [6 2 1 4 3 3 1 3]
표준정규 난수: [ 0.64 -0.29 -0.31  0.3 ]
같은 초기 조건: True
```

기존 문서에서 사용한 `np.random.seed()`나 `np.random.randint()`도 볼 수 있지만, 새 예제에서는 Generator API를 사용하겠습니다. 이러한 난수는 **암호화 키나 비밀번호 생성용 보안 난수로 사용하면 안 됩니다.**


---

<a id="section-3-11"></a>
## 3.11. Data Types, Memory & Numerical Precision

NumPy에서는 정수·부동소수점 등의 자료형(`dtype`)을 명시할 수 있습니다. 어떤 자료형을 선택하는지는 수치 범위, 정밀도, 메모리 사용량에 영향을 줍니다.

| dtype 예 | 원소당 크기 | 사용 사례 |
|---|---|---|
| `np.int16` | 2 byte | 제한된 범위의 정수 |
| `np.int32` | 4 byte | 비교적 큰 정수 |
| `np.int64` | 8 byte | 큰 범위의 정수 |
| `np.float32` | 4 byte | 메모리 사용을 줄이는 실수 배열 |
| `np.float64` | 8 byte | 일반적인 고정밀 수치 계산 |
| `np.bool_` | 보통 1 byte | 조건 마스크 |

`astype()`는 자료형을 변환하며 필요한 경우 새 버퍼를 만듭니다. 작은 자료형으로의 변환은 데이터가 범위를 벗어나거나 정밀도가 낮아질 수 있습니다. 자료형 변환 전에 `np.iinfo()`, `np.finfo()` 등으로 범위를 확인할 수 있습니다.

**예제 코드 — [11_dtypes_precision.py](./examples/11_dtypes_precision.py)**

```python
"""자료형과 메모리, 변환, 부동소수점 비교 주의."""
import numpy as np

small = np.array([1.1, 2.2, 3.3], dtype=np.float32)
wide = small.astype(np.float64)
print("float32 bytes:", small.nbytes)
print("float64 bytes:", wide.nbytes)
print("float32 -> float64:", wide.dtype)

value = np.float64(0.1) + np.float64(0.2)
print("0.1 + 0.2 == 0.3:", value == 0.3)
print("isclose:", bool(np.isclose(value, 0.3)))
print("int16 범위:", np.iinfo(np.int16).min, np.iinfo(np.int16).max)
```

**실행 결과**

```text
float32 bytes: 12
float64 bytes: 24
float32 -> float64: float64
0.1 + 0.2 == 0.3: False
isclose: True
int16 범위: -32768 32767
```

컴퓨터의 이진 부동소수점은 일부 십진수를 정확히 표현할 수 없습니다. 따라서 `0.1 + 0.2 == 0.3`처럼 **실수의 직접 동일성 검사**가 의도와 다를 수 있습니다. 숫자의 크기와 허용 오차에 적절한 `np.isclose()` 또는 `np.allclose()`를 사용하고, 필요하다면 허용 오차를 명시합니다.

**중요:** `np.isclose()`는 모든 데이터 의미를 자동으로 이해하지 않습니다. 특히 매우 작은 값이나 0 근처의 비교에는 `atol` 선택이 결과에 큰 영향을 미칠 수 있습니다.


---

<a id="section-3-12"></a>
## 3.12. Vectorization & Performance — 반복문과 비교

NumPy는 반복적인 수치 연산을 Python 코드의 개별 반복문 대신 배열 연산으로 실행할 수 있습니다. 다만 처리 시간은 데이터 크기, 배열 생성 비용, 메모리 접근 방식, 라이브러리 빌드 등 여러 요소에 따라 달라집니다.

다음 예제는 **동일한 계산 결과**를 먼저 확인하고, `timeit.repeat()`로 여러 번 측정한 시간 중 최소값을 비교합니다. 측정 대상 함수와 입력 크기를 명시하므로 결과를 다시 재현해볼 수 있습니다.

**예제 코드 — [12_vectorization_performance.py](./examples/12_vectorization_performance.py)**

```python
"""같은 계산을 Python 루프와 NumPy로 실행해 소요 시간 비교."""
import timeit
import numpy as np

values = list(range(100_000))
array = np.array(values)

def with_python():
    return [value * 2 + 1 for value in values]

def with_numpy():
    return array * 2 + 1

assert np.array_equal(np.array(with_python()), with_numpy())
t_python = min(timeit.repeat(with_python, number=3, repeat=3))
t_numpy = min(timeit.repeat(with_numpy, number=3, repeat=3))
print("계산 결과 일치: True")
print(f"Python 반복: {t_python * 1000:.2f} ms (3회 호출)")
print(f"NumPy 연산: {t_numpy * 1000:.2f} ms (3회 호출)")
print("측정값은 하드웨어·환경에 따라 달라집니다.")
```

**실행 결과**

```text
계산 결과 일치: True
Python 반복: [측정값] ms (3회 호출)
NumPy 연산: [측정값] ms (3회 호출)
측정값은 하드웨어·환경에 따라 달라집니다.
```

위 실행 결과의 `[측정값]`은 각자의 환경에서 출력되는 밀리초 단위 실행 시간입니다. 해당 수치를 성능 보장 또는 일반적인 속도 배율로 해석해서는 안 됩니다.

**성능 점검 순서:** 결과 정확성 확인 → 실제 입력 규모에서 측정 → 병목 확인 → 자료형과 중간 배열 최소화. 반복문이 무조건 잘못된 것은 아니며, 데이터 구조가 작거나 복잡한 제어 흐름이 필요한 경우 Python 코드가 더 읽기 쉬울 수 있습니다.


---

<a id="section-3-13"></a>
## 3.13. Mini Project — Sensor Temperature Quality Report

이 프로젝트에서는 **4개 가상 센서의 7일간 온도 측정값**을 NumPy 2차원 배열로 불러오고, 품질 검사 후 일별·센서별 평균과 경보 횟수를 계산하여 CSV로 저장합니다.

**입력 자료:** [weekly_temperatures.csv](./data/weekly_temperatures.csv) · [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)

| 항목 | 규칙 |
|---|---|
| `-999` | 이 파일에서만 결측치로 취급 |
| `0~45°C` | 본 프로젝트의 유효 온도 범위(양 끝 포함) |
| `>30°C` | 유효한 온도 중 경보로 분류 |
| NaN 또는 Infinity | 범위 오류로 분류 |
| 집계 | 무효 측정값 제외 후 평균 계산 |

**처리 순서**

1. `np.loadtxt()`로 헤더와 날짜 열을 제외한 온도 값을 `(7, 4)` 배열로 불러옵니다.
2. 결측 표식, 범위 오류, 정상값을 Boolean Mask로 구분합니다.
3. 무효값을 `np.nan`으로 바꾸고 일별·센서별 평균을 계산합니다.
4. 정상값 가운데 `30°C`를 초과한 항목의 개수를 셉니다.
5. `output/sensor_summary.csv`에 센서별 평균과 경보 횟수를 저장합니다.

**예제 코드 — [13_sensor_quality_report.py](./examples/13_sensor_quality_report.py)**

```python
"""Mini Project: 온도 센서 행렬의 품질 검사와 집계 및 CSV 출력."""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "weekly_temperatures.csv"
OUTPUT = ROOT / "output" / "sensor_summary.csv"
SENSOR_NAMES = ("ST-01", "ST-02", "ST-03", "ST-04")

def analyze_measurements(raw: np.ndarray) -> dict:
    """행=날짜, 열=센서인 2차원 측정값을 검사합니다."""
    readings = np.asarray(raw, dtype=np.float64)
    if readings.ndim != 2 or readings.shape[1] != len(SENSOR_NAMES):
        raise ValueError("(날짜 수, 4) 형태의 입력이 필요합니다.")
    if readings.shape[0] == 0:
        raise ValueError("측정 날짜가 하나 이상 필요합니다.")

    missing = readings == -999.0
    out_of_range = (~np.isfinite(readings) | (readings < 0) | (readings > 45)) & ~missing
    valid = ~missing & ~out_of_range
    if not np.all(valid.any(axis=0)) or not np.all(valid.any(axis=1)):
        raise ValueError("각 날짜와 센서에 유효한 값이 하나 이상 필요합니다.")

    clean = np.where(valid, readings, np.nan)
    alarms = valid & (readings > 30)
    return {
        "raw_count": readings.size,
        "missing_count": int(np.count_nonzero(missing)),
        "range_error_count": int(np.count_nonzero(out_of_range)),
        "valid_count": int(np.count_nonzero(valid)),
        "alarm_count": int(np.count_nonzero(alarms)),
        "daily_mean": np.nanmean(clean, axis=1),
        "sensor_mean": np.nanmean(clean, axis=0),
        "sensor_alarm_count": np.count_nonzero(alarms, axis=0),
    }

def load_data(path: Path = INPUT) -> np.ndarray:
    return np.loadtxt(path, delimiter=",", skiprows=1, usecols=(1, 2, 3, 4))

def save_report(stats: dict, path: Path = OUTPUT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    report = np.column_stack((
        np.arange(1, len(SENSOR_NAMES) + 1),
        stats["sensor_mean"],
        stats["sensor_alarm_count"],
    ))
    np.savetxt(
        path, report, delimiter=",", fmt=["%d", "%.2f", "%d"],
        header="sensor_number,mean_temperature_c,alarm_count", comments="",
        encoding="utf-8",
    )

def main() -> None:
    raw = load_data()
    stats = analyze_measurements(raw)
    save_report(stats)
    print("원본 측정값:", stats["raw_count"])
    print("결측(-999):", stats["missing_count"])
    print("범위 오류:", stats["range_error_count"])
    print("유효 측정값:", stats["valid_count"])
    print("30°C 초과 경보:", stats["alarm_count"])
    print("일별 평균(°C):", np.round(stats["daily_mean"], 2))
    print("센서별 평균(°C):", np.round(stats["sensor_mean"], 2))
    print("센서별 경보 횟수:", stats["sensor_alarm_count"])
    print("저장:", OUTPUT.relative_to(ROOT).as_posix())

if __name__ == "__main__":
    main()
```

**실행 결과**

```text
원본 측정값: 28
결측(-999): 1
범위 오류: 1
유효 측정값: 26
30°C 초과 경보: 2
일별 평균(°C): [22.82 23.6  23.2  23.75 25.35 25.   23.5 ]
센서별 평균(°C): [22.51 25.86 22.62 24.63]
센서별 경보 횟수: [0 2 0 0]
저장: output/sensor_summary.csv
```

**생성되는 파일** — `output/sensor_summary.csv`

```csv
sensor_number,mean_temperature_c,alarm_count
1,22.51,0
2,25.86,2
3,22.62,0
4,24.63,0
```

`np.savetxt()`를 사용하므로 출력 파일의 센서 번호는 `1~4`의 숫자로 표현합니다. 실제 장치 ID는 [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)에서 `ST-01`~`ST-04`로 확인할 수 있습니다. 문자열과 수치 열을 함께 관리하는 방법은 Chapter 04의 Pandas에서 다룹니다.

**검증:** 입력 형상이 `(날짜 수, 4)`가 아니거나, 특정 날짜 또는 센서의 값이 모두 무효라면 `ValueError`가 발생하도록 처리했습니다. 원본 CSV는 수정하지 않습니다.

**실행**

```bash
python examples/13_sensor_quality_report.py
python -m unittest discover -s tests -v
```


---

<a id="section-3-14"></a>
## 3.14. Coding Practice

각 문제는 `exercises/`에 **미완성 코드**가 있고, 대응하는 `solutions/`에 정답 코드가 있습니다. 아래의 **예상 실행 결과**를 기준으로 스스로 구현한 뒤 정답을 확인하세요. Exercises 파일은 일부러 `NotImplementedError`를 발생시키며, 정답을 채우기 전에는 완료되지 않은 상태가 정상입니다.

| 번호 | 문제 | Exercise | Solution |
|:---:|---|---|---|
| 01 | Array Metrics | [01_array_metrics.py](./exercises/01_array_metrics.py) | [01_array_metrics.py](./solutions/01_array_metrics.py) |
| 02 | Axis Summary | [02_axis_summary.py](./exercises/02_axis_summary.py) | [02_axis_summary.py](./solutions/02_axis_summary.py) |
| 03 | Sensor Calibration | [03_sensor_calibration.py](./exercises/03_sensor_calibration.py) | [03_sensor_calibration.py](./solutions/03_sensor_calibration.py) |
| 04 | Clean Temperature | [04_clean_temperature.py](./exercises/04_clean_temperature.py) | [04_clean_temperature.py](./solutions/04_clean_temperature.py) |
| 05 | Sales Broadcasting | [05_sales_broadcasting.py](./exercises/05_sales_broadcasting.py) | [05_sales_broadcasting.py](./solutions/05_sales_broadcasting.py) |

### Exercise 01 — Array Metrics — 개수·평균·최솟값·최댓값

수치 배열을 만들어 `size`, `mean()`, `min()`, `max()`를 계산합니다. 입력이 비어 있으면 `ValueError`를 발생시킵니다.

**예상 실행 결과**

```text
(4, 30.0, 15, 45)
```

### Exercise 02 — Axis Summary — 행별·열별 평균

2차원 배열을 입력받아 행별 평균과 열별 평균을 순서대로 반환합니다. 입력 형식과 빈 배열도 검증합니다.

**예상 실행 결과**

```text
(array([90., 75.]), array([70. , 82.5, 95. ]))
```

### Exercise 03 — Sensor Calibration — 센서별 보정값

측정값 행렬과 센서별 보정값의 shape를 검증한 다음 Broadcasting으로 각 열을 보정합니다.

**예상 실행 결과**

```text
[[20.5 20.5 23. ]
 [23.5 23.5 26. ]]
```

### Exercise 04 — Clean Temperature — 유효값만 집계

-999 또는 범위 밖의 값을 `np.nan`으로 바꾸고, 유효값의 평균을 계산합니다. 전부 무효이면 오류를 반환합니다.

**예상 실행 결과**

```text
[20. nan 25. nan 30.] 25.0
```

### Exercise 05 — Sales Broadcasting — 날짜별 매출 집계

수량 행렬 `(날짜, 상품)`에 상품 가격 벡터를 곱해 날짜별 매출 합계를 구합니다.

**예상 실행 결과**

```text
[4000 7500]
```

**테스트:** `python -m unittest discover -s tests -v` 명령으로 프로젝트와 `solutions/`의 동작을 확인할 수 있습니다. 연습문제를 직접 작성한 결과는 실행 및 출력 비교로 검증하세요. 테스트는 연습문제 파일에 답을 자동으로 입력하지 않습니다.


---

<a id="section-3-15"></a>
## 3.15. Quiz & Summary

다음 문제를 풀고, **각 문제 아래의 정답 및 해설을 개별적으로 펼쳐** 확인해 보세요. GitHub에서는 `<details>`를 클릭하면 해당 문항의 정답만 표시됩니다.

### Q1. 다음 배열의 `shape`는 무엇인가요? `np.array([[1, 2, 3], [4, 5, 6]])`

A. `(6,)` · B. `(2, 3)` · C. `(3, 2)` · D. `(2,)`

<details>
<summary>Q1. 정답 및 해설 확인</summary>

**정답: B — 행이 2개, 열이 3개이므로 `shape=(2, 3)`입니다.**

</details>

### Q2. `np.arange(2, 9, 2)`의 결과는 무엇인가요?

A. `[2, 4, 6, 8]` · B. `[2, 4, 6, 8, 9]` · C. `[2, 3, 4, 5, 6, 7, 8]` · D. `[2, 9]`

<details>
<summary>Q2. 정답 및 해설 확인</summary>

**정답: A — 시작 2부터 2씩 증가하지만 끝값 9는 포함되지 않습니다.**

</details>

### Q3. `np.array([1, 2, 3]) + 5`를 실행하면 무엇이 출력되나요?

A. `[1, 2, 3, 5]` · B. `[5, 5, 5]` · C. `[6, 7, 8]` · D. 오류

<details>
<summary>Q3. 정답 및 해설 확인</summary>

**정답: C — 스칼라 5가 배열의 각 원소에 더해집니다.**

</details>

### Q4. `(3, 1)` 배열과 `(1, 4)` 배열을 더할 때 결과의 `shape`는 무엇인가요?

A. `(3, 4)` · B. `(1, 4)` · C. `(3, 1)` · D. `(4, 3)`

<details>
<summary>Q4. 정답 및 해설 확인</summary>

**정답: A — 뒤쪽 차원부터 비교하면 1과 4, 3과 1이 각각 호환되므로 `(3, 4)`로 확장됩니다.**

</details>

### Q5. shape `(2, 3)` 배열에서 `mean(axis=0)`의 의미는 무엇인가요?

A. 행마다 한 값 계산 · B. 열마다 한 값 계산 · C. 전체 원소를 한 값으로 계산 · D. 2차원 배열을 그대로 반환

<details>
<summary>Q5. 정답 및 해설 확인</summary>

**정답: B — `axis=0`인 행 방향을 줄이므로 각 열의 평균이 계산되며 shape는 `(3,)`입니다.**

</details>

### Q6. 다음 코드가 끝난 뒤 `a`의 값은 무엇인가요? `a=np.array([10,20,30]); b=a[1:]; b[0]=99`

A. `[10, 20, 30]` · B. `[99, 20, 30]` · C. `[10, 99, 30]` · D. `[10, 20, 99]`

<details>
<summary>Q6. 정답 및 해설 확인</summary>

**정답: C — 일반 슬라이싱의 결과 `b`는 원본 `a`와 데이터를 공유하는 View이므로 두 번째 원소가 수정됩니다.**

</details>

### Q7. `x=np.array([2,4,6,8])`에서 `x[x>4]`의 결과는 무엇인가요?

A. `[2, 4]` · B. `[6, 8]` · C. `[4, 6, 8]` · D. `[True, True]`

<details>
<summary>Q7. 정답 및 해설 확인</summary>

**정답: B — 4보다 큰 값만 Boolean Mask로 선택하므로 6과 8이 남습니다.**

</details>

### Q8. 같은 시드로 새 Generator 두 개를 초기화하고 같은 API를 같은 순서로 호출하면, 같은 Generator 구현에서 어떤 결과를 기대할 수 있나요?

A. 호출마다 항상 새로운 순서 · B. 동일한 난수열 재현 · C. 모든 NumPy 버전에서 동일성 보장 · D. 암호학적으로 안전한 난수 생성

<details>
<summary>Q8. 정답 및 해설 확인</summary>

**정답: B — 같은 Generator 구현과 동일한 호출 순서에서는 재현성을 기대할 수 있습니다. NumPy 버전 사이의 영구적인 동일성이나 암호학적 안전성은 보장하지 않습니다.**

</details>

### Q9. 원소가 5개인 `float32` 배열의 데이터 버퍼 크기(`nbytes`)는 얼마인가요?

A. 5 bytes · B. 10 bytes · C. 20 bytes · D. 40 bytes

<details>
<summary>Q9. 정답 및 해설 확인</summary>

**정답: C — `float32`는 원소당 4바이트이므로 `5 × 4 = 20`바이트입니다. 객체 전체 메모리 사용량을 뜻하지는 않습니다.**

</details>

### Q10. `np.nanmean(np.array([10.0, np.nan, 30.0]))`의 결과는 얼마인가요?

A. `10.0` · B. `20.0` · C. `30.0` · D. `nan`

<details>
<summary>Q10. 정답 및 해설 확인</summary>

**정답: B — NaN을 제외한 유효값 10과 30의 평균 `(10+30)/2`는 20입니다.**

</details>

### Summary

- **NumPy:** 다차원 배열 기반의 수치 연산 라이브러리입니다.
- **ndarray:** `shape`, `ndim`, `size`, `dtype`를 통해 배열 구조를 확인합니다.
- **인덱싱:** 일반 슬라이싱은 View를 반환하는 경우가 많으며, 고급 인덱싱은 Copy를 만듭니다.
- **원소별 연산:** `ufunc`와 벡터화로 수치 계산을 배열 단위로 표현합니다.
- **Axis:** 어느 차원을 줄이며 집계하는지 구분해야 합니다.
- **Broadcasting:** 오른쪽 끝 차원부터 크기가 같거나 1인지 비교합니다.
- **Mask:** Boolean 배열로 조건에 맞는 데이터를 선택합니다.
- **난수:** `np.random.default_rng()`로 Generator를 생성합니다.
- **정밀도:** dtype의 범위, 변환 오차, 부동소수점 비교를 고려합니다.
- **데이터 품질:** 결측·오류값의 의미를 검증하고 원본을 보존합니다.

## References

- [NumPy — Documentation](https://numpy.org/doc/stable/)
- [NumPy — Absolute Basics for Beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy — Array Creation](https://numpy.org/doc/stable/user/basics.creation.html)
- [NumPy — Indexing](https://numpy.org/doc/stable/user/basics.indexing.html)
- [NumPy — Copies and Views](https://numpy.org/doc/stable/user/basics.copies.html)
- [NumPy — Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [NumPy — Universal Functions](https://numpy.org/doc/stable/reference/ufuncs.html)
- [NumPy — Random Generator](https://numpy.org/doc/stable/reference/random/generator.html)
- [NumPy — Data Types](https://numpy.org/doc/stable/user/basics.types.html)
- [Python — timeit](https://docs.python.org/3/library/timeit.html)

---

[← Data Processing 목차](../README.md) · [← Chapter 02](../Chapter-02/)
