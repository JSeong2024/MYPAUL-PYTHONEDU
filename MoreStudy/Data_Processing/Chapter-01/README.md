# Chapter 01. Introduction to Data Processing

데이터 처리(Data Processing)의 목적과 전체 흐름을 이해하고, Python으로 작은 데이터셋의 구조를 확인하고 기본적인 검증·집계를 수행하는 방법을 학습합니다. 원본 데이터와 처리 결과를 구분하고, 데이터 품질을 확인하는 첫 번째 절차를 구현합니다.

본 Chapter는 **Python 3.13 이상** 환경을 권장하며, 예제는 Python 표준 라이브러리만 사용합니다. NumPy와 Pandas는 이후 Chapter에서 다룹니다.

**선행 학습:** 변수, 리스트, 딕셔너리, 조건문, 반복문, 함수의 기본 사용법

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [1.1](#section-1-1) | Data Processing의 개념과 목적 |
| [1.2](#section-1-2) | 데이터 유형과 표현 방식 |
| [1.3](#section-1-3) | Data Processing Workflow |
| [1.4](#section-1-4) | Python 개발 환경과 실행 방법 |
| [1.5](#section-1-5) | Record, Field, Schema와 Metadata |
| [1.6](#section-1-6) | Basic Data Inspection — 데이터 구조 확인 |
| [1.7](#section-1-7) | Data Quality — 기본 검증 |
| [1.8](#section-1-8) | First Data Processing — 기본 집계 |
| [1.9](#section-1-9) | Mini Project — Weekly Order Report |
| [1.10](#section-1-10) | Coding Practice |
| [1.11](#section-1-11) | Quiz & Summary |

---

<a id="section-1-1"></a>
## 1.1. Data Processing의 개념과 목적

데이터 처리(Data Processing)는 **원본 데이터(Raw Data)를 목적에 맞게 확인하고, 검증하고, 변환하여 활용 가능한 형태로 만드는 과정**입니다. 데이터를 파일로 읽는 행위 자체뿐 아니라, 잘못된 값을 구분하고 필요한 지표를 계산하여 결과를 전달하는 작업도 포함됩니다.

예를 들어 여러 상점에서 수집한 주문 기록을 그대로 합치면 주문 번호가 중복되거나 수량이 비어 있을 수 있습니다. 데이터를 신뢰할 수 있는 기준에 맞춰 정리한 뒤 매출을 계산해야 의미 있는 결과를 얻을 수 있습니다.

| 용어 | 의미 | 예시 |
|---|---|---|
| Raw Data | 가공 전 수집한 데이터 | 주문 내역 CSV 원본 |
| Validation | 정해진 조건을 만족하는지 검사 | 수량이 양의 정수인지 확인 |
| Cleaning | 불완전하거나 잘못된 값 정리 | 빈 값 처리, 중복 확인 |
| Transformation | 표현 또는 구조 변경 | 수량·단가를 숫자로 변환 |
| Aggregation | 여러 값을 기준별로 집계 | 상품 분류별 매출 합계 |
| Output | 처리 결과 | 집계 표, 보고서, 저장 파일 |

**데이터 처리와 데이터 분석의 차이:** 데이터 처리는 데이터를 사용할 수 있도록 준비하는 데 초점을 둡니다. 분석은 준비된 데이터를 바탕으로 비교, 추세, 관계 등의 질문에 답하는 활동입니다. 두 작업은 서로 겹칠 수 있습니다.

**데이터 시각화와의 연결:** 이 과정에서 만들어진 집계 데이터를 그래프나 대시보드에 표현하는 방법은 [Data Visualization](../../Data_Visualization/)에서 다룹니다.

---

<a id="section-1-2"></a>
## 1.2. 데이터 유형과 표현 방식

데이터는 구조에 따라 다음과 같이 나눌 수 있습니다.

| 구분 | 특징 | 예시 |
|---|---|---|
| 정형 데이터(Structured) | 열과 행, 자료형 등 구조가 비교적 명확 | 관계형 데이터베이스 테이블, 정형 CSV |
| 반정형 데이터(Semi-structured) | 필드·태그가 있으나 레코드 구조가 유동적일 수 있음 | JSON, XML, 로그 이벤트 |
| 비정형 데이터(Unstructured) | 일정한 열·행 구조로 직접 표현하기 어려움 | 이미지, 오디오, 자유 형식 문서 |

**저장 형식과 데이터 의미는 다릅니다.** 예를 들어 `"2026-11-01"`은 Python에서 문자열(`str`)이지만, 데이터의 의미는 날짜입니다. `"S-001"`도 문자열이지만 연산할 숫자가 아니라 학생을 구분하는 식별자입니다.

| 데이터 의미 | 예시 | 처리할 때 고려할 점 |
|---|---|---|
| 수치형(Numerical) | 온도 23.5, 판매 수량 12 | 단위, 허용 범위 |
| 범주형(Categorical) | 지역, 제품 분류 | 값의 종류와 표기 통일 |
| 날짜·시간(Temporal) | `2026-11-01` | 문자열 형식, 시간대 |
| 식별자(Identifier) | `S-001`, `0012` | 앞자리 0이나 기호를 보존 |
| 텍스트(Text) | 고객 의견, 리뷰 | 인코딩, 공백, 언어 |

**예제 코드 — [01_data_types.py](./examples/01_data_types.py)**

```python
# 데이터의 의미(수량, 분류, 날짜)와 Python 자료형을 구분합니다.
records = [
    {"student_id": "S-001", "subject": "Python", "score": 92},
    {"student_id": "S-002", "subject": "Python", "score": 85},
]

print("기록 수:", len(records))
print("첫 번째 기록:", records[0])
print("점수 자료형:", type(records[0]["score"]).__name__)
print("학생 번호 자료형:", type(records[0]["student_id"]).__name__)
```

**실행 결과**

```text
기록 수: 2
첫 번째 기록: {'student_id': 'S-001', 'subject': 'Python', 'score': 92}
점수 자료형: int
학생 번호 자료형: str
```

`type()`은 Python 객체의 자료형을 알려 주지만 데이터가 지닌 **의미·단위·유효 범위**를 자동으로 알려 주지는 않습니다. 이러한 설명은 데이터 명세에 별도로 기록해야 합니다.

---

<a id="section-1-3"></a>
## 1.3. Data Processing Workflow

하나의 데이터 처리 작업은 다음과 같이 연결됩니다.

```text
원본 데이터 확인 (Raw Data)
        ↓
불러오기 (Loading)
        ↓
구조 및 품질 확인 (Inspection & Validation)
        ↓
정제 (Cleaning)
        ↓
변환 (Transformation)
        ↓
집계 (Aggregation)
        ↓
결과 저장·전달 (Export & Reporting)
```

각 단계의 역할을 분리하면 문제가 발생한 위치를 확인하기 쉽습니다. 모든 데이터셋에 반드시 모든 단계가 필요한 것은 아니며, 검사와 변환을 반복해야 할 수도 있습니다.

| 단계 | 질문 | 산출물 |
|---|---|---|
| Loading | 어떤 파일·시스템에서 가져왔는가? | 읽어 들인 데이터 |
| Inspection | 행 수와 필드는 예상과 같은가? | 구조 요약 |
| Validation | 필수값과 허용 범위를 만족하는가? | 오류 목록, 유효 기록 |
| Cleaning | 누락값·중복·형식을 어떻게 다룰 것인가? | 정제 데이터 |
| Transformation | 계산에 사용할 자료형과 구조인가? | 변환 데이터 |
| Aggregation | 어떤 기준으로 묶고 계산할 것인가? | 요약 지표 |
| Reporting | 어떤 결과를 어떻게 전달할 것인가? | 표, 파일, 처리 요약 |

**예제 코드 — [03_workflow_preview.py](./examples/03_workflow_preview.py)**

```python
# 원본 데이터는 별도로 유지하고, 검증된 값을 새 목록에 담습니다.
raw_readings = ["23.5", " 25.0 ", "", "error", "22.0"]
valid_readings = []
invalid_count = 0

for item in raw_readings:
    text = item.strip()
    try:
        if not text:
            raise ValueError("빈 값")
        valid_readings.append(float(text))
    except ValueError:
        invalid_count += 1

print("원본:", raw_readings)
print("처리 후:", valid_readings)
print("제외된 값:", invalid_count)
```

**실행 결과**

```text
원본: ['23.5', ' 25.0 ', '', 'error', '22.0']
처리 후: [23.5, 25.0, 22.0]
제외된 값: 2
```

이 예제에서는 문자열을 숫자로 바꿀 수 없는 값을 제외하고, 원본 목록은 그대로 둡니다. 실제 데이터에서는 잘못된 값을 **삭제할지, 수정할지, 별도로 기록할지**에 대한 기준을 먼저 정해야 합니다. 단순 변환 실패를 무조건 삭제하는 방식이 정답은 아닙니다.

---

<a id="section-1-4"></a>
## 1.4. Python 개발 환경과 실행 방법

**권장 환경**

- Python 3.13 이상 (**권장**)
- VS Code, 터미널 또는 Jupyter Notebook 중 선택
- Windows, macOS, Linux 사용 가능
- 이 Chapter의 예제는 별도 패키지 설치 불필요

**버전 확인**

```bash
python --version
```

Windows에서 `python` 명령을 사용할 수 없으면 `py --version`, macOS·Linux에서는 `python3 --version`을 확인할 수 있습니다.

**실행 방법 — `Chapter-01/`을 현재 작업 디렉터리로 사용**

```bash
cd MoreStudy/Data_Processing/Chapter-01
python examples/01_data_types.py
python examples/07_weekly_order_report.py
```

이미 저장소 안에 있다면 현재 위치에 따라 `cd` 경로를 조정합니다. Git Bash에서는 `python` 명령이 연결되지 않은 경우 `py -3`을 사용할 수도 있습니다.

데이터 파일을 다루는 예제는 스크립트 파일의 위치를 기준으로 경로를 구성하므로, 터미널 실행 위치가 달라도 동일한 파일을 읽도록 작성했습니다.

**폴더 구성**

```text
Chapter-01/
├── README.md
├── data/
│   ├── DATA_DICTIONARY.md
│   └── weekly_orders.csv
├── examples/
│   ├── 01_data_types.py
│   ├── 02_record_schema.py
│   ├── 03_workflow_preview.py
│   ├── 04_basic_inspection.py
│   ├── 05_quality_checks.py
│   ├── 06_first_processing.py
│   └── 07_weekly_order_report.py
├── exercises/
│   ├── 01_score_summary.py
│   ├── 02_reading_validation.py
│   └── 03_category_sales.py
└── solutions/
    ├── 01_score_summary.py
    ├── 02_reading_validation.py
    └── 03_category_sales.py
```

---

<a id="section-1-5"></a>
## 1.5. Record, Field, Schema와 Metadata

표 형태의 데이터에서는 **행(Row)**을 하나의 기록(Record)으로 보고, **열(Column)**을 해당 기록의 필드(Field)로 볼 수 있습니다.

| 용어 | 의미 | 예시 |
|---|---|---|
| Record | 하나의 관측·거래 등 데이터 단위 | 관측소 ST-01의 11월 1일 기록 |
| Field | 레코드의 항목 | `temperature_c` |
| Schema | 필드 이름, 자료형, 필수 여부 등 구조 규칙 | 온도는 실수, 관측소 ID는 필수 |
| Metadata | 데이터의 내용·출처·단위 등을 설명하는 정보 | 수집일, 원자료 출처, 측정 단위 |

**예제 코드 — [02_record_schema.py](./examples/02_record_schema.py)**

```python
# 한 행(Record)이 어떤 필드로 구성되는지 확인합니다.
record = {"station_id": "ST-01", "temperature_c": 23.5, "measured_at": "2026-11-01"}

print("필드:", ", ".join(record.keys()))
print("관측소:", record["station_id"])
print("기온:", record["temperature_c"], "°C")
print("날짜:", record["measured_at"])
```

**실행 결과**

```text
필드: station_id, temperature_c, measured_at
관측소: ST-01
기온: 23.5 °C
날짜: 2026-11-01
```

`measured_at`은 아직 문자열입니다. 실제 날짜 처리와 시간대 해석은 Chapter 06에서 자세히 다룹니다. 데이터의 의미를 잃지 않도록 필드 이름에 단위를 표현하는 습관도 유용합니다(`temperature_c`, `unit_price` 등).

---

<a id="section-1-6"></a>
## 1.6. Basic Data Inspection — 데이터 구조 확인

처리 전에 최소한 **행 개수, 필드 이름, 일부 샘플, 자료형, 누락값**을 살펴보는 것이 좋습니다. 작은 목록에서는 `len()`, `type()`, `keys()` 등을 사용할 수 있습니다.

**예제 코드 — [04_basic_inspection.py](./examples/04_basic_inspection.py)**

```python
# 데이터 개수, 필드, 상위 기록, 비어 있는 값을 점검합니다.
records = [
    {"id": "A-01", "region": "서울", "value": 18},
    {"id": "A-02", "region": "광주", "value": None},
    {"id": "A-03", "region": "부산", "value": 25},
]

print("전체 행:", len(records))
print("필드:", ", ".join(records[0].keys()))
print("첫 행:", records[0])
missing = sum(row["value"] is None for row in records)
print("값 누락:", missing)
```

**실행 결과**

```text
전체 행: 3
필드: id, region, value
첫 행: {'id': 'A-01', 'region': '서울', 'value': 18}
값 누락: 1
```

- `len(records)`: 레코드 개수
- `records[0].keys()`: 첫 번째 레코드의 필드 이름
- `None`: Python에서 값이 없음을 표현하는 객체
- `sum(조건식 for ...)`: 조건을 만족하는 항목의 개수 계산 (`True`를 1로 합산)

**주의:** 이 코드는 모든 레코드에 `value` 필드가 존재하고 목록이 비어 있지 않다는 전제로 작성했습니다. 외부에서 받은 데이터는 이러한 가정이 성립하는지 먼저 확인해야 합니다. 필드가 없는 경우에는 `row.get("value")` 등을 고려할 수 있습니다.

---

<a id="section-1-7"></a>
## 1.7. Data Quality — 기본 검증

데이터를 신뢰할 수 있으려면 어떤 값이 **유효한 값(Valid Value)**인지 정의해야 합니다. 기본적으로 다음을 점검합니다.

| 항목 | 질문 | 예시 규칙 |
|---|---|---|
| Completeness (완전성) | 필요한 값이 존재하는가? | 주문 번호 필수 |
| Validity (유효성) | 값이 범위·형식을 만족하는가? | 점수 0~100 |
| Uniqueness (고유성) | 중복되면 안 되는 값이 있는가? | 학생 번호 중복 금지 |
| Consistency (일관성) | 동일 의미의 값이 같은 형식인가? | `Seoul` / `서울` 표기 정리 |
| Accuracy (정확성) | 실제 현상을 올바르게 반영하는가? | 센서 교정값·원본 자료와 비교 |

형식이 올바르다고 해서 실제 값이 정확하다는 뜻은 아닙니다. 예를 들어 29°C는 허용 범위 안에 있지만 실제로 측정한 값인지 확인하려면 별도의 근거가 필요합니다.

**예제 코드 — [05_quality_checks.py](./examples/05_quality_checks.py)**

```python
# 기본 유효성 규칙: 점수는 0~100, 학생 번호는 고유값입니다.
records = [
    {"student_id": "S-01", "score": 90},
    {"student_id": "S-02", "score": 110},
    {"student_id": "S-01", "score": 80},
    {"student_id": "S-03", "score": None},
]
seen = set()
valid = []
reasons = []

for record in records:
    student_id = record["student_id"]
    score = record["score"]
    if student_id in seen:
        reasons.append("중복 학생 번호")
    elif not isinstance(score, (int, float)) or isinstance(score, bool):
        reasons.append("점수 누락 또는 자료형 오류")
    elif not 0 <= score <= 100:
        reasons.append("점수 범위 초과")
    else:
        seen.add(student_id)
        valid.append(record)

print("유효 기록:", len(valid))
print("제외 기록:", len(reasons))
print("사유:", ", ".join(reasons))
```

**실행 결과**

```text
유효 기록: 1
제외 기록: 3
사유: 점수 범위 초과, 중복 학생 번호, 점수 누락 또는 자료형 오류
```

이 예제는 점수의 범위를 검사하고 유효한 학생 번호만 `seen`에 기록합니다. `110`은 범위를 초과하고, 동일 학생 번호가 다시 등장한 레코드는 중복으로 분류하며, `None`은 점수 누락으로 분류합니다. 검증 규칙에 따라 결과가 달라지므로 **제외 사유를 보관**하는 것이 좋습니다.

---

<a id="section-1-8"></a>
## 1.8. First Data Processing — 기본 집계

검증된 데이터에 대해서는 합계, 평균, 개수와 같은 기초 통계를 계산할 수 있습니다. 다음 예제는 상품 분류(Category)별 매출을 합산합니다.

$$
\text{주문 매출} = \text{수량} \times \text{단가}
$$

$$
\text{총매출} = \sum_{i=1}^{n} \text{주문 매출}_i
$$

**예제 코드 — [06_first_processing.py](./examples/06_first_processing.py)**

```python
# 상품별 매출 계산: 수량 × 단가 (원)
orders = [
    {"category": "음료", "quantity": 2, "unit_price": 1800},
    {"category": "문구", "quantity": 3, "unit_price": 1200},
    {"category": "음료", "quantity": 1, "unit_price": 2500},
]

revenue_by_category = {}
for order in orders:
    category = order["category"]
    amount = order["quantity"] * order["unit_price"]
    revenue_by_category[category] = revenue_by_category.get(category, 0) + amount

print("전체 주문:", len(orders), "건")
print("전체 매출:", sum(revenue_by_category.values()), "원")
for category in sorted(revenue_by_category):
    print(f"{category}: {revenue_by_category[category]}원")
```

**실행 결과**

```text
전체 주문: 3 건
전체 매출: 9700 원
문구: 3600원
음료: 6100원
```

- `revenue_by_category`: 분류 이름을 Key, 누적 매출액을 Value로 보관하는 딕셔너리
- `dict.get(category, 0)`: 아직 집계되지 않은 분류의 시작값을 0으로 처리
- `sorted(...)`: 출력 순서를 일정하게 유지

이 예제는 데이터가 이미 올바른 숫자로 준비되었다고 가정합니다. 파일에서 받은 값은 문자열일 수 있으므로, 실제 처리에서는 **검증 및 형변환을 먼저 수행**해야 합니다.

---

<a id="section-1-9"></a>
## 1.9. Mini Project — Weekly Order Report

Chapter 01에서 배운 내용을 이용해 CSV로 제공되는 주문 기록을 점검하고 분류별 매출을 계산합니다. CSV의 입출력과 복잡한 파일 처리 자체는 Chapter 05에서 자세히 학습하므로, 여기서는 `csv.DictReader`의 기본 사용만 소개합니다.

**입력 데이터:** [weekly_orders.csv](./data/weekly_orders.csv) · [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)

| 항목 | 처리 규칙 |
|---|---|
| `order_id` | 비어 있지 않고, 유효한 기록에서 중복되지 않음 |
| `category` | 비어 있지 않은 분류명 |
| `quantity` | 1 이상의 정수 |
| `unit_price` | 0 이상의 정수, 원화 기준 |
| 집계 기준 | 분류별 `quantity × unit_price` 합계 |
| 오류 보고 | 제외된 기록 수와 제외 사유 출력 |

입력 CSV에는 의도적으로 4건의 잘못된 값이 포함되어 있습니다. **원본은 수정하지 않고** 유효한 데이터만 계산에 사용합니다. 수량·단가는 정수로 표현하며, 이 예제에서는 할인이나 세금을 고려하지 않습니다.

**예제 코드 — [07_weekly_order_report.py](./examples/07_weekly_order_report.py)**

```python
"""Chapter 01 Mini Project: 주간 주문 데이터 검증 및 매출 요약."""

import csv
from collections import Counter
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "weekly_orders.csv"


def validate_order(row: dict[str, str], seen_ids: set[str]) -> tuple[dict | None, str | None]:
    order_id = (row.get("order_id") or "").strip()
    category = (row.get("category") or "").strip()
    if not order_id or not category:
        return None, "필수값 누락"
    if order_id in seen_ids:
        return None, "주문 번호 중복"

    try:
        quantity = int((row.get("quantity") or "").strip())
        unit_price = int((row.get("unit_price") or "").strip())
    except ValueError:
        return None, "수량/단가 변환 실패"

    if quantity < 1 or unit_price < 0:
        return None, "허용 범위 초과"

    seen_ids.add(order_id)
    return {"order_id": order_id, "category": category,
            "quantity": quantity, "unit_price": unit_price}, None


def main() -> None:
    seen_ids: set[str] = set()
    revenue_by_category: dict[str, int] = {}
    errors: Counter[str] = Counter()
    rows = 0
    valid_rows = 0

    with DATA_PATH.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        expected = {"order_id", "category", "quantity", "unit_price"}
        if reader.fieldnames is None or set(reader.fieldnames) != expected:
            raise ValueError("CSV 헤더가 데이터 명세와 다릅니다.")

        for row in reader:
            rows += 1
            order, reason = validate_order(row, seen_ids)
            if reason is not None:
                errors[reason] += 1
                continue

            valid_rows += 1
            category = order["category"]
            amount = order["quantity"] * order["unit_price"]
            revenue_by_category[category] = revenue_by_category.get(category, 0) + amount

    print("주간 주문 처리 결과")
    print(f"원본: {rows}건 | 유효: {valid_rows}건 | 제외: {sum(errors.values())}건")
    for category in sorted(revenue_by_category):
        print(f"{category}: {revenue_by_category[category]:,}원")
    print(f"총매출: {sum(revenue_by_category.values()):,}원")
    for reason in sorted(errors):
        print(f"제외 사유 - {reason}: {errors[reason]}건")


if __name__ == "__main__":
    main()
```

**실행 결과**

```text
주간 주문 처리 결과
원본: 12건 | 유효: 8건 | 제외: 4건
간식: 10,500원
문구: 15,600원
음료: 9,700원
총매출: 35,800원
제외 사유 - 수량/단가 변환 실패: 2건
제외 사유 - 주문 번호 중복: 1건
제외 사유 - 허용 범위 초과: 1건
```

**실행 명령**

```bash
python examples/07_weekly_order_report.py
```

**처리 흐름 설명**

1. `Path(__file__)`로 스크립트 위치를 기준으로 입력 CSV 경로를 구성합니다.
2. `csv.DictReader`로 첫 행을 필드 이름으로 읽습니다.
3. `validate_order()`에서 필수값·중복·숫자 변환·값의 범위를 확인합니다.
4. 유효한 주문의 금액만 분류별로 누적하고, 제외된 기록의 사유는 `Counter`로 계산합니다.
5. 전체 기록 수, 유효 기록 수, 제외 사유, 분류별 매출을 출력합니다.

`csv`는 숫자를 자동으로 정수로 바꾸지 않습니다. 정수 변환 실패는 `ValueError`로 처리하며, 이 데이터셋에서는 수량·단가에 소수값을 허용하지 않습니다. 실제 외부 CSV는 필드 수가 일정하지 않거나 인코딩이 다를 수도 있으며, 여기서는 **제공된 CSV 명세에 맞는 입문용 검증**을 다룹니다.

**확장 과제:** 특정 분류만 출력하는 기능, 주문 개수 기준 정렬, 제외 기록의 행 번호 출력, 결과를 CSV로 저장하는 기능을 추가해 보세요. (저장 기능은 Chapter 05에서 자세히 학습)

---

<a id="section-1-10"></a>
## 1.10. Coding Practice

`exercises/`의 TODO를 채운 뒤 직접 실행하고, `solutions/`의 정답 코드와 비교합니다. 연습문제는 별도 라이브러리 설치 없이 실행할 수 있습니다.

| 번호 | 실습 | 문제 파일 | 정답 코드 |
|:---:|---|---|---|
| 01 | Score Summary | [01_score_summary.py](./exercises/01_score_summary.py) | [01_score_summary.py](./solutions/01_score_summary.py) |
| 02 | Reading Validation | [02_reading_validation.py](./exercises/02_reading_validation.py) | [02_reading_validation.py](./solutions/02_reading_validation.py) |
| 03 | Category Sales | [03_category_sales.py](./exercises/03_category_sales.py) | [03_category_sales.py](./solutions/03_category_sales.py) |

### Exercise 01 — Score Summary

점수 목록 `[78, 92, 85, 100, 67]`의 인원, 최저·최고, 평균, 80점 이상 인원을 계산합니다.

**구현 조건**

- 평균은 소수 첫째 자리까지 출력합니다.
- 인원이 0명인 일반적인 입력에서는 평균 계산 전에 빈 목록을 검사해야 함을 생각해 봅니다.

**정답 실행 결과**

```text
인원: 5 명
최저: 67 점
최고: 100 점
평균: 84.4점
80점 이상: 3 명
```

### Exercise 02 — Reading Validation

문자열로 수집된 센서값 중 0~50 범위에 속하는 숫자만 골라 평균을 계산합니다.

**구현 조건**

- 빈 문자열과 `error`처럼 변환할 수 없는 값을 제외합니다.
- `-5`처럼 범위를 벗어난 값도 제외합니다.
- 유효값이 0개이면 평균을 계산하지 않습니다.

**정답 실행 결과**

```text
유효: 3 건
제외: 3 건
유효값 평균: 20.0
```

### Exercise 03 — Category Sales

주어진 주문 4건의 분류별 매출과 전체 매출을 계산합니다.

**구현 조건**

- 주문 매출은 수량 × 단가로 계산합니다.
- 출력 순서는 분류 이름의 오름차순입니다.

**정답 실행 결과**

```text
간식: 4000원
문구: 3000원
음료: 5500원
전체 매출: 12500 원
```

---

<a id="section-1-11"></a>
## 1.11. Quiz & Summary

### Quiz

1. 데이터 처리(Data Processing)는 파일을 저장하는 작업만을 의미하나요?
2. `"0012"`처럼 앞자리에 0이 포함된 식별자를 항상 정수로 바꾸면 어떤 문제가 발생하나요?
3. Python에서 `len(records)`와 `type(records[0])`가 각각 알려 주는 정보는 무엇인가요?
4. 원본에 `quantity = "abc"`가 있다면 곧바로 `int()`로 계산해도 되나요?
5. 누락값을 무조건 삭제하는 것이 바람직하지 않은 이유는 무엇인가요?
6. 분류별 매출 합계를 구할 때 주문 데이터에 무엇이 먼저 확인되어야 하나요?

<details>
<summary><strong>Quiz 정답 확인</strong></summary>

1. 아닙니다. 수집, 검증, 정제, 변환, 집계, 저장 등 데이터를 활용 가능하게 만드는 전체 과정을 포함합니다.
2. 선행 0이 사라져 원래 식별자와 달라질 수 있습니다.
3. `len()`은 기록의 개수, `type()`은 Python 객체의 자료형을 알려 줍니다.
4. 아닙니다. 정수 변환에 실패하므로 `ValueError` 등의 예외를 고려한 검증이 필요합니다.
5. 누락의 의미와 처리 기준에 따라 보정, 제외, 별도 표시 등이 필요할 수 있기 때문입니다.
6. 자료형 변환, 필수값·허용 범위, 중복 규칙과 금액 단위를 확인해야 합니다.

</details>

### Summary

- **Data Processing:** 원본 데이터를 검증·변환·집계하여 활용 가능한 결과를 만드는 과정
- **데이터 유형:** 정형·반정형·비정형 데이터와 수치·범주·시간·식별자 의미를 구분
- **Record & Schema:** 데이터 한 건의 구조와 필드별 규칙 이해
- **Inspection:** 행 개수, 필드, 샘플, 누락 여부 확인
- **Validation:** 필수값, 범위, 자료형, 중복 조건 검사
- **Aggregation:** 목적에 맞는 그룹별 합계·평균 계산
- **Reproducibility:** 동일한 원본과 처리 규칙으로 동일한 결과를 얻을 수 있도록 입력과 기준 유지

다음 Chapter에서는 리스트, 튜플, 딕셔너리, 집합을 활용하여 데이터를 구조화하고 처리하는 방법을 자세히 학습합니다.

## References

- [Python — The Python Tutorial](https://docs.python.org/3/tutorial/)
- [Python — Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python — `csv` Module](https://docs.python.org/3/library/csv.html)
- [Python — `pathlib` Module](https://docs.python.org/3/library/pathlib.html)
- [Python — `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)
- [Python — Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)

---

[← Data Processing 목차](../README.md)
