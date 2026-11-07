# Chapter 07. Data Transformation & Aggregation

여러 데이터셋을 결합하고 필요한 형태로 변환하여 **데이터의 의미를 유지하면서 집계 가능한 결과를 만드는 방법**을 학습합니다. `GroupBy`, `Merge`, `Join`, `Pivot`, 시계열 집계, 이동평균과 재사용 가능한 처리 파이프라인을 다룹니다.

본 자료는 **Python 3.13.5 / Pandas 2.2.3 / NumPy 2.3.5** 환경에서 실행 검증했습니다. Pandas 3.x의 Copy-on-Write 및 문자열 자료형 변경 사항도 고려하여 연결 대입을 사용하지 않고 명시적인 결합·집계 규칙을 적용했습니다. 출력 표시 형식은 라이브러리 버전에 따라 조금 다를 수 있습니다. 모든 데이터는 교육용 가상 데이터입니다.

<details>
<summary><strong>선행 학습 목록</strong></summary>

- [Chapter 02 — Python Data Structures](../Chapter-02/)
- [Chapter 03 — NumPy Fundamentals](../Chapter-03/)
- [Chapter 04 — Pandas & DataFrames](../Chapter-04/)
- [Chapter 05 — File I/O & Data Formats](../Chapter-05/)
- [Chapter 06 — Data Cleaning & Validation](../Chapter-06/)

</details>

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [7.1](#section-7-1) | Data Transformation — 변환의 목적 |
| [7.2](#section-7-2) | Mapping & Conditional Operations — 값 매핑과 조건 처리 |
| [7.3](#section-7-3) | GroupBy & Aggregation — 그룹별 집계 |
| [7.4](#section-7-4) | GroupBy Transform — 원래 행을 유지한 계산 |
| [7.5](#section-7-5) | Merge & Join — 테이블 결합과 관계 검증 |
| [7.6](#section-7-6) | Concatenation & Index Alignment — 행 연결과 정렬 |
| [7.7](#section-7-7) | Reshaping — Pivot & Melt |
| [7.8](#section-7-8) | Pivot Table & Crosstab — 교차 집계 |
| [7.9](#section-7-9) | Time-Based Aggregation — 날짜 및 기간별 집계 |
| [7.10](#section-7-10) | Rolling & Cumulative Operations — 이동·누적 계산 |
| [7.11](#section-7-11) | Missing Dates & Zero-Fill Policy — 빈 날짜의 의미 |
| [7.12](#section-7-12) | Vectorization & Memory — 효율적인 처리 |
| [7.13](#section-7-13) | Reusable Processing Pipelines — 처리 단계의 함수화 |
| [7.14](#section-7-14) | Mini Project — Store Sales Transformation Pipeline |
| [7.15](#section-7-15) | Coding Practice |
| [7.16](#section-7-16) | Quiz & Summary |

## Getting Started

**권장 환경:** Python 3.13 이상, Pandas 2.2 이상. 이 장의 예제는 인터넷 연결 없이 실행할 수 있습니다.

```bash
python -m pip install -r requirements.txt
```

**실행 기준 경로:** `Data_Processing/Chapter-07/`

```bash
python examples/01_transformation_basics.py
python examples/14_store_sales_pipeline.py
python -m unittest discover -s tests -v
```

**디렉터리 구성**

```text
Chapter-07/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── DATA_DICTIONARY.md
│   ├── order_lines.csv
│   ├── products.csv
│   └── stores.csv
├── examples/             # 학습 예제 14개, 마지막은 Mini Project
├── exercises/            # 학습자가 구현하는 연습문제 5개
├── solutions/            # 연습문제 정답 코드 5개
├── tests/                # 자동 테스트
└── output/               # 실행 시 생성, Git 추적 제외
```

**실습 데이터:** [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)에서 열의 정의와 매출 계산 정책을 확인할 수 있습니다. `data/`의 원본을 수정하지 않고 `output/`에 결과를 생성합니다. 실행 경로가 바뀌어도 예제는 소스 파일 기준으로 데이터 경로를 찾습니다.

---

<a id="section-7-1"></a>
## 7.1. Data Transformation — 변환의 목적

데이터 변환(Data Transformation)은 데이터를 저장하거나 분석하기에 적합하도록 **열의 이름·값·형태를 바꾸는 작업**입니다. 새로운 열을 만드는 것뿐만 아니라 동일한 의미의 데이터가 일관된 형식으로 표현되도록 하는 과정도 포함합니다.

| 작업 | 대표 메서드 | 예시 |
|---|---|---|
| 새로운 열 계산 | `assign()`, `df["new"] = ...` | 수량 × 가격 |
| 열 이름 변경 | `rename()` | `sales` → `gross_sales_won` |
| 값 변환 | `map()`, `replace()` | 코드 → 표시 이름 |
| 행 조건 처리 | `.loc[]`, `where()` | 특정 기준 이상에 레이블 부여 |
| 형태 변경 | `pivot()`, `melt()` | 세로형 ↔ 가로형 |

**데이터의 단위(Grain)**를 먼저 확인하는 습관이 중요합니다. 예를 들어 '주문 한 건'과 '주문 상품 한 줄'은 서로 다른 단위입니다. 두 단위를 혼동하면 매출 합계가 맞더라도 주문 건수는 틀리게 됩니다.

`assign()`은 새 DataFrame을 반환하며, 기존 DataFrame에 직접 대입하는 방식과 용도가 다릅니다. 원본을 변경하지 않으려면 반환값을 다른 변수에 보관하세요.

**예제 코드 — [01_transformation_basics.py](./examples/01_transformation_basics.py)**

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": ["A1", "A2", "A3"],
    "quantity": [2, 3, 1],
    "unit_price_won": [10000, 5000, 12000],
})
orders = orders.assign(sales_won=orders["quantity"] * orders["unit_price_won"])
orders = orders.rename(columns={"sales_won": "gross_sales_won"})
print(orders[["order_id", "gross_sales_won"]].to_string(index=False))
```

**실행 결과**

```text
order_id  gross_sales_won
      A1            20000
      A2            15000
      A3            12000
```

---

<a id="section-7-2"></a>
## 7.2. Mapping & Conditional Operations — 값 매핑과 조건 처리

상품 코드나 매장 코드를 읽기 쉬운 이름으로 표시할 때는 `Series.map()`을 사용할 수 있습니다. 작은 사전(Dictionary)으로 처리하기 편리하지만, 다른 파일에 저장된 대규모 기준정보는 이후의 `merge()`가 더 적합할 수 있습니다.

`map()`에 등록되지 않은 코드는 기본적으로 결측값이 됩니다. **매핑 실패를 곧바로 정상적인 기본값으로 대체하면 미등록 코드를 놓칠 수 있습니다.** 먼저 미등록 건수를 확인한 뒤 보완하거나 오류로 처리하세요.

조건에 따라 열을 변경할 때는 `df.loc[조건, "열"] = 값` 형태를 사용합니다. `df["열"][조건] = 값` 같은 연결 대입(Chained Assignment)은 지양합니다. Pandas 3.0부터는 Copy-on-Write가 기본 동작이므로 이런 패턴은 의도한 원본 DataFrame을 수정하지 못합니다.

| 방법 | 결과 | 주의 |
|---|---|---|
| `map(mapping)` | 코드에 대응하는 값 생성 | 등록되지 않은 키는 결측 가능 |
| `replace(mapping)` | 일치하는 값만 변경 | 미매핑 값이 그대로 남을 수 있음 |
| `loc[mask, col] = x` | 특정 조건을 만족하는 행 수정 | 원본 의도를 명확하게 표현 |

**예제 코드 — [02_mapping_and_conditionals.py](./examples/02_mapping_and_conditionals.py)**

```python
import pandas as pd

orders = pd.DataFrame({"store_id": ["S01", "S02", "S99"], "quantity": [2, 5, 1]})
store_names = {"S01": "서울점", "S02": "부산점"}
orders["store_name"] = orders["store_id"].map(store_names)
orders["size_class"] = "일반"
orders.loc[orders["quantity"] >= 4, "size_class"] = "대량"
print(orders.to_string(index=False))
print("Unknown store:", int(orders["store_name"].isna().sum()))
```

**실행 결과**

```text
store_id  quantity store_name size_class
     S01         2        서울점         일반
     S02         5        부산점         대량
     S99         1        NaN         일반
Unknown store: 1
```

---

<a id="section-7-3"></a>
## 7.3. GroupBy & Aggregation — 그룹별 집계

집계(Aggregation)는 여러 행을 하나의 통계값으로 요약하는 작업입니다. `groupby()`는 지정한 키가 같은 행을 모은 뒤 합계, 평균, 개수 등을 계산합니다.

**그룹 집계의 핵심 단계:** `그룹 열 선택 → 그룹별 계산 → 결과 이름 지정 → 검증`.

| 집계 | 함수 | 의미 |
|---|---|---|
| 행 수 | `size()` | 결측 여부와 관계없이 그룹의 행 개수 |
| 비결측 수 | `count()` | 해당 열에 값이 존재하는 행 개수 |
| 고유 값 수 | `nunique()` | 중복을 제외한 고유 값의 개수 |
| 합계 | `sum()` | 그룹별 숫자 합계 |
| 평균 | `mean()` | 그룹별 산술평균 |
| 여러 통계 | `agg()` | 하나 이상의 집계 결과 생성 |

여기서 `lines`는 주문 상품 **행 수**, `orders`는 고유 **주문 ID 개수**입니다. 예제의 서울은 행 2개가 같은 주문 번호이므로 `lines=2`, `orders=1`입니다. 두 값이 같은 의미라고 생각하면 잘못된 보고서가 만들어질 수 있습니다.

`groupby()`는 결측된 그룹 키를 기본적으로 제외할 수 있으므로, 누락 키를 포함할지(`dropna=False`) 먼저 정해야 합니다. 범주형 열에서는 `observed`의 기본값도 버전에 따라 달라질 수 있어, 필요하면 명시합니다.

**예제 코드 — [03_groupby_named_aggregation.py](./examples/03_groupby_named_aggregation.py)**

```python
import pandas as pd

orders = pd.DataFrame({
    "region": ["서울", "서울", "부산", "부산"],
    "order_id": ["O1", "O1", "O2", "O3"],
    "units": [2, 1, 3, 2],
    "sales_won": [20000, 10000, 15000, 14000],
})
summary = orders.groupby("region", as_index=False).agg(
    lines=("order_id", "size"),
    orders=("order_id", "nunique"),
    units=("units", "sum"),
    sales_won=("sales_won", "sum"),
).sort_values("region")
print(summary.to_string(index=False))
```

**실행 결과**

```text
region  lines  orders  units  sales_won
    부산      2       2      5      29000
    서울      2       1      3      30000
```

---

<a id="section-7-4"></a>
## 7.4. GroupBy Transform — 원래 행을 유지한 계산

`agg()`와 `transform()`은 결과의 모양이 다릅니다. 집계는 한 그룹을 하나의 결과 행으로 줄이는 반면, `transform()`은 **원래 행 개수를 유지하면서 각 행에 해당 그룹의 결과를 붙입니다.**

| 메서드 | 출력 행 수 | 적합한 용도 |
|---|---|---|
| `groupby(...).agg(...)` | 그룹 개수 | 지역별 매출 요약표 |
| `groupby(...).transform(...)` | 일반적으로 원래 행 개수 유지 | 각 주문의 지역 매출 대비 비중 |

예제의 서울 지역 매출 합계는 `10,000 + 30,000 = 40,000원`이므로 첫 번째 주문의 비중은 `10,000 / 40,000 × 100 = 25%`입니다.

\[\text{매출 비중(\%)} = \frac{\text{해당 행 매출}}{\text{동일 그룹의 매출 총합}}\times 100\]

실제 데이터에 총합이 0원인 그룹이 있다면 0으로 나누지 않도록 별도 규칙이 필요합니다.

**예제 코드 — [04_groupby_transform.py](./examples/04_groupby_transform.py)**

```python
import pandas as pd

sales = pd.DataFrame({
    "region": ["서울", "서울", "부산", "부산"],
    "sales_won": [10000, 30000, 20000, 10000],
})
sales["region_total"] = sales.groupby("region")["sales_won"].transform("sum")
sales["share_pct"] = (100 * sales["sales_won"] / sales["region_total"]).round(1)
print(sales.to_string(index=False))
```

**실행 결과**

```text
region  sales_won  region_total  share_pct
    서울      10000         40000       25.0
    서울      30000         40000       75.0
    부산      20000         30000       66.7
    부산      10000         30000       33.3
```

---

<a id="section-7-5"></a>
## 7.5. Merge & Join — 테이블 결합과 관계 검증

`merge()`는 두 DataFrame에서 공통 키를 기준으로 행을 연결합니다. 상품 주문 행에 상품 분류를 연결하거나, 센서 측정값에 장치 정보를 추가할 때 사용합니다.

| 결합 방식 | 의미 |
|---|---|
| `inner` | 양쪽에 일치하는 키가 있는 행만 반환 |
| `left` | 왼쪽 행을 모두 유지하고 오른쪽의 일치하는 값을 연결 |
| `right` | 오른쪽 행을 모두 유지 |
| `outer` | 양쪽의 모든 키를 포함 |

**`validate="many_to_one"`은 주문 행 다수 → 상품 마스터 한 행 관계를 검증합니다.** 상품 마스터의 동일한 `product_id`가 중복되어 있으면 잘못된 행 증가를 방지하는 데 도움이 됩니다. `indicator=True`를 지정하면 `_merge` 열에서 `both`, `left_only`, `right_only` 등 매칭 상태를 볼 수 있습니다.

`merge()`로 테이블을 결합할 때는 ① 키의 자료형·공백 통일, ② 기준 테이블의 고유 키 확인, ③ 결합 전후 행 수 비교, ④ 미매칭 값 검사 순서로 검증하세요.

**중요:** Pandas의 `merge()`는 양쪽 결합 키가 결측일 때 결측끼리 연결할 수 있습니다. SQL의 `NULL` 비교와 다른 점이므로 결합 전에 필수 키의 결측 여부를 검사하는 것이 안전합니다. `join()`은 주로 인덱스를 기준으로 결합할 때 편리합니다.

**예제 코드 — [05_merge_join_validation.py](./examples/05_merge_join_validation.py)**

```python
import pandas as pd

orders = pd.DataFrame({"line_id": ["L1", "L2", "L3"], "product_id": ["P1", "P2", "PX"]})
products = pd.DataFrame({"product_id": ["P1", "P2"], "category": ["디지털", "문구"]})
merged = orders.merge(products, on="product_id", how="left", validate="many_to_one", indicator=True)
print(merged[["line_id", "product_id", "category", "_merge"]].to_string(index=False))
print("Unmatched:", int(merged["_merge"].eq("left_only").sum()))
```

**실행 결과**

```text
line_id product_id category    _merge
     L1         P1      디지털      both
     L2         P2       문구      both
     L3         PX      NaN left_only
Unmatched: 1
```

---

<a id="section-7-6"></a>
## 7.6. Concatenation & Index Alignment — 행 연결과 정렬

`pd.concat()`은 여러 테이블을 이어 붙입니다. `axis=0`은 행 방향(기본값), `axis=1`은 열 방향으로 연결합니다. 월별 파일을 하나의 표로 합칠 때는 보통 `pd.concat([jan, feb], ignore_index=True)`를 사용합니다.

하지만 **`concat()`은 관계형 결합을 수행하지 않습니다.** 키를 기준으로 다른 열을 찾는 작업에는 `merge()`를 사용하세요. `concat` 시 열 이름이 서로 다르면 누락 열이 만들어질 수 있습니다.

Pandas의 Series 간 연산은 단순한 위치가 아니라 **인덱스 레이블 기준으로 정렬**됩니다. 예제의 `A`는 10과 7이 합쳐져 17, `B`는 20과 5가 합쳐져 25입니다. 같은 위치끼리 계산하려는 의도라면 인덱스 일치 여부를 먼저 확인해야 합니다.

**예제 코드 — [06_concat_alignment.py](./examples/06_concat_alignment.py)**

```python
import pandas as pd

january = pd.DataFrame({"order_id": ["O1", "O2"], "sales_won": [10000, 15000]})
february = pd.DataFrame({"order_id": ["O3"], "sales_won": [20000]})
combined = pd.concat([january, february], ignore_index=True)
print("Rows:", len(combined))

left = pd.Series([10, 20], index=["A", "B"])
right = pd.Series([5, 7], index=["B", "A"])
print("Aligned addition:", (left + right).to_dict())
```

**실행 결과**

```text
Rows: 3
Aligned addition: {'A': 17, 'B': 25}
```

---

<a id="section-7-7"></a>
## 7.7. Reshaping — Pivot & Melt

데이터를 세로형(Long Format)과 가로형(Wide Format)으로 변환하는 작업을 Reshaping이라고 합니다.

| 형식 | 모습 | 특징 |
|---|---|---|
| Long | `store`, `month`, `sales_won` | 관측값 하나가 한 행에 존재 |
| Wide | `store`, `2026-01`, `2026-02` | 월이 열로 표현됨 |

`pivot(index=..., columns=..., values=...)`은 **한 인덱스·열 조합에 데이터가 하나만 있을 때** 사용합니다. 같은 매장과 같은 월의 행이 여러 개면 `pivot()`은 오류가 발생합니다. 먼저 집계하려면 `pivot_table()`을 사용해야 합니다.

`melt()`는 Wide 형식에서 여러 열을 다시 Long 형식으로 펼칩니다. 데이터 시각화 도구에서는 Long 형식이 편리한 경우가 많습니다. `pivot` 후 복원해도 결측이나 자료형, 열 순서는 원본과 달라질 수 있으므로 필요한 조건을 확인하세요.

**예제 코드 — [07_pivot_and_melt.py](./examples/07_pivot_and_melt.py)**

```python
import pandas as pd

long = pd.DataFrame({
    "store": ["서울", "서울", "부산", "부산"],
    "month": ["2026-01", "2026-02", "2026-01", "2026-02"],
    "sales_won": [30000, 41000, 25000, 38000],
})
wide = long.pivot(index="store", columns="month", values="sales_won")
round_trip = wide.reset_index().melt(id_vars="store", var_name="month", value_name="sales_won")
print(wide.to_string())
print("Recovered rows:", len(round_trip))
```

**실행 결과**

```text
month  2026-01  2026-02
store                  
부산       25000    38000
서울       30000    41000
Recovered rows: 4
```

---

<a id="section-7-8"></a>
## 7.8. Pivot Table & Crosstab — 교차 집계

`pivot_table()`은 중복된 조합을 집계하면서 표를 재배치합니다. 예를 들어 지역과 상품 분류의 조합별 매출 합계를 계산하는 데 적합합니다.

`pd.crosstab()`은 두 범주형 변수가 함께 등장한 **횟수**를 확인할 때 자주 사용합니다. 매출 금액과 주문 행 수는 서로 다른 통계이므로, 예제에서는 같은 데이터를 두 방식으로 계산해 비교합니다.

- `aggfunc="sum"`: 매출 금액의 합계
- `fill_value=0`: 결과 표에서 관측되지 않은 조합의 값을 0으로 표시
- `margins=True`: 필요할 때 전체 합계 추가

**주의:** 관측되지 않은 조합을 0으로 표시하는 것이 항상 적절한 것은 아닙니다. 단순히 정보가 없다는 뜻인지 실제 거래가 0건이었다는 뜻인지 확인해야 합니다.

**예제 코드 — [08_pivot_table_and_crosstab.py](./examples/08_pivot_table_and_crosstab.py)**

```python
import pandas as pd

data = pd.DataFrame({
    "region": ["서울", "서울", "서울", "부산"],
    "category": ["문구", "문구", "디지털", "문구"],
    "sales_won": [5000, 7000, 30000, 8000],
})
table = data.pivot_table(index="region", columns="category", values="sales_won", aggfunc="sum", fill_value=0)
counts = pd.crosstab(data["region"], data["category"])
print("Sales:")
print(table.to_string())
print("Row counts:")
print(counts.to_string())
```

**실행 결과**

```text
Sales:
category    디지털     문구
region                
부산            0   8000
서울        30000  12000
Row counts:
category  디지털  문구
region           
부산          0   1
서울          1   2
```

---

<a id="section-7-9"></a>
## 7.9. Time-Based Aggregation — 날짜 및 기간별 집계

시계열 데이터(Time Series)는 시간 순서가 의미를 갖는 데이터입니다. Pandas에서는 날짜 열을 `datetime64` 계열로 변환한 후 `resample()` 또는 `dt.to_period()` 등을 사용하여 기간별 통계를 만듭니다.

- `pd.to_datetime(..., format="%Y-%m-%d")`: 날짜 문자열 파싱
- `set_index("date").resample("D")`: 하루 단위 집계
- `dt.to_period("M")`: 날짜를 달력 월로 구분
- `sort_index()`: 날짜 순서 정렬

예제에서 `2026-01-03` 두 행의 합계는 15,000원입니다. `2026-01-04`에는 기록이 없으므로 일별 `sum()` 결과가 0으로 보일 수 있지만, **데이터 미수집**과 **거래 없음**은 서로 구분해야 합니다.

실제 시각이 포함된 데이터는 시간대를 저장하고, '하루'의 시작과 종료가 어느 지역 기준인지 명시해야 합니다. 이번 예제는 시간을 포함하지 않는 날짜 데이터로 제한합니다.

**예제 코드 — [09_time_based_aggregation.py](./examples/09_time_based_aggregation.py)**

```python
import pandas as pd

sales = pd.DataFrame({
    "date": pd.to_datetime(["2026-01-03", "2026-01-03", "2026-01-17", "2026-02-02"]),
    "sales_won": [10000, 5000, 22000, 8000],
})
daily = sales.set_index("date").resample("D")["sales_won"].sum()
monthly = sales.assign(month=sales["date"].dt.to_period("M").astype(str)).groupby("month")["sales_won"].sum()
print("Jan 3:", int(daily.loc["2026-01-03"]))
print("Jan 4:", int(daily.loc["2026-01-04"]))
print("Monthly:", monthly.to_dict())
```

**실행 결과**

```text
Jan 3: 15000
Jan 4: 0
Monthly: {'2026-01': 37000, '2026-02': 8000}
```

---

<a id="section-7-10"></a>
## 7.10. Rolling & Cumulative Operations — 이동·누적 계산

일별 매출의 변동을 완화하거나 일정 기간의 추세를 확인할 때 이동 계산(Rolling)을 사용할 수 있습니다. `rolling(window=3)`은 일반적으로 최근 **3개 관측 행**을 대상으로 계산합니다. 데이터가 하루에 한 행이고 날짜가 빠짐없이 정렬되어 있을 때만 3일 이동평균과 같은 의미가 됩니다.

\[\text{3일 이동평균}_t = \frac{x_{t-2}+x_{t-1}+x_t}{3}\]

`min_periods=1`을 사용하면 처음 두 날짜처럼 관측 행이 부족한 경우에도 존재하는 값만으로 평균을 계산합니다. `cumsum()`은 처음부터 해당 행까지의 누적 합계를 구합니다.

매장별로 이동평균을 계산할 때는 **매장별 그룹화와 날짜 정렬**이 필요합니다. 여러 매장의 값을 섞은 뒤 계산하면 의도와 다른 결과가 만들어집니다.

**예제 코드 — [10_rolling_cumulative.py](./examples/10_rolling_cumulative.py)**

```python
import pandas as pd

sales = pd.Series([100, 0, 300, 200, 400], index=pd.date_range("2026-01-01", periods=5, freq="D"))
rolling = sales.rolling(window=3, min_periods=1).mean()
cumulative = sales.cumsum()
print("Day 3 moving average:", float(rolling.iloc[2]))
print("Day 5 cumulative:", int(cumulative.iloc[-1]))
```

**실행 결과**

```text
Day 3 moving average: 133.33333333333334
Day 5 cumulative: 1000
```

---

<a id="section-7-11"></a>
## 7.11. Missing Dates & Zero-Fill Policy — 빈 날짜의 의미

날짜가 기록되지 않았을 때 빈 날짜를 생성하는 방법으로 `reindex(pd.date_range(...))`, `asfreq()` 등을 사용할 수 있습니다.

| 실제 상황 | 적합한 처리 |
|---|---|
| 데이터가 완전하고 해당 날짜에 판매가 없었다는 것을 확인 | 매출 0원으로 표시 가능 |
| 센서가 고장 나서 해당 날짜를 관측하지 못함 | 결측으로 보존하고 장애를 기록 |
| 파일 수집이 지연되어 최신 날짜가 빠짐 | 보완 대상 또는 미확정 상태로 유지 |

이 장의 Mini Project는 **각 거래 기록이 완전히 수집된 교육용 데이터**라는 전제를 두고 거래가 없는 날짜의 매출을 0으로 채웁니다. 이러한 전제를 모든 데이터셋에 적용하지 마세요.

**예제 코드 — [11_missing_dates_and_zero.py](./examples/11_missing_dates_and_zero.py)**

```python
import pandas as pd

observed = pd.Series(
    [1000, 2000],
    index=pd.to_datetime(["2026-01-01", "2026-01-03"]),
)
calendar = pd.date_range("2026-01-01", "2026-01-04", freq="D")
unknown = observed.reindex(calendar)
zero_assumed = unknown.fillna(0).astype("int64")
print("Missing before assumption:", int(unknown.isna().sum()))
print("After zero-fill:", zero_assumed.to_list())
```

**실행 결과**

```text
Missing before assumption: 2
After zero-fill: [1000, 0, 2000, 0]
```

---

<a id="section-7-12"></a>
## 7.12. Vectorization & Memory — 효율적인 처리

동일한 열에 단순 수치 연산을 반복할 때는 Python 행 반복보다 Pandas의 벡터화 연산이 간결하고 빠를 수 있습니다. 예를 들어 `quantity * unit_price_won`는 열 전체에 원소별 곱셈을 적용합니다.

Pandas의 `DataFrame.apply(axis=1)`는 편리하지만 행별 Python 함수 호출 비용이 발생할 수 있습니다. 간단한 수치 계산은 벡터화 연산을 먼저 검토하세요. 다만 문자열·객체 연산에서는 벡터화 표현만으로 항상 성능이나 메모리가 개선되는 것은 아닙니다.

`df.memory_usage(deep=True)`는 열별 메모리 사용량을 살펴볼 때 유용합니다. 작은 데이터에서 시간을 한 번 측정한 결과를 일반적인 성능 우위로 단정하지 말고, 작업과 데이터 크기를 동일하게 맞춰 반복 측정해야 합니다.

**예제 코드 — [12_vectorization_and_memory.py](./examples/12_vectorization_and_memory.py)**

```python
import pandas as pd

orders = pd.DataFrame({"quantity": [2, 3, 4], "price": [5000, 7000, 2000]})
vectorized = orders["quantity"] * orders["price"]
row_loop = [row.quantity * row.price for row in orders.itertuples(index=False)]
assert vectorized.to_list() == row_loop
print("Revenue:", vectorized.to_list())
print("Memory bytes:", int(orders.memory_usage(deep=True).sum()))
```

**실행 결과**

```text
Revenue: [10000, 21000, 8000]
Memory bytes: 180
```

---

<a id="section-7-13"></a>
## 7.13. Reusable Processing Pipelines — 처리 단계의 함수화

데이터 처리 코드를 여러 함수로 분리하면 각 단계의 목적과 입력·출력이 뚜렷해지고 테스트하기 쉬워집니다.

`pipe()`는 DataFrame을 함수의 첫 번째 인수로 전달하여 일련의 처리 과정을 연결합니다. 다음의 예제는 **매출 열 생성 → 지역별 집계**를 단계별 함수로 표현합니다.

```text
원본 테이블 → add_revenue() → summarize_by_region() → 결과 테이블
```

완성도 있는 파이프라인은 단순히 함수를 여러 개 호출하는 것에 그치지 않습니다. **입력 데이터 조건, 오류 시 동작, 원본 보존, 출력 데이터 구조, 결과 재현성**을 정의해야 합니다. Chapter 06의 Validation 정책을 토대로 이 장에서는 결합 관계와 집계 총액을 추가로 확인합니다.

**예제 코드 — [13_reusable_pipeline.py](./examples/13_reusable_pipeline.py)**

```python
import pandas as pd


def add_revenue(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.assign(revenue_won=frame["quantity"] * frame["price_won"])


def summarize_by_region(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.groupby("region", as_index=False).agg(revenue_won=("revenue_won", "sum"))


orders = pd.DataFrame({"region": ["서울", "서울", "부산"], "quantity": [2, 1, 3], "price_won": [5000, 5000, 3000]})
report = orders.pipe(add_revenue).pipe(summarize_by_region)
print(report.sort_values("region").to_string(index=False))
```

**실행 결과**

```text
region  revenue_won
    부산         9000
    서울        15000
```

---

<a id="section-7-14"></a>
## 7.14. Mini Project — Store Sales Transformation Pipeline

### 목표

주문 행(`order_lines.csv`)과 상품 기준정보(`products.csv`), 매장 기준정보(`stores.csv`)를 결합해 매출 보고서를 생성합니다. 이 장에서는 이미 정제된 입력 데이터를 사용한다고 가정하며, **주문 행의 보존, 참조 관계의 유효성, 매출 총액의 일치**를 주요 검증 기준으로 삼습니다.

```text
order_lines.csv ───┐
products.csv ──────┼─ 검증 → 다대일 결합 → 정수 금액 계산 ─┐
stores.csv ────────┘                                      ├─ 매장별 집계
                                                          ├─ 월별·분류별 집계
                                                          └─ 매장별 일별·7일 이동평균
                                                               ↓
                                                    CSV 4개 + JSON 요약
```

**매출 금액 정의**

\[\text{순매출액(원)} = \frac{\text{수량}\times\text{적용 단가(원)}\times(100-\text{할인율(\%)})}{100}\]

교육용 데이터에서는 금액이 정수 원 단위로 정확하게 계산되도록 구성했습니다. 1원 미만 금액이 발생하면 반올림 규칙을 임의로 적용하지 않고 오류를 발생시킵니다. 부가세, 환불, 환율, 쿠폰의 중복 적용은 이 예제의 범위에 포함하지 않습니다.

### 입력 데이터와 관계

| 파일 | 주요 키 | 행 수 | 활용 |
|---|---|---:|---|
| [order_lines.csv](./data/order_lines.csv) | `line_id` (고유), `order_id` (반복 가능) | 48 | 주문 상품별 수량·단가·할인율 |
| [products.csv](./data/products.csv) | `product_id` (고유) | 5 | 상품 분류·명칭 |
| [stores.csv](./data/stores.csv) | `store_id` (고유) | 3 | 매장·지역 |

상품과 매장의 기준 테이블에서 키가 중복되면 **한 주문 행이 여러 결과 행으로 늘어날 수 있습니다.** `validate="many_to_one"`으로 잘못된 결합 관계를 검사하고, 결합 후 누락된 기준정보가 없음을 확인합니다.

### CLI & `argparse` — 명령행 인수 처리

**CLI(Command-Line Interface)**는 터미널에서 명령과 옵션을 입력해 프로그램을 실행하는 방식입니다. Python 표준 라이브러리의 `argparse`는 `--data`, `--output`처럼 실행 시 전달한 옵션을 읽고, 도움말을 표시하고, 잘못된 인수 사용을 안내합니다. 별도 설치가 필요하지 않습니다.

```python
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="매출 보고서 실행 옵션")
parser.add_argument("--data", type=Path, default=Path("data"))
parser.add_argument("--output", type=Path, default=Path("output"))
args = parser.parse_args()

print("입력 폴더:", args.data)
print("출력 폴더:", args.output)
```

위 예제에서 `ArgumentParser()`는 인수 처리기를 만들고, `add_argument()`는 사용할 옵션을 등록하며, `parse_args()`는 명령행 인수를 해석합니다. `type=Path`는 전달된 경로 문자열을 `Path` 객체로 바꿔 주지만, 폴더의 존재나 데이터의 유효성을 자동으로 확인하지는 않습니다.

| 구성 | 의미 |
|---|---|
| `--data` | 데이터 입력 폴더를 지정하는 선택 옵션 |
| `--output` | 결과 저장 폴더를 지정하는 선택 옵션 |
| `default=...` | 옵션을 생략했을 때 사용할 기본값 |
| `args.data` | 해석된 `--data` 옵션 값에 접근 |
| `--help` / `-h` | 자동으로 생성된 도움말을 출력하고 종료 |

이 Chapter의 실제 프로젝트 코드에는 동일한 방식을 적용했습니다. `Chapter-07/`에서 다음 명령으로 확인할 수 있습니다.

```bash
python examples/14_store_sales_pipeline.py --help
python examples/14_store_sales_pipeline.py --data data --output output
```

프로젝트는 입력 데이터와 출력 경로를 추가로 검증합니다. 다음 Chapter 08에서는 이 방식을 `--data-dir`, `--output-dir`, `--parquet` 옵션으로 확장합니다.

### 파이프라인 코드

**예제 코드 — [14_store_sales_pipeline.py](./examples/14_store_sales_pipeline.py)**

아래는 완전한 실행 코드입니다. 데이터 로딩 → 검증 → 결합 → 집계 → 저장 순서로 구성했으며, 앞에서 배운 `argparse`의 `--data`, `--output` 인수로 입출력 경로를 변경할 수 있습니다. `from __future__ import annotations`는 Chapter 06에서 설명한 타입 힌트 평가 관련 선언입니다.

```python
"""Chapter 07 Mini Project: 검증된 테이블 결합 및 매출 데이터 마트 생성."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"


def load_sources(data_dir: Path = DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    orders = pd.read_csv(data_dir / "order_lines.csv", dtype={
        "line_id": "string", "order_id": "string", "store_id": "string", "product_id": "string",
        "quantity": "int64", "unit_price_won": "int64", "discount_pct": "int64",
    })
    orders["order_date"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="raise")
    products = pd.read_csv(data_dir / "products.csv", dtype={"product_id": "string"})
    stores = pd.read_csv(data_dir / "stores.csv", dtype={"store_id": "string"})
    return orders, products, stores


def validate_sources(orders: pd.DataFrame, products: pd.DataFrame, stores: pd.DataFrame) -> None:
    for frame, key in ((orders, "line_id"), (products, "product_id"), (stores, "store_id")):
        if frame[key].isna().any() or frame[key].duplicated().any():
            raise ValueError(f"Missing or duplicated key: {key}")
    required = ["line_id", "order_id", "order_date", "store_id", "product_id", "quantity", "unit_price_won", "discount_pct"]
    if orders[required].isna().any().any():
        raise ValueError("Missing required order field")
    if (orders["quantity"] < 1).any() or (orders["unit_price_won"] < 0).any():
        raise ValueError("Invalid quantity or unit price")
    if (~orders["discount_pct"].between(0, 100)).any():
        raise ValueError("Discount percentage is outside 0..100")
    if orders["order_date"].isna().any():
        raise ValueError("Invalid order date")


def enrich_orders(orders: pd.DataFrame, products: pd.DataFrame, stores: pd.DataFrame) -> pd.DataFrame:
    result = orders.merge(
        products[["product_id", "product_name", "category"]],
        on="product_id", how="left", validate="many_to_one", indicator="product_match",
    )
    if result["product_match"].ne("both").any():
        raise ValueError("Unknown product_id in orders")
    result = result.drop(columns="product_match").merge(
        stores[["store_id", "store_name", "region"]],
        on="store_id", how="left", validate="many_to_one", indicator="store_match",
    )
    if result["store_match"].ne("both").any():
        raise ValueError("Unknown store_id in orders")
    result = result.drop(columns="store_match")
    gross = result["quantity"] * result["unit_price_won"]
    numerator = gross * (100 - result["discount_pct"])
    if (numerator % 100).ne(0).any():
        raise ValueError("Discount creates fractional KRW: rounding policy required")
    result["net_sales_won"] = numerator // 100
    result["month"] = result["order_date"].dt.strftime("%Y-%m")
    return result.sort_values("line_id").reset_index(drop=True)


def make_summaries(frame: pd.DataFrame, store_ids: pd.Series) -> dict[str, pd.DataFrame]:
    by_store = frame.groupby(["store_id", "store_name", "region"], as_index=False).agg(
        order_lines=("line_id", "size"), orders=("order_id", "nunique"),
        units=("quantity", "sum"), net_sales_won=("net_sales_won", "sum"),
    ).sort_values("store_id").reset_index(drop=True)
    by_category_month = frame.groupby(["month", "category"], as_index=False).agg(
        order_lines=("line_id", "size"), units=("quantity", "sum"),
        net_sales_won=("net_sales_won", "sum"),
    ).sort_values(["month", "category"]).reset_index(drop=True)
    sparse_daily = frame.groupby(["order_date", "store_id"], as_index=False).agg(
        order_lines=("line_id", "size"), net_sales_won=("net_sales_won", "sum"),
    )
    # 예제의 거래 기록은 모든 날짜가 완전히 수집되었다는 전제. 없는 거래일은 0원.
    calendar = pd.date_range(frame["order_date"].min(), frame["order_date"].max(), freq="D")
    full_index = pd.MultiIndex.from_product(
        [calendar, sorted(store_ids.tolist())], names=["order_date", "store_id"],
    )
    daily = (sparse_daily.set_index(["order_date", "store_id"])
             .reindex(full_index, fill_value=0).reset_index())
    daily = daily.sort_values(["store_id", "order_date"]).reset_index(drop=True)
    daily["rolling_7d_avg_won"] = (daily.groupby("store_id")["net_sales_won"]
        .transform(lambda values: values.rolling(window=7, min_periods=1).mean())
        .round(2))
    daily["cumulative_sales_won"] = daily.groupby("store_id")["net_sales_won"].cumsum()
    return {"sales_by_store": by_store, "sales_by_category_month": by_category_month,
            "sales_daily_by_store": daily}


def run_pipeline(data_dir: Path = DATA_DIR, output_dir: Path = OUTPUT_DIR) -> dict[str, object]:
    orders, products, stores = load_sources(data_dir)
    validate_sources(orders, products, stores)
    enriched = enrich_orders(orders, products, stores)
    reports = make_summaries(enriched, stores["store_id"])
    assert len(enriched) == len(orders), "Merge must not multiply source rows"
    assert int(reports["sales_by_store"]["net_sales_won"].sum()) == int(enriched["net_sales_won"].sum())
    assert int(reports["sales_by_category_month"]["net_sales_won"].sum()) == int(enriched["net_sales_won"].sum())
    summary = {
        "source_lines": int(len(orders)),
        "distinct_orders": int(orders["order_id"].nunique()),
        "stores": int(stores["store_id"].nunique()),
        "products": int(products["product_id"].nunique()),
        "net_sales_won": int(enriched["net_sales_won"].sum()),
        "first_date": enriched["order_date"].min().strftime("%Y-%m-%d"),
        "last_date": enriched["order_date"].max().strftime("%Y-%m-%d"),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, report in {"enriched_order_lines": enriched, **reports}.items():
        to_write = report.copy()
        if "order_date" in to_write:
            to_write["order_date"] = to_write["order_date"].dt.strftime("%Y-%m-%d")
        to_write.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8", lineterminator="\n")
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate validated store sales summaries")
    parser.add_argument("--data", type=Path, default=DATA_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    arguments = parser.parse_args()
    print(json.dumps(run_pipeline(arguments.data, arguments.output), ensure_ascii=False, sort_keys=True))
```

**실행 방법** — `Chapter-07/` 디렉터리 기준

```bash
python examples/14_store_sales_pipeline.py
```

**기본 실행 결과**

```json
{"distinct_orders": 24, "first_date": "2026-01-01", "last_date": "2026-02-14", "net_sales_won": 1523300, "products": 5, "source_lines": 48, "stores": 3}
```

**생성되는 파일**

| 경로 | 내용 |
|---|---|
| `output/enriched_order_lines.csv` | 상품·매장 정보가 연결된 원본 주문 행, 순매출 열 포함 |
| `output/sales_by_store.csv` | 매장별 주문 행·고유 주문 수·수량·매출 |
| `output/sales_by_category_month.csv` | 월별·상품 분류별 집계 |
| `output/sales_daily_by_store.csv` | 매장별 모든 날짜, 매출, 7일 이동평균, 누적매출 |
| `output/summary.json` | 처리한 행 수·주문 수·매장 수·상품 수·총액·날짜 범위 |

### 검증 항목

1. 원본 주문 행 수 48건을 결합 후에도 유지합니다.
2. 상품과 매장 기준정보의 키는 고유해야 합니다.
3. 모든 주문의 상품·매장 키가 기준 테이블과 일치해야 합니다.
4. 매장별 합계와 월별 분류 합계가 원본 순매출 총액과 일치해야 합니다.
5. 동일한 입력으로 재실행하면 동일한 출력 파일이 생성되어야 합니다.
6. 매장별 이동평균은 각 매장의 날짜 순서대로 계산합니다.

**주의:** 날짜별 매출이 없는 날을 0으로 채우는 것은 수집이 완전하다는 교육용 전제에 따른 정책입니다. 누락된 관측값까지 0으로 만드는 일반 규칙이 아닙니다.

추가로 아래 명령을 실행하면 결합 오류, 집계 총액, 재실행 일관성 등을 검증하는 자동 테스트를 수행할 수 있습니다.

```bash
python -m unittest discover -s tests -v
```

---

<a id="section-7-15"></a>
## 7.15. Coding Practice

각 연습문제의 `exercises/` 파일에는 미완성 함수가 있고, `solutions/`에는 모범답안이 있습니다. 정답 확인 전 시작 코드를 먼저 구현하고, 정상·오류 조건을 함께 확인하세요.


| 번호 | 문제 | 시작 코드 | 정답 코드 |
|:---:|---|---|---|
| 01 | Conditional Sales Columns | [문제](./exercises/01_conditional_columns.py) | [모범답안](./solutions/01_conditional_columns.py) |
| 02 | Region Summary | [문제](./exercises/02_groupby_region.py) | [모범답안](./solutions/02_groupby_region.py) |
| 03 | Safe Product Merge | [문제](./exercises/03_safe_product_merge.py) | [모범답안](./solutions/03_safe_product_merge.py) |
| 04 | Pivot & Melt Round Trip | [문제](./exercises/04_pivot_melt_roundtrip.py) | [모범답안](./solutions/04_pivot_melt_roundtrip.py) |
| 05 | Daily Rolling Sum | [문제](./exercises/05_daily_rolling.py) | [모범답안](./solutions/05_daily_rolling.py) |



### Exercise 01 — Conditional Sales Columns

`quantity × unit_price_won`으로 `sales_won`을 계산한 후, 30,000원 이상이면 `대량`, 그렇지 않으면 `일반`으로 표시합니다. **원본 DataFrame은 변경하지 않습니다.**

**실행 예시**

```text
 quantity  unit_price_won  sales_won size_class
        2           10000      20000         일반
        4           10000      40000         대량
        1            5000       5000         일반
```


### Exercise 02 — Region Summary

`region`을 기준으로 주문 행 수(`line_count`), 판매 수량 합계(`units`), 매출 합계(`sales_won`)를 구하고 지역명 오름차순으로 반환합니다.

**실행 예시**

```text
region  line_count  units  sales_won
    부산           1      3       9000
    서울           2      3      15000
```


### Exercise 03 — Safe Product Merge

주문 정보에 상품의 `category`를 연결합니다. 상품 기준정보는 `product_id`가 고유해야 하며, 미등록 상품 ID가 존재하면 `ValueError`로 처리합니다.

**실행 예시**

```text
line_id product_id category
     L1         P1      디지털
     L2         P2       문구
```


### Exercise 04 — Pivot & Melt Round Trip

`store`, `month`, `sales_won`으로 구성된 Long 테이블을 Wide로 바꾼 뒤 `melt()`로 복원하고, 정렬된 두 결과를 반환합니다. 각 매장·월 조합은 하나만 존재한다고 가정합니다.

**실행 예시**

```text
month  2026-01  2026-02
store                  
A           10       20
B           30       40
store   month  sales_won
    A 2026-01         10
    A 2026-02         20
    B 2026-01         30
    B 2026-02         40
```


### Exercise 05 — Daily Rolling Sum

동일 날짜의 매출을 합친 뒤 지정한 시작일~종료일의 전체 날짜를 구성합니다. 미기록일은 거래가 없었다는 전제하에 0원으로 채우고 3일 이동합을 계산합니다.

**실행 예시**

```text
      date  sales_won  rolling_3d_sum
2026-01-01        100             100
2026-01-02          0             100
2026-01-03        250             350
2026-01-04          0             250
```


연습문제의 정답을 직접 실행할 때는 `python solutions/01_conditional_columns.py`처럼 실행합니다. `tests/test_chapter07.py`에서 오류 입력과 원본 불변성까지 확인할 수 있습니다.

---

<a id="section-7-16"></a>
## 7.16. Quiz & Summary

### Quiz

각 문항은 정답과 해설을 개별적으로 펼쳐 확인할 수 있습니다.


**Q1.** `assign()`을 사용해 계산 열을 추가한 경우 기존 DataFrame의 값을 반드시 변경하나요?

<details>
<summary>Q1. 정답 및 해설 확인</summary>

**정답:** 아닙니다. `assign()`은 새로운 DataFrame을 반환합니다. 결과를 변수에 할당해야 하며, 원본 객체의 변경 여부와 반환 객체를 혼동하면 안 됩니다.

</details>


**Q2.** `map()`으로 코드 이름을 변환했는데 사전에 없는 코드가 나타나면 어떤 값을 확인해야 하나요?

<details>
<summary>Q2. 정답 및 해설 확인</summary>

**정답:** 매핑되지 않은 값은 결측(`NaN`/`NA`)이 될 수 있으므로 `isna()` 등으로 누락 건수를 검사해야 합니다. 무조건 기본값으로 대체하지 않습니다.

</details>


**Q3.** 주문 상품 행이 10개이지만 주문 ID가 6개라면 `size()`와 `nunique()`의 값은 각각 무엇인가요?

<details>
<summary>Q3. 정답 및 해설 확인</summary>

**정답:** 행 수를 세는 `size()`는 10, 고유한 주문 ID를 세는 `nunique()`는 6입니다. 행 단위와 주문 단위를 구분해야 합니다.

</details>


**Q4.** 그룹별 합계를 구하되 원래 DataFrame의 각 행은 유지하고 싶다면 어떤 메서드를 사용하나요?

<details>
<summary>Q4. 정답 및 해설 확인</summary>

**정답:** `groupby(...)[열].transform("sum")`을 사용할 수 있습니다. `agg()`는 대개 그룹별 요약 행으로 축약합니다.

</details>


**Q5.** 주문 행 다수에 상품 기준정보 하나를 붙이는 `merge()`에서 중복 기준 키를 방지하려면 무엇을 지정하나요?

<details>
<summary>Q5. 정답 및 해설 확인</summary>

**정답:** `validate="many_to_one"`을 사용합니다. 오른쪽 기준 테이블의 결합 키가 고유하지 않으면 오류를 발생시켜 행이 불필요하게 늘어나는 것을 방지합니다.

</details>


**Q6.** Pandas `merge()`에서 양쪽 결합 키가 모두 결측이면 SQL의 `NULL`과 항상 동일하게 처리되나요?

<details>
<summary>Q6. 정답 및 해설 확인</summary>

**정답:** 아닙니다. Pandas는 양쪽 결합 키의 결측끼리 연결할 수 있습니다. 필수 키는 병합 전에 결측 여부를 검사해야 합니다.

</details>


**Q7.** 서로 다른 월의 주문 테이블을 행 방향으로 이어 붙일 때 가장 직접적인 방법은 무엇인가요?

<details>
<summary>Q7. 정답 및 해설 확인</summary>

**정답:** `pd.concat([january, february], ignore_index=True)`가 적합합니다. `merge()`는 공통 키를 기준으로 열 정보를 결합할 때 사용합니다.

</details>


**Q8.** 같은 매장·월 조합의 행이 2개일 때 `pivot()`이 반드시 합계를 계산하나요?

<details>
<summary>Q8. 정답 및 해설 확인</summary>

**정답:** 아닙니다. `pivot()`은 중복된 인덱스·열 조합에 대해 오류를 발생시킵니다. 합산할 필요가 있다면 `pivot_table(..., aggfunc="sum")`을 사용합니다.

</details>


**Q9.** `pd.crosstab(region, category)`의 기본 출력 값은 무엇을 나타내나요?

<details>
<summary>Q9. 정답 및 해설 확인</summary>

**정답:** 지역과 카테고리의 각 조합에 속하는 행 개수입니다. 기본 결과가 매출 합계인 것은 아닙니다.

</details>


**Q10.** 시계열에 하루 기록이 없다면 반드시 그날의 매출을 0원으로 채워야 하나요?

<details>
<summary>Q10. 정답 및 해설 확인</summary>

**정답:** 아닙니다. 데이터가 완전히 수집되었고 거래가 없었다는 것을 확인했을 때만 0원이 적절할 수 있습니다. 수집 누락이면 결측 상태를 유지해야 합니다.

</details>


**Q11.** `rolling(window=3)`은 날짜가 불규칙할 때도 항상 최근 3일을 뜻하나요?

<details>
<summary>Q11. 정답 및 해설 확인</summary>

**정답:** 아닙니다. 정수 `window=3`은 일반적으로 최근 3개 행(관측값)을 가리킵니다. 3일 단위로 해석하려면 날짜 빈도와 정렬을 확인하거나 시간 기반 윈도우를 사용해야 합니다.

</details>


**Q12.** 할인 계산에서 결과가 1원 미만 단위로 떨어졌을 때 이 장의 Mini Project는 어떻게 처리하나요?

<details>
<summary>Q12. 정답 및 해설 확인</summary>

**정답:** 오류를 발생시킵니다. 실제 금액 처리에 필요한 반올림·절사 정책이 정해지지 않았으므로 임의로 적용하지 않습니다.

</details>


**Q13. `argparse`에서 `parser.add_argument("--data", type=Path, default=Path("data"))`를 작성했다면 `--data`를 생략했을 때 어떤 값이 사용되나요?**

<details>
<summary>Q13. 정답 및 해설 확인</summary>

**정답:** `Path("data")`가 기본값으로 사용됩니다. `type=Path`는 문자열을 경로 객체로 변환하지만 폴더가 실제로 존재하는지까지 검사하지는 않습니다.

</details>

### Summary

- **Transformation:** 계산 열, 값 매핑, 조건 처리로 데이터의 형태·표현 변경
- **Grain:** 주문 한 건과 주문 상품 한 줄의 집계 단위 구별
- **GroupBy:** 그룹 키 기준의 합계·고유 수·여러 통계 계산
- **`transform()`:** 원래 행 수를 유지하면서 그룹별 결과 추가
- **Merge & Join:** 참조 키로 테이블을 결합하고 관계·미매칭 검증
- **`validate="many_to_one"`:** 기준 테이블의 중복 키로 인한 행 증가 방지
- **Concat:** 행·열 방향으로 테이블 연결, Index Alignment 주의
- **Pivot & Melt:** Long↔Wide 변환, 중복 조합이면 `pivot_table()` 고려
- **Time-Based Aggregation:** 날짜 파싱·정렬, 일별·월별 집계
- **Rolling & Cumulative:** 이동평균·누적합, 빈 날짜의 의미 확인
- **Vectorization:** 열 단위 계산을 우선 고려하고 측정으로 성능 확인
- **Pipeline:** 입력 검증, 변환, 집계, 출력, 테스트를 함수로 구성
- **CLI / `argparse`:** 명령행 옵션·기본값·도움말을 구성하고 입력·출력 경로를 전달
- **Validation:** 결합 전후 행 수와 집계 총액, 반복 실행 결과 확인

### References

- [Python — `argparse`](https://docs.python.org/3/library/argparse.html)

- [Pandas User Guide — Group By](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Pandas User Guide — Merge, Join, Concatenate](https://pandas.pydata.org/docs/user_guide/merging.html)
- [Pandas User Guide — Reshaping & Pivot Tables](https://pandas.pydata.org/docs/user_guide/reshaping.html)
- [Pandas User Guide — Time Series](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [Pandas User Guide — Windowing Operations](https://pandas.pydata.org/docs/user_guide/window.html)
- [Pandas 3.0 — Copy-on-Write & String Data Type](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html)
- [NumPy — Array Operations](https://numpy.org/doc/stable/user/basics.html)

---

[← Data Processing 목차](../README.md) · [Chapter 06 — Data Cleaning & Validation](../Chapter-06/)
