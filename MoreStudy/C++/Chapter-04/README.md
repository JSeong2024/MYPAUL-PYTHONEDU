# Chapter 04. Loops

`for`, `while`, `do-while` 반복문과 범위 기반 반복, 반복 중단, 입력 재시도, 누적 계산 및 2차원 데이터 순회를 다룹니다.

본 자료는 **C++23(ISO/IEC 14882:2024)**을 기준으로 작성되었습니다.

## Contents

| Section | Topic |
|:---:|---|
| 4.1 | 반복문의 종류와 선택 기준 |
| 4.2 | `for` — 횟수가 정해진 반복 |
| 4.3 | 범위 기반 `for` |
| 4.4 | `while` — 조건 기반 반복 |
| 4.5 | `do-while` — 최소 한 번 실행 |
| 4.6 | `break`, `continue` |
| 4.7 | 반복 입력과 재시도 제한 |
| 4.8 | 누적 계산과 오버플로 방지 |
| 4.9 | 중첩 반복문과 격자 데이터 |
| 4.10 | `std::views::iota` |
| 4.11 | Coding Practice |
| 4.12 | Summary |

---

## 4.1. 반복문의 종류와 선택 기준

반복문은 같은 작업을 여러 번 수행할 때 사용합니다. 반복 횟수가 이미 정해져 있는지, 종료 조건을 실행 중에 판단해야 하는지에 따라 적절한 형식을 선택합니다.

| 구문 | 주로 사용하는 상황 | 종료 기준 |
|---|---|---|
| `for` | 정해진 횟수의 샘플 수집, 인덱스 순회 | 반복 조건 |
| 범위 기반 `for` | 배열·컨테이너의 요소 처리 | 범위의 끝 |
| `while` | 센서 상태 확인, 연결 대기 | 매 반복 전 조건 검사 |
| `do-while` | 메뉴 표시, 최소 1회 실행해야 하는 작업 | 반복 후 조건 검사 |

**설계 시 고려할 항목**

- **종료 조건:** 어떤 상태에서 반복이 멈추는지 명확하게 정의
- **실행 한도:** 입력 재시도·장치 폴링에는 최대 횟수나 시간 제한 설정
- **데이터 범위:** 인덱스가 배열의 유효 범위를 벗어나지 않도록 검증
- **오류 처리:** 입력이 종료되거나 장치가 응답하지 않을 때의 동작 정의

실제 장치 폴링에는 시간 제한, 대기 간격, 작업 취소, 장치 오류 처리가 추가로 필요할 수 있습니다. 아래 예제의 센서·연결 상태는 학습용 시뮬레이션 데이터입니다.

## 4.2. `for` — 횟수가 정해진 반복

`for (초기화; 조건; 갱신)`은 정해진 횟수만큼 반복하기에 적합합니다. 초기화는 반복 시작 시 한 번, 조건은 매 반복 직전에 평가됩니다.

[예제 코드 — 01_for_sampling.cpp](./examples/01_for_sampling.cpp)

```cpp
#include <print>

int main() {
    constexpr int sample_count{5};
    int total{};

    for (int i{0}; i < sample_count; ++i) {
        const int sample{10 + 2 * i};
        total += sample;
        std::println("Sample {}: {}", i + 1, sample);
    }

    std::println("Total: {}", total);
}
```

**실행 결과**

```text
Sample 1: 10
Sample 2: 12
Sample 3: 14
Sample 4: 16
Sample 5: 18
Total: 70
```

위 예제에서는 5개의 샘플을 생성하고 합계를 누적합니다.

- **`int i{0}`:** 반복 인덱스를 0으로 초기화
- **`i < sample_count`:** 5회 실행 후 종료
- **`++i`:** 매 반복 후 인덱스 증가
- **`total += sample`:** 누적 합계 계산

종료 조건을 `i <= sample_count`로 작성하면 6번 실행되므로 경계값에 주의해야 합니다.

## 4.3. 범위 기반 `for`

배열이나 표준 컨테이너의 모든 요소를 순서대로 처리할 때 범위 기반 `for`가 유용합니다. 직접 인덱스를 관리할 필요가 없어 범위 오류를 줄일 수 있습니다.

[예제 코드 — 02_range_for_readings.cpp](./examples/02_range_for_readings.cpp)

```cpp
#include <array>
#include <print>

int main() {
    constexpr std::array readings{120, 135, 119, 142};
    int total{};

    for (const int reading : readings) {
        total += reading;
    }

    std::println("Samples: {}", readings.size());
    std::println("Total: {}", total);
}
```

**실행 결과**

```text
Samples: 4
Total: 516
```

```cpp
for (const auto& reading : readings) {
    // reading 사용
}
```

- **작은 기본 타입:** `int`처럼 복사 비용이 작은 값은 값으로 순회해도 무방
- **큰 객체:** 복사를 피하려면 `const auto&` 사용
- **요소 수정:** 필요하다면 `auto&` 사용, 읽기 전용이라면 `const` 유지

`std::array`는 크기가 고정된 표준 라이브러리 컨테이너입니다. 배열과 컨테이너의 자세한 내용은 Chapter 06에서 다룹니다.

## 4.4. `while` — 조건 기반 반복

`while`은 반복 시작 전에 조건을 검사합니다. 조건이 처음부터 거짓이면 본문이 한 번도 실행되지 않을 수 있습니다.

[예제 코드 — 03_while_polling.cpp](./examples/03_while_polling.cpp)

```cpp
#include <array>
#include <cstddef>
#include <print>

int main() {
    constexpr std::array responses{false, false, true, true};
    std::size_t attempt{};

    while (attempt < responses.size() && !responses[attempt]) {
        ++attempt;
    }

    if (attempt < responses.size()) {
        std::println("Connected on attempt {}", attempt + 1);
    } else {
        std::println("Connection failed");
        return 1;
    }
}
```

**실행 결과**

```text
Connected on attempt 3
```

이 예제는 장치 연결 응답을 미리 정의한 배열에서 순서대로 읽는 시뮬레이션입니다. **실제 네트워크 연결이나 장치 통신을 수행하는 코드는 아닙니다.**

`attempt < responses.size()`를 먼저 확인하여 배열 경계를 넘지 않도록 처리했습니다. `&&` 단락 평가를 이용해 첫 번째 조건이 거짓이면 다음 요소에 접근하지 않습니다.

실제 연결 재시도에는 각 시도 사이의 대기 시간, 전체 타임아웃, 종료 요청 처리가 추가될 수 있습니다.

## 4.5. `do-while` — 최소 한 번 실행

`do-while`은 코드를 먼저 실행한 뒤 조건을 확인합니다. 메뉴를 최소 한 번 표시해야 하는 상황에서 사용할 수 있습니다.

[예제 코드 — 04_do_while_menu.cpp](./examples/04_do_while_menu.cpp)

```cpp
#include <iostream>
#include <limits>
#include <print>

int main() {
    int selection{};

    do {
        std::println("1. Show device status");
        std::println("0. Exit");
        std::cout << "Select: " << std::flush;

        if (!(std::cin >> selection)) {
            if (std::cin.eof()) {
                return 0;
            }
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::println("Invalid input");
            continue;
        }

        if (selection == 1) {
            std::println("Device: READY");
        } else if (selection != 0) {
            std::println("Unknown menu item");
        }
    } while (selection != 0);
}
```

**실행 결과**

```text
1. Show device status
0. Exit
Select: Device: READY
1. Show device status
0. Exit
Select:
```

이 예제는 `1`을 입력하면 장치 상태를 출력하고, `0`을 입력하면 종료합니다.

- **유효하지 않은 메뉴 번호:** 안내 후 메뉴 다시 표시
- **정수가 아닌 입력:** 스트림 오류 상태 초기화 및 남은 입력 제거
- **입력 종료(EOF):** 더 이상 입력받을 수 없으므로 프로그램 종료

입력 오류 후 `std::cin.clear()`만 호출하고 잘못된 문자를 제거하지 않으면 같은 입력을 반복해서 읽으려는 문제가 생길 수 있습니다. 따라서 `ignore()`로 해당 줄의 나머지를 버립니다.

## 4.6. `break`, `continue`

반복 중 종료하거나 현재 반복을 건너뛰는 경우에 사용합니다.

| 키워드 | 동작 |
|---|---|
| `break` | 가장 가까운 반복문 또는 `switch` 종료 |
| `continue` | 현재 반복의 나머지를 건너뛰고 다음 반복으로 진행 |

[예제 코드 — 05_break_and_continue.cpp](./examples/05_break_and_continue.cpp)

```cpp
#include <array>
#include <print>

int main() {
    constexpr std::array readings{-1, 10, 25, 150, 30};

    for (const int reading : readings) {
        if (reading < 0) {
            continue;
        }
        if (reading > 100) {
            std::println("Threshold exceeded: {}", reading);
            break;
        }
        std::println("Accepted: {}", reading);
    }
}
```

**실행 결과**

```text
Accepted: 10
Accepted: 25
Threshold exceeded: 150
```

음수 측정값은 무시하고(`continue`), 임계값 100을 초과하는 값이 나오면 처리를 중단합니다(`break`). 중첩 반복문에서 `break`는 모든 반복문이 아니라 **가장 안쪽 반복문만 종료**한다는 점에 주의해야 합니다.

## 4.7. 반복 입력과 재시도 제한

사용자가 입력을 잘못했을 때 무한정 다시 입력받으면 프로그램이 종료되지 않을 수 있습니다. 실무형 콘솔 프로그램에서는 최대 재시도 횟수와 입력 종료 상황을 함께 처리하는 편이 안전합니다.

[예제 코드 — 06_retry_valid_input.cpp](./examples/06_retry_valid_input.cpp)

```cpp
#include <charconv>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    constexpr int max_attempts{3};

    for (int attempt{1}; attempt <= max_attempts; ++attempt) {
        std::cout << "Port (1-65535): " << std::flush;
        std::string line;
        if (!std::getline(std::cin, line)) {
            std::cerr << "Error: input stream closed.\n";
            return 1;
        }

        int port{};
        const auto result = std::from_chars(
            line.data(), line.data() + line.size(), port);
        const bool valid = result.ec == std::errc{} &&
                           result.ptr == line.data() + line.size() &&
                           port >= 1 && port <= 65'535;

        if (valid) {
            std::println("Selected port: {}", port);
            return 0;
        }

        std::println("Invalid port ({}/{})", attempt, max_attempts);
    }

    std::cerr << "Error: retry limit exceeded.\n";
    return 1;
}
```

**실행 결과**

```text
Port (1-65535): Invalid port (1/3)
Port (1-65535): Selected port: 8080
```

`std::getline()`으로 한 줄을 읽고, `std::from_chars()`로 문자열 전체가 정수인지 확인합니다.

- **빈 입력 또는 잘못된 문자열:** 재입력 요청
- **허용 범위 외의 값:** 재입력 요청
- **입력 스트림 종료:** 즉시 오류 반환
- **3회 모두 실패:** 재시도 한도 초과 처리

입력으로 `12abc`, `0`, `65536`을 전달하면 정상적인 포트 번호로 인정하지 않습니다. 이 예제는 포트 번호의 **형식과 범위만 검증**하며 실제 포트를 열거나 연결하지는 않습니다.

## 4.8. 누적 계산과 오버플로 방지

반복문에서 합계를 계산할 때는 누적 결과가 자료형 범위를 넘지 않는지 확인해야 합니다. 특히 장시간 실행되는 시스템의 통계 카운터는 처음에는 작은 값이라도 시간이 지나면서 커질 수 있습니다.

[예제 코드 — 07_safe_accumulation.cpp](./examples/07_safe_accumulation.cpp)

```cpp
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <print>

int main() {
    constexpr std::array<std::int64_t, 4> packets{
        1'000'000, 2'000'000, 3'000'000, 4'000'000
    };
    std::int64_t total{};

    for (const std::int64_t packet_count : packets) {
        if (packet_count < 0 ||
            total > std::numeric_limits<std::int64_t>::max() - packet_count) {
            std::cerr << "Error: invalid packet count or overflow.\n";
            return 1;
        }
        total += packet_count;
    }

    std::println("Packets: {}", total);
}
```

**실행 결과**

```text
Packets: 10000000
```

위 예제는 **음수가 아닌 패킷 개수**만 허용합니다. 각 값을 더하기 전에 `max() - packet_count`와 비교해 오버플로 가능성을 확인합니다.

- **정수 크기:** 합계 범위에 맞는 자료형 선택
- **값의 부호:** 양수·음수를 모두 허용한다면 각 경우에 맞는 검사 필요
- **실패 처리:** 잘못된 값이 발생하면 중단하거나 호출자에게 오류 전달

필요에 따라 더 넓은 자료형, 포화 연산, 별도의 checked arithmetic 함수 등을 설계할 수 있습니다.

## 4.9. 중첩 반복문과 격자 데이터

2차원 지도나 센서 격자처럼 행과 열이 있는 데이터를 처리할 때 반복문을 중첩할 수 있습니다.

[예제 코드 — 08_nested_grid.cpp](./examples/08_nested_grid.cpp)

```cpp
#include <array>
#include <cstddef>
#include <print>

int main() {
    constexpr std::array grid{
        std::array{0, 1, 0, 0},
        std::array{1, 0, 0, 1},
        std::array{0, 0, 1, 0}
    };

    for (std::size_t row{0}; row < grid.size(); ++row) {
        for (std::size_t column{0}; column < grid[row].size(); ++column) {
            if (grid[row][column] == 1) {
                std::println("Obstacle: ({}, {})", row, column);
            }
        }
    }
}
```

**실행 결과**

```text
Obstacle: (0, 1)
Obstacle: (1, 0)
Obstacle: (1, 3)
Obstacle: (2, 2)
```

`1`은 장애물, `0`은 빈 공간으로 가정합니다. 바깥 반복문은 행을, 안쪽 반복문은 열을 순회합니다.

**성능 참고:** 행이 `R`개이고 각 행의 열이 `C`개라면 모든 셀을 확인하는 작업량은 일반적으로 `O(R × C)`입니다. 공간과 처리 시간 요구사항이 큰 지도에서는 필요한 영역만 탐색하거나 별도 자료구조를 고려할 수 있습니다.

## 4.10. `std::views::iota`

C++20부터 제공되는 `<ranges>`의 `std::views::iota()`는 정수 등의 연속된 값을 범위로 나타낼 수 있습니다. C++23 기준 코드에서도 그대로 사용할 수 있습니다.

[예제 코드 — 09_ranges_iota.cpp](./examples/09_ranges_iota.cpp)

```cpp
#include <print>
#include <ranges>

int main() {
    for (const int sample_number : std::views::iota(1, 6)) {
        std::println("Processing sample {}", sample_number);
    }
}
```

**실행 결과**

```text
Processing sample 1
Processing sample 2
Processing sample 3
Processing sample 4
Processing sample 5
```

`std::views::iota(1, 6)`은 `1, 2, 3, 4, 5`를 순회하며 **끝값 6은 포함하지 않습니다.** 복잡한 범위 연산과 뷰 조합은 표준 라이브러리 과정에서 추가로 다룹니다.

## 4.11. Coding Practice

`exercises/`에는 일부 구현이 비어 있는 시작 코드가, `solutions/`에는 정답 코드가 있습니다. 반복 종료 조건과 경계값을 확인하면서 구현합니다.

| 번호 | 실습 | 문제 파일 | 정답 코드 |
|:---:|---|---|---|
| 01 | 센서 샘플 평균 | [01_sensor_average.cpp](./exercises/01_sensor_average.cpp) | [01_sensor_average.cpp](./solutions/01_sensor_average.cpp) |
| 02 | 연결 재시도 | [02_connection_retry.cpp](./exercises/02_connection_retry.cpp) | [02_connection_retry.cpp](./solutions/02_connection_retry.cpp) |
| 03 | 격자 장애물 수 | [03_grid_obstacles.cpp](./exercises/03_grid_obstacles.cpp) | [03_grid_obstacles.cpp](./solutions/03_grid_obstacles.cpp) |

### Exercise 01 — Sensor Average

ADC 샘플 다섯 개를 입력받고 평균을 계산합니다. 입력 파싱 부분은 제공하며, 누적 합계와 평균 출력 부분을 직접 구현합니다.

**구현 조건**

- 샘플 수: 5개
- 각 측정값: `0~4095` 정수
- 입력 전체에 대한 유효성 검증 유지
- 합계는 `std::int64_t`에 누적
- 평균은 `double`로 계산하여 소수 첫째 자리까지 출력

**실행 예시**

```text
ADC sample 1 (0-4095): 100
ADC sample 2 (0-4095): 200
ADC sample 3 (0-4095): 300
ADC sample 4 (0-4095): 400
ADC sample 5 (0-4095): 500
Average: 300.0
```

### Exercise 02 — Connection Retry

미리 정의된 장치 응답 배열로 연결 재시도를 시뮬레이션합니다.

**구현 조건**

- 최대 시도 횟수: 4회
- 응답 배열: `{false, false, true, false, true}`
- 첫 번째 `true`를 만나면 반복 종료
- 성공: `Connected on attempt N`
- 최대 시도까지 성공하지 못한 경우: `Connection failed` 및 오류 종료

**실행 결과**

```text
Connected on attempt 3
```

### Exercise 03 — Grid Obstacles

3행 4열의 격자 데이터에서 장애물(`1`)의 개수를 계산합니다.

**구현 조건**

- 중첩 반복문으로 모든 셀 확인
- 값이 `1`인 셀만 개수에 포함
- `Obstacles: N` 형식으로 출력

**실행 결과**

```text
Obstacles: 4
```

### 실습 코드 컴파일

`Chapter-04/` 위치에서 실행합니다.

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -g exercises/01_sensor_average.cpp -o sensor_average
./sensor_average
```

정답 코드는 `exercises/` 대신 `solutions/`를 지정해 컴파일합니다. GCC 14 이상과 C++23을 지원하는 표준 라이브러리 환경을 권장합니다. `<print>`를 제공하지 않는 오래된 표준 라이브러리에서는 해당 코드가 컴파일되지 않을 수 있습니다.

## 4.12. Summary

- **`for`:** 실행 횟수가 정해진 반복, 인덱스 관리
- **범위 기반 `for`:** 배열·컨테이너의 요소 순회
- **`while`:** 매 반복 전 조건 검사, 상태 기반 반복
- **`do-while`:** 최소 한 번 본문 실행
- **`break`:** 가장 안쪽 반복문 종료
- **`continue`:** 다음 반복으로 진행
- **입력 재시도:** 엄격한 값 검증 및 횟수 제한
- **누적 계산:** 자료형 범위와 오버플로 가능성 확인
- **중첩 반복:** 행·열 등의 다차원 데이터 순회
- **Ranges:** `std::views::iota()`를 활용한 순차 범위

## References

- [C++ `for` statement — cppreference](https://en.cppreference.com/w/cpp/language/for)
- [Range-based `for` — cppreference](https://en.cppreference.com/w/cpp/language/range-for)
- [C++ `while` statement — cppreference](https://en.cppreference.com/w/cpp/language/while)
- [C++ `do-while` statement — cppreference](https://en.cppreference.com/w/cpp/language/do)
- [`std::views::iota` — cppreference](https://en.cppreference.com/w/cpp/ranges/iota_view)
- [C++ Core Guidelines — ES: Expressions and Statements](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-expr)

---

[← C++ 목차](../README.md) · [이전 Chapter — Operators & Conditions](../Chapter-03/)
