# Chapter 06. Arrays & Strings

배열(Array)과 문자열(String)을 사용하여 여러 값을 저장하고 탐색·정렬·변환하는 방법을 학습합니다. 고정 크기 배열과 동적 배열의 차이, 안전한 인덱스 접근, 문자열의 분리 및 정수 변환, C++20의 `std::span`을 다룹니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서 도입된 기능을 함께 사용하며, C++23의 관련 기능은 필요할 때 별도로 소개합니다.

<details>
<summary>선행 학습</summary>

- [Chapter 01. Getting Started with C++](../Chapter-01/) — 표준 입출력, `std::string`, `std::getline()`
- [Chapter 02. Variables & Data Types](../Chapter-02/) — 자료형, `auto`, 형변환, 표현 범위
- [Chapter 03. Operators & Conditions](../Chapter-03/) — 조건식, 오류 처리, 논리 연산
- [Chapter 04. Loops](../Chapter-04/) — 반복문, 누적 계산, 중첩 반복
- [Chapter 05. Functions](../Chapter-05/) — 함수, 참조 매개변수, `std::string_view`, 람다

</details>

## Contents

| Section | Topic |
|:---:|---|

| [6.1](#section-6-1) | Arrays & Strings — 데이터 묶음과 문자열 |

| [6.2](#section-6-2) | Fixed-Size Arrays — `std::array` |

| [6.3](#section-6-3) | Dynamic Arrays — `std::vector` |

| [6.4](#section-6-4) | Indexing & Bounds Checking |

| [6.5](#section-6-5) | Iteration & Aggregation |

| [6.6](#section-6-6) | Search & Sorting |

| [6.7](#section-6-7) | Non-Owning Views — `std::span` |

| [6.8](#section-6-8) | Multidimensional Data |

| [6.9](#section-6-9) | String Operations — `std::string` |

| [6.10](#section-6-10) | Line Input — `std::getline()` |

| [6.11](#section-6-11) | String Views — `std::string_view` |

| [6.12](#section-6-12) | Numeric Parsing — `std::from_chars()` |

| [6.13](#section-6-13) | Delimited Text |

| [6.14](#section-6-14) | UTF-8 & Text Length |

| [6.15](#section-6-15) | Container Selection & C-Style Arrays |

| [6.16](#section-6-16) | Coding Practice |

| [6.17](#section-6-17) | Mini Project — Sensor Batch Report |

| [6.18](#section-6-18) | Quiz & Summary |

## Getting Started

다음 명령어는 **`Chapter-06/` 디렉터리**에서 실행하는 경우를 기준으로 합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_fixed_array.cpp -o arrays
./arrays
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_fixed_array.cpp -o arrays
./arrays
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_fixed_array.cpp /Fe:arrays.exe
arrays.exe
```

Windows PowerShell에서는 `./arrays` 대신 `.\arrays.exe`로 실행합니다. 컴파일러 설정은 [Chapter 01](../Chapter-01/)에서 확인할 수 있습니다.

**학습 목표**

1. `std::array`와 `std::vector`를 구분하고 요소를 안전하게 관리할 수 있습니다.
2. 반복문과 표준 알고리즘으로 값을 집계·검색·정렬할 수 있습니다.
3. `std::span`과 `std::string_view`의 비소유(Non-Owning) 특성을 설명할 수 있습니다.
4. 문자열 검색·분할·숫자 변환에서 잘못된 입력을 검증할 수 있습니다.
5. 데이터의 구조와 사용 목적에 맞게 저장 타입을 선택할 수 있습니다.

---

<a id="section-6-1"></a>
## 6.1. Arrays & Strings — 데이터 묶음과 문자열

배열(Array)은 같은 자료형의 여러 요소(Element)를 하나의 이름으로 관리하는 자료구조입니다. 센서 값 세 개를 `first`, `second`, `third`처럼 따로 저장하면 모든 값에 동일한 작업을 적용하기 불편합니다. 배열을 사용하면 반복문으로 순회하거나 함수에 묶어서 전달할 수 있습니다.

문자열(String)은 여러 문자로 이루어진 텍스트를 표현합니다. C++의 `std::string`은 저장 공간을 직접 관리하지만, `std::string_view`는 다른 곳에 저장된 문자열을 읽기 위한 뷰(View)입니다.

| 타입 | 용도 | 요소 개수 | 데이터 소유 |
|---|---|---|---|
| `std::array<T, N>` | 고정 개수의 요소 | 선언 시 결정 | O |
| `std::vector<T>` | 실행 중 개수가 바뀌는 요소 | 실행 중 변경 | O |
| `std::span<T>` | 연속된 배열의 범위 전달 | 실행 중 확인 가능 | X |
| `std::string` | 텍스트 저장 및 수정 | 실행 중 변경 | O |
| `std::string_view` | 읽기 전용 문자열 접근 | 실행 중 확인 가능 | X |

**소유(Ownership)** 는 객체가 해당 데이터를 관리한다는 뜻입니다. **비소유 뷰(Non-Owning View)** 는 데이터를 복사하지 않고 참조하는 방식이므로, 원본이 사라지거나 저장 위치가 바뀌면 사용할 수 없게 될 수 있습니다. 객체 수명과 메모리 주소는 Chapter 07에서 더 자세히 다룹니다.

<a id="section-6-2"></a>
## 6.2. Fixed-Size Arrays — `std::array`

`std::array<T, N>`은 **요소의 자료형 `T`와 개수 `N`이 정해진 배열**입니다. 예를 들어 센서 채널이 네 개로 고정되어 있다면 `std::array<int, 4>`가 적합합니다.

`#include <array>`는 `std::array`를 사용할 때 필요한 표준 헤더입니다.

```cpp
std::array<int, 4> readings{21, 24, 19, 23};
```

| 구문 | 의미 |
|---|---|
| `readings.size()` | 요소 개수 `4` |
| `readings[0]` | 첫 번째 요소 `21` (범위 검사 없음) |
| `readings.at(1)` | 두 번째 요소 `24` (범위 검사 있음) |
| `readings.front()` | 첫 번째 요소 |
| `readings.back()` | 마지막 요소 |

인덱스(Index)는 **0부터 시작**하므로 크기가 4일 때 유효한 인덱스는 `0, 1, 2, 3`입니다. 배열을 생성한 후 요소값은 변경할 수 있지만 요소 개수는 변경할 수 없습니다.

**예제 코드 — [01_fixed_array.cpp](./examples/01_fixed_array.cpp)**

```cpp
#include <array>
#include <iostream>

int main() {
    const std::array<int, 4> readings{21, 24, 19, 23};
    std::cout << "Samples: " << readings.size() << '\n';
    std::cout << "First: " << readings.front() << '\n';
    std::cout << "Last: " << readings.back() << '\n';
}
```

**실행 결과**

```text
Samples: 4
First: 21
Last: 23
```

`std::array<int, 0>`처럼 크기가 0인 배열도 선언할 수 있습니다. 그러나 비어 있는 배열에서 `front()`나 `back()`을 호출해서는 안 됩니다.

<a id="section-6-3"></a>
## 6.3. Dynamic Arrays — `std::vector`

`std::vector<T>`는 요소를 연속된 저장 공간에 보관하면서 필요할 때 개수를 늘리거나 줄일 수 있는 **동적 배열(Dynamic Array)** 입니다. 실행 전에 데이터 개수를 정확히 알 수 없는 측정 결과나 목록에 적합합니다.

`#include <vector>`는 `std::vector`를 선언하고 사용하는 데 필요한 헤더입니다.

| 멤버 함수 | 기능 | 요소 개수 변화 |
|---|---|:---:|
| `size()` | 현재 존재하는 요소 수 반환 | X |
| `capacity()` | 현재 확보된 저장 공간의 수용 가능 요소 수 반환 | X |
| `reserve(n)` | 최소 `n`개를 위한 용량 확보 | X |
| `resize(n)` | 요소 수를 `n`으로 조정 | O |
| `push_back(value)` | 맨 뒤에 새 요소 하나 추가 | O |

`reserve(100)`은 100개의 요소를 만드는 것이 아닙니다. `size()`는 여전히 기존 값이므로, 저장 공간만 확보한 상태에서 `values[0]`을 읽으면 안 됩니다.

**예제 코드 — [02_dynamic_vector.cpp](./examples/02_dynamic_vector.cpp)**

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings;
    readings.reserve(5);
    readings.push_back(12);
    readings.push_back(18);
    readings.push_back(15);
    std::cout << "After reserve and insert: " << readings.size() << '\n';
    readings.resize(4);
    std::cout << "After resize: " << readings.size() << '\n';
    std::cout << "Fourth: " << readings.at(3) << '\n';
}
```

**실행 결과**

```text
After reserve and insert: 3
After resize: 4
Fourth: 0
```

이 예제에서 `resize(4)`로 새로 추가된 `int` 요소 하나는 0으로 초기화됩니다. `vector`에 요소를 추가하면서 공간을 재할당(Reallocation)하면 예전에 해당 요소를 가리키던 참조·반복자 등이 무효가 될 수 있습니다.

<a id="section-6-4"></a>
## 6.4. Indexing & Bounds Checking

`container[index]`는 일반적으로 자동 범위 검사를 수행하지 않습니다. 잘못된 인덱스로 접근하면 **미정의 동작(Undefined Behavior, UB)** 이 발생할 수 있습니다. 미정의 동작은 항상 오류 메시지가 나오는 현상을 뜻하지 않으며, 실행 결과를 신뢰할 수 없다는 의미입니다.

`at(index)`는 범위를 검사합니다. 인덱스가 잘못되면 `std::out_of_range` 예외(Exception)를 발생시킵니다. 예외는 정상 실행 흐름에서 벗어난 문제를 호출자에게 전달하는 기능이며 `try`·`catch`로 처리할 수 있습니다.

| 새로운 헤더 | 역할 |
|---|---|
| `<stdexcept>` | `std::out_of_range` 등 표준 예외 타입 제공 |
| `<cstddef>` | 인덱스·크기 표현에 자주 쓰이는 `std::size_t` 제공 (`std::size_t`는 이전 Chapter에서 학습) |

`std::size_t`는 음수가 아닌 크기와 인덱스를 나타내는 부호 없는 정수 타입입니다. 예제에서는 `std::array`가 필요한 크기 타입을 관련 헤더를 통해 제공하지만, 코드에서 `std::size_t`를 직접 사용할 때는 `<cstddef>`를 명시적으로 포함하는 것이 명확합니다.

**예제 코드 — [03_checked_access.cpp](./examples/03_checked_access.cpp)**

```cpp
#include <array>
#include <iostream>
#include <stdexcept>

int main() {
    const std::array<int, 3> voltages{12, 24, 48};
    const std::size_t index{3};

    if (index >= voltages.size()) {
        std::cout << "Index out of range: " << index << '\n';
    }
    try {
        const int value = voltages.at(index);
        std::cout << "Voltage: " << value << '\n';
    } catch (const std::out_of_range&) {
        std::cout << "at() rejected the index\n";
    }
}
```

**실행 결과**

```text
Index out of range: 3
at() rejected the index
```

이 코드는 오류가 예상되는 위치에서 `at()`과 `catch`를 비교하기 위한 예제입니다. 실제 입력을 처리할 때는 우선 `index < container.size()`인지 검사하여 잘못된 접근을 방지할 수 있습니다. 예외 처리 설계는 심화 Chapter에서 다룹니다.

<a id="section-6-5"></a>
## 6.5. Iteration & Aggregation

배열을 순회하면 합계(Sum), 최솟값(Minimum), 최댓값(Maximum), 평균(Mean) 등을 계산할 수 있습니다. Chapter 04의 범위 기반 `for` 문을 그대로 활용합니다.

평균을 계산할 때 두 정수끼리 나누면 소수 부분이 사라집니다. 하나를 `double`로 변환해야 소수 결과를 얻습니다. 출력 자릿수를 조절하는 `<iomanip>`의 `std::fixed`, `std::setprecision()`은 Chapter 02에서 다뤘습니다.

빈 배열에는 첫 번째 요소가 없으므로, `front()`로 최솟값·최댓값을 초기화할 때는 배열에 값이 하나 이상 있는지 확인해야 합니다.

**예제 코드 — [04_accumulate_readings.cpp](./examples/04_accumulate_readings.cpp)**

```cpp
#include <array>
#include <iomanip>
#include <iostream>

int main() {
    const std::array<int, 5> samples{8, 12, 14, 10, 16};
    int total{};
    int minimum{samples.front()};
    int maximum{samples.front()};
    for (const int sample : samples) {
        total += sample;
        if (sample < minimum) minimum = sample;
        if (sample > maximum) maximum = sample;
    }
    const double average = static_cast<double>(total) / samples.size();
    std::cout << "Total: " << total << '\n';
    std::cout << "Min: " << minimum << '\n';
    std::cout << "Max: " << maximum << '\n';
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Average: " << average << '\n';
}
```

**실행 결과**

```text
Total: 60
Min: 8
Max: 16
Average: 12.00
```

이 예제는 크기가 5로 정해진 배열을 사용하므로 비어 있지 않습니다. 측정값의 개수나 범위를 외부에서 입력받는 경우에는 빈 배열, 정수 누적 합계의 오버플로, 잘못된 값 등을 추가로 검증해야 합니다.

<a id="section-6-6"></a>
## 6.6. Search & Sorting

정렬(Sorting)은 값을 일정한 순서로 재배치하는 작업이고, 검색(Searching)은 특정 값 또는 조건을 만족하는 요소를 찾는 작업입니다. 단순한 반복문으로 직접 구현할 수도 있지만, C++ 표준 라이브러리의 알고리즘을 사용하면 의도를 명확하게 나타낼 수 있습니다.

| 헤더 | 제공 기능 | 예시 |
|---|---|---|
| `<algorithm>` | 정렬·검색·조건 집계 | `std::ranges::sort`, `std::ranges::count_if` |
| `<numeric>` | 수치 계산·누적 합계 | `std::accumulate` |

`std::ranges` 알고리즘은 **C++20**에서 도입된 범위(Range) 기반 알고리즘입니다. 반복자(Iterator)를 직접 두 개 전달하는 대신 컨테이너 자체를 인수로 전달할 수 있습니다. 반복자는 요소를 순서대로 가리키며 이동하는 도구로, `begin()`과 `end()`는 해당 범위의 시작과 끝을 나타냅니다.

`std::ranges::binary_search`는 데이터가 **검색 기준에 맞게 정렬되어 있어야** 올바르게 사용할 수 있습니다.

**예제 코드 — [05_sort_search.cpp](./examples/05_sort_search.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> delays{42, 18, 31, 18, 55};
    const auto high = std::ranges::count_if(delays, [](int value) { return value >= 40; });
    const long long total = std::accumulate(delays.begin(), delays.end(), 0LL);
    std::ranges::sort(delays);
    std::cout << "Total: " << total << '\n';
    std::cout << "Slow: " << high << '\n';
    std::cout << std::boolalpha;
    std::cout << "Has 31: " << std::ranges::binary_search(delays, 31) << '\n';
    std::cout << "First sorted: " << delays.front() << '\n';
}
```

**실행 결과**

```text
Total: 164
Slow: 2
Has 31: true
First sorted: 18
```

`std::ranges::count_if(delays, ...)`에 전달한 람다는 Chapter 05에서 다룬 조건 함수입니다. `std::accumulate(..., 0LL)`의 `0LL`은 `long long` 정수 리터럴이므로 누적 계산 타입을 `long long`으로 선택하도록 합니다. 다만 큰 값이 계속 누적되면 이 타입도 오버플로될 수 있습니다.

대표적인 작업량은 전체 순회 `O(n)`, 비교 정렬 `O(n log n)`, 정렬된 범위의 이진 검색 `O(log n)`입니다. 여기서 `n`은 요소 개수이며, 자세한 성능 분석은 별도 알고리즘 학습 과정과 연결됩니다.

<a id="section-6-7"></a>
## 6.7. Non-Owning Views — `std::span`

`std::span<T>`은 **C++20에서 도입된 연속 데이터 뷰(Contiguous View)** 입니다. 기존 배열의 요소를 복사하지 않고, 시작 위치와 요소 개수를 함께 전달할 때 사용합니다.

`#include <span>`은 `std::span`을 사용하기 위한 표준 헤더입니다.

- `std::span<int>`: 원본 요소를 수정할 수 있는 뷰
- `std::span<const int>`: 원본 요소를 변경하지 않고 읽는 뷰

`std::array`와 `std::vector`는 각자 데이터를 소유하지만, `std::span`은 **데이터를 소유하지 않습니다.** 따라서 뷰를 사용하는 동안 원본의 수명이 유지되어야 하고, 원본 `vector`에 대한 크기 변경·재할당 뒤에는 이전 뷰의 유효성을 다시 확인해야 합니다.

**예제 코드 — [06_span_view.cpp](./examples/06_span_view.cpp)**

```cpp
#include <array>
#include <iostream>
#include <span>
#include <vector>

[[nodiscard]] int sum_readings(std::span<const int> readings) {
    int total{};
    for (const int value : readings) total += value;
    return total;
}

int main() {
    const std::array<int, 3> fixed{10, 20, 30};
    const std::vector<int> dynamic{4, 6};
    std::cout << "Array total: " << sum_readings(fixed) << '\n';
    std::cout << "Vector total: " << sum_readings(dynamic) << '\n';
}
```

**실행 결과**

```text
Array total: 60
Vector total: 10
```

같은 `sum_readings()` 함수가 `std::array`와 `std::vector`를 모두 받을 수 있는 것이 장점입니다. 단, 모든 컨테이너의 데이터가 연속 저장되는 것은 아니므로 `std::span`을 모든 종류의 컨테이너에 적용할 수 있는 것은 아닙니다.

<a id="section-6-8"></a>
## 6.8. Multidimensional Data

행(Row)과 열(Column)을 가진 격자는 2차원 배열로 표현할 수 있습니다. 고정된 크기의 경우 `std::array<std::array<int, C>, R>`처럼 배열 안에 배열을 저장할 수 있습니다.

```cpp
std::array<std::array<int, 3>, 2> grid{{
    {0, 1, 0},
    {1, 0, 0}
}};
```

`grid.at(1).at(0)`은 두 번째 행의 첫 번째 요소입니다. 행과 열도 모두 0부터 시작합니다. 중첩 반복문에서는 바깥 반복이 행, 안쪽 반복이 각 행의 열을 담당합니다.

**예제 코드 — [07_two_dimensional_array.cpp](./examples/07_two_dimensional_array.cpp)**

```cpp
#include <array>
#include <iostream>

int main() {
    const std::array grid{
        std::array{0, 1, 0, 0},
        std::array{1, 0, 0, 1},
        std::array{0, 0, 1, 0},
    };
    int blocked{};
    for (const auto& row : grid) {
        for (const int cell : row) {
            if (cell == 1) ++blocked;
        }
    }
    std::cout << "Rows: " << grid.size() << '\n';
    std::cout << "Columns: " << grid.front().size() << '\n';
    std::cout << "Blocked: " << blocked << '\n';
    std::cout << "Cell (1, 3): " << grid.at(1).at(3) << '\n';
}
```

**실행 결과**

```text
Rows: 3
Columns: 4
Blocked: 4
Cell (1, 3): 1
```

실행 중 크기가 달라지는 격자에는 `std::vector<std::vector<int>>` 등을 사용할 수 있지만 행별 저장 공간이 따로 구성될 수 있습니다. 실제로 연속된 1차원 메모리가 필요하다면 인덱스를 `row * width + col`로 계산하는 방식도 있으며, 이때는 행·열 범위와 곱셈 결과를 검사해야 합니다.

<a id="section-6-9"></a>
## 6.9. String Operations — `std::string`

`std::string`은 문자열 데이터를 소유하고 관리하는 표준 라이브러리 타입입니다. Chapter 01에서는 입력·출력에 활용했으며, 이번에는 문자열 내부를 검색하고 수정하는 방법을 배웁니다.

| 멤버 함수 | 역할 | 특징 |
|---|---|---|
| `size()` | 문자열 크기 | 바이트 수이며 UTF-8 글자 수가 아닐 수 있음 |
| `empty()` | 비어 있는지 검사 | 길이가 0이면 `true` |
| `find(text)` | 부분 문자열의 시작 위치 검색 | 없으면 `std::string::npos` |
| `substr(pos, count)` | 부분 문자열 복사 | 새 `std::string` 생성 |
| `starts_with(text)` | 특정 문자열로 시작하는지 검사 | C++20 |
| `ends_with(text)` | 특정 문자열로 끝나는지 검사 | C++20 |

`std::string::npos`는 검색 결과가 없다는 뜻을 나타내는 특별한 값입니다. `find()` 결과를 인덱스로 사용하기 전 반드시 검색 성공 여부를 확인해야 합니다.

**예제 코드 — [08_string_methods.cpp](./examples/08_string_methods.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    std::string device{"SENSOR-ROOM-07"};
    std::cout << std::boolalpha;
    std::cout << "Prefix: " << device.starts_with("SENSOR-") << '\n';
    std::cout << "Suffix: " << device.ends_with("-07") << '\n';
    std::cout << "Contains ROOM: " << (device.find("ROOM") != std::string::npos) << '\n';
    const auto first_dash = device.find('-');
    std::cout << "Category: " << device.substr(0, first_dash) << '\n';
    device += "-A";
    std::cout << "Updated: " << device << '\n';
}
```

**실행 결과**

```text
Prefix: true
Suffix: true
Contains ROOM: true
Category: SENSOR
Updated: SENSOR-ROOM-07-A
```

이 예제의 `Contains ROOM`은 `find("ROOM") != std::string::npos`로 검사합니다. **C++23**에서는 `device.contains("ROOM")`로 더 간결하게 표현할 수 있지만, `contains()`는 C++20의 기본 문자열 기능이 아니므로 기본 예제에서는 사용하지 않습니다.

<a id="section-6-10"></a>
## 6.10. Line Input — `std::getline()`

입력 연산자 `std::cin >> name`은 일반적으로 공백에서 입력을 구분하므로 `LiDAR Front`를 입력하면 `LiDAR`까지만 읽습니다. 반면 `std::getline(std::cin, name)`은 줄바꿈 전까지의 한 줄을 읽기 때문에 공백을 포함한 문자열을 받을 수 있습니다.

입력 실패나 파일 끝(EOF)에 도달한 경우 `std::getline()`은 실패 상태로 평가됩니다. 문자열이 비어 있는지 별도로 검사하면 필수 입력값을 확인할 수 있습니다.

**예제 코드 — [09_line_input.cpp](./examples/09_line_input.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    std::string device;
    std::cout << "Device: " << std::flush;
    if (!std::getline(std::cin, device) || device.empty()) {
        std::cerr << "Error: device name required.\n";
        return 1;
    }
    std::cout << "Registered: " << device << '\n';
}
```

**실행 결과**

```text
Device: LiDAR Front Left
Registered: LiDAR Front Left
```

예시는 사용자가 `LiDAR Front Left`를 입력했을 때의 터미널 표시입니다. 테스트에서는 프롬프트 뒤에 입력 에코가 포함되지 않는 환경을 기준으로 출력 자체만 검증합니다.

**주의:** `std::cin >> count`로 숫자를 읽은 직후 `getline()`을 사용하면 남아 있는 개행 문자가 읽힐 수 있습니다. 이때 숫자 입력을 한 줄 전체로 제한했다면 `std::getline(std::cin, remainder)`로 남은 줄을 읽거나, 처음부터 모든 입력을 한 줄씩 처리해 파싱할 수 있습니다. 단순히 `ignore()`를 무조건 호출하면 이미 필요한 문자가 소실될 수도 있으므로 입력 형식을 먼저 정의해야 합니다.

<a id="section-6-11"></a>
## 6.11. String Views — `std::string_view`

`std::string_view`는 **문자열을 복사하지 않고 읽는 뷰**로, Chapter 05에서 함수의 매개변수로 사용했습니다. `std::string`과 달리 내부 문자 데이터를 직접 소유하지 않으므로 뷰를 보관하는 동안 원본이 유효해야 합니다.

`#include <string_view>`는 `std::string_view`를 선언·사용할 때 필요한 헤더입니다.

| 구문 | 반환 타입 | 원본 데이터 복사 |
|---|---|---|
| `std::string::substr(...)` | `std::string` | O |
| `std::string_view::substr(...)` | `std::string_view` | X |

반환한 뷰가 원본의 일부를 계속 가리키는지 확인해야 하며, 지역 임시 문자열의 수명이 끝난 뒤 해당 문자열을 가리키는 뷰를 사용해서는 안 됩니다.

**예제 코드 — [10_string_view.cpp](./examples/10_string_view.cpp)**

```cpp
#include <iostream>
#include <string>
#include <string_view>

[[nodiscard]] std::string_view category_of(std::string_view identifier) {
    const auto separator = identifier.find(':');
    if (separator == std::string_view::npos) return {};
    return identifier.substr(0, separator);
}

int main() {
    const std::string owned{"MOTOR:FRONT-LEFT"};
    const std::string_view category = category_of(owned);
    std::cout << "Category: " << category << '\n';
}
```

**실행 결과**

```text
Category: MOTOR
```

`category_of()`가 `std::string_view`를 반환하더라도 호출자의 `owned` 문자열은 계속 살아 있으므로 안전하게 출력할 수 있습니다. 반대로 사라진 임시 `std::string`을 가리키는 뷰는 댕글링 뷰(Dangling View)가 될 수 있습니다.

<a id="section-6-12"></a>
## 6.12. Numeric Parsing — `std::from_chars()`

외부에서 읽은 `"42"`는 숫자 42가 아니라 숫자로 보이는 **문자열**입니다. 정수로 계산하려면 문자열의 문자들을 실제 정수값으로 변환(Parsing)해야 합니다.

`std::from_chars()`는 **C++17**에서 도입된 숫자 변환 함수입니다. 문자열 범위와 결과 변수에 대한 접근을 받아, 변환이 끝난 위치와 오류 상태를 반환합니다. 공백을 자동으로 무시하지 않으며, 정수 변환에서 선행 `+` 기호도 허용하지 않습니다.

| 헤더 | 역할 |
|---|---|
| `<charconv>` | `std::from_chars()` 등 문자와 숫자 간 변환 기능 |
| `<system_error>` | 변환 결과의 `std::errc` 오류 코드 타입 |

```cpp
const auto [next, error] = std::from_chars(first, last, value);
```

`next`는 변환이 끝난 위치이고 `error`는 변환 성공 여부를 나타냅니다. **부분 변환을 잘못 인정하지 않으려면** `error == std::errc{}`와 `next == last`를 함께 검사해야 합니다.

**예제 코드 — [11_from_chars.cpp](./examples/11_from_chars.cpp)**

```cpp
#include <charconv>
#include <iostream>
#include <string_view>
#include <system_error>

[[nodiscard]] bool parse_int(std::string_view text, int& value) {
    const char* first = text.data();
    const char* last = first + text.size();
    const auto [next, error] = std::from_chars(first, last, value);
    return error == std::errc{} && next == last;
}

int main() {
    for (const std::string_view text : {"42", "42ms", "-7"}) {
        int result{};
        if (parse_int(text, result)) {
            std::cout << "Accepted: " << result << '\n';
        } else {
            std::cout << "Rejected: " << text << '\n';
        }
    }
}
```

**실행 결과**

```text
Accepted: 42
Rejected: 42ms
Accepted: -7
```

`42ms`는 처음의 `42`까지 변환될 수 있지만 `next`가 마지막 위치와 다르므로 거부됩니다. 앞뒤 공백을 허용하려면 먼저 허용할 공백 문자의 범위를 정의하고 제거한 뒤 변환하는 과정이 필요합니다.

<a id="section-6-13"></a>
## 6.13. Delimited Text

구분자(Delimiter)는 텍스트의 여러 필드를 나누는 문자입니다. 예를 들어 `ROOM-01|OK`를 `|`로 나누면 장치명과 상태값을 분리할 수 있습니다.

단순 분리만으로는 데이터가 유효하다고 판단할 수 없습니다. **구분자가 없거나 너무 많지 않은지, 빈 필드는 없는지, 각 필드의 값이 허용 범위에 있는지**를 검사해야 합니다.

**예제 코드 — [12_delimited_fields.cpp](./examples/12_delimited_fields.cpp)**

```cpp
#include <iostream>
#include <string>
#include <string_view>

[[nodiscard]] bool split_record(std::string_view text,
                                std::string_view& device,
                                std::string_view& status) {
    const auto separator = text.find('|');
    if (separator == std::string_view::npos || separator == 0 ||
        separator + 1 == text.size() || text.find('|', separator + 1) != std::string_view::npos) {
        return false;
    }
    device = text.substr(0, separator);
    status = text.substr(separator + 1);
    return true;
}

int main() {
    for (const std::string_view record : {"ROOM-01|OK", "ROOM-02|WARN|EXTRA"}) {
        std::string_view device;
        std::string_view status;
        if (split_record(record, device, status)) {
            std::cout << device << ": " << status << '\n';
        } else {
            std::cout << "Rejected: " << record << '\n';
        }
    }
}
```

**실행 결과**

```text
ROOM-01: OK
Rejected: ROOM-02|WARN|EXTRA
```

이 예제는 `|`가 정확히 한 개이고 양쪽 값이 비어 있지 않은지만 검사합니다. 상태값을 `OK` 또는 `WARN`으로 제한하려면 별도의 검증을 추가해야 합니다. 인용 부호, 이스케이프 및 줄바꿈 규칙이 있는 **CSV·JSON 전체 형식의 파서**로 이 간단한 분리 코드를 그대로 사용해서는 안 됩니다.

<a id="section-6-14"></a>
## 6.14. UTF-8 & Text Length

문자열의 `size()`는 메모리에 저장된 **바이트(Byte) 단위의 길이**를 반환합니다. UTF-8은 영문 ASCII 문자는 보통 1바이트로, 한글 음절은 보통 3바이트로 인코딩합니다. 따라서 **바이트 수와 눈에 보이는 글자 수는 서로 다를 수 있습니다.**

| 구분 | 의미 |
|---|---|
| Bit(비트) | 0 또는 1을 나타내는 정보 단위 |
| Byte(바이트) | C++에서 `char` 한 개의 크기. `CHAR_BIT` 비트로 구성 |
| Code Point(코드 포인트) | 유니코드 문자를 식별하는 번호 |
| Grapheme Cluster(문자소 클러스터) | 사용자에게 하나의 글자처럼 보이는 문자 단위 |

일반적인 PC 환경에서 1바이트는 8비트지만, C++이 모든 플랫폼에서 8비트를 강제하는 것은 아닙니다. `<climits>`에 정의된 `CHAR_BIT`로 해당 실행 환경의 바이트당 비트 수를 확인할 수 있습니다.

**예제 코드 — [13_utf8_bytes.cpp](./examples/13_utf8_bytes.cpp)**

```cpp
#include <climits>
#include <iostream>
#include <string>

int main() {
    const std::string ascii{"ABC"};
    const std::string korean{"가"}; // UTF-8 소스 및 실행 문자 인코딩 가정
    std::cout << "Bits per byte: " << CHAR_BIT << '\n';
    std::cout << "ASCII bytes: " << ascii.size() << '\n';
    std::cout << "Korean bytes (UTF-8): " << korean.size() << '\n';
}
```

**실행 결과**

```text
Bits per byte: 8
ASCII bytes: 3
Korean bytes (UTF-8): 3
```

이 실행 결과는 UTF-8 소스·실행 문자 인코딩과 8비트 바이트 환경을 가정합니다. 다른 플랫폼이나 문자 인코딩에서는 결과가 달라질 수 있습니다. UTF-8 문자열의 `text[i]`는 글자 하나가 아니라 **바이트 하나**이므로 임의의 인덱스로 잘라내면 문자가 깨질 수 있습니다. 정확한 사용자 표시 글자 수 계산에는 전문적인 유니코드 처리 기능이 필요할 수 있습니다.

<a id="section-6-15"></a>
## 6.15. Container Selection & C-Style Arrays

C++에는 표준 라이브러리 컨테이너뿐 아니라 C 스타일 배열(C-Style Array)도 존재합니다.

```cpp
int raw[3]{10, 20, 30};
```

다만 함수에 전달할 때 배열의 크기 정보가 쉽게 사라질 수 있으므로 새 코드를 작성할 때는 크기를 함께 관리하기 편한 `std::array`, `std::vector`, `std::span`을 고려하는 편이 좋습니다. C 라이브러리나 하드웨어 API와 연결해야 하는 경우에는 기존 배열과 포인터 형식이 필요할 수 있으며, 포인터 자체는 Chapter 07에서 자세히 학습합니다.

| 상황 | 우선 고려할 타입 | 이유 |
|---|---|---|
| 요소 개수가 고정됨 | `std::array` | 고정 크기, 값 소유 |
| 요소 개수가 바뀜 | `std::vector` | 크기 변경, 연속 저장 |
| 연속 데이터를 함수에서 읽기만 함 | `std::span<const T>` | 데이터 복사 없이 요소와 길이 전달 |
| 저장하거나 수정할 텍스트 | `std::string` | 문자열 직접 소유 |
| 짧게 읽기만 할 텍스트 | `std::string_view` | 복사 없이 범위 참조 |

`std::vector`의 마지막 요소 추가는 평균적으로 **분할 상환(Amortized) `O(1)`** 이지만 용량 확장 시에는 더 큰 비용이 발생할 수 있습니다. 중간 삽입·삭제는 일반적으로 `O(n)`의 이동 비용이 발생합니다. 우선 데이터의 소유, 크기 변경 여부, 접근 방식이 정확한 타입을 선택하는 것이 중요합니다.

<a id="section-6-16"></a>
## 6.16. Coding Practice

`exercises/`에 미완성 코드를, `solutions/`에 모범답안을 제공합니다. 문제에서 지정한 입력 형식과 출력 결과를 확인한 뒤 직접 구현합니다.

| No. | Practice | Exercise | Solution |
|:---:|---|---|---|
| 01 | Vector Statistics | [문제 코드](./exercises/01_vector_statistics.cpp) | [정답 코드](./solutions/01_vector_statistics.cpp) |
| 02 | Device Lookup | [문제 코드](./exercises/02_device_lookup.cpp) | [정답 코드](./solutions/02_device_lookup.cpp) |
| 03 | Comma-Separated Values | [문제 코드](./exercises/03_comma_separated_values.cpp) | [정답 코드](./solutions/03_comma_separated_values.cpp) |
| 04 | Grid Border Check | [문제 코드](./exercises/04_grid_border.cpp) | [정답 코드](./solutions/04_grid_border.cpp) |

### Exercise 01 — Vector Statistics

1~20개의 센서 측정값을 입력받아 `std::vector`에 저장하고 통계를 출력합니다.

**구현 조건**

- 첫 번째 입력: 정수 `N` (`1~20`)
- 이어서 정확히 `N`개의 측정값 입력 (각 `-100~100`)
- 최솟값, 최댓값, 평균을 소수 둘째 자리까지 출력
- 입력 실패나 범위 초과 시 `std::cerr`에 `Error: invalid input.` 출력 후 오류 종료

**입력**

```text
5
18 22 22 25 13
```

**출력**

```text
Count: 5
Min: 13
Max: 25
Average: 20.00
```

### Exercise 02 — Device Lookup

여러 장치 이름 중 원하는 이름과 정확히 일치하는 첫 번째 항목을 찾습니다.

**구현 조건**

- 장치 개수 `N`: `1~10`
- 다음 `N`줄: 장치 이름(공백 포함 가능, 빈 문자열 금지)
- 마지막 줄: 검색할 장치 이름
- 이름 비교는 대소문자를 구분하며, 중복 이름은 먼저 발견된 위치를 사용
- 위치는 **1부터 시작**하여 출력하며, 없으면 `Not found` 출력

**입력**

```text
3
Motor A
LiDAR Front
IMU Main
LiDAR Front
```

**출력**

```text
Found: LiDAR Front (index 2)
```

### Exercise 03 — Comma-Separated Values

한 줄에 쉼표로 구분된 정수 값을 읽어 개수와 합계를 계산합니다.

**구현 조건**

- 정수 개수: `1~10`, 각 값은 `-100~100`
- 값 앞뒤의 ASCII 스페이스(` `)는 허용
- 빈 필드, 숫자 뒤 문자, 허용 범위 초과는 오류
- 원소 개수와 합계를 출력. 오류 출력 형식은 `Error: invalid input.`

**입력**

```text
20,25,19,21
```

**출력**

```text
Count: 4
Sum: 85
```

**오류 사례:** `20,,30`, `20,30ms`, `20,101`, `20,`

### Exercise 04 — Grid Border Check

`#`가 장애물이고 `.`이 빈 공간인 격자에서 장애물 수와 외곽 장애물 여부를 확인합니다.

**구현 조건**

- 첫 줄: `width height` (각 `1~20`)
- 이어서 `height`줄: 길이가 정확히 `width`인 `.` 또는 `#` 문자열
- 전체 장애물 개수를 세고 상·하·좌·우 테두리에 장애물이 없는지 확인
- 가로 또는 세로 크기가 `1`인 격자도 올바르게 처리

**입력**

```text
4 3
....
.#..
....
```

**출력**

```text
Blocked: 1
Borders clear: yes
```

### 실행 및 검증

`Chapter-06/` 디렉터리에서 다음 명령어를 실행합니다.

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic solutions/01_vector_statistics.cpp -o vector_statistics
./vector_statistics
```

Python 3이 설치되어 있다면 다음 테스트를 실행할 수 있습니다.

```bash
python3 tests/check.py
python3 tests/check.py --exercise 01
```

**첫 번째 명령어**는 예제와 모범답안을 확인하는 용도입니다. **두 번째 명령어**는 직접 수정한 Exercise 01을 검사합니다. 아직 코드를 작성하지 않은 초기 상태에서는 FAIL이 나오는 것이 정상입니다. 테스트는 C++20으로 컴파일한 다음 다양한 입력값으로 표준 출력, 오류 출력, 종료 코드를 검증합니다.

<a id="section-6-17"></a>
## 6.17. Mini Project — Sensor Batch Report

장치 이름과 쉼표로 구분된 측정값을 입력받아 **정렬 및 통계 보고서**를 생성하는 콘솔 프로그램입니다. `std::string`, `std::string_view`, `std::vector`, `std::from_chars()`, `std::ranges::sort` 등을 함께 사용합니다.

**파일 구성**

- [실습 코드 — sensor_batch_report.cpp](./project/sensor_batch_report.cpp)
- [모범답안 — sensor_batch_report.cpp](./solutions/sensor_batch_report.cpp)

**입력 조건**

1. 첫 줄: 장치 이름(비어 있지 않은 문자열, 공백 포함 가능)
2. 두 번째 줄: 쉼표로 구분한 정수 `1~20`개, 각 `-100~100`
3. 정수 앞뒤의 ASCII 공백은 허용하지만, 빈 필드·숫자 뒤 문자·범위 밖 값은 거부

**입력**

```text
LiDAR Front
18, 22, 19, 24
```

**실행 예시**

```text
Device: LiDAR Front
Readings (-100 to 100, comma-separated): 18, 22, 19, 24

--- Sensor Batch Report ---
Device: LiDAR Front
Count: 4
Minimum: 18
Maximum: 24
Average: 20.75
Sorted: 18, 19, 22, 24
```

**구현 흐름**

```text
장치 이름 입력
      ↓
쉼표 구분 문자열 입력
      ↓
문자열 분할 → 공백 제거 → 정수 전체 변환 및 범위 검사
      ↓
벡터에 측정값 저장 → 합계·최솟값·최댓값·평균 계산
      ↓
정렬한 목록과 보고서 출력
```

**완료 기준**

- **문자열 보존:** 공백이 포함된 장치 이름을 온전히 처리합니다.
- **입력 형식 검증:** 측정값의 개수, 범위, 빈 필드, 숫자 뒤 문자를 검사합니다.
- **정렬 및 통계:** 음수·중복·단일 측정값에서도 최솟값·최댓값·평균과 오름차순 목록이 정확합니다.
- **오류 처리:** 장치 이름이 비어 있으면 `Error: invalid device.`, 측정값이 잘못되면 `Error: invalid readings.`를 `std::cerr`로 출력하고 비정상 종료합니다.
- **빌드:** `g++ -std=c++20`으로 정상 컴파일됩니다.

**컴파일 및 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/sensor_batch_report.cpp -o sensor_report
./sensor_report
```

**자동 검증**

```bash
python3 tests/check.py
python3 tests/check.py --project
```

**첫 번째 명령어**는 예제와 모범답안을 확인하는 용도입니다. **두 번째 명령어**는 직접 수정한 프로젝트 파일을 검사합니다. 아직 코드를 작성하지 않아 초기 상태에는 FAIL이 나오는 것이 정상입니다.

해당 프로젝트는 한 번 입력받아 보고서를 출력하는 콘솔 프로그램입니다. 입력을 바꾸고 다시 실행하면 변경된 데이터에 맞는 보고서가 생성됩니다.

<a id="section-6-18"></a>
## 6.18. Quiz & Summary

### Quiz

먼저 문제를 풀고, 각 항목의 **정답 및 해설**을 펼쳐 확인합니다.

**Q1. 다음 중 요소 수가 실행 중 변경되는 데이터를 저장하기에 가장 적합한 타입은 무엇인가요?**

A. `std::array`  
B. `std::vector`  
C. `std::span`  
D. `std::string_view`

<details>
<summary>정답 및 해설</summary>

**정답: B**

`std::vector`는 요소의 추가·삭제로 크기를 변경할 수 있습니다. A는 요소 개수가 고정되고, C와 D는 데이터를 직접 소유하지 않는 뷰이므로 역할이 다릅니다.

</details>

**Q2. `std::array<int, 4>`의 마지막 요소에 접근할 때 사용할 수 있는 인덱스는 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

**정답: `3`**

배열 인덱스는 0부터 시작하므로 네 요소의 인덱스는 `0, 1, 2, 3`입니다. `4`는 범위를 벗어납니다.

</details>

**Q3. 비어 있는 `std::vector<int> values;`에 `values.reserve(100);`을 호출했습니다. 직후 `values.size()`의 값은 무엇인가요?**

A. 0  
B. 1  
C. 100  
D. 구현마다 달라짐

<details>
<summary>정답 및 해설</summary>

**정답: A**

`reserve()`는 저장 용량만 늘릴 뿐 실제 요소를 생성하지 않습니다. `size()`는 0이고 `values[0]`에도 접근해서는 안 됩니다. `resize(100)`은 요소 수를 100으로 변경합니다.

</details>

**Q4. `container[index]`와 `container.at(index)`의 차이를 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**정답 예시:** `[]`는 범위 검사를 보장하지 않아 잘못된 인덱스로 접근하면 미정의 동작이 발생할 수 있습니다. `at()`은 범위 초과를 검사하고 `std::out_of_range` 예외를 발생시킵니다.

`at()`도 비어 있는 컨테이너를 안전한 값으로 바꿔 주지는 않으므로 적절한 오류 처리가 필요합니다.

</details>

**Q5. 다음 중 `std::ranges::binary_search`에 필요한 전제 조건은 무엇인가요?**

A. 요소 개수가 반드시 짝수여야 합니다.  
B. 검색 기준에 맞게 정렬되어 있어야 합니다.  
C. `std::vector`만 사용할 수 있습니다.  
D. 모든 요소가 달라야 합니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

이진 탐색은 정렬된 범위를 이용해 탐색 범위를 줄입니다. A와 D는 필요 없는 조건이고, C도 틀렸습니다. 적합한 범위와 비교 기준을 만족하면 `std::array` 등에서도 사용할 수 있습니다.

</details>

**Q6. `std::span<const int>`을 사용하는 주된 목적은 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

**정답 예시:** 연속된 원본 데이터를 복사하지 않고 읽기 전용으로 함수에 전달하기 위해 사용합니다. 길이 정보와 함께 접근할 수 있지만 원본 데이터를 소유하지 않습니다.

원본이 사라지거나 재할당되는 경우에는 뷰가 유효하지 않을 수 있습니다.

</details>

**Q7. `std::string`의 `find()`가 부분 문자열을 찾지 못하면 어떤 값을 반환하나요?**

A. `-1`  
B. `0`  
C. `std::string::npos`  
D. `nullptr`

<details>
<summary>정답 및 해설</summary>

**정답: C**

검색 실패 여부는 `std::string::npos`와 비교합니다. A의 `-1`은 해당 API가 보장하는 명시적 실패 표현이 아니고, B의 `0`은 문자열 맨 앞에서 찾았을 때의 정상 위치입니다. D는 이 함수가 반환하는 실패 값이 아닙니다.

</details>

**Q8. `std::from_chars()`로 `"25ms"`를 정수로 읽었습니다. 변환이 완전히 성공했는지 추가로 무엇을 검사해야 하나요?**

<details>
<summary>정답 및 해설</summary>

**정답 예시:** 오류 코드가 `std::errc{}`인지 확인하고, 변환 종료 위치 `next`가 입력의 끝 `last`와 일치하는지 확인합니다.

`25ms`는 숫자 `25`까지만 변환될 수 있으므로 오류 코드만 검사하면 잘못된 전체 입력을 허용할 수 있습니다.

</details>

**Q9. UTF-8로 저장된 한글 음절 `"가"`에 대해 일반적인 8비트 바이트 환경에서 `std::string::size()` 결과는 무엇인가요?**

A. 1  
B. 2  
C. 3  
D. 8

<details>
<summary>정답 및 해설</summary>

**정답: C**

UTF-8에서 `가`는 3바이트로 인코딩됩니다. `std::string::size()`는 글자 수가 아니라 바이트 수를 반환하므로 3입니다. 이 설명은 UTF-8 인코딩을 전제로 합니다.

</details>

**Q10. 장치 이름이 `"LiDAR Front Left"`처럼 공백을 포함할 때 어떤 입력 방식이 적합한가요?**

<details>
<summary>정답 및 해설</summary>

**정답 예시:** `std::getline(std::cin, device)`를 사용합니다. `std::cin >> device`는 공백을 기준으로 입력을 나누기 때문에 전체 이름을 읽지 못합니다.

그 전에 `std::cin >> count`를 사용했다면 남아 있는 개행 문자도 주의해야 합니다.

</details>

**Q11. `std::string::substr()`와 `std::string_view::substr()`의 차이는 무엇인가요?**

A. 둘 다 항상 새 문자열을 복사합니다.  
B. 앞쪽은 새 문자열을 만들고, 뒤쪽은 원본의 일부를 가리키는 뷰를 반환합니다.  
C. 뒤쪽은 원본 문자열의 저장 공간을 소유합니다.  
D. 앞쪽은 C++23에서만 사용할 수 있습니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

`std::string::substr()`는 새 문자열 값을 반환하지만, `std::string_view::substr()`는 원본 데이터를 복사하지 않는 뷰를 반환합니다. 뷰를 보관할 경우 원본 데이터의 수명을 확인해야 합니다.

</details>

**Q12. 가로 3칸, 세로 1칸의 격자에서 중간 칸이 장애물(`#`)입니다. 바깥 테두리에 장애물이 없는 격자인가요? 이유도 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**정답: 아니요.**

세로 크기가 1이면 모든 칸이 동시에 윗변과 아랫변에 놓여 있습니다. 따라서 가운데 칸도 테두리이며, `#`가 하나 있으므로 테두리가 비어 있지 않습니다. 격자의 가로 또는 세로 크기가 1인 경계 사례를 테스트해야 하는 이유입니다.

</details>

### Summary

- **`std::array`:** 크기가 정해진 데이터의 저장과 접근
- **`std::vector`:** 요소 추가·삭제가 가능한 연속 데이터 컨테이너
- **`reserve()` / `resize()`:** 용량 확보와 실제 요소 개수 변경의 구분
- **인덱스·범위 검사:** `[]`와 `at()`의 동작 차이, 빈 컨테이너 검사
- **순회와 집계:** 범위 기반 `for`, 누적 합계, 평균·최솟값·최댓값
- **표준 알고리즘:** 정렬·검색·조건별 개수 계산, 정렬 전제 조건
- **`std::span`:** 원본을 소유하지 않는 C++20 연속 데이터 뷰
- **다차원 배열:** 행·열 인덱스와 중첩 반복 처리
- **`std::string`:** 텍스트 저장, 검색, 수정 및 부분 문자열 복사
- **`std::getline()`:** 공백을 포함하는 한 줄 입력
- **`std::string_view`:** 원본을 복사하지 않는 읽기 전용 문자열 뷰
- **`std::from_chars()`:** 정수 변환과 전체 입력 소비 여부 검증
- **UTF-8:** 바이트 수와 화면에 표시되는 글자 수 구분

### References

- [cppreference — `std::array`](https://en.cppreference.com/w/cpp/container/array)
- [cppreference — `std::vector`](https://en.cppreference.com/w/cpp/container/vector)
- [cppreference — `std::span`](https://en.cppreference.com/w/cpp/container/span)
- [cppreference — `std::basic_string`](https://en.cppreference.com/w/cpp/string/basic_string)
- [cppreference — `std::string_view`](https://en.cppreference.com/w/cpp/string/basic_string_view)
- [cppreference — `std::from_chars`](https://en.cppreference.com/w/cpp/utility/from_chars)
- [cppreference — Ranges algorithms](https://en.cppreference.com/w/cpp/algorithm/ranges)
- [cppreference — `std::accumulate`](https://en.cppreference.com/w/cpp/algorithm/accumulate)
- [cppreference — `CHAR_BIT`](https://en.cppreference.com/w/cpp/types/climits)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

---

[← C++ 목차](../README.md#contents)

