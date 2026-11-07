# Chapter 08. Data Processing Project

기상 관측 데이터를 기반으로 **데이터 불러오기 → 검증 → 정제 → 결합 → 집계 → 결과 저장 → 테스트**에 이르는 전체 처리 흐름을 구현합니다. 이전 Chapter에서 학습한 Python, NumPy, Pandas, 파일 입출력, 데이터 품질 검증 및 집계 기법을 하나의 프로젝트에 적용합니다.

본 자료는 **Python 3.13.5 / Pandas 2.2.3 / NumPy 2.3.5**에서 실행 검증했습니다. 모든 데이터는 **교육용 가상 데이터**이며, 실제 기상 관측값이나 공식 관측 규정을 나타내지 않습니다. Parquet 출력은 선택 기능이며 PyArrow 설치가 필요합니다.

<details>
<summary><strong>선행 학습 목록</strong></summary>

- [Chapter 01 — Introduction to Data Processing](../Chapter-01/)
- [Chapter 02 — Python Data Structures](../Chapter-02/)
- [Chapter 03 — NumPy Fundamentals](../Chapter-03/)
- [Chapter 04 — Pandas & DataFrames](../Chapter-04/)
- [Chapter 05 — File I/O & Data Formats](../Chapter-05/)
- [Chapter 06 — Data Cleaning & Validation](../Chapter-06/)
- [Chapter 07 — Data Transformation & Aggregation](../Chapter-07/)

</details>

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [8.1](#section-8-1) | Project Overview — 목표와 결과물 |
| [8.2](#section-8-2) | Dataset & Schema — 데이터 구조와 관측 기준 |
| [8.3](#section-8-3) | Project Structure & Environment — 환경과 파일 구조 |
| [8.4](#section-8-4) | Data Loading — CSV·JSON 읽기 |
| [8.5](#section-8-5) | Validation Rules — 데이터 검증과 상태 분류 |
| [8.6](#section-8-6) | Type Conversion & Missing Data — 자료형과 결측값 |
| [8.7](#section-8-7) | Reference Data Integration — 관측소 정보 결합 |
| [8.8](#section-8-8) | Daily Aggregation — 일별 통계 계산 |
| [8.9](#section-8-9) | Coverage & Completeness — 수집률과 누락 날짜 |
| [8.10](#section-8-10) | Monthly Aggregation & NumPy — 월별 요약과 통계 검증 |
| [8.11](#section-8-11) | Data Export — CSV·JSON·Parquet 출력 |
| [8.12](#section-8-12) | Reusable Pipeline & CLI — 재사용 가능한 실행 구조 |
| [8.13](#section-8-13) | Testing & Error Handling — 테스트와 예외 처리 |
| [8.14](#section-8-14) | Mini Project — Weather Data Processing System |
| [8.15](#section-8-15) | Coding Practice |
| [8.16](#section-8-16) | Quiz & Summary |

## Getting Started

**필요 환경:** Python 3.11 이상 권장, NumPy, Pandas. 문서의 실행 결과는 Python 3.13.5에서 확인했습니다.

`Data_Processing/Chapter-08/` 디렉터리를 기준으로 실행합니다.

```bash
python -m pip install -r requirements.txt
python examples/01_project_data_overview.py
python project/main.py
python -m unittest discover -s tests -v
```

- 기본 실행은 인터넷 연결이나 API 키가 필요하지 않습니다.
- 프로젝트는 원본 `data/`를 수정하지 않고 `output/`에 결과를 저장합니다.
- Parquet까지 저장하려면 `python -m pip install -r requirements-parquet.txt`를 실행합니다.
- Windows에서는 `python` 대신 `py`를 사용할 수 있습니다. 가상환경이 활성화되어 있다면 해당 환경의 Python으로 실행하세요.
- 출력 파일은 이전 결과를 덮어쓸 수 있으므로 보관이 필요한 보고서는 별도 위치에 복사합니다.

---

<a id="section-8-1"></a>
## 8.1. Project Overview — 목표와 결과물

이번 프로젝트는 소규모 기상 관측 데이터를 대상으로 **재현 가능한 처리 흐름**을 구현하는 데 목적이 있습니다. 관측값을 읽는 것뿐 아니라 **왜 데이터를 제외했는지**, **누락된 날짜가 있는지**, **통계 수치가 어떻게 계산됐는지**까지 확인하도록 구성했습니다.

```text
weather_observations.csv + stations.json + cleaning_policy.json
    ↓
데이터 로드 · 구조 검증
    ↓
날짜/숫자 변환 · 중복/누락/범위 검사
    ↓
accepted / review / rejected 분리 및 감사 기록
    ↓
관측소 기준정보 결합 · 일별/월별 집계 · 관측 커버리지 계산
    ↓
CSV · JSON (선택: Parquet) 결과 저장
    ↓
자동 테스트 및 결과 확인
```

**완료 기준**

| 영역 | 확인할 내용 |
|---|---|
| 입력 | CSV의 열 구조, JSON 기준정보의 필수 항목 검사 |
| 검증 | 오류 코드와 분류 상태가 행 단위로 기록되는지 확인 |
| 결합 | 관측소 ID가 유일하며 모든 유효 관측값과 연결되는지 확인 |
| 집계 | 관측소·날짜별 통계와 전체 유효 기록 수가 일치하는지 확인 |
| 수집률 | 예정된 관측 슬롯과 실제 유효 기록을 구분하는지 확인 |
| 출력 | 원본은 보존하고 결과만 지정 폴더에 기록 |
| 테스트 | 정상 데이터뿐 아니라 잘못된 입력도 검증 |

이 챕터에서는 데이터 시각화 코드를 다루지 않습니다. 생성된 일별·월별 결과 파일은 이후 [Data Visualization](../../Data_Visualization/) 과정에서 그래프와 대시보드 제작에 활용할 수 있습니다.


---

<a id="section-8-2"></a>
## 8.2. Dataset & Schema — 데이터 구조와 관측 기준

입력 데이터는 세 파일로 구성됩니다. 데이터의 **열 이름, 자료형, 단위, 결측 표현, 허용 범위**를 확인하는 작업을 Schema와 Metadata 확인이라고 합니다.

| 파일 | 내용 | 주요 필드 |
|---|---|---|
| `weather_observations.csv` | 기상 관측 기록 | ID, 현지 시각, 관측소, 기온, 습도, 강수량 |
| `stations.json` | 관측소 기준정보 | 관측소 ID, 지역, 고도 |
| `cleaning_policy.json` | 검증 정책 | 날짜 범위, 허용 시각, 측정값 범위 |

**관측 데이터의 단위(Grain):** 한 행은 한 관측소에서 특정 시각에 수집한 하나의 기록입니다. 2026년 10월 1일부터 14일까지 관측소 3곳에서 하루 2회(09:00, 18:00) 측정한다고 가정하므로 예정된 관측 슬롯은 다음과 같습니다.

$$
14\text{일} \times 3\text{개 관측소} \times 2\text{회/일} = 84\text{개 슬롯}
$$

원본 CSV에는 82개의 예정된 슬롯 기록과 검증 실습용 추가 기록 10개, 총 **92개 행**이 있습니다. `ST-02` 관측소의 10월 9일 2개 슬롯은 원본에서 누락했습니다. 82개 행 중 일부에도 결측값과 의심값이 포함돼 있습니다.

| 열 | 의미 | 정상 조건 |
|---|---|---|
| `observation_id` | 관측 기록 고유 ID | 빈 값·중복 없음 |
| `timestamp_local` | 관측 일시(KST) | `YYYY-MM-DD HH:MM` 형식, 지정 날짜·시각 |
| `station_id` | 관측소 ID | 기준정보에 등록된 값 |
| `temperature_c` | 기온(°C) | -30~45°C, 유한한 숫자 |
| `humidity_pct` | 상대습도(%) | 0~100%, 유한한 숫자 |
| `precipitation_mm` | 이전 관측부터의 누적 강수량(mm) | 0 이상, 유한한 숫자 |

강수량이 `0`이면 **강수량 0mm로 관측한 값**입니다. 관측 기록이 없거나 숫자 필드가 비어 있는 상태와 같지 않습니다. 날짜 문자열은 KST 기준으로 해석하지만 파일 자체에는 UTC Offset이 포함돼 있지 않습니다. 다른 시간대 자료와 결합할 때는 시간대를 명시적으로 지정해야 합니다.

자세한 열 정의와 검증 정책은 [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)를 참고하세요.


---

<a id="section-8-3"></a>
## 8.3. Project Structure & Environment — 환경과 파일 구조

여러 기능을 한 파일에 모두 작성하는 대신 **입력·검증·집계·저장**을 각각 함수로 구성합니다. `project/main.py`는 명령행 인수를 받아 파이프라인을 실행하는 진입점입니다.

```text
Chapter-08/
├── README.md
├── requirements.txt
├── requirements-parquet.txt
├── .gitignore
├── data/
│   ├── DATA_DICTIONARY.md
│   ├── weather_observations.csv
│   ├── stations.json
│   └── cleaning_policy.json
├── examples/                     # 실행 가능한 단계별 예제 11개
├── exercises/                    # 연습문제 시작 코드 5개
├── solutions/                    # 연습문제 정답 코드 5개
├── project/
│   ├── main.py
│   └── processing/
│       ├── __init__.py
│       └── pipeline.py
├── tests/
│   └── test_chapter08.py
└── output/                       # 실행 시 자동 생성, Git 추적 제외
```

필요한 패키지는 `requirements.txt`로 관리합니다. 예제 파일은 `Path(__file__)` 기준으로 데이터 경로를 찾아 실행 위치에 따른 경로 오류를 줄였습니다.

**핵심 함수** — [pipeline.py](./project/processing/pipeline.py)

| 함수 | 역할 |
|---|---|
| `load_inputs()` | CSV·JSON 읽기, 필수 열과 기준정보 검증 |
| `validate_and_clean()` | 데이터 타입·품질 검사, accepted/review/rejected 분리 |
| `make_summaries()` | 일별·관측소별·월별 요약 및 수집 현황 생성 |
| `make_quality_report()` | 품질 검사 결과와 수집률 요약 |
| `run_pipeline()` | 전체 과정 연결 및 파일 저장 |

각 함수는 앞 단계의 결과를 입력으로 받기 때문에 개별 검증과 재사용이 용이합니다.


---

<a id="section-8-4"></a>
## 8.4. Data Loading — CSV·JSON 읽기

CSV는 열의 이름이 올바른지 확인한 뒤 **모든 원본 값을 먼저 문자열로 읽습니다**. 숫자 변환을 먼저 수행하면 공백, `sensor_error` 같은 원래 입력이 어떤 형태였는지 구분하기 어려워질 수 있기 때문입니다.

```python
raw = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
```

- `dtype=str`: 원본 필드 값을 문자열로 읽습니다.
- `keep_default_na=False`: 빈 필드를 자동으로 NaN으로 변경하지 않습니다.
- `encoding="utf-8-sig"`: UTF-8과 UTF-8 BOM이 포함된 CSV를 읽습니다.
- JSON은 Python 표준 라이브러리 `json.load()`로 처리합니다.

**필수 열 검사:** 동일한 이름의 CSV 열이 두 번 존재하면 데이터 열의 의미가 모호해질 수 있습니다. 프로젝트는 `csv.reader`로 원본 헤더를 먼저 검사하고, 예상 열과 정확하게 일치하는지 확인합니다.


**예제 코드 — [01_project_data_overview.py](./examples/01_project_data_overview.py)**

```python
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
raw = pd.read_csv(DATA / "weather_observations.csv", dtype=str, keep_default_na=False)
print("Rows:", len(raw))
print("Columns:", ", ".join(raw.columns))
print("Stations (raw):", sorted(raw["station_id"].unique().tolist()))
```

**실행 결과**

```text
Rows: 92
Columns: observation_id, timestamp_local, station_id, temperature_c, humidity_pct, precipitation_mm
Stations (raw): ['ST-01', 'ST-02', 'ST-03', 'ST-X']
```


---

<a id="section-8-5"></a>
## 8.5. Validation Rules — 데이터 검증과 상태 분류

수집된 모든 기록을 무조건 합산하면 잘못된 결과가 나올 수 있습니다. 이 프로젝트에서는 검증 결과에 따라 세 가지 상태로 분류합니다.

| 상태 | 의미 | 집계 포함 여부 |
|---|---|:---:|
| `accepted` | 정의한 검증 규칙을 모두 만족 | O |
| `review` | 누락되거나 의심스러워 추가 확인 필요 | X |
| `rejected` | 고유 ID·관측소·일시·필수 범위 등의 규칙 위반 | X |

**대표 규칙**

| 검증 조건 | 처리 | 사유 코드 예시 |
|---|---|---|
| 관측 ID가 중복 | rejected | `duplicate_observation_id` |
| 등록되지 않은 관측소 | rejected | `unknown_station` |
| 관측 일시가 잘못되거나 예정 외 시간 | rejected | `invalid_timestamp`, `unexpected_observation_time` |
| 동일 관측소·시각 중복 | rejected | `duplicate_observation_slot` |
| 음수 강수량·습도 범위 위반 | rejected | `negative_precipitation`, `humidity_out_of_range` |
| 기온 결측·문자열 오류·범위 밖 값 | review | `missing_temperature_c`, `temperature_out_of_range` |

한 행에 여러 문제가 있을 수 있으므로 `reason`에는 여러 코드가 `|`로 구분되어 기록됩니다. **하나라도 rejected 규칙을 위반하면 최종 상태는 rejected**이며, 그렇지 않고 review 규칙만 해당하면 review입니다.

이 장의 정책은 학습을 위한 예시입니다. 실제 관측 자료에서는 센서의 사양, 품질 규정, 측정 단위, 보정 이력 등을 별도로 고려해야 합니다.


**예제 코드 — [04_validation_summary.py](./examples/04_validation_summary.py)**

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean

raw, stations, policy = load_inputs(ROOT / "data")
clean, issues, audit = validate_and_clean(raw, stations, policy)
print("Statuses:", audit["status"].value_counts().sort_index().to_dict())
print("Issue rows:", len(issues))
print("Clean rows:", len(clean))
```

**실행 결과**

```text
Statuses: {'accepted': 79, 'rejected': 10, 'review': 3}
Issue rows: 13
Clean rows: 79
```


---

<a id="section-8-6"></a>
## 8.6. Type Conversion & Missing Data — 자료형과 결측값

`pd.to_datetime(..., errors="coerce")`는 올바르지 않은 날짜를 `NaT`로 변환합니다. `pd.to_numeric(..., errors="coerce")`는 숫자로 바꿀 수 없는 값을 `NaN`으로 변환합니다.

두 함수는 **변환 실패를 탐지**하기 위한 도구이며, `NaN`이 생겼다는 이유만으로 결측 원인까지 알 수 있는 것은 아닙니다. 검증 단계에서는 원본 문자열이 비어 있는지, 문자가 들어 있는지 등을 구분해 사유를 기록합니다.

```python
numeric = pd.to_numeric(raw["temperature_c"], errors="coerce")
finite = numeric.notna() & np.isfinite(numeric)
```

`NaN` 외에도 `inf`와 `-inf` 같은 비유한값을 검사해야 합니다. `NaN`을 기온 0°C로 바꾸면 실제 관측값과 구분이 불가능해지므로 프로젝트는 자동 대체하지 않습니다. 결측값이 포함된 기록은 review로 분리한 뒤 별도 판단을 기다립니다.

**주의:** 다음 예제의 유효한 기온 개수는 **기온 열에 대해서만** 조건을 검사한 결과입니다. 최종 accepted 건수와 같지 않습니다. 다른 열과 참조정보까지 검증해야 최종 기록으로 인정됩니다.


**예제 코드 — [03_type_conversion.py](./examples/03_type_conversion.py)**

```python
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
raw = pd.read_csv(DATA / "weather_observations.csv", dtype=str, keep_default_na=False)
converted = pd.to_numeric(raw["temperature_c"], errors="coerce")
timestamps = pd.to_datetime(raw["timestamp_local"], format="%Y-%m-%d %H:%M", errors="coerce")
print("Unparseable/missing temperatures:", int(converted.isna().sum()))
print("Invalid timestamps:", int(timestamps.isna().sum()))
print("Finite temperatures:", int((converted.notna() & converted.between(-30, 45)).sum()))
```

**실행 결과**

```text
Unparseable/missing temperatures: 3
Invalid timestamps: 1
Finite temperatures: 87
```


---

<a id="section-8-7"></a>
## 8.7. Reference Data Integration — 관측소 정보 결합

기상 관측 CSV에는 관측소 ID만 들어 있습니다. 지역명과 고도는 별도의 `stations.json`에서 읽어 `merge()`로 결합합니다.

```python
joined = measurements.merge(
    stations, on="station_id", how="left",
    validate="many_to_one", indicator=True,
)
```

- `many_to_one`: 관측 데이터에는 같은 관측소 ID가 여러 번 나타나도 되지만 **기준정보의 ID는 유일**해야 합니다.
- `indicator=True`: `_merge` 열에 `both`, `left_only` 등을 기록해 미등록 값을 확인할 수 있습니다.
- 기준정보가 잘못돼도 행이 임의로 증식하지 않도록 결합 전에 고유성 검사를 수행합니다.

**중요:** `merge()`가 성공했다는 것만으로 데이터가 모두 연결된 것은 아닙니다. `_merge == "both"` 여부를 확인해야 합니다.


**예제 코드 — [05_reference_data_merge.py](./examples/05_reference_data_merge.py)**

```python
from pathlib import Path
import json
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
with (DATA / "stations.json").open(encoding="utf-8") as file:
    stations = pd.DataFrame(json.load(file))
measurements = pd.DataFrame({"station_id": ["ST-01", "ST-03"], "temperature_c": [19.5, 21.0]})
joined = measurements.merge(stations, on="station_id", how="left", validate="many_to_one", indicator=True)
assert joined["_merge"].eq("both").all()
print(joined[["station_id", "region", "temperature_c"]].to_string(index=False))
```

**실행 결과**

```text
station_id  region  temperature_c
     ST-01   Seoul           19.5
     ST-03 Gwangju           21.0
```


---

<a id="section-8-8"></a>
## 8.8. Daily Aggregation — 일별 통계 계산

날짜와 관측소를 기준으로 묶은 뒤 유효 관측 개수, 기온 평균, 습도 평균, 관측 구간별 강수량 합계를 계산합니다.

```python
daily = clean.groupby(["station_id", "region", "date"], as_index=False).agg(
    readings=("observation_id", "size"),
    avg_temperature_c=("temperature_c", "mean"),
    avg_humidity_pct=("humidity_pct", "mean"),
    total_precipitation_mm=("precipitation_mm", "sum"),
)
```

**단위 확인:** 기온의 평균은 °C, 강수량 합계는 mm입니다. 이 프로젝트에서 강수량은 이전 관측 시점부터의 누적량으로 정의했으므로 **구간별 강수량이 겹치지 않는다는 가정** 아래 합산합니다.

`readings`는 그날의 유효 관측 개수입니다. 원본에 1건만 남은 날은 2회 관측이 모두 완료된 날과 비교해 평균의 대표성이 낮을 수 있습니다. 집계값을 생성하더라도 `complete_day` 열로 불완전한 날임을 표시합니다.


**예제 코드 — [06_daily_station_summary.py](./examples/06_daily_station_summary.py)**

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean, make_summaries

raw, stations, policy = load_inputs(ROOT / "data")
clean, _, _ = validate_and_clean(raw, stations, policy)
daily, _, _, _ = make_summaries(clean, stations, policy)
print("Daily summary rows:", len(daily))
print("Partial days:", int((~daily["complete_day"]).sum()))
```

**실행 결과**

```text
Daily summary rows: 41
Partial days: 3
```


---

<a id="section-8-9"></a>
## 8.9. Coverage & Completeness — 수집률과 누락 날짜

집계 결과에 없는 날짜를 확인하려면 **예상되는 날짜 목록을 먼저 만들어야 합니다.** 관측 데이터만 그룹화하면 원본에 전혀 존재하지 않는 날짜는 결과 테이블에 나타나지 않습니다.

프로젝트는 관측소 3개와 14일의 전체 조합으로 예상 날짜·관측소 42개 행을 생성합니다. 각 행에서 예정된 관측 2건과 실제 accepted 건수를 비교합니다.

| 상태 | 조건 | 의미 |
|---|---|---|
| `complete` | 2건 수집 | 해당 날짜의 예정 관측 2건이 유효 |
| `partial` | 1건 수집 | 예정 관측 중 1건만 유효 |
| `missing` | 0건 수집 | 해당 날짜에 유효 관측 없음 |

**관측 슬롯 기준 수집률**

$$
\text{Coverage(\%)} = \frac{\text{유효 관측 건수}}{\text{예정 관측 슬롯 수}} \times 100
$$

$$
\frac{79}{84} \times 100 \approx 94.05\%
$$

예정 슬롯 84개 중 5개는 유효 관측 결과가 없습니다. 이 중 2개는 원본에 기록 자체가 없고, 3개는 원본에 존재하지만 review로 분리했습니다. **관측 자체가 없는 날을 0°C 또는 강수량 0mm로 채우지 않습니다.**


**예제 코드 — [07_missing_dates_and_coverage.py](./examples/07_missing_dates_and_coverage.py)**

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean, make_summaries

raw, stations, policy = load_inputs(ROOT / "data")
clean, _, _ = validate_and_clean(raw, stations, policy)
_, _, _, coverage = make_summaries(clean, stations, policy)
print("Coverage counts:", coverage["status"].value_counts().sort_index().to_dict())
missing = coverage.loc[coverage["status"].eq("missing"), ["station_id", "date"]]
print(missing.to_string(index=False))
```

**실행 결과**

```text
Coverage counts: {'complete': 38, 'missing': 1, 'partial': 3}
station_id       date
     ST-02 2026-10-09
```


---

<a id="section-8-10"></a>
## 8.10. Monthly Aggregation & NumPy — 월별 요약과 통계 검증

`year_month`로 월을 구분하고 `region`으로 그룹화하여 월별 관측값 기반 평균 기온과 누적 강수량을 계산합니다. 월별 기온 평균은 **accepted 관측값의 산술평균**이며, 서로 다른 지역의 관측 개수가 같지 않을 수 있다는 점에 주의해야 합니다.

일별 평균 기온들의 단순 평균과 전체 측정값의 평균은 관측 수가 다르면 달라질 수 있습니다. 프로젝트는 측정값을 직접 집계하고, 계산된 결과를 NumPy로 한 번 더 확인합니다.

또한 `monthly_region_summary.csv`의 월별 평균은 관측소가 하나씩 포함된 가상 예제의 결과입니다. 실제 지역 평균을 대표하려면 관측소 선정, 공간 분포, 측정 간격 등 별도의 통계적 판단이 필요합니다.


**예제 코드 — [08_monthly_region_summary.py](./examples/08_monthly_region_summary.py)**

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean, make_summaries

raw, stations, policy = load_inputs(ROOT / "data")
clean, _, _ = validate_and_clean(raw, stations, policy)
_, _, monthly, _ = make_summaries(clean, stations, policy)
print(monthly[["year_month", "region", "readings", "avg_temperature_c"]].to_string(index=False))
```

**실행 결과**

```text
year_month  region  readings  avg_temperature_c
   2026-10   Busan        25              19.06
   2026-10 Gwangju        27              21.11
   2026-10   Seoul        27              17.02
```


---

**NumPy를 이용한 검산**

NumPy 배열로 계산한 평균과 Pandas 열 평균이 같은지 확인합니다. 두 방법은 동일한 유효 값을 사용한다는 전제에서 같은 결과를 얻습니다.

<a id="section-8-10-example"></a>
### 8.10.1. NumPy 교차 검산

아래 예제는 `ST-01` 관측소의 accepted 기온 27개를 동일한 배열로 계산합니다.


**예제 코드 — [09_numpy_statistics_check.py](./examples/09_numpy_statistics_check.py)**

```python
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import load_inputs, validate_and_clean

raw, stations, policy = load_inputs(ROOT / "data")
clean, _, _ = validate_and_clean(raw, stations, policy)
values = clean.loc[clean["station_id"].eq("ST-01"), "temperature_c"].to_numpy(dtype=float)
print("Records:", len(values))
print("NumPy mean:", round(float(np.mean(values)), 2))
print("Pandas mean:", round(float(clean.loc[clean["station_id"].eq("ST-01"), "temperature_c"].mean()), 2))
```

**실행 결과**

```text
Records: 27
NumPy mean: 17.02
Pandas mean: 17.02
```


---

<a id="section-8-11"></a>
## 8.11. Data Export — CSV·JSON·Parquet 출력

정제된 관측 자료와 집계 결과를 서로 다른 파일로 저장합니다. 원본 `data/`에 쓰지 않고 **출력 전용 `output/` 폴더**를 사용합니다.

| 형식 | 출력 파일 | 용도 |
|---|---|---|
| CSV | `cleaned_weather.csv` | 검증을 통과한 상세 관측 데이터 |
| CSV | `issues.csv` | rejected/review로 분리한 기록과 사유 |
| CSV | `audit.csv` | 모든 원본 행의 최종 상태와 이유 |
| CSV | `daily_station_summary.csv` | 관측소·날짜별 집계 |
| CSV | `station_summary.csv` | 관측소별 기간 요약 |
| CSV | `monthly_region_summary.csv` | 월별·지역별 집계 |
| CSV | `coverage.csv` | 예상 슬롯과 수집 현황 |
| JSON | `quality_report.json` | 처리 건수, 사유별 건수, 수집률 |
| Parquet | `cleaned_weather.parquet` | 선택 출력, 열 기반 분석 파일 |

CSV는 `encoding="utf-8-sig"`로 저장해 일반적인 Windows 환경에서 한글 열이나 텍스트를 다루기 쉽게 했습니다. 출력 파일을 다시 읽어 행 수가 보존되는지도 확인합니다.

**Parquet 선택 실행**

```bash
python -m pip install -r requirements-parquet.txt
python project/main.py --parquet
```

Parquet 출력은 `pyarrow`가 설치되어 있어야 작동합니다. 기본 프로젝트는 PyArrow 없이 실행할 수 있습니다. CSV는 원시 시각의 표기 형식을 보장하기 어렵거나 재읽기에서 타입이 달라질 수 있으므로, 저장 후 필요에 따라 자료형을 명시하여 다시 읽어야 합니다.


**예제 코드 — [10_export_and_reload.py](./examples/10_export_and_reload.py)**

```python
import sys
from pathlib import Path
import tempfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import run_pipeline

with tempfile.TemporaryDirectory() as temp_dir:
    result = run_pipeline(ROOT / "data", Path(temp_dir))
    loaded = pd.read_csv(Path(temp_dir) / "daily_station_summary.csv")
    assert len(loaded) == len(result.daily)
    print("Saved daily rows:", len(loaded))
    print("Saved files:", len(list(Path(temp_dir).iterdir())))
```

**실행 결과**

```text
Saved daily rows: 41
Saved files: 8
```


---

<a id="section-8-12"></a>
## 8.12. Reusable Pipeline & CLI — 재사용 가능한 실행 구조

파이프라인의 각 단계를 함수로 분리하면 같은 원본 데이터를 대상으로 결과를 재현하거나 부분 단계만 테스트하기 쉽습니다.

```python
def run_pipeline(data_dir, output_dir, parquet=False):
    raw, stations, policy = load_inputs(data_dir)
    clean, issues, audit = validate_and_clean(raw, stations, policy)
    daily, station, monthly, coverage = make_summaries(clean, stations, policy)
    report = make_quality_report(audit, clean, coverage)
    # 출력 경로 검증 → CSV·JSON 저장 → 선택적으로 Parquet 저장
    ...
```

위 코드는 기능 구성을 설명하기 위한 축약본입니다. 실제 구현은 [pipeline.py](./project/processing/pipeline.py)에 있습니다.

**명령행 실행** — [main.py](./project/main.py)

```bash
python project/main.py
python project/main.py --data-dir data --output-dir output
```

`--data-dir`와 `--output-dir`로 입력과 출력 위치를 지정할 수 있습니다. 두 경로가 같거나 입력 폴더 안에 결과를 저장하려 하면 오류를 발생시킵니다. 원본을 수정하지 않지만 **출력 폴더의 파일은 갱신될 수 있습니다.** 파일 여러 개를 한꺼번에 원자적으로 교체하는 기능은 구현하지 않았습니다.


**예제 코드 — [11_weather_data_pipeline.py](./examples/11_weather_data_pipeline.py)**

```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import run_pipeline

result = run_pipeline(ROOT / "data", ROOT / "output")
report = result.report
print(f"Raw: {report['total_raw_rows']} | Accepted: {report['accepted_rows']} | "
      f"Review: {report['review_rows']} | Rejected: {report['rejected_rows']}")
print(f"Coverage: {report['valid_observations']}/{report['expected_observation_slots']} "
      f"({report['coverage_pct']:.2f}%)")
```

**실행 결과**

```text
Raw: 92 | Accepted: 79 | Review: 3 | Rejected: 10
Coverage: 79/84 (94.05%)
```


---

<a id="section-8-13"></a>
## 8.13. Testing & Error Handling — 테스트와 예외 처리

자동 테스트에서는 **결과의 숫자뿐 아니라 오류 처리 규칙과 원본 보존 여부**도 확인합니다. 프로젝트의 테스트 코드는 [test_chapter08.py](./tests/test_chapter08.py)에 있습니다.

```bash
python -m unittest discover -s tests -v
```

**테스트 범위**

| 항목 | 검증 예시 |
|---|---|
| 입력 | CSV 필수 열 검사, 원본 문자열 보존, 관측소 ID 중복 감지 |
| 데이터 분류 | accepted/review/rejected 건수, 사유 코드 확인 |
| 날짜·숫자 | 날짜 변환, 정상 시각, 기온·습도·강수량 범위 |
| 결합 | 미등록 관측소 차단, 중복 관측 슬롯 검사 |
| 집계 | 일별·관측소별·월별 기록 수와 강수량 합계 일치 |
| 수집률 | 누락된 관측소·날짜와 부분 수집 일자 판별 |
| 출력 | 생성 파일, JSON 내용, 반복 실행 결과의 동일성 |
| 안전성 | 입력 폴더 보존, 잘못된 기준정보 입력 시 출력 전 오류 |
| 정답 코드 | Coding Practice 5문제의 함수 결과 검증 |
| 선택 기능 | PyArrow 설치 여부에 따른 Parquet 기능 검사 |

**예외 처리 기준:** 입력 파일 구조나 관측소 기준정보의 심각한 오류는 파이프라인을 중단합니다. 개별 관측 기록의 오류는 원본 행과 사유를 `issues.csv`에 남겨 전체 원본을 무조건 버리지 않도록 합니다. 어떤 오류를 치명적인 오류로 취급할지는 실제 데이터와 요구사항에 맞춰 조정해야 합니다.

정제 알고리즘 자체는 같은 입력과 정책에서 같은 값을 생성하며, 프로젝트는 반복 실행 시 출력 파일이 동일하게 생성되는지 테스트합니다. 단, 이 예제는 **동시 실행 잠금, 출력 파일의 트랜잭션, 전원 장애 이후 내구성**을 보장하는 시스템은 아닙니다.


---

<a id="section-8-14"></a>
## 8.14. Mini Project — Weather Data Processing System

앞의 내용을 하나로 연결한 완성 프로젝트입니다. 제공된 가상 기상 데이터를 처리하여 최종 CSV·JSON 파일을 생성합니다.

**입력 데이터 및 정책**

- 2026-10-01~2026-10-14, 3개 관측소, 하루 2회 측정
- 관측 예정 슬롯: 84개, 원본 CSV 행: 92개(추가 오류 행 포함)
- 유효하지 않은 시간·ID·습도·강수량 기록은 rejected
- 기온 또는 수치형 필드에 확인이 필요한 값이 있으면 review
- accepted만 집계하고, 모든 행의 상태는 감사 기록에 보관

**처리 결과**

| 항목 | 건수 |
|---|---:|
| 원본 CSV | 92 |
| 정상(accepted) | 79 |
| 검토(review) | 3 |
| 제외(rejected) | 10 |
| 예정 관측 슬롯 | 84 |
| 유효 관측 슬롯 | 79 |
| 전체 수집률 | 94.05% |
| 완전 수집 관측소·일자 | 38 |
| 부분 수집 관측소·일자 | 3 |
| 관측 누락 관측소·일자 | 1 |

**관측소별 결과 (`station_summary.csv`)**

| 관측소 | 지역 | 유효 기록 | 평균 기온 | 누적 강수량 |
|---|---|---:|---:|---:|
| ST-01 | Seoul | 27 | 17.02°C | 18.00mm |
| ST-02 | Busan | 25 | 19.06°C | 17.50mm |
| ST-03 | Gwangju | 27 | 21.11°C | 17.50mm |

이 값은 프로젝트에서 정의한 가상 관측값을 계산한 결과이며 지역별 기후를 비교하기 위한 지표가 아닙니다.

**확인할 사항**

1. `issues.csv`에서 각 오류 기록의 `source_row`, `status`, `reason`을 확인합니다.
2. `coverage.csv`에서 `ST-02 / 2026-10-09`가 `missing`으로 기록되는지 확인합니다.
3. `daily_station_summary.csv`에서 `complete_day`가 `False`인 날짜를 찾습니다.
4. `quality_report.json`의 각 상태 건수 합계가 원본 92개와 일치하는지 확인합니다.
5. `cleaned_weather.csv`의 유효 기록 수가 79개인지 확인합니다.

**추가 탐구:** 실제 데이터로 바꾸려면 측정 주기, 시간대, 결측 표시, 관측소 ID 및 각 측정 변수의 단위가 프로젝트 정책과 일치하는지 먼저 검증해야 합니다. 단순히 CSV 경로만 변경해서 결과를 신뢰해서는 안 됩니다.


---

<a id="section-8-15"></a>
## 8.15. Coding Practice

각 문제의 미완성 함수는 `exercises/`, 정답 함수는 `solutions/`에 있습니다. 먼저 함수의 주석과 반환 조건을 확인하고 직접 작성한 뒤 모범답안과 비교하세요. `NotImplementedError`는 함수 구현 전임을 나타냅니다.

| 번호 | 실습 | 문제 코드 | 정답 코드 |
|:---:|---|---|---|
| 01 | 필수 컬럼 검증 | [01_required_columns.py](./exercises/01_required_columns.py) | [정답](./solutions/01_required_columns.py) |
| 02 | 기온 자료형·범위 검증 | [02_temperature_validation.py](./exercises/02_temperature_validation.py) | [정답](./solutions/02_temperature_validation.py) |
| 03 | 관측소별 평균 기온 | [03_station_aggregation.py](./exercises/03_station_aggregation.py) | [정답](./solutions/03_station_aggregation.py) |
| 04 | 안전한 기준정보 결합 | [04_safe_station_join.py](./exercises/04_safe_station_join.py) | [정답](./solutions/04_safe_station_join.py) |
| 05 | 유효 관측 수집률 | [05_observation_coverage.py](./exercises/05_observation_coverage.py) | [정답](./solutions/05_observation_coverage.py) |

### Exercise 01 — Required Columns

`check_required_columns(df, columns)`를 구현합니다. `columns`의 모든 열이 존재하면 `True`, 하나라도 누락되면 `False`를 반환합니다. 빈 목록은 `True`입니다.

```text
check_required_columns(DataFrame({'a': [1]}), ['a'])       → True
check_required_columns(DataFrame({'a': [1]}), ['a', 'b'])  → False
```

### Exercise 02 — Temperature Validation

문자열 기온을 숫자로 변환하고 `-30~45°C` 범위의 유한한 값만 `valid=True`로 표시합니다. 원본 데이터는 수정하지 않습니다.

```text
입력:  ['21.5', '', '68', 'invalid']
valid: [True, False, False, False]
```

### Exercise 03 — Station Aggregation

`station_id`별 평균 기온을 구하고 소수 둘째 자리로 반올림합니다. 결과는 관측소 ID 오름차순으로 정렬합니다.

```text
ST-01: [20, 22] → 21.0
ST-02: [25]     → 25.0
```

### Exercise 04 — Safe Station Join

관측값과 관측소 테이블을 `station_id`로 결합합니다. 기준정보에 중복 키가 있거나 미등록 관측소가 발견되면 `ValueError`를 발생시킵니다. 원래 관측값의 순서를 유지합니다.

### Exercise 05 — Observation Coverage

예정된 관측 슬롯과 accepted 기록 수로 수집률을 계산합니다. 입력 슬롯 수는 양의 정수여야 하며 유효 관측 수가 예정 슬롯 수를 초과하는 경우에도 오류를 발생시킵니다.

```text
유효 관측 3건 / 예정 슬롯 4개 → 75.0%
```

**정답 실행** — `Chapter-08/` 기준

```bash
python solutions/01_required_columns.py
python solutions/02_temperature_validation.py
python solutions/03_station_aggregation.py
python solutions/04_safe_station_join.py
python solutions/05_observation_coverage.py
```

실습 함수에 대해 다양한 입력을 자동 검증하는 테스트도 포함돼 있습니다. `python -m unittest discover -s tests -v`로 확인할 수 있습니다.


---

<a id="section-8-16"></a>
## 8.16. Quiz & Summary

### Quiz

문제를 먼저 풀고 각 질문 아래의 **정답 및 해설 확인**을 펼쳐 답을 확인하세요. 정답은 문제별로 독립적으로 열립니다.

**Q1.** 기상 관측 프로젝트에서 원본 CSV의 숫자 열을 처음부터 모두 문자열로 읽는 이유는 무엇인가요?

<details>
<summary>Q1. 정답 및 해설 확인</summary>

**정답:** 원래 필드의 공백, 오류 문자열, 숫자 표기를 보존하고 나중에 검증하기 위해서입니다. 처음부터 자동 변환하면 오류 원인을 구분하기 어려울 수 있습니다.

</details>

**Q2.** 한 행에 `temperature_out_of_range`와 `unexpected_observation_time`이 동시에 있으면 최종 상태는 무엇인가요?

<details>
<summary>Q2. 정답 및 해설 확인</summary>

**정답:** `rejected`입니다. 예정 외 관측 시각이 rejected 규칙이며, rejected 규칙은 review 규칙보다 우선합니다. 두 사유는 모두 감사 기록에 남습니다.

</details>

**Q3.** `review` 상태인 기록을 유효 관측 통계에 포함하나요?

<details>
<summary>Q3. 정답 및 해설 확인</summary>

**정답:** 포함하지 않습니다. 확인이 필요한 데이터는 `issues.csv`와 `audit.csv`에 기록하고 accepted 기록만 집계합니다.

</details>

**Q4.** `merge(validate="many_to_one")`에서 관측소 기준정보의 ID가 중복되면 어떻게 되나요?

<details>
<summary>Q4. 정답 및 해설 확인</summary>

**정답:** 결합 관계 조건을 위반하므로 오류가 발생합니다. 관측 데이터에는 같은 관측소가 여러 행이어도 되지만 기준정보의 ID는 유일해야 합니다.

</details>

**Q5.** 강수량 0mm와 관측 기록이 없는 날은 같은 의미인가요?

<details>
<summary>Q5. 정답 및 해설 확인</summary>

**정답:** 다릅니다. 0mm는 측정 후 강수가 없음을 나타내며, 기록 누락은 해당 기간의 측정 여부를 알 수 없다는 의미입니다. 누락 날짜에 0을 채우면 잘못된 결론이 나올 수 있습니다.

</details>

**Q6.** 데이터 전체 행이 92개인데 예정 관측 슬롯은 왜 84개인가요?

<details>
<summary>Q6. 정답 및 해설 확인</summary>

**정답:** 관측소 3개 × 14일 × 하루 2회로 예정 슬롯이 84개이며, 원본 92행에는 유효하지 않은 별도 오류 기록 10개가 포함돼 있습니다. 반대로 예정 슬롯 2개는 원본에 없습니다.

</details>

**Q7.** 유효 관측 79건, 예정 관측 84건일 때 수집률은 얼마인가요? 소수 둘째 자리까지 반올림하세요.

<details>
<summary>Q7. 정답 및 해설 확인</summary>

**정답:** `79 / 84 × 100 ≈ 94.05%`입니다. 원본 전체 92행을 분자로 사용하면 수집률을 잘못 계산합니다.

</details>

**Q8.** `ST-02`의 2026-10-09 관측이 모두 누락된 경우 `daily_station_summary.csv`에는 해당 날짜의 평균 기온이 0으로 생성되나요?

<details>
<summary>Q8. 정답 및 해설 확인</summary>

**정답:** 아닙니다. 해당 날짜의 유효 기록이 없어 일별 집계 행은 생성되지 않습니다. 대신 `coverage.csv`에 `missing`으로 나타납니다.

</details>

**Q9.** 월별 지역 평균 기온을 계산할 때 일별 평균을 단순히 다시 평균 내도 항상 같은 결과가 나오나요?

<details>
<summary>Q9. 정답 및 해설 확인</summary>

**정답:** 아닙니다. 각 날짜의 유효 관측 건수가 다르면 단순 일별 평균의 평균과 전체 관측값의 평균이 달라질 수 있습니다. 프로젝트는 개별 유효 관측값을 기준으로 계산합니다.

</details>

**Q10.** `pd.to_numeric(..., errors="coerce")`에서 숫자로 바꿀 수 없는 문자열은 어떻게 처리하나요?

<details>
<summary>Q10. 정답 및 해설 확인</summary>

**정답:** 일반적으로 `NaN`으로 변환됩니다. 원본 값이 실제 결측이었는지 오류 문자열이었는지는 별도로 구분해야 하며, `inf` 같은 비유한값도 검사해야 합니다.

</details>

**Q11.** Parquet 파일을 저장하기 위해 반드시 필요한 선택 패키지는 무엇인가요?

<details>
<summary>Q11. 정답 및 해설 확인</summary>

**정답:** 이 프로젝트는 `pyarrow`를 사용합니다. 설치되지 않으면 Parquet 출력 전에 명시적인 오류를 발생시키며 기본 CSV·JSON 실행에는 필요하지 않습니다.

</details>

**Q12.** 같은 원본 데이터를 두 번 실행했을 때 결과가 같더라도 여러 출력 파일이 동시에 안전하게 교체된다고 보장되나요?

<details>
<summary>Q12. 정답 및 해설 확인</summary>

**정답:** 보장되지 않습니다. 결과가 재현 가능하다는 것과 다중 파일의 원자적 교체·장애 복구·동시 실행 안전성은 서로 다른 요구사항입니다.

</details>

### Summary

- **Data Pipeline:** 입력, 검증, 정제, 결합, 집계, 출력 단계를 독립적인 함수로 설계
- **Schema:** CSV 열 구조와 JSON 기준정보의 필수 필드 확인
- **Raw Data:** 처음에는 원본 값을 보존하고 변환·검증 단계에서 의미 부여
- **Validation:** accepted/review/rejected 상태 및 사유 코드를 행마다 기록
- **Audit Trail:** 원본 행 번호, 분류 상태, 원인으로 처리 과정을 추적
- **Reference Join:** `merge(validate="many_to_one")`로 중복 키에 따른 행 증가 방지
- **Time Series:** 일별·월별 집계 시 관측 단위와 시간대를 명시
- **Coverage:** 예정 슬롯과 accepted 관측 수를 비교하고 누락 날짜를 별도로 기록
- **Missing vs Zero:** 관측이 없는 상태와 값이 0인 측정을 구분
- **Export:** CSV·JSON 기본 출력, 필요할 때 Parquet 선택 사용
- **Testing:** 데이터 오류, 반복 실행, 원본 보존, 집계 일치 여부 검증
- **Next Step:** Data Visualization에서 정제 결과와 집계 데이터를 그래프로 표현

### References

- [Python Documentation — `pathlib`](https://docs.python.org/3/library/pathlib.html)
- [Python Documentation — `json`](https://docs.python.org/3/library/json.html)
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Pandas — `read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [Pandas — `to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)
- [Pandas — Merge, Join, Concatenate](https://pandas.pydata.org/docs/user_guide/merging.html)
- [Pandas — GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Pandas — Time Series](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [Pandas — `to_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html)
- [Apache Arrow — Python Documentation](https://arrow.apache.org/docs/python/)
- [Python Documentation — `unittest`](https://docs.python.org/3/library/unittest.html)

---

[← Data Processing 목차](../README.md) · [Chapter 07 — Data Transformation & Aggregation](../Chapter-07/) · [Data Visualization](../../Data_Visualization/)
