# 자동화 프로그램의 개념과 원리

수업 준비물 신청서에 연필, 자, 지우개 같은 품목이 한 줄씩 적혀 있다고 생각해 봅시다. 신청이 다섯 건 정도라면 사람이 직접 세어도 충분합니다. 하지만 신청이 수십 건에 달하고 매주 같은 작업을 반복해야 한다면 어떨까요? 이때는 **신청 내역을 읽고, 항목 이름을 정리하고, 개수를 세어 표로 저장하는 일련의 절차**를 코드로 만들어 자동화할 수 있습니다.

이 자료에서는 이러한 자동화 절차를 Python으로 직접 구현해 봅니다. 실습을 마친 뒤에는 이어지는 파일 관리자 프로젝트에서 작업의 입력과 출력, 처리 규칙, 예외 상황을 스스로 설계해 보게 됩니다.

## 1. 알아둘 개념

### 1.1 사용자 정의 함수 (User-Defined Function, UDF)

함수는 특정 작업을 수행하는 코드의 묶음입니다. Python에서 기본으로 제공하는 `print()`, `len()` 같은 내장 함수 외에도 `def` 키워드를 사용해 필요한 함수를 직접 정의할 수 있습니다.

도서관 대출 창구에 책과 대출증을 건네면 전산에 대출 기록이 남습니다. 이때 건네는 정보가 **입력(Input)** 이고, 처리를 거쳐 얻는 결과가 **출력(Output)** 입니다. 함수 역시 외부에서 필요한 값을 전달받고, 내부 처리를 거친 결과를 다시 돌려줄 수 있습니다.

```python
def normalize_item(text):
    return text.strip().lower()


item = normalize_item(" PENCIL ")
print(item)  # pencil
```

위 코드에서 `text`는 함수가 전달받는 값을 저장하는 **매개변수(Parameter)** 이며, `" PENCIL "`은 함수를 호출할 때 실제로 전달하는 **인수(Argument)** 입니다. 함수 내부에서는 `strip()`으로 앞뒤 공백을 제거하고, `lower()`로 영문자를 모두 소문자로 변환합니다.

`return`은 처리 결과를 함수를 호출한 곳으로 돌려주면서 함수의 실행을 즉시 종료합니다. 반면 `print()`는 값을 화면에 출력해 보여줄 뿐, 그 값을 호출한 곳에 반환하지는 않습니다. 만약 `return`으로 반환값을 따로 지정하지 않으면 함수는 기본적으로 `None`을 반환합니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">구분</th>
<th align="center" style="text-align: center;">역할</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>def</code></td>
<td align="center" style="text-align: center;">새로운 함수 정의</td>
</tr>
<tr>
<td align="center" style="text-align: center;">매개변수</td>
<td align="center" style="text-align: center;">함수가 전달받을 입력값 지정</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>return</code></td>
<td align="center" style="text-align: center;">처리 결과를 호출한 곳으로 반환</td>
</tr>
<tr>
<td align="center" style="text-align: center;">함수 호출</td>
<td align="center" style="text-align: center;">정의된 함수를 실제로 실행</td>
</tr>
</tbody>
</table>

데이터를 계산·처리하는 함수와 결과를 화면에 출력하는 부분을 분리하면, 같은 처리 기능을 프로그램의 여러 곳에서 손쉽게 재사용할 수 있습니다. 다음은 계산 결과를 변수에 저장한 뒤 출력하는 예제입니다.

```python
def calculate_total(price, quantity):
    return price * quantity


amount = calculate_total(1500, 3)
print(amount)  # 4500
```

> **주의:** 함수를 `def`로 정의하는 것만으로는 함수 내부의 코드가 실행되지 않습니다. 반드시 `calculate_total(1500, 3)`처럼 **함수를 호출**해야 내부 코드가 동작합니다.

### 1.2 자료구조 (Data Structures)

자동화 프로그램에서는 여러 데이터를 저장하고, 검색하거나 수정하는 작업이 반복됩니다. 따라서 데이터의 형태와 처리 목적에 맞는 자료구조를 선택하는 것이 중요합니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">자료구조</th>
<th align="center" style="text-align: center;">특징</th>
<th align="center" style="text-align: center;">주요 활용 사례</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><strong>리스트 (List)</strong></td>
<td align="center" style="text-align: center;">순서가 있으며, 요소를 추가하거나 수정할 수 있음</td>
<td align="center" style="text-align: center;">학생 명단, 측정값 목록</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>딕셔너리 (Dictionary)</strong></td>
<td align="center" style="text-align: center;">고유한 키(Key)와 값(Value)의 쌍으로 데이터를 관리함</td>
<td align="center" style="text-align: center;">상품별 가격, 학번별 점수</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>튜플 (Tuple)</strong></td>
<td align="center" style="text-align: center;">순서가 있으며, 생성 이후 요소를 추가·삭제하거나 다른 값으로 교체할 수 없음</td>
<td align="center" style="text-align: center;">좌표, 날짜, 개별 거래 기록</td>
</tr>
</tbody>
</table>

#### 리스트 (List)

리스트는 여러 값을 순서대로 나열하여 저장합니다. 요소의 위치를 나타내는 인덱스는 `0`부터 시작하며, `append()` 메서드로 맨 뒤에 새 항목을 추가할 수 있습니다.

```python
students = ["민지", "지우", "하나"]
students.append("서준")

print(students[0])         # 민지
print(len(students))      # 4
print("지우" in students)  # True
```

`in` 연산자를 사용하면 리스트 안에 특정 값이 포함되어 있는지 확인할 수 있습니다. 또한 리스트에는 동일한 값이 중복되어 여러 번 저장될 수 있습니다.

#### 딕셔너리 (Dictionary)

딕셔너리는 고유한 **키(Key)** 를 이용해 연결된 **값(Value)** 을 빠르게 조회하거나 수정합니다. **이미 존재하는 키에 새로운 값을 대입하면 기존 값이 덮어씌워집니다.**

```python
boxes = {"pencil": 2, "ruler": 5}
print(boxes.get("pencil", 0))  # 2
print(boxes.get("eraser", 0))  # 0

boxes["ruler"] = 7
boxes["eraser"] = 3
print(boxes["ruler"])  # 7
```

`get(키, 기본값)` 메서드는 키가 존재하면 해당 값을 반환하고, 존재하지 않으면 지정한 기본값을 반환합니다. 만약 `boxes["eraser"]`처럼 대괄호(`[]`)로 존재하지 않는 키에 직접 접근하면 `KeyError` 예외가 발생합니다. (위 예제에서는 `boxes["eraser"] = 3`으로 키와 값을 새로 추가했습니다.)

딕셔너리에서도 `in` 연산자로 특정 키가 있는지 검사할 수 있으며, `items()` 메서드를 사용하면 키와 값을 한 쌍씩 꺼내어 함께 순회할 수 있습니다. `keys()`는 키들을 나타내는 뷰(view)를 반환합니다. 두 딕셔너리의 `keys()`를 비교하면 키의 순서와 관계없이 같은 키로 구성되어 있는지 확인할 수 있습니다.

```python
scores = {"S101": 85, "S102": 92}
for student_id, score in scores.items():
    print(student_id, score)
```

딕셔너리를 다른 변수에 그대로 대입(`working = original`)하면 두 변수가 같은 데이터를 공유하게 됩니다. 원본을 유지한 채 작업하려면 `copy()` 메서드로 별도의 복사본을 만들어야 합니다. 다음은 값이 정수로 이루어진 딕셔너리에서 복사본을 수정해도 원본이 바뀌지 않는 예제입니다.

```python
original = {"연필": 10, "자": 5}
working = original.copy()
working["연필"] = 8

print(original["연필"])  # 10
print(working["연필"])   # 8
```

> **참고:** `copy()`는 얕은 복사(Shallow Copy)를 수행합니다. 딕셔너리의 값으로 리스트나 다른 딕셔너리 같은 변경 가능한 객체가 저장되어 있다면, 원본과 복사본은 해당 내부 객체를 공유합니다.

#### 튜플 (Tuple)

튜플은 여러 값을 하나의 순서 있는 데이터 묶음으로 표현할 때 사용합니다. 리스트와 달리 한 번 생성한 뒤에는 인덱스로 특정 요소를 수정하거나 교체할 수 없습니다. 프로그램 실행 중에 요소의 구성이 바뀌면 안 되는 데이터 묶음을 다룰 때 유용합니다. 단, 튜플의 요소가 리스트처럼 변경 가능한 객체라면 그 객체의 내부 값은 수정할 수 있습니다.

```python
record = ("가위", "대여", 2)
item, action, quantity = record

print(item)      # 가위
print(action)    # 대여
print(quantity)  # 2
```

위 코드처럼 튜플의 각 요소를 여러 변수에 한 번에 나누어 대입하는 방식을 **언패킹(Unpacking)** 이라고 합니다. 또한, 여러 개의 튜플을 리스트 안에 담아 일련의 기록 목록을 구성할 수도 있습니다.

```python
measurements = [("월요일", 21), ("화요일", 23)]

for number, (day, temperature) in enumerate(measurements, start=1):
    print(number, day, temperature)
```

```text
1 월요일 21
2 화요일 23
```

`enumerate()` 함수를 사용하면 데이터를 순회할 때 항목과 함께 번호(인덱스)를 동시에 얻을 수 있습니다. `start=1`을 지정하면 번호가 `0`이 아닌 `1`부터 시작합니다.

#### 문자열 비교와 조건에 따른 데이터 선택

입력 데이터에 불필요한 공백이나 대소문자 차이가 섞여 있으면, 실제로는 같은 값이라도 프로그램이 서로 다른 데이터로 인식할 수 있습니다. 데이터를 비교하거나 집계하기 전에 표기 형식을 일정하게 통일하는 작업을 **데이터 정규화(Data Normalization)** 라고 합니다.

```python
text = "  Python Basics  "
print(text.strip())          # Python Basics
print(text.strip().lower())  # python basics
print(text.strip().upper())  # PYTHON BASICS
```

문자열을 비교할 때 `in` 연산자는 특정 문구가 포함되어 있는지(부분 일치)를 확인하며, `==` 연산자는 두 문자열이 정확히 같은지(완전 일치)를 비교합니다.

```python
title = "Python Basics"
print("python" in title.lower())   # True
print(title.lower() == "python")  # False
```

전체 데이터에서 특정 조건을 만족하는 항목만 골라내는 작업을 **필터링(Filtering)** 이라고 합니다.

```python
temperatures = [18, 24, 20, 27]
selected = []

for value in temperatures:
    if value >= 24:
        selected.append(value)

print(selected)  # [24, 27]
```

데이터를 순서대로 정렬할 때는 `sorted()` 함수를 사용합니다. `sorted()`는 원본 데이터를 직접 바꾸지 않고, 정렬된 새로운 리스트를 반환합니다. 딕셔너리를 전달하면 키(Key)를 기준으로 정렬한 리스트를 돌려줍니다.

```python
stock = {"자": 3, "가위": 4, "풀": 2}
print(sorted(stock))  # ['가위', '자', '풀']
```

### 1.3 파일 시스템과 경로 (File System & Path)

파일 시스템은 운영체제가 파일과 폴더(디렉터리)를 저장하고 관리하는 체계입니다. 파일이나 폴더가 저장된 위치는 **경로(Path)** 로 나타냅니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">구분</th>
<th align="center" style="text-align: center;">설명</th>
<th align="center" style="text-align: center;">예시 (Windows)</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><strong>절대 경로 (Absolute Path)</strong></td>
<td align="center" style="text-align: center;">파일 시스템의 최상위 기준점(루트)부터 전체 위치를 나타낸 경로</td>
<td align="center" style="text-align: center;"><code>D:\수업\자료\안내.TXT</code></td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>상대 경로 (Relative Path)</strong></td>
<td align="center" style="text-align: center;">현재 작업 디렉터리 등 특정 기준 위치를 출발점으로 삼은 경로</td>
<td align="center" style="text-align: center;"><code>자료/안내.TXT</code></td>
</tr>
</tbody>
</table>

Python 표준 라이브러리인 `pathlib` 모듈을 사용하면 경로 문자열을 객체로 다루면서 파일명이나 확장자 등을 손쉽게 추출할 수 있습니다.

```python
from pathlib import Path

path = Path("자료/안내.TXT")
print(path.name)    # 안내.TXT
print(path.stem)    # 안내
print(path.suffix)  # .TXT
print(path.parent)  # 자료
```

경로의 이름이나 확장자 같은 구성 요소를 확인하는 작업은 실제 파일이 컴퓨터에 존재하지 않아도 동작합니다. 파일이나 폴더가 실제로 있는지 확인하려면 별도의 메서드를 사용해야 합니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">속성 및 메서드</th>
<th align="center" style="text-align: center;">역할</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>name</code>, <code>stem</code>, <code>suffix</code></td>
<td align="center" style="text-align: center;">전체 파일명, 확장자를 제외한 파일명, 마지막 확장자 확인</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>parent</code></td>
<td align="center" style="text-align: center;">현재 경로의 바로 위 상위 폴더 경로 반환</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>exists()</code></td>
<td align="center" style="text-align: center;">해당 경로에 실제 파일이나 폴더가 존재하는지 확인</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>is_file()</code></td>
<td align="center" style="text-align: center;">해당 경로가 일반 파일인지 확인</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>is_dir()</code></td>
<td align="center" style="text-align: center;">해당 경로가 폴더(디렉터리)인지 확인</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>Path.cwd()</code></td>
<td align="center" style="text-align: center;">현재 작업 디렉터리(Current Working Directory) 경로 반환</td>
</tr>
</tbody>
</table>

`Path("자료") / "안내.TXT"`처럼 슬래시(`/`) 연산자를 사용하면 운영체제에 구애받지 않고 경로를 직관적으로 결합할 수 있습니다. 상대 경로는 기본적으로 프로그램을 실행한 위치인 **현재 작업 디렉터리**를 기준으로 해석됩니다. 따라서 작성 중인 `.py` 소스 파일이 저장된 폴더와 프로그램이 실행되는 현재 작업 디렉터리가 항상 일치하는 것은 아니라는 점에 유의해야 합니다.

> **생각해 보기:** `과학/발표.pdf`와 `동아리/발표.pdf`는 마지막 파일명이 모두 `발표.pdf`로 같습니다. 파일 관리자 프로그램에서 두 파일을 서로 다른 항목으로 구분하려면 파일명 외에 어떤 정보가 추가로 필요할까요?

### 1.4 파일 입출력 (File I/O)

리스트나 딕셔너리에 저장한 데이터는 메모리에서만 유지되므로, 프로그램이 종료되면 모두 사라집니다. 프로그램을 다시 실행했을 때도 데이터를 보존하여 활용하려면 파일 같은 영구 저장 매체에 기록해야 합니다.

#### 파일 열기와 닫기

`open()` 함수는 지정한 경로의 파일을 열고, 설정한 모드에 따라 데이터를 읽거나 기록할 수 있는 파일 객체를 반환합니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">모드</th>
<th align="center" style="text-align: center;">동작 설명</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>r</code></td>
<td align="center" style="text-align: center;"><strong>읽기:</strong> 기존 파일의 내용을 읽습니다. 파일이 없으면 예외(<code>FileNotFoundError</code>)가 발생합니다.</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>w</code></td>
<td align="center" style="text-align: center;"><strong>쓰기:</strong> 새 파일을 만들어 기록합니다. 같은 이름의 파일이 이미 있으면 <strong>기존 내용을 모두 지우고</strong> 새로 기록합니다.</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>a</code></td>
<td align="center" style="text-align: center;"><strong>추가 쓰기:</strong> 기존 파일 내용의 맨 끝에 새로운 내용을 이어 붙입니다. 파일이 없으면 새로 생성합니다.</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>x</code></td>
<td align="center" style="text-align: center;"><strong>새 파일 생성:</strong> 새 파일을 만들어 기록합니다. 같은 이름의 파일이 이미 있으면 덮어쓰지 않고 예외(<code>FileExistsError</code>)가 발생합니다.</td>
</tr>
</tbody>
</table>

`with` 구문을 사용하면 코드 블록의 실행이 끝날 때 파일이 자동으로 닫힙니다. 또한 텍스트 파일을 다룰 때는 `encoding="utf-8"`처럼 인코딩 방식을 명확히 지정해 두는 것이 운영체제 간 글자 깨짐 현상을 예방하는 좋은 습관입니다.

> 아래의 TXT, CSV, JSON 예제는 실행 시 각각 실습용 파일을 생성합니다. 기존 문서와 섞이지 않도록 빈 실습 폴더에서 실행해 보세요. 특히 **`w` 모드는 같은 이름의 파일이 있을 때 기존 내용을 즉시 삭제**하므로, 실제 데이터를 다룰 때는 **파일명과 저장 위치를 반드시 먼저 확인**해야 합니다.

#### TXT (Text File)

TXT는 서식 없는 일반 텍스트를 저장하는 가장 단순한 파일 형식입니다. 한 줄씩 기록된 측정값, 실행 로그, 간단한 목록 등을 읽거나 저장할 때 주로 사용합니다.

```python
with open("sample_text.txt", "w", encoding="utf-8") as file:
    file.write("월요일\n화요일\n수요일\n")

with open("sample_text.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

```text
월요일
화요일
수요일
```

`read()` 메서드는 파일의 전체 내용을 하나의 긴 문자열로 읽어 오고, `readlines()` 메서드는 각 줄을 요소로 담은 리스트를 반환합니다. 위 예제처럼 파일 객체를 `for` 반복문으로 직접 순회하면 메모리를 효율적으로 사용하면서 내용을 한 줄씩 차례대로 처리할 수 있습니다.

#### CSV (Comma-Separated Values)

CSV는 행과 열로 이루어진 표 형태의 데이터를 쉼표(`,`)로 구분해 저장하는 텍스트 형식입니다. Python 표준 라이브러리인 `csv` 모듈을 사용하면 각 행을 리스트 형태로 손쉽게 읽고 쓸 수 있습니다.

```python
import csv

with open("sample_scores.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["학번", "점수"])
    writer.writerow(["S101", 85])
    writer.writerow(["S102", 92])

with open("sample_scores.csv", "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

```text
['학번', '점수']
['S101', '85']
['S102', '92']
```

`writerow()`는 전달받은 리스트를 하나의 행으로 기록합니다. 반대로 `csv.reader()`로 파일을 읽으면 모든 칸의 데이터가 문자열(`str`) 형태로 반환되므로, 점수처럼 수치 계산이 필요한 데이터는 `int()`나 `float()`로 변환해 사용해야 합니다.

> **참고:** CSV 파일은 엑셀(Excel) 같은 스프레드시트 프로그램에서도 바로 열어볼 수 있지만, `.xlsx` 같은 전용 통합 문서 형식과는 다릅니다. 코드를 작성할 때 `newline=""` 옵션을 지정하면 줄바꿈 문자가 중복으로 들어가는 현상을 막을 수 있습니다. 또한 `utf-8-sig` 인코딩은 파일 맨 앞에 UTF-8 BOM 정보를 함께 기록하여, 엑셀 등에서 CSV 파일을 열 때 한글이 깨지지 않도록 도와줍니다.

#### JSON (JavaScript Object Notation)

JSON은 키-값 쌍(객체)과 목록(배열) 등 계층적으로 구조화된 데이터를 저장하고 교환할 때 널리 쓰이는 텍스트 형식입니다. 프로그램의 환경 설정이나 여러 속성을 지닌 복합 데이터를 저장할 때 매우 유용합니다.

Python의 `json` 모듈을 사용하면 딕셔너리나 리스트 같은 Python 데이터를 JSON 형식으로 변환해 저장하거나, 반대로 JSON 파일을 읽어 Python 데이터로 복원할 수 있습니다.

```python
import json

settings = {
    "language": "한국어",
    "font_size": 14,
    "notifications": True,
}

with open("sample_settings.json", "w", encoding="utf-8") as file:
    json.dump(settings, file, ensure_ascii=False, indent=4)

with open("sample_settings.json", "r", encoding="utf-8") as file:
    restored = json.load(file)

print(restored["language"])   # 한국어
print(restored["font_size"])  # 14
```

위 코드를 실행해 생성된 `sample_settings.json` 파일의 실제 내용은 다음과 같습니다.

```json
{
    "language": "한국어",
    "font_size": 14,
    "notifications": true
}
```

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">함수 및 옵션</th>
<th align="center" style="text-align: center;">역할</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>json.dump(data, file)</code></td>
<td align="center" style="text-align: center;">Python 데이터를 JSON 형식으로 변환해 파일에 기록</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>json.load(file)</code></td>
<td align="center" style="text-align: center;">JSON 파일의 내용을 읽어 Python 데이터로 복원</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>ensure_ascii=False</code></td>
<td align="center" style="text-align: center;">한글 등을 <code>\uXXXX</code> 같은 유니코드 이스케이프 문자로 바꾸지 않고 원문 그대로 기록</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>indent=4</code></td>
<td align="center" style="text-align: center;">사람이 읽기 쉽도록 지정한 칸수만큼 들여쓰기를 적용해 줄 바꿈</td>
</tr>
</tbody>
</table>

JSON에서 객체의 키(Key)는 항상 문자열로 저장되며, Python의 튜플(Tuple)은 JSON 배열로 저장되기 때문에 나중에 다시 읽어 오면 리스트(List)로 변환됩니다. 또한 Python의 `True`, `False`, `None`은 JSON 표준에 따라 각각 `true`, `false`, `null`로 대응됩니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">파일 형식</th>
<th align="center" style="text-align: center;">주요 용도</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><strong>TXT</strong></td>
<td align="center" style="text-align: center;">서식 없는 일반 텍스트, 단순 목록, 실행 로그</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>CSV</strong></td>
<td align="center" style="text-align: center;">행과 열로 구성된 통계 보고서, 표 형태의 데이터</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>JSON</strong></td>
<td align="center" style="text-align: center;">프로그램 환경 설정, 계층적·구조화된 데이터, 프로그램 상태 저장</td>
</tr>
</tbody>
</table>

### 1.5 라이브러리와 API (Library & API)

**라이브러리(Library)** 는 **여러 프로그램에서 재사용할 수 있도록 유용한 기능을 미리 만들어 모아 둔 도구 모음**입니다. Python은 파일 처리, 데이터 변환, 날짜 계산 등 다양한 기능을 표준 라이브러리로 기본 제공합니다. 앞서 살펴본 `pathlib`, `csv`, `json` 역시 표준 라이브러리에 포함되어 있어 별도의 패키지를 설치하지 않고도 바로 불러와 사용할 수 있습니다.

**API(Application Programming Interface)** 는 **프로그램이나 라이브러리의 기능을 외부에서 사용할 수 있도록 정의해 둔 규칙이자 창구**입니다. 예를 들어 `json.load(file)`은 JSON 파일을 읽어 Python 데이터로 변환하는 기능을 호출하기 위해 약속된 API 사용법입니다.

API를 올바르게 활용하려면 호출할 함수나 메서드의 이름, 전달해야 할 인수의 형태, 반환되는 결과값, 그리고 실행 중 발생할 수 있는 예외의 종류를 정확히 확인해야 합니다. 이러한 API는 날씨·지도 등을 제공하는 인터넷 서비스뿐만 아니라 프로그래밍 라이브러리에도 동일하게 존재합니다.

### 1.6 예외 처리 (Exception Handling)

프로그램의 처리 절차가 올바르더라도 실행 환경에 따라 예상치 못한 문제가 발생할 수 있습니다. 예를 들어 읽어야 할 입력 파일이 없거나, 결과 파일을 저장할 권한이 부족한 경우입니다. Python에서는 `try`, `except`, `else` 구문을 사용해 이러한 예외 상황에 안전하게 대응할 수 있습니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">구문</th>
<th align="center" style="text-align: center;">역할</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>try</code></td>
<td align="center" style="text-align: center;">실행 중 예외가 발생할 가능성이 있는 코드 블록 실행</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>except</code></td>
<td align="center" style="text-align: center;">지정한 예외가 발생했을 때 실행할 대응 코드 작성</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>else</code></td>
<td align="center" style="text-align: center;"><code>try</code> 블록이 아무런 예외 없이 정상 종료되었을 때 실행</td>
</tr>
</tbody>
</table>

```python
text = input("신청 수량을 정수로 입력하세요. ")

try:
    count = int(text)
except ValueError:
    print("3과 같은 정수를 입력해 주세요.")
else:
    print(f"신청 수량은 {count}개입니다.")
```

위 코드에 `3`을 입력하면 정수 변환에 성공해 `else` 블록이 실행됩니다. 반면 `"세 개"`처럼 숫자가 아닌 문자열을 입력하면 `int(text)` 변환 과정에서 `ValueError`가 발생해 `except` 블록의 안내 문구가 출력됩니다.

정수로 변환할 수 있는 값이라 하더라도 `-5` 같은 음수 수량은 프로그램의 규칙에 어긋날 수 있습니다. 이처럼 입력된 데이터가 정해진 업무 규칙과 조건에 맞는지 확인하는 작업을 **유효성 검사(Validation)** 라고 합니다. 유효성 검사는 예외 처리와는 별도로 `if` 조건문을 사용해 검사할 수 있습니다.

#### 파일 처리에서 발생하는 주요 예외

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">예외 클래스</th>
<th align="center" style="text-align: center;">주요 발생 상황</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>FileNotFoundError</code></td>
<td align="center" style="text-align: center;">읽으려는 파일이나 지정한 경로가 존재하지 않음</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>FileExistsError</code></td>
<td align="center" style="text-align: center;"><code>x</code> 모드로 새로 생성하려는 파일이 이미 존재함</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>PermissionError</code></td>
<td align="center" style="text-align: center;">파일에 접근하거나 내용을 기록할 권한이 없음</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>UnicodeDecodeError</code></td>
<td align="center" style="text-align: center;">지정한 인코딩 방식으로 파일의 문자를 해석할 수 없음</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>json.JSONDecodeError</code></td>
<td align="center" style="text-align: center;">읽어 들인 JSON 데이터의 문법 형식이 올바르지 않음</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>OSError</code></td>
<td align="center" style="text-align: center;">파일 접근 및 입출력 등 운영체제 관련 작업 전반에서 예외 발생</td>
</tr>
</tbody>
</table>

```python
try:
    with open("practice_note.txt", "x", encoding="utf-8") as note:
        note.write("실습 결과를 확인했습니다.\n")
except FileExistsError:
    print("실습 기록이 이미 있습니다.")
except OSError as error:
    print(f"실습 기록을 저장할 수 없습니다. {error}")
else:
    print("새 실습 기록을 만들었습니다.")
```

> **작성 유의사항:** `FileExistsError`처럼 구체적인 하위 예외는 이를 포괄하는 상위 예외인 `OSError`보다 반드시 먼저 작성해야 합니다. 상위 예외를 먼저 적으면 구체적인 예외 처리 블록이 실행되지 않고 건너뛰어지기 때문입니다.

위 코드를 `practice_note.txt` 파일이 없는 실습 폴더에서 두 번 연속 실행해 보세요. 첫 번째 실행에서는 새 파일이 생성되고, 두 번째 실행에서는 `FileExistsError`가 처리되면서 기존 파일을 덮어쓰지 않습니다.


## 2. 자동화 프로그램 (Automation Programs)

### 2.1 자동화 프로그램의 개념

**자동화 프로그램은 사람이 수행하던 반복 작업을 미리 정해 둔 조건과 규칙에 따라 대신 처리하는 프로그램입니다.**

예를 들어 사용자가 실행 버튼을 누른 뒤 프로그램이 모든 신청 항목을 자동으로 집계한다면, 작업의 시작은 사람이 했더라도 실제 집계 과정은 자동화된 것입니다. 이처럼 작업의 시작 조건은 사용자의 직접 실행이나 입력뿐만 아니라 지정된 시각(스케줄링), 특정 폴더의 파일 변경 감지 등으로 다양하게 설정할 수 있습니다.

자동화를 적용하면 반복 업무의 부담을 크게 줄이고, 많은 양의 데이터에 동일한 처리 규칙을 일관되게 적용할 수 있습니다. 다만 설계한 규칙에 오류가 있으면 그 잘못된 규칙 역시 모든 데이터에 반복해서 적용되므로, 실제 데이터에 사용하기 전에 작은 샘플 데이터로 동작을 충분히 검증해야 합니다.

### 2.2 주요 활용 사례

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">활용 사례</th>
<th align="center" style="text-align: center;">자동화 처리 내용</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><strong>과제 제출 현황 확인</strong></td>
<td align="center" style="text-align: center;">전체 학생 명단과 제출 기록을 대조하여 미제출자 명단 추출</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>일일 매출 집계</strong></td>
<td align="center" style="text-align: center;">거래 내역 데이터를 읽어 품목별·지점별 합계를 계산하고 보고서 생성</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>데이터 백업</strong></td>
<td align="center" style="text-align: center;">지정한 조건이나 주기에 따라 중요 파일 및 데이터를 자동으로 복사·보관</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>파일 목록 관리</strong></td>
<td align="center" style="text-align: center;">특정 폴더 내의 파일 정보를 스캔하여 최신 목록으로 갱신</td>
</tr>
</tbody>
</table>

### 2.3 자동화 프로그램의 설계

자동화할 작업을 정했다면 코드를 작성하기 전에 **시작 조건, 입력, 처리 규칙, 출력, 예외 상황**의 다섯 가지 요소를 먼저 명확히 정의해야 합니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">설계 항목</th>
<th align="center" style="text-align: center;">핵심 역할</th>
<th align="center" style="text-align: center;">준비물 신청 집계 예시</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><strong>시작 조건 (Trigger)</strong></td>
<td align="center" style="text-align: center;">자동화 작업을 개시하는 조건</td>
<td align="center" style="text-align: center;">사용자가 터미널에서 프로그램 실행</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>입력 (Input)</strong></td>
<td align="center" style="text-align: center;">프로그램이 읽어 들일 원본 데이터</td>
<td align="center" style="text-align: center;">한 줄에 한 건씩 작성된 신청 내역 텍스트 파일</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>처리 규칙 (Process)</strong></td>
<td align="center" style="text-align: center;">데이터에 적용할 정제 조건과 연산 로직</td>
<td align="center" style="text-align: center;">앞뒤 공백 제거, 소문자 통일, 품목별 건수 집계</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>출력 (Output)</strong></td>
<td align="center" style="text-align: center;">처리를 마친 뒤 생성되는 최종 결과물</td>
<td align="center" style="text-align: center;">품목명과 신청 건수가 정리된 CSV 보고서 파일</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>예외 상황 (Exception)</strong></td>
<td align="center" style="text-align: center;">정상적인 처리가 불가능할 때의 대응 방식</td>
<td align="center" style="text-align: center;">입력 파일 누락, 인코딩 오류, 기존 보고서 이름 충돌 시 안내</td>
</tr>
</tbody>
</table>

프로그램을 구현한 뒤에는 올바른 정상 데이터뿐만 아니라 빈 입력, 중복 데이터, 파일 누락 같은 다양한 예외 조건에서도 요구사항대로 동작하는지 테스트해야 합니다. 예외 상황에서 사용자에게 적절한 안내 메시지가 출력되는지, 그리고 유효하지 않은 데이터가 처리 대상에서 제외되는지도 중요한 검증 대상입니다.

## 3. Example — 준비물 신청 내역 집계

### 3.1 요구사항 및 처리 절차

준비물 신청 내역 파일을 읽어 품목별 신청 건수를 계산하고, 결과를 CSV 보고서로 저장하는 프로그램입니다. 입력 파일의 한 줄을 신청 한 건으로 처리하며, 영문 대소문자나 앞뒤 공백의 차이는 구분하지 않습니다. 공백만 있는 빈 줄은 집계에서 제외하고, 최종 결과는 품목명 오름차순으로 정렬해 저장합니다. 또한 같은 이름의 보고서 파일이 이미 있다면 덮어쓰지 않고 안내 메시지를 출력합니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">순서</th>
<th align="center" style="text-align: center;">처리 내용</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><strong>1</strong></td>
<td align="center" style="text-align: center;">입력 파일(<code>requests.txt</code>) 열기</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>2</strong></td>
<td align="center" style="text-align: center;">각 줄의 앞뒤 공백 제거 및 영문 소문자 통일</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>3</strong></td>
<td align="center" style="text-align: center;">빈 줄을 제외하고 품목별 신청 건수 집계</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>4</strong></td>
<td align="center" style="text-align: center;">품목명을 오름차순 정렬하여 CSV 보고서에 기록</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>5</strong></td>
<td align="center" style="text-align: center;">최종 처리 결과 또는 예외 안내 메시지 출력</td>
</tr>
</tbody>
</table>

### 3.2 입력 데이터

새 실습 폴더에 `requests.txt` 파일을 만들고 다음 내용을 UTF-8 인코딩으로 저장하세요. 테스트를 위해 중간에 빈 줄도 함께 포함합니다.

```text
Pencil
ruler
PENCIL

eraser
pencil
```

### 3.3 전체 코드

입력 파일과 같은 폴더에 다음 코드를 작성해 `summarize_requests.py`로 저장합니다.

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

### 3.4 코드 분석

**입력과 집계:** `main()` 함수에서 입력 파일을 열어 `count_requests()` 함수에 전달합니다. 파일 객체는 반복문으로 한 줄씩 바로 순회할 수 있으므로 파일 전체 내용을 미리 리스트로 변환할 필요가 없습니다. `Path.open()` 메서드는 기본 `open()` 함수와 동일하게 파일을 여는 역할을 합니다.

`count_requests()` 함수는 각 줄의 문자열을 정리한 뒤, 빈 문자열(`""`)이면 `continue`로 건너뜁니다. 이어지는 다음 코드는 기존 신청 건수에 `1`을 더한 값을 해당 품목의 키에 저장합니다.

```python
counts[item] = counts.get(item, 0) + 1
```

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">읽은 줄</th>
<th align="center" style="text-align: center;">정리된 품목</th>
<th align="center" style="text-align: center;">처리 후 <code>counts</code> 상태</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>Pencil</code></td>
<td align="center" style="text-align: center;"><code>pencil</code></td>
<td align="center" style="text-align: center;"><code>{'pencil': 1}</code></td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>ruler</code></td>
<td align="center" style="text-align: center;"><code>ruler</code></td>
<td align="center" style="text-align: center;"><code>{'pencil': 1, 'ruler': 1}</code></td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>PENCIL</code></td>
<td align="center" style="text-align: center;"><code>pencil</code></td>
<td align="center" style="text-align: center;"><code>{'pencil': 2, 'ruler': 1}</code></td>
</tr>
<tr>
<td align="center" style="text-align: center;">빈 줄</td>
<td align="center" style="text-align: center;"><code>""</code> (빈 문자열)</td>
<td align="center" style="text-align: center;">변화 없음 (건너뜀)</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>eraser</code></td>
<td align="center" style="text-align: center;"><code>eraser</code></td>
<td align="center" style="text-align: center;"><code>{'pencil': 2, 'ruler': 1, 'eraser': 1}</code></td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>pencil</code></td>
<td align="center" style="text-align: center;"><code>pencil</code></td>
<td align="center" style="text-align: center;"><code>{'pencil': 3, 'ruler': 1, 'eraser': 1}</code></td>
</tr>
</tbody>
</table>

**보고서 저장:** 집계 함수가 반환한 딕셔너리를 `sorted(counts)`로 순회하여 품목명 오름차순으로 정렬해 기록합니다. 파일을 열 때 `"x"` 모드를 사용하므로 같은 이름의 기존 보고서는 덮어쓰지 않습니다.

**예외 처리:** 입력 파일 누락, 보고서 이름 충돌, 인코딩 오류 등 상황별로 알맞은 안내 메시지를 출력합니다. 파일 읽기와 저장이 모두 예외 없이 정상적으로 끝나면 `else` 블록이 실행되며, `sum(counts.values())`로 전체 신청 건수를 합산해 화면에 표시합니다.

#### 함수 정의와 직접 실행

`if __name__ == "__main__":` 조건문은 해당 Python 파일을 터미널 등에서 직접 실행할 때만 내부 코드를 실행하도록 제어합니다. 다른 파일에서 이 모듈을 `import`로 불러오는 경우에는 조건이 거짓이 되므로 `main()`이 자동으로 실행되지 않습니다. 단, 모듈을 처음 불러올 때 조건문 밖의 최상위 코드는 실행됩니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">파일 끝의 구성 방식</th>
<th align="center" style="text-align: center;">직접 실행 시</th>
<th align="center" style="text-align: center;">다른 파일에서 처음 불러올 시</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>if __name__ == "__main__":</code> 아래 <code>main()</code> 호출</td>
<td align="center" style="text-align: center;"><code>main()</code> 실행</td>
<td align="center" style="text-align: center;"><code>main()</code> 자동 실행 안 됨</td>
</tr>
<tr>
<td align="center" style="text-align: center;">조건문 없이 바로 <code>main()</code> 호출</td>
<td align="center" style="text-align: center;"><code>main()</code> 실행</td>
<td align="center" style="text-align: center;">불러오는 과정에서도 <code>main()</code> 즉시 실행</td>
</tr>
<tr>
<td align="center" style="text-align: center;">함수 정의만 작성 (<code>main()</code> 호출 없음)</td>
<td align="center" style="text-align: center;">함수만 정의됨</td>
<td align="center" style="text-align: center;">함수만 정의됨</td>
</tr>
</tbody>
</table>

실습 폴더에서 다음 명령어를 실행하면 보고서를 생성하지 않고 `count_requests()` 함수만 따로 불러와 동작을 검증할 수 있습니다.

```bash
python -c "from summarize_requests import count_requests; print(count_requests(['Pencil', 'PENCIL']))"
```

```text
{'pencil': 2}
```

이 명령은 `main()` 함수를 호출하지 않으므로 새로운 CSV 보고서 파일을 만들지 않습니다.

### 3.5 실행 결과 및 검증

터미널에서 두 파일이 저장된 실습 폴더로 이동한 뒤 프로그램을 실행합니다. Windows 환경에서 Python 실행 명령어로 `py`를 사용하는 경우에는 `py summarize_requests.py`를 입력하면 됩니다.

```bash
python summarize_requests.py
```

```text
신청 5건을 집계했습니다.
```

정상 실행 후 생성된 `summary.csv` 파일에는 다음과 같은 내용이 저장됩니다.

```csv
품목,신청 건수
eraser,1
pencil,3
ruler,1
```

다음 네 가지 테스트 조건에서 프로그램을 각각 실행해 예상 결과와 일치하는지 검증해 보세요. 각 테스트를 진행하기 전에는 필요한 파일 상태를 먼저 맞추어야 하며, 기존 보고서 보존 테스트를 제외한 나머지 경우에는 이전 보고서의 이름을 바꾸거나 별도의 실습 폴더를 사용하는 것이 좋습니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">테스트 조건</th>
<th align="center" style="text-align: center;">예상 결과</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;">기본 입력 데이터 존재, 보고서 없음</td>
<td align="center" style="text-align: center;"><code>5건</code> 집계 완료 및 <code>summary.csv</code> 생성</td>
</tr>
<tr>
<td align="center" style="text-align: center;">빈 입력 파일 또는 공백만 있는 파일 존재, 보고서 없음</td>
<td align="center" style="text-align: center;"><code>0건</code> 집계 완료 및 제목 행만 있는 보고서 생성</td>
</tr>
<tr>
<td align="center" style="text-align: center;">입력 파일(<code>requests.txt</code>)이 없을 때</td>
<td align="center" style="text-align: center;">입력 파일 누락 안내 메시지 출력</td>
</tr>
<tr>
<td align="center" style="text-align: center;">입력 파일은 정상이나 보고서(<code>summary.csv</code>)가 이미 있을 때</td>
<td align="center" style="text-align: center;">기존 보고서 보존 및 이름 충돌 안내 출력</td>
</tr>
</tbody>
</table>

> **참고:** `"x"` 모드는 같은 이름의 기존 파일이 덮어씌워지는 것을 방지하는 용도입니다. 파일을 기록하는 도중 저장 장치에 물리적 오류가 발생하는 등 모든 저장 실패 상황에서 결과 파일의 완전성까지 보장하는 것은 아닙니다.

## 4. Practice

각 실습에서는 요구사항을 분석한 뒤 STEP별 안내에 따라 프로그램을 완성합니다. 시작 코드에 표시된 `TODO` 부분을 직접 채워 넣으세요. `raise NotImplementedError`는 아직 구현되지 않은 함수가 호출되었음을 알리는 코드이므로, 기능을 구현할 때 이 줄을 지우고 알맞은 코드를 작성하면 됩니다.

제시된 함수 구조는 구현을 돕기 위한 권장 가이드입니다. 요구사항을 모두 충족한다면 다른 구조로 작성해도 무방합니다. 각 실습의 예상 실행 결과는 작성한 프로그램이 올바르게 동작하는지 검증하는 기준이 됩니다.

### 4.1 Practice 01 — 과제 미제출자 확인

전체 학생 명단과 과제 제출 기록을 비교하여 아직 과제를 제출하지 않은 학생의 학번을 출력하는 프로그램을 작성하세요. 제출 기록에는 중복된 학번, 불필요한 공백, 그리고 영문 대소문자 차이가 섞여 있을 수 있습니다.

#### 입력 데이터

```python
roster = ["S101", "S102", "S103", "S104", "S105"]
records = [" s103 ", "S103", "", "s101", "S999", "  "]
```

#### 구현 조건

* 제출 기록의 앞뒤 공백을 제거하고 영문자를 모두 대문자로 통일합니다.
* 공백만 있는 빈 기록, 전체 학생 명단에 없는 학번, 이미 집계된 중복 제출 기록은 제외합니다.
* 미제출자는 **전체 학생 명단(`roster`)에 등록된 순서**대로 출력해야 합니다.
* 전체 학생 명단은 중복 없이 대문자로 정리되어 있으며, 제출 기록의 모든 요소는 문자열(`str`)이라고 가정합니다.

#### STEP 01. 프로그램 설계

시작 조건, 입력, 처리 규칙, 출력, 그리고 예외 및 유효하지 않은 데이터의 처리 방식을 미리 정리해 보세요. 제출자 목록과 미제출자 목록을 어떤 자료구조로 관리할지도 함께 결정합니다.

#### STEP 02. 유효한 제출 기록 처리

제출 기록을 정리하고, 유효한 학생의 학번만 중복 없이 모아 반환하는 함수를 작성하세요.

```python
def valid_submissions(roster, records):
    # TODO: 제출 기록 정리, 유효성 검사 및 중복 제거
    raise NotImplementedError
```

#### STEP 03. 미제출자 확인

전체 학생 명단과 유효한 제출자 목록을 비교하여 미제출자의 학번을 리스트로 반환하는 함수를 작성하세요.

```python
def find_missing(roster, submitted):
    # TODO: 학생 명단 순서대로 미제출자 목록 생성
    raise NotImplementedError
```

#### STEP 04. 프로그램 통합

STEP 02와 STEP 03에서 작성한 함수들과 아래의 시작 코드를 하나의 Python 파일로 통합하세요. `main()` 함수에서 필요한 함수를 차례로 호출하고 제출 인원과 미제출자 목록을 출력합니다.

```python
def main():
    roster = ["S101", "S102", "S103", "S104", "S105"]
    records = [" s103 ", "S103", "", "s101", "S999", "  "]

    # TODO: 제출 기록 처리
    # TODO: 미제출자 확인
    # TODO: 제출 현황 및 미제출자 출력
    raise NotImplementedError


if __name__ == "__main__":
    main()
```

#### 예상 실행 결과

```text
제출 2명 / 전체 5명
미제출: S102, S104, S105
```

> **참고:** 모든 학생이 과제를 제출해 미제출자가 없는 경우에는 `미제출: 없음`을 출력해야 합니다.

#### STEP 05. 테스트

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">테스트 조건</th>
<th align="center" style="text-align: center;">예상 결과</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;">기본 입력 데이터 사용</td>
<td align="center" style="text-align: center;">제출 2명, 미제출 3명 (<code>S102, S104, S105</code>)</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>records = []</code></td>
<td align="center" style="text-align: center;">제출 0명, 전체 학생 미제출</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>records = ["S105", "S103", "S101", "S104", "S102"]</code></td>
<td align="center" style="text-align: center;">제출 5명, <code>미제출: 없음</code> 출력</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>records = [" s102 ", "S102", "S999", " "]</code></td>
<td align="center" style="text-align: center;">제출 1명 (<code>S102</code>), 미제출 4명</td>
</tr>
</tbody>
</table>

각 테스트 케이스를 실행하면서 제출 인원과 미제출자 목록의 순서가 요구사항을 정확히 만족하는지 확인해 보세요.

### 4.2 Practice 02 — 실습실 교구 대여 관리

실습실의 교구 대여·반납 기록을 입력 순서대로 처리하고, 품목별 최종 대여 가능 수량을 JSON 파일로 관리하는 프로그램을 작성하세요. 조건에 맞지 않아 처리할 수 없는 기록은 제외 사유를 남기고 다음 기록을 이어서 처리합니다.

#### 입력 데이터

```python
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
```

#### 구현 조건

1. 각 기록은 `(품목, 동작, 수량)` 형태의 튜플로 주어집니다. 품목은 초기 재고에 등록된 문자열이어야 하며, 동작은 `"대여"` 또는 `"반납"`, 수량은 양의 정수(`int`)여야 합니다. 이때 불리언 값인 `True`, `False`는 수량으로 허용하지 않습니다.
2. 유효성 검사에서 여러 조건을 동시에 위반한 경우, **품목 → 동작 → 수량** 순서대로 가장 먼저 발견한 사유 하나만 기록합니다.
3. **대여** 시에는 현재 재고에서 수량을 빼고, **반납** 시에는 현재 재고에 수량을 더합니다. 계산된 결과는 `0` 이상이면서 해당 품목의 초기 재고 이하여야 합니다.
4. 잘못된 기록은 재고에 반영하지 않고 **`(기록 번호, 이유)` 형태로 기록**합니다. 기록 번호는 `1`부터 시작하며, 원본인 초기 재고 딕셔너리(`initial_stock`)는 수정되지 않고 그대로 유지되어야 합니다.
5. 처리 결과는 `equipment_stock.json` 파일에 저장하며, 저장된 재고 파일을 다시 읽어 화면에 표시할 수 있어야 합니다. 기존 재고 파일이 있으면 그 수량을 이어서 사용하며, 초기 재고는 품목별 최대 보유 수량을 판단하는 기준으로 계속 유지합니다.
6. 저장된 재고 파일이 없으면 초기 재고를 사용합니다. 반면, 기존 파일을 읽을 수 없거나 JSON 문법 또는 저장된 수량 데이터가 올바르지 않으면 오류 안내 메시지를 출력하고 처리를 중단해야 합니다. 이때 손상되거나 잘못된 저장 파일을 초기값으로 덮어쓰지 않도록 주의합니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">제외 사유</th>
<th align="center" style="text-align: center;">발생 조건</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><code>등록되지 않은 품목</code></td>
<td align="center" style="text-align: center;">문자열이 아니거나 초기 재고(<code>initial_stock</code>)에 없는 품목</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>알 수 없는 동작</code></td>
<td align="center" style="text-align: center;"><code>"대여"</code>, <code>"반납"</code> 외의 동작</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>잘못된 수량</code></td>
<td align="center" style="text-align: center;">양의 정수가 아닌 수량 (<code>0</code>, 음수, 문자열, 불리언 등)</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>재고 부족</code></td>
<td align="center" style="text-align: center;">대여 수량이 현재 재고를 초과</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><code>초기 재고 초과</code></td>
<td align="center" style="text-align: center;">반납 후 수량이 초기 재고를 초과</td>
</tr>
</tbody>
</table>

> **가정 사항:** 이 실습에서는 초기 재고의 품목 목록과 최대 수량이 실행 도중 변경되지 않으며, 입력되는 각 기록 튜플의 길이와 구조(`(품목, 동작, 수량)`)는 올바르다고 가정합니다.

#### STEP 01. 프로그램 설계

전체 처리 순서와 각 함수가 맡을 역할을 미리 정리해 보세요. 초기 재고와 현재 재고를 어떻게 구분해 다룰지, 그리고 제외된 기록을 어떤 형태로 수집할지 결정합니다. 프로그램을 다시 실행했을 때 기존 JSON 데이터를 불러와 이어가는 흐름도 함께 설계합니다.

#### STEP 02. 재고 변경 및 기록 검증

입력된 대여·반납 기록을 순서대로 처리하고, 갱신된 현재 재고와 제외된 기록 목록을 함께 반환하는 함수를 작성하세요. 함수에 전달된 원본 `initial_stock`과 `current_stock` 딕셔너리는 직접 수정하지 않아야 합니다.

```python
def apply_records(initial_stock, current_stock, records):
    stock = current_stock.copy()
    rejected = []

    # TODO: 기록별 유효성 검사
    # TODO: 대여·반납에 따른 재고 변경 또는 제외 사유 기록
    raise NotImplementedError
```

#### STEP 03. JSON 저장 및 불러오기

현재 재고를 JSON 파일에 저장하고, 저장된 파일을 다시 읽어 오는 함수를 작성하세요. 저장 파일이 아직 없는 정상적인 초기 상황과 기존 파일이 손상되어 문제가 있는 예외 상황을 명확히 구분해야 합니다.

저장된 데이터에는 초기 재고의 모든 품목이 빠짐없이 정확히 한 번씩 포함되어야 하며, 각 품목의 수량은 `0` 이상 초기 재고 이하의 정수(`bool` 제외)여야 합니다. JSON 파일 내부의 중복 키 검출은 이번 실습 범위에서 제외하고, 읽어 들인 딕셔너리의 키와 값이 조건을 만족하는지 검사하세요.

> **참고:** `w` 모드는 기존 파일의 내용을 제거한 뒤 새 데이터를 기록합니다. 저장 도중 오류가 발생하면 파일이 손상될 수 있으므로, 중요한 데이터를 관리하는 프로그램에서는 별도의 백업이나 안전한 저장 방식을 고려해야 합니다.

```python
def load_stock(path, initial_stock):
    # TODO: 저장 파일 불러오기, 파일 누락 및 데이터 검증 처리
    raise NotImplementedError


def save_stock(path, stock):
    # TODO: 재고 데이터를 JSON으로 저장
    raise NotImplementedError
```

#### STEP 04. 프로그램 통합

앞서 구현한 함수들을 조합해 전체 프로그램을 완성하세요. 사용자가 아래 두 가지 동작 중 하나를 선택해 실행할 수 있도록 구성합니다. 메뉴 형태, 함수 호출 순서, 화면 출력 방식은 자유롭게 설계할 수 있습니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">동작</th>
<th align="center" style="text-align: center;">요구사항</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><strong>기록 처리</strong></td>
<td align="center" style="text-align: center;">저장된 재고(없으면 초기 재고)를 불러온 뒤, 입력된 대여·반납 기록을 한 번 처리하고 결과를 저장합니다.</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>재고 조회</strong></td>
<td align="center" style="text-align: center;">저장된 재고(없으면 초기 재고)를 불러와 화면에 표시합니다. 대여·반납 기록을 다시 적용하지 않습니다.</td>
</tr>
</tbody>
</table>

```python
from pathlib import Path


def main():
    path = Path("equipment_stock.json")

    # TODO: 초기 재고와 입력 기록 준비
    # TODO: 사용자 입력으로 기록 처리 또는 재고 조회 선택
    # TODO: 필요한 함수 호출 및 예외 처리
    # TODO: 결과 출력
    raise NotImplementedError


if __name__ == "__main__":
    main()
```

#### 예상 실행 결과

저장 파일이 없는 상태에서 기본 입력 데이터로 **기록 처리**를 선택했을 때의 처리 결과 예시입니다. 메뉴와 입력 안내는 생략했으며, 재고 현황은 품목명 오름차순으로 정렬해 표시합니다.

```text
2번 기록 제외: 재고 부족
4번 기록 제외: 등록되지 않은 품목
5번 기록 제외: 초기 재고 초과
6번 기록 제외: 알 수 없는 동작
7번 기록 제외: 잘못된 수량
가위: 3개
자: 2개
재고를 저장했습니다.
```

생성된 `equipment_stock.json` 파일에 저장되는 데이터 예시는 다음과 같습니다. 키의 저장 순서나 들여쓰기 칸수는 달라도 무방합니다.

```json
{
    "가위": 3,
    "자": 2
}
```

프로그램을 다시 실행한 뒤 **재고 조회**를 선택하면 대여·반납 기록을 중복 적용하지 않고 저장된 수량을 그대로 표시해야 합니다.

```text
가위: 3개
자: 2개
```

#### STEP 05. 테스트

독립적인 기능 테스트를 진행할 때는 이전 테스트에서 생성된 저장 파일을 다른 위치로 옮기거나 삭제해 초기 재고 상태에서 시작하세요. 반면, 저장 및 복원 테스트는 생성된 `equipment_stock.json` 파일을 유지한 상태에서 진행합니다.

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">테스트 조건</th>
<th align="center" style="text-align: center;">예상 결과</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;">기본 입력 데이터 실행</td>
<td align="center" style="text-align: center;">가위 3개, 자 2개, 총 5건 제외</td>
</tr>
<tr>
<td align="center" style="text-align: center;">빈 기록 목록(<code>records = []</code>) 실행</td>
<td align="center" style="text-align: center;">현재 재고 유지, 제외된 기록 없음</td>
</tr>
<tr>
<td align="center" style="text-align: center;">가위 4개 대여 (초기 상태 기준)</td>
<td align="center" style="text-align: center;">가위 0개, 정상 처리</td>
</tr>
<tr>
<td align="center" style="text-align: center;">가위 1개 반납 (초기 상태 기준)</td>
<td align="center" style="text-align: center;"><code>초기 재고 초과</code>로 제외</td>
</tr>
<tr>
<td align="center" style="text-align: center;">미등록 품목, 잘못된 동작, 수량 <code>0</code>이 한 기록에 동시 포함</td>
<td align="center" style="text-align: center;"><code>등록되지 않은 품목</code> 사유 하나만 기록</td>
</tr>
<tr>
<td align="center" style="text-align: center;">수량이 <code>True</code>인 기록</td>
<td align="center" style="text-align: center;"><code>잘못된 수량</code>으로 제외</td>
</tr>
<tr>
<td align="center" style="text-align: center;">품목이 리스트 등 문자열이 아닌 기록</td>
<td align="center" style="text-align: center;"><code>등록되지 않은 품목</code>으로 제외</td>
</tr>
<tr>
<td align="center" style="text-align: center;">기본 기록 처리 후 프로그램 재실행 및 재고 조회</td>
<td align="center" style="text-align: center;">가위 3개, 자 2개 그대로 유지</td>
</tr>
<tr>
<td align="center" style="text-align: center;">저장 파일에 잘못된 JSON 형식이나 범위를 벗어난 수량 포함</td>
<td align="center" style="text-align: center;">오류 안내 출력 및 기존 저장 파일 보존</td>
</tr>
</tbody>
</table>

테스트를 마친 뒤에는 원본인 초기 재고(`initial_stock`)와 함수에 전달한 현재 재고(`current_stock`)가 처리 이후에도 변하지 않았는지 함께 확인해 보세요.

#### 추가 과제 (선택)

* 교구 이름에 사용자가 입력한 검색어가 포함된 항목만 필터링하여 조회하는 기능을 추가해 보세요.
* 지정한 기준 수량 이하로 남은 재고만 골라 조회하는 기능을 구현해 보세요.
* 현재 재고 현황을 품목명 오름차순으로 정렬하여 CSV 보고서 파일로 내보내는 기능을 추가해 보세요. 이때 기존 보고서 파일이 있으면 덮어쓰지 않아야 합니다.

## 5. Summary

* **사용자 정의 함수:** `def` 키워드로 반복되는 기능을 함수로 정의하고, `return`으로 처리 결과를 반환하여 코드의 재사용성을 높입니다.
* **자료구조 선택:** 순서가 있는 목록은 **리스트**, 키-값 쌍의 빠른 조회는 **딕셔너리**, 변경되지 않아야 할 데이터 묶음은 **튜플**에 담아 목적에 맞게 활용합니다.
* **데이터 정제 및 처리:** 데이터를 비교하기 전에 공백 제거와 대소문자 통일(데이터 정규화)을 먼저 수행하고, 조건문으로 유효성 검사와 필터링을 처리합니다.
* **파일 시스템과 입출력:** `pathlib`으로 경로를 다루고, `with` 구문으로 파일을 열고 닫습니다. 데이터 형태와 용도에 따라 **TXT, CSV, JSON** 중 알맞은 형식을 선택해 영구 저장합니다.
* **라이브러리와 API:** 표준 라이브러리나 외부 도구를 사용할 때는 호출할 함수의 이름, 인수 형식, 반환값, 그리고 발생 가능한 예외를 확인해 규칙에 맞게 호출합니다.
* **예외 처리와 검증:** 파일 누락이나 형식 오류 같은 실행 예외는 `try-except`로 대응하고, 업무 규칙 위반 여부는 조건문 기반의 유효성 검사로 구분해 처리합니다.
* **자동화 설계와 테스트:** 자동화할 작업의 **시작 조건, 입력, 처리 규칙, 출력, 예외 상황**을 먼저 정의하고, 구현 후에는 정상 데이터뿐만 아니라 경계값과 오류 조건에서도 올바르게 동작하는지 검증합니다.

## 6. Quiz

### 문제 1.

다음 중 준비물 신청 집계를 자동화한 사례로 가장 적절한 것을 고르세요.

A. 사람이 신청서를 한 줄씩 직접 세어 결과를 기록합니다.  
B. 사용자가 실행 버튼을 누르면 프로그램이 신청 건수를 세어 표에 저장합니다.  
C. 집계 버튼을 누르면 기능에 대한 설명 문장만 나타납니다.  
D. 사람이 건수를 모두 계산한 뒤, 프로그램에 입력해 그 값을 그대로 표시합니다.

### 문제 2.

이름이 같은 동명이인 두 학생의 출석 여부를 딕셔너리에 저장하려고 합니다. 학생의 이름만 키(Key)로 사용하면 어떤 문제가 발생하나요? 또한, 두 학생을 명확히 구분할 수 있는 방법 한 가지를 서술하세요.

### 문제 3.

입력된 품목 이름을 소문자로 변환하고, 딕셔너리에 해당 품목이 없으면 `0`을 반환하도록 빈칸 두 곳을 채우세요. 코드를 실행했을 때의 출력 결과도 함께 적어 보세요.

```python
stock = {"pencil": 12, "ruler": 5}
item = "PENCIL".____()
print(stock.____(item, 0))
```

### 문제 4.

다음 코드를 실행했을 때 출력되는 두 줄을 순서대로 쓰세요.

```python
def calculate(price, quantity):
    return price * quantity


orders = [("연필", 500, 2), ("자", 1000, 3)]
for name, price, quantity in orders:
    print(name, calculate(price, quantity))
```

### 문제 5.

다음 코드를 실행했을 때 출력되는 두 줄의 결과를 쓰고, 두 속성이 서로 다른 값을 반환하는 이유를 설명하세요.

```python
from pathlib import Path

path = Path("자료/안내.TXT")
print(path.name)
print(path.suffix)
```

### 문제 6.

다음 각 상황에 가장 적합한 파일 형식(`TXT`, `CSV`, `JSON`)을 하나씩 고르세요.

A. 날짜와 매출액을 행과 열로 정리한 통계 보고서  
B. 언어, 글자 크기, 알림 여부 등 여러 속성을 담은 프로그램 설정 데이터  
C. 한 줄씩 차례대로 작성된 서식 없는 일반 텍스트 일지

### 문제 7.

실행 폴더에 `note.txt` 파일이 이미 존재한다고 가정합니다. 다음 코드를 실행했을 때 화면에 출력되는 문장과 기존 `note.txt` 파일의 내용이 변경되는지 여부를 쓰세요.

```python
try:
    with open("note.txt", "x", encoding="utf-8") as file:
        file.write("새 기록")
except FileExistsError:
    print("파일이 이미 있습니다.")
else:
    print("저장했습니다.")
```

### 문제 8.

매일 기록되는 실내 온도 데이터를 분석해 일일 평균 온도와 최고 온도를 보고서로 저장하는 자동화 프로그램을 설계하려고 합니다.

이 프로그램의 **시작 조건, 입력, 처리 규칙, 출력, 예외 상황**을 각각 한 가지 이상 구체적으로 제시하세요. (구현 코드는 작성하지 않아도 됩니다.)

## 7. Solutions

Quiz의 정답 및 해설입니다.

### 문제 1.

<details>
<summary>정답 및 해설 보기</summary>

**정답: B**

사용자가 실행 버튼을 눌러 작업을 시작했더라도, 실제 신청 건수의 집계와 표 저장은 프로그램이 자동으로 처리하므로 자동화된 사례에 해당합니다. 반면 A와 D는 사람이 직접 집계 과정을 수행하며, C는 버튼만 있을 뿐 실제 집계 작업을 수행하지 않습니다.

</details>

### 문제 2.

<details>
<summary>정답 및 해설 보기</summary>

**정답 예시:** 딕셔너리는 키(Key)의 중복을 허용하지 않으므로, 이름이 같은 두 학생을 동일한 키로 저장하면 나중에 저장한 값이 이전 학생의 기록을 덮어씁니다. 학생마다 고유하게 부여되는 **학번**이나 **회원 번호** 등을 키로 사용하면 두 사람의 출석 기록을 각각 구분하여 저장할 수 있습니다.

</details>

### 문제 3.

<details>
<summary>정답 및 해설 보기</summary>

**정답: `lower`, `get` / 출력 결과: `12`**

`"PENCIL".lower()`로 변환된 문자열 `"pencil"`은 `stock` 딕셔너리에 존재하는 키이므로, `get()` 메서드를 통해 해당 값인 `12`가 반환되어 출력됩니다. 키가 존재하지 않으면 두 번째 인수로 지정한 기본값 `0`을 반환합니다.

</details>

### 문제 4.

<details>
<summary>정답 및 해설 보기</summary>

**출력 결과:**

```text
연필 1000
자 3000
```

`for` 반복문에서 `orders` 리스트의 각 튜플을 `name`, `price`, `quantity` 세 변수로 언패킹합니다. `calculate()` 함수는 전달받은 가격과 수량의 곱을 반환하며, `print()` 함수는 품목명과 반환된 계산 결과를 순서대로 출력합니다.

</details>

### 문제 5.

<details>
<summary>정답 및 해설 보기</summary>

**출력 결과:**

```text
안내.TXT
.TXT
```

`name` 속성은 경로의 마지막 요소인 전체 파일명(`안내.TXT`)을 반환하고, `suffix` 속성은 파일의 마지막 확장자(`.TXT`)만 추출해 반환합니다. 지정한 경로에 실제 파일이 존재하지 않더라도 경로 객체의 구성 요소는 확인할 수 있습니다.

</details>

### 문제 6.

<details>
<summary>정답 및 해설 보기</summary>

**정답: A — CSV, B — JSON, C — TXT**

* **A (`CSV`):** 행과 열로 이루어진 표 형태의 통계 및 보고서 데이터를 저장하기에 적합합니다.
* **B (`JSON`):** 여러 속성과 계층을 가진 구조화된 설정 데이터를 저장하고 불러오기에 적합합니다.
* **C (`TXT`):** 별도의 데이터 구조나 서식이 필요 없는 일반 텍스트를 기록하기에 적합합니다.

</details>

### 문제 7.

<details>
<summary>정답 및 해설 보기</summary>

**출력 결과:**

```text
파일이 이미 있습니다.
```

**파일 변경 여부:** 변경되지 않음 (기존 내용 유지)

파일을 `"x"` 모드로 열면 같은 이름의 파일이 이미 존재할 때 `FileExistsError` 예외가 발생합니다. 따라서 파일을 새로 생성하거나 기존 내용을 덮어쓰지 않고 `except FileExistsError` 블록이 실행되며, 예외가 발생했으므로 `else` 블록은 실행되지 않습니다.

</details>

### 문제 8.

<details>
<summary>정답 및 해설 보기</summary>

**설계 예시:**

<table align="center" style="margin-left: auto; margin-right: auto;">
<thead>
<tr>
<th align="center" style="text-align: center;">설계 항목</th>
<th align="center" style="text-align: center;">예시 답안</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center" style="text-align: center;"><strong>시작 조건</strong></td>
<td align="center" style="text-align: center;">사용자가 터미널에서 일일 온도 보고서 생성 프로그램을 실행함</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>입력</strong></td>
<td align="center" style="text-align: center;">해당 날짜에 시간별로 기록된 실내 온도 측정 데이터 파일</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>처리 규칙</strong></td>
<td align="center" style="text-align: center;">온도 측정값을 숫자로 변환하고, 결측값이나 유효하지 않은 측정값을 제외한 뒤 일일 평균 온도와 최고 온도를 계산함</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>출력</strong></td>
<td align="center" style="text-align: center;">날짜, 평균 온도, 최고 온도가 정리된 CSV 보고서 파일</td>
</tr>
<tr>
<td align="center" style="text-align: center;"><strong>예외 상황</strong></td>
<td align="center" style="text-align: center;">입력 파일이 없거나 유효한 온도 데이터가 하나도 없는 경우 계산을 중단하고 안내 메시지를 출력함</td>
</tr>
</tbody>
</table>

> **참고:** 제시한 처리 규칙과 예외 상황이 서로 모순되지 않고, 정해진 입력을 통해 요구하는 출력을 도출할 수 있는 논리적인 구조라면 다른 형태의 설계도 정답으로 인정됩니다.

</details>

## 8. Reference

- [Python 공식 자습서 — 함수 정의](https://docs.python.org/ko/3/tutorial/controlflow.html#defining-functions)
- [Python 공식 자습서 — 자료구조](https://docs.python.org/ko/3/tutorial/datastructures.html)
- [Python 표준 라이브러리 — pathlib](https://docs.python.org/ko/3/library/pathlib.html)
- [Python 공식 자습서 — 입력과 출력](https://docs.python.org/ko/3/tutorial/inputoutput.html)
- [Python 표준 라이브러리 — csv](https://docs.python.org/ko/3/library/csv.html)
- [Python 표준 라이브러리 — json](https://docs.python.org/ko/3/library/json.html)
- [Python 공식 자습서 — 에러와 예외](https://docs.python.org/ko/3/tutorial/errors.html)
- [Python 공식 자습서 — 모듈](https://docs.python.org/ko/3/tutorial/modules.html)
