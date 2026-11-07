# Chapter 04. Pandas & DataFrames

Python의 **Pandas**를 이용해 표 형태의 데이터를 만들고, 읽고, 탐색하고, 선택하고, 가공하는 방법을 학습합니다. Chapter 02의 Python 자료구조와 Chapter 03의 NumPy 배열을 확장하여, 데이터의 **행(Row)·열(Column)·인덱스(Index)** 를 기준으로 작업하는 방법을 살펴봅니다.

본 자료의 예제는 **Python 3.13.5 / Pandas 2.2.3** 환경에서 실행 검증했습니다. Pandas 3.x에서 기본 동작으로 도입된 **Copy-on-Write(CoW)** 및 연결된 인덱싱(Chained Assignment) 관련 주의사항도 반영했습니다. 출력 형식과 문자열 열의 기본 자료형은 Pandas 버전 또는 실행 환경에 따라 달라질 수 있습니다.


<details>
<summary><strong>선행 학습 목록</strong></summary>

- [Chapter 01 — Introduction to Data Processing](../Chapter-01/)
- [Chapter 02 — Python Data Structures](../Chapter-02/)
- [Chapter 03 — NumPy Fundamentals](../Chapter-03/)
- [Chapter 04 — Pandas & DataFrames](../Chapter-04/)

</details>


<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [4.1](#section-4-1) | Introduction to Pandas — 데이터프레임의 역할 |
| [4.2](#section-4-2) | Series & DataFrame — 구조와 생성 |
| [4.3](#section-4-3) | Index & Columns — 행·열 이름 관리 |
| [4.4](#section-4-4) | Data Inspection — 기본 탐색과 요약 |
| [4.5](#section-4-5) | Data Selection — `loc`, `iloc` |
| [4.6](#section-4-6) | Filtering & Sorting — 조건 선택과 정렬 |
| [4.7](#section-4-7) | Column Operations — 파생 열과 안전한 수정 |
| [4.8](#section-4-8) | Data Types & Conversion — 문자열·숫자·날짜 |
| [4.9](#section-4-9) | Basic GroupBy — 그룹별 요약 |
| [4.10](#section-4-10) | String & Date Operations — 간단한 텍스트·날짜 처리 |
| [4.11](#section-4-11) | Copy-on-Write & Chained Assignment — 복사와 수정 규칙 |
| [4.12](#section-4-12) | Iteration & Vectorized Operations — 행 순회와 벡터화 |
| [4.13](#section-4-13) | CSV Export — 처리 결과 저장 |
| [4.14](#section-4-14) | Mini Project — Order Sales Report |
| [4.15](#section-4-15) | Coding Practice |
| [4.16](#section-4-16) | Quiz & Summary |

## Getting Started

### 개발 환경

- Python 3.13 이상 권장. 사용 중인 Pandas와 Python의 지원 관계를 확인하세요.
- Pandas 2.2 이상 또는 3.x 사용 가능. 예제 출력은 Pandas 2.2.3 기준으로 표기했습니다.
- Windows, macOS, Linux에서 실행 가능하며 VS Code 또는 Jupyter Notebook을 사용할 수 있습니다.

가상환경이 활성화된 상태에서 Pandas를 설치합니다.

```bash
python -m pip install pandas
python -c "import pandas as pd; print(pd.__version__)"
```

**`Data_Processing/Chapter-04/`** 디렉터리에서 실행합니다. 예제는 대부분 Python 파일 자신의 위치에서 실습 CSV 경로를 계산하므로 다른 작업 디렉터리에서 실행해도 동일한 데이터를 읽습니다.

```bash
python examples/01_series_dataframe.py
python examples/14_sales_report.py
python -m unittest discover -s tests -v
```

- `examples/`에는 완성된 예제, `exercises/`에는 미완성 코드, `solutions/`에는 모범답안이 들어 있습니다.
- 데이터는 `data/orders.csv`에 보관하며 자세한 컬럼 정의는 [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)를 참고하세요.
- 실습의 저장 결과는 `output/`에 생성되며, 원본 데이터는 수정하지 않습니다.
- Chapter 05에서 CSV·JSON·Excel·Parquet 등의 입출력을 자세히, Chapter 06에서 결측·중복·이상치 정제를, Chapter 07에서 결합·피벗·고급 집계를 다룹니다.

---

<a id="section-4-1"></a>
## 4.1. Introduction to Pandas — 데이터프레임의 역할

**Pandas**는 데이터 분석과 가공을 위한 Python 라이브러리입니다. 특히 여러 행과 열로 이루어진 **표 형식 데이터(Tabular Data)**를 다루는 데 적합합니다.

| 구조 | 역할 | 예시 |
|---|---|---|
| `list` / `dict` | Python의 범용 자료구조 | `[{"name": "A"}]` |
| NumPy `ndarray` | 주로 동종 원소의 다차원 배열 | 센서 측정값 행렬 |
| Pandas `Series` | 인덱스가 붙은 1차원 데이터 | 학생별 점수 |
| Pandas `DataFrame` | 열마다 자료형이 다를 수 있는 2차원 표 | 주문, 상품, 날짜, 가격 목록 |

Pandas의 `DataFrame`은 표의 각 열을 이름으로 찾을 수 있고, 행에는 인덱스를 부여합니다. NumPy를 모두 대체하는 도구는 아니며, 내부 배열과 확장 자료형을 함께 사용합니다.

```text
order_id  product  quantity  unit_price
ORD001    커피             2        3500
ORD002    노트             3        2500
```

`order_id`처럼 업무적으로 식별 가능한 값과 Pandas의 행 인덱스는 별개의 개념입니다. 기본적으로 CSV에서 `read_csv()`로 읽으면 0부터 시작하는 RangeIndex가 생성됩니다. 필요하면 고유 키를 인덱스로 지정할 수 있습니다.

---

<a id="section-4-2"></a>
## 4.2. Series & DataFrame — 구조와 생성

**`Series`는 1차원 인덱스 기반 데이터**, **`DataFrame`은 열 이름을 가진 2차원 데이터**를 나타냅니다. `Series`의 각 원소는 인덱스 레이블과 값의 쌍으로 볼 수 있습니다.

| 작성 방법 | 예시 | 반환 타입 |
|---|---|---|
| `pd.Series([10, 20])` | 한 개의 수치 열 | `Series` |
| `pd.DataFrame({"a": [1, 2]})` | 한 개 이상의 열 | `DataFrame` |
| `df["a"]` | 열 하나 선택 | 보통 `Series` |
| `df[["a"]]` | 열 하나를 표 형태로 선택 | `DataFrame` |

**예제 코드 — [01_series_dataframe.py](./examples/01_series_dataframe.py)**

```python
import pandas as pd

scores = pd.Series([82, 95, 78], index=["민수", "지은", "하나"], name="score")
students = pd.DataFrame({"name": ["민수", "지은", "하나"], "score": [82, 95, 78]})

print("Series:", scores.to_dict())
print("Series dtype:", scores.dtype)
print("DataFrame shape:", students.shape)
print(students.to_string(index=False))
```

**실행 결과**

```text
Series: {'민수': 82, '지은': 95, '하나': 78}
Series dtype: int64
DataFrame shape: (3, 2)
name  score
  민수     82
  지은     95
  하나     78
```



`Series`의 인덱스와 `DataFrame`의 첫 번째 열은 다릅니다. 인덱스는 행 선택이나 데이터 정렬(Alignment)에 관여하고, 실제 데이터 열은 `columns`에 포함됩니다.

---

<a id="section-4-3"></a>
## 4.3. Index & Columns — 행·열 이름 관리

`index`는 행을 식별하는 레이블이며, `columns`는 열의 이름을 담고 있습니다. 자료를 정렬하거나 그룹을 만들 때 인덱스가 예상과 다르게 작동하면 결과 해석이 달라질 수 있습니다.

| 작업 | 코드 | 의미 |
|---|---|---|
| 인덱스 조회 | `df.index` | 현재 행 인덱스 |
| 열 이름 조회 | `df.columns` | 열 레이블 목록 |
| 인덱스 변경 | `df.set_index("order_id")` | 주문 번호를 인덱스로 사용 |
| 인덱스 초기화 | `df.reset_index()` | 인덱스를 다시 열로 돌림 |
| 열 이름 변경 | `df.rename(columns={...})` | 지정한 열 이름 변경 |

**예제 코드 — [02_index_columns.py](./examples/02_index_columns.py)**

```python
from pathlib import Path
import pandas as pd

file_path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(file_path)
indexed = orders.set_index("order_id")
renamed = indexed.rename(columns={"unit_price": "price_krw"})

print("Index name:", indexed.index.name)
print("First order product:", indexed.loc["ORD001", "product"])
print("Renamed:", "price_krw" in renamed.columns)
print("Restored index:", indexed.reset_index().columns[0])
print("Original unchanged:", "unit_price" in orders.columns)
```

**실행 결과**

```text
Index name: order_id
First order product: 커피
Renamed: True
Restored index: order_id
Original unchanged: True
```



기본 `set_index()`와 `rename()`은 새 DataFrame을 반환하므로, 결과를 변수에 담아야 이후에도 사용할 수 있습니다. `order_id`에 중복값이 있다면 인덱스에 같은 레이블이 여러 개 존재할 수 있습니다. **인덱스가 항상 고유하다고 가정하지 마세요.**

### 4.3.1. 인덱스 기반 정렬(Alignment)

Pandas는 Series 사이의 연산에서 **원소의 위치보다 인덱스 레이블을 우선 맞춥니다.**

```python
import pandas as pd

left = pd.Series([10, 20], index=["A", "B"])
right = pd.Series([1, 2], index=["B", "A"])
print((left + right).to_dict())  # {'A': 12, 'B': 21}
```

단순 배열에서 같은 위치끼리 더하는 NumPy 연산과 달리, Pandas에서는 레이블의 일치 여부를 확인해야 합니다. 한쪽에만 있는 레이블은 일반적으로 결측 결과로 나타날 수 있습니다.

---

<a id="section-4-4"></a>
## 4.4. Data Inspection — 기본 탐색과 요약

처음 보는 데이터를 받았다면 먼저 **행 수·열 수, 컬럼 이름, 자료형, 결측 여부, 값의 범위**를 확인하는 것이 좋습니다.

| 기능 | 사용 예 | 의미 |
|---|---|---|
| 모양 | `df.shape` | `(행 개수, 열 개수)` |
| 앞부분 | `df.head(5)` | 앞 5개 행 |
| 뒷부분 | `df.tail(5)` | 끝 5개 행 |
| 구조 요약 | `df.info()` | 열, 자료형, 비결측 개수 등의 정보 |
| 통계 요약 | `df.describe()` | 수치형 열의 개수, 평균, 사분위수 등 |
| 자료형 | `df.dtypes` | 각 열의 dtype |
| 고유값 | `df["status"].unique()` | 해당 열에 등장하는 서로 다른 값 |
| 결측 개수 | `df.isna().sum()` | 열별 결측 개수 |

**예제 코드 — [03_inspection.py](./examples/03_inspection.py)**

```python
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
print("Shape:", orders.shape)
print("Columns:", orders.columns.tolist())
print("Order IDs:", orders.head(3)["order_id"].tolist())
print("Statuses:", sorted(orders["status"].unique().tolist()))
print("Quantity dtype:", orders["quantity"].dtype)
print("Quantity min/max:", orders["quantity"].min(), orders["quantity"].max())
print("Missing count:", int(orders.isna().sum().sum()))
```

**실행 결과**

```text
Shape: (20, 8)
Columns: ['order_id', 'order_date', 'region', 'category', 'product', 'quantity', 'unit_price', 'status']
Order IDs: ['ORD001', 'ORD002', 'ORD003']
Statuses: ['canceled', 'completed']
Quantity dtype: int64
Quantity min/max: 1 10
Missing count: 0
```



`shape`는 메서드가 아니라 속성이므로 `df.shape()`로 호출하지 않습니다. `describe()`의 기본 대상은 대개 수치형 열이며, 문자열 등 비수치형 열은 `include="all"` 옵션으로 함께 확인할 수 있습니다.

CSV로 읽은 날짜 문자열은 자동으로 날짜 자료형이 되지 않을 수 있습니다. 4.8에서 명시적으로 변환하는 방법을 학습합니다.

---

<a id="section-4-5"></a>
## 4.5. Data Selection — `loc`, `iloc`

`loc`와 `iloc`는 모두 행과 열을 선택하는 인덱서이지만 **선택 기준이 서로 다릅니다.**

| 구문 | 기준 | 예시 |
|---|---|---|
| `df.loc["ORD001"]` | 인덱스 레이블 | 주문 ID가 `ORD001`인 행 |
| `df.iloc[0]` | 0부터 시작하는 정수 위치 | 첫 번째 행 |
| `df.loc["ORD001":"ORD003"]` | 레이블 범위, 끝 포함 | 두 레이블을 포함한 구간 |
| `df.iloc[0:3]` | 정수 위치 범위, 끝 제외 | 위치 0·1·2 |
| `df.loc[mask, ["product", "quantity"]]` | 조건과 열 이름 | 조건에 맞는 두 열 |

**예제 코드 — [04_loc_iloc.py](./examples/04_loc_iloc.py)**

```python
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path).set_index("order_id")
print("loc one:", orders.loc["ORD002", "product"])
print("loc slice:", orders.loc["ORD001":"ORD003", "product"].tolist())
print("iloc slice:", orders.iloc[0:3, 3].tolist())
print("iloc row positions:", orders.iloc[[0, 2]]["order_date"].tolist())
```

**실행 결과**

```text
loc one: 노트
loc slice: ['커피', '노트', '마우스']
iloc slice: ['커피', '노트', '마우스']
iloc row positions: ['2026-10-01', '2026-10-02']
```



**중요:** `loc[0]`에서 `0`은 단순한 첫 번째 행 번호가 아니라 **인덱스 레이블**입니다. `set_index("order_id")`한 다음 `loc[0]`을 쓰면 해당 레이블이 없는 경우 `KeyError`가 발생할 수 있습니다.

`loc` 범위 슬라이싱은 인덱스의 정렬 상태나 중복 레이블에 따라 조건 및 결과가 달라질 수 있으므로, 교육용 예제에서는 정렬된 고유 키를 사용합니다. 일반적인 날짜 필터에는 명시적인 Boolean 조건도 유용합니다.

---

<a id="section-4-6"></a>
## 4.6. Filtering & Sorting — 조건 선택과 정렬

필터링(Filtering)은 특정 조건을 만족하는 행을 선택하고, 정렬(Sorting)은 기준 열의 값에 따라 순서를 변경합니다.

```python
mask = (df["quantity"] >= 2) & (df["status"] == "completed")
selected = df.loc[mask]
```

| 연산 | 예시 | 의미 |
|---|---|---|
| AND | `(a) & (b)` | 두 조건 모두 참 |
| OR | `(a) \| (b)` | 하나 이상 참 |
| NOT | `~(a)` | 조건 반전 |
| 포함 | `.isin(["서울", "부산"])` | 목록 중 하나와 일치 |
| 정렬 | `.sort_values("quantity")` | 지정한 값 오름차순 |
| 다중 정렬 | `.sort_values(["a", "b"])` | 첫 기준 후 다음 기준 |
| 상위 N | `.head(3)` | 앞 3개 행 |

파이썬의 `and` / `or` 대신 Pandas의 Series 조건에는 `&` / `|`를 사용하며, **각 비교식에 괄호**를 붙이는 습관이 좋습니다.

**예제 코드 — [05_filter_conditions.py](./examples/05_filter_conditions.py)**

```python
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
mask = (orders["status"] == "completed") & (orders["region"] == "서울")
seoul = orders.loc[mask, ["order_id", "product", "quantity"]]
print("Seoul completed:", len(seoul))
print(seoul.to_string(index=False))
print("In Seoul or Busan:", int(orders["region"].isin(["서울", "부산"]).sum()))
```

**실행 결과**

```text
Seoul completed: 6
order_id product  quantity
  ORD001      커피         2
  ORD003     마우스         1
  ORD006       펜        10
  ORD009       차         3
  ORD012     키보드         1
  ORD015      노트         4
In Seoul or Busan: 14
```



### 정렬 기준과 상위 데이터

**예제 코드 — [06_sort_topn.py](./examples/06_sort_topn.py)**

```python
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
completed = orders.loc[orders["status"] == "completed"].copy()
completed["amount"] = completed["quantity"] * completed["unit_price"]
top3 = completed.sort_values(["amount", "order_id"], ascending=[False, True]).head(3)
print(top3[["order_id", "amount"]].to_string(index=False))
```

**실행 결과**

```text
order_id  amount
  ORD007   58000
  ORD011   36000
  ORD012   29000
```



상위 순위에서 값이 같은 경우 순서가 명확하도록 보조 정렬 기준을 추가했습니다. `sort_values()`는 별도로 지정하지 않으면 오름차순으로 정렬합니다. **상위 3건**과 **동률을 모두 포함한 상위 3개 순위**는 다른 문제입니다.

---

<a id="section-4-7"></a>
## 4.7. Column Operations — 파생 열과 안전한 수정

기존 열을 바탕으로 새로운 열을 만드는 작업을 **파생 열(Derived Column)** 생성이라고 합니다. 예를 들어 주문 수량과 단가로 주문 금액을 계산할 수 있습니다.

\[
\text{주문금액}=\text{수량}\times\text{단가}
\]

`df["amount"] = ...`로 새 열을 추가하거나, `df.assign()`을 활용해 새 데이터프레임을 만들 수 있습니다. 특정 조건의 행만 수정할 때는 `.loc[조건, 열이름] = 값`을 사용합니다.

**예제 코드 — [07_columns_assign_loc.py](./examples/07_columns_assign_loc.py)**

```python
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
orders = orders.assign(amount=lambda df: df["quantity"] * df["unit_price"])
orders["recognized_sales"] = 0
orders.loc[orders["status"] == "completed", "recognized_sales"] = orders.loc[
    orders["status"] == "completed", "amount"
]
print("All gross order amounts:", int(orders["amount"].sum()))
print("Recognized sales:", int(orders["recognized_sales"].sum()))
print("Canceled sales:", int(orders.loc[orders["status"] == "canceled", "recognized_sales"].sum()))
```

**실행 결과**

```text
All gross order amounts: 281800
Recognized sales: 266300
Canceled sales: 0
```



예제의 `amount`는 **주문 상태와 무관한 단순 주문 금액**, `recognized_sales`는 완료 주문의 금액만 반영한 값입니다. 취소 주문을 처리하는 정책을 명확히 정의하지 않으면 매출이 과대 계산될 수 있습니다.

Pandas의 `df["열"][조건] = 값` 같은 **연결된 인덱싱 방식**은 예상과 다르게 작동할 수 있습니다. 특히 Pandas 3.x에서는 Copy-on-Write로 인해 원본 수정이 의도대로 이루어지지 않습니다. 직접 수정하려는 DataFrame에 `.loc`를 한 번 사용하는 방법을 권장합니다.

---

<a id="section-4-8"></a>
## 4.8. Data Types & Conversion — 문자열·숫자·날짜

외부에서 읽은 데이터는 모두 올바른 자료형이라는 보장이 없습니다. 예를 들어 `"2,500"`은 정수 `2500`이 아니라 문자입니다. 계산하기 전에 의미와 형식을 확인해야 합니다.

| 도구 | 기능 | 예 |
|---|---|---|
| `astype()` | 명시적 자료형 변환 | `.astype("Int64")` |
| `pd.to_numeric()` | 문자열을 수치로 해석 | `errors="coerce"` |
| `pd.to_datetime()` | 문자열을 날짜로 해석 | `format="%Y-%m-%d"` |
| `.str.replace()` | 문자열 일부 교체 | 쉼표 제거 |
| `.isna()` | 결측 여부 확인 | 파싱 실패 탐지 |

**예제 코드 — [08_dtype_conversion.py](./examples/08_dtype_conversion.py)**

```python
import pandas as pd

raw = pd.DataFrame({"price_text": ["2,500", "N/A", "1,200"],
                    "date_text": ["2026-10-01", "invalid", "2026-10-03"]})
clean = raw.copy()
clean["price"] = pd.to_numeric(
    clean["price_text"].str.replace(",", "", regex=False), errors="coerce"
).astype("Int64")
clean["order_date"] = pd.to_datetime(clean["date_text"], format="%Y-%m-%d", errors="coerce")
print("Parsed prices:", clean["price"].astype("string").fillna("NA").tolist())
print("Price dtype:", clean["price"].dtype)
print("Invalid price/date:", int(clean["price"].isna().sum()), int(clean["order_date"].isna().sum()))
print("Original columns:", raw.columns.tolist())
```

**실행 결과**

```text
Parsed prices: ['2500', 'NA', '1200']
Price dtype: Int64
Invalid price/date: 1 1
Original columns: ['price_text', 'date_text']
```



- `errors="coerce"`는 변환할 수 없는 값을 **결측값**으로 표시합니다. 원본 오류가 자동으로 해결되는 것은 아니므로 개수와 원인을 확인해야 합니다.
- Pandas의 문자열 자료형(`string` 또는 3.x의 기본 문자열 처리)과 NumPy 기반 `object` 열은 환경에 따라 다르게 나타날 수 있습니다.
- `Int64`(대문자 I)는 결측값을 지원하는 Pandas 확장 정수 자료형입니다. NumPy의 일반 `int64`와 구분합니다.
- `pd.to_datetime(..., format=...)`로 날짜 입력 형식을 명시하면 예상하지 못한 해석을 줄일 수 있습니다. 실재하는 날짜인지도 함께 검증해야 합니다.

가격이나 정밀한 화폐 연산은 부동소수점 오차를 고려해야 합니다. 본 예제는 **원 단위 정수**를 사용하며, 여러 통화와 소수 단위의 정산 규칙은 별도의 설계가 필요합니다.

---

<a id="section-4-9"></a>
## 4.9. Basic GroupBy — 그룹별 요약

`groupby()`는 같은 범주에 속한 행을 묶어 집계합니다. 흔히 **Split → Apply → Combine** 과정으로 설명합니다.

```text
지역별 주문
    ↓ 그룹 분리
서울 / 부산 / 인천
    ↓ 그룹별 집계
주문 건수 · 매출 합계
    ↓ 결과 결합
지역별 요약표
```

| 표현 | 의미 |
|---|---|
| `df.groupby("region")["amount"].sum()` | 지역별 매출 합계 |
| `.agg(orders=("order_id", "size"))` | 주문 건수 집계 |
| `.agg(avg_price=("unit_price", "mean"))` | 지역별 평균 단가 |
| `as_index=False` | 집계 기준을 결과의 일반 열로 보관 |

**예제 코드 — [09_groupby_basic.py](./examples/09_groupby_basic.py)**

```python
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
completed = orders.loc[orders["status"] == "completed"].copy()
completed["amount"] = completed["quantity"] * completed["unit_price"]
summary = completed.groupby("region", as_index=False).agg(
    order_count=("order_id", "size"), sales=("amount", "sum")
).sort_values("region")
print(summary.to_string(index=False))
```

**실행 결과**

```text
region  order_count  sales
    부산            6  85400
    서울            6  80600
    인천            5 100300
```



- `sum()`은 합계, `mean()`은 산술평균, `size`는 행 개수입니다.
- `count()`는 해당 열의 **비결측 값 개수**를 세는 데 사용합니다. 결측값이 있는 데이터에서는 `size()`와 다른 결과가 나올 수 있습니다.
- 먼저 완료 주문만 선택한 뒤 그룹화했기 때문에 취소 주문 매출이 포함되지 않습니다.

여러 데이터프레임을 병합하는 `merge()`, 여러 집계축을 다루는 `pivot_table()`, 이동 창 계산 등은 Chapter 07에서 더 자세히 학습합니다.

---

<a id="section-4-10"></a>
## 4.10. String & Date Operations — 간단한 텍스트·날짜 처리

Pandas는 문자열 열에 `.str`, 날짜/시간 열에 `.dt` 접근자를 제공합니다.

| 표현 | 의미 |
|---|---|
| `s.str.strip()` | 앞뒤 공백 제거 |
| `s.str.contains("커", regex=False)` | 문자열 포함 여부 |
| `s.str.lower()` | 소문자로 변환 |
| `date_series.dt.year` | 연도 추출 |
| `date_series.dt.month` | 월 추출 |
| `date_series.dt.day` | 일 추출 |

**예제 코드 — [10_string_datetime.py](./examples/10_string_datetime.py)**

```python
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
orders["order_date"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d")
print("October orders:", int(orders["order_date"].dt.month.eq(10).sum()))
print("Products containing '커':", orders.loc[orders["product"].str.contains("커", regex=False), "product"].unique().tolist())
print("Earliest date:", orders["order_date"].min().date())
```

**실행 결과**

```text
October orders: 20
Products containing '커': ['커피']
Earliest date: 2026-10-01
```



`.str.contains()`는 기본적으로 정규표현식(Regular Expression) 패턴을 처리합니다. 단순 부분 문자열을 찾으려면 `regex=False`를 명시할 수 있습니다. 결측 문자열이 있는 경우 반환 마스크에서 결측 처리 규칙도 고려해야 합니다.

날짜 파싱, 시간대, 데이터 형식의 정확한 판별은 Chapter 05~06에서 확장합니다.

---

<a id="section-4-11"></a>
## 4.11. Copy-on-Write & Chained Assignment — 복사와 수정 규칙

Pandas에서 데이터를 선택한 결과가 원본과 같은 데이터를 공유하는지 여부는 사용 중인 버전과 연산에 따라 다르게 느껴질 수 있습니다. **Pandas 3.0부터 Copy-on-Write가 기본이자 유일한 동작 방식**입니다. 사용자가 하나의 객체를 수정할 때, 다른 객체의 값이 의도치 않게 바뀌지 않도록 합니다.

**피해야 할 방식**

```python
# 연결된 인덱싱: 원본 변경을 의도해도 보장되지 않습니다.
df["stock"][df["stock"] < 3] = 0
```

**권장 방식**

```python
# 수정 대상 df를 직접 지정합니다.
df.loc[df["stock"] < 3, "stock"] = 0
```

**예제 코드 — [11_copy_on_write.py](./examples/11_copy_on_write.py)**

```python
import pandas as pd

data = pd.DataFrame({"product": ["커피", "노트", "펜"], "stock": [8, 2, 0]})
subset = data.loc[data["stock"] <= 2, ["product", "stock"]].copy()
subset.loc[subset["product"] == "노트", "stock"] = 5
print("Original notebook stock:", int(data.loc[data["product"] == "노트", "stock"].iloc[0]))
print("Subset notebook stock:", int(subset.loc[subset["product"] == "노트", "stock"].iloc[0]))
data.loc[data["product"] == "펜", "stock"] = 4
print("Updated original pen stock:", int(data.loc[data["product"] == "펜", "stock"].iloc[0]))
```

**실행 결과**

```text
Original notebook stock: 2
Subset notebook stock: 5
Updated original pen stock: 4
```



`copy()`는 독립된 결과가 필요하다는 의도를 명확히 표현합니다. 하지만 Pandas 3.x에서 부분 선택이 이미 객체 수준의 독립 수정 의미를 갖는다는 이유만으로 **모든 선택 결과에 무조건 `copy()`를 호출할 필요는 없습니다.** 학습 예제에서는 원본과 처리본을 명확히 구분하려고 일부 복사를 사용합니다.

Pandas 2.x에서도 연결된 인덱싱으로 인해 `SettingWithCopyWarning`이 나타날 수 있습니다. 두 버전에서 모두 안전하게 읽히는 코드는 직접 수정과 명시적인 반환 결과를 구분하는 방식입니다.

---

<a id="section-4-12"></a>
## 4.12. Iteration & Vectorized Operations — 행 순회와 벡터화

Pandas의 행을 하나씩 읽을 때는 `itertuples()`를 사용할 수 있습니다. 그러나 **모든 행에 같은 계산 규칙을 적용한다면 벡터화된 열 연산을 우선 고려**하는 편이 일반적으로 간결하고 성능상 유리할 수 있습니다.

**예제 코드 — [12_iteration_vs_vectorized.py](./examples/12_iteration_vs_vectorized.py)**

```python
from pathlib import Path
import pandas as pd

path = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(path)
values = [row.quantity * row.unit_price for row in orders.itertuples(index=False)]
vectorized = (orders["quantity"] * orders["unit_price"]).tolist()
print("Same results:", values == vectorized)
print("Row count:", len(values))
print("First 3 amounts:", vectorized[:3])
```

**실행 결과**

```text
Same results: True
Row count: 20
First 3 amounts: [7000, 7500, 18000]
```



`iterrows()`는 각 행을 Series로 만들어 반환하므로 **행별 원본 자료형이 그대로 유지되지 않을 수 있습니다.** 행 단위 처리가 불가피하면 `itertuples()`를 우선 고려할 수 있습니다. 단, 파이썬 반복문이 항상 나쁘다는 뜻은 아닙니다. 복잡한 외부 API 호출이나 사용자 정의 처리 과정에는 적절할 수 있습니다.

자료의 크기와 함수 종류에 따라 성능이 달라지므로, 최적화가 필요할 때는 실행 시간을 실제로 비교해야 합니다. Chapter 07에서 처리량과 메모리를 함께 다룹니다.

---

<a id="section-4-13"></a>
## 4.13. CSV Export — 처리 결과 저장

DataFrame의 처리 결과를 저장하려면 `to_csv()`를 사용할 수 있습니다. 반대로 CSV를 읽을 때는 `pd.read_csv()`를 사용합니다.

```python
df.to_csv("result.csv", index=False, encoding="utf-8")
```

- `index=False`: DataFrame의 행 인덱스를 별도 CSV 열로 기록하지 않습니다.
- `encoding="utf-8"`: UTF-8 인코딩으로 저장합니다.
- `to_csv()`는 출력 경로가 이미 존재하면 덮어쓸 수 있으므로 보존할 파일과 결과물을 구분합니다.
- Excel 등 일부 프로그램의 설정에서는 UTF-8 BOM(`utf-8-sig`)이 필요한 경우도 있습니다. 용도에 따라 선택합니다.

**예제 코드 — [13_csv_export.py](./examples/13_csv_export.py)**

```python
from pathlib import Path
import pandas as pd

chapter = Path(__file__).resolve().parents[1]
orders = pd.read_csv(chapter / "data" / "orders.csv")
completed = orders.loc[orders["status"] == "completed", ["order_id", "region", "quantity", "unit_price"]].copy()
completed["amount"] = completed["quantity"] * completed["unit_price"]
output_path = chapter / "output" / "completed_orders.csv"
output_path.parent.mkdir(exist_ok=True)
completed.to_csv(output_path, index=False, encoding="utf-8")
reloaded = pd.read_csv(output_path)
print("Saved:", output_path.name)
print("Saved rows:", len(reloaded))
print("Total amount:", int(reloaded["amount"].sum()))
```

**실행 결과**

```text
Saved: completed_orders.csv
Saved rows: 17
Total amount: 266300
```



CSV 파일의 자료형 정보는 저장 후 다시 읽는 과정에서 자동 추론될 수 있습니다. 따라서 `read_csv()`로 다시 읽은 결과의 자료형이 원래 DataFrame과 언제나 같다고 가정하면 안 됩니다.

전체적인 파일 형식의 장단점과 JSON·Excel·Parquet·SQLite 연동은 Chapter 05에서 소개합니다.

---

<a id="section-4-14"></a>
## 4.14. Mini Project — Order Sales Report

### 목표

`orders.csv`의 주문 20건을 읽고, 기본적인 컬럼·값 검사를 수행한 뒤 **완료된 주문만 매출로 인정**하여 지역별·상품 분류별·일별 통계를 생성합니다. Pandas의 DataFrame, 조건 선택, 파생 열, `groupby()` 및 CSV 저장을 하나의 흐름으로 묶는 프로젝트입니다.

### 입력 데이터

- [orders.csv](./data/orders.csv) — 교육용 가상 주문 20건
- [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md) — 열 이름·단위·값 규칙
- `status`: `completed` 또는 `canceled`
- 매출액: **완료 주문의 `quantity × unit_price` 합계**

### 처리 과정

```text
orders.csv (20건)
    ↓ 데이터 읽기 및 기본 검증
DataFrame — 날짜·수량·단가 해석
    ↓ status == completed 조건 선택
완료 주문 17건
    ↓ 주문 금액 열 계산
amount = quantity × unit_price
    ↓ 그룹 집계
지역 / 분류 / 날짜
    ↓ CSV 저장
output/sales_by_region.csv
output/sales_by_category.csv
output/sales_by_day.csv
```

### 코드 구성

프로젝트는 `examples/14_sales_report.py` 하나의 파일에서 함수를 나누어 작성했습니다.

| 함수 | 역할 |
|---|---|
| `load_orders()` | 파일 읽기, 필수 열·중복 주문·기본 값 검사 |
| `make_reports()` | 완료 주문 필터링 및 3개 요약표 계산 |
| `export_reports()` | 결과를 지정 디렉터리 아래 CSV로 저장 |
| `main()` | 전체 처리 흐름 제어 및 요약 출력 |

**예제 코드 — [14_sales_report.py](./examples/14_sales_report.py)**

```python
"""Mini Project: 주문 데이터 읽기 → 기본 검증 → 집계 → CSV 저장."""
from pathlib import Path
import pandas as pd

CHAPTER = Path(__file__).resolve().parents[1]
REQUIRED = {"order_id", "order_date", "region", "category", "product", "quantity", "unit_price", "status"}


def load_orders(path: Path) -> pd.DataFrame:
    orders = pd.read_csv(path)
    missing_columns = REQUIRED.difference(orders.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing_columns))}")
    if orders.empty or orders["order_id"].isna().any() or orders["order_id"].duplicated().any():
        raise ValueError("Order IDs must be present and unique")
    if orders[list(REQUIRED)].isna().any().any():
        raise ValueError("Required fields contain missing values")
    if not orders["status"].isin(["completed", "canceled"]).all():
        raise ValueError("Unexpected order status")
    for column in ("quantity", "unit_price"):
        values = pd.to_numeric(orders[column], errors="coerce")
        if values.isna().any() or (values < (1 if column == "quantity" else 0)).any() or (values % 1 != 0).any():
            raise ValueError(f"Invalid numeric column: {column}")
        orders[column] = values.astype("int64")
    parsed_dates = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="coerce")
    if parsed_dates.isna().any():
        raise ValueError("Invalid order date")
    orders["order_date"] = parsed_dates
    return orders


def make_reports(orders: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    completed = orders.loc[orders["status"] == "completed"].copy()
    completed["amount"] = completed["quantity"] * completed["unit_price"]
    by_region = completed.groupby("region", as_index=False).agg(
        orders=("order_id", "size"), revenue=("amount", "sum")
    ).sort_values("region").reset_index(drop=True)
    by_category = completed.groupby("category", as_index=False).agg(
        orders=("order_id", "size"), revenue=("amount", "sum")
    ).sort_values("category").reset_index(drop=True)
    by_day = completed.groupby("order_date", as_index=False).agg(
        orders=("order_id", "size"), revenue=("amount", "sum")
    ).sort_values("order_date").reset_index(drop=True)
    return by_region, by_category, by_day


def export_reports(reports: tuple[pd.DataFrame, ...], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, frame in zip(("sales_by_region.csv", "sales_by_category.csv", "sales_by_day.csv"), reports):
        frame.to_csv(output_dir / filename, index=False, encoding="utf-8")


def main() -> None:
    orders = load_orders(CHAPTER / "data" / "orders.csv")
    reports = make_reports(orders)
    export_reports(reports, CHAPTER / "output")
    valid_count = int(orders["status"].eq("completed").sum())
    total_sales = int(reports[0]["revenue"].sum())
    print(f"Orders: {len(orders)} (completed {valid_count}, canceled {len(orders) - valid_count})")
    print(f"Revenue: {total_sales:,} KRW")
    print("Sales by region:")
    print(reports[0].to_string(index=False))
    print("Saved: sales_by_region.csv, sales_by_category.csv, sales_by_day.csv")


if __name__ == "__main__":
    main()
```

**실행 결과**

```text
Orders: 20 (completed 17, canceled 3)
Revenue: 266,300 KRW
Sales by region:
region  orders  revenue
    부산       6    85400
    서울       6    80600
    인천       5   100300
Saved: sales_by_region.csv, sales_by_category.csv, sales_by_day.csv
```



### 실행

```bash
python examples/14_sales_report.py
```

### 결과 확인

| 출력 파일 | 내용 |
|---|---|
| `sales_by_region.csv` | 지역별 완료 주문 수와 총매출 |
| `sales_by_category.csv` | 상품 분류별 완료 주문 수와 총매출 |
| `sales_by_day.csv` | 날짜별 완료 주문 수와 총매출 |

이 예제의 오류 검사는 **교육용 데이터의 필수 열, ID 중복, 상태, 수량·단가, 날짜 형식**에 한정합니다. 임의의 외부 데이터가 가진 모든 품질 문제를 해결하는 정제 도구는 아닙니다. 불완전한 데이터의 오류 유형별 처리 기준은 Chapter 06에서 확장합니다.

**원본 파일을 수정하지 않으며**, 결과 파일은 `.gitignore`에 등록된 `output/`에 생성됩니다. 동일한 이름의 결과를 다시 생성하면 파일 내용이 갱신됩니다.

---

<a id="section-4-15"></a>
## 4.15. Coding Practice

각 문제에는 `exercises/`의 시작 코드와 `solutions/`의 모범답안이 들어 있습니다. 먼저 직접 구현한 뒤 정답 코드를 확인하세요. 예제는 모두 교육용 주문 데이터 또는 작은 DataFrame을 대상으로 합니다.

| 번호 | 문제 | 시작 코드 | 정답 코드 |
|:---:|---|---|---|
| 01 | DataFrame 생성 | [01_build_dataframe.py](./exercises/01_build_dataframe.py) | [정답](./solutions/01_build_dataframe.py) |
| 02 | 조건별 완료 주문 추출 | [02_filter_orders.py](./exercises/02_filter_orders.py) | [정답](./solutions/02_filter_orders.py) |
| 03 | 상위 매출 주문 계산 | [03_top_revenue.py](./exercises/03_top_revenue.py) | [정답](./solutions/03_top_revenue.py) |
| 04 | 숫자·날짜 열 변환 | [04_parse_columns.py](./exercises/04_parse_columns.py) | [정답](./solutions/04_parse_columns.py) |
| 05 | 분류별 완료 주문 집계 | [05_category_summary.py](./exercises/05_category_summary.py) | [정답](./solutions/05_category_summary.py) |

### Exercise 01 — DataFrame Creation

`build_dataframe()`를 완성하여 다음 세 상품을 `product`, `quantity`, `unit_price` 순서로 가지는 DataFrame을 반환하세요.

| product | quantity | unit_price |
|---|---:|---:|
| 커피 | 2 | 3500 |
| 노트 | 3 | 2500 |
| 펜 | 5 | 1000 |

**조건:** 딕셔너리와 `pd.DataFrame()` 사용. 세 컬럼을 모두 포함하고 행 순서 유지.

### Exercise 02 — Filtering Completed Orders

`filter_orders(orders, region, minimum_quantity)`를 완성하세요.

- 주문 상태가 `completed`인 데이터만 선택합니다.
- 지역이 지정한 문자열과 일치해야 합니다.
- 수량이 `minimum_quantity` 이상이어야 합니다.
- 반환 열은 `order_id`, `product`, `quantity`이며 인덱스는 0부터 시작해야 합니다.
- 원본 DataFrame은 변경하지 않습니다.

### Exercise 03 — Top Revenue Orders

`top_revenue_orders(orders, n=3)`를 완성하세요.

- 완료 주문의 `amount = quantity × unit_price`를 계산합니다.
- 금액 내림차순, 동일 금액일 때 `order_id` 오름차순으로 정렬합니다.
- 상위 `n`건의 `order_id`, `amount` 열만 반환합니다.
- `n < 0`인 경우 `ValueError`를 발생시킵니다.

### Exercise 04 — Safe Type Conversion

`parse_columns(raw)`를 완성하세요.

- `price_text`: 쉼표가 있는 수치 문자열에서 `price` 열 생성, nullable 정수 `Int64` 사용
- `date_text`: `YYYY-MM-DD` 형식의 문자열을 날짜 자료형 `date` 열로 변환
- 잘못된 숫자와 날짜는 결측값 처리하고, 원본은 변경하지 않습니다.

### Exercise 05 — Category Sales Summary

`category_summary(orders)`를 완성하세요.

- 완료 주문만 포함하고, `category`별로 주문 건수(`orders`)와 총매출(`revenue`)을 계산합니다.
- 매출 내림차순, 동률이면 분류 이름 오름차순으로 정렬합니다.
- 결과 컬럼은 `category`, `orders`, `revenue`이며 인덱스를 초기화합니다.

### 연습문제 점검

`exercises/`의 시작 코드는 직접 구현하도록 의도적으로 `NotImplementedError`가 포함되어 있습니다. 제공한 자동 테스트는 **정답 코드(`solutions/`)와 Mini Project**를 대상으로 합니다.

```bash
python solutions/01_build_dataframe.py
python -m unittest discover -s tests -v
```

연습문제를 완성한 뒤 모범답안과 비교하고, 정상 입력뿐 아니라 빈 DataFrame이나 잘못된 값 등 경계 조건도 점검하세요.

---

<a id="section-4-16"></a>
## 4.16. Quiz & Summary

### Quiz

각 문제의 정답은 해당 문항 아래에서 개별적으로 확인할 수 있습니다.

**Q1.** `pd.Series([4, 8, 12])`와 `pd.DataFrame({"x": [4, 8, 12]})`의 주요 차이는 무엇인가요?

<details>
<summary>Q1. 정답 및 해설 확인</summary>

`Series`는 인덱스를 가진 1차원 자료구조이고, `DataFrame`은 열 이름을 가진 2차원 표입니다. 한 열을 가진 DataFrame도 2차원입니다.

</details>

**Q2.** DataFrame의 행이 20개, 열이 8개라면 `df.shape`의 값은 무엇인가요?

<details>
<summary>Q2. 정답 및 해설 확인</summary>

`(20, 8)`입니다. `shape`는 (행 수, 열 수) 순서의 튜플입니다.

</details>

**Q3.** 인덱스를 `order_id`로 설정했을 때 `df.loc["ORD003"]`과 `df.iloc[2]`는 어떤 기준으로 행을 찾나요?

<details>
<summary>Q3. 정답 및 해설 확인</summary>

`loc`는 인덱스 레이블 `ORD003`을, `iloc`는 정수 위치 2(세 번째 행)를 기준으로 행을 선택합니다.

</details>

**Q4.** 레이블 인덱스가 `A`, `B`, `C`, `D`라면 `loc["A":"C"]`의 마지막 `C`는 포함되나요? `iloc[0:3]`의 위치 3은 포함되나요?

<details>
<summary>Q4. 정답 및 해설 확인</summary>

레이블 슬라이싱 `loc["A":"C"]`는 끝 레이블 `C`를 포함하지만, `iloc[0:3]`은 위치 3을 포함하지 않아 위치 0, 1, 2만 선택합니다.

</details>

**Q5.** `(df["quantity"] >= 2) and (df["status"] == "completed")`는 왜 올바른 Pandas 조건식이 아닌가요?

<details>
<summary>Q5. 정답 및 해설 확인</summary>

두 비교식은 각각 Boolean Series를 반환합니다. 요소별 AND를 계산해야 하므로 `and`가 아니라 괄호와 `&`를 사용합니다.

</details>

**Q6.** `df["quantity"] * df["unit_price"]` 결과로 어떤 데이터가 만들어지나요?

<details>
<summary>Q6. 정답 및 해설 확인</summary>

각 행의 수량과 단가를 원소별로 곱한 Series가 만들어집니다. 매출로 집계하려면 취소 주문 제외 등 상태 조건을 추가해야 합니다.

</details>

**Q7.** `pd.to_numeric(["10", "invalid"], errors="coerce")`에서 두 번째 값은 어떻게 처리되나요?

<details>
<summary>Q7. 정답 및 해설 확인</summary>

파싱할 수 없는 `"invalid"`는 결측값(NaN)으로 표시됩니다. 잘못된 값을 정답으로 고친 것은 아니므로 별도의 검증이 필요합니다.

</details>

**Q8.** `groupby()`의 `size()`와 `count()`는 결측값이 있을 때 어떤 차이를 보이나요?

<details>
<summary>Q8. 정답 및 해설 확인</summary>

`size()`는 그룹의 행 수를 세고, `count()`는 해당 열의 비결측 값 수를 세므로 결측값이 있는 경우 다를 수 있습니다.

</details>

**Q9.** Pandas 3.x에서 `df["stock"][mask] = 0` 대신 권장하는 수정 방식은 무엇인가요?

<details>
<summary>Q9. 정답 및 해설 확인</summary>

`df.loc[mask, "stock"] = 0`으로 수정 대상을 한 번에 지정합니다. Chained Assignment는 Copy-on-Write 동작에서 원본 갱신에 사용할 수 없습니다.

</details>

**Q10.** CSV로 저장한 뒤 다시 읽은 DataFrame의 자료형이 원래와 항상 같을까요?

<details>
<summary>Q10. 정답 및 해설 확인</summary>

항상 같지 않습니다. CSV는 자료형 정보를 충분히 보존하지 않으며, `read_csv()`가 다시 타입을 추론할 수 있으므로 필요하면 `dtype` 또는 변환 규칙을 명시해야 합니다.

</details>

### Summary

- **Pandas:** 표 형태의 데이터를 다루는 Python 라이브러리
- **Series / DataFrame:** 인덱스가 있는 1차원 데이터 / 열 이름이 있는 2차원 표
- **Index / Columns:** 행·열 레이블 및 정렬 기준
- **Inspection:** `shape`, `head()`, `info()`, `describe()`, `dtypes`, `isna()`
- **Selection:** 레이블 기반 `loc`, 위치 기반 `iloc`
- **Filtering:** Boolean Series를 이용한 행 선택과 `&`, `|`, `~` 연산
- **Sorting:** `sort_values()`로 다중 조건 정렬
- **Column Operation:** 기존 열의 연산으로 파생 열 생성, 조건부 변경은 `.loc`
- **Data Conversion:** `to_numeric()`, `to_datetime()`, nullable `Int64` 사용
- **GroupBy:** 범주별 주문 수·합계·평균 집계
- **Copy-on-Write:** 원본 객체에 직접 쓰고 연결된 인덱싱 수정은 피함
- **Export:** `to_csv(index=False)`로 결과 저장, 재로딩 시 자료형 확인

### References

- [Pandas — Getting Started](https://pandas.pydata.org/docs/getting_started/)
- [Pandas — Intro to Data Structures](https://pandas.pydata.org/docs/user_guide/dsintro.html)
- [Pandas — Indexing and Selecting Data](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Pandas — Essential Basic Functionality](https://pandas.pydata.org/docs/user_guide/basics.html)
- [Pandas — GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Pandas — Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html)
- [Pandas — Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [Pandas — IO Tools](https://pandas.pydata.org/docs/user_guide/io.html)

---

[← Data Processing 목차](../README.md) · [Chapter 03 — NumPy Fundamentals](../Chapter-03/)

