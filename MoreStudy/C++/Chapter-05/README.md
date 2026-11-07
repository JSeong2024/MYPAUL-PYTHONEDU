# Chapter 05. Functions

함수의 선언과 정의, 매개변수 전달, 참조, 반환값, 기본 인수, 오버로딩, 람다 및 파일 분리를 다룹니다.

본 자료는 **C++23(ISO/IEC 14882:2024)**을 기준으로 작성되었습니다.

## Contents

| Section | Topic |
|:---:|---|
| 5.1 | 함수의 역할과 인터페이스 |
| 5.2 | 함수 선언, 정의 및 호출 |
| 5.3 | 값 전달과 복사 |
| 5.4 | 참조 매개변수와 문자열 뷰 |
| 5.5 | 반환값과 `std::optional` |
| 5.6 | 오류 정보를 반환하는 `std::expected` |
| 5.7 | 기본 인수 |
| 5.8 | 함수 오버로딩 |
| 5.9 | `constexpr`, `[[nodiscard]]`, `noexcept` |
| 5.10 | 람다 표현식과 캡처 |
| 5.11 | 헤더와 구현 파일 분리 |
| 5.12 | 함수 단위 테스트 |
| 5.13 | Coding Practice |
| 5.14 | Summary |

---

## 5.1. 함수의 역할과 인터페이스

함수는 반복되는 작업을 이름으로 분리하고, 필요한 입력과 결과를 명확하게 표현하는 기본 단위입니다. 호출하는 쪽은 **무엇을 수행하는지**에 집중하고, 구현부는 **어떻게 계산하는지**를 담당합니다.

- **함수 선언:** 이름, 매개변수, 반환 자료형을 외부에 알림
- **함수 정의:** 실제 수행할 코드를 작성
- **함수 호출:** 매개변수에 값을 전달하고 결과를 사용
- **부수 효과:** 출력·파일 수정·외부 상태 변경 등 함수 바깥에 영향을 주는 동작

범위가 작은 기능 단위로 작성하고, 함수명은 동작과 반환 결과를 알 수 있도록 구체적으로 지정합니다. 하나의 함수에 입력, 계산, 출력, 저장을 모두 넣기보다는 필요에 따라 역할을 분리하는 편이 테스트와 유지보수에 유리합니다.

---

## 5.2. 함수 선언, 정의 및 호출

함수를 호출하기 전에 컴파일러가 함수 선언을 알아야 합니다. 반환형, 함수명, 매개변수 목록으로 인터페이스를 표현하고 본문에서 실제 로직을 구현합니다.

`[[nodiscard]]`는 호출자가 반환값을 실수로 무시하지 않도록 경고를 유도하는 속성입니다. `noexcept`는 함수가 예외를 외부로 전파하지 않겠다는 계약으로, 보장할 수 있을 때만 지정합니다. 아래 계산은 예제의 작은 유한한 입력을 전제로 합니다.

[예제 코드 — 01_function_basics.cpp](./examples/01_function_basics.cpp)

```cpp
#include <print>

[[nodiscard]] double rectangle_area(double width, double height) noexcept {
    return width * height;
}

int main() {
    const double width{2.5};
    const double height{4.0};
    std::println("Area: {:.2f} m2", rectangle_area(width, height));
}
```

**실행 결과**

```text
Area: 10.00 m2
```

- **매개변수:** `width`, `height` — 계산에 필요한 입력값
- **반환값:** `double` — 계산된 면적
- **호출:** `rectangle_area(width, height)` — 반환 결과를 출력에 사용

---

## 5.3. 값 전달과 복사

값으로 전달한 매개변수는 호출자와 별개의 객체입니다. 함수에서 매개변수를 수정해도 원본은 바뀌지 않습니다.

작은 정수·실수는 값 전달이 단순하고 효율적입니다. 문자열처럼 복사 비용이 큰 객체는 읽기만 한다면 `const T&` 또는 `std::string_view`를 고려합니다. 함수 내부에서 **자기 소유의 복사본**을 변형해야 한다면 값 전달이 의도적으로 유용할 수 있습니다.

[예제 코드 — 02_pass_by_value.cpp](./examples/02_pass_by_value.cpp)

```cpp
#include <print>
#include <string>

[[nodiscard]] std::string make_device_code(std::string prefix, int number) {
    prefix += '-';
    prefix += std::to_string(number);
    return prefix;
}

int main() {
    const std::string prefix{"SENSOR"};
    const std::string code{make_device_code(prefix, 3)};

    std::println("Original: {}", prefix);
    std::println("Generated: {}", code);
}
```

**실행 결과**

```text
Original: SENSOR
Generated: SENSOR-3
```

이 예제는 복사한 접두 문자열만 수정합니다. 함수가 전달받은 객체를 수정해 반환하는 형태이며 원본 `prefix`는 유지됩니다.

---

## 5.4. 참조 매개변수와 문자열 뷰

`T&`는 호출자가 가진 객체에 접근할 수 있어 값을 직접 변경할 때 사용합니다. 반대로 변경이 필요하지 않은 큰 객체는 `const T&`를 사용하여 복사 없이 읽을 수 있습니다.

`std::string_view`는 문자열을 소유하지 않는 읽기 전용 뷰입니다. 문자열을 **함수 호출 중에만 확인**하는 용도에 적합하며, 원본 문자열의 수명보다 오래 보관해서는 안 됩니다.

[예제 코드 — 03_references_and_views.cpp](./examples/03_references_and_views.cpp)

```cpp
#include <algorithm>
#include <print>
#include <string_view>

void set_motor_speed(int& current_rpm, int requested_rpm) noexcept {
    current_rpm = std::clamp(requested_rpm, 0, 3'000);
}

void print_motor_status(std::string_view name, int rpm) {
    std::println("{}: {} RPM", name, rpm);
}

int main() {
    int current_rpm{1'200};
    set_motor_speed(current_rpm, 3'500);
    print_motor_status("Motor-A", current_rpm);
}
```

**실행 결과**

```text
Motor-A: 3000 RPM
```

- **`int&`:** 호출자의 모터 속도 변수를 직접 갱신
- **`std::clamp`:** 요청값을 0~3000 범위로 제한
- **`std::string_view`:** 별도 문자열 복사 없이 장치 이름을 읽음

변경이 필요 없는 경우에는 가능한 한 반환값으로 결과를 전달하고, 참조로 수정하는 동작은 API 이름에서 명확히 드러나도록 설계합니다.

---

## 5.5. 반환값과 `std::optional`

함수의 정상 결과를 반환할 수 없는 경우, 특별한 숫자(`-1` 등)로 실패를 표현하면 정상적인 데이터와 구분하기 어려울 수 있습니다. 결과가 존재할 수도, 존재하지 않을 수도 있다면 `std::optional<T>`를 사용할 수 있습니다.

`std::optional`은 **실패 이유까지 전달하지는 않습니다.** 단순한 유무 확인에 적합합니다.

[예제 코드 — 04_optional_result.cpp](./examples/04_optional_result.cpp)

```cpp
#include <optional>
#include <print>

[[nodiscard]] std::optional<double> utilization(int used, int capacity) noexcept {
    if (capacity <= 0 || used < 0 || used > capacity) {
        return std::nullopt;
    }
    return static_cast<double>(used) / capacity;
}

int main() {
    if (const auto ratio = utilization(75, 100)) {
        std::println("Utilization: {:.1f}%", *ratio * 100.0);
    }

    if (!utilization(15, 0)) {
        std::println("Invalid capacity");
    }
}
```

**실행 결과**

```text
Utilization: 75.0%
Invalid capacity
```

- **`std::nullopt`:** 반환할 유효한 결과가 없음을 표시
- **`if (const auto result = ...)`:** 유효한 결과가 있는 경우에만 사용
- **`*result`:** 값이 존재한다고 확인한 뒤 내부 값 접근

---

## 5.6. 오류 정보를 반환하는 `std::expected`

C++23의 `std::expected<T, E>`는 성공 시 `T`, 실패 시 오류 정보 `E`를 보관합니다. **실패 이유를 호출자에게 알려야 하는 함수**에 활용할 수 있습니다.

아래 예제는 문자열을 네트워크 포트 번호로 변환합니다. `std::from_chars`는 입력을 부분적으로만 해석할 수 있으므로, 문자열 전체가 소비되었는지 확인해야 합니다.

[예제 코드 — 05_expected_result.cpp](./examples/05_expected_result.cpp)

```cpp
#include <charconv>
#include <cstdint>
#include <expected>
#include <print>
#include <string>
#include <string_view>

[[nodiscard]] std::expected<std::uint16_t, std::string>
parse_port(std::string_view text) {
    unsigned int value{};
    const auto [ptr, ec] = std::from_chars(text.data(),
                                            text.data() + text.size(), value);

    if (ec != std::errc{} || ptr != text.data() + text.size() ||
        value == 0 || value > 65'535) {
        return std::unexpected("Port must be an integer from 1 to 65535");
    }
    return static_cast<std::uint16_t>(value);
}

int main() {
    for (const std::string_view input : {"8080", "70000"}) {
        const auto result = parse_port(input);
        if (result) {
            std::println("Port: {}", *result);
        } else {
            std::println("Error: {}", result.error());
        }
    }
}
```

**실행 결과**

```text
Port: 8080
Error: Port must be an integer from 1 to 65535
```

- **`std::expected<std::uint16_t, std::string>`:** 성공 값과 오류 메시지를 구분
- **`std::unexpected(...)`:** 실패 결과 생성
- **`result.error()`:** 실패 원인 확인

`std::expected`는 C++23 기능이므로 컴파일러뿐 아니라 해당 표준 라이브러리의 지원 여부도 확인해야 합니다.

---

## 5.7. 기본 인수

일반적으로 사용하는 매개변수 값을 함수 선언에서 기본 인수로 지정할 수 있습니다. 호출 시 생략한 인수에만 기본값이 적용됩니다.

기본 인수는 매개변수 목록의 오른쪽부터 부여하며, 헤더에 선언과 구현을 분리한다면 보통 **헤더의 선언 한 곳에만** 작성합니다.

[예제 코드 — 06_default_arguments.cpp](./examples/06_default_arguments.cpp)

```cpp
#include <format>
#include <print>
#include <string>
#include <string_view>

[[nodiscard]] std::string log_message(std::string_view message,
                                      std::string_view level = "INFO") {
    return std::format("[{}] {}", level, message);
}

int main() {
    std::println("{}", log_message("Service started"));
    std::println("{}", log_message("Connection timeout", "WARN"));
}
```

**실행 결과**

```text
[INFO] Service started
[WARN] Connection timeout
```

첫 번째 호출은 `level`을 생략해 `INFO`를 사용하고, 두 번째 호출은 `WARN`을 직접 전달합니다.

---

## 5.8. 함수 오버로딩

이름이 같더라도 **매개변수의 타입 또는 개수가 다르면** 서로 다른 함수를 정의할 수 있습니다. 컴파일러가 호출에 가장 적합한 오버로드를 선택합니다.

반환형만 다른 함수는 오버로딩할 수 없습니다. 여러 타입 사이에 암묵적 변환이 가능한 경우 호출이 모호해질 수 있으므로 주의가 필요합니다.

[예제 코드 — 07_function_overloading.cpp](./examples/07_function_overloading.cpp)

```cpp
#include <format>
#include <print>
#include <string>

[[nodiscard]] std::string describe_reading(int count) {
    return std::format("{} counts", count);
}

[[nodiscard]] std::string describe_reading(double temperature) {
    return std::format("{:.2f} C", temperature);
}

int main() {
    std::println("{}", describe_reading(120));
    std::println("{}", describe_reading(23.5));
}
```

**실행 결과**

```text
120 counts
23.50 C
```

`describe_reading(120)`은 정수 버전, `describe_reading(23.5)`는 실수 버전을 호출합니다. 서로 다른 단위의 값을 동일한 타입으로 모호하게 섞지 않도록 함수 이름과 인수의 의미를 함께 설계해야 합니다.

---

## 5.9. `constexpr`, `[[nodiscard]]`, `noexcept`

함수의 의도와 계약을 표현하는 표준 기능을 활용할 수 있습니다.

| 요소 | 의미 | 사용 기준 |
|---|---|---|
| `constexpr` | 조건을 만족하면 컴파일 시점 계산 가능 | 부작용 없는 작은 계산 등 |
| `[[nodiscard]]` | 반환값 무시 시 진단 권고 | 상태·검증·계산 결과 |
| `noexcept` | 예외를 외부로 전파하지 않는 계약 | 예외가 발생하지 않도록 설계된 함수 |
| `static_assert` | 컴파일 시점의 조건 검증 | 상수 계산과 타입 조건 |

`constexpr` 함수도 일반 실행 시점에 호출할 수 있습니다. `noexcept` 함수에서 처리되지 않은 예외가 발생하면 프로그램은 종료되므로, 단순히 최적화를 기대하고 붙이지 않습니다.

[예제 코드 — 08_constexpr_and_attributes.cpp](./examples/08_constexpr_and_attributes.cpp)

```cpp
#include <print>

[[nodiscard]] constexpr int clamp_percentage(int value) noexcept {
    if (value < 0) {
        return 0;
    }
    if (value > 100) {
        return 100;
    }
    return value;
}

static_assert(clamp_percentage(-5) == 0);
static_assert(clamp_percentage(120) == 100);

int main() {
    const int measured_quality{127};
    std::println("Quality: {}%", clamp_percentage(measured_quality));
}
```

**실행 결과**

```text
Quality: 100%
```

`static_assert`는 두 경계 조건을 컴파일 시점에 확인하며, 실제 입력 `127`은 `100`으로 제한됩니다.

---

## 5.10. 람다 표현식과 캡처

람다는 이름이 없는 함수 객체를 간단하게 만드는 문법입니다. 정렬, 필터링, 조건 검사 등의 알고리즘에서 자주 사용합니다.

`[threshold]`는 지역 변수의 값을 캡처하고, `[&threshold]`는 참조로 캡처합니다. **원본보다 오래 실행될 수 있는 람다**에서는 참조 캡처의 수명 문제에 주의해야 합니다.

[예제 코드 — 09_lambda_and_capture.cpp](./examples/09_lambda_and_capture.cpp)

```cpp
#include <algorithm>
#include <array>
#include <print>

int main() {
    constexpr std::array readings{42, 68, 73, 49, 81, 55};
    const int threshold{60};

    const auto is_high = [threshold](int value) {
        return value > threshold;
    };

    const auto count = std::ranges::count_if(readings, is_high);
    std::println("Above threshold: {}", count);
}
```

**실행 결과**

```text
Above threshold: 3
```

`std::ranges::count_if`는 조건을 만족하는 요소 수를 반환합니다. 배열 순회와 표준 알고리즘은 이후 Chapter에서 더 자세히 다룹니다.

---

## 5.11. 헤더와 구현 파일 분리

규모가 커진 프로그램에서는 함수의 **선언(인터페이스)**과 **정의(구현)**를 별도 파일로 나누는 것이 일반적입니다. 헤더는 다른 소스 파일이 사용하는 선언을 제공하고, 구현 파일은 실제 코드를 보관합니다.

아래 예제는 `main.cpp`, `inventory.hpp`, `inventory.cpp` 세 파일로 구성됩니다. `namespace inventory`는 다른 코드와 함수 이름이 겹치는 것을 방지합니다.

**파일 구성**

```text
examples/10_multi_file/
├── inventory.hpp
├── inventory.cpp
└── main.cpp
```

**헤더** — [inventory.hpp](./examples/10_multi_file/inventory.hpp)

```cpp
#ifndef MORESTUDY_CHAPTER_05_INVENTORY_HPP
#define MORESTUDY_CHAPTER_05_INVENTORY_HPP

#include <optional>

namespace inventory {

[[nodiscard]] std::optional<int>
remaining_stock(int received, int shipped) noexcept;

}  // namespace inventory

#endif
```

**구현** — [inventory.cpp](./examples/10_multi_file/inventory.cpp)

```cpp
#include "inventory.hpp"

namespace inventory {

std::optional<int> remaining_stock(int received, int shipped) noexcept {
    if (received < 0 || shipped < 0 || shipped > received) {
        return std::nullopt;
    }
    return received - shipped;
}

}  // namespace inventory
```

**호출 코드** — [main.cpp](./examples/10_multi_file/main.cpp)

```cpp
#include "inventory.hpp"
#include <print>

int main() {
    const auto stock = inventory::remaining_stock(25, 13);
    if (!stock) {
        std::println("Invalid inventory data");
        return 1;
    }
    std::println("Available: {}", *stock);
}
```

**컴파일**

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic examples/10_multi_file/main.cpp examples/10_multi_file/inventory.cpp -o inventory_demo
./inventory_demo
```

**실행 결과**

```text
Available: 12
```

헤더 가드(`ifndef`/`define`)는 동일한 선언이 중복 포함되는 문제를 방지합니다. `#include "inventory.hpp"`는 호출 파일에 함수 선언을 제공하며, 실제 함수 정의는 링크 단계에서 연결됩니다.

---

## 5.12. 함수 단위 테스트

입력과 결과가 명확한 함수는 자동 검증하기 쉽습니다. 결과값, 경계값, 잘못된 입력을 별도 사례로 테스트하는 것이 좋습니다.

아래 예제는 세 가지 입력에 대한 기대 결과를 확인하고, 실패하면 오류 종료 코드를 반환합니다. 실제 규모가 큰 프로젝트에서는 GoogleTest, Catch2 등의 테스트 프레임워크를 사용할 수 있습니다.

[예제 코드 — 11_function_tests.cpp](./examples/11_function_tests.cpp)

```cpp
#include <algorithm>
#include <print>

[[nodiscard]] constexpr int clamp_score(int score) noexcept {
    return std::clamp(score, 0, 100);
}

int main() {
    const bool tests_passed =
        clamp_score(-10) == 0 &&
        clamp_score(70) == 70 &&
        clamp_score(150) == 100;

    if (!tests_passed) {
        std::println("Test failed");
        return 1;
    }
    std::println("All tests passed (3 cases)");
}
```

**실행 결과**

```text
All tests passed (3 cases)
```

`assert`는 빌드 설정에 따라 비활성화될 수 있으므로, 지속적으로 실행해야 하는 검증은 테스트 프레임워크나 명시적 검사 코드로 관리하는 편이 적절합니다.

---

## 5.13. Coding Practice

`exercises/`에는 함수의 핵심 구현이 비어 있는 시작 코드가 있으며, `solutions/`에는 검증 가능한 완성 코드가 있습니다. 먼저 시작 코드를 수정하고, 정답과 비교합니다.

| 번호 | 실습 | 문제 파일 | 정답 코드 |
|:---:|---|---|---|
| 01 | 온도 변환 함수 | [01_temperature_converter.cpp](./exercises/01_temperature_converter.cpp) | [01_temperature_converter.cpp](./solutions/01_temperature_converter.cpp) |
| 02 | 배송비 정책 함수 | [02_shipping_policy.cpp](./exercises/02_shipping_policy.cpp) | [02_shipping_policy.cpp](./solutions/02_shipping_policy.cpp) |
| 03 | 센서 평균 및 검증 | [03_sensor_average.cpp](./exercises/03_sensor_average.cpp) | [03_sensor_average.cpp](./solutions/03_sensor_average.cpp) |

### Exercise 01 — Temperature Converter

섭씨를 화씨로 변환하는 `to_fahrenheit()` 함수를 완성합니다. 입력과 출력 로직은 이미 제공되어 있습니다.

**구현 조건**

- `double` 타입 매개변수 1개, 반환값 1개
- 변환식: `화씨 = 섭씨 × 9 / 5 + 32`
- `NaN`, 무한대 및 입력 실패 시 오류 메시지 출력
- 함수 내부에는 입출력 코드를 작성하지 않음

**실행 예시**

```text
Celsius: 25
Fahrenheit: 77.0
```

### Exercise 02 — Shipping Policy

주문 금액과 도서·산간 여부를 받아 배송비를 계산하는 `shipping_fee()` 함수를 완성합니다. 금액은 소수 오차를 피하기 위해 정수 원(`won`) 단위로 처리합니다.

**구현 조건**

- 주문 금액이 음수이면 `std::nullopt` 반환
- 기본 배송비: 3,000원
- 주문 금액이 50,000원 이상이면 기본 배송비 면제
- 도서·산간 지역은 주문 금액과 관계없이 2,000원 추가
- 도서·산간 여부 입력: `0` 또는 `1`

**실행 예시**

```text
Order (won) and remote area (0/1): 60000 1
Shipping: 2000 won
```

### Exercise 03 — Sensor Average

고정된 센서 측정값 배열의 유효성을 검증하고 평균을 계산하는 `average_reading()` 함수를 완성합니다.

**구현 조건**

- 측정값 5개를 `const std::array<double, 5>&`로 전달
- 모든 측정값이 유한한 실수이며 0~100 범위인지 검증
- 하나라도 범위를 벗어나면 `std::nullopt` 반환
- 정상 데이터인 경우 산술평균 반환

**실행 결과**

```text
Average: 13.0
```

### 실습 코드 컴파일

`Chapter-05/` 위치에서 실행합니다.

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -g exercises/01_temperature_converter.cpp -o temperature_converter
./temperature_converter
```

정답 확인 시에는 `exercises/` 대신 `solutions/` 파일을 지정하면 됩니다. `std::expected`와 `<print>` 등 C++23 라이브러리 기능을 사용하는 예제는 해당 기능을 지원하는 최신 표준 라이브러리가 필요합니다.

## 5.14. Summary

- **함수 인터페이스:** 입력(매개변수)과 출력(반환값)을 구분
- **값 전달:** 독립된 매개변수 객체 생성, 원본 값 유지
- **참조 전달:** `T&`로 원본 수정, `const T&`로 읽기 전용 접근
- **`std::string_view`:** 문자열 복사 없는 읽기 전용 접근, 원본 수명에 주의
- **`std::optional`:** 결과의 유무를 반환
- **`std::expected`:** C++23 성공 결과와 오류 원인을 구분
- **기본 인수:** 생략된 매개변수에 기본값 사용
- **오버로딩:** 매개변수 타입·개수에 따라 함수 구분
- **`constexpr` / `[[nodiscard]]` / `noexcept`:** 함수의 의도와 계약 표현
- **람다:** 지역 조건을 담는 함수 객체 및 값 캡처
- **헤더·소스 분리:** 인터페이스와 구현 분리, 별도 컴파일 후 링크
- **함수 테스트:** 정상값·경계값·오류값 검증

## References

- [Functions — cppreference](https://en.cppreference.com/w/cpp/language/functions)
- [Reference declaration — cppreference](https://en.cppreference.com/w/cpp/language/reference)
- [`std::optional` — cppreference](https://en.cppreference.com/w/cpp/utility/optional)
- [`std::expected` — cppreference](https://en.cppreference.com/w/cpp/utility/expected)
- [Lambda expressions — cppreference](https://en.cppreference.com/w/cpp/language/lambda)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

---

[← C++ 목차](../README.md) · [이전 Chapter — Loops](../Chapter-04/)
