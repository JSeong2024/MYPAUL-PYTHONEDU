# 자동화 프로그램의 개념과 원리

수업 준비물 신청서에 연필, 자, 지우개가 한 줄씩 적혀 있다고 생각해 봅시다. 신청이 다섯 건이라면 직접 세어도 됩니다. 신청이 수십 건이고 매주 같은 작업을 한다면, **신청 내역을 읽고, 항목 이름을 정리하고, 개수를 세어, 표로 저장하는 절차**를 코드로 만들 수 있습니다.

이 자료에서는 그 절차를 Python으로 구현합니다. 실습을 마친 뒤에는 파일 관리자 프로젝트에서 같은 방식으로 작업의 입력과 출력, 처리 규칙, 예외 상황을 스스로 정해 봅니다.

## 1. 들어가며

### 1.1 입력과 출력

도서관 대출 창구에 책과 대출증을 건네면 대출 기록이 남습니다. 건네는 정보가 **입력**, 처리 뒤에 얻는 기록이 **출력**입니다.

준비물 집계 프로그램의 입력은 신청 내역이고, 출력은 항목별 개수를 담은 표입니다. 함수에도 입력과 출력이 있습니다. 예를 들어 아래 함수는 입력받은 문자열의 앞뒤 공백과 대소문자를 정리한 뒤, 결과를 호출한 곳에 돌려줍니다.

```python
def normalize_item(text):
    return text.strip().lower()


item = normalize_item(" PENCIL ")
print(item)  # pencil
```

`print()`는 값을 화면에서 확인할 때 쓰고, `return`은 함수 밖에서 그 값을 이어서 쓸 수 있게 합니다.

### 1.2 파일 시스템과 경로

파일 시스템은 운영체제가 파일과 폴더를 저장하고 찾는 방식입니다. **절대 경로**는 드라이브나 파일 시스템의 시작점부터 위치를 나타냅니다. **상대 경로**는 정해 둔 기준 위치를 출발점으로 삼습니다. 예를 들어 `D:\수업`을 기준으로 `D:\수업\자료\안내.TXT`의 상대 경로는 `자료/안내.TXT`입니다.

다음 코드는 주어진 경로 하나에서 파일명과 확장자를 확인합니다. 지정한 파일이 실제로 없어도 경로의 구성 요소는 확인할 수 있습니다.

```python
from pathlib import Path

path = Path("자료/안내.TXT")
print(path.name)    # 안내.TXT
print(path.suffix)  # .TXT
```

`과학/발표.pdf`와 `동아리/발표.pdf`는 마지막 파일명이 같습니다. 파일 관리자에서 두 항목에 다른 메모를 붙이려면, 어떤 정보까지 있어야 두 파일을 구분할 수 있을지 생각해 보세요.

### 1.3 리스트와 딕셔너리

**리스트**는 여러 항목을 순서대로 모으는 데 사용합니다. **딕셔너리**는 키를 이용해 연결된 값을 찾는 데 사용합니다. 예를 들어 교구함 번호를 품목 이름으로 알아볼 수 있습니다.

```python
boxes = {"pencil": 2, "ruler": 5}
print(boxes.get("pencil", 0))  # 2
print(boxes.get("eraser", 0))  # 0
```

`get(키, 기본값)`은 키가 있으면 연결된 값을, 키가 없으면 기본값을 반환합니다. (`0`은 교구함 번호가 등록되지 않았다는 뜻입니다.) 집계 실습에서는 처음 보는 항목의 신청 건수를 0부터 시작하는 데 같은 방식으로 사용합니다.

### 1.4 라이브러리와 API

**라이브러리**는 여러 프로그램에서 재사용할 수 있도록 기능을 모아 둔 도구입니다. Python의 `csv` 모듈을 사용하면 각 칸의 값을 전달하는 것만으로 쉼표나 따옴표가 들어간 값도 형식에 맞춰 기록할 수 있습니다.

**API**는 그 도구에 일을 요청하는 약속입니다. 예를 들어 `writer.writerow(["품목", "신청 건수"])`는 CSV 작성기에 한 행을 기록해 달라는 요청입니다. 호출할 이름과 전달할 값, 결과를 사용하는 방법이 중요합니다. Python 모듈의 함수에도 API가 있고 인터넷 서비스에도 API가 있습니다.

### 1.5 예외 처리

절차가 올바르더라도 입력 파일이 없거나 결과 파일을 저장할 권한이 없을 수 있습니다. 이런 상황에서 어떤 안내를 보여줄지 정해 두면, 사용자가 다음 행동을 선택하기 쉽습니다.

`try`에는 예외가 발생할 수 있는 코드를 넣습니다. `except`에는 처리할 예외와 그때 할 일을 적습니다. `else`는 `try` 블록이 예외 없이 끝났을 때 실행합니다.

```python
text = input("신청 수량을 정수로 입력하세요. ")

try:
    count = int(text)
except ValueError:
    print("3과 같은 정수를 입력해 주세요.")
else:
    print(f"신청 수량은 {count}개입니다.")
```

`3`을 입력하면 `else`가 실행됩니다. `세 개`를 입력하면 `int(text)`에서 `ValueError`가 발생해 `except`가 실행됩니다.

파일 작업에서도 같은 흐름을 사용합니다. `"x"` 모드로 파일을 열면 새 파일을 만들고, 같은 이름의 파일이 이미 있을 때는 `FileExistsError`가 발생합니다.

```python
try:
    with open("practice_note.txt", "x", encoding="utf-8") as note:
        note.write("실습 결과를 확인했습니다.\n")
except FileExistsError:
    print("실습 기록이 이미 있습니다. 기존 내용을 유지합니다.")
else:
    print("새 실습 기록을 만들었습니다.")
```

`practice_note.txt`가 없는 폴더에서 두 번 실행해 보세요. 첫 번째에는 파일이 생성되고, 두 번째에는 기존 파일의 내용이 보존됩니다.

## 2. 자동화 프로그램이란 무엇인가?

**자동화 프로그램은 사람의 반복 작업을 정해 둔 조건과 규칙에 따라 수행하는 프로그램**입니다. 사용자가 버튼을 누르는 것도 시작 조건이 될 수 있습니다. 버튼을 한 번 누른 뒤 프로그램이 모든 신청 항목을 집계한다면, 사용자가 시작했어도 집계 자체는 자동화된 것입니다.

| 설계할 항목 | 준비물 신청 집계 예시 |
|---|---|
| **시작 조건** | 사용자가 터미널에서 집계 프로그램을 실행합니다. |
| **입력** | 한 줄에 한 건씩 적은 신청 내역입니다. |
| **규칙** | 공백만 있는 줄은 건너뜁니다. 앞뒤 공백과 영문 대소문자를 정리한 뒤 같은 품목으로 셉니다. |
| **출력** | 품목과 신청 건수가 적힌 CSV 보고서입니다. |
| **예외 상황** | 신청 파일을 읽을 수 없거나 같은 이름의 보고서가 이미 있을 때 안내합니다. |

자동화를 적용하면 입력이 늘어나도 같은 절차를 되풀이할 수 있고, 여러 번 실행해도 규칙이 일정하게 적용됩니다. 규칙에 실수가 있으면 그 실수도 여러 항목에 반복되므로, 작은 샘플로 정상 입력과 예외 입력을 함께 확인하는 것이 중요합니다.

### 일상과 실무에서의 활용

- **과제 제출 현황 확인** — 제출 목록과 학생 명단을 비교해 확인이 필요한 학생을 모읍니다.
- **일일 매출 집계** — 당일 거래 내역에서 지점별 합계를 계산해 보고서로 저장합니다.
- **파일 목록 갱신** — 사용자가 새로고침을 누르면 현재 폴더의 상태를 다시 확인합니다.

## 3. 실습 - 준비물 신청 내역 집계

### 3.1 준비

한 폴더에 `requests.txt`를 만들고 아래 내용을 UTF-8로 저장합니다. (빈 줄도 포함)

```text
Pencil
ruler
PENCIL

eraser
pencil
```

같은 폴더에 다음 코드를 `summarize_requests.py`로 저장합니다.

### 3.2 전체 코드

```python
import csv
from pathlib import Path


def count_requests(lines):
    counts = {}
    for line in lines:
        item = line.strip().lower()
        if not item:
            continue
        counts[item] = counts.get(item, 0) + 1
    return counts


def main():
    source = Path("requests.txt")
    report = Path("summary.csv")

    try:
        with source.open(encoding="utf-8-sig") as input_file:
            counts = count_requests(input_file)

        with report.open("x", encoding="utf-8-sig", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["품목", "신청 건수"])
            for item in sorted(counts):
                writer.writerow([item, counts[item]])

    except FileNotFoundError:
        print("requests.txt를 찾을 수 없습니다.")
    except FileExistsError:
        print("summary.csv가 이미 있습니다. 기존 보고서의 이름을 바꿔 주세요.")
    except UnicodeDecodeError:
        print("requests.txt를 UTF-8로 저장해 주세요.")
    except OSError as error:
        print(f"파일을 읽거나 저장할 수 없습니다. {error}")
    else:
        print(f"신청 {sum(counts.values())}건을 집계했습니다.")


if __name__ == "__main__":
    main()
```

### 3.3 코드가 실행되는 순서

1. **파일을 읽습니다.** `main()`에서 `requests.txt`를 엽니다. `with` 블록이 끝나면 파일이 닫힙니다.
2. **신청을 한 줄씩 셉니다.** `count_requests()`의 `strip()`은 줄바꿈과 앞뒤 공백을 없애고, `lower()`는 영문자를 소문자로 바꿉니다. 결과가 빈 문자열이면 `continue`로 건너뜁니다. `counts.get(item, 0) + 1`은 기존 건수에 1을 더합니다. 처음 나온 품목이라면 0에 1을 더합니다.
3. **결과를 표로 씁니다.** 집계 함수가 반환한 딕셔너리를 품목 이름순으로 기록합니다. `newline=""`을 지정해 CSV 모듈에 줄바꿈 처리를 맡깁니다. `"x"` 모드로 열기 때문에 같은 이름의 보고서가 있으면 그 파일이 보존됩니다.
4. **결과를 알립니다.** 입력 파일 없음, 보고서 이름 충돌, 문자 인코딩 문제에 각각 맞는 안내를 표시합니다. `FileNotFoundError`와 `FileExistsError`는 `OSError`의 하위 유형이므로 구체적인 예외를 앞에 둡니다. 읽기와 저장이 예외 없이 끝나면 `else`에서 전체 신청 건수를 표시합니다.

#### 함수 정의와 직접 실행

`def main():`은 실행 절차를 이름 붙여 정의합니다. `main()`을 호출할 때 함수 안의 작업이 실행됩니다. `python summarize_requests.py`로 직접 실행하면, 맨 아래에 `main()`만 써도 같은 결과가 나옵니다. 이 예제에서는 다른 파일에서도 `count_requests()`를 가져다 쓸 수 있도록 직접 실행 여부를 확인하는 조건을 붙입니다.

| 파일 끝의 코드 | 직접 실행 | 다른 파일에서 처음 불러오기 |
|---|---|---|
| `if __name__ == "__main__":` 아래에 `main()` | 집계 보고서를 만듭니다. | 집계 함수를 가져다 쓸 수 있고 보고서 작성은 시작되지 않습니다. |
| 들여쓰기 없이 `main()` | 집계 보고서를 만듭니다. | 불러오는 과정에서도 집계 보고서 작성을 시작합니다. |
| 함수 정의까지만 작성 | 함수를 정의합니다. | 가져온 함수는 호출할 때 실행됩니다. |

같은 폴더에서 `python -c "from summarize_requests import count_requests; print(count_requests(['Pencil', 'PENCIL']))"`를 실행해 보세요. `{'pencil': 2}`가 출력됩니다. `summary.csv`가 없는 상태에서 확인하면, 함수를 불러오는 과정에서는 보고서가 생성되지 않는다는 점도 볼 수 있습니다.

### 3.4 결과와 예외 확인하기

터미널에서 두 파일이 있는 폴더로 이동한 뒤 `python summarize_requests.py`를 실행합니다. Windows에서 Python 실행 명령이 `py`라면 `py summarize_requests.py`를 사용합니다. 정상적으로 실행되면 `신청 5건을 집계했습니다.`가 표시됩니다.

| 품목 | 신청 건수 |
|---|---:|
| eraser | 1 |
| pencil | 3 |
| ruler | 1 |

보고서를 그대로 두고 다시 실행하여 기존 파일이 보존되는지 확인하세요. 다음으로 `requests.txt`의 이름을 잠시 바꾸고 실행해 입력 파일이 없을 때의 안내를 확인하세요.

## 4. 핵심 요약

- 자동화할 일을 정할 때는 **시작 조건, 입력, 처리 규칙, 출력, 예외 상황**을 먼저 정합니다.
- 처리 함수가 값을 반환하면 호출하는 쪽에서 결과를 화면에 표시하거나 파일로 저장할 수 있습니다.
- 규칙을 작성한 뒤에는 정상 입력뿐 아니라 빈 입력과 누락된 입력도 확인합니다.
- 파일 관리자 프로젝트에서는 같은 이름을 가진 항목을 어떻게 구별할지, 분류에 적용할 조건은 무엇인지, 재실행 후 어떤 정보가 남아야 하는지 먼저 적어 봅니다.

## 5. 연습 문제

### 문제 1.
다음 중 준비물 신청 집계를 자동화한 사례로 가장 적절한 것을 고르세요.

A. 사람이 신청서를 한 줄씩 직접 세어 결과를 기록합니다.  
B. 사용자가 실행 버튼을 누르면 프로그램이 신청 건수를 세어 표에 저장합니다.  
C. 화면에 있는 집계 버튼을 누르면 기능에 대한 설명 문장만 나타납니다.  
D. 사람이 건수를 모두 계산한 뒤, 프로그램에 입력해 그 값을 그대로 보여줍니다.

### 문제 2.
체육관에 동명이인인 두 학생이 있습니다. 출석 기록 딕셔너리의 키(Key)로 이름만 사용하면 어떤 문제가 발생하나요? 또한, 두 학생을 구분할 수 있는 방법 한 가지를 서술하세요.

### 문제 3.
입력된 품목 이름을 소문자로 변환하고, 표에 해당 품목이 없으면 0을 반환하도록 빈칸 두 곳을 채우세요. 코드를 실행했을 때의 출력 결과도 함께 적어 보세요.

```python
stock = {"pencil": 12, "ruler": 5}
item = "PENCIL".____()
print(stock.____(item, 0))
```

### 문제 4.
준비물의 기본 배부량은 1개이며, 개별 수량이 지정된 학생에게는 지정된 수량을 배부합니다. 다음 코드를 실행했을 때 출력되는 세 줄을 순서대로 쓰세요.

```python
default_amount = 1
special_amounts = {"민지": 3}
students = ["민지", "지우", "하나"]

for student in students:
    print(student, special_amounts.get(student, default_amount))
```

### 문제 5. 미니 프로젝트 — 과제 미제출자 확인

과제 제출 기록을 분석해 **아직 과제를 제출하지 않은 학생의 학번**을 출력하는 프로그램을 완성하세요. 같은 학생이 과제를 여러 번 중복 제출할 수 있으며, 제출 기록에는 불필요한 공백이나 대소문자가 섞여 있을 수 있습니다.

#### 구현 조건

1. 제출 기록의 앞뒤 공백을 제거하고 영문을 모두 대문자로 통일합니다. 공백만 들어 있는 빈 기록이나 학생 명단에 없는 학번은 제외합니다.
2. 같은 학생이 여러 번 제출했더라도 한 명으로만 집계합니다.
3. 미제출자 목록은 **전체 학생 명단(`roster`)에 적힌 순서**대로 반환해야 합니다.
4. 학생 명단의 학번은 중복되지 않으며, 이미 대문자로 깔끔하게 정리되어 있다고 가정합니다.

#### 시작 코드

```python
def valid_submissions(roster, records):
    # TODO 1. 유효한 제출자 학번을 중복 없이 모아 반환합니다.
    raise NotImplementedError


def find_missing(roster, submitted):
    # TODO 2. 학생 명단 순서대로 미제출자 학번을 모아 반환합니다.
    raise NotImplementedError


def main():
    roster = ["S101", "S102", "S103", "S104", "S105"]
    records = [" s103 ", "S103", "", "s101", "S999", "  "]

    submitted = valid_submissions(roster, records)
    missing = find_missing(roster, submitted)

    print(f"제출 {len(submitted)}명 / 전체 {len(roster)}명")
    print("미제출:", ", ".join(missing) if missing else "없음")


if __name__ == "__main__":
    main()
```

#### 예상 출력

```text
제출 2명 / 전체 5명
미제출: S102, S104, S105
```

> **추가 확인:** `records`를 빈 리스트(`[]`)로 바꾸었을 때 모든 학생이 미제출자로 출력되는지 확인해 보세요. 반대로 모든 학생이 한 번 이상 제출한 경우에는 `미제출: 없음`이 출력되어야 합니다.

### 문제 6. 미니 프로젝트 — 실습실 교구 대여 보고서

실습실의 대여·반납 기록을 **입력된 순서대로** 처리하고, 품목별 최종 대여 가능 수량을 CSV 파일로 저장하는 프로그램을 완성하세요. 조건에 맞지 않아 처리할 수 없는 기록은 제외 사유를 남기고 다음 기록을 이어서 확인합니다.

#### 구현 조건

1. 각 기록은 `(품목, 동작, 수량)` 형태의 튜플로 주어집니다. 품목이 초기 재고에 등록되어 있고, 동작이 `"대여"` 또는 `"반납"`이며, 수량이 양의 정수(`int`)일 때만 유효한 기록으로 처리합니다. 
   - 유효성 검사에서 여러 조건을 동시에 위반한 경우 **품목 → 동작 → 수량** 순서대로 가장 먼저 발견된 사유 하나만 기록합니다. (`등록되지 않은 품목`, `알 수 없는 동작`, `잘못된 수량`)
2. **대여** 시에는 현재 재고에서 수량을 뺍니다. 대여 수량이 현재 재고보다 많으면 `재고 부족`으로 처리합니다.
3. **반납** 시에는 현재 재고에 수량을 더합니다. 반납 후 수량이 초기 재고를 넘어서면 `초기 재고 초과`로 처리합니다.
4. 처리하지 못한 기록은 재고에 반영하지 않고, **`(기록 번호, 이유)`** 형태로 모아서 반환합니다. 기록 번호는 `1`부터 시작합니다.
5. `equipment_report.csv` 파일에 품목명 오름차순으로 `품목,대여 가능 수량`을 저장합니다. 기존 보고서 파일이 이미 있다면 덮어쓰지 않고 유지하며 안내 메시지를 출력합니다. 원본인 초기 재고 딕셔너리(`initial_stock`) 역시 수정되지 않고 그대로 유지되어야 합니다.

#### 시작 코드

```python
import csv
from pathlib import Path


def apply_records(initial_stock, records):
    stock = initial_stock.copy()
    rejected = []
    # TODO 1. 기록을 순서대로 검사하고, 처리 가능한 기록만 재고에 반영합니다.
    # rejected에는 (기록 번호, 이유) 형태로 추가합니다.
    raise NotImplementedError
    return stock, rejected


def save_report(path, stock):
    # TODO 2. 기존 보고서를 보존하는 모드로 열고 제목 행과 재고를 기록합니다.
    raise NotImplementedError


def main():
    initial_stock = {"자": 3, "가위": 4}
    records = [
        ("가위", "대여", 2),
        ("자", "대여", 4),
        ("가위", "반납", 1),
        ("풀", "대여", 1),
        ("자", "반납", 1),
        ("자", "예약", 1),
        ("가위", "대여", 0),
        ("자", "대여", 1),
    ]

    stock, rejected = apply_records(initial_stock, records)
    for number, reason in rejected:
        print(f"{number}번 기록 제외: {reason}")

    try:
        save_report(Path("equipment_report.csv"), stock)
    except FileExistsError:
        print("보고서가 이미 있습니다. 기존 파일을 유지합니다.")
    except OSError as error:
        print(f"보고서를 저장할 수 없습니다. {error}")
    else:
        print("교구 대여 보고서를 저장했습니다.")


if __name__ == "__main__":
    main()
```

#### 예상 출력

```text
2번 기록 제외: 재고 부족
4번 기록 제외: 등록되지 않은 품목
5번 기록 제외: 초기 재고 초과
6번 기록 제외: 알 수 없는 동작
7번 기록 제외: 잘못된 수량
교구 대여 보고서를 저장했습니다.
```

생성된 `equipment_report.csv` 파일에는 다음과 같은 내용이 저장됩니다.

```csv
품목,대여 가능 수량
가위,3
자,2
```

> **추가 확인:** 생성된 보고서 파일을 지우지 않은 상태에서 프로그램을 한 번 더 실행해 기존 파일이 안전하게 보존되는지 확인해 보세요. 또한, 첫 번째 대여 기록보다 반납 기록이 먼저 들어왔을 때 어떤 결과가 나올지 예상해 보세요.

## 6. 정답 및 해설

### 문제 1.

<details>
<summary>정답 및 해설 보기</summary>

**정답: B**

버튼은 프로그램이 작업을 시작하도록 하는 실행 조건입니다. B는 사용자가 버튼을 누른 뒤, 프로그램이 직접 건수를 세고 표에 저장까지 수행하므로 자동화된 사례에 해당합니다. 반면, A와 D는 집계 과정을 사람이 직접 처리하며, C는 버튼이 있지만 실제 집계 기능은 동작하지 않습니다.

</details>

### 문제 2.

<details>
<summary>정답 및 해설 보기</summary>

**정답 예시: 같은 키(Key)로 데이터를 저장하면 기존의 출석 기록이 덮어씌워집니다.**

딕셔너리는 키의 중복을 허용하지 않으므로, 이름이 같은 두 학생의 기록을 저장할 때 먼저 입력된 학생의 정보가 사라지게 됩니다. 학생마다 고유하게 부여되는 **학번**이나 **회원 번호** 등을 키로 사용하면 동명이인도 각각 구분하여 정확히 기록할 수 있습니다.

</details>

### 문제 3.

<details>
<summary>정답 및 해설 보기</summary>

**정답: `lower`, `get` / 출력 결과: `12`**

`"PENCIL".lower()`는 문자열을 모두 소문자로 변환하여 `"pencil"`을 만듭니다. 변환된 `"pencil"`은 `stock` 딕셔너리에 존재하는 키이므로, `get()` 메서드를 통해 해당 값인 `12`가 출력됩니다. 만약 소문자로 변환하지 않은 `"PENCIL"`을 그대로 찾았다면, 일치하는 키가 없어 기본값으로 지정한 `0`을 반환했을 것입니다.

</details>

### 문제 4.

<details>
<summary>정답 및 해설 보기</summary>

**정답(출력 결과):**

```text
민지 3
지우 1
하나 1
```

`get(키, 기본값)` 메서드는 첫 번째 인수로 전달된 키를 딕셔너리에서 찾고, 해당 키가 없으면 두 번째 인수로 지정한 기본값을 반환합니다. 따라서 `special_amounts`에 등록된 `"민지"`는 지정된 값인 `3`을 출력하고, 등록되지 않은 `"지우"`와 `"하나"`는 기본값인 `1`을 출력합니다.

</details>

### 문제 5. 과제 미제출자 확인

<details>
<summary>해설과 예시 코드 보기</summary>

**핵심 전략: 제출 기록 정리와 미제출자 판별 과정을 나누어 처리합니다.**  
제출 기록을 가공하지 않고 원래 표기 그대로 명단에서 찾으면, `" s103 "`처럼 앞뒤 공백이나 소문자가 섞인 학번을 누락할 수 있습니다. 따라서 공백을 제거하고 대문자로 통일한 뒤 명단과 대조해야 합니다.

```python
def valid_submissions(roster, records):
    submitted = []
    for record in records:
        student_id = record.strip().upper()
        if student_id in roster and student_id not in submitted:
            submitted.append(student_id)
    return submitted


def find_missing(roster, submitted):
    missing = []
    for student_id in roster:
        if student_id not in submitted:
            missing.append(student_id)
    return missing
```

- **중복 및 유효하지 않은 기록 제외:** 예제에서 첫 두 기록은 정리하면 모두 `S103`이 되므로 한 번만 추가합니다. 명단에 없는 `S999`와 빈 문자열 기록은 명단 조회 조건(`student_id in roster`)에서 자연스럽게 걸러집니다.
- **원래 순서 유지:** 미제출자 목록은 제출 기록이 아닌 **전체 학생 명단(`roster`)을 처음부터 순회**하며 만들기 때문에 기존 명단의 순서가 그대로 유지됩니다.

</details>

### 문제 6. 실습실 교구 대여 보고서

<details>
<summary>해설과 예시 코드 보기</summary>

**핵심 전략: 기록의 유효성을 먼저 검증한 뒤 재고에 반영합니다.**  
검증 없이 재고부터 수정하면 잘못된 대여 기록이 이후의 정상 기록 처리에도 연쇄적인 오류를 일으킵니다. 각 기록의 형식이 올바른지, 그리고 계산된 수량이 `0`과 초기 재고 사이에 있는지 모두 확인한 뒤 안전하게 반영해야 합니다.

아래 두 함수를 시작 코드의 `TODO` 자리에 넣어 동작을 확인할 수 있습니다.

```python
def apply_records(initial_stock, records):
    stock = initial_stock.copy()
    rejected = []

    for number, (item, action, amount) in enumerate(records, start=1):
        if item not in stock:
            rejected.append((number, "등록되지 않은 품목"))
            continue
        if action not in ("대여", "반납"):
            rejected.append((number, "알 수 없는 동작"))
            continue
        if type(amount) is not int or amount <= 0:
            rejected.append((number, "잘못된 수량"))
            continue

        if action == "대여":
            next_stock = stock[item] - amount
        else:
            next_stock = stock[item] + amount

        if next_stock < 0:
            rejected.append((number, "재고 부족"))
        elif next_stock > initial_stock[item]:
            rejected.append((number, "초기 재고 초과"))
        else:
            stock[item] = next_stock

    return stock, rejected


def save_report(path, stock):
    with path.open("x", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["품목", "대여 가능 수량"])
        for item in sorted(stock):
            writer.writerow([item, stock[item]])
```

- **1번과 3번 기록 (정상 처리):** 가위 재고는 `4개`에서 `2개`로 줄었다가 반납을 거쳐 `3개`가 됩니다. 만약 반납이 대여보다 먼저 들어왔다면 이미 초기 재고인 `4개`에 도달한 상태이므로 해당 반납 기록은 제외됩니다.
- **2번과 5번 기록 (제외 처리):** **2번**은 자 `4개`를 대여하려 하지만 현재 재고가 `3개`뿐이라 제외됩니다. 이 대여가 무효 처리되었기 때문에, 이어지는 **5번**에서 자를 반납하면 초기 재고를 초과하게 되어 함께 제외됩니다. 두 기록 모두 반영되지 않으므로 8번 대여 전까지 자의 재고는 `3개`로 유지됩니다.
- **주요 메서드 활용:** `enumerate(..., start=1)`을 사용해 기록 번호를 1번부터 매겼습니다. 또한 `copy()`로 작업용 재고 딕셔너리를 분리하여, 원본인 `initial_stock`이 반납 한도를 판단하는 기준값으로 안전하게 유지되도록 했습니다.
- **안전한 파일 저장:** 파일을 `"x"` 모드로 열면 같은 이름의 파일이 이미 있을 때 덮어쓰지 않고 오류를 발생시킵니다. 파일이 이미 존재할 때의 예외 처리는 시작 코드의 `main()` 함수에서 안내하도록 구성되어 있습니다.

</details>

## 7. 더 읽어보기

- 경로를 다루는 방법은 [Python 공식 문서 · pathlib](https://docs.python.org/ko/3/library/pathlib.html)을 참고하세요.
- 표를 읽고 쓰는 방법은 [Python 공식 문서 · csv](https://docs.python.org/ko/3.13/library/csv.html)를 참고하세요.
- `try`, `except`, `else`의 동작은 [Python 공식 자습서 · 에러와 예외](https://docs.python.org/ko/3.13/tutorial/errors.html)를 참고하세요.
