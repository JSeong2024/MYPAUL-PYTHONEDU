# Chapter 02. Variables & Data Types

변수의 선언과 초기화, 기본 자료형, 정수 범위, 상수, 타입 추론, 형변환 및 열거형을 다룹니다.

본 자료는 **C++23(ISO/IEC 14882:2024)** 을 기준으로 작성되었습니다.

## Contents

| Section | Topic |
|:---:|---|
| 2.1 | 변수 선언과 초기화 |
| 2.2 | 기본 자료형 |
| 2.3 | 정수의 크기와 표현 범위 |
| 2.4 | 리터럴과 단위 |
| 2.5 | `const`, `constexpr` |
| 2.6 | `auto`와 타입 추론 |
| 2.7 | 형변환과 값 손실 방지 |
| 2.8 | 부동소수점과 금액 처리 |
| 2.9 | `enum class`와 상태 표현 |
| 2.10 | Coding Practice |
| 2.11 | Summary |

---

## 2.1. 변수 선언과 초기화

변수는 값을 저장하는 이름 있는 객체입니다. C++에서는 자료형을 지정하고, 필요한 값으로 초기화하여 사용합니다.

```cpp
int retry_count{0};
int timeout_ms{5'000};
bool connected{false};
```

| 구문 | 의미 |
|---|---|
| `int count{3};` | `int` 타입의 변수를 3으로 초기화 |
| `int count{};` | 0으로 초기화 |
| `int count;` | 지역 정수 변수의 초기값이 정해지지 않음 |
| `count = 5;` | 기존 변수에 새로운 값 대입 |

`{}`를 사용하는 초기화는 값의 **축소 변환(narrowing conversion)**을 제한합니다. 예를 들어 `int count{3.5};`는 컴파일 오류가 발생합니다. 숫자를 암묵적으로 잘라서 저장하는 실수를 방지하기 위한 규칙입니다.

지역 변수는 선언할 때 초기화하는 습관이 좋습니다. 값이 나중에 결정된다면 사용 전 반드시 올바르게 대입되어야 합니다.

[예제 코드 — 01_variable_initialization.cpp](./examples/01_variable_initialization.cpp)

```cpp
#include <print>
#include <string>

int main() {
    int retry_count{};
    bool connected{false};
    std::string device_name{"Lidar-01"};

    std::println("Device: {}", device_name);
    std::println("Retries: {}", retry_count);
    std::println("Connected: {}", connected);
}
```

**실행 결과**

```text
Device: Lidar-01
Retries: 0
Connected: false
```

## 2.2. 기본 자료형

자료형은 값의 종류와 처리 방식을 결정합니다. C++의 기본 자료형은 정수, 실수, 문자, 논리값 등을 표현합니다. 문자열은 기본 자료형이 아니라 표준 라이브러리 타입인 `std::string`을 사용합니다.

| 자료형 | 용도 | 예시 |
|---|---|---|
| `bool` | 참·거짓 | `bool ready{true};` |
| `char` | 문자 코드 단위 | `char channel{'A'};` |
| `int` | 일반적인 정수 | `int count{12};` |
| `long long` | 큰 범위의 정수 | `long long ticks{10'000'000};` |
| `float` | 단정밀도 실수 | `float ratio{0.5F};` |
| `double` | 배정밀도 실수 | `double temperature{23.75};` |
| `std::string` | 문자열 | `std::string name{"Sensor-A"};` |

`int`, `long`, `long long`의 실제 크기는 실행 환경에 따라 달라질 수 있습니다. 정확한 비트 폭이 필요한 데이터에는 2.3의 고정 폭 정수 타입을 고려합니다.

`char` 하나가 항상 사람이 인식하는 문자 하나를 표현하는 것은 아닙니다. UTF-8로 인코딩한 한글 등은 여러 바이트로 구성될 수 있습니다.

[예제 코드 — 02_fundamental_types.cpp](./examples/02_fundamental_types.cpp)

```cpp
#include <print>
#include <string>

int main() {
    using std::println;

    bool ready{true};
    char channel{'A'};
    int sample_count{12};
    double temperature_c{23.75};
    std::string sensor_name{"Temperature-01"};

    println("Sensor: {}", sensor_name);
    println("Channel: {}", channel);
    println("Ready: {}", ready);
    println("Samples: {}", sample_count);
    println("Temperature: {:.2f} C", temperature_c);
}
```

**실행 결과**

```text
Sensor: Temperature-01
Channel: A
Ready: true
Samples: 12
Temperature: 23.75 C
```

## 2.3. 정수의 크기와 표현 범위

센서 값, 장치 번호, 통신 메시지처럼 저장 범위가 정해진 데이터에는 `<cstdint>`의 고정 폭 정수 타입을 사용할 수 있습니다.

| 타입 | 의미 | 대표 사용 예시 |
|---|---|---|
| `std::int8_t` | 부호 있는 8비트 정수 | 작은 범위의 부호 있는 데이터 |
| `std::uint16_t` | 부호 없는 16비트 정수 | ADC 샘플 값 |
| `std::int32_t` | 부호 있는 32비트 정수 | 장치의 측정값 |
| `std::uint32_t` | 부호 없는 32비트 정수 | 프로토콜의 식별 번호 |
| `std::int64_t` | 부호 있는 64비트 정수 | 큰 누적값, 시간값 |

`intN_t`, `uintN_t`는 해당 비트 폭을 정확히 표현할 수 있는 정수 타입이 존재할 때 제공됩니다. 실습에서 사용하는 일반적인 데스크톱 환경에서는 위 타입을 사용할 수 있습니다.

- **부호 있는 정수(signed):** 음수와 양수를 표현
- **부호 없는 정수(unsigned):** 0 이상의 정수만 표현
- **`std::numeric_limits<T>`:** 자료형의 최솟값·최댓값 등 조회
- **`sizeof(T)`:** 자료형의 저장 크기를 바이트 단위로 확인

부호 없는 정수는 음수를 표현할 수 없습니다. 뺄셈 결과가 음수가 되는 계산에 무분별하게 사용하면 예상과 다른 값이 나올 수 있습니다. 수치 계산에서는 기본적으로 `int` 등 부호 있는 정수를 사용하고, 고정된 비트 폭이나 외부 데이터 형식이 필요할 때 해당 타입을 선택합니다.

[예제 코드 — 03_fixed_width_integers.cpp](./examples/03_fixed_width_integers.cpp)

```cpp
#include <cstdint>
#include <limits>
#include <print>

int main() {
    const std::uint32_t device_id{1'024};
    const std::int64_t uptime_ms{86'400'000};

    std::println("Device ID: {}", device_id);
    std::println("Uptime: {} ms", uptime_ms);
    std::println("uint16_t maximum: {}",
                 std::numeric_limits<std::uint16_t>::max());
}
```

**실행 결과**

```text
Device ID: 1024
Uptime: 86400000 ms
uint16_t maximum: 65535
```

## 2.4. 리터럴과 단위

리터럴은 코드에 직접 작성한 값입니다. 큰 숫자는 작은따옴표(`'`)로 자릿수를 구분할 수 있으며, 숫자 값 자체에는 영향을 주지 않습니다.

| 리터럴 | 의미 |
|---|---|
| `115'200` | 십진 정수 115200 |
| `0b0000'0101` | 이진 정수 5 |
| `0xFF` | 16진 정수 255 |
| `2.5` | `double` 리터럴 |
| `2.5F` | `float` 리터럴 |
| `'A'` | 문자 리터럴 |
| `"A"` | 문자열 리터럴 |

측정값의 단위는 변수 이름에 표시하면 의미를 파악하기 쉽습니다. 예를 들어 `timeout_ms`, `distance_m`, `temperature_c`처럼 작성합니다. 단, 이름만으로 단위가 강제되는 것은 아니므로 서로 다른 단위의 값을 섞어 계산하지 않도록 주의해야 합니다.

[예제 코드 — 04_literals_and_units.cpp](./examples/04_literals_and_units.cpp)

```cpp
#include <cstdint>
#include <print>

int main() {
    constexpr std::uint32_t serial_baud{115'200};
    constexpr int retry_limit{3};
    constexpr double max_distance_m{2.5};
    constexpr std::uint8_t status_mask{0b0000'0101};

    std::println("Serial baud: {}", serial_baud);
    std::println("Retries: {}", retry_limit);
    std::println("Maximum distance: {:.1f} m", max_distance_m);
    std::println("Status mask: {}", static_cast<unsigned int>(status_mask));
}
```

**실행 결과**

```text
Serial baud: 115200
Retries: 3
Maximum distance: 2.5 m
Status mask: 5
```

## 2.5. `const`, `constexpr`

값이 바뀌지 않아야 하는 변수에는 `const`를 사용합니다. 컴파일 시점에 계산할 수 있는 상수식이 필요한 경우에는 `constexpr`를 사용합니다.

| 선언 | 의미 |
|---|---|
| `const int limit{10};` | 초기화 이후 값 변경 불가 |
| `constexpr int limit{10};` | 상수식으로 사용 가능한 값 |
| `const std::string name{"IMU-01"};` | 변경하지 않는 문자열 객체 |

`constexpr` 변수는 상수식으로 초기화되어야 합니다. 반면 `const` 변수는 실행 중 입력받거나 계산한 값으로 초기화할 수도 있습니다.

[예제 코드 — 05_constexpr_and_auto.cpp](./examples/05_constexpr_and_auto.cpp)

```cpp
#include <cstdint>
#include <print>
#include <string>

int main() {
    constexpr int samples_per_second{50};
    constexpr int milliseconds_per_second{1'000};
    constexpr auto interval_ms = milliseconds_per_second / samples_per_second;

    const std::string sensor_name{"IMU-01"};
    auto sample_count = std::uint32_t{120};

    std::println("Sensor: {}", sensor_name);
    std::println("Interval: {} ms", interval_ms);
    std::println("Samples: {}", sample_count);
}
```

**실행 결과**

```text
Sensor: IMU-01
Interval: 20 ms
Samples: 120
```

`interval_ms`는 샘플링 주기와 기준 시간을 이용해 컴파일 시점에 계산할 수 있는 값입니다. 위 예제는 1초에 50개 샘플을 처리하는 설정을 가정합니다.

## 2.6. `auto`와 타입 추론

`auto`는 초기화 식을 기반으로 변수의 자료형을 추론하도록 하는 키워드입니다. 실행 중 자료형이 바뀌는 동적 타입이 아니라, **컴파일 시점에 타입이 결정**됩니다.

```cpp
auto count = std::uint32_t{120};  // std::uint32_t
auto temperature = 23.5;          // double
auto enabled = true;              // bool
```

| 방식 | 권장 상황 |
|---|---|
| `int count{3};` | 자료형을 명시하는 것이 읽기 쉬운 경우 |
| `auto count = std::uint32_t{3};` | 초기화 식에 타입이 명확하게 드러나는 경우 |
| `auto size = text.size();` | 라이브러리 함수의 반환 타입을 그대로 사용하는 경우 |

특히 `std::string::size()`처럼 반환 타입이 `std::size_t`인 함수를 다룰 때 `auto`가 유용합니다. 반면 코드만 보고 자료형을 이해하기 어렵다면 타입을 명시하는 편이 좋습니다.

`auto value{3};`는 `int`로 추론됩니다. `auto value = {3};`은 `std::initializer_list<int>`로 추론되는 등 중괄호 사용 방식에 따라 결과가 달라질 수 있으므로 주의해야 합니다.

## 2.7. 형변환과 값 손실 방지

서로 다른 타입의 값을 변환할 때는 저장 가능한 범위와 값 손실을 확인해야 합니다.

```cpp
// int count{3.9};  // 컴파일 오류: 축소 변환
const int count{static_cast<int>(3.9)};  // 명시적 변환: 3
```

`static_cast`는 의도적인 변환을 코드에 명시합니다. 그러나 안전성을 자동으로 보장하지는 않습니다. 예를 들어 실수를 정수로 변환하면 소수 부분이 제거되며, 표현 불가능한 값을 변환하면 문제가 발생할 수 있습니다.

C++20의 `std::in_range<T>()`는 정수값이 대상 정수 타입에 손실 없이 들어가는지 검사합니다. 이는 **타입의 표현 범위**를 확인하는 것이며, 센서의 허용 범위처럼 **업무 규칙**은 별도로 검사해야 합니다.

[예제 코드 — 06_safe_numeric_conversion.cpp](./examples/06_safe_numeric_conversion.cpp)

```cpp
#include <cstdint>
#include <iostream>
#include <print>
#include <utility>

int main() {
    const std::int64_t raw_adc{3'872};
    constexpr std::int64_t max_adc{4'095};

    if (raw_adc < 0 || raw_adc > max_adc ||
        !std::in_range<std::uint16_t>(raw_adc)) {
        std::cerr << "Error: ADC value is out of range.\n";
        return 1;
    }

    const auto adc = static_cast<std::uint16_t>(raw_adc);
    std::println("ADC value: {}", adc);
}
```

**실행 결과**

```text
ADC value: 3872
```

위 예제는 ADC의 물리적 허용 범위(`0~4095`)와 `std::uint16_t`의 표현 범위를 확인한 뒤, `static_cast`로 변환합니다. 외부 입력을 변환할 때는 [Chapter 01의 입력 검증](../Chapter-01/#18-정수-입력의-엄격한-검증)처럼 문자열 전체가 정상적으로 변환되었는지도 확인해야 합니다.

## 2.8. 부동소수점과 금액 처리

`float`와 `double`은 실수를 유한한 비트 수로 근사하여 표현합니다. 따라서 `0.1 + 0.2`와 `0.3` 같은 연산 결과가 비트 단위로 일치하지 않을 수 있습니다.

[예제 코드 — 07_floating_point_precision.cpp](./examples/07_floating_point_precision.cpp)

```cpp
#include <cmath>
#include <print>

int main() {
    const double measured{0.1 + 0.2};
    constexpr double expected{0.3};
    constexpr double tolerance{1e-12};

    const bool equal_with_tolerance =
        std::abs(measured - expected) <= tolerance;

    std::println("Measured: {:.17f}", measured);
    std::println("Expected: {:.17f}", expected);
    std::println("Within tolerance: {}", equal_with_tolerance);
}
```

**실행 예시 (일반적인 IEEE 754 환경)**

```text
Measured: 0.30000000000000004
Expected: 0.29999999999999999
Within tolerance: true
```

`std::abs()`로 차이의 절댓값을 구하고, 상황에 맞는 허용 오차를 적용할 수 있습니다. 허용 오차 `1e-12`는 이 예제를 위한 값이며, 실제 계산에서는 값의 크기와 필요한 정확도에 따라 기준을 정해야 합니다.

금액처럼 오차 없이 저장해야 하는 값은 **최소 화폐 단위의 정수**를 사용하는 방법이 있습니다. 원화 금액은 원 단위 정수로 계산할 수 있으며, 소수 단위 화폐라면 센트 등 최소 단위를 기준으로 설계할 수 있습니다.

[예제 코드 — 08_money_in_integer_units.cpp](./examples/08_money_in_integer_units.cpp)

```cpp
#include <cstdint>
#include <limits>
#include <print>

int main() {
    constexpr std::int64_t unit_price_won{12'900};
    const std::int64_t quantity{3};

    if (quantity < 0 ||
        quantity > std::numeric_limits<std::int64_t>::max() / unit_price_won) {
        std::println("Error: invalid quantity.");
        return 1;
    }

    const std::int64_t total_won{unit_price_won * quantity};
    std::println("Total: {} KRW", total_won);
}
```

**실행 결과**

```text
Total: 38700 KRW
```

정수 금액도 곱셈 결과가 자료형의 범위를 초과할 수 있습니다. 위 예제는 수량을 곱하기 전에 오버플로 가능성을 검사합니다. 결제·회계 등 실제 시스템에서는 통화, 반올림 규칙, 정밀도, 금액 범위까지 함께 정의해야 합니다.

## 2.9. `enum class`와 상태 표현

장치 상태나 처리 단계처럼 선택 가능한 값이 정해져 있다면 `enum class`를 사용할 수 있습니다. 숫자를 직접 전달하는 방식보다 의미가 분명하고, 다른 열거형과의 혼용도 방지할 수 있습니다.

[예제 코드 — 09_scoped_enum.cpp](./examples/09_scoped_enum.cpp)

```cpp
#include <cstdint>
#include <print>
#include <utility>

enum class DeviceState : std::uint32_t {
    idle = 0,
    running = 1,
    fault = 2
};

int main() {
    const DeviceState state{DeviceState::running};
    std::println("Device state code: {}", std::to_underlying(state));
}
```

**실행 결과**

```text
Device state code: 1
```

- **`enum class`**: 범위가 있는 열거형 선언
- **`DeviceState::running`**: 열거형 멤버에 명시적으로 접근
- **`: std::uint32_t`**: 열거형의 기반 정수 타입 지정
- **`std::to_underlying()`**: 열거형을 기반 정수 타입으로 변환하는 C++23 함수

실제 장치 프로토콜에서 상태 번호가 정의되어 있다면, 명시적인 숫자 값과 기반 타입을 사용해 대응시킬 수 있습니다. 다만 외부 입력을 열거형으로 해석할 때는 정의되지 않은 상태 번호를 별도로 검증해야 합니다.

## 2.10. Coding Practice

`exercises/`에는 실습용 미완성 코드가, `solutions/`에는 정답 코드가 있습니다. 설명을 참고하여 직접 구현한 뒤 결과를 비교합니다.

| 번호 | 실습 | 문제 파일 | 정답 코드 |
|:---:|---|---|---|
| 01 | 장치 정보 출력 | [01_device_info.cpp](./exercises/01_device_info.cpp) | [01_device_info.cpp](./solutions/01_device_info.cpp) |
| 02 | ADC 입력 및 범위 검증 | [02_sensor_range.cpp](./exercises/02_sensor_range.cpp) | [02_sensor_range.cpp](./solutions/02_sensor_range.cpp) |
| 03 | 주문 금액 계산 | [03_order_total.cpp](./exercises/03_order_total.cpp) | [03_order_total.cpp](./solutions/03_order_total.cpp) |

### Exercise 01 — Device Information

장치 이름, 장치 번호, 활성 상태를 각각 적절한 자료형으로 선언하고 정보를 출력합니다.

**구현 조건**

- 장치 이름: `Sensor-A1`
- 장치 번호: `1024` (`std::uint32_t`)
- 활성 상태: `true` (`bool`)
- 필요한 변수는 선언 시 초기화

**실행 결과**

```text
Device: Sensor-A1 (ID: 1024)
Active: true
```

### Exercise 02 — ADC Reading

ADC 측정값을 한 줄 입력받고 `0~4095` 범위의 정수인지 검증합니다. 입력 검증 방식은 Chapter 01의 `std::from_chars()`를 활용합니다.

**구현 조건**

- 입력 전체가 정수인지 확인
- 음수, 범위 초과, 빈 입력, `12abc` 등 잘못된 입력 거부
- `std::in_range<std::uint16_t>()`로 표현 범위 확인
- 정상 입력만 `std::uint16_t`로 변환
- 오류 발생 시 `std::cerr`로 메시지 출력 후 비정상 종료

**실행 예시**

```text
ADC (0-4095): 2048
ADC: 2048
```

### Exercise 03 — Order Total

상품 단가와 주문 수량을 이용해 총액을 계산합니다. 원 단위 정수 금액을 사용하여 부동소수점 오차를 피합니다.

**구현 조건**

- 단가: `12'900`원 (`std::int64_t`)
- 수량: `1~100` 범위의 정수만 허용
- 입력 전체의 유효성 검사
- 총액 계산 후 `KRW` 단위로 출력
- 오류 발생 시 `std::cerr`로 메시지 출력 후 비정상 종료

**실행 예시**

```text
Quantity (1-100): 3
Total: 38700 KRW
```

### 실습 코드 컴파일

다음 명령어는 `Chapter-02/` 폴더에서 실행합니다.

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -g exercises/01_device_info.cpp -o device_info
./device_info
```

정답 코드의 실행 결과를 확인하려면 `exercises/`를 `solutions/`로 변경해 컴파일합니다. GCC 14 이상의 표준 라이브러리 환경을 권장하며, `<print>` 지원 여부는 설치된 컴파일러 및 표준 라이브러리의 버전에 따라 달라질 수 있습니다. Windows에서 사용 중인 GCC 환경에 따라 `-lstdc++exp` 링크 옵션이 추가로 필요할 수 있습니다.

## 2.11. Summary

- **변수 선언:** 자료형과 이름 지정, 선언 시 초기화
- **중괄호 초기화:** 암묵적인 축소 변환 방지
- **기본 자료형:** `bool`, `char`, `int`, `double` 등
- **고정 폭 정수:** `<cstdint>`의 `std::int64_t`, `std::uint32_t` 등
- **리터럴:** 숫자 구분자(`'`), 이진·16진 표현, 접미사
- **상수:** `const`는 변경 방지, `constexpr`는 상수식 요구
- **타입 추론:** `auto`로 초기화 식에서 타입 결정
- **안전한 변환:** 허용 범위 검증 후 `static_cast`, 정수 타입 검증에 `std::in_range()` 활용
- **부동소수점:** 표현 오차 고려, 금액은 최소 화폐 단위 정수 활용 가능
- **상태 표현:** `enum class`, C++23의 `std::to_underlying()`

## References

- [C++ Core Guidelines — ES.23: Prefer the `{}` initializer syntax](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-list)
- [Fundamental Types — cppreference](https://en.cppreference.com/w/cpp/language/types)
- [Fixed Width Integer Types — cppreference](https://en.cppreference.com/w/cpp/types/integer)
- [List Initialization — cppreference](https://en.cppreference.com/w/cpp/language/list_initialization)
- [`std::numeric_limits` — cppreference](https://en.cppreference.com/w/cpp/types/numeric_limits)
- [`std::in_range` — cppreference](https://en.cppreference.com/w/cpp/utility/in_range)
- [`std::to_underlying` — cppreference](https://en.cppreference.com/w/cpp/utility/to_underlying)

---

[← C++ 목차](../README.md)
