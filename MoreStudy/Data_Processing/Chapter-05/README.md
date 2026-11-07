# Chapter 05. File I/O & Data Formats

Python에서 파일을 안전하게 읽고 저장하는 방법과 **Text, CSV, JSON, JSON Lines, Excel, Parquet, SQLite, HTTP API**의 특성을 학습합니다. Chapter 04에서 익힌 Pandas DataFrame을 다양한 데이터 저장 형식과 연결하고, 스키마·인코딩·자료형·오류 처리를 고려한 입출력을 구현합니다.

본 자료의 예제는 **Python 3.13.5 / Pandas 2.2.3 / openpyxl 3.1.5** 환경에서 실행 검증했습니다. Parquet 예제는 `pyarrow`가 필요한 선택 실습이며, 설치되지 않은 환경에서는 안내 메시지를 출력합니다. 외부 API 호출 예제는 기본적으로 로컬 JSON 파일을 이용하므로 인터넷 연결이 필요하지 않습니다.

**선행 학습:** [Chapter 01 — Introduction to Data Processing](../Chapter-01/) · [Chapter 02 — Python Data Structures](../Chapter-02/) · [Chapter 03 — NumPy Fundamentals](../Chapter-03/) · [Chapter 04 — Pandas & DataFrames](../Chapter-04/)

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [5.1](#section-5-1) | File Paths & `pathlib` — 경로 구성과 기준 디렉터리 |
| [5.2](#section-5-2) | Text File I/O — UTF-8 텍스트 읽기와 저장 |
| [5.3](#section-5-3) | CSV & `csv` — 필드, 인용부호, 표준 라이브러리 |
| [5.4](#section-5-4) | CSV with Pandas — 열 자료형과 인코딩 제어 |
| [5.5](#section-5-5) | JSON — 객체·배열·중첩 구조 |
| [5.6](#section-5-6) | JSON Lines — 행 단위 JSON 데이터 |
| [5.7](#section-5-7) | Excel — 시트별 읽기와 저장 |
| [5.8](#section-5-8) | Parquet & Apache Arrow — 열 기반 데이터 저장 |
| [5.9](#section-5-9) | SQLite & SQL Basics — 관계형 데이터 조회와 매개변수 |
| [5.10](#section-5-10) | HTTP API & JSON Responses — 오프라인 응답과 선택적 API 호출 |
| [5.11](#section-5-11) | Data Format Comparison — 파일 형식 선택과 상호 변환 |
| [5.12](#section-5-12) | Encoding & Safe Export — 인코딩, 덮어쓰기, 임시 파일 |
| [5.13](#section-5-13) | Error Handling & Validation — 실패 원인 구분 |
| [5.14](#section-5-14) | Mini Project — Multi-Format Sales Report |
| [5.15](#section-5-15) | Coding Practice |
| [5.16](#section-5-16) | Quiz & Summary |

## Getting Started

Chapter 05는 Python 표준 라이브러리 외에 `pandas`와 Excel용 `openpyxl`을 사용합니다. `pyarrow`는 Parquet 실습에 필요합니다. 가상환경에서 다음 명령어로 설치할 수 있습니다.

```bash
python -m pip install pandas openpyxl pyarrow
```

또는 제공된 `requirements.txt`를 이용합니다.

```bash
python -m pip install -r requirements.txt
```

**실행 기준 경로:** `Data_Processing/Chapter-05/`

```bash
python examples/01_paths.py
python examples/07_excel_read.py
python examples/15_multiformat_report.py
python -m unittest discover -s tests -v
```

Windows의 경우 Python 실행 명령어가 `py`일 수 있습니다. 대부분의 예제는 `Path(__file__)`로 현재 소스 파일을 기준으로 데이터 위치를 계산하므로 VS Code나 Git Bash에서도 같은 파일을 읽습니다.

```text
Chapter-05/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   ├── DATA_DICTIONARY.md
│   ├── notes.txt
│   ├── orders.csv
│   ├── products.json
│   ├── readings.jsonl
│   ├── regions.xlsx
│   └── api_response.json
├── examples/
│   ├── 01_paths.py
│   ├── ...
│   └── 15_multiformat_report.py
├── exercises/
├── solutions/
├── tests/
│   └── test_chapter05.py
└── output/                 # 실행 시 생성, Git 추적 제외
```

전체 실습 데이터의 의미와 컬럼 정의는 [DATA_DICTIONARY.md](./data/DATA_DICTIONARY.md)에 있습니다. 모든 데이터는 학습용으로 제작한 가상 데이터입니다. 프로그램은 원본 `data/`를 변경하지 않고 결과를 `output/`에 저장합니다.

---

<a id="section-5-1"></a>
## 5.1. File Paths & `pathlib` — 경로 구성과 기준 디렉터리

데이터가 저장된 위치를 나타내는 문자열을 **파일 경로(Path)**라고 합니다. Python 표준 라이브러리의 `pathlib.Path`는 운영체제별 경로 구분자를 직접 처리하지 않고 경로를 조합하고 확인할 수 있도록 도와줍니다.

| 표현 | 의미 | 예시 |
|---|---|---|
| 절대 경로(Absolute Path) | 파일 시스템의 기준 위치부터 표현 | `D:/Hub/data/orders.csv` |
| 상대 경로(Relative Path) | 현재 작업 디렉터리를 기준으로 표현 | `data/orders.csv` |
| 현재 작업 디렉터리 | 프로그램을 실행한 셸의 위치 | `Path.cwd()` |
| 스크립트 위치 | 현재 `.py` 파일의 위치 | `Path(__file__).resolve()` |

상대 경로는 프로그램의 **현재 작업 디렉터리**에 따라 달라질 수 있습니다. 따라서 별도 실습 파일을 참조할 때는 소스 파일의 위치를 기준으로 경로를 계산하면 실행 위치 차이로 발생하는 오류를 줄일 수 있습니다.

**예제 코드 — [01_paths.py](./examples/01_paths.py)**

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
source = CHAPTER / "data" / "orders.csv"

print("Chapter:", CHAPTER.name)
print("Name:", source.name)
print("Suffix:", source.suffix)
print("Exists:", source.is_file())
```

**실행 결과**

```text
Chapter: Chapter-05
Name: orders.csv
Suffix: .csv
Exists: True
```

`Path(__file__).resolve().parents[1]`은 현재 예제가 `examples/` 안에 있다는 디렉터리 구조를 전제로 합니다. 파일 구조를 변경하면 상위 경로 계산도 함께 확인해야 합니다.

- `path.name`: 확장자를 포함한 파일명
- `path.suffix`: 마지막 확장자
- `path.parent`: 상위 경로
- `path.is_file()`: 현재 시점의 일반 파일 존재 여부
- `path / "name.csv"`: 경로 구성 요소 결합

파일이 존재한다는 검사를 통과해도, 실제로 열기 전 삭제되거나 접근 권한이 변경될 수 있습니다. 따라서 **존재 검사만으로 읽기 성공을 보장할 수는 없습니다.**

---

<a id="section-5-2"></a>
## 5.2. Text File I/O — UTF-8 텍스트 읽기와 저장

텍스트 파일은 문자 데이터를 특정 **문자 인코딩(Encoding)**으로 변환한 바이트를 저장합니다. `read_text()`와 `write_text()`는 작은 텍스트 파일을 다룰 때 간단하게 사용할 수 있습니다. 기본 인코딩에 의존하지 않도록 `encoding="utf-8"`을 명시하는 것이 좋습니다.

| 방법 | 용도 | 특성 |
|---|---|---|
| `Path.read_text()` | 파일 전체 읽기 | 파일 전체를 문자열로 반환 |
| `Path.write_text()` | 파일 전체 쓰기 | 기본적으로 기존 파일 내용 교체 |
| `path.open("r")` | 파일 입력 스트림 | 한 줄씩 읽는 방식 사용 가능 |
| `path.open("a")` | 파일 내용 추가 | 기존 파일 뒤에 기록 |
| `with ... as file` | 파일 열기와 닫기 관리 | 블록 종료 시 파일 닫기 |

**예제 코드 — [02_text_io.py](./examples/02_text_io.py)**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "data" / "notes.txt"
output = ROOT / "output" / "notes_copy.txt"

lines = source.read_text(encoding="utf-8").splitlines()
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("Lines:", len(lines))
print("First:", lines[0])
print("Saved:", output.name)
```

**실행 결과**

```text
Lines: 3
First: Data Processing 학습 노트
Saved: notes_copy.txt
```

**주의:** `write_text()`는 이미 존재하는 파일의 내용을 교체합니다. 원본을 덮어쓰지 않도록 결과를 별도 `output/` 경로에 저장합니다. 파일이 수 GB 이상으로 크다면 `read_text()`로 전체를 한 번에 읽기보다는 `with path.open(...) as file:`을 통해 한 줄씩 처리하는 편이 적합할 수 있습니다.

`splitlines()`는 줄바꿈 구분자를 제거한 문자열 목록을 반환합니다. 원본의 줄바꿈 형식 자체가 중요한 파일이라면 `splitlines(keepends=True)` 또는 바이트 단위 입출력을 검토합니다.

---

<a id="section-5-3"></a>
## 5.3. CSV & `csv` — 필드, 인용부호, 표준 라이브러리

CSV(Comma-Separated Values)는 구분자로 필드를 나누는 텍스트 기반 표 형식입니다. CSV 파일은 간단해 보이지만 **필드 내부에 쉼표·큰따옴표·줄바꿈이 포함될 수 있으므로**, 문자열을 단순히 `split(",")`하는 방식으로 일반적인 CSV를 파싱하면 안 됩니다.

```csv
product,description
"A, Set","size ""Large"""
```

위 데이터의 두 번째 행은 두 필드입니다. 첫 번째 필드에는 쉼표가 있고, 두 번째 필드의 `""`는 큰따옴표 한 개로 해석됩니다.

Python 표준 라이브러리의 `csv.reader`, `csv.DictReader`, `csv.writer`, `csv.DictWriter`는 이러한 구문 규칙을 처리합니다. 파일을 열 때 `newline=""`로 설정하여 CSV 모듈 자체가 줄바꿈을 처리하도록 합니다.

**예제 코드 — [03_csv_stdlib.py](./examples/03_csv_stdlib.py)**

```python
import csv
import io
from pathlib import Path

source = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
with source.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

assert reader.fieldnames is not None
print("Columns:", len(reader.fieldnames))
print("Records:", len(rows))
print("First order:", rows[0]["order_id"])
print("Region code:", rows[0]["region_code"])

# 쉼표와 큰따옴표가 포함된 필드도 올바르게 읽습니다.
sample = 'name,note\n"sensor, A","says ""hello"""\n'
quoted = list(csv.DictReader(io.StringIO(sample)))
print("Quoted name:", quoted[0]["name"])
print("Quoted note:", quoted[0]["note"])
```

**실행 결과**

```text
Columns: 7
Records: 12
First order: ORD001
Region code: 01
Quoted name: sensor, A
Quoted note: says "hello"
```

- `DictReader`는 헤더를 Key로 사용하는 사전 형태로 각 행을 반환합니다.
- CSV에서 읽은 값은 기본적으로 **문자열**입니다. 숫자를 계산하려면 변환이 필요합니다.
- `"01"`이라는 지역 코드 또는 우편번호를 정수로 변환하면 선행 `0`이 사라질 수 있습니다.
- CSV는 고정된 자료형, 표의 시트, 수식, 서식을 저장하지 않습니다.

UTF-8 BOM이 붙은 CSV를 읽어야 한다면 `encoding="utf-8-sig"`를 사용할 수 있습니다. 인코딩은 실제 파일의 인코딩을 확인한 뒤 선택해야 합니다.

---

<a id="section-5-4"></a>
## 5.4. CSV with Pandas — 열 자료형과 인코딩 제어

Pandas는 CSV를 `DataFrame`으로 읽는 `pd.read_csv()`와, DataFrame을 CSV로 내보내는 `DataFrame.to_csv()`를 제공합니다. `read_csv()`는 자료형을 추론하지만, ID나 분류 코드처럼 **숫자처럼 보여도 문자열이어야 하는 열**은 `dtype`을 지정하는 편이 안전합니다.

**예제 코드 — [04_pandas_csv.py](./examples/04_pandas_csv.py)**

```python
from pathlib import Path
import pandas as pd

source = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
orders = pd.read_csv(
    source,
    dtype={"order_id": "string", "region_code": "string", "product_id": "string"},
    encoding="utf-8",
)
completed = orders.loc[orders["status"].eq("completed")].copy()
completed["revenue"] = completed["quantity"] * completed["unit_price"]

print("All orders:", len(orders))
print("Completed:", len(completed))
print("Revenue:", int(completed["revenue"].sum()))
print("First region:", orders.loc[0, "region_code"])
```

**실행 결과**

```text
All orders: 12
Completed: 10
Revenue: 79200
First region: 01
```

| 인수 | 역할 | 예시 |
|---|---|---|
| `dtype` | 열 자료형 명시 | `{"region_code": "string"}` |
| `encoding` | 문자열 인코딩 | `"utf-8"` |
| `usecols` | 필요한 열만 읽기 | `["order_id", "status"]` |
| `parse_dates` | 날짜 열 파싱 | `["order_date"]` |
| `chunksize` | 여러 행씩 나누어 읽기 | `10_000` |
| `na_values` | 결측값으로 취급할 문자 정의 | `["N/A", "-"]` |

`read_csv()`에서 분리 규칙, 소수점 표기, 날짜 형식, 결측값 표기를 잘못 지정하면 데이터가 조용히 바뀔 수 있습니다. 데이터를 읽은 후 `df.info()`, `df.dtypes`, `df.head()`로 자료형과 내용을 확인합니다.

데이터 정제와 검증은 Chapter 06에서, 대용량 데이터의 청크별 집계와 최적화는 Chapter 07에서 더 자세히 다룹니다.

---

<a id="section-5-5"></a>
## 5.5. JSON — 객체·배열·중첩 구조

JSON(JavaScript Object Notation)은 Key-Value 객체와 배열로 계층적인 데이터를 표현하는 형식입니다. Python의 `json` 모듈을 이용하면 파일을 읽어 사전과 리스트 등의 자료구조로 변환할 수 있습니다.

| JSON | Python 변환 결과 |
|---|---|
| Object `{}` | `dict` |
| Array `[]` | `list` |
| String | `str` |
| Number | `int` 또는 `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

**예제 코드 — [05_json_stdlib.py](./examples/05_json_stdlib.py)**

```python
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "data" / "products.json"
with path.open("r", encoding="utf-8") as file:
    document = json.load(file)

if document.get("schema_version") != 1:
    raise ValueError("지원하지 않는 상품 데이터 버전입니다.")
products = document["products"]
print("Products:", len(products))
print("First:", products[0]["name"])
```

**실행 결과**

```text
Products: 4
First: 커피
```

JSON에는 날짜(Date)나 Decimal 같은 별도의 표준 자료형이 없습니다. 날짜는 일반적으로 문자열로 표현하며, 이후 필요한 형식으로 변환합니다. 데이터 구조가 중첩되어 있다면 `pd.json_normalize()`를 이용해 표 형태로 펼칠 수 있습니다.

```python
import pandas as pd

items = [{"user": {"id": "U01"}, "score": 95}]
table = pd.json_normalize(items)
print(table.columns.tolist())  # ['score', 'user.id']
```

JSON은 파일 확장자만 확인할 것이 아니라, 최상위에 객체가 있는지 배열이 있는지, 예상 Key와 스키마 버전이 있는지 함께 확인해야 합니다.

---

<a id="section-5-6"></a>
## 5.6. JSON Lines — 행 단위 JSON 데이터

JSON Lines(`.jsonl`)는 **각 줄마다 독립적인 JSON 값 하나**를 기록하는 방식입니다. 일반 JSON 배열과 달리 하나의 큰 배열로 감쌀 필요가 없어 로그나 이벤트 데이터를 한 줄씩 기록하거나 처리할 때 유용합니다.

```jsonl
{"sensor":"ST-01","temperature_c":22.5}
{"sensor":"ST-02","temperature_c":25.0}
```

**예제 코드 — [06_json_lines.py](./examples/06_json_lines.py)**

```python
import json
from pathlib import Path

source = Path(__file__).resolve().parents[1] / "data" / "readings.jsonl"
records = []
with source.open("r", encoding="utf-8") as file:
    for line_no, line in enumerate(file, start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSONL {line_no}행 오류") from exc

print("Readings:", len(records))
print("Max temp:", max(item["temperature_c"] for item in records))
```

**실행 결과**

```text
Readings: 4
Max temp: 25.0
```

JSON Lines는 일반 JSON 문서와 구분해야 합니다. 전체 파일을 하나의 JSON으로 `json.load()`하면 여러 JSON 객체가 연속되어 있다는 이유로 오류가 발생할 수 있습니다. 각 줄에 대해 `json.loads()`를 사용하거나, Pandas의 `pd.read_json(path, lines=True)`를 이용합니다.

빈 줄 처리 정책, 각 행의 스키마 일치 여부, 오류가 발생한 줄 번호는 처리 과정에서 별도로 관리하는 것이 좋습니다.

---

<a id="section-5-7"></a>
## 5.7. Excel — 시트별 읽기와 저장

Excel `.xlsx` 파일은 CSV와 달리 여러 Worksheet(시트), 셀 서식 및 수식 등을 포함할 수 있는 파일 형식입니다. Pandas는 `pd.read_excel()`을 통해 특정 시트를 DataFrame으로 읽을 수 있고, `DataFrame.to_excel()`로 데이터를 저장할 수 있습니다. `.xlsx` 읽기·쓰기에 `openpyxl` 엔진을 사용할 수 있습니다.

**예제 — 여러 시트에서 데이터 읽기**

**예제 코드 — [07_excel_read.py](./examples/07_excel_read.py)**

```python
from pathlib import Path
import pandas as pd

source = Path(__file__).resolve().parents[1] / "data" / "regions.xlsx"
with pd.ExcelFile(source, engine="openpyxl") as excel:
    names = excel.sheet_names
    regions = pd.read_excel(excel, sheet_name="Regions", dtype={"region_code": "string"})
    targets = pd.read_excel(excel, sheet_name="Targets", dtype={"region_code": "string"})

print("Sheets:", ", ".join(names))
print("Regions:", len(regions))
print("First code:", regions.loc[0, "region_code"])
print("Total target:", int(targets["target_revenue"].sum()))
```

**실행 결과**

```text
Sheets: Regions, Targets
Regions: 3
First code: 01
Total target: 75000
```

`ExcelFile`을 사용하면 파일 내의 `sheet_names`를 확인하고 여러 시트를 읽을 수 있습니다. 코드와 지역 코드가 숫자처럼 보이는 경우에는 CSV와 마찬가지로 문자열 자료형을 명시해야 선행 0을 보호할 수 있습니다.

**예제 — 두 시트를 새 Excel 파일로 내보내기**

**예제 코드 — [08_excel_write.py](./examples/08_excel_write.py)**

```python
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parents[1]
source = root / "data" / "regions.xlsx"
output = root / "output" / "region_targets_copy.xlsx"
regions = pd.read_excel(source, sheet_name="Regions", dtype={"region_code": "string"}, engine="openpyxl")
targets = pd.read_excel(source, sheet_name="Targets", dtype={"region_code": "string"}, engine="openpyxl")

output.parent.mkdir(parents=True, exist_ok=True)
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    regions.to_excel(writer, sheet_name="Regions", index=False)
    targets.to_excel(writer, sheet_name="Targets", index=False)
print("Saved:", output.name)
print("Sheets: 2")
```

**실행 결과**

```text
Saved: region_targets_copy.xlsx
Sheets: 2
```

Pandas의 Excel 입출력은 **표 데이터 중심**입니다. 기존 파일의 차트, 셀 스타일, 조건부 서식, 복잡한 수식 등을 수정 없이 완전히 보존한다고 가정해서는 안 됩니다. 예제는 새 파일을 생성하며 원본 `data/regions.xlsx`를 수정하지 않습니다.

`sheet_name`을 지정하지 않으면 기본적으로 첫 번째 시트를 읽습니다. 원하는 시트가 항상 첫 번째에 있다고 가정하지 않는 것이 좋습니다.

---

<a id="section-5-8"></a>
## 5.8. Parquet & Apache Arrow — 열 기반 데이터 저장

Parquet은 데이터를 **열(Column) 중심으로 저장**하는 바이너리 파일 형식입니다. 같은 열에 있는 데이터를 효율적으로 압축하거나 필요한 열만 읽는 데 유리합니다. Apache Arrow는 메모리 내 열 기반 데이터 형식과 데이터 교환을 위한 프로젝트이며, Python에서는 `pyarrow` 패키지를 사용할 수 있습니다.

| CSV | Parquet |
|---|---|
| 텍스트 기반, 일반 편집기에서 확인 가능 | 바이너리 기반, 전용 도구 필요 |
| 스키마 정보가 제한적 | 자료형·스키마 정보를 함께 저장 가능 |
| 모든 열이 텍스트로 기록됨 | 열 중심의 압축 및 선택적 읽기 지원 |
| 간단한 교환에 적합 | 반복 분석과 대규모 테이블에 적합 |

**예제 코드 — [09_parquet_arrow.py](./examples/09_parquet_arrow.py)**

```python
from importlib.util import find_spec
from pathlib import Path
import pandas as pd

if find_spec("pyarrow") is None:
    print("PyArrow가 필요합니다: python -m pip install pyarrow")
else:
    root = Path(__file__).resolve().parents[1]
    orders = pd.read_csv(root / "data" / "orders.csv", dtype={"region_code": "string"})
    destination = root / "output" / "orders.parquet"
    destination.parent.mkdir(parents=True, exist_ok=True)
    orders.to_parquet(destination, engine="pyarrow", compression="snappy", index=False)
    selected = pd.read_parquet(destination, engine="pyarrow", columns=["order_id", "region_code"])
    print("Rows:", len(selected))
    print("Columns:", ", ".join(selected.columns))
```

**실행 결과**

```text
PyArrow가 필요합니다: python -m pip install pyarrow
```

`DataFrame.to_parquet()`는 `pyarrow` 같은 별도 엔진이 필요할 수 있습니다. 위 예제는 설치 여부를 확인하고, 설치되어 있다면 Parquet 파일을 생성한 뒤 `columns=[...]` 인수로 **두 개의 열만 읽습니다**.

Parquet을 사용한다고 모든 처리에서 무조건 빠른 것은 아닙니다. 데이터 크기·열 구조·압축·읽는 방법·저장 환경에 따라 결과가 달라집니다. 성능 비교 시에는 동일한 입력과 처리 조건을 맞춰 측정해야 합니다.

---

<a id="section-5-9"></a>
## 5.9. SQLite & SQL Basics — 관계형 데이터 조회와 매개변수

SQLite는 별도의 서버 설치 없이 사용할 수 있는 **파일 기반 관계형 데이터베이스**입니다. Python은 표준 라이브러리 `sqlite3`를 제공합니다. 메모리 DB(`:memory:`)를 사용하면 별도 파일 생성 없이 SQL을 학습할 수도 있습니다.

| SQL 구문 | 기능 |
|---|---|
| `CREATE TABLE` | 테이블 생성 |
| `INSERT INTO` | 레코드 추가 |
| `SELECT` | 레코드 조회 |
| `WHERE` | 조건별 행 필터링 |
| `ORDER BY` | 조회 결과 정렬 |
| `GROUP BY` | 그룹별 집계 |

**예제 코드 — [10_sqlite_basics.py](./examples/10_sqlite_basics.py)**

```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as conn, conn:
    conn.execute("CREATE TABLE sensors (sensor_id TEXT PRIMARY KEY, temperature REAL)")
    conn.executemany(
        "INSERT INTO sensors VALUES (?, ?)",
        [("ST-01", 22.5), ("ST-02", 26.0), ("ST-03", 20.5)],
    )
    threshold = 23.0
    rows = conn.execute(
        "SELECT sensor_id, temperature FROM sensors WHERE temperature >= ? ORDER BY sensor_id",
        (threshold,),
    ).fetchall()
print("Matched:", len(rows))
print("Sensors:", ", ".join(item[0] for item in rows))
```

**실행 결과**

```text
Matched: 1
Sensors: ST-02
```

**보안:** 변수로 받은 값을 SQL 문자열에 직접 붙이지 않습니다. SQL의 값 자리에는 `?` 매개변수 표시를 사용하고, 값은 `execute(sql, (value,))` 형태로 별도 전달합니다. 이를 통해 값이 SQL 구문으로 해석되는 위험을 줄일 수 있습니다.

```python
# 권장: 값은 매개변수로 전달
rows = conn.execute("SELECT * FROM sensors WHERE temperature >= ?", (23.0,))

# 피해야 하는 방식: 입력을 SQL 문자열에 연결
# conn.execute(f"SELECT * FROM sensors WHERE sensor_id = '{user_input}'")
```

`with sqlite3.connect(...) as conn:`은 트랜잭션 완료나 롤백을 도와주지만, 일반적인 `with` 블록만으로 **연결 자체가 닫히는 것은 아닙니다.** 연결 수명은 별도로 관리해야 합니다. 실제 파일 DB는 예제 15에서 출력 결과로 생성합니다.

---

<a id="section-5-10"></a>
## 5.10. HTTP API & JSON Responses — 오프라인 응답과 선택적 API 호출

외부 시스템은 HTTP API를 통해 JSON 데이터를 반환할 수 있습니다. Python에서는 `urllib.request`나 서드파티 라이브러리를 사용해 요청할 수 있습니다. 다만 API를 다룰 때는 응답의 **상태 코드, Content-Type, 타임아웃, 응답 크기, 인증 및 스키마**를 확인해야 합니다.

이번 예제는 **외부 API를 실제 호출하지 않는 오프라인 모드**가 기본입니다. `data/api_response.json`에 저장된 응답을 읽고 데이터의 개수를 출력합니다. 선택적으로 신뢰할 수 있는 HTTPS 주소를 직접 전달하여 실제 요청 동작을 연습할 수 있습니다.

**예제 코드 — [11_api_json.py](./examples/11_api_json.py)**

```python
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse

fixture = Path(__file__).resolve().parents[1] / "data" / "api_response.json"

def load_payload(url=None):
    if url is None:
        return json.loads(fixture.read_text(encoding="utf-8"))
    if urlparse(url).scheme != "https":
        raise ValueError("신뢰할 수 있는 HTTPS URL만 사용하세요.")
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "DataProcessing-Lesson/1.0"})
    with urlopen(request, timeout=10) as response:
        if "json" not in response.headers.get("Content-Type", "").lower():
            raise ValueError("JSON 응답이 아닙니다.")
        content = response.read(1_000_001)
    if len(content) > 1_000_000:
        raise ValueError("응답 크기 제한(1MB) 초과")
    return json.loads(content.decode("utf-8"))

if __name__ == "__main__":
    payload = load_payload(sys.argv[1] if len(sys.argv) > 1 else None)
    print("Payload type:", type(payload).__name__)
    if isinstance(payload, dict) and "data" in payload:
        print("Records:", len(payload["data"]))
```

**실행 결과**

```text
Payload type: dict
Records: 3
```

실행 예시는 다음과 같습니다.

```bash
python examples/11_api_json.py
# 사용자가 신뢰하는 JSON API 주소가 있는 경우에만 선택적으로 실행
python examples/11_api_json.py https://example.org/your-json-api
```

두 번째 명령어의 URL은 **형식을 보여주기 위한 예시**이며 실제 JSON API가 존재한다는 의미는 아닙니다. HTTPS를 사용하더라도 응답이 신뢰할 수 있다고 자동으로 보장되지 않습니다. 실제 API에서는 인증 토큰 노출 방지, 재시도 정책, 요청 횟수 제한, 리디렉션 대상 확인 등도 필요할 수 있습니다.

---

<a id="section-5-11"></a>
## 5.11. Data Format Comparison — 파일 형식 선택과 상호 변환

모든 데이터를 한 가지 형식으로 통일할 필요는 없습니다. 데이터의 구조, 교환 대상, 저장 용량, 열별 자료형, 검색 방식에 따라 적절한 형식을 선택합니다.

| Format | 주요 특징 | 적합한 활용 |
|---|---|---|
| Text | 구조가 자유로운 문자열 | 메모, 간단한 보고서 |
| CSV | 표 형태, 다른 프로그램과 교환 용이 | 주문 목록, 공개 통계 |
| JSON | 중첩 객체·배열 | 설정, API 응답 |
| JSONL | 한 줄당 JSON 레코드 | 로그, 이벤트 스트림 |
| Excel | 복수 시트와 사용자 편집 | 사람 중심의 검토·공유 |
| Parquet | 열 기반 바이너리·스키마 정보 | 큰 테이블, 반복 분석 |
| SQLite | SQL 검색·조건 조회 | 로컬 관계형 데이터 |

다음 예제는 CSV를 JSON으로 변환합니다. **변환 전후의 지역 코드를 비교**하여 선행 0이 유지되는지 확인합니다.

**예제 코드 — [12_convert_json.py](./examples/12_convert_json.py)**

```python
import json
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parents[1]
source = root / "data" / "orders.csv"
output = root / "output" / "orders.json"
orders = pd.read_csv(source, dtype={"region_code": "string"})
output.parent.mkdir(parents=True, exist_ok=True)
orders.to_json(output, orient="records", force_ascii=False, indent=2)

converted = json.loads(output.read_text(encoding="utf-8"))
print("Exported:", len(converted))
print("Region code:", converted[0]["region_code"])
```

**실행 결과**

```text
Exported: 12
Region code: 01
```

자료형과 구조를 옮기는 과정에서 날짜·소수 정밀도·결측값·시간대 정보는 별도로 검증해야 합니다. 파일 변환 성공은 곧 데이터의 의미가 완전히 보존되었다는 뜻은 아닙니다.

---

<a id="section-5-12"></a>
## 5.12. Encoding & Safe Export — 인코딩, 덮어쓰기, 임시 파일

파일에 데이터를 저장할 때는 **올바른 인코딩으로 쓰였는지**뿐 아니라, 기록 중 오류가 발생했을 때 기존 결과가 어떻게 되는지 고려해야 합니다.

| 고려 사항 | 권장 방법 |
|---|---|
| UTF-8 텍스트 | `encoding="utf-8"` 명시 |
| 일부 Excel 호환 CSV | 필요 시 `encoding="utf-8-sig"` 검토 |
| CSV 줄바꿈 | `open(..., newline="")` 사용 |
| 원본 파일 보호 | 입력 경로와 출력 경로 분리 |
| 중간 파일 | 같은 디렉터리에 임시 파일 작성 후 교체 |
| 오류 확인 | 쓰기 예외와 출력 경로 확인 |

**예제 코드 — [14_safe_export.py](./examples/14_safe_export.py)**

```python
import csv
import os
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
destination = root / "output" / "status_report.csv"
destination.parent.mkdir(parents=True, exist_ok=True)

# 같은 디렉터리에 임시 파일을 만든 뒤 교체합니다.
temp_name = None
try:
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=destination.parent,
        prefix=".status_", suffix=".tmp", delete=False,
    ) as file:
        temp_name = file.name
        writer = csv.writer(file)
        writer.writerow(["state", "count"])
        writer.writerow(["completed", 10])
        writer.writerow(["canceled", 2])
    os.replace(temp_name, destination)
finally:
    if temp_name is not None and os.path.exists(temp_name):
        os.unlink(temp_name)
print("Saved:", destination.name)
```

**실행 결과**

```text
Saved: status_report.csv
```

이 예제는 새 임시 파일에 전체 결과를 기록한 뒤 `os.replace()`로 대상 파일을 교체합니다. 교체 작업의 원자성 및 내구성은 운영체제와 파일 시스템에 따라 다를 수 있습니다. 특히 **전원 장애 이후 데이터가 반드시 보존된다는 보장**은 별도 동기화 절차 없이 할 수 없습니다.

외부에서 받은 문자열을 CSV로 저장하고 Excel 등 스프레드시트에서 열 때는 `=`, `+`, `-`, `@` 등으로 시작하는 값이 수식으로 해석되는 **CSV Formula Injection** 위험도 검토해야 합니다. 임의의 외부 입력을 그대로 스프레드시트 수식으로 실행시키지 않도록 데이터 사용 목적에 맞는 처리 정책이 필요합니다.

---

<a id="section-5-13"></a>
## 5.13. Error Handling & Validation — 실패 원인 구분

파일 입출력이 실패하는 이유는 다양합니다. 파일이 없을 수 있고, 인코딩이 다를 수 있으며, JSON 형식은 올바르지만 필요한 필드가 없을 수도 있습니다. 따라서 오류를 단순히 숨기기보다 **어떤 단계에서 실패했는지 구분**하는 것이 중요합니다.

| 오류/상태 | 대표 원인 | 대응 |
|---|---|---|
| `FileNotFoundError` | 파일 경로가 없거나 잘못됨 | 입력 경로 확인 |
| `PermissionError` | 접근 권한 부족 | 읽기·쓰기 권한 확인 |
| `UnicodeError` | 실제 인코딩과 지정한 인코딩 불일치 | 파일 인코딩 확인 |
| `json.JSONDecodeError` | JSON 문법 오류 | 오류 위치와 구조 확인 |
| `pd.errors.ParserError` | CSV 구분자·인용부호 등의 파싱 문제 | 입력 형식 검증 |
| `KeyError` | 필요한 열이나 키가 없음 | 스키마 검사 |
| `sqlite3.Error` | SQL 또는 DB 관련 오류 | SQL 구문과 파일 상태 확인 |

**예제 코드 — [13_error_handling.py](./examples/13_error_handling.py)**

```python
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def load_products(path: Path):
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise ValueError("상품 파일을 찾을 수 없습니다.") from exc
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("상품 파일의 인코딩 또는 JSON 형식을 확인하세요.") from exc
    if not isinstance(data, dict) or not isinstance(data.get("products"), list):
        raise ValueError("상품 목록(products)이 필요합니다.")
    return data["products"]

products = load_products(root / "data" / "products.json")
print("Valid products:", len(products))
```

**실행 결과**

```text
Valid products: 4
```

이 예제는 **파일 읽기·JSON 해석 오류**를 사용자에게 이해하기 쉬운 메시지로 바꾼 뒤, `products`가 목록인지 확인합니다. 실행 중 모든 오류를 무조건 잡아 무시하는 `except Exception: pass` 방식은 실제 문제를 숨기므로 피합니다.

데이터의 결측·중복·이상값과 같은 품질 문제는 Chapter 06에서 더 체계적으로 검증합니다.

---

<a id="section-5-14"></a>
## 5.14. Mini Project — Multi-Format Sales Report

### 프로젝트 목표

서로 다른 형식의 주문·상품·지역 데이터를 읽어 하나의 판매 보고서를 생성합니다. 이전 Chapter에서 익힌 Pandas의 선택·계산·집계 방법을 활용하지만, **이번 프로젝트의 중심은 서로 다른 데이터 형식의 올바른 입출력과 저장**에 있습니다.

```text
data/orders.csv        (주문 12건)
        ├─ CSV 읽기 ────────────────┐
data/products.json     (상품 4종)    ├─ 식별 코드 연결 → 완료 주문만 추출
        ├─ JSON 읽기 ──────────────┤
data/regions.xlsx      (지역 3곳)    │
        └─ Excel 읽기 ─────────────┘
                                    ↓
                     지역·카테고리별 매출 집계
                                    ↓
              output/revenue_by_region.csv
              output/revenue_by_category.json
              output/report.sqlite
```

**입력 규칙**

- `orders.csv`: `order_id`, `order_date`, `region_code`, `product_id`, `quantity`, `unit_price`, `status` 열
- `products.json`: `schema_version=1` 및 상품 식별자, 이름, 카테고리
- `regions.xlsx`: `Regions` 시트 및 지역 코드·이름
- 주문 ID, 상품 ID, 지역 코드는 서로 의미가 다른 식별자이며 자료형을 보존해야 합니다.
- `status=completed` 주문만 합산하고, `canceled` 주문은 제외합니다.
- 필수값 누락, 중복 ID, 미등록 코드, 잘못된 상태·날짜·수량은 오류로 처리합니다.

**예제 코드 — [15_multiformat_report.py](./examples/15_multiformat_report.py)**

```python
"""Mini Project — CSV + JSON + Excel 데이터를 읽어 지역·분류별 보고서를 생성합니다."""
import json
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def load_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    orders = pd.read_csv(
        data_dir / "orders.csv",
        dtype={"order_id": "string", "region_code": "string", "product_id": "string"},
        encoding="utf-8",
    )
    catalog = json.loads((data_dir / "products.json").read_text(encoding="utf-8"))
    if catalog.get("schema_version") != 1 or not isinstance(catalog.get("products"), list):
        raise ValueError("지원하지 않는 상품 데이터 스키마입니다.")
    products = pd.DataFrame(catalog["products"])
    regions = pd.read_excel(data_dir / "regions.xlsx", sheet_name="Regions", engine="openpyxl", dtype={"region_code": "string"})
    return orders, products, regions

def build_report(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    orders, products, regions = load_data(data_dir)
    required = {"order_id", "order_date", "region_code", "product_id", "quantity", "unit_price", "status"}
    if not required.issubset(orders.columns):
        raise ValueError("주문 파일의 필수 열이 누락되었습니다.")
    if orders["order_id"].isna().any() or orders["order_id"].duplicated().any():
        raise ValueError("주문 ID가 누락되었거나 중복되었습니다.")
    if orders[["quantity", "unit_price", "status", "product_id", "region_code"]].isna().any().any():
        raise ValueError("주문 데이터에 필수값이 누락되었습니다.")
    if not orders["status"].isin(["completed", "canceled"]).all():
        raise ValueError("알 수 없는 주문 상태가 있습니다.")
    if (orders["quantity"] <= 0).any() or (orders["unit_price"] < 0).any():
        raise ValueError("수량과 단가 범위를 확인하세요.")
    dates = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="coerce")
    if dates.isna().any():
        raise ValueError("주문 날짜를 확인하세요.")
    if products["product_id"].isna().any() or products["product_id"].duplicated().any():
        raise ValueError("상품 ID에 중복 또는 누락이 있습니다.")
    if regions["region_code"].isna().any() or regions["region_code"].duplicated().any():
        raise ValueError("지역 코드에 중복 또는 누락이 있습니다.")
    completed = orders.loc[orders["status"].eq("completed")].copy()
    joined = completed.merge(products[["product_id", "name", "category"]], on="product_id", how="left", validate="many_to_one")
    joined = joined.merge(regions[["region_code", "region_name"]], on="region_code", how="left", validate="many_to_one")
    if joined[["name", "category", "region_name"]].isna().any().any():
        raise ValueError("상품 또는 지역 참조 데이터에 일치하지 않는 코드가 있습니다.")
    joined["revenue"] = joined["quantity"] * joined["unit_price"]
    by_region = joined.groupby("region_name", as_index=False)["revenue"].sum().sort_values("region_name").reset_index(drop=True)
    by_category = joined.groupby("category", as_index=False)["revenue"].sum().sort_values("category").reset_index(drop=True)
    return joined, by_region, by_category

def export_report(output_dir: Path, completed: pd.DataFrame, by_region: pd.DataFrame, by_category: pd.DataFrame) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    by_region.to_csv(output_dir / "revenue_by_region.csv", index=False, encoding="utf-8-sig")
    (output_dir / "revenue_by_category.json").write_text(
        by_category.to_json(orient="records", force_ascii=False, indent=2), encoding="utf-8"
    )
    db_path = output_dir / "report.sqlite"
    connection = sqlite3.connect(db_path)
    try:
        with connection:
            by_region.to_sql("revenue_by_region", connection, if_exists="replace", index=False)
            by_category.to_sql("revenue_by_category", connection, if_exists="replace", index=False)
    finally:
        connection.close()

def main() -> None:
    completed, by_region, by_category = build_report(ROOT / "data")
    export_report(ROOT / "output", completed, by_region, by_category)
    print("Completed orders:", len(completed))
    print("Total revenue:", int(completed["revenue"].sum()))
    print("Regions:", len(by_region))
    print("Categories:", len(by_category))
    print("Saved: revenue_by_region.csv, revenue_by_category.json, report.sqlite")

if __name__ == "__main__":
    main()
```

**실행 방법** — `Chapter-05/` 기준

```bash
python examples/15_multiformat_report.py
```

**실행 결과**

```text
Completed orders: 10
Total revenue: 79200
Regions: 3
Categories: 3
Saved: revenue_by_region.csv, revenue_by_category.json, report.sqlite
```

**지역별 매출 결과** (`output/revenue_by_region.csv`)

```csv
region_name,revenue
광주,30500
부산,27900
서울,20800
```

**카테고리별 매출 결과** (`output/revenue_by_category.json`)

```json
[
  {"category":"문구","revenue":25700},
  {"category":"생활","revenue":36000},
  {"category":"음료","revenue":17500}
]
```

**핵심 확인**

- 완료 주문: **10건**, 취소 주문: **2건**, 완료 주문 총매출: **79,200원**
- `merge(..., validate="many_to_one")`을 이용해 참조 테이블의 고유성을 확인합니다.
- 일치하지 않는 상품·지역 코드가 있으면 조용히 누락하거나 임의의 값으로 대체하지 않습니다.
- 출력은 CSV·JSON·SQLite 세 종류로 저장하되 원본 파일은 유지합니다.
- 출력 단계에서 개별 파일 중 일부만 저장될 수 있습니다. 여러 출력 파일 전체의 원자적 갱신까지 구현한 것은 아닙니다.

**테스트 실행**

```bash
python -m unittest discover -s tests -v
```

테스트에서는 정상 출력뿐 아니라 중복 주문 ID, 잘못된 상태, 존재하지 않는 상품 코드, 음수 수량, 잘못된 날짜를 검증합니다.

---

<a id="section-5-15"></a>
## 5.15. Coding Practice

`exercises/`에 학생이 직접 작성할 시작 코드, `solutions/`에 모범답안을 제공합니다. 먼저 TODO 항목을 구현한 뒤 정답을 비교해 보세요. 문제의 결과는 제공된 가상 데이터에 맞춰 작성했습니다.

| 번호 | 문제 | 시작 코드 | 정답 코드 |
|:---:|---|---|---|
| 01 | CSV 완료 주문 집계 | [01_csv_order_summary.py](./exercises/01_csv_order_summary.py) | [정답](./solutions/01_csv_order_summary.py) |
| 02 | JSON 상품 ID 조회 | [02_json_product_lookup.py](./exercises/02_json_product_lookup.py) | [정답](./solutions/02_json_product_lookup.py) |
| 03 | Excel 지역 목표 합계 | [03_excel_target_summary.py](./exercises/03_excel_target_summary.py) | [정답](./solutions/03_excel_target_summary.py) |
| 04 | SQLite 매개변수 조회 | [04_sql_parameter_query.py](./exercises/04_sql_parameter_query.py) | [정답](./solutions/04_sql_parameter_query.py) |
| 05 | CSV → JSON 변환 | [05_safe_json_export.py](./exercises/05_safe_json_export.py) | [정답](./solutions/05_safe_json_export.py) |

### ① Completed Orders — CSV

- **입력:** `data/orders.csv`
- **조건:** `completed`만 선택하고, 선행 0이 있는 지역 코드는 문자열로 보존
- **출력:** 완료 주문 건수와 `quantity × unit_price` 합계

```text
(10, 79200)
```

### ② Product Lookup — JSON

- **입력:** `data/products.json`
- **조건:** 상품 ID를 키, 카테고리를 값으로 하는 `dict` 생성
- **출력:** 총 4개 상품의 카테고리 조회 가능

```text
{'P01': '음료', 'P02': '문구', 'P03': '문구', 'P04': '생활'}
```

### ③ Region Targets — Excel

- **입력:** `data/regions.xlsx`의 `Targets` 시트
- **조건:** 지역 코드의 선행 0 보존, 목표 매출의 총합 계산

```text
75000
```

### ④ SQL Parameter Query — SQLite

- **입력:** `ST-01=22.5`, `ST-02=26.0`, `ST-03=20.5`
- **조건:** 온도가 `22.0` 이상인 센서를 `?` 매개변수로 조회하고 이름순 반환

```text
['ST-01', 'ST-02']
```

### ⑤ CSV → JSON Export

- **입력:** `data/orders.csv`
- **조건:** 완료 주문만 JSON으로 저장하고 다시 읽어서 항목 수 확인
- **추가 확인:** `region_code="01"`이 JSON에서도 문자열로 보존되는지 확인

```text
10
```

---

<a id="section-5-16"></a>
## 5.16. Quiz & Summary

### Quiz

**Q1.** 현재 작업 디렉터리에 따라 상대 경로의 실제 대상 파일이 달라질 수 있는 이유는 무엇인가요?

<details>
<summary>Q1. 정답 및 해설 확인</summary>

상대 경로는 현재 작업 디렉터리를 기준으로 해석되기 때문입니다. `Path(__file__).resolve()`를 기준으로 실습 데이터의 위치를 계산하면 실행 위치에 따른 차이를 줄일 수 있습니다.

</details>

**Q2.** CSV의 한 행에 `"sensor, A",23.5`가 있을 때, `split(",")`으로 처리하면 문제가 생길 수 있는 이유는 무엇인가요?

<details>
<summary>Q2. 정답 및 해설 확인</summary>

큰따옴표 내부의 쉼표는 필드 구분자가 아니기 때문입니다. 일반적인 CSV 파싱에는 `csv.reader()` 또는 `pd.read_csv()`처럼 인용부호 규칙을 처리하는 기능을 사용해야 합니다.

</details>

**Q3.** `"01"`과 같은 지역 코드를 `pd.read_csv()`로 읽을 때 문자열 `dtype`을 지정하는 이유는 무엇인가요?

<details>
<summary>Q3. 정답 및 해설 확인</summary>

숫자로 추론되면 선행 0이 제거되어 지역 코드의 원래 형태가 바뀔 수 있기 때문입니다. 코드·전화번호·상품 ID처럼 계산 대상이 아닌 식별자는 문자열로 처리하는 것이 적절합니다.

</details>

**Q4.** JSON 객체(Object)와 배열(Array)은 Python에서 각각 주로 어떤 자료구조로 변환되나요?

<details>
<summary>Q4. 정답 및 해설 확인</summary>

JSON Object는 `dict`, Array는 `list`로 변환됩니다. JSON의 `null`은 Python의 `None`에 해당합니다.

</details>

**Q5.** JSON Lines 파일을 일반 JSON 파일처럼 `json.load()`로 한 번에 읽으면 실패할 수 있는 이유는 무엇인가요?

<details>
<summary>Q5. 정답 및 해설 확인</summary>

JSON Lines는 각 줄이 독립적인 JSON 값이므로, 파일 전체가 하나의 JSON 값이라는 조건을 만족하지 않을 수 있습니다. 줄마다 `json.loads()`를 적용하거나 `pd.read_json(..., lines=True)`를 사용합니다.

</details>

**Q6.** Excel 파일에서 반드시 `Targets` 시트를 읽으려면 어떤 인수를 사용해야 하나요?

<details>
<summary>Q6. 정답 및 해설 확인</summary>

`pd.read_excel(path, sheet_name="Targets")`와 같이 `sheet_name`을 지정합니다. 특정 시트가 항상 첫 번째라고 가정하면 잘못된 데이터를 읽을 수 있습니다.

</details>

**Q7.** Parquet과 CSV의 핵심적인 저장 방식 차이는 무엇인가요?

<details>
<summary>Q7. 정답 및 해설 확인</summary>

CSV는 텍스트 기반의 행 중심 표현이고, Parquet은 열 기반의 바이너리 형식입니다. Parquet은 스키마 및 열 선택적 읽기를 지원할 수 있으며, Python에서 보통 `pyarrow` 엔진을 사용합니다.

</details>

**Q8.** SQLite에서 사용자가 제공한 문자열을 SQL 구문에 직접 붙이는 대신 `?`를 사용하는 이유는 무엇인가요?

<details>
<summary>Q8. 정답 및 해설 확인</summary>

SQL 값과 명령 구문을 분리하여 입력값이 SQL 문법으로 해석되는 위험을 줄이기 위해서입니다. `execute(query, (value,))` 형태로 매개변수를 전달합니다.

</details>

**Q9.** HTTP API 호출에 `timeout`과 응답 크기 제한을 설정하는 이유는 무엇인가요?

<details>
<summary>Q9. 정답 및 해설 확인</summary>

요청이 지나치게 오래 대기하거나 예상보다 큰 응답을 계속 받아 프로그램 자원을 소모하는 상황을 줄이기 위해서입니다. 두 제한만으로 API의 신뢰성이나 보안을 전부 보장하는 것은 아닙니다.

</details>

**Q10.** `os.replace()`를 통해 임시 파일을 교체하면 전원 장애가 발생해도 데이터가 반드시 보존되나요?

<details>
<summary>Q10. 정답 및 해설 확인</summary>

보장되지 않습니다. 원자적 교체와 저장장치에 실제로 기록되는 내구성은 다른 성질이며, 운영체제·파일 시스템·동기화 처리에 따라 달라집니다.

</details>

**Q11.** 파일을 열 수 없는 오류와 JSON 문법 오류를 구분하는 것이 중요한 이유는 무엇인가요?

<details>
<summary>Q11. 정답 및 해설 확인</summary>

문제의 원인과 해결 방법이 다르기 때문입니다. `FileNotFoundError`는 경로 확인, `JSONDecodeError`는 내용 형식 확인이 필요합니다. 모든 예외를 무시하면 원인을 파악하기 어렵습니다.

</details>

**Q12.** Chapter 05 Mini Project에서 원본 주문 12건 중 총매출 계산에 포함되는 주문은 몇 건이며, 그 이유는 무엇인가요?

<details>
<summary>Q12. 정답 및 해설 확인</summary>

**10건**입니다. 주문 상태가 `completed`인 주문만 매출 집계에 사용하고 `canceled`인 주문 2건은 제외하기 때문입니다. 완료 주문의 총매출은 **79,200원**입니다.

</details>

### Summary

- **`pathlib.Path`**: 운영체제에 맞는 파일 경로 구성과 파일·디렉터리 상태 확인
- **Text I/O**: 인코딩을 명시한 텍스트 읽기·쓰기, 작은 파일과 스트림 처리의 차이 이해
- **CSV**: 필드 구분, 인용부호 규칙, 문자열과 수치 데이터의 구별
- **Pandas I/O**: `read_csv()`와 `to_csv()`를 통한 DataFrame 입출력
- **JSON**: 중첩 객체·배열과 Python 사전·리스트 간 변환
- **JSON Lines**: 한 줄당 독립적인 JSON 데이터 처리
- **Excel**: `read_excel()`, `to_excel()`, 시트 선택 및 보존 범위의 한계
- **Parquet**: 열 기반 바이너리 저장, PyArrow 엔진 활용
- **SQLite**: SQL을 이용한 데이터 조회와 매개변수 바인딩
- **HTTP API**: JSON 응답 처리, 타임아웃·응답 크기·형식 검증
- **파일 선택**: 데이터 구조·스키마·교환 목적에 따라 적절한 형식 사용
- **데이터 보존**: 원본 입력과 결과 출력 분리, 저장 실패에 대비한 임시 파일 사용
- **오류 처리**: 파일 접근, 디코딩, 파싱, 스키마 오류의 단계별 구분

### References

- [Python — `pathlib`](https://docs.python.org/3/library/pathlib.html)
- [Python — `open()`](https://docs.python.org/3/library/functions.html#open)
- [Python — `csv`](https://docs.python.org/3/library/csv.html)
- [Python — `json`](https://docs.python.org/3/library/json.html)
- [Python — `sqlite3`](https://docs.python.org/3/library/sqlite3.html)
- [Python — `urllib.request`](https://docs.python.org/3/library/urllib.request.html)
- [Pandas — IO tools](https://pandas.pydata.org/docs/user_guide/io.html)
- [Pandas — `read_excel`](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)
- [Pandas — `read_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)
- [Apache Arrow — Python](https://arrow.apache.org/docs/python/)
- [Apache Parquet — Documentation](https://parquet.apache.org/docs/)
- [JSON Lines](https://jsonlines.org/)

---

[← Data Processing 목차](../README.md) · [Chapter 04 — Pandas & DataFrames](../Chapter-04/)
