# Chapter 03. Operators & Conditions

산술·비교·논리 연산자와 조건문을 이용한 데이터 검증, 상태 판단, 처리 흐름 제어를 다룹니다.

본 자료는 **C++23(ISO/IEC 14882:2024)** 을 기준으로 작성되었습니다.

## Contents

| Section | Topic |
|:---:|---|
| 3.1 | 산술 연산과 정수 계산 |
| 3.2 | 비교·논리 연산과 단락 평가 |
| 3.3 | `if`, `else if`, `else` |
| 3.4 | 가드 절(Guard Clause)과 오류 처리 |
| 3.5 | `switch`와 `enum class` |
| 3.6 | 초기화 구문을 포함한 `if` |
| 3.7 | 조건 연산자 `?:` |
| 3.8 | 비트 연산과 상태 플래그 |
| 3.9 | 경계값과 연산자 우선순위 |
| 3.10 | Coding Practice |
| 3.11 | Summary |

---

## 3.1. 산술 연산과 정수 계산

산술 연산자는 수치 계산에 사용됩니다. 두 정수가 나눗셈에 사용되면 결과도 정수이며, 소수 부분은 버려집니다. `%`는 정수 나눗셈의 나머지를 구하는 연산자입니다.

| 연산자 | 기능 | 예시 |
|---|---|---|
| `+` | 덧셈 | `7 + 3` → `10` |
| `-` | 뺄셈 | `7 - 3` → `4` |
| `*` | 곱셈 | `7 * 3` → `21` |
| `/` | 나눗셈 | `7 / 3` → `2` (정수 계산) |
| `%` | 나머지 | `7 % 3` → `1` |
| `+=`, `-=` | 복합 대입 | `total += value;` |
| `++`, `--` | 1 증가·감소 | `++count;` |

[예제 코드 — 01_arithmetic_and_remainder.cpp](./examples/01_arithmetic_and_remainder.cpp)

```cpp
#include <print>

int main() {
    constexpr int item_count{17};
    constexpr int items_per_box{5};

    const int full_boxes{item_count / items_per_box};
    const int remainder{item_count % items_per_box};

    std::println("Full boxes: {}", full_boxes);
    std::println("Remaining items: {}", remainder);
}
```

**실행 결과**

```text
Full boxes: 3
Remaining items: 2
```

박스 하나에 5개를 담을 수 있는 상황을 가정합니다. 정수 나눗셈으로 가득 찬 박스 수를 계산하고, 나머지 연산으로 남은 품목 수를 구합니다.

**주의 사항**

- **0으로 나누기:** 정수의 0 나눗셈은 정의되지 않은 동작. 연산 전에 제수 검증 필요
- **정수 오버플로:** 부호 있는 정수의 표현 범위를 넘는 계산 주의
- **형식 선택:** 실수 결과가 필요하면 실수 타입으로 변환한 뒤 계산

```cpp
const double average = static_cast<double>(sum) / count;
```

위 계산에서는 `count`가 0보다 큰지 먼저 확인해야 합니다.

## 3.2. 비교·논리 연산과 단락 평가

비교 연산은 두 값을 비교하고 `bool` 결과를 반환합니다. 논리 연산은 여러 조건을 결합하는 데 사용합니다.

| 연산자 | 의미 |
|---|---|
| `==`, `!=` | 같음, 다름 |
| `<`, `<=` | 작음, 작거나 같음 |
| `>`, `>=` | 큼, 크거나 같음 |
| `&&` | 두 조건이 모두 참일 때 참 |
| `\|\|` | 둘 중 하나 이상 참일 때 참 |
| `!` | 논리값 반전 |

**단락 평가(short-circuit evaluation)**는 불필요한 조건을 평가하지 않는 동작입니다.

- `A && B`: `A`가 거짓이면 `B`를 평가하지 않음
- `A || B`: `A`가 참이면 `B`를 평가하지 않음

[예제 코드 — 02_logical_short_circuit.cpp](./examples/02_logical_short_circuit.cpp)

```cpp
#include <print>

int main() {
    constexpr bool connected{true};
    constexpr double temperature_c{78.5};
    constexpr int sample_count{0};
    constexpr int total_samples{120};

    const bool overheating = connected && temperature_c >= 75.0;
    const bool has_high_average =
        sample_count != 0 && total_samples / sample_count > 30;

    std::println("Overheating: {}", overheating);
    std::println("High average: {}", has_high_average);
}
```

**실행 결과**

```text
Overheating: true
High average: false
```

`sample_count != 0`이 거짓이므로 `total_samples / sample_count`는 실행되지 않습니다. 다만 단락 평가는 **올바른 조건 순서**로 작성했을 때만 안전장치가 됩니다.

비교할 때 `=`(대입)과 `==`(같음)을 혼동하지 않아야 합니다. 부동소수점의 정확한 일치 여부는 측정 오차와 표현 오차를 고려해 판단합니다.

## 3.3. `if`, `else if`, `else`

`if` 문은 조건이 참일 때만 코드 블록을 실행합니다. 여러 경우를 구분하려면 `else if`와 `else`를 함께 사용합니다.

[예제 코드 — 03_if_else_threshold.cpp](./examples/03_if_else_threshold.cpp)

```cpp
#include <print>

int main() {
    constexpr double distance_cm{28.5};

    if (distance_cm < 0.0) {
        std::println("Invalid measurement");
    } else if (distance_cm < 30.0) {
        std::println("STOP");
    } else if (distance_cm <= 100.0) {
        std::println("SLOW DOWN");
    } else {
        std::println("CLEAR");
    }
}
```

**실행 결과**

```text
STOP
```

조건은 위에서 아래 순서로 확인하며, **처음으로 참이 된 분기 하나만** 실행합니다. 따라서 범위가 겹치는 조건은 순서가 결과에 영향을 줄 수 있습니다.

위 예제는 장애물과의 거리에 따라 정지, 감속, 정상 주행 상태를 결정하는 단순화한 판단 로직입니다. 실제 로봇 제어에서는 측정 신뢰도, 제동 거리, 센서 이상 등 추가 조건이 필요합니다.

## 3.4. 가드 절(Guard Clause)과 오류 처리

가드 절은 잘못된 입력이나 처리할 수 없는 상태를 먼저 확인하고 작업을 종료하는 방식입니다. 중첩된 `if`를 줄이고 정상 처리 경로를 읽기 쉽게 만들 수 있습니다.

[예제 코드 — 04_guard_clauses.cpp](./examples/04_guard_clauses.cpp)

```cpp
#include <iostream>
#include <print>

int main() {
    constexpr int max_retries{3};
    const int requested_retries{2};

    if (requested_retries < 0) {
        std::cerr << "Error: retries cannot be negative.\n";
        return 1;
    }
    if (requested_retries > max_retries) {
        std::cerr << "Error: retry limit exceeded.\n";
        return 1;
    }

    std::println("Retry setting accepted: {}", requested_retries);
}
```

**실행 결과**

```text
Retry setting accepted: 2
```

- **입력 범위 확인:** 음수 또는 정책상 허용되지 않는 값 거부
- **오류 출력:** `std::cerr`로 원인 표시
- **종료 코드:** 정상 종료는 `0`, 오류 종료는 일반적으로 `0`이 아닌 값 반환

정상 흐름에서는 불필요한 조건문 중첩을 만들지 않는 것이 좋습니다. 실제 시스템에서는 오류 종료 대신 호출자에게 실패 정보를 반환하거나 복구 절차를 수행할 수도 있습니다.

## 3.5. `switch`와 `enum class`

`switch`는 정수 또는 열거형 값에 따라 여러 동작 중 하나를 선택합니다. 장치 상태, 메뉴 번호, 메시지 종류처럼 **선택 가능한 값이 명확한 경우**에 적합합니다.

[예제 코드 — 05_switch_device_mode.cpp](./examples/05_switch_device_mode.cpp)

```cpp
#include <print>

enum class DeviceMode {
    off,
    standby,
    active
};

int main() {
    constexpr DeviceMode mode{DeviceMode::active};

    switch (mode) {
        case DeviceMode::off:
            std::println("Power off");
            break;
        case DeviceMode::standby:
            std::println("Waiting for command");
            break;
        case DeviceMode::active:
            std::println("Device running");
            break;
        default:
            std::println("Unknown device mode");
            return 1;
    }
}
```

**실행 결과**

```text
Device running
```

`case` 끝의 `break`는 다음 `case`로 실행이 이어지는 것을 방지합니다. 의도적으로 이어서 실행할 때에는 `[[fallthrough]]`를 사용해 의도를 표시할 수 있습니다.

- **`enum class`:** 허용 상태를 이름 있는 값으로 표현
- **`case`:** 각 상태별 처리
- **`default`:** 처리하지 않은 값에 대한 대응

`switch`는 일반적인 실수 범위(`distance < 30.0`)를 검사하는 용도로는 적절하지 않습니다. 범위 비교에는 `if`가 더 자연스럽습니다.

## 3.6. 초기화 구문을 포함한 `if`

C++17부터 `if (초기화; 조건)` 형식을 사용할 수 있습니다. 초기화 구문에서 선언한 변수는 해당 `if`와 `else` 문 내부에서만 사용됩니다.

[예제 코드 — 06_if_initializer.cpp](./examples/06_if_initializer.cpp)

```cpp
#include <charconv>
#include <print>
#include <string_view>
#include <system_error>

int main() {
    constexpr std::string_view input{"250"};
    int port{};

    if (const auto result = std::from_chars(
            input.data(), input.data() + input.size(), port);
        result.ec == std::errc{} &&
        result.ptr == input.data() + input.size()) {
        std::println("Parsed port: {}", port);
    } else {
        std::println("Invalid port number");
        return 1;
    }
}
```

**실행 결과**

```text
Parsed port: 250
```

`std::from_chars()`는 문자열을 정수로 변환하면서 오류 정보와 변환이 끝난 위치를 반환합니다. **오류가 없고 문자열 전체를 사용했는지** 확인하면 `250abc` 같은 입력을 거부할 수 있습니다.

이 기능은 C++23에서 그대로 사용할 수 있으며, Chapter 01의 입력 검증과 연결됩니다.

## 3.7. 조건 연산자 `?:`

조건에 따라 두 값 중 하나를 선택할 때 `조건 ? 참일 때 값 : 거짓일 때 값` 형식을 사용할 수 있습니다.

[예제 코드 — 07_conditional_operator.cpp](./examples/07_conditional_operator.cpp)

```cpp
#include <print>

int main() {
    constexpr int response_time_ms{180};
    constexpr int slow_threshold_ms{200};

    const char* label = response_time_ms > slow_threshold_ms
                            ? "SLOW"
                            : "NORMAL";

    std::println("Response: {} ms ({})", response_time_ms, label);
}
```

**실행 결과**

```text
Response: 180 ms (NORMAL)
```

단순한 값 선택에는 유용하지만, 여러 단계의 조건을 중첩하면 가독성이 저하될 수 있습니다. 여러 작업을 실행해야 한다면 `if` 문을 사용합니다.

## 3.8. 비트 연산과 상태 플래그

장치 프로토콜이나 임베디드 시스템에서는 여러 상태를 정수의 비트로 표현하기도 합니다. 하나의 비트가 전원 상태, 센서 준비 여부, 오류 상태를 나타내는 방식입니다.

| 연산자 | 기능 | 활용 |
|---|---|---|
| `&` | 비트 AND | 특정 플래그 확인 |
| `\|` | 비트 OR | 여러 플래그 결합 |
| `^` | 비트 XOR | 서로 다른 비트 확인·토글 |
| `~` | 비트 NOT | 비트 반전 |
| `<<`, `>>` | 비트 이동 | 비트 위치 설정·이동 |

[예제 코드 — 08_bitwise_status_flags.cpp](./examples/08_bitwise_status_flags.cpp)

```cpp
#include <cstdint>
#include <print>

int main() {
    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};

    constexpr std::uint32_t status{power_on | sensor_ready};

    const bool ready = (status & (power_on | sensor_ready)) ==
                           (power_on | sensor_ready) &&
                       (status & fault) == 0U;

    std::println("Status flags: {}", status);
    std::println("Device ready: {}", ready);
}
```

**실행 결과**

```text
Status flags: 3
Device ready: true
```

비트 마스크는 이름 있는 상수로 선언하고 `std::uint32_t`처럼 폭이 분명한 부호 없는 정수형을 사용하는 편이 좋습니다. 프로토콜 데이터는 허용되지 않은 비트가 설정되어 있는지도 확인해야 합니다.

> `&`는 비트 연산, `&&`는 논리 연산입니다. 두 연산자의 의미를 구분해야 합니다.

## 3.9. 경계값과 연산자 우선순위

정책상 허용되는 범위의 **최솟값·최댓값과 바로 인접한 값**을 테스트하는 것이 중요합니다. 예를 들어 배터리 잔량 20% 이하를 경고 상태로 정의했다면 19%, 20%, 21%를 각각 확인합니다.

[예제 코드 — 09_boundary_conditions.cpp](./examples/09_boundary_conditions.cpp)

```cpp
#include <iostream>
#include <print>

int main() {
    constexpr int battery_percent{20};

    if (battery_percent < 0 || battery_percent > 100) {
        std::cerr << "Error: battery percentage is out of range.\n";
        return 1;
    }

    if (battery_percent <= 20) {
        std::println("LOW BATTERY");
    } else if (battery_percent < 80) {
        std::println("NORMAL");
    } else {
        std::println("HIGH");
    }
}
```

**실행 결과**

```text
LOW BATTERY
```

다음과 같은 표현은 괄호를 사용하여 조건의 의도를 명확하게 만드는 편이 좋습니다.

```cpp
if (connected && (temperature_c >= 75.0 || voltage_v < 10.0)) {
    // 경고 처리
}
```

- **`&&`와 `||` 혼합:** 괄호로 평가 의도 표시
- **경계값:** `29`, `30`, `100`, `101` 등 구간 경계 테스트
- **조건 범위:** 유효하지 않은 값이 정상 조건에 포함되지 않도록 선검증

## 3.10. Coding Practice

`exercises/`에는 일부 구현이 비어 있는 시작 코드가, `solutions/`에는 정답 코드가 있습니다. 직접 조건식을 구현한 뒤 정상·오류·경계값을 테스트합니다.

| 번호 | 실습 | 문제 파일 | 정답 코드 |
|:---:|---|---|---|
| 01 | 거리 센서 경보 | [01_sensor_alarm.cpp](./exercises/01_sensor_alarm.cpp) | [01_sensor_alarm.cpp](./solutions/01_sensor_alarm.cpp) |
| 02 | 주문 금액과 배송비 | [02_shipping_fee.cpp](./exercises/02_shipping_fee.cpp) | [02_shipping_fee.cpp](./solutions/02_shipping_fee.cpp) |
| 03 | 장치 상태 플래그 | [03_device_flags.cpp](./exercises/03_device_flags.cpp) | [03_device_flags.cpp](./solutions/03_device_flags.cpp) |

### Exercise 01 — Sensor Alarm

거리 센서로 측정한 정수 값을 입력받아 상태를 분류합니다.

**구현 조건**

- 허용 입력: `0~400`cm 정수
- `0~29`: `STOP`
- `30~100`: `SLOW DOWN`
- `101~400`: `CLEAR`
- 범위 초과, 빈 입력, `30abc` 같은 입력은 오류 처리

**실행 예시**

```text
Distance (0-400 cm): 29
STOP
```

### Exercise 02 — Shipping Fee

단가가 12,900원인 상품의 수량을 입력받아 총 결제 금액을 계산합니다.

**구현 조건**

- 수량: `1~20`의 정수만 허용
- 주문 금액 50,000원 이상: 무료 배송
- 주문 금액 50,000원 미만: 배송비 3,000원
- 소계, 배송비, 최종 금액 출력

**실행 예시**

```text
Quantity (1-20): 3
Subtotal: 38700 KRW
Shipping: 3000 KRW
Total: 41700 KRW
```

### Exercise 03 — Device Status Flags

`0~15` 범위의 장치 상태 비트를 입력받아 상태를 출력합니다.

**구현 조건**

- 0번 비트(`1`): 전원 ON
- 1번 비트(`2`): 센서 준비
- 2번 비트(`4`): 오류
- 오류 비트가 있으면 `FAULT` 우선
- 전원·센서 준비 비트가 모두 있고 오류가 없으면 `READY`
- 그 외에는 `NOT READY`

**실행 예시**

```text
Status flags (0-15): 3
READY
```

### 실습 코드 컴파일

`Chapter-03/` 위치에서 실행합니다.

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -g exercises/01_sensor_alarm.cpp -o sensor_alarm
./sensor_alarm
```

정답은 `exercises/`를 `solutions/`로 변경해 컴파일합니다. GCC 14 이상과 C++23을 지원하는 표준 라이브러리 환경을 권장합니다. `std::print` 지원 수준은 컴파일러·표준 라이브러리 조합에 따라 다를 수 있습니다.

## 3.11. Summary

- **산술 연산:** 사칙연산, 정수 나눗셈, 나머지, 복합 대입
- **비교 연산:** `==`, `!=`, `<`, `<=`, `>`, `>=`
- **논리 연산:** `&&`, `||`, `!` 및 단락 평가
- **조건 분기:** `if`, `else if`, `else`, `switch`
- **가드 절:** 오류 상태 선검증 및 빠른 종료
- **초기화 구문:** `if (초기화; 조건)`으로 임시 변수의 범위 제한
- **조건 연산자:** 단순한 두 값 중 하나 선택
- **비트 마스크:** 비트 단위의 장치 상태 표현
- **테스트:** 정상 입력, 잘못된 입력, 경계값 검증

## References

- [C++ `if` statement — cppreference](https://en.cppreference.com/w/cpp/language/if)
- [C++ `switch` statement — cppreference](https://en.cppreference.com/w/cpp/language/switch)
- [C++ Operators — cppreference](https://en.cppreference.com/w/cpp/language/expressions)
- [`std::from_chars()` — cppreference](https://en.cppreference.com/w/cpp/utility/from_chars)
- [C++ Core Guidelines — ES: Expressions and Statements](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-expr)

---

[← C++ 목차](../README.md) · [다음 Chapter — Loops](../Chapter-04/)
