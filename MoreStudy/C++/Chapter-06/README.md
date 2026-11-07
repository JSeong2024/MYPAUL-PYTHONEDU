# Chapter 06. Arrays & Strings

배열과 문자열의 저장 방식, 요소 접근, 반복 처리, 검색 및 변환을 다룹니다. 고정 크기 배열과 동적 배열을 구분하고, 문자열 입력과 외부 데이터 처리 시 필요한 안전성도 함께 살펴봅니다.

본 자료는 **C++23(ISO/IEC 14882:2024)** 을 기준으로 작성되었습니다. 예제는 GCC 14 이상 또는 C++23 표준 라이브러리 지원이 충분한 개발 환경을 권장합니다.

## Contents

| Section | Topic |
|:---:|---|
| 6.1 | 배열과 문자열의 역할 |
| 6.2 | 고정 크기 배열 — `std::array` |
| 6.3 | 가변 크기 배열 — `std::vector` |
| 6.4 | 인덱스와 안전한 요소 접근 |
| 6.5 | 반복 처리, 검색, 정렬 및 집계 |
| 6.6 | 연속 데이터의 뷰 — `std::span` |
| 6.7 | 다차원 배열과 격자 데이터 |
| 6.8 | 문자열 저장과 조작 — `std::string` |
| 6.9 | 공백을 포함한 문자열 입력 — `std::getline` |
| 6.10 | 소유하지 않는 문자열 — `std::string_view` |
| 6.11 | 문자열을 숫자로 변환 — `std::from_chars` |
| 6.12 | UTF-8과 문자열 길이 |
| 6.13 | 구분자로 구성된 데이터 처리 |
| 6.14 | C 스타일 배열과 메모리 관리 |
| 6.15 | 컨테이너 선택 및 성능 고려 |
| 6.16 | Coding Practice |
| 6.17 | Quiz & Summary |

---

## 6.1. 배열과 문자열의 역할

동일한 종류의 값을 여러 개 처리할 때 배열을 사용합니다. 예를 들어 온도 센서의 최근 측정값, 장치 목록, 영상의 픽셀 데이터 등을 개별 변수로 관리하면 반복 처리와 범위 검증이 어려워집니다.

```cpp
int first{21};
int second{24};
int third{19};
```

배열을 사용하면 데이터를 하나의 객체로 관리하고 반복문과 표준 알고리즘을 적용할 수 있습니다.

```cpp
#include <array>

std::array<int, 3> readings{21, 24, 19};
```

문자열은 텍스트 데이터에 특화된 객체입니다. 장치 이름, 로그 메시지, 사용자 입력, 프로토콜 명령어 등을 표현할 때 사용합니다.

| 자료형 | 역할 | 크기 | 요소 소유 여부 |
|---|---|---|---|
| `std::array<T, N>` | 고정 개수의 동일 자료형 요소 | 컴파일 시점에 결정 | 소유 |
| `std::vector<T>` | 실행 중 늘어나거나 줄어드는 요소 | 실행 시점에 변경 가능 | 소유 |
| `std::span<T>` | 연속된 요소들의 범위 참조 | 고정/동적 범위 지원 | 소유하지 않음 |
| `std::string` | 변경 가능한 문자열 | 실행 시점에 변경 가능 | 소유 |
| `std::string_view` | 읽기 전용 문자열 범위 참조 | 실행 시점에 결정 | 소유하지 않음 |

**기본 원칙:** 데이터의 소유권(Ownership)을 갖는 객체와, 데이터를 소유하지 않고 참조하는 뷰(View)를 구분합니다. View를 사용할 때는 원본 객체의 수명(Lifetime)을 보장해야 합니다.

---

## 6.2. 고정 크기 배열 — `std::array`

`std::array<T, N>`은 요소의 수가 고정되어 있을 때 사용합니다. 센서 채널 수, 장치별 고정 파라미터, 색상 채널처럼 요소 개수가 설계상 일정한 데이터에 적합합니다.

```cpp
#include <array>

std::array<int, 4> channels{10, 20, 30, 40};
```

- **`int`:** 배열 요소의 자료형
- **`4`:** 요소 개수. 컴파일 시점에 결정
- **`channels.size()`:** 요소 개수 조회
- **`channels[0]`:** 첫 번째 요소 접근. 인덱스 검사 없음
- **`channels.at(0)`:** 범위를 검사하며 요소 접근

배열의 첫 번째 요소 인덱스는 `0`, 마지막 요소 인덱스는 `size() - 1`입니다. `std::array`의 크기는 생성한 뒤 변경할 수 없습니다.

**예제 코드 — [01_std_array.cpp](./examples/01_std_array.cpp)**

```cpp
#include <algorithm>
#include <array>
#include <print>

int main() {
    constexpr std::array<int, 5> readings{21, 24, 19, 23, 22};
    const auto [minimum, maximum] = std::ranges::minmax(readings);

    std::println("Samples: {}", readings.size());
    std::println("Minimum: {} C", minimum);
    std::println("Maximum: {} C", maximum);
}
```

**실행 결과**

```text
Samples: 5
Minimum: 19 C
Maximum: 24 C
```

`std::ranges::minmax`는 최솟값과 최댓값을 함께 반환합니다. 이 예제는 고정 크기의 데이터이므로 `std::vector`를 사용할 필요가 없습니다.

**주의:** `std::array<int, 0>`도 생성할 수 있지만, `front()`와 `back()`은 비어 있는 배열에서 사용할 수 없습니다.

---

## 6.3. 가변 크기 배열 — `std::vector`

`std::vector<T>`는 요소 개수가 실행 중 달라지는 배열입니다. 센서 수집 데이터, 검색 결과, 사용자 목록처럼 데이터의 개수를 미리 알 수 없을 때 사용합니다.

**예제 코드 — [02_std_vector.cpp](./examples/02_std_vector.cpp)**

```cpp
#include <print>
#include <vector>

int main() {
    std::vector<int> samples;
    samples.reserve(4);

    for (const int value : {12, 15, 13, 18}) {
        samples.push_back(value);
    }

    std::println("Size: {}", samples.size());
    for (const int sample : samples) {
        std::println("Reading: {}", sample);
    }
}
```

**실행 결과**

```text
Size: 4
Reading: 12
Reading: 15
Reading: 13
Reading: 18
```

### `size`, `capacity`, `reserve`, `resize`

이 네 가지는 서로 다릅니다.

| API | 의미 | 실제 요소 개수 변경 |
|---|---|:---:|
| `size()` | 현재 존재하는 요소 수 | X |
| `capacity()` | 재할당(Reallocation) 없이 담을 수 있는 요소 수 | X |
| `reserve(n)` | 최소 `n`개를 담을 수 있는 저장 공간 확보 | X |
| `resize(n)` | 요소 수를 `n`개로 조정 | O |
| `push_back(value)` | 요소 하나를 끝에 추가 | O |

```cpp
std::vector<int> values;
values.reserve(100);
// values.size() == 0. values[0]에 접근하면 안 됨.

values.resize(3);
// values.size() == 3. int 요소는 0으로 초기화됨.
```

`reserve()`는 메모리 Reallocation 횟수를 줄이기 위한 기능이지, 요소를 생성하는 기능이 아닙니다. 실제 요소를 채울 때는 `push_back()`을 사용하거나 `resize()`로 먼저 크기를 설정해야 합니다.

요소 추가 과정에서 내부 저장 공간이 이동하면 기존 요소를 가리키던 **포인터·참조·반복자(Iterator)**가 더 이상 유효하지 않을 수 있습니다. 이를 무효화(Invalidation)라고 합니다. 주소를 오래 보관해야 하는 설계라면 컨테이너의 특성을 먼저 검토해야 합니다.

---

## 6.4. 인덱스와 안전한 요소 접근

외부 입력을 배열 인덱스로 사용하거나 요소가 없을 수 있는 위치에 접근할 때는 범위를 확인해야 합니다.

| 접근 방법 | 범위 검사 | 범위 초과 시 |
|---|---|---|
| `container[index]` | 없음 | 미정의 동작(Undefined Behavior, UB) 발생 가능 |
| `container.at(index)` | 있음 | `std::out_of_range` 예외 발생 |
| `container.front()` | 없음 | 비어 있는 컨테이너에서는 사용 불가 |
| `container.back()` | 없음 | 비어 있는 컨테이너에서는 사용 불가 |

**예제 코드 — [03_safe_access.cpp](./examples/03_safe_access.cpp)**

```cpp
#include <array>
#include <print>
#include <stdexcept>

int main() {
    const std::array<int, 3> voltages{12, 24, 48};
    const std::size_t requested_index{3};

    if (requested_index >= voltages.size()) {
        std::println("Index {} is out of range", requested_index);
    }

    try {
        std::println("Voltage: {}", voltages.at(requested_index));
    } catch (const std::out_of_range&) {
        std::println("Access rejected by at()");
    }
}
```

**실행 결과**

```text
Index 3 is out of range
Access rejected by at()
```

일반적인 실무 코드에서는 범위를 미리 검증하고, API 계약상 예외가 필요한 경우 `at()`을 활용합니다. `at()`이 있다고 해서 입력값 검증 전체가 불필요해지는 것은 아닙니다.

---

## 6.5. 반복 처리, 검색, 정렬 및 집계

배열에서 반복문을 이용하면 합계·평균·최댓값 등을 계산할 수 있습니다. 다만 널리 사용되는 작업은 표준 알고리즘으로 작성하는 편이 의도를 명확히 표현할 수 있습니다.

| 작업 | 대표 API | 헤더 |
|---|---|---|
| 정렬 | `std::ranges::sort` | `<algorithm>` |
| 조건별 개수 | `std::ranges::count_if` | `<algorithm>` |
| 특정 값 검색 | `std::ranges::find` | `<algorithm>` |
| 정렬된 범위 검색 | `std::ranges::binary_search` | `<algorithm>` |
| 합계 | `std::accumulate` | `<numeric>` |

**예제 코드 — [04_algorithms.cpp](./examples/04_algorithms.cpp)**

```cpp
#include <algorithm>
#include <numeric>
#include <print>
#include <vector>

int main() {
    std::vector<int> delays_ms{42, 18, 31, 18, 55};
    const long long total = std::accumulate(delays_ms.begin(), delays_ms.end(), 0LL);
    const auto slow = std::ranges::count_if(delays_ms, [](int value) {
        return value >= 40;
    });

    std::ranges::sort(delays_ms);
    std::println("Total: {} ms", total);
    std::println("Slow samples: {}", slow);
    std::println("Has 31 ms: {}", std::ranges::binary_search(delays_ms, 31));
    std::println("Sorted first: {} ms", delays_ms.front());
}
```

**실행 결과**

```text
Total: 164 ms
Slow samples: 2
Has 31 ms: true
Sorted first: 18 ms
```

- `std::accumulate(..., 0LL)`은 누적값의 초기 타입을 `long long`으로 지정하여 정수 합산의 범위를 넓힙니다. 입력값에 따라 `long long` 범위도 확인해야 합니다.
- `std::ranges::binary_search`는 **정렬 조건을 만족하는 데이터**에서 사용해야 합니다. 정렬되지 않은 배열에서 바로 호출하면 올바른 결과를 보장할 수 없습니다.
- 알고리즘의 시간 복잡도(Time Complexity)는 자료구조와 전제 조건에 따라 달라집니다. 일반적인 비교 정렬은 `O(n log n)`, 정렬된 범위의 이진 탐색은 `O(log n)`입니다.

---

## 6.6. 연속 데이터의 View — `std::span`

함수가 배열 전체를 복사하거나 특정 컨테이너 타입에 의존할 필요가 없다면 `std::span`을 사용할 수 있습니다. `std::span<T>`는 원본 데이터를 소유하지 않고 연속 메모리(Contiguous Memory)에 저장된 요소 범위를 참조합니다.

**예제 코드 — [05_std_span.cpp](./examples/05_std_span.cpp)**

```cpp
#include <array>
#include <span>
#include <vector>

[[nodiscard]] long long total_samples(std::span<const int> samples) {
    long long total{};
    for (const int value : samples) {
        total += value;
    }
    return total;
}

int main() {
    std::array<int, 3> fixed{10, 20, 30};
    std::vector<int> dynamic{5, 15};

    // 같은 함수에 서로 다른 컨테이너 전달
    const auto fixed_total = total_samples(fixed);
    const auto dynamic_total = total_samples(dynamic);
}
```

전체 실행 코드는 링크된 예제 파일에서 확인할 수 있습니다. 원본을 수정하는 함수에는 `std::span<int>`, 읽기만 하는 함수에는 `std::span<const int>`를 사용합니다.

- **장점:** 배열 데이터를 복사하지 않고, 길이 정보와 함께 함수에 전달
- **제약:** 메모리를 소유하지 않으므로 원본 객체가 살아 있어야 함
- **주의:** `std::vector`의 크기 변경이나 Reallocation 이후에는 기존 `span`이 유효하지 않게 될 수 있음

`std::span`은 **Contiguous Memory**를 전제로 합니다. 모든 종류의 컨테이너에 적용할 수 있는 것은 아닙니다.

---

## 6.7. 다차원 배열과 격자 데이터

센서 매트릭스, 픽셀, 지도, 보드판처럼 행과 열이 있는 데이터는 다차원 배열로 표현할 수 있습니다.

**예제 코드 — [06_grid.cpp](./examples/06_grid.cpp)**

```cpp
#include <array>

constexpr std::array grid{
    std::array{0, 1, 0, 0},
    std::array{0, 1, 1, 0},
    std::array{0, 0, 0, 0},
};

// grid[row][col] 형식으로 접근
const int cell = grid.at(1).at(2);  // 1
```

**전체 예제 실행 결과**

```text
Rows: 3, Columns: 4
Blocked cells: 3
Cell (1, 2): 1
```

각 행과 열의 크기가 고정된 경우 `std::array<std::array<T, C>, R>`를 사용할 수 있습니다. 크기가 동적으로 변경되는 경우에는 `std::vector<std::vector<T>>`도 가능하지만, 행별 할당이 별도로 발생할 수 있습니다.

성능이나 하드웨어 인터페이스를 고려해야 한다면 2차원 데이터를 **1차원 연속 저장 공간**으로 표현하는 방법도 사용합니다.

```cpp
#include <vector>

const std::size_t width{4};
const std::size_t height{3};
std::vector<int> pixels(width * height, 0);

const std::size_t row{1};
const std::size_t col{2};
pixels.at(row * width + col) = 255;
```

`row * width + col`은 행 우선(Row-Major) 배치에서 좌표를 인덱스로 변환하는 공식입니다. 외부 좌표를 사용할 때는 `row < height`, `col < width`를 먼저 검증해야 하며, 실제 할당 전에는 `width * height`의 오버플로(Overflow)도 고려해야 합니다.

---

## 6.8. 문자열 저장과 조작 — `std::string`

`std::string`은 문자열 데이터와 저장 공간을 소유합니다. 문자열을 생성하고 수정하거나 다른 객체로 전달할 때 기본적으로 사용하는 타입입니다.

```cpp
#include <string>

std::string device_name{"Motor-A"};
device_name += "-Front";
```

**예제 코드 — [07_string_operations.cpp](./examples/07_string_operations.cpp)**

```cpp
#include <print>
#include <string>

int main() {
    const std::string device_id{"SENSOR-ROOM-07"};

    std::println("Prefix: {}", device_id.starts_with("SENSOR-"));
    std::println("Contains ROOM: {}", device_id.contains("ROOM"));
    std::println("Suffix: {}", device_id.ends_with("-07"));

    const auto delimiter = device_id.find('-');
    if (delimiter != std::string::npos) {
        std::println("Category: {}", device_id.substr(0, delimiter));
    }
}
```

**실행 결과**

```text
Prefix: true
Contains ROOM: true
Suffix: true
Category: SENSOR
```

| 함수 | 동작 | 비고 |
|---|---|---|
| `size()` | 문자열의 바이트 수 조회 | UTF-8 글자 수와 다를 수 있음 |
| `empty()` | 비어 있는 문자열 여부 | 길이가 0인지 검사 |
| `find(text)` | 부분 문자열의 시작 위치 검색 | 실패 시 `std::string::npos` |
| `substr(pos, count)` | 부분 문자열 복사본 생성 | `std::string` 반환 |
| `starts_with(text)` | 접두 문자열 검사 | C++20 |
| `ends_with(text)` | 접미 문자열 검사 | C++20 |
| `contains(text)` | 부분 문자열 포함 여부 검사 | **C++23** |

`contains()`는 C++23의 표준 문자열 기능입니다. 기존 `find() != std::string::npos`와 목적은 비슷하지만 포함 여부를 직접 표현한다는 장점이 있습니다.

---

## 6.9. 공백을 포함한 문자열 입력 — `std::getline`

`std::cin >> name`은 일반적으로 공백에서 입력을 구분합니다. 공백이 포함된 장치명이나 파일 경로를 입력받으려면 `std::getline()`을 사용합니다.

**예제 코드 — [08_getline.cpp](./examples/08_getline.cpp)**

```cpp
#include <iostream>
#include <print>
#include <string>

int main() {
    std::cout << "Device name: " << std::flush;
    std::string name;

    if (!std::getline(std::cin, name) || name.empty() || name.size() > 80) {
        std::println(stderr, "Invalid device name");
        return 1;
    }

    std::println("Registered: {}", name);
}
```

**실행 예시**

```text
Device name: LiDAR Front Left
Registered: LiDAR Front Left
```

### `operator>>`와 `getline()`을 함께 사용하는 경우

정수를 `std::cin >> count`로 입력한 다음 `getline()`을 호출하면, 정수 뒤의 줄바꿈이 먼저 읽힐 수 있습니다.

```cpp
int count{};
std::cin >> count;

std::string ignored;
std::getline(std::cin, ignored);  // 같은 줄에 남은 내용을 제거

std::string name;
std::getline(std::cin, name);     // 다음 줄의 이름 입력
```

이 방법은 **개수만 한 줄에 입력하는 형식**을 전제로 합니다. 한 줄에 여러 데이터를 섞어 입력받는 프로그램에서는 입력 형식을 명확히 정의하거나, 한 줄 전체를 읽어 개별 항목으로 파싱(Parsing)하는 편이 안전합니다.

또한 입력 검증을 길이만으로 끝내지 않습니다. 실제 서비스에서 허용할 문자, 공백, 중복 여부 등은 요구사항에 따라 결정해야 합니다.

---

## 6.10. 소유하지 않는 문자열 — `std::string_view`

`std::string_view`는 문자 데이터를 복사하거나 소유하지 않는(Non-Owning) **읽기 전용 View**를 표현합니다. 단순 검색, 접두어 확인, 짧은 함수 호출 인수 등에 적합합니다.

**예제 코드 — [09_string_view.cpp](./examples/09_string_view.cpp)**

```cpp
#include <string>
#include <string_view>

[[nodiscard]] std::string_view category_of(std::string_view identifier) {
    const auto delimiter = identifier.find(':');
    if (delimiter == std::string_view::npos) {
        return {};
    }
    return identifier.substr(0, delimiter);
}

int main() {
    const std::string identifier{"MOTOR:FRONT-LEFT"};
    const std::string_view category = category_of(identifier);
    // identifier의 수명 내에서만 category를 사용해야 함.
}
```

**전체 예제 실행 결과**

```text
Category: MOTOR
```

`std::string_view::substr()`는 문자열을 복사하지 않고 원본 데이터의 일부를 참조하는 새 View를 반환합니다. 반면 `std::string::substr()`는 일반적으로 새 `std::string` 객체를 반환합니다.

### Lifetime 관련 주의사항

```cpp
// 잘못된 예: 임시 std::string이 문장 끝에서 소멸함.
std::string_view invalid = std::string{"temporary"};

// 안전한 예: 원본 문자열을 별도로 보관함.
const std::string owned{"persistent"};
std::string_view valid = owned;
```

`invalid`처럼 원본 객체의 Lifetime이 끝난 뒤에도 메모리를 참조하는 상태를 댕글링 뷰(Dangling View)라고 합니다. 이 View를 통해 문자에 접근하면 UB가 발생할 수 있습니다. 또한 `std::vector`나 `std::string`을 변경한 뒤에는 이전 View가 여전히 유효한지 확인해야 합니다.

**함수 설계 기준:** 문자열 내용을 읽기만 하는 짧은 함수에서는 `std::string_view`를 고려하되, 반환값으로 View를 돌려준다면 호출자가 원본의 Lifetime을 보장해야 합니다.

---

## 6.11. 문자열을 숫자로 변환 — `std::from_chars`

센서, 설정 파일, 명령어 처리에서는 텍스트 숫자를 실제 정수로 변환해야 합니다. `std::from_chars`는 **할당 및 예외 없이 변환 결과와 입력 소비 위치를 확인할 수 있는 API**입니다.

**예제 코드 — [10_from_chars.cpp](./examples/10_from_chars.cpp)**

```cpp
#include <charconv>
#include <expected>
#include <string_view>

[[nodiscard]] std::expected<int, std::string_view>
parse_percentage(std::string_view input) {
    int value{};
    const auto [end, error] = std::from_chars(
        input.data(), input.data() + input.size(), value);

    if (error != std::errc{} || end != input.data() + input.size()) {
        return std::unexpected("not an integer");
    }
    if (value < 0 || value > 100) {
        return std::unexpected("out of range (0..100)");
    }
    return value;
}
```

**전체 예제 실행 결과**

```text
85 -> 85
85% -> error: not an integer
120 -> error: out of range (0..100)
```

변환 결과 검증에는 두 가지 조건이 필요합니다.

1. `error == std::errc{}` — 숫자 변환 성공 여부
2. `end == input.data() + input.size()` — 입력 전체를 소비했는지 확인

`"85%"`에서 `%`가 남더라도 부분 변환은 성공할 수 있으므로 두 조건을 모두 검사해야 합니다. 정수용 `from_chars`는 기본적으로 선행 공백이나 `+` 부호를 허용하지 않습니다. 필요하다면 Parsing 전에 입력 형식에 맞춰 별도로 처리해야 합니다.

`std::expected`는 Chapter 05에서 학습한 기능입니다. 여기에서는 변환 성공값과 오류 메시지를 구분하는 용도로 사용합니다.

---

## 6.12. UTF-8과 문자열 길이

`std::string`은 바이트 시퀀스(Byte Sequence)를 보관합니다. UTF-8로 인코딩된 한국어, 이모지 등의 문자는 하나의 문자가 여러 바이트로 저장될 수 있습니다.

**예제 코드 — [11_utf8_bytes.cpp](./examples/11_utf8_bytes.cpp)**

```cpp
#include <print>
#include <string>

int main() {
    const std::string text{"A\xED\x95\x9C"}; // UTF-8의 A + 한
    std::println("Bytes: {}", text.size());
    std::println("First ASCII byte: {}", text.front());
}
```

**실행 결과**

```text
Bytes: 4
First ASCII byte: A
```

| 개념 | 설명 |
|---|---|
| 바이트 수 | `std::string::size()`가 반환하는 값 |
| 코드 포인트(Code Point) 수 | UTF-8을 해석하여 얻는 Unicode Code Point의 수 |
| 사용자에게 보이는 글자 수 | 결합 문자·이모지 시퀀스 등을 고려한 문자소 클래스터(Grapheme Cluster) 수 |

이 예제는 4바이트지만 Code Point는 2개입니다. 실제 화면에 보이는 Grapheme Cluster까지 정확히 계산하려면 Unicode 텍스트 처리 라이브러리(예: ICU)나 플랫폼의 문자 처리 기능이 필요할 수 있습니다.

**주의:** UTF-8 문자열에서 `text[i]`로 접근하면 글자 하나가 아니라 **바이트 하나**를 읽습니다. 임의 위치에서 잘라내면 UTF-8 문자의 중간 바이트를 분리할 수 있습니다.

---

## 6.13. 구분자(Delimiter)로 구성된 데이터 처리

장치 로그나 간단한 설정값에는 Delimiter로 연결된 레코드가 사용될 수 있습니다. 예를 들어 아래 형식은 장치 ID, 온도, 상태를 `|`로 구분합니다.

```text
ROOM-01|23|OK
```

이런 입력은 문자열을 분할한 뒤 각 필드의 형식과 범위를 개별 검증해야 합니다.

**예제 코드 — [12_record_parser.cpp](./examples/12_record_parser.cpp)**

```cpp
const auto first = line.find('|');
const auto second = line.find('|', first + 1);

const auto id = line.substr(0, first);
const auto number = line.substr(first + 1, second - first - 1);
const auto status = line.substr(second + 1);
```

위 부분은 구조를 설명하기 위한 발췌 코드입니다. 실제 실행 파일에서는 Delimiter 존재 여부, 필드 수, 정수 형식, 온도 범위, 상태값을 검증한 뒤 분리합니다.

**실행 결과**

```text
ROOM-01: 23 C (OK)
Rejected: invalid temperature
```

Parsing 함수가 반환하는 `SensorRecord`는 장치명과 상태값을 `std::string`으로 **복사하여 소유**합니다. 원본 문자열이 사라진 후에도 결과 객체를 안전하게 저장할 수 있도록 설계한 것입니다.

이 예제는 단순 Delimiter 기반 프로토콜 전용입니다. 인용 부호와 이스케이프 규칙이 있는 실제 CSV, JSON 등을 다룰 때는 해당 형식의 규격에 맞는 파서를 사용해야 합니다.

---

## 6.14. C 스타일 배열(C-Style Array)과 메모리 관리

C++에서도 다음과 같은 C-Style Array를 사용할 수 있습니다.

```cpp
int values[3]{10, 20, 30};
```

하지만 배열을 함수에 전달할 때 크기 정보가 쉽게 소실될 수 있습니다.

```cpp
void process(const int* data, std::size_t size);
```

위와 같은 인터페이스 대신 C++ 코드에서는 연속 데이터의 범위를 나타내는 `std::span<const int>`를 고려할 수 있습니다.

```cpp
void process(std::span<const int> values);
```

C-Style Array가 항상 잘못된 것은 아닙니다. C 언어 API, 특정 하드웨어 SDK, 외부 라이브러리와의 호환성이 필요할 수 있습니다. 다만 일상적인 C++ 코드에서는 다음 원칙을 권장합니다.

- **고정 크기 데이터:** `std::array`
- **가변 크기 데이터:** `std::vector`
- **소유하지 않는 연속 데이터 인수:** `std::span`
- **외부 C API 연동:** 명시적인 포인터와 길이, Ownership 규칙 확인

메모리 주소와 포인터의 동작 원리는 Chapter 07에서 자세히 다룹니다.

---

## 6.15. 컨테이너 선택 및 성능 고려

### 어떤 타입을 사용할까?

| 상황 | 우선 고려할 타입 | 이유 |
|---|---|---|
| 고정 개수의 센서 채널 | `std::array` | 요소 수가 일정함 |
| 실행 중 증가하는 측정 데이터 | `std::vector` | 동적 크기와 연속 저장 지원 |
| 배열을 읽는 함수의 인수 | `std::span<const T>` | 불필요한 복사 방지 |
| 수정 가능한 여러 요소를 받는 함수 | `std::span<T>` | 데이터 범위를 전달하고 수정 |
| 소유하고 저장할 텍스트 | `std::string` | Lifetime을 독립적으로 관리 |
| 짧은 읽기 전용 텍스트 인수 | `std::string_view` | 문자열 복사 방지 |

### Invalidation 문제

**예제 코드 — [13_vector_invalidation.cpp](./examples/13_vector_invalidation.cpp)**

```cpp
std::vector<int> readings{10, 20};
const std::size_t selected_index{1};

readings.push_back(30);

if (selected_index < readings.size()) {
    std::println("Selected reading: {}", readings.at(selected_index));
}
```

요소 추가로 메모리에 Reallocation이 발생하면 기존 참조·포인터·Iterator가 유효하지 않게 될 수 있습니다. 위 예제는 이전 참조를 계속 사용하지 않고 인덱스를 이용해 다시 접근합니다. 다만 인덱스도 **삽입·삭제 등으로 요소 순서가 바뀌면 같은 대상을 가리킨다는 보장이 없으므로**, 안정적인 객체 식별이 필요한 경우 별도의 ID 체계를 사용해야 합니다.

### Time Complexity 요약

| 연산 | `std::array` | `std::vector` |
|---|---|---|
| 인덱스 접근 | `O(1)` | `O(1)` |
| 전체 순회 | `O(n)` | `O(n)` |
| 마지막에 요소 추가 | 지원하지 않음 | 분할 상환(Amortized) `O(1)` |
| 중간에 요소 삽입/삭제 | 크기 변경 불가 | 일반적으로 `O(n)` |

표의 Amortized는 여러 번의 연산에 걸쳐 비용을 나누어 분석한다는 의미이며, 모든 개별 호출이 `O(1)`이라는 뜻은 아닙니다. 성능은 Time Complexity뿐 아니라 데이터 크기, 캐시 지역성(Cache Locality), Reallocation, 메모리 사용량 등에도 영향을 받습니다. 우선 올바르게 동작하는 구조를 만들고, 실제 병목이 확인되면 측정하여 최적화하는 방식이 좋습니다.

---

## 6.16. Coding Practice

`exercises/`에는 직접 구현할 코드 뼈대를, `solutions/`에는 모범답안을 배치했습니다. 문제의 입력 조건과 출력 형식을 먼저 확인한 뒤 코드를 완성합니다.

### 6.16.1. Sensor Statistics — 센서 데이터 통계

**요구사항**

1. 첫 번째 정수 `N`을 입력받습니다. (`1 ≤ N ≤ 1000`)
2. 다음으로 `N`개의 센서 측정값을 입력받습니다. (각 `-1000000`~`1000000`)
3. 입력 개수 및 값의 범위를 검증합니다.
4. 측정값의 개수, 최솟값, 최댓값, 평균을 출력합니다.
5. 평균은 소수 둘째 자리까지 출력합니다.

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

- [연습문제 — 01_sensor_statistics.cpp](./exercises/01_sensor_statistics.cpp)
- [정답 코드 — 01_sensor_statistics.cpp](./solutions/01_sensor_statistics.cpp)

**확인할 사항:** 빈 배열에서 최솟값 함수를 호출하지 않도록 입력 개수를 검증하고, 평균 계산에는 정수 나눗셈을 사용하지 않습니다.

### 6.16.2. Device Lookup — 장치 목록 검색

**요구사항**

1. 장치 개수 `N`을 입력받습니다. (`1 ≤ N ≤ 20`)
2. 다음 `N`줄에 장치 이름을 입력받습니다. (공백 포함 허용, 1~60바이트)
3. 마지막 줄에 검색할 장치 이름을 입력받습니다.
4. 정확하게 일치하는 장치를 찾아 이름과 **1부터 시작하는 위치**를 출력합니다.
5. 없으면 `Not found`를 출력합니다. 이름 비교는 대소문자를 구분합니다.

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

- [연습문제 — 02_device_lookup.cpp](./exercises/02_device_lookup.cpp)
- [정답 코드 — 02_device_lookup.cpp](./solutions/02_device_lookup.cpp)

**확인할 사항:** `std::cin >> N` 이후 남아 있는 줄바꿈을 처리하고, 이름에는 `std::getline()`을 사용합니다. 중복된 이름이 있다면 처음 발견한 장치의 위치를 출력합니다.

### 6.16.3. Measurement Parser — 측정 데이터 검증

**요구사항**

1. 한 줄의 쉼표 구분 정수 목록을 입력받습니다.
2. 측정값은 1~100개이며 각 값은 `-100`~`100`이어야 합니다.
3. 값 앞뒤의 ASCII 공백은 허용합니다.
4. 빈 값, 숫자 뒤에 붙은 문자, 범위 밖의 값은 오류로 처리합니다.
5. 값의 개수, 평균(소수 둘째 자리), 최댓값을 출력합니다.

**입력**

```text
20,25,19,21
```

**출력**

```text
Samples: 4
Average: 21.25
Peak: 25
```

**오류 입력 예시:** `20,,30`, `20,30ms`, `20,300`

- [연습문제 — 03_parse_measurements.cpp](./exercises/03_parse_measurements.cpp)
- [정답 코드 — 03_parse_measurements.cpp](./solutions/03_parse_measurements.cpp)

**확인할 사항:** `std::string_view`로 필드를 나누고, `std::from_chars`의 변환 결과와 입력 소비 위치를 모두 검사합니다.

### 6.16.4. Grid Obstacles — 격자 장애물 분석

**요구사항**

1. 첫 줄에서 격자 크기 `W H`를 입력받습니다. (각 `1`~`30`)
2. 다음 `H`줄에 정확히 `W`개의 `.` 또는 `#` 문자를 입력받습니다.
3. `.`은 빈 공간, `#`은 장애물입니다.
4. 전체 장애물 수와 빈 공간 수를 출력합니다.
5. 격자의 **바깥 테두리**에 장애물이 하나도 없다면 `yes`, 있으면 `no`를 출력합니다.

**입력**

```text
4 3
....
.#..
....
```

**출력**

```text
Grid: 4x3
Blocked: 1
Free: 11
All borders clear: yes
```

- [연습문제 — 04_grid_obstacles.cpp](./exercises/04_grid_obstacles.cpp)
- [정답 코드 — 04_grid_obstacles.cpp](./solutions/04_grid_obstacles.cpp)

**확인할 사항:** 입력된 행 수, 열 수, 허용 문자를 검증합니다. 가로·세로 크기가 `1`인 경우에도 테두리 판정이 올바르게 동작해야 합니다.

### 컴파일 및 실행

**GCC** — `Chapter-06/` 폴더에서 실행

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -O2 \
  solutions/01_sensor_statistics.cpp -o sensor_statistics
./sensor_statistics
```

**Clang** — 지원되는 C++ 표준 라이브러리를 사용하는 환경

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic -O2 \
  solutions/01_sensor_statistics.cpp -o sensor_statistics
./sensor_statistics
```

**MSVC** — Developer Command Prompt

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 solutions\01_sensor_statistics.cpp /Fe:sensor_statistics.exe
sensor_statistics.exe
```

MSVC의 C++23 언어 옵션과 개별 표준 라이브러리 지원 범위는 설치된 버전에 따라 달라질 수 있습니다. `/std:c++23`이 제공되는 버전에서는 해당 옵션도 사용할 수 있습니다.

---

## 6.17. Quiz & Summary

### Quiz

1. `std::vector`의 `reserve(100)`을 호출한 직후 요소 100개에 접근할 수 있나요?
2. `std::array<int, 4>`의 마지막 요소 인덱스는 무엇인가요?
3. `std::string_view`를 `std::string` 대신 저장할 때 주의할 점은 무엇인가요?
4. `std::from_chars`가 `"25ms"`의 `25`를 읽은 경우, 추가로 어떤 검증이 필요한가요?
5. UTF-8 문자열에서 `std::string::size()`가 반환하는 값은 무엇인가요?

<details>
<summary>정답 확인</summary>

1. 아니요. `reserve()`는 용량만 확보하며 `size()`를 변경하지 않음.
2. `3`. 인덱스는 `0`부터 시작함.
3. 원본 문자열의 Lifetime과 View의 유효성을 보장해야 함.
4. 변환 종료 위치가 입력의 끝인지 검사해야 함.
5. 문자열의 바이트 수. 화면에 표시되는 글자 수와 다를 수 있음.

</details>

### Summary

- **`std::array`:** 크기가 고정된 데이터의 소유 및 관리
- **`std::vector`:** 크기가 변하는 연속 데이터의 소유 및 관리
- **`reserve()` / `resize()`:** 저장 용량 예약과 실제 요소 개수 조정의 차이
- **범위 검사:** `at()` 또는 명시적인 인덱스 검증을 통한 잘못된 접근 방지
- **표준 알고리즘:** 정렬, 검색, 집계를 표현하는 재사용 가능한 기능
- **`std::span`:** 원본 배열을 복사하지 않고 연속된 요소에 접근
- **`std::string`:** 문자열 데이터를 소유하고 변경하는 객체
- **`std::string_view`:** 원본의 Lifetime에 의존하는 읽기 전용 문자열 View
- **`std::getline()`:** 공백을 포함한 한 줄 입력 처리
- **`std::from_chars`:** 숫자 Parsing 결과와 전체 입력 소비 여부 검증
- **UTF-8:** 바이트 수, Code Point 수, Grapheme Cluster 수의 차이

### References

- [cppreference — `std::array`](https://en.cppreference.com/w/cpp/container/array)
- [cppreference — `std::vector`](https://en.cppreference.com/w/cpp/container/vector)
- [cppreference — `std::span`](https://en.cppreference.com/w/cpp/container/span)
- [cppreference — `std::string`](https://en.cppreference.com/w/cpp/string/basic_string)
- [cppreference — `std::string_view`](https://en.cppreference.com/w/cpp/string/basic_string_view)
- [cppreference — `std::from_chars`](https://en.cppreference.com/w/cpp/utility/from_chars)
- [cppreference — C++23 compiler support](https://en.cppreference.com/w/cpp/compiler_support/23)

---

[← C++ 목차](../README.md) · [Chapter 05 — Functions](../Chapter-05/)
