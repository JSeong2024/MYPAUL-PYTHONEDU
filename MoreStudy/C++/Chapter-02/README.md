# Chapter 02. Variables & Data Types

변수의 선언과 초기화, 기본 자료형, 정수 범위, 상수, 타입 추론, 형변환, 부동소수점과 열거형을 학습합니다. 값을 어떤 형태로 저장할지 판단하고, 자료형에 따라 달라지는 표현 범위와 변환 결과를 이해합니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서 도입된 주요 기능을 함께 사용하며, 관련성이 있는 C++23 기능은 별도로 소개합니다.

<details>
<summary>선행 학습</summary>

- [Chapter 01. Getting Started with C++](../Chapter-01/) — 컴파일·실행, `main()`, 표준 입출력, 문자열 입력

</details>

## Contents

| Section | Topic |
|:---:|---|
| [2.1](#section-2-1) | Variables & Initialization — 변수와 초기화 |
| [2.2](#section-2-2) | Fundamental Types — 기본 자료형 |
| [2.3](#section-2-3) | Integer Types & Ranges — 정수와 표현 범위 |
| [2.4](#section-2-4) | Literals & Units — 리터럴과 단위 |
| [2.5](#section-2-5) | `const`, `constexpr` & `auto` — 상수와 타입 추론 |
| [2.6](#section-2-6) | Numeric Conversion — 명시적 형변환 |
| [2.7](#section-2-7) | Floating-Point Precision — 실수의 표현 |
| [2.8](#section-2-8) | `enum class` — 상태값 표현 |
| [2.9](#section-2-9) | Coding Practice |
| [2.10](#section-2-10) | Mini Project — Measurement Card |
| [2.11](#section-2-11) | Quiz & Summary |

## Getting Started

아래 명령어는 **`Chapter-02/` 디렉터리**에서 실행하는 경우를 기준으로 합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_variables_and_initialization.cpp -o variables
./variables
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_variables_and_initialization.cpp -o variables
./variables
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /utf-8 examples\01_variables_and_initialization.cpp /Fe:variables.exe
variables.exe
```

Windows PowerShell에서는 `./variables` 대신 `.\variables.exe`로 실행합니다. 컴파일러와 개발 환경의 기본 설정은 [Chapter 01](../Chapter-01/)에서 확인할 수 있습니다.

**학습 목표**

1. 변수를 선언하고 초기화·재할당하는 방법을 설명할 수 있습니다.
2. 값의 성질에 맞는 자료형과 리터럴을 선택할 수 있습니다.
3. `const`, `constexpr`, `auto`의 역할을 구별할 수 있습니다.
4. 정수·실수의 표현 범위와 형변환에서 발생할 수 있는 값 손실을 설명할 수 있습니다.
5. 여러 자료형을 활용해 측정값을 출력하는 프로그램을 작성할 수 있습니다.

---

<a id="section-2-1"></a>
## 2.1. Variables & Initialization — 변수와 초기화

**변수(variable)** 는 값을 저장하는 이름 있는 객체입니다. C++에서는 변수의 **자료형(type)** 을 지정하고 필요한 값으로 **초기화(initialization)** 합니다. 이후 값이 변경 가능한 변수라면 새로운 값을 **대입(assignment)** 할 수 있습니다.

```cpp
int sample_count{12};   // 변수 선언과 초기화
sample_count = 15;      // 새로운 값 대입
```

| 표현 | 의미 |
|---|---|
| `int count{5};` | 정수 변수 `count`를 5로 초기화 |
| `int count{};` | 정수 변수를 0으로 초기화 |
| `int count = 5;` | 정수 변수를 5로 초기화하는 또 다른 방식 |
| `count = 8;` | 이미 선언된 변수의 값을 8로 변경 |
| `int count;` | 지역 정수 변수의 초기값이 정해지지 않음 |

지역 변수는 선언과 동시에 초기화하는 것이 안전합니다. 초기화되지 않은 지역 정수 변수를 읽으면 프로그램의 올바른 동작을 보장할 수 없습니다.

**중괄호 초기화(`{}`)** 는 일부 암묵적인 값 손실을 막습니다. 예를 들어 `int count{3.5};`는 실수 값을 정수로 좁히는 변환이므로 컴파일 오류가 발생합니다.

**예제 코드 — [01_variables_and_initialization.cpp](./examples/01_variables_and_initialization.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    int sample_count{12};
    bool connected{true};
    std::string sensor_name{"Sensor-A"};

    std::cout << std::boolalpha;
    std::cout << "Sensor: " << sensor_name << '\n';
    std::cout << "Samples: " << sample_count << '\n';
    std::cout << "Connected: " << connected << '\n';

    sample_count = 15;
    std::cout << "Updated samples: " << sample_count << '\n';
}
```

**실행 결과**

```text
Sensor: Sensor-A
Samples: 12
Connected: true
Updated samples: 15
```

- `std::boolalpha`: `bool` 값을 `1`과 `0` 대신 `true`와 `false`로 출력합니다.
- `std::noboolalpha`: `bool` 값을 다시 `1`과 `0`으로 출력하도록 설정합니다. 별도 설정이 없을 때도 이 방식이 기본값입니다.
- `sample_count = 15;`: 이미 선언한 변수에 새로운 정수 값을 대입합니다.
- `std::string`은 Chapter 01에서 사용한 문자열 저장 타입입니다.

`std::boolalpha`와 `std::noboolalpha`는 출력 스트림의 표시 방식을 바꾸며, 다시 변경하기 전까지 적용됩니다.

```cpp
bool connected{true};
std::cout << connected << '\n';                   // 1 (기본값)
std::cout << std::boolalpha << connected << '\n'; // true
std::cout << std::noboolalpha << connected << '\n'; // 1
```

`false`도 같은 방식으로 `false` 또는 `0`으로 출력됩니다.

---

<a id="section-2-2"></a>
## 2.2. Fundamental Types — 기본 자료형

**자료형(type)** 은 값의 종류와 표현 방식, 사용할 수 있는 연산 등을 결정합니다. `int`, `double`, `bool`, `char`는 언어에서 제공하는 기본 자료형이고, `std::string`은 표준 라이브러리의 문자열 타입입니다.

| 자료형 | 주요 용도 | 선언 예시 |
|---|---|---|
| `bool` | 참·거짓 | `bool ready{true};` |
| `char` | 문자 코드 단위 | `char channel{'A'};` |
| `int` | 일반적인 정수 | `int count{12};` |
| `long long` | 더 넓은 정수 범위 | `long long total{1'000'000};` |
| `float` | 단정밀도 부동소수점 | `float ratio{0.5F};` |
| `double` | 배정밀도 부동소수점 | `double temperature_c{23.75};` |
| `std::string` | 여러 문자로 구성된 문자열 | `std::string name{"Sensor-A"};` |

**정수**는 소수 부분이 없는 수를 저장하고, **부동소수점 실수**는 제한된 정밀도로 소수 값을 근사하여 표현합니다. `double`은 일반적으로 `float`보다 많은 정밀도를 제공합니다.

**리터럴(Literal)** 은 소스 코드에 직접 적은 값입니다. 예를 들어 `'A'`는 문자 리터럴(character literal)이고, `"A"`는 문자열 리터럴(string literal)입니다. 종류와 표기법은 2.4에서 자세히 다룹니다.

`char` 하나가 항상 사람이 인식하는 글자 하나와 일치하지는 않으며, UTF-8로 인코딩된 한글은 여러 바이트로 표현될 수 있습니다.

**예제 코드 — [02_fundamental_types.cpp](./examples/02_fundamental_types.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    char channel{'B'};
    int count{24};
    long long total{1'000'000};
    float ratio{0.5F};
    double temperature_c{23.75};
    std::string label{"Thermal sensor"};

    std::cout << "Channel: " << channel << '\n';
    std::cout << "Count: " << count << '\n';
    std::cout << "Total: " << total << '\n';
    std::cout << "Ratio: " << ratio << '\n';
    std::cout << "Temperature: " << temperature_c << " C\n";
    std::cout << "Label: " << label << '\n';
}
```

**실행 결과**

```text
Channel: B
Count: 24
Total: 1000000
Ratio: 0.5
Temperature: 23.75 C
Label: Thermal sensor
```

예제의 `std::string`은 기본 자료형이 아닌 별도의 문자열 타입입니다. 자료형을 선택할 때는 값의 의미와 저장 범위를 함께 고려해야 합니다.

---

<a id="section-2-3"></a>
## 2.3. Integer Types & Ranges — 정수와 표현 범위

정수 자료형은 표현할 수 있는 값의 범위가 정해져 있습니다. `int`와 `long long`의 정확한 크기는 구현에 따라 다를 수 있습니다. 외부 데이터 형식 등에서 **정해진 비트 폭**이 필요하다면 `<cstdint>`의 고정 폭 정수 타입을 사용할 수 있습니다.

### Bit & Byte — 비트와 바이트

- **비트(Bit):** 컴퓨터가 데이터를 표현할 때 사용하는 이진 정보의 한 자리입니다. 한 비트는 `0` 또는 `1`의 두 상태를 나타냅니다.
- **바이트(Byte):** 메모리의 저장 크기를 나타내는 기본 단위입니다. 현대적인 일반 PC에서는 1바이트가 8비트이므로, 8비트로 `2⁸ = 256`개의 서로 다른 상태를 표현할 수 있습니다.
- **저장 공간:** 일반적인 8비트 바이트 환경에서 16비트 값은 2바이트, 32비트 값은 4바이트를 사용합니다. 다만 C++에서 1바이트는 최소 8비트이며, 모든 환경에서 반드시 8비트인 것은 아닙니다.

예를 들어 이진수 `0000 0101`은 8개의 비트로 나타낸 숫자 5입니다. 8비트 **부호 없는 정수**라면 가능한 값은 0부터 255까지이고, 16비트 부호 없는 정수라면 0부터 65,535까지입니다. 실제 객체의 크기는 `sizeof` 연산자로 바이트 단위로 확인할 수 있습니다.

### 고정 폭 정수와 헤더

| 헤더 | 제공 기능 |
|---|---|
| `<cstdint>` | `std::int32_t`, `std::uint16_t` 등 정해진 비트 폭의 정수 타입 |
| `<limits>` | `std::numeric_limits<T>`를 통해 자료형의 표현 범위 확인 |

| 타입 | 비트 폭 | 의미 |
|---|---:|---|
| `std::int8_t` | 8 | 부호 있는 정수 |
| `std::uint16_t` | 16 | 부호 없는 정수 |
| `std::int32_t` | 32 | 부호 있는 정수 |
| `std::uint32_t` | 32 | 부호 없는 정수 |
| `std::int64_t` | 64 | 부호 있는 정수 |

고정 폭 타입은 해당 폭의 정수 타입을 구현이 제공하는 경우에 사용할 수 있습니다. 예제는 일반적인 데스크톱 컴파일 환경을 가정합니다.

- **signed(부호 있는 정수):** 음수, 0, 양수를 표현합니다.
- **unsigned(부호 없는 정수):** 0과 양수를 표현합니다. 음수가 되는 계산에 사용하면 예상과 다른 결과가 나올 수 있습니다.
- **`std::numeric_limits<T>::min()` / `max()`:** 해당 타입의 최솟값과 최댓값을 확인합니다.
- **`sizeof(T)`:** 타입이 차지하는 저장 크기를 바이트 단위로 확인합니다. 실제 바이트의 비트 수는 구현에 따라 달라질 수 있습니다.

정확한 비트 폭이 필요하지 않은 일반적인 계산에는 `int`처럼 읽기 쉬운 기본 정수 자료형을 선택하면 됩니다.

**예제 코드 — [03_integer_ranges.cpp](./examples/03_integer_ranges.cpp)**

```cpp
#include <cstdint>
#include <iostream>
#include <limits>

int main() {
    const std::int32_t position{-250};
    const std::uint16_t port{8'080};

    std::cout << "Position: " << position << '\n';
    std::cout << "Port: " << port << '\n';
    std::cout << "uint16_t maximum: "
              << std::numeric_limits<std::uint16_t>::max() << '\n';
    std::cout << "int32_t minimum: "
              << std::numeric_limits<std::int32_t>::min() << '\n';
}
```

**실행 결과**

```text
Position: -250
Port: 8080
uint16_t maximum: 65535
int32_t minimum: -2147483648
```

`std::uint16_t`는 0부터 65,535까지 표현합니다. `std::int32_t`는 −2,147,483,648부터 2,147,483,647까지 표현합니다. **표현 범위를 넘어서는 값**을 저장하려고 하면 변환 결과가 달라지거나 잘못된 계산으로 이어질 수 있습니다.

---

<a id="section-2-4"></a>
## 2.4. Literals & Units — 리터럴과 단위

리터럴은 **변수 이름이나 계산 결과가 아니라 소스 코드에 직접 작성한 값**을 말합니다. 예를 들어 `int count{12};`에서 `count`는 변수 이름이고 `12`는 정수 리터럴입니다. `count = 20;`에서는 새로 대입하는 값 `20`이 리터럴입니다.

리터럴은 작성 방법에 따라 자료형이 정해집니다. `12`는 기본적으로 `int`, `2.5`는 `double`, `2.5F`는 `float` 리터럴입니다. `true`와 `false` 역시 `bool` 리터럴입니다. **`const` 변수는 값을 변경할 수 없다는 의미이지, 변수 자체가 리터럴이라는 뜻은 아닙니다.**

정수 리터럴은 십진수 외에도 이진수와 16진수로 표현할 수 있고, 큰 숫자의 자릿수는 작은따옴표(`'`)로 구분할 수 있습니다. 자릿수 구분자는 값을 변경하지 않습니다.

| 리터럴 | 의미 |
|---|---|
| `1'000` | 십진수 1000 (숫자 구분자 사용) |
| `0b0101` | 이진수 5 |
| `0xFF` | 16진수 255 |
| `2.5` | 기본적으로 `double`인 실수 리터럴 |
| `2.5F` | `float` 실수 리터럴 |
| `'B'` | 문자 리터럴 |
| `"B"` | 문자열 리터럴 |
| `true`, `false` | 논리값 리터럴 |

`0b0101`과 `0x05`는 표현만 다를 뿐 같은 정수 값 5를 나타냅니다.

측정값을 저장할 때는 `distance_m`, `timeout_ms`, `sampling_rate_hz`처럼 변수 이름에 **단위**를 포함하면 해석하기 쉽습니다. 단위가 이름에 있다고 해서 C++이 자동으로 단위를 검사하지는 않습니다.

**예제 코드 — [04_literals_and_units.cpp](./examples/04_literals_and_units.cpp)**

```cpp
#include <iostream>

int main() {
    int sampling_rate_hz{1'000};
    int status_mask{0b0000'0101};
    int color_value{0xFF};
    double distance_m{2.5};

    std::cout << "Sampling rate: " << sampling_rate_hz << " Hz\n";
    std::cout << "Status mask: " << status_mask << '\n';
    std::cout << "Color value: " << color_value << '\n';
    std::cout << "Distance: " << distance_m << " m\n";
}
```

**실행 결과**

```text
Sampling rate: 1000 Hz
Status mask: 5
Color value: 255
Distance: 2.5 m
```

---

<a id="section-2-5"></a>
## 2.5. `const`, `constexpr` & `auto` — 상수와 타입 추론

값이 초기화 이후 바뀌면 안 된다면 `const`를 사용합니다. `constexpr` 변수는 **컴파일 시점에 평가 가능한 상수식**으로 초기화되어야 하므로, 프로그램의 고정된 설정값을 나타낼 때 유용합니다.

| 표현 | 의미 |
|---|---|
| `const int limit{10};` | 초기화 이후 변경할 수 없는 정수 |
| `constexpr int limit{10};` | 컴파일 시점의 상수식으로 사용할 수 있는 정수 |
| `const std::string name{"Sensor-A"};` | 초기화 이후 변경하지 않는 문자열 |

`const`는 실행 중에 결정되는 값도 보관할 수 있지만, `constexpr` 변수의 초기화에는 상수식이 필요합니다. 모든 `const` 변수가 `constexpr` 변수인 것은 아닙니다.

**`auto`** 는 초기화 식으로부터 자료형을 추론합니다. 자료형은 실행 중에 계속 바뀌는 것이 아니라 **컴파일 시점에 결정**됩니다.

```cpp
auto count = 12;            // int
auto temperature = 23.5;    // double
auto connected = true;      // bool
```

단순한 숫자 리터럴로도 타입을 추론할 수 있지만, 값의 범위나 단위가 중요하면 자료형을 명시하는 편이 더 읽기 쉬울 수 있습니다.

**예제 코드 — [05_const_constexpr_auto.cpp](./examples/05_const_constexpr_auto.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    constexpr int capacity{100};
    const std::string device_name{"Counter-01"};
    auto recorded_count = 12;

    std::cout << "Device: " << device_name << '\n';
    std::cout << "Capacity: " << capacity << '\n';
    std::cout << "Recorded: " << recorded_count << '\n';

    recorded_count = 15;
    std::cout << "Updated: " << recorded_count << '\n';
}
```

**실행 결과**

```text
Device: Counter-01
Capacity: 100
Recorded: 12
Updated: 15
```

`auto`는 문법을 간결하게 만드는 도구이지, 모든 변수를 `auto`로 선언해야 한다는 의미는 아닙니다. `auto value{3};`은 `int`로 추론되지만 `auto value = {3};`은 초기화 리스트 타입으로 추론될 수 있으므로 두 표기를 같은 의미로 보지 않아야 합니다.

---

<a id="section-2-6"></a>
## 2.6. Numeric Conversion — 명시적 형변환

서로 다른 자료형으로 값을 변환하면 원래 값의 일부 정보가 사라질 수 있습니다. 이러한 **값 손실(loss of information)** 가능성을 알고 변환 방식을 선택해야 합니다.

```cpp
// int count{3.9};                // 컴파일 오류: 축소 변환
const int count{static_cast<int>(3.9)};  // 3
```

`static_cast<자료형>(값)`은 변환 의도를 명시합니다. 실수를 정수로 바꿀 때는 **소수 부분을 0 방향으로 버립니다.** 예를 들어 `3.9`는 `3`, `-3.9`는 `-3`이 됩니다. 다만 정수로 표현할 수 없는 실수 값을 변환하는 것은 안전하지 않으므로 **`static_cast` 자체가 변환을 검증해 주지는 않습니다.**

C++20의 `std::in_range<T>(value)`는 **정수값이 대상 정수 타입에 손실 없이 들어가는지** 확인합니다. 검사 결과는 `bool`입니다. 실수를 정수로 변환하기 전에 실수의 범위를 확인하는 용도로 사용하지는 않습니다.

**새로운 헤더 — `<utility>`:** `std::in_range()`와 같은 유틸리티 함수를 제공합니다. 이 예제에서는 값이 특정 정수 타입의 범위에 들어가는지 확인하기 위해 포함합니다. `<cstdint>`는 2.3에서 설명한 고정 폭 정수 타입을 사용하기 위한 헤더입니다.

**예제 코드 — [06_explicit_conversions.cpp](./examples/06_explicit_conversions.cpp)**

```cpp
#include <cstdint>
#include <iostream>
#include <utility>

int main() {
    const double measurement{8.9};
    const int whole_part{static_cast<int>(measurement)};
    const int sample_id{300};
    const bool fits_in_byte{std::in_range<std::uint8_t>(sample_id)};

    std::cout << std::boolalpha;
    std::cout << "Measurement: " << measurement << '\n';
    std::cout << "Whole part: " << whole_part << '\n';
    std::cout << "Fits in uint8_t: " << fits_in_byte << '\n';
}
```

**실행 결과**

```text
Measurement: 8.9
Whole part: 8
Fits in uint8_t: false
```

`std::uint8_t`는 0부터 255까지 표현할 수 있습니다. 따라서 `sample_id`가 300이면 `std::in_range<std::uint8_t>(sample_id)`는 `false`를 반환합니다. 값을 검증한 뒤 변환할지 결정하는 조건 처리 방식은 별도로 학습할 수 있습니다.

---

<a id="section-2-7"></a>
## 2.7. Floating-Point Precision — 실수의 표현

`float`와 `double`은 모든 십진 소수를 정확하게 저장할 수 없습니다. 컴퓨터 내부에서는 제한된 비트 수의 이진 부동소수점으로 근삿값을 표현하기 때문입니다.

예를 들어 `0.1`과 `0.2`는 일반적인 이진 부동소수점 환경에서 정확하게 표현되지 않습니다. 두 값을 더한 결과와 `0.3`을 서로 비교하면 기대와 다른 차이가 나타날 수 있습니다.

아래 예제의 `+`는 두 수를 더하는 산술 연산자입니다. 이 절에서는 덧셈 문법보다 **실수 표현과 출력 정밀도**에 집중합니다.

**새로운 헤더 — `<iomanip>`:** 숫자의 출력 형식을 조절하는 기능을 제공합니다. 이 예제에서는 `std::setprecision()`으로 표시 자릿수를 지정합니다. `std::fixed`는 표준 입출력 헤더인 `<iostream>`을 통해 사용할 수 있습니다.

**예제 코드 — [07_floating_point.cpp](./examples/07_floating_point.cpp)**

```cpp
#include <iomanip>
#include <iostream>

int main() {
    const double sum{0.1 + 0.2};
    const double expected{0.3};

    std::cout << std::fixed << std::setprecision(17);
    std::cout << "Sum: " << sum << '\n';
    std::cout << "Expected: " << expected << '\n';

    std::cout << std::setprecision(2);
    std::cout << "Displayed: " << sum << '\n';
}
```

**실행 결과**

```text
Sum: 0.30000000000000004
Expected: 0.29999999999999999
Displayed: 0.30
```

**일반적인 IEEE 754 배정밀도 환경**에서는 위와 같이 출력됩니다. 실제 표현은 컴파일러와 실행 환경의 부동소수점 구현에 영향을 받을 수 있습니다.

- `std::fixed`: 부동소수점 수를 고정 소수점 표기로 출력합니다.
- `std::setprecision(17)`: `std::fixed`와 함께 사용할 때 소수점 아래 17자리를 표시합니다.
- `std::setprecision(2)`: 소수점 아래 2자리까지 출력하도록 설정합니다.

표시 자릿수를 줄이는 것은 **출력 형태를 바꾸는 것**이지, 변수 내부의 값을 정확한 십진수로 바꾸는 것은 아닙니다. 금액처럼 소수 오차를 허용하기 어려운 값은 최소 화폐 단위(원, 센트 등)의 정수로 저장하는 방법을 고려할 수 있습니다.

---

<a id="section-2-8"></a>
## 2.8. `enum class` — 상태값 표현

**열거형(enumeration)** 은 선택 가능한 값들의 집합을 이름으로 정의하는 자료형입니다. `enum class`는 정수 코드 대신 `DeviceState::running`처럼 **의미가 드러나는 이름**을 사용하도록 돕습니다.

**예제 코드 — [08_scoped_enum.cpp](./examples/08_scoped_enum.cpp)**

```cpp
#include <iostream>

enum class DeviceState {
    idle = 0,
    running = 1,
    stopped = 2
};

int main() {
    const DeviceState state{DeviceState::running};

    std::cout << "State code: " << static_cast<int>(state) << '\n';
}
```

**실행 결과**

```text
State code: 1
```

| 문법 | 의미 |
|---|---|
| `enum class DeviceState` | `DeviceState`라는 범위가 있는 열거형 선언 |
| `running = 1` | `running` 항목의 정수 코드가 1임을 지정 |
| `DeviceState::running` | 열거형 항목을 명시적으로 선택 |
| `static_cast<int>(state)` | 명시적으로 정수 코드로 변환 |

`enum class`의 값은 일반 정수로 자동 변환되지 않으므로 필요한 경우 명시적 변환을 사용합니다. 상태를 정수 코드로 출력하는 목적과 상태 자체를 비교·판단하는 목적은 구분해야 합니다.

**C++23 참고 — `std::to_underlying()`**

C++23에서는 `<utility>` 헤더의 `std::to_underlying()`으로 열거형의 기반 정수값을 얻을 수 있습니다. C++20 기본 예제에서는 같은 용도로 `static_cast`를 사용합니다. C++17에서도 이러한 `enum class`와 `static_cast` 문법을 사용할 수 있습니다.

---

<a id="section-2-9"></a>
## 2.9. Coding Practice

`exercises/`에는 미완성 코드가, `solutions/`에는 모범답안이 제공됩니다.

| No. | 문제 | 미완성 코드 | 모범답안 |
|:---:|---|---|---|
| 01 | Device Profile — 자료형과 초기화 | [문제](./exercises/01_device_profile.cpp) | [정답](./solutions/01_device_profile.cpp) |
| 02 | Constants & Literals — 리터럴과 상수 | [문제](./exercises/02_constants_and_literals.cpp) | [정답](./solutions/02_constants_and_literals.cpp) |
| 03 | Explicit Conversion — 형변환 | [문제](./exercises/03_explicit_conversion.cpp) | [정답](./solutions/03_explicit_conversion.cpp) |
| 04 | Temperature Adjustment — 실수와 출력 자릿수 | [문제](./exercises/04_temperature_adjustment.cpp) | [정답](./solutions/04_temperature_adjustment.cpp) |

### Exercise 01 — Device Profile

장치 이름, 장치 번호, 준비 상태를 각각 적절한 자료형으로 저장하여 출력합니다.

**구현 조건**

- 이름: `Sensor-A1` (`std::string`)
- ID: `1024` (`std::uint32_t`)
- 준비 상태: `true` (`bool`)
- 변수는 선언과 동시에 초기화하며 `std::boolalpha`를 사용합니다.

**실행 결과**

```text
Device: Sensor-A1
ID: 1024
Ready: true
```

### Exercise 02 — Constants & Literals

변경하지 않는 설정값을 `constexpr` 변수로 선언하여 출력합니다.

**구현 조건**

- 대기 시간: `1'500`밀리초
- 재시도 횟수: 3회
- 상태 비트: 이진수 `0b0101`
- 숫자의 출력은 십진수로 합니다.

**실행 결과**

```text
Timeout: 1500 ms
Retry limit: 3
Status mask: 5
```

### Exercise 03 — Explicit Conversion

실수 하나를 입력받아 원래 값과 정수로 변환한 값을 출력합니다.

**구현 조건**

- `double` 타입으로 입력받습니다.
- `static_cast<int>`를 사용하여 정수로 변환합니다.
- 입력되는 실수는 `int`로 표현 가능한 범위의 유한한 값이라고 가정합니다.

**입력·출력 예시**

```text
Reading: 8.9
Original: 8.9
Whole part: 8
```

음수 입력 시에도 정수 변환은 **0 방향으로 소수 부분을 버리는 동작**을 유지해야 합니다.

### Exercise 04 — Temperature Adjustment

측정 기온과 보정값을 입력받고, 두 값을 합한 결과를 소수 둘째 자리까지 출력합니다.

**구현 조건**

- 측정 기온과 보정값은 모두 `double` 타입입니다.
- 두 값을 더한 결과를 `const double` 변수에 저장합니다.
- `std::fixed`와 `std::setprecision(2)`를 사용합니다.

**입력·출력 예시**

```text
Temperature (C): 23.75
Offset (C): -0.25
Original: 23.75 C
Adjusted: 23.50 C
```

**실습 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/04_temperature_adjustment.cpp -o temperature
./temperature
```

**선택: 자동 검증**

```bash
python tests/check.py
python tests/check.py --mode student --only exercise-04
```

**첫 번째 명령어**는 예제와 모범답안을 확인하는 용도입니다. **두 번째 명령어**는 직접 수정한 Exercise 04를 검사합니다. 아직 코드가 작성되지 않은 초기 상태에는 FAIL이 나오는 것이 정상입니다. 테스트 실행기(Test Runner)는 소스 코드를 C++20으로 컴파일한 뒤 다양한 입력값을 전달하여 출력 결과와 종료 상태가 예상과 일치하는지 자동으로 검증합니다.

---

<a id="section-2-10"></a>
## 2.10. Mini Project — Measurement Card

### 프로젝트 목표

장치의 이름과 측정 기온, 보정값, 측정 횟수를 입력받아 측정 정보를 정리한 콘솔 프로그램을 작성합니다. **변수, 정수·실수 자료형, 상수, 명시적 형변환, 출력 자릿수 설정**을 활용합니다.

**제공 파일**

- [프로젝트 시작 코드 — measurement_card.cpp](./project/measurement_card.cpp)
- [프로젝트 모범답안 — measurement_card.cpp](./solutions/measurement_card.cpp)

### 구현 요구사항

1. `std::getline()`으로 공백을 포함한 장치 이름을 입력받습니다.
2. `double` 타입의 측정 기온과 보정값, `int` 타입의 측정 횟수를 순서대로 입력받습니다.
3. 측정 기온과 보정값을 더한 값을 `const double` 변수에 저장합니다.
4. 측정 기온을 `static_cast<int>`로 변환하여 정수 부분을 저장합니다.
5. 실수는 모두 소수 둘째 자리까지 출력하고, 나머지 항목은 지정된 순서를 따릅니다.

**입력·출력 예시**

```text
Device: Robotics Lab Sensor
Temperature (C): 23.75
Offset (C): -0.25
Samples: 12

--- Measurement Card ---
Device: Robotics Lab Sensor
Temperature: 23.75 C
Offset: -0.25 C
Adjusted: 23.50 C
Samples: 12
Whole degrees: 23
```

**완료 기준**

- **문자열 입력:** 장치 이름에 공백이 포함되어도 전체 이름을 읽어야 합니다.
- **자료형 구분:** 측정 기온·보정값은 `double`, 측정 횟수는 `int`로 처리해야 합니다.
- **값과 자릿수:** 보정 결과는 두 수의 합과 일치하고, 모든 실수 항목은 소수 둘째 자리까지 출력되어야 합니다.
- **형변환:** 정수 부분은 `static_cast<int>`로 구하며, 소수 부분을 0 방향으로 버려야 합니다.
- **출력 순서:** 입력 안내와 측정 카드의 출력 순서는 예시와 일치해야 합니다.
- **빌드 정합성:** `g++ -std=c++20` 옵션으로 오류 없이 컴파일되어야 합니다.

해당 프로젝트는 정상 형식의 입력을 전제로 하며, 복잡한 입력 검증이나 반복 입력 처리는 구현 대상에 포함하지 않습니다.

**프로젝트 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/measurement_card.cpp -o measurement
./measurement
```

**선택: 자동 검증**

```bash
python tests/check.py --mode student --only project
```

---

<a id="section-2-11"></a>
## 2.11. Quiz & Summary

### Quiz

각 문제의 답을 먼저 생각한 뒤 **정답 및 해설**을 펼쳐 확인하세요.

**Q1. 다음 코드에서 초기화와 대입의 차이는 무엇인가요?**

```cpp
int count{5};
count = 8;
```

<details>
<summary>정답 및 해설</summary>

**예시 답안:** `int count{5};`는 정수 변수를 선언하면서 5로 초기화합니다. `count = 8;`은 이미 존재하는 변수에 새로운 값 8을 대입합니다.

</details>

**Q2. `bool` 타입의 값으로 적절한 것은 무엇인가요?**

- A. `"true"`
- B. `true`
- C. `'T'`
- D. `3.14`

<details>
<summary>정답 및 해설</summary>

**정답: B**

`true`와 `false`는 `bool` 리터럴입니다. `"true"`는 문자열 리터럴이고, `3.14`는 실수 리터럴입니다. `'T'`는 문자 리터럴이므로 `bool` 리터럴과 다릅니다.

</details>

**Q3. 다음 중 `std::string`에 대한 올바른 설명은 무엇인가요?**

- A. C++의 기본 제공 정수 타입입니다.
- B. 문자 하나를 반드시 저장하는 타입입니다.
- C. 표준 라이브러리에서 제공하는 문자열 타입입니다.
- D. 모든 입력을 자동으로 검증하는 기능입니다.

<details>
<summary>정답 및 해설</summary>

**정답: C**

`std::string`은 여러 문자를 저장하고 다룰 수 있는 표준 라이브러리 타입입니다. `char`는 문자 코드 단위를 나타내며, `std::string` 자체가 입력값의 유효성을 보장하지는 않습니다.

</details>

**Q4. `int value{3.5};`가 일반적으로 컴파일 오류를 일으키는 이유를 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** 중괄호 초기화는 실수에서 정수로의 축소 변환을 허용하지 않기 때문입니다.

`3.5`의 소수 부분이 사라질 수 있으므로 `int value{3.5};`는 올바른 초기화가 아닙니다. 의도적으로 변환하려면 값의 범위를 확인하고 `static_cast<int>`처럼 명시적 변환을 사용합니다.

</details>

**Q5. 다음 리터럴의 십진수 값은 무엇인가요?**

```cpp
0b0101
0xFF
```

<details>
<summary>정답 및 해설</summary>

**정답:** `0b0101`은 5, `0xFF`는 255입니다.

`0b`는 이진수, `0x`는 16진수 리터럴을 나타냅니다.

</details>

**Q6. `const`와 `constexpr`의 관계로 가장 적절한 것은 무엇인가요?**

- A. 두 키워드는 언제나 같은 의미입니다.
- B. `const` 변수는 항상 실행 중에 값이 변경됩니다.
- C. `constexpr` 변수는 상수식으로 초기화되어야 합니다.
- D. `constexpr` 변수는 반드시 문자열만 저장합니다.

<details>
<summary>정답 및 해설</summary>

**정답: C**

`const`는 초기화 후 변경할 수 없도록 하고, `constexpr` 변수는 컴파일 시점에 평가할 수 있는 상수식으로 초기화되어야 합니다. 두 키워드의 의미가 완전히 같은 것은 아닙니다.

</details>

**Q7. 다음 코드에서 `value`의 자료형은 무엇이고 언제 결정되나요?**

```cpp
auto value = 23.5;
```

<details>
<summary>정답 및 해설</summary>

**정답:** `double`이며 컴파일 시점에 결정됩니다.

`23.5`는 기본적으로 `double` 리터럴이므로 `auto`가 `double`을 추론합니다. `auto`가 실행 중에 자료형을 바꾸는 기능은 아닙니다.

</details>

**Q8. `static_cast<int>(-3.9)`의 결과는 무엇인가요?**

- A. `-4`
- B. `-3`
- C. `3`
- D. 항상 컴파일 오류

<details>
<summary>정답 및 해설</summary>

**정답: B**

부동소수점을 정수로 변환할 때 소수 부분은 **0 방향으로 제거**되므로 결과는 `-3`입니다. 가장 가까운 정수로 반올림하거나 무조건 내림하는 동작과 다릅니다. 이러한 변환은 대상 정수 타입으로 표현 가능한 유한한 실수값에서만 사용해야 합니다.

</details>

**Q9. `std::in_range<std::uint8_t>(300)`이 반환하는 값은 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

**정답:** `false`입니다.

8비트 부호 없는 정수의 범위는 0~255이므로 값 300을 손실 없이 저장할 수 없습니다. `std::in_range`는 C++20에서 도입된 정수 범위 확인 함수입니다.

</details>

**Q10. `std::fixed << std::setprecision(2)`를 적용하면 어떤 점이 달라지나요?**

- A. 모든 실수 변수의 실제 값이 소수 둘째 자리에서 잘립니다.
- B. 화면에 표시할 때 소수점 아래 두 자리로 출력 형식이 변경됩니다.
- C. `double` 변수가 `int`로 바뀝니다.
- D. 모든 계산에서 오차가 제거됩니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

출력 형식만 바뀌며 변수 내부의 실제 값을 바꾸거나 부동소수점 오차를 제거하지는 않습니다. A·D는 표시 형식과 저장·계산 정확도를 혼동한 설명이고 C는 자료형 변경과 관련이 없습니다.

</details>

**Q11. `enum class`를 이용하면 숫자 상태값 대신 어떤 방식으로 의미를 나타낼 수 있나요?**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** `DeviceState::running`처럼 열거형 이름과 항목 이름을 함께 사용하여 상태의 의미를 드러낼 수 있습니다.

`enum class`의 항목은 일반 정수로 자동 변환되지 않으며, 정수 코드를 출력하려면 필요한 경우 `static_cast` 등을 사용합니다.

</details>

**Q12. `float`와 `double`로 십진 소수를 처리할 때 주의할 점을 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** 일부 십진 소수는 이진 부동소수점으로 정확히 표현할 수 없어 근사값으로 저장됩니다. 따라서 계산과 비교에서 작은 오차가 생길 수 있습니다.

출력 자릿수 조절은 표현 형식만 바꾸므로 정확한 십진 연산이 필요한 경우에는 저장 방식과 수치 계산 정책을 별도로 고려해야 합니다.

</details>

### Summary

- **변수:** 이름 있는 객체에 값을 저장하며, 선언·초기화와 재대입을 구분합니다.
- **기본 자료형:** `bool`, `char`, `int`, `long long`, `float`, `double` 등을 사용합니다.
- **문자열:** `std::string`은 표준 라이브러리 문자열 타입입니다.
- **비트·바이트:** 비트는 0과 1을 표현하는 이진 정보의 한 자리이며, 일반적인 PC에서 1바이트는 8비트입니다.
- **고정 폭 정수:** `<cstdint>`의 `std::int32_t`, `std::uint16_t` 등을 필요에 따라 사용합니다.
- **리터럴:** 코드에 직접 작성한 값이며, 이진수(`0b`), 16진수(`0x`), 자릿수 구분(`'`) 등을 사용할 수 있습니다.
- **상수:** `const`는 값 변경을 금지하고, `constexpr` 변수는 상수식 초기화를 요구합니다.
- **타입 추론:** `auto`는 초기화 식으로부터 컴파일 시점에 타입을 결정합니다.
- **형변환:** `static_cast`로 변환을 명시하고 값 손실 가능성을 확인합니다.
- **C++20:** `std::in_range`로 정수값의 표현 가능 범위를 확인합니다.
- **부동소수점:** 일부 십진 소수는 정확하게 저장되지 않으며, 출력 자릿수와 내부 값은 구분합니다.
- **열거형:** `enum class`는 이름을 가진 상태 항목을 정의합니다.

### References

- [ISO C++ — The Standard](https://isocpp.org/std/the-standard)
- [cppreference — Fundamental Types](https://en.cppreference.com/w/cpp/language/types)
- [cppreference — List-initialization](https://en.cppreference.com/w/cpp/language/list_initialization)
- [cppreference — Fixed-width Integer Types](https://en.cppreference.com/w/cpp/types/integer)
- [cppreference — `std::numeric_limits`](https://en.cppreference.com/w/cpp/types/numeric_limits)
- [cppreference — `std::in_range`](https://en.cppreference.com/w/cpp/utility/in_range)
- [cppreference — `std::to_underlying` (C++23)](https://en.cppreference.com/w/cpp/utility/to_underlying)
- [cppreference — `std::setprecision`](https://en.cppreference.com/w/cpp/io/manip/setprecision)
- [cppreference — `std::boolalpha` / `std::noboolalpha`](https://en.cppreference.com/w/cpp/io/manip/boolalpha)
- [cppreference — `CHAR_BIT` (Bytes and Bits)](https://en.cppreference.com/w/cpp/types/climits)

---

[← C++ 목차](../README.md#part-1--c-fundamentals)
