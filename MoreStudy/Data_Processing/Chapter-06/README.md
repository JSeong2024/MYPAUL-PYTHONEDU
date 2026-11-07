# Chapter 06. Data Cleaning & Validation

데이터의 결측치, 중복, 자료형 오류, 비정상적인 값과 날짜를 탐색하고, **정제 규칙을 근거로 데이터를 유지·제외·검토하는 방법**을 학습합니다. Pandas를 이용한 데이터 품질 검증부터 원본 보존, 감사 로그, 품질 보고서 작성까지 연결합니다.

본 자료는 **Python 3.13.5 / Pandas 2.2.3 / NumPy 2.3.5** 환경에서 실행 검증했습니다. Pandas 버전이나 데이터 유형에 따라 표시 형식이 일부 달라질 수 있습니다. 사용된 데이터는 학습용 가상 데이터이며, 실제 주문이나 개인 정보를 포함하지 않습니다.

<details>
<summary><strong>선행 학습 목록</strong></summary>

- [Chapter 01 — Introduction to Data Processing](../Chapter-01/)
- [Chapter 02 — Python Data Structures](../Chapter-02/)
- [Chapter 03 — NumPy Fundamentals](../Chapter-03/)
- [Chapter 04 — Pandas & DataFrames](../Chapter-04/)
- [Chapter 05 — File I/O & Data Formats](../Chapter-05/)

</details>

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [6.1](#section-6-1) | Data Quality와 Cleaning의 목적 |
| [6.2](#section-6-2) | Missing Values — 결측치 탐색 |
| [6.3](#section-6-3) | Missing Data Strategies — 삭제와 대체 |
| [6.4](#section-6-4) | Duplicate Records — 중복 행과 고유 키 |
| [6.5](#section-6-5) | Data Type Conversion — 숫자와 자료형 검증 |
| [6.6](#section-6-6) | String Cleaning — 문자열 표준화 |
| [6.7](#section-6-7) | Outlier Detection — 이상치 탐색 |
| [6.8](#section-6-8) | Date & Time Handling — 날짜 유효성 |
| [6.9](#section-6-9) | Cross-Field & Schema Validation — 관계와 규칙 검증 |
| [6.10](#section-6-10) | Validation Rules & Quality Report — 검증 결과 기록 |
| [6.11](#section-6-11) | Reproducible Cleaning & Audit Trail |
| [6.12](#section-6-12) | Idempotent Cleaning — 반복 실행 시 결과 일관성 |
| [6.13](#section-6-13) | Mini Project — Order Data Quality Pipeline |
| [6.14](#section-6-14) | Coding Practice |
| [6.15](#section-6-15) | Quiz & Summary |

## Getting Started

**권장 환경:** Python 3.13 이상, NumPy 및 Pandas 설치. 모든 예제는 인터넷 접속 없이 실행됩니다.

```bash
python -m pip install -r requirements.txt
```

**실행 기준 경로:** `Data_Processing/Chapter-06/`

```bash
python examples/01_quality_dimensions.py
python examples/07_outlier_iqr.py
python examples/13_order_quality_pipeline.py
python -m unittest discover -s tests -v
```

Windows 환경에서 `python` 명령을 찾을 수 없다면 설치한 Python 실행기와 가상환경을 확인하거나 `py`를 사용할 수 있습니다.

```text
Chapter-06/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── DATA_DICTIONARY.md
│   ├── raw_orders.csv
│   └── cleaning_policy.json
├── examples/
│   ├── 01_quality_dimensions.py
│   ├── ...
│   └── 13_order_quality_pipeline.py
├── exercises/
├── solutions/
├── tests/
│   └── test_chapter06.py
└── output/                 # 실행 시 생성, Git 추적 제외
```

원본 데이터의 필드와 정제 규칙은 [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)에 정리했습니다. `data/`의 원본은 수정하지 않고 `output/`에 새 결과를 생성합니다.

---

<a id="section-6-1"></a>
## 6.1. Data Quality와 Cleaning의 목적

데이터 정제(Data Cleaning)는 단순히 비어 있는 값을 제거하는 과정이 아닙니다. **데이터가 사용 목적에 맞는지 검증한 뒤, 정해진 정책에 따라 수정하거나 분리하는 과정**입니다. 동일한 값이라도 데이터의 의미와 업무 규칙에 따라 다른 판단이 필요합니다.

| 품질 요소 | 의미 | 주문 데이터 예시 |
|---|---|---|
| 정확성(Accuracy) | 실제 사실과 부합하는가? | 실제 결제 금액과 기록된 금액의 일치 |
| 완전성(Completeness) | 필요한 항목이 존재하는가? | 주문 ID·날짜의 누락 여부 |
| 유효성(Validity) | 값이 허용 범위·형식에 맞는가? | 수량 1 이상, 정해진 날짜 형식 |
| 일관성(Consistency) | 표기·규칙이 통일되어 있는가? | `seoul`과 `Seoul`의 표기 통일 |
| 고유성(Uniqueness) | 중복되어서는 안 되는 값이 유일한가? | 주문 ID 중복 여부 |
| 적시성(Timeliness) | 데이터가 필요한 시점에 갱신되었는가? | 어제 주문 데이터의 수집 지연 |

**정확성과 유효성은 다릅니다.** 형식상 유효한 금액이라도 실제 결제 기록과 다르면 정확하지 않은 값입니다. 코드만으로 알 수 없는 사실은 외부 기록이나 담당자의 확인이 필요합니다.

아래 예제에서는 누락, 중복, 유효하지 않은 단가를 간단하게 계산합니다.

**주의:** 이 예제는 각 품질 지표를 **독립적으로 집계**합니다. 하나의 행이 여러 문제를 동시에 가질 수 있으므로 지표의 합계가 잘못된 행의 개수와 항상 같지는 않습니다.

**예제 코드 — [01_quality_dimensions.py](./examples/01_quality_dimensions.py)**

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": ["ORD-001", "ORD-002", "ORD-002"],
    "quantity": [2, None, 3],
    "unit_price": [1500, 2500, -5],
})
print("Rows:", len(orders))
print("Missing quantity:", int(orders["quantity"].isna().sum()))
print("Duplicate order ID:", int(orders["order_id"].duplicated().sum()))
print("Invalid unit price:", int((orders["unit_price"] <= 0).sum()))
```

**실행 결과**

```text
Rows: 3
Missing quantity: 1
Duplicate order ID: 1
Invalid unit price: 1
```

---

<a id="section-6-2"></a>
## 6.2. Missing Values — 결측치 탐색

결측치(Missing Value)는 값이 기록되지 않았거나 사용할 수 없는 상태입니다. `None`, `numpy.nan`, `pandas.NA`, `NaT`는 데이터의 자료형에 따라 서로 다른 형태로 등장할 수 있습니다. Pandas에서는 일반적으로 `isna()`와 `notna()`로 확인합니다.

문자열 열의 빈 문자열 `""`이나 공백 문자열 `"   "`은 **자동으로 결측치가 되지 않을 수 있습니다.** 특히 `keep_default_na=False`로 CSV를 읽으면 원본의 빈 문자열을 그대로 보존합니다. 공백을 제거한 뒤 결측 상태로 변환하는 처리가 필요합니다.

| 함수 | 역할 |
|---|---|
| `isna()` | 값이 결측인지 검사 |
| `notna()` | 값이 존재하는지 검사 |
| `isna().sum()` | 열별 결측 수 계산 |
| `isna().mean()` | 열별 결측 비율 계산(0~1) |
| `replace("", pd.NA)` | 정제된 빈 문자열을 명시적 결측으로 변경 |

결측 비율을 계산할 때 분모는 해당 열에서 관찰한 전체 행 수입니다. **결측이 0개라는 사실이 그 열이 올바르다는 뜻은 아닙니다.** 예를 들어 `"unknown"`은 문자열로 존재하지만 수치 변환에는 실패할 수 있습니다.

**예제 코드 — [02_missing_profile.py](./examples/02_missing_profile.py)**

```python
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
data = pd.read_csv(ROOT / "data/raw_orders.csv", dtype="string", keep_default_na=False)
data = data.apply(lambda column: column.str.strip().replace("", pd.NA))
print("Missing quantity:", int(data["quantity"].isna().sum()))
print("Missing region:", int(data["region"].isna().sum()))
print("Missing price:", int(data["unit_price"].isna().sum()))
```

**실행 결과**

```text
Missing quantity: 1
Missing region: 1
Missing price: 0
```

---

<a id="section-6-3"></a>
## 6.3. Missing Data Strategies — 삭제와 대체

결측치를 처리하는 방법은 값의 의미에 따라 선택합니다. `dropna()`로 행을 제외하거나, `fillna()`로 정해진 값을 채우거나, 결측 상태 자체를 보존할 수 있습니다.

| 방법 | 사용 상황 | 주의 |
|---|---|---|
| 삭제(`dropna`) | 필수 식별자나 날짜가 없는 기록 | 표본 수 감소, 편향 발생 가능 |
| 고정값 대체(`fillna`) | 원래 0이 의미 있는 항목 | 결측과 실제 0을 혼동하지 않기 |
| 평균·중앙값 대체 | 탐색 목적의 연속형 측정값 | 분포와 분산 변화 가능 |
| 이전 값 대체(`ffill`) | 연속 시점의 상태형 데이터 | 장기간 결측에 부정확할 수 있음 |
| 결측 유지 | 추가 확인이 필요한 데이터 | 후속 단계에서 결측 처리 명시 필요 |

**예제에서는 중앙값 24를 사용하여 누락된 측정값을 채웁니다.** 다만 실측 온도 등에서 대체값을 사용했다면 원본 측정과 추정값을 구분할 수 있도록 별도 열이나 로그를 남기는 방식이 좋습니다.

특히 시험 점수처럼 미응시자를 0점으로 처리하면 분석 결과가 달라지므로, 임의의 대체 규칙을 적용하지 않습니다.

**예제 코드 — [03_missing_strategies.py](./examples/03_missing_strategies.py)**

```python
import pandas as pd

values = pd.Series([18.0, None, 24.0, None, 30.0], name="temperature")
print("Valid measurements:", int(values.count()))
print("Drop missing:", values.dropna().tolist())
print("Fill with median:", values.fillna(values.median()).tolist())
print("Forward fill:", values.ffill().tolist())
```

**실행 결과**

```text
Valid measurements: 3
Drop missing: [18.0, 24.0, 30.0]
Fill with median: [18.0, 24.0, 24.0, 24.0, 30.0]
Forward fill: [18.0, 18.0, 24.0, 24.0, 30.0]
```

---

<a id="section-6-4"></a>
## 6.4. Duplicate Records — 중복 행과 고유 키

중복은 **행 전체가 완전히 동일한 중복**과 **식별자(Key)가 같은 중복**으로 나눠 생각해야 합니다. `duplicated()`의 기본 동작은 모든 열을 비교하지만 `subset=["order_id"]`를 지정하면 ID 중복만 검사합니다.

| 형태 | Pandas 표현 | 의미 |
|---|---|---|
| 완전 중복 | `df.duplicated()` | 모든 열 값이 같은 행 |
| ID 중복 | `df.duplicated(subset=["order_id"])` | 같은 주문 ID가 반복 |
| 첫 기록 유지 | `drop_duplicates(..., keep="first")` | 이후 중복 행 제외 |
| 모든 중복 표시 | `duplicated(..., keep=False)` | 첫 기록까지 표시 |

**중복 ID라고 해서 반드시 같은 내용은 아닙니다.** 예시에서는 `ORD-002`의 수량이 서로 다르지만 같은 주문 ID이므로 고유성 문제가 발생합니다. 어떤 기록을 유지할지는 최신 수정 시점, 원본 시스템 등 별도의 근거가 필요합니다. 이 Chapter의 Mini Project는 학습을 위해 **첫 기록을 유지**하는 정책을 명시합니다.

또한 DataFrame의 인덱스 중복과 주문 ID 컬럼 중복은 별도의 문제입니다.

**예제 코드 — [04_duplicates.py](./examples/04_duplicates.py)**

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": ["ORD-001", "ORD-002", "ORD-002"],
    "quantity": [1, 2, 4],
})
print("Exact row duplicates:", int(orders.duplicated().sum()))
print("Duplicate IDs:", int(orders.duplicated(subset=["order_id"]).sum()))
print("Kept first IDs:", orders.drop_duplicates(subset=["order_id"])["order_id"].tolist())
```

**실행 결과**

```text
Exact row duplicates: 0
Duplicate IDs: 1
Kept first IDs: ['ORD-001', 'ORD-002']
```

---

<a id="section-6-5"></a>
## 6.5. Data Type Conversion — 숫자와 자료형 검증

외부 파일에서 읽은 수량이 `"12"`라면 문자열입니다. 수치 계산을 하려면 숫자로 변환해야 하며, 변환 가능한지와 **값의 범위**를 별도로 확인해야 합니다.

- `pd.to_numeric(values, errors="coerce")`: 변환 실패를 결측으로 표시
- `.notna()`: 변환이 성공한 값 검사
- `.mod(1).eq(0)`: 정수 여부 확인(정수형 수량 규칙)
- `.between(1, 100)`: 허용 범위 확인
- `astype("Int64")`: 결측값을 허용하는 Pandas 정수 자료형(대문자 `I`)

`errors="coerce"`는 **잘못된 원본 값을 올바른 값으로 고치는 기능이 아닙니다.** 변환 실패 위치를 표시할 뿐이며, 원본 문자열 `"unknown"`이 왜 들어왔는지는 별도로 확인해야 합니다. 큰 정수를 실수형으로 변환하면 정밀도 문제가 생길 수 있으므로, 금액이나 식별자를 다룰 때는 자료형 정책도 확인해야 합니다.

**예제 코드 — [05_numeric_conversion.py](./examples/05_numeric_conversion.py)**

```python
import pandas as pd

raw = pd.Series(["12", " 3 ", "unknown", "1.5", ""], dtype="string")
parsed = pd.to_numeric(raw, errors="coerce")
integer_ok = parsed.notna() & parsed.gt(0) & parsed.mod(1).eq(0)
print("Valid positive integers:", int(integer_ok.fillna(False).sum()))
print("Invalid values:", int((~integer_ok.fillna(False)).sum()))
```

**실행 결과**

```text
Valid positive integers: 2
Invalid values: 3
```

---

<a id="section-6-6"></a>
## 6.6. String Cleaning — 문자열 표준화

외부 데이터는 같은 지역이 `" seoul "`, `"SEOUL"`, `"Seoul"` 등 여러 형태로 기록될 수 있습니다. 비교하거나 집계하기 전에 공백·대소문자·표기 규칙을 통일합니다.

1. `.str.strip()`으로 앞뒤 공백 제거
2. `.str.casefold()`로 비교용 표기 통일(영문 기준 대소문자 통일에 유용)
3. 사전에 정의한 허용 값으로 매핑
4. 매핑되지 않은 값은 **임의로 교정하지 않고 검토**

예제에서 `"unknown"`은 허용 지역이 아니므로 `NaN`으로 표시한 후 출력할 때만 `INVALID`로 변경합니다. 데이터 자체에 `INVALID`라는 새 지역을 생성하는 것이 아닙니다.

전화번호, 우편번호, 상품 코드처럼 앞의 `0`이 중요한 값은 숫자보다는 문자열로 보관해야 합니다.

**예제 코드 — [06_string_standardization.py](./examples/06_string_standardization.py)**

```python
import pandas as pd

raw = pd.Series([" seoul ", "BUSAN", "Gwangju", "unknown"], dtype="string")
lookup = {"seoul": "Seoul", "busan": "Busan", "gwangju": "Gwangju"}
normalized = raw.str.strip().str.casefold().map(lookup)
print("Normalized:", normalized.fillna("INVALID").tolist())
```

**실행 결과**

```text
Normalized: ['Seoul', 'Busan', 'Gwangju', 'INVALID']
```

---

<a id="section-6-7"></a>
## 6.7. Outlier Detection — 이상치 탐색

이상치(Outlier)는 다른 값과 비교해 눈에 띄게 벗어난 관측값입니다. **이상치라는 이유만으로 오류는 아닙니다.** 실제 고가 주문일 수도 있고 센서 오작동일 수도 있으므로, 통계적 탐색과 도메인 규칙을 구분합니다.

이 예제에서는 사분위수 범위(Interquartile Range, IQR)를 사용합니다.

\[
IQR = Q_3-Q_1,\qquad
L=Q_1-1.5\times IQR,\qquad
U=Q_3+1.5\times IQR
\]

`L` 미만 또는 `U` 초과인 값을 **검토 후보**로 표시합니다. 본 예제에서는 `Q1=15`, `Q3=19`, `IQR=4`이므로 범위가 `9~25`이고 `100`이 후보가 됩니다.

IQR은 표본이 작거나 심하게 비대칭인 분포에서 과도하게 많은 값을 표시할 수 있습니다. 계절성·지역·상품군에 따라 정상 범위가 다를 수 있으므로 기준을 설명할 수 있어야 합니다. Mini Project에서는 **계약상 허용 최대 가격**과 **고가 주문 검토 임계값**을 구분하여 사용합니다.

**예제 코드 — [07_outlier_iqr.py](./examples/07_outlier_iqr.py)**

```python
import pandas as pd

prices = pd.Series([12, 14, 15, 15, 16, 18, 19, 21, 100])
q1, q3 = prices.quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
flagged = prices.loc[~prices.between(lower, upper)]
print(f"IQR bounds: {lower:.1f} to {upper:.1f}")
print("Review candidates:", flagged.tolist())
```

**실행 결과**

```text
IQR bounds: 9.0 to 25.0
Review candidates: [100]
```

---

<a id="section-6-8"></a>
## 6.8. Date & Time Handling — 날짜 유효성

날짜는 문자열 비교보다 날짜 자료형으로 변환해 검사하는 편이 안전합니다. `pd.to_datetime(..., format="%Y-%m-%d", errors="coerce")`는 지정된 형식으로 변환할 수 없는 값을 `NaT`로 표시합니다.

| 항목 | 확인할 내용 |
|---|---|
| 형식 | `YYYY-MM-DD`와 같은 데이터 계약 |
| 달력상 유효성 | 2월 30일 등 존재하지 않는 날짜 제외 |
| 허용 범위 | 데이터 수집 기간 안에 있는지 확인 |
| 시간대 | UTC와 현지 시각 혼용 여부 |
| 중복 시각 | 표준시 전환(DST) 등에 따른 모호성 |

Mini Project에서는 날짜만 저장된 주문 데이터를 다루므로 **시간대 없는 날짜**로 처리합니다. 실제 시간 정보가 들어온다면 시각과 시간대의 의미를 별도로 정의해야 합니다. 문자열이 특정 형식이어야 한다면 정규식 검사와 날짜 파싱을 함께 사용할 수 있습니다.

**예제 코드 — [08_dates.py](./examples/08_dates.py)**

```python
import pandas as pd

raw = pd.Series(["2026-10-01", "2026-02-30", "2026-10-03"], dtype="string")
parsed = pd.to_datetime(raw, format="%Y-%m-%d", errors="coerce")
print("Valid dates:", int(parsed.notna().sum()))
print("Invalid dates:", int(parsed.isna().sum()))
```

**실행 결과**

```text
Valid dates: 2
Invalid dates: 1
```

---

<a id="section-6-9"></a>
## 6.9. Cross-Field & Schema Validation — 관계와 규칙 검증

데이터 검증은 각 열의 자료형만 확인하는 과정이 아닙니다. **열 간의 관계도 함께 검사**해야 합니다. 예를 들어 매출을 계산할 때는 수량이 양수인지 확인한 뒤, 완료 상태 주문에만 매출 계산 규칙을 적용할 수 있습니다.

다음과 같은 규칙을 정의할 수 있습니다.

- 필수 열 존재 여부와 열 이름 확인
- `order_id`의 고유성
- 수량은 양의 정수, 단가는 허용 구간의 정수
- `status`가 허용된 상태 중 하나인지 확인
- 매출 집계는 `completed` 주문만 포함
- 날짜가 지정한 수집 기간 안에 있는지 확인

위 예제의 `cancelled` 주문은 데이터 자체가 유효하더라도 **완료 매출에서는 제외**됩니다. 이처럼 **정제 결과의 유효성**과 **집계 대상 여부**는 서로 다른 판단입니다.

**예제 코드 — [09_cross_field_validation.py](./examples/09_cross_field_validation.py)**

```python
import pandas as pd

orders = pd.DataFrame({
    "status": ["completed", "cancelled", "completed"],
    "quantity": [2, 1, 0],
    "unit_price": [1500, 2000, 5000],
})
valid_qty = orders["quantity"].gt(0)
revenue = orders.loc[valid_qty & orders["status"].eq("completed"), "quantity"] * orders["unit_price"]
print("Invalid quantity:", int((~valid_qty).sum()))
print("Completed revenue:", int(revenue.sum()))
```

**실행 결과**

```text
Invalid quantity: 1
Completed revenue: 3000
```

---

<a id="section-6-10"></a>
## 6.10. Validation Rules & Quality Report — 검증 결과 기록

정제 규칙은 코드에 흩어지게 작성하기보다 **스키마(Schema)와 명시적인 정책**으로 관리하는 것이 좋습니다. 필수 열 목록, 허용 값, 수치 범위, 품질 보고서 항목을 정하면 다른 사람이 결과를 재현하고 검토하기 쉬워집니다.

예제에서는 필수 열 `order_id`, `quantity`, `unit_price` 중 하나가 누락되어 스키마 검증에 실패합니다. **중요한 필수 열이 빠진 상태에서 임의로 처리하면 잘못된 결과가 나올 수 있으므로** 먼저 실패 원인을 알리는 것이 적절합니다.

데이터 품질 보고서에는 원본 행 수, 정상 처리 수, 제외 수, 별도 검토 수, 오류 사유별 개수를 기록하는 것을 추천합니다. 정상·제외·검토로 나눈다면 다음 관계가 성립해야 합니다.

\[
N_{raw}=N_{accepted}+N_{rejected}+N_{review}
\]

이를 검사하면 처리 과정에서 일부 행이 실수로 누락되거나 중복 계산되는 문제를 발견할 수 있습니다.

**예제 코드 — [10_schema_validation.py](./examples/10_schema_validation.py)**

```python
import pandas as pd

required = {"order_id", "quantity", "unit_price"}
frame = pd.DataFrame({"order_id": ["ORD-001"], "quantity": [2]})
missing = sorted(required - set(frame.columns))
print("Missing columns:", missing)
print("Schema valid:", not missing)
```

**실행 결과**

```text
Missing columns: ['unit_price']
Schema valid: False
```

---

<a id="section-6-11"></a>
## 6.11. Reproducible Cleaning & Audit Trail

같은 원본 데이터와 같은 정책으로 실행하면 결과도 같아야 합니다. **재현 가능성(Reproducibility)**은 입력, 규칙, 라이브러리 환경이 동일하다는 전제에서 결과를 다시 만들 수 있는 성질입니다.

데이터 처리 과정에서 다음 정보를 남기면 추적이 쉬워집니다.

| 기록 | 목적 |
|---|---|
| 원본 파일 | 최초 입력 보존 |
| 정책 파일 | 허용 범위와 검토 기준 확인 |
| 품질 요약 | 전체 데이터의 판정 분포 확인 |
| 감사 로그(Audit Log) | 원본 행별 판정과 사유 추적 |
| 결과 파일 | 정상 데이터와 검토·제외 데이터를 분리 |

**중요:** 감사 로그에 `source_line`을 포함하면 어떤 원본 CSV 행에서 문제가 있었는지 다시 확인할 수 있습니다. 다만 실제 개인정보가 포함된 데이터에서는 로그에 원본 값을 무제한 복사하지 않고 접근권한과 보존 기간을 관리해야 합니다.

**예제 코드 — [11_quality_report.py](./examples/11_quality_report.py)**

```python
import pandas as pd

records = pd.DataFrame({
    "decision": ["accepted", "rejected", "review", "accepted", "rejected"]
})
counts = records["decision"].value_counts()
for state in ("accepted", "rejected", "review"):
    print(f"{state}: {int(counts.get(state, 0))}")
print("Total:", len(records))
```

**실행 결과**

```text
accepted: 2
rejected: 2
review: 1
Total: 5
```

---

<a id="section-6-12"></a>
## 6.12. Idempotent Cleaning — 반복 실행 시 결과 일관성

멱등성(Idempotence)은 같은 처리를 다시 적용해도 결과가 바뀌지 않는 성질입니다. 문자열 정규화는 이를 쉽게 확인할 수 있는 예시입니다.

`normalize(normalize(data)) == normalize(data)`가 성립하면 같은 정규화 함수를 반복 호출해도 값이 누적 변경되지 않습니다.

**주의:** 처리 함수가 멱등성을 갖는 것과 전체 파일 파이프라인이 원자적으로 저장되는 것은 별개입니다. 본 Chapter의 Mini Project는 동일한 파일로 재실행 시 결과가 동일하도록 작성했지만, 중간 쓰기 실패 시 모든 출력 파일을 한꺼번에 교체하는 **원자적 저장**까지 구현하지는 않습니다.

**예제 코드 — [12_reproducible_cleaning.py](./examples/12_reproducible_cleaning.py)**

```python
import pandas as pd

source = pd.Series([" Seoul ", "BUSAN"], dtype="string")
def normalize_regions(values):
    return values.str.strip().str.casefold().map({"seoul": "Seoul", "busan": "Busan"})

once = normalize_regions(source)
twice = normalize_regions(once)
print("Original unchanged:", source.iloc[0] == " Seoul ")
print("Same after rerun:", once.equals(twice))
```

**실행 결과**

```text
Original unchanged: True
Same after rerun: True
```

---

<a id="section-6-13"></a>
## 6.13. Mini Project — Order Data Quality Pipeline

### 목표

원본 주문 CSV(`raw_orders.csv`)에 포함된 오류 데이터를 검사하고, **정상 처리·제외·검토** 상태로 구분합니다. 정제된 주문과 별도 검토 데이터를 파일로 저장한 뒤, 완료된 주문에 한해 지역별 매출을 계산합니다.

| 입력 파일 | 내용 |
|---|---|
| [`raw_orders.csv`](./data/raw_orders.csv) | 주문 31건과 의도적으로 포함한 오류·중복 |
| [`cleaning_policy.json`](./data/cleaning_policy.json) | 지역·상품군·상태·날짜·수량·가격 허용 규칙 |

**정제 기준**

1. `order_id`는 `ORD-`와 3자리 숫자, `customer_id`는 `C`와 3자리 숫자로 구성되어야 합니다.
2. 필수값 누락, 날짜 오류, 잘못된 지역·상품군·상태, 수량·단가 위반은 `rejected`로 분류합니다.
3. 같은 주문 ID의 두 번째 이후 행은 `rejected`로 분류합니다. 이는 학습용 명시적 정책이며, 실제 시스템의 수정 이력 정책과는 별개입니다.
4. 유효하지만 단가가 **500,000원을 초과**하는 주문은 `review`로 분류합니다. 자동 삭제하거나 완료 매출에 포함하지 않습니다.
5. 그 밖에 유효한 행은 `accepted`로 분류하고, 이 중 `completed` 주문만 매출에 포함합니다.
6. 판정 결과와 오류 사유는 원본 CSV의 행 번호와 함께 감사 로그에 남깁니다.

**주요 알고리즘**

```text
CSV + Policy JSON
    → 필수 열 검사
    → 공백·표기 표준화
    → 숫자·날짜 변환 및 도메인 규칙 확인
    → ID 중복 확인
    → rejected / review / accepted 분리
    → 감사 로그 및 품질 보고서 저장
    → 완료 주문의 지역별 매출 집계
```

### Type Annotation Evaluation — `from __future__ import annotations`

Chapter 02에서 다룬 타입 힌트는 `value: int`, `def f(...) -> str:`처럼 기대 자료형을 기록하는 표기입니다. `from __future__ import annotations`는 **타입 힌트를 평가하는 시점과 저장 방식**에 영향을 주는 선언입니다.

Python 3.13 이하에서는 일반적으로 함수의 타입 힌트를 정의할 때 평가합니다. 아직 정의되지 않은 클래스 이름을 타입 힌트로 사용하면 오류가 발생할 수 있습니다. 다음 예제에서는 이 선언을 사용해 자기 자신의 클래스를 반환 타입에 표현합니다.

```python
from __future__ import annotations

class Record:
    def next_record(self) -> Record | None:
        return None

print(Record().next_record())
```

**실행 결과**

```text
None
```

- **Python 3.13 이하:** 이 선언을 사용하면 타입 힌트를 문자열 형태로 저장하여 아직 정의 중인 이름을 타입 힌트에 사용할 수 있습니다.
- **Python 3.14 이상:** 기본 타입 힌트 평가 방식이 필요할 때 평가하는 방식으로 변경되었습니다. 다만 `from __future__ import annotations`를 명시한 파일에서는 기존의 **문자열화(Stringified Annotations)** 동작이 적용됩니다. 두 방식은 동일하지 않습니다.
- **선언 위치:** 파일의 맨 앞에 배치하되, 모듈 설명 문자열(Docstring), 주석, 다른 `__future__` 선언은 앞에 올 수 있습니다.

이 선언은 **데이터 검증이나 타입 강제를 수행하지 않습니다.** `pd.to_numeric()`과 `pd.to_datetime()` 등의 실제 검증·변환 로직과는 별개입니다. 아래 프로젝트에서는 타입 힌트의 평가 문제를 피하기 위해 사용했으며, 필요하지 않은 작은 함수에 관례적으로 추가할 필요는 없습니다.

**프로젝트 코드 — [13_order_quality_pipeline.py](./examples/13_order_quality_pipeline.py)**

아래 코드는 원본을 덮어쓰지 않고 `output/` 아래에 새 결과를 생성합니다.

```python
"""주문 데이터 품질 검사: 원본 보존 / 제외·검토 분리 / 결과 및 감사 로그 생성."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
COLUMNS = (
    "order_id", "order_date", "customer_id", "region", "category",
    "quantity", "unit_price", "status",
)


def load_policy(path: Path) -> dict:
    policy = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "allowed_regions", "allowed_categories", "allowed_statuses",
        "revenue_status", "max_quantity", "max_unit_price",
        "review_unit_price_over", "earliest_date", "latest_date",
    }
    missing = required - policy.keys()
    if missing:
        raise ValueError(f"Policy keys missing: {sorted(missing)}")
    for key in ("max_quantity", "max_unit_price", "review_unit_price_over"):
        if type(policy[key]) is not int or policy[key] <= 0:
            raise ValueError(f"Invalid positive integer policy: {key}")
    if policy["review_unit_price_over"] > policy["max_unit_price"]:
        raise ValueError("Review threshold exceeds maximum price")
    for key in ("allowed_regions", "allowed_categories", "allowed_statuses"):
        values = policy[key]
        if not isinstance(values, list) or not values or not all(isinstance(v, str) and v for v in values):
            raise ValueError(f"Invalid policy list: {key}")
        if len({v.casefold() for v in values}) != len(values):
            raise ValueError(f"Duplicate case-insensitive values: {key}")
    if policy["revenue_status"] not in policy["allowed_statuses"]:
        raise ValueError("Revenue status must be allowed")
    start = pd.Timestamp(policy["earliest_date"])
    end = pd.Timestamp(policy["latest_date"])
    if start > end:
        raise ValueError("Invalid policy date range")
    return policy


def _canonical(values: pd.Series, allowed: list[str]) -> pd.Series:
    lookup = {item.casefold(): item for item in allowed}
    return values.str.casefold().map(lookup).astype("string")


def clean_orders(source: pd.DataFrame, policy: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """accepted, rejected, review, audit 반환. source를 직접 수정하지 않음."""
    if tuple(source.columns) != COLUMNS:
        raise ValueError(f"Expected columns: {', '.join(COLUMNS)}")
    if not all(pd.api.types.is_string_dtype(dtype) for dtype in source.dtypes):
        raise ValueError("Read raw data with dtype='string' before cleaning")

    values = source.copy(deep=True)
    for name in COLUMNS:
        values[name] = values[name].str.strip().replace("", pd.NA)

    values["region"] = _canonical(values["region"], policy["allowed_regions"])
    values["category"] = _canonical(values["category"], policy["allowed_categories"])
    values["status"] = values["status"].str.casefold()

    numeric_qty = pd.to_numeric(values["quantity"], errors="coerce")
    numeric_price = pd.to_numeric(values["unit_price"], errors="coerce")
    parsed_dates = pd.to_datetime(values["order_date"], format="%Y-%m-%d", errors="coerce")
    date_shape = values["order_date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}").fillna(False)

    rules = {
        "INVALID_ORDER_ID": values["order_id"].str.fullmatch(r"ORD-\d{3}").fillna(False),
        "INVALID_CUSTOMER_ID": values["customer_id"].str.fullmatch(r"C\d{3}").fillna(False),
        "INVALID_DATE": (date_shape & parsed_dates.between(
            pd.Timestamp(policy["earliest_date"]), pd.Timestamp(policy["latest_date"])
        )).fillna(False),
        "INVALID_REGION": values["region"].notna(),
        "INVALID_CATEGORY": values["category"].notna(),
        "INVALID_QUANTITY": (
            numeric_qty.notna() & numeric_qty.ge(1) &
            numeric_qty.le(policy["max_quantity"]) & numeric_qty.mod(1).eq(0)
        ).fillna(False),
        "INVALID_UNIT_PRICE": (
            numeric_price.notna() & numeric_price.ge(1) &
            numeric_price.le(policy["max_unit_price"]) & numeric_price.mod(1).eq(0)
        ).fillna(False),
        "INVALID_STATUS": values["status"].isin(policy["allowed_statuses"]).fillna(False),
        "DUPLICATE_ORDER_ID": (~values["order_id"].duplicated(keep="first")).fillna(False),
    }

    decisions: list[str] = []
    issues: list[str] = []
    audit_rows: list[dict] = []
    for position in range(len(source)):
        failures = [code for code, passing in rules.items() if not bool(passing.iloc[position])]
        if failures:
            decision = "rejected"
        elif bool(numeric_price.iloc[position] > policy["review_unit_price_over"]):
            decision = "review"
            failures = ["HIGH_UNIT_PRICE"]
        else:
            decision = "accepted"
        decisions.append(decision)
        joined = ";".join(failures)
        issues.append(joined)
        audit_rows.append({
            "source_line": position + 2,
            "order_id": source.iloc[position]["order_id"],
            "decision": decision,
            "issues": joined,
        })

    accepted_positions = [i for i, value in enumerate(decisions) if value == "accepted"]
    rejected_positions = [i for i, value in enumerate(decisions) if value == "rejected"]
    review_positions = [i for i, value in enumerate(decisions) if value == "review"]

    accepted = values.iloc[accepted_positions].copy().reset_index(drop=True)
    accepted["order_date"] = parsed_dates.iloc[accepted_positions].dt.strftime("%Y-%m-%d").to_numpy()
    accepted["quantity"] = numeric_qty.iloc[accepted_positions].astype("int64").to_numpy()
    accepted["unit_price"] = numeric_price.iloc[accepted_positions].astype("int64").to_numpy()
    accepted["total_price"] = accepted["quantity"] * accepted["unit_price"]

    def quarantined(positions: list[int]) -> pd.DataFrame:
        result = source.iloc[positions].copy().reset_index(drop=True)
        result.insert(0, "source_line", [p + 2 for p in positions])
        result["issues"] = [issues[p] for p in positions]
        return result

    return accepted, quarantined(rejected_positions), quarantined(review_positions), pd.DataFrame(audit_rows)


def run_pipeline(source_path: Path, policy_path: Path, output_dir: Path) -> dict:
    policy = load_policy(policy_path)
    raw = pd.read_csv(source_path, dtype="string", keep_default_na=False, encoding="utf-8")
    accepted, rejected, review, audit = clean_orders(raw, policy)

    revenue = (
        accepted.loc[accepted["status"] == policy["revenue_status"]]
        .groupby("region", as_index=False)["total_price"]
        .sum()
        .rename(columns={"total_price": "revenue_krw"})
        .sort_values("region")
        .reset_index(drop=True)
    )
    issue_counts = Counter(
        issue for issue_list in audit["issues"]
        for issue in issue_list.split(";") if issue
    )
    report = {
        "source_records": int(len(raw)),
        "accepted_records": int(len(accepted)),
        "rejected_records": int(len(rejected)),
        "review_records": int(len(review)),
        "completed_orders": int(accepted["status"].eq(policy["revenue_status"]).sum()),
        "completed_revenue_krw": int(revenue["revenue_krw"].sum()),
        "issue_counts": dict(sorted(issue_counts.items())),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, frame in (
        ("cleaned_orders.csv", accepted),
        ("rejected_orders.csv", rejected),
        ("review_orders.csv", review),
        ("audit_log.csv", audit),
        ("revenue_by_region.csv", revenue),
    ):
        frame.to_csv(output_dir / name, index=False, encoding="utf-8-sig")
    (output_dir / "quality_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    summary = run_pipeline(
        ROOT / "data/raw_orders.csv",
        ROOT / "data/cleaning_policy.json",
        ROOT / "output",
    )
    for label in (
        "source_records", "accepted_records", "rejected_records",
        "review_records", "completed_orders", "completed_revenue_krw",
    ):
        print(f"{label}: {summary[label]}")
    print("Saved to: output/")
```

**실행 결과**

```text
source_records: 31
accepted_records: 22
rejected_records: 8
review_records: 1
completed_orders: 19
completed_revenue_krw: 202800
Saved to: output/
```

**생성된 결과**

| 파일 | 내용 |
|---|---|
| `cleaned_orders.csv` | 자동 검증에 통과한 주문 22건 |
| `rejected_orders.csv` | 유효성·중복 규칙에 위배되는 주문 8건 |
| `review_orders.csv` | 검토가 필요한 고가 주문 1건 |
| `audit_log.csv` | 31개 원본 행별 판정·오류 사유 |
| `revenue_by_region.csv` | 완료 주문의 지역별 매출 |
| `quality_report.json` | 전체 건수·판정별 건수·오류 종류별 개수·완료 매출 |

**지역별 매출 — 검증 통과 및 완료 주문 기준**

```text
Busan:   54,000원
Gwangju: 41,600원
Incheon: 17,500원
Seoul:   89,700원
------------------
Total:  202,800원
```

**판정 결과는 `22 + 8 + 1 = 31`건으로 원본 수와 일치합니다.** 오류 사유는 한 행에 여러 개가 함께 기록될 수 있습니다. 예를 들어 허용되지 않은 지역과 음수 수량이 모두 발견되면 두 오류를 모두 남깁니다. 따라서 `issue_counts`의 합계를 단순히 제외 행 수로 해석해서는 안 됩니다.

### 설계 확인

- 원본의 공백과 자료형을 보존하기 위해 `pd.read_csv(..., dtype="string", keep_default_na=False)` 사용
- 열 구성이 다르면 예외를 발생시켜 잘못된 분석을 조기에 중지
- `pd.to_numeric(..., errors="coerce")`, `pd.to_datetime(..., errors="coerce")` 후 범위 검증
- 검토 대상은 자동으로 승인되지 않으며 매출 집계에서 제외
- 원본 파일 불변, 결과 재실행 시 동일 출력 확인
- 저장 중 파일 시스템 장애에 대비한 **원자적 교체 기능은 포함하지 않음**

---

<a id="section-6-14"></a>
## 6.14. Coding Practice

각 문제는 `exercises/`의 미완성 함수에서 시작하며, `solutions/`의 정답 코드와 비교할 수 있습니다. **먼저 직접 구현하고**, 필요한 경우 제공된 자동 테스트로 결과를 확인합니다.

| 번호 | 문제 | 시작 코드 | 정답 코드 |
|:---:|---|---|---|
| 01 | Missing Value Profile | [Exercise](./exercises/01_missing_profile.py) | [Solution](./solutions/01_missing_profile.py) |
| 02 | Duplicate Order IDs | [Exercise](./exercises/02_deduplicate_orders.py) | [Solution](./solutions/02_deduplicate_orders.py) |
| 03 | Positive Integer Validation | [Exercise](./exercises/03_validate_quantities.py) | [Solution](./solutions/03_validate_quantities.py) |
| 04 | Region Normalization | [Exercise](./exercises/04_normalize_regions.py) | [Solution](./solutions/04_normalize_regions.py) |
| 05 | Sensor Data Validation | [Exercise](./exercises/05_validate_sensor.py) | [Solution](./solutions/05_validate_sensor.py) |

### Exercise 01 — Missing Value Profile

문자열 열의 빈 문자열과 공백 문자열도 결측으로 판단하여 각 열의 결측 수를 반환하는 `missing_counts(frame)`을 구현합니다.

- 원본 `frame`을 수정하지 않음
- `None`, `NaN`, 빈 문자열과 공백 문자열을 결측으로 집계
- 컬럼 이름을 인덱스로 하는 `pd.Series` 반환

**기대 결과:** `name=["Kim", "  ", None]`, `score=[80, 90, None]` → `name=2`, `score=1`

### Exercise 02 — Duplicate Order IDs

주문 ID가 중복된 DataFrame에서 첫 기록만 남긴 새 DataFrame을 반환합니다.

- `order_id`를 중복 판단 기준으로 사용
- 원본 순서 유지 및 인덱스 재설정
- 원본 변경 금지

**기대 결과:** `A(수량1), B(수량2), A(수량3)` → `A(수량1), B(수량2)`

### Exercise 03 — Positive Integer Validation

문자열로 제공된 수량을 검사하여 **1~100 사이의 정수**인지 Boolean Mask를 반환합니다.

- 숫자로 변환 불가, 결측, 소수, 0, 음수, 범위 초과는 `False`
- `"1"`, `"100"`은 `True`, `"2.5"`, `"unknown"`은 `False`

### Exercise 04 — Region Normalization

`Seoul`, `Busan`, `Gwangju`를 허용 지역으로 정하고, 지역 문자열을 표준화합니다.

- 앞뒤 공백과 대소문자 차이 처리
- 허용되지 않은 지역은 결측으로 표시
- 결과를 `Series`로 반환

**기대 결과:** `" seoul ", "BUSAN", "unknown"` → `"Seoul", "Busan", <NA>`

### Exercise 05 — Sensor Data Validation

날짜와 온도 측정값을 검사하는 `valid_sensor_rows(frame)`을 구현합니다.

- 날짜는 `YYYY-MM-DD` 형식이며 실제 존재하는 날짜여야 함
- 온도는 **−40°C 이상 85°C 이하**의 유한한 숫자만 허용
- 결과의 `date`는 Pandas 날짜 자료형, `temperature_c`는 `float`
- 비정상 행을 제거하고 인덱스를 재설정

**실행 및 검증** — `Chapter-06/` 기준

```bash
python solutions/01_missing_profile.py
python solutions/05_validate_sensor.py
python -m unittest discover -s tests -v
```

제공된 테스트는 `solutions/`의 모범답안과 Mini Project를 대상으로 합니다. 직접 작성한 `exercises/` 코드는 테스트의 import 경로를 변경하거나 별도 코드를 작성하여 검증할 수 있습니다.

---

<a id="section-6-15"></a>
## 6.15. Quiz & Summary

### Quiz

각 문제의 정답과 해설은 독립적으로 확인할 수 있습니다.

**Q1. 데이터의 유효성(Validity)과 정확성(Accuracy)은 어떻게 다른가요?**

<details>
<summary>정답 및 해설 확인</summary>

유효성은 정해진 형식·범위를 만족하는지를, 정확성은 실제 사실과 일치하는지를 의미합니다. 형식에 맞는 가격도 실제 거래 금액과 다르면 정확하지 않습니다.

</details>

**Q2. `keep_default_na=False`로 불러온 빈 문자열을 왜 별도로 검사해야 하나요?**

<details>
<summary>정답 및 해설 확인</summary>

`""`와 공백 문자열은 결측값으로 자동 인식되지 않을 수 있기 때문입니다. 공백을 제거하고 `pd.NA` 등으로 변경한 뒤 `isna()`를 사용합니다.

</details>

**Q3. 모든 결측값을 0으로 채우면 안 되는 이유는 무엇인가요?**

<details>
<summary>정답 및 해설 확인</summary>

0이 실제 의미 있는 측정값일 수 있기 때문입니다. 결측과 0을 혼동하면 평균·합계·분포가 왜곡될 수 있으므로 데이터 의미에 따라 처리합니다.

</details>

**Q4. `df.duplicated()`와 `df.duplicated(subset=["order_id"])`의 차이는 무엇인가요?**

<details>
<summary>정답 및 해설 확인</summary>

전자는 행 전체가 같은지, 후자는 주문 ID만 같은지 검사합니다. 다른 열이 달라도 동일한 ID는 중복으로 판단될 수 있습니다.

</details>

**Q5. `pd.to_numeric(..., errors="coerce")`가 `"unknown"`을 변환하면 어떻게 되나요?**

<details>
<summary>정답 및 해설 확인</summary>

변환할 수 없는 값은 결측값으로 표시됩니다. 원본이 정상 수치로 바뀌는 것은 아니므로 해당 행의 오류 원인을 별도로 기록해야 합니다.

</details>

**Q6. 결측값을 포함한 정수 열을 다룰 때 Pandas의 `Int64` 자료형이 유용한 이유는 무엇인가요?**

<details>
<summary>정답 및 해설 확인</summary>

`Int64`는 결측값(`pd.NA`)을 허용하는 Nullable Integer 자료형입니다. 파이썬·NumPy의 일반 정수형과 구분해야 합니다.

</details>

**Q7. `" seoul "`과 `"SEOUL"`을 같은 지역으로 처리하려면 어떤 단계가 필요한가요?**

<details>
<summary>정답 및 해설 확인</summary>

공백을 제거하고 대소문자를 통일한 뒤, 미리 정의한 지역 사전으로 정규화합니다. 사전에 없는 지역은 근거 없이 자동 교정하지 않습니다.

</details>

**Q8. IQR 방법으로 이상치를 탐색할 때 기준 범위는 어떻게 계산하나요?**

<details>
<summary>정답 및 해설 확인</summary>

`IQR = Q3 − Q1`, 하한은 `Q1 − 1.5 × IQR`, 상한은 `Q3 + 1.5 × IQR`입니다. 범위 밖의 값은 우선 검토 대상으로 판단합니다.

</details>

**Q9. `pd.to_datetime`의 `errors="coerce"` 옵션은 존재하지 않는 날짜를 어떻게 처리하나요?**

<details>
<summary>정답 및 해설 확인</summary>

파싱할 수 없는 날짜를 `NaT`로 표시합니다. 이후 `isna()`나 날짜 범위 검사를 통해 오류를 검출합니다.

</details>

**Q10. Mini Project에서 단가 9,999,999원인 주문을 바로 삭제하지 않은 이유는 무엇인가요?**

<details>
<summary>정답 및 해설 확인</summary>

정책상 허용 상한 내의 값이지만 단가 검토 임계값을 초과하기 때문입니다. 오류로 단정하지 않고 `review`로 분리해 확인 전 매출 집계에서 제외했습니다.

</details>

**Q11. 원본 31건 중 정상 22건, 제외 8건, 검토 1건으로 분류했습니다. 이때 확인할 수 있는 검증 불변식은 무엇인가요?**

<details>
<summary>정답 및 해설 확인</summary>

`원본 건수 = 정상 + 제외 + 검토`이며, `31 = 22 + 8 + 1`이 성립합니다. 각 원본 행이 하나의 판정 상태를 가져야 합니다.

</details>

**Q12. 정제된 데이터에 `cancelled`나 `pending` 주문이 남아 있는데도 매출 집계에는 왜 포함하지 않나요?**

<details>
<summary>정답 및 해설 확인</summary>

데이터의 유효성과 집계 대상 여부는 다릅니다. 이 프로젝트에서는 `completed` 상태의 정상 주문만 매출 계산에 포함하도록 명시했습니다.

</details>

**Q13. `from __future__ import annotations`를 추가하면 Pandas 데이터의 자료형 오류가 자동으로 검증되나요?**

<details>
<summary>정답 및 해설 확인</summary>

아닙니다. 이 선언은 타입 힌트의 평가·저장 방식에 영향을 줄 뿐, 입력 데이터의 자료형이나 값의 유효성을 검사하지 않습니다. 데이터 검증은 별도 코드로 수행해야 합니다.

</details>

### Summary

- **Data Quality:** 정확성, 완전성, 유효성, 일관성, 고유성, 적시성을 구분합니다.
- **Missing Values:** `isna()`로 탐색하고, 빈 문자열을 별도 처리합니다.
- **Missing Strategies:** 삭제·대체·보존을 데이터 의미에 따라 선택합니다.
- **Duplicates:** 전체 행 중복과 비즈니스 키 중복을 구분합니다.
- **Type Conversion:** `to_numeric`, `to_datetime` 후 형식과 범위를 검증합니다.
- **Future Annotations:** `from __future__ import annotations`는 타입 힌트 평가 방식을 조정하며 실제 값의 유효성 검사는 수행하지 않습니다.
- **String Cleaning:** 공백·대소문자·허용 값의 표준화를 수행합니다.
- **Outlier Detection:** 통계적 이상치는 자동 삭제보다 검토 근거로 활용합니다.
- **Validation:** 열별 규칙과 열 간 관계를 함께 검사합니다.
- **Audit Trail:** 원본 행 번호와 판정·오류 사유를 남깁니다.
- **Reproducibility:** 원본·정책·환경을 명시하고 재실행 결과를 검증합니다.
- **Output Separation:** 정상, 제외, 검토 데이터를 구분하여 저장합니다.

### References

- [Python — `__future__`](https://docs.python.org/3/library/__future__.html)
- [Python — Annotation Semantics](https://docs.python.org/3/library/annotationlib.html#annotation-semantics)

- [Python Documentation](https://docs.python.org/3/)
- [Pandas — Working with Missing Data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [Pandas — Duplicate Labels](https://pandas.pydata.org/docs/user_guide/duplicates.html)
- [Pandas — `DataFrame.duplicated`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html)
- [Pandas — `DataFrame.drop_duplicates`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html)
- [Pandas — `to_numeric`](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html)
- [Pandas — `to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)
- [Pandas — Working with Text Data](https://pandas.pydata.org/docs/user_guide/text.html)
- [NumPy — Quantiles](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html)

---

[← Data Processing 목차](../README.md) · [Chapter 05 — File I/O & Data Formats](../Chapter-05/)
