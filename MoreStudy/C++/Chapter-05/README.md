# Chapter 05. Functions

함수(Function)를 정의하고 호출하는 방법부터 매개변수·반환값, 값 전달과 읽기 전용 참조, 기본 인수, 함수 오버로딩, 람다(Lambda), 헤더와 구현 파일 분리 및 함수 테스트까지 학습합니다. 여러 작업을 함수로 나누고 각 함수의 결과를 검증하는 방법을 다룹니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17의 주요 기능을 함께 사용하며, C++23의 관련 기능은 참고 사항으로 소개합니다.

<details>
<summary>선행 학습</summary>

- [Chapter 01. Getting Started with C++](../Chapter-01/) — 프로그램 구조, 표준 입출력, 컴파일·링크
- [Chapter 02. Variables & Data Types](../Chapter-02/) — 자료형, 상수, 형변환, `auto`
- [Chapter 03. Operators & Conditions](../Chapter-03/) — 산술·논리 연산, `if`, `switch`, 오류 처리
- [Chapter 04. Loops](../Chapter-04/) — 반복문, 누적 계산, `break`, `continue`

</details>

## Contents

| Section | Topic |
|:---:|---|
| [5.1](#section-5-1) | Function Basics — 함수의 목적과 구성 |
| [5.2](#section-5-2) | Declaration & Definition — 선언, 정의, 호출 |
| [5.3](#section-5-3) | Parameters & Pass by Value — 값 전달 |
| [5.4](#section-5-4) | Return Values & `void` — 반환값 |
| [5.5](#section-5-5) | Read-Only Parameters — `const&`, `std::string_view` |
| [5.6](#section-5-6) | Default Arguments & Overloading |
| [5.7](#section-5-7) | Scope & Lifetime — 변수의 유효 범위 |
| [5.8](#section-5-8) | Optional Results — `std::optional` |
| [5.9](#section-5-9) | Function Contracts — `constexpr`, `[[nodiscard]]`, `noexcept` |
| [5.10](#section-5-10) | Lambda & Capture — 람다 표현식 |
| [5.11](#section-5-11) | Multi-File Programs — 선언·구현 파일 분리 |
| [5.12](#section-5-12) | Function Testing — 결과 검증 |
| [5.13](#section-5-13) | Coding Practice |
| [5.14](#section-5-14) | Mini Project — Sensor Calibration Report |
| [5.15](#section-5-15) | Quiz & Summary |

## Getting Started

아래 명령어는 **`Chapter-05/` 디렉터리**에서 실행하는 경우를 기준으로 합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_function_basics.cpp -o functions
./functions
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_function_basics.cpp -o functions
./functions
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_function_basics.cpp /Fe:functions.exe
functions.exe
```

Windows PowerShell에서는 `./functions` 대신 `.\functions.exe`로 실행합니다. 컴파일러 설정은 [Chapter 01](../Chapter-01/)에서 확인할 수 있습니다.

**학습 목표**

1. 함수를 선언·정의·호출하고 매개변수와 인수의 차이를 설명할 수 있습니다.
2. 값 전달·읽기 전용 참조와 반환값을 상황에 맞게 사용할 수 있습니다.
3. 기본 인수·오버로딩·람다를 활용하여 짧은 기능을 구성할 수 있습니다.
4. 함수가 반환할 유효한 결과가 없는 상황을 표현할 수 있습니다.
5. 여러 소스 파일의 함수를 연결하고 입력·경계값·오류 사례를 검증할 수 있습니다.

---

<a id="section-5-1"></a>
## 5.1. Function Basics — 함수의 목적과 구성

**함수(Function)** 는 특정 작업을 수행하도록 이름을 붙인 코드 단위입니다. 계산식을 반복해서 작성하는 대신 함수로 분리하면 입력, 동작, 결과를 한곳에서 관리할 수 있습니다.

```cpp
double rectangle_area(double width, double height) {
    return width * height;
}
```

| 구성 요소 | 의미 | 예시 |
|---|---|---|
| 반환 자료형(Return Type) | 함수가 돌려주는 값의 타입 | `double` |
| 함수 이름(Function Name) | 호출에 사용하는 이름 | `rectangle_area` |
| 매개변수(Parameter) | 함수 정의에서 입력을 받는 이름 | `width`, `height` |
| 함수 본문(Body) | 실제로 실행하는 코드 | `{ ... }` |
| 반환(Return) | 결과를 호출한 곳으로 돌려줌 | `return width * height;` |

**예제 코드 — [01_function_basics.cpp](./examples/01_function_basics.cpp)**

```cpp
#include <iostream>

double rectangle_area(double width, double height) {
    return width * height;
}

int main() {
    std::cout << "Area: " << rectangle_area(2.5, 4.0) << " m2\n";
}
```

**실행 결과**

```text
Area: 10 m2
```

`rectangle_area(2.5, 4.0)`에서 `2.5`와 `4.0`은 **인수(Argument)** 입니다. 함수에 전달된 값이 매개변수 `width`와 `height`를 초기화합니다. 함수가 반환한 `10.0`을 `std::cout`으로 출력합니다.

함수 이름에는 `calculate_total`, `print_status`처럼 수행하는 동작을 드러내는 표현이 유용합니다. 입력·계산·출력을 무조건 하나의 함수에 묶을 필요는 없습니다.

---

<a id="section-5-2"></a>
## 5.2. Declaration & Definition — 선언, 정의, 호출

**선언(Declaration)** 은 함수의 이름·매개변수·반환 자료형을 컴파일러에 알리는 구문입니다. **정의(Definition)** 는 함수의 본문을 작성하는 구문입니다. **호출(Call)** 은 실제로 함수를 실행하도록 요청하는 동작입니다.

```cpp
int remaining_stock(int received, int shipped);  // 선언
```

끝에 세미콜론(`;`)이 있고 본문이 없으므로 선언입니다. 함수를 호출하는 위치보다 앞에서 선언이 알려져 있다면, 함수의 정의는 `main()` 뒤에 있어도 됩니다.

**예제 코드 — [02_declaration_definition.cpp](./examples/02_declaration_definition.cpp)**

```cpp
#include <iostream>

int remaining_stock(int received, int shipped);  // Declaration

int main() {
    std::cout << "Remaining: " << remaining_stock(25, 13) << '\n';
}

int remaining_stock(int received, int shipped) {  // Definition
    return received - shipped;
}
```

**실행 결과**

```text
Remaining: 12
```

`main()`에서 `remaining_stock()`을 호출할 때 컴파일러는 앞쪽에 있는 함수 선언을 확인합니다. 이후 정의에서 `received - shipped`를 계산합니다. 함수가 선언만 있고 정의가 연결되지 않으면 링크 단계에서 오류가 발생할 수 있습니다.

함수의 선언과 정의에는 서로 호환되는 매개변수 타입과 반환 타입을 사용해야 합니다. 다른 파일로 분리할 때도 동일한 원칙이 적용됩니다.

---

<a id="section-5-3"></a>
## 5.3. Parameters & Pass by Value — 값 전달

**값 전달(Pass by Value)** 은 인수의 값을 복사해 함수의 매개변수를 초기화하는 방식입니다. 함수 안에서 매개변수를 변경해도 호출한 쪽의 원본 변수는 바뀌지 않습니다.

```cpp
int add_one(int number) {
    ++number;
    return number;
}
```

`number`는 함수 안에 따로 존재하는 매개변수입니다. `add_one(original)`을 호출해도 `original`은 변경되지 않습니다.

**예제 코드 — [03_pass_by_value.cpp](./examples/03_pass_by_value.cpp)**

```cpp
#include <iostream>
#include <string>

std::string add_suffix(std::string name) {
    name += "-A";
    return name;
}

int main() {
    const std::string original{"SENSOR"};
    std::cout << "Original: " << original << '\n';
    std::cout << "Updated: " << add_suffix(original) << '\n';
}
```

**실행 결과**

```text
Original: SENSOR
Updated: SENSOR-A
```

함수는 문자열의 복사본에 `-A`를 추가해 반환합니다. 원래 문자열은 그대로 유지됩니다. 정수·실수처럼 작은 값은 값 전달이 간단하고, 문자열처럼 복사 비용이 있는 값은 다음 Section의 읽기 전용 전달 방식도 고려할 수 있습니다.

---

<a id="section-5-4"></a>
## 5.4. Return Values & `void` — 반환값

함수는 계산 결과를 `return`으로 반환하거나, 반환값이 필요 없다면 반환 자료형에 `void`를 지정할 수 있습니다.

| 구문 | 용도 |
|---|---|
| `int calculate(...)` | `int` 결과를 반환 |
| `bool is_valid(...)` | 참·거짓 반환 |
| `std::string make_label(...)` | 문자열 반환 |
| `void print_result(...)` | 호출자에게 값을 반환하지 않음 |

`return`을 실행하면 해당 함수는 즉시 종료되고 호출한 위치로 흐름이 돌아갑니다. `void` 함수는 `return;`으로 일찍 종료할 수 있지만, `return 10;`처럼 값을 반환할 수는 없습니다.

**예제 코드 — [04_return_and_void.cpp](./examples/04_return_and_void.cpp)**

```cpp
#include <iostream>

int square(int number) {
    return number * number;
}

void print_result(int value) {
    std::cout << "Squared: " << value << '\n';
}

int main() {
    const int answer{square(6)};
    print_result(answer);
}
```

**실행 결과**

```text
Squared: 36
```

`square()`는 계산 결과를 반환하고, `print_result()`는 화면에 출력하는 역할만 담당합니다. 계산 함수에서 표준 출력을 직접 수행하지 않으면 같은 함수를 다른 프로그램이나 테스트에서 재사용하기 쉬워집니다.

---

<a id="section-5-5"></a>
## 5.5. Read-Only Parameters — `const&`, `std::string_view`

`const std::string&`는 문자열 객체를 복사하지 않고 **읽기 전용 참조(Const Reference)** 로 전달하는 방식입니다. 여기서 `&`는 참조를 나타내고, `const`는 함수를 통해 해당 값을 수정하지 못하도록 합니다. 참조의 상세한 동작과 객체 수명은 Chapter 07에서 다룹니다.

```cpp
void print_device(const std::string& name);
```

**`std::string_view`(문자열 뷰)** 는 문자열의 내용을 소유하지 않고 읽기 위한 C++17 타입입니다. `<string_view>` 헤더를 포함해야 합니다. 원본 문자열의 수명이 끝나면 해당 내용을 안전하게 사용할 수 없으므로, 함수를 호출하는 동안 읽기만 하는 용도로 먼저 익히면 됩니다.

C++20의 `std::string_view::starts_with()`는 문자열이 지정한 접두사로 시작하는지 `bool`로 알려줍니다.

**예제 코드 — [05_read_only_parameters.cpp](./examples/05_read_only_parameters.cpp)**

```cpp
#include <iostream>
#include <string>
#include <string_view>

void print_device(const std::string& name) {
    std::cout << "Device: " << name << '\n';
}

bool has_prefix(std::string_view name) {
    return name.starts_with("DEV-");
}

int main() {
    const std::string name{"DEV-42"};
    print_device(name);
    std::cout << std::boolalpha << "Valid prefix: " << has_prefix(name) << '\n';
}
```

**실행 결과**

```text
Device: DEV-42
Valid prefix: true
```

`print_device()`는 `std::string`을 참조로 전달받고, `has_prefix()`는 `std::string_view`로 내용을 검사합니다. 값을 읽기만 하는 상황에서 사용할 수 있는 두 방식이지만, 함수가 문자열을 저장하거나 소유해야 한다면 다른 설계가 필요합니다.

---

<a id="section-5-6"></a>
## 5.6. Default Arguments & Overloading

**기본 인수(Default Argument)** 는 함수를 호출할 때 생략할 수 있는 매개변수의 기본값입니다. 기본값이 있는 매개변수는 일반적으로 뒤쪽에 배치합니다.

```cpp
int shipping_fee(int order_won, int base_fee = 3000);
```

`shipping_fee(42000)`은 `base_fee`로 `3000`을 사용하고, `shipping_fee(42000, 4500)`은 직접 전달한 `4500`을 사용합니다.

**함수 오버로딩(Function Overloading)** 은 함수 이름은 같지만 매개변수의 **개수 또는 타입이 다른 함수**를 정의하는 기능입니다. 반환 자료형만 다른 함수는 오버로딩할 수 없습니다.

**예제 코드 — [06_defaults_and_overloads.cpp](./examples/06_defaults_and_overloads.cpp)**

```cpp
#include <iostream>

int shipping_fee(int order_won, int base_fee = 3000) {
    return order_won >= 50000 ? 0 : base_fee;
}

void show_value(int value) {
    std::cout << "Count: " << value << '\n';
}

void show_value(double value) {
    std::cout << "Temperature: " << value << " C\n";
}

int main() {
    std::cout << "Shipping: " << shipping_fee(42000) << " won\n";
    std::cout << "Custom shipping: " << shipping_fee(42000, 4500) << " won\n";
    show_value(12);
    show_value(23.5);
}
```

**실행 결과**

```text
Shipping: 3000 won
Custom shipping: 4500 won
Count: 12
Temperature: 23.5 C
```

`show_value(12)`는 `int` 버전을, `show_value(23.5)`는 `double` 버전을 호출합니다. 기본 인수와 오버로딩을 함께 사용하면 호출이 모호해질 수 있으므로 함수 인터페이스를 단순하게 유지하는 편이 좋습니다.

---

<a id="section-5-7"></a>
## 5.7. Scope & Lifetime — 변수의 유효 범위

**범위(Scope)** 는 이름을 사용할 수 있는 코드의 영역입니다. 함수 안에서 선언한 변수는 일반적으로 함수 밖에서 이름으로 접근할 수 없습니다. `{ ... }`로 감싼 블록 내부의 지역 변수는 그 블록에서만 사용할 수 있습니다.

**수명(Lifetime)** 은 객체가 존재하는 기간입니다. 일반적인 지역 변수는 해당 블록에서 선언 위치를 지나 초기화될 때부터 블록 종료까지 존재합니다. 이름을 사용할 수 있는 범위와 객체의 수명은 서로 관련되지만 동일한 개념은 아닙니다.

**예제 코드 — [07_scope_and_lifetime.cpp](./examples/07_scope_and_lifetime.cpp)**

```cpp
#include <iostream>

int next_attempt(int current) {
    const int updated{current + 1};
    return updated;
}

int main() {
    int attempt{1};
    {
        const int local_bonus{2};
        attempt += local_bonus;
    }
    std::cout << "Attempt: " << next_attempt(attempt) << '\n';
}
```

**실행 결과**

```text
Attempt: 4
```

`local_bonus`는 안쪽 `{ ... }` 블록을 벗어나면 사용할 수 없습니다. `next_attempt()`의 `current` 역시 함수 호출 때 전달되는 별도의 매개변수입니다. 같은 이름의 변수를 안쪽 범위에 다시 선언하는 **이름 가리기(Shadowing)** 는 혼란을 일으킬 수 있으므로 불필요하게 사용하지 않는 편이 좋습니다.

---

<a id="section-5-8"></a>
## 5.8. Optional Results — `std::optional`

계산 결과가 항상 존재하는 것은 아닙니다. 예를 들어 전체 용량이 0이면 사용 비율을 계산할 수 없습니다. 실패를 `-1` 같은 특수 숫자로 표현하면 정상 데이터와 구분하기 어려울 수 있습니다.

C++17에서 도입된 **`std::optional<T>`** 는 값이 있거나 없을 수 있는 결과를 표현합니다. 사용하려면 `<optional>` 헤더를 포함합니다.

| 표현 | 의미 |
|---|---|
| `std::optional<double>` | `double`이 있거나 없는 결과 |
| `std::nullopt` | 값이 없는 상태 |
| `result.has_value()` | 값 존재 여부 검사 |
| `*result` | 값이 있음을 확인한 뒤 내부 값 사용 |

`*result`는 여기서 `std::optional`에 들어 있는 값을 가져오는 표현입니다. Chapter 07에서 다루는 포인터 역참조와 같은 기호를 사용하지만, 사용하는 타입과 맥락이 다릅니다.

**예제 코드 — [08_optional_result.cpp](./examples/08_optional_result.cpp)**

```cpp
#include <iostream>
#include <optional>

std::optional<double> utilization(int used, int capacity) {
    if (capacity <= 0 || used < 0 || used > capacity) {
        return std::nullopt;
    }
    return 100.0 * used / capacity;
}

int main() {
    const auto valid{utilization(30, 40)};
    if (valid.has_value()) {
        std::cout << "Utilization: " << *valid << "%\n";
    }
    if (!utilization(5, 0).has_value()) {
        std::cout << "Invalid capacity\n";
    }
}
```

**실행 결과**

```text
Utilization: 75%
Invalid capacity
```

`utilization(5, 0)`은 유효한 비율을 반환할 수 없으므로 `std::nullopt`를 돌려줍니다. 값이 있는지 확인하지 않고 `*result`를 사용하는 것은 안전하지 않습니다. `std::optional`은 결과 유무를 표현하지만 **왜 실패했는지에 대한 상세한 오류 정보는 담지 않습니다.**

**C++23 참고 — `std::expected`**

C++23에는 정상 결과와 오류 정보를 함께 표현하는 `std::expected<T, E>`가 도입되었습니다. 해당 기능은 `<expected>` 헤더를 사용하며, 컴파일러와 표준 라이브러리의 지원 여부를 확인해야 합니다. 기본 예제에서는 C++20에서 사용할 수 있는 `std::optional`을 사용합니다.

---

<a id="section-5-9"></a>
## 5.9. Function Contracts — `constexpr`, `[[nodiscard]]`, `noexcept`

함수의 사용 의도와 제약을 표현하는 기능입니다.

| 요소 | 의미 | 주의 사항 |
|---|---|---|
| `constexpr` | 조건을 만족하면 컴파일 시점 계산이 가능 | 일반 실행 시점에도 호출 가능 |
| `[[nodiscard]]` | 반환값을 무시하면 진단하도록 권고 | 진단이 반드시 오류인 것은 아님 |
| `noexcept` | 함수에서 예외를 외부로 전파하지 않겠다는 명시 | 처리되지 않은 예외가 발생하면 `std::terminate()` 호출 |
| `static_assert` | 컴파일 시점에 조건을 검사 | 조건이 거짓이면 컴파일 실패 |

`constexpr`, `noexcept`, `static_assert`는 별도 헤더 없이 언어에서 제공하는 기능이며, `[[nodiscard]]`는 C++17에서 도입된 속성입니다.

**예제 코드 — [09_constexpr_and_attributes.cpp](./examples/09_constexpr_and_attributes.cpp)**

```cpp
#include <iostream>

[[nodiscard]] constexpr int clamp_score(int score) noexcept {
    if (score < 0) {
        return 0;
    }
    if (score > 100) {
        return 100;
    }
    return score;
}

static_assert(clamp_score(-1) == 0);
static_assert(clamp_score(101) == 100);

int main() {
    std::cout << "Score: " << clamp_score(125) << '\n';
}
```

**실행 결과**

```text
Score: 100
```

`static_assert`는 컴파일 시점에 `clamp_score()`의 경계값을 검사합니다. `noexcept`는 실제로 예외를 전파하지 않도록 설계할 수 있을 때 사용해야 하며, 모든 함수에 습관적으로 추가하는 기능은 아닙니다.

---

<a id="section-5-10"></a>
## 5.10. Lambda & Capture — 람다 표현식

**람다 표현식(Lambda Expression)** 은 짧은 함수를 필요한 위치에서 직접 정의하는 문법입니다. 이름 있는 함수를 새로 정의하지 않고도 값 비교나 조건 판정을 표현할 수 있습니다.

```cpp
int threshold{60};
const auto is_high = [threshold](int value) {
    return value > threshold;
};
```

- **`[threshold]`:** 바깥 변수 `threshold`의 값을 복사하는 **값 캡처(Value Capture)**
- **`(int value)`:** 호출 시 전달할 매개변수
- **`return value > threshold;`:** 판정 결과 반환
- **`is_high(70)`:** 람다 호출. `true` 반환

`[&threshold]`은 참조 캡처입니다. 참조 캡처를 사용하는 람다가 원본 변수보다 오래 살아남으면 문제가 생길 수 있으므로, 처음에는 값 캡처를 중심으로 사용하는 것이 안전합니다.

**예제 코드 — [12_lambda_capture.cpp](./examples/12_lambda_capture.cpp)**

```cpp
#include <iostream>

int main() {
    int threshold{60};
    const auto above_threshold = [threshold](int value) {
        return value > threshold;
    };

    int count{};
    for (const int value : {42, 68, 73, 49, 81}) {
        if (above_threshold(value)) {
            ++count;
        }
    }
    std::cout << "Above threshold: " << count << '\n';
}
```

**실행 결과**

```text
Above threshold: 3
```

예제에서는 값 5개를 순회하면서 `60`을 초과하는 값만 셉니다. 람다 내부에서는 바깥의 `threshold`를 값을 복사해 사용합니다. 람다를 표준 알고리즘에 전달하는 방법은 Chapter 10의 STL에서 더 자세히 다룹니다.

---

<a id="section-5-11"></a>
## 5.11. Multi-File Programs — 선언·구현 파일 분리

프로그램이 커지면 함수 선언과 구현을 여러 파일로 분리할 수 있습니다. **헤더 파일(Header File)** 은 외부에서 사용할 선언을 제공하고, **구현 파일(Source File)** 은 실제 함수 정의를 보관합니다.

```text
examples/10_multi_file/
├── inventory.hpp
├── inventory.cpp
└── main.cpp
```

**헤더 — [inventory.hpp](./examples/10_multi_file/inventory.hpp)**

```cpp
#ifndef MORESTUDY_CHAPTER05_INVENTORY_HPP
#define MORESTUDY_CHAPTER05_INVENTORY_HPP

#include <optional>

namespace inventory {

[[nodiscard]] std::optional<int> remaining_stock(int received, int shipped) noexcept;

}  // namespace inventory

#endif
```

`#include <optional>`은 표준 라이브러리의 헤더를 포함하고, `#include "inventory.hpp"`는 프로젝트의 헤더를 포함합니다. `#ifndef`·`#define`·`#endif`는 **헤더 가드(Header Guard)** 로, 같은 선언이 여러 번 포함되는 문제를 방지합니다.

`namespace inventory`는 관련 함수 이름을 묶어 다른 코드와의 이름 충돌을 피하는 네임스페이스입니다. `using namespace ...;` 지시문 없이 `inventory::remaining_stock()`처럼 호출합니다.

**구현 — [inventory.cpp](./examples/10_multi_file/inventory.cpp)**

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

**호출 — [main.cpp](./examples/10_multi_file/main.cpp)**

```cpp
#include "inventory.hpp"
#include <iostream>

int main() {
    const auto stock{inventory::remaining_stock(25, 13)};
    if (!stock.has_value()) {
        std::cerr << "Error: invalid inventory data.\n";
        return 1;
    }
    std::cout << "Available: " << *stock << '\n';
}
```

**컴파일 및 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic \
  examples/10_multi_file/main.cpp \
  examples/10_multi_file/inventory.cpp -o inventory
./inventory
```

**실행 결과**

```text
Available: 12
```

헤더에서 함수의 선언을 확인할 수 있지만 `inventory.cpp`를 빌드 명령어에서 빠뜨리면 구현이 연결되지 않아 링크 오류가 발생합니다. 이는 Chapter 01에서 학습한 컴파일과 링크의 차이를 보여주는 사례입니다.

---

<a id="section-5-12"></a>
## 5.12. Function Testing — 결과 검증

함수는 입력과 반환값이 분명하면 검증하기 쉽습니다. 정상값뿐 아니라 **최솟값·최댓값·범위 밖 값**을 확인하여 의도하지 않은 동작을 찾을 수 있습니다.

**예제 코드 — [11_function_tests.cpp](./examples/11_function_tests.cpp)**

```cpp
#include <iostream>

[[nodiscard]] constexpr int clamp_score(int score) noexcept {
    if (score < 0) {
        return 0;
    }
    if (score > 100) {
        return 100;
    }
    return score;
}

int main() {
    const bool passed = clamp_score(-10) == 0 &&
                        clamp_score(70) == 70 &&
                        clamp_score(150) == 100;
    if (!passed) {
        std::cerr << "Test failed\n";
        return 1;
    }
    std::cout << "All tests passed (3 cases)\n";
}
```

**실행 결과**

```text
All tests passed (3 cases)
```

`clamp_score()`는 `0~100`으로 값을 제한합니다. 테스트는 음수, 정상 범위, 초과값의 세 경우를 확인합니다. 조건이 거짓이면 오류 메시지를 출력하고 `1`을 반환하므로 자동화된 환경에서도 실패를 식별할 수 있습니다.

함수 테스트에는 정상 동작을 확인하는 사례뿐 아니라 입력 경계와 잘못된 사용을 확인하는 사례를 함께 포함하는 것이 좋습니다.

---

<a id="section-5-13"></a>
## 5.13. Coding Practice

각 문제의 시작 코드는 `exercises/`, 모범답안은 `solutions/`에 있습니다. 시작 코드의 `TODO` 부분을 구현하고 정답과 실행 결과를 비교합니다.

| No. | Practice | Exercise | Solution |
|:---:|---|---|---|
| 01 | Temperature Converter | [문제 코드](./exercises/01_temperature_converter.cpp) | [정답 코드](./solutions/01_temperature_converter.cpp) |
| 02 | Shipping Fee | [문제 코드](./exercises/02_shipping_fee.cpp) | [정답 코드](./solutions/02_shipping_fee.cpp) |
| 03 | Function Overload | [문제 코드](./exercises/03_function_overload.cpp) | [정답 코드](./solutions/03_function_overload.cpp) |
| 04 | Lambda Threshold | [문제 코드](./exercises/04_lambda_threshold.cpp) | [정답 코드](./solutions/04_lambda_threshold.cpp) |

### Exercise 01 — Temperature Converter

섭씨를 화씨로 변환하는 `to_fahrenheit(double)` 함수를 완성합니다. 화면 입출력 코드는 제공되며, 함수의 계산과 반환값을 직접 구현합니다.

**구현 조건**

- 매개변수와 반환 자료형 모두 `double` 사용
- 변환식: `Fahrenheit = Celsius × 9 / 5 + 32`
- 결과는 소수 첫째 자리까지 출력
- 숫자 입력 실패 시 오류 출력 후 종료

**입력 / 기대 출력**

```text
입력: 25
출력: Fahrenheit: 77.0
```

### Exercise 02 — Shipping Fee

주문 금액과 지역 구분값에 따라 배송비를 계산하는 `shipping_fee()` 함수를 완성합니다.

**구현 조건**

- 주문 금액이 음수이거나 지역 구분값이 `0`, `1`이 아니면 `std::nullopt` 반환
- 기본 배송비는 3,000원, 주문 금액이 50,000원 이상이면 기본 배송비 면제
- 지역 구분값이 `1`이면 2,000원을 추가
- 함수를 호출하는 코드는 반환값의 존재 여부를 확인한 뒤 결과 출력

**입력 / 기대 출력**

```text
입력: 60000 1
출력: Shipping: 2000 won
```

### Exercise 03 — Function Overload

동일한 이름의 함수 두 개를 정의해 정수와 실수를 서로 다른 방식으로 출력합니다.

**구현 조건**

- `show_reading(int)`는 `Count: N` 형식으로 출력
- `show_reading(double)`은 `Temperature: N C` 형식으로 출력
- 두 함수는 반환값 없는 `void` 함수로 구현

**실행 결과**

```text
Count: 12
Temperature: 23.5 C
```

### Exercise 04 — Lambda Threshold

임계값을 입력받아 5개의 정수 중 임계값을 **초과하는** 값의 개수를 계산합니다.

**구현 조건**

- `threshold`를 값으로 캡처하는 람다 구현
- `value > threshold` 조건을 만족하는 값만 카운트
- 임계값 또는 측정값 입력 실패 시 오류 출력 후 종료

**입력 예시**

```text
60
42 68 73 49 81
```

**기대 결과**

```text
High readings: 3
```

### 실행 및 검증

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/01_temperature_converter.cpp -o converter
./converter
```

모범답안을 컴파일하려면 `exercises/`를 `solutions/`로 변경하면 됩니다. 자동 검증은 다음 명령어를 사용합니다.

```bash
python3 tests/check.py
python3 tests/check.py --exercise 04
```

**첫 번째 명령어**는 예제와 모범답안, Mini Project의 모범 구현을 확인하는 용도입니다. **두 번째 명령어**는 직접 수정한 Exercise 04를 검사합니다. 아직 코드가 작성되지 않아 초기 상태에는 FAIL이 나오는 것이 정상입니다. Test Runner는 소스코드를 C++20으로 컴파일한 뒤 다양한 입력을 전달하여 출력 결과와 종료 상태를 검증합니다.

---

<a id="section-5-14"></a>
## 5.14. Mini Project — Sensor Calibration Report

센서에서 수집한 측정값 세 개에 보정값(Offset)을 적용하고, 함수별 계산 결과를 이용해 보고서를 출력하는 콘솔 프로그램을 작성합니다.

**구현 파일**

- [시작 코드](./project/calibration_report.cpp)
- [모범답안](./solutions/calibration_report.cpp)

**프로그램 구성**

| 함수 | 역할 |
|---|---|
| `apply_offset(reading, offset)` | 측정값에 보정값을 더해 반환 |
| `average_of_three(first, second, third)` | 세 측정값의 산술평균 반환 |
| `status_of(adjusted_average)` | 평균 보정값이 35.0 초과면 `HIGH`, 그 외에는 `NORMAL` 반환 |
| `main()` | 입력값 확인, 함수 호출, 보고서 출력 |

**입력 예시**

```text
Lab Sensor A
-0.5
20
22
24
```

**실행 결과**

```text
Device: Lab Sensor A
Offset (C): -0.5
Reading 1 (C): 20
Reading 2 (C): 22
Reading 3 (C): 24

--- Calibration Report ---
Device: Lab Sensor A
Offset: -0.50 C
Average (raw): 22.00 C
Average (adjusted): 21.50 C
Status: NORMAL
```

**완료 기준**

- **함수의 역할 분리:** 보정, 평균 계산, 상태 판정을 각각 별도의 함수로 구현해야 합니다.
- **계산 결과:** 원본 평균과 보정 평균이 입력값에 맞게 계산되어야 합니다.
- **경계값 처리:** 보정 평균이 `35.00`이면 `NORMAL`, 초과하면 `HIGH`로 분류해야 합니다.
- **입력 처리:** 공백이 포함된 장치 이름을 온전히 읽고, 잘못된 숫자 및 허용 범위 밖의 값은 오류 처리해야 합니다.
- **빌드 및 출력:** `g++ -std=c++20`으로 정상 컴파일되며, 출력 항목과 순서는 명시된 예시를 따라야 합니다.

**입력 범위:** 보정값 `-20~20`, 개별 측정값 `-50~150`의 유한한 실수입니다. 시작 코드의 `<cmath>` 헤더는 실수의 유한성(`std::isfinite()`)을 검사할 때 사용합니다. 장치 이름은 공백을 포함할 수 있지만 빈 문자열은 허용하지 않습니다. 시작 코드의 입력 처리 부분은 제공되며, 세 함수의 `TODO` 구현에 집중합니다.

**컴파일**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/calibration_report.cpp -o calibration
./calibration
```

**검증**

```bash
python3 tests/check.py --project
```

프로젝트 시작 코드는 일부 함수가 미완성 상태이므로, 구현을 완료하기 전에는 검증에 실패할 수 있습니다.

---

<a id="section-5-15"></a>
## 5.15. Quiz & Summary

### Quiz

**Q1. 함수 선언(Declaration)에 관한 설명으로 올바른 것은 무엇인가요?**

A. 호출할 때마다 실행 파일을 새로 만듭니다.  
B. 함수 이름·매개변수·반환 자료형을 컴파일러에 알립니다.  
C. 함수의 본문을 반드시 포함해야 합니다.  
D. 모든 함수는 `main()`보다 앞에 정의되어야 합니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

함수 선언은 컴파일러에 함수의 인터페이스를 알립니다. 선언에 본문이 없어도 되므로 C는 틀렸습니다. 선언이 먼저 알려져 있다면 정의는 `main()` 뒤에 위치할 수 있으므로 D도 틀렸습니다.

</details>

**Q2. 다음 함수에서 `square(4)`의 반환값과 `return`의 역할을 설명하세요.**

```cpp
int square(int value) {
    return value * value;
}
```

<details>
<summary>정답 및 해설</summary>

**정답: 16**

매개변수 `value`에 4가 전달되므로 `4 × 4 = 16`을 계산합니다. `return`은 계산 결과를 호출한 곳으로 돌려주면서 해당 함수의 실행을 종료합니다.

</details>

**Q3. 값 전달(Pass by Value)에 관한 설명으로 올바른 것은 무엇인가요?**

A. 함수 내부에서 매개변수를 변경하면 원본도 항상 바뀝니다.  
B. 함수는 인수로 전달된 값의 별도 복사본을 매개변수로 사용합니다.  
C. 함수는 호출자의 지역 변수에 항상 직접 접근합니다.  
D. 값 전달에는 `return`을 사용할 수 없습니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

값으로 전달한 매개변수는 별도로 초기화되므로 함수 내부의 변경이 원본 변수에 직접 반영되지 않습니다. A와 C는 값 전달의 동작과 맞지 않으며, `return` 사용 여부는 매개변수를 전달하는 방식과 별개의 문제입니다.

</details>

**Q4. 반환 자료형을 `void`로 선언하는 이유는 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

`void`는 호출자에게 반환할 값이 없는 함수를 나타냅니다. 화면에 메시지를 출력하는 `print_result()`처럼 작업을 수행하지만 결과값을 돌려줄 필요가 없는 경우에 사용합니다. `void` 함수도 `return;`으로 일찍 종료할 수 있습니다.

</details>

**Q5. `const std::string&` 매개변수를 사용하는 이유와 주의할 점을 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**정답 예시:** 문자열 객체 전체를 복사하지 않고 읽기 위해 사용합니다. `const` 때문에 해당 참조를 통해 문자열을 수정할 수 없습니다. 참조 대상이 유효한 동안에만 사용해야 하며, 자세한 참조와 수명 규칙은 이후 학습합니다.

</details>

**Q6. 다음 호출에 대한 설명 중 맞는 것은 무엇인가요?**

```cpp
int shipping_fee(int order_won, int base_fee = 3000);
shipping_fee(42000, 4500);
```

A. `base_fee`는 `3000`으로 고정됩니다.  
B. 두 번째 인수 `4500`이 기본 인수를 대신합니다.  
C. 인수를 두 개 주면 함수 선언이 무효가 됩니다.  
D. 기본 인수가 있으면 반환값을 사용할 수 없습니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

기본 인수는 호출에서 해당 인수가 생략된 경우에만 사용됩니다. 두 번째 인수로 `4500`을 전달했으므로 `base_fee`는 `4500`으로 초기화됩니다.

</details>

**Q7. 다음 코드에서 `local_bonus`를 블록 밖에서 사용할 수 없는 이유는 무엇인가요?**

```cpp
int count{1};
{
    const int local_bonus{2};
    count += local_bonus;
}
// 이 위치에서 local_bonus를 사용할 수 있나요?
```

<details>
<summary>정답 및 해설</summary>

**정답: 사용할 수 없습니다.**

`local_bonus`는 안쪽 블록에서 선언된 지역 변수이기 때문에 블록 밖에서는 이름을 사용할 수 없습니다. 반면 `count`는 바깥 범위에 선언되어 블록을 벗어나도 사용할 수 있습니다.

</details>

**Q8. `std::optional<double>`이 `std::nullopt`를 반환하는 상황은 무엇을 의미하나요?**

A. 반드시 `0.0`을 반환한 것입니다.  
B. 실수 변환이 자동으로 발생한 것입니다.  
C. 유효한 결과값이 존재하지 않음을 나타냅니다.  
D. 프로그램이 반드시 종료되었습니다.

<details>
<summary>정답 및 해설</summary>

**정답: C**

`std::nullopt`는 값이 없는 상태입니다. `0.0`은 정상적인 실수값이 될 수 있으므로 A와 구분해야 합니다. 값이 없는 결과를 반환하더라도 호출자가 처리 방법을 결정할 수 있으므로 프로그램이 반드시 종료되는 것은 아닙니다.

</details>

**Q9. `constexpr` 함수와 `static_assert`는 어떤 관계가 있나요?**

<details>
<summary>정답 및 해설</summary>

**정답 예시:** `constexpr` 함수는 조건을 만족하는 호출을 컴파일 시점에 평가할 수 있습니다. `static_assert`는 그 결과를 상수식 조건으로 검사하며, 조건이 거짓이면 컴파일 오류를 발생시킵니다. `constexpr` 함수가 모든 호출에서 반드시 컴파일 시점에 실행되는 것은 아닙니다.

</details>

**Q10. 다음 중 `noexcept`에 대한 설명으로 올바른 것은 무엇인가요?**

A. 함수를 언제나 빠르게 실행하도록 보장합니다.  
B. 함수에서 오류 조건을 검사할 필요가 없어진다는 뜻입니다.  
C. 예외가 발생해도 무조건 무시하고 계속 실행합니다.  
D. 예외를 외부로 전파하지 않겠다는 계약을 나타냅니다.

<details>
<summary>정답 및 해설</summary>

**정답: D**

`noexcept` 함수에서 처리되지 않은 예외가 외부로 나가려 하면 `std::terminate()`가 호출됩니다. 단순히 성능을 높이는 키워드가 아니며, 오류 처리 자체를 대신하지도 않습니다.

</details>

**Q11. 다음 람다에서 `[threshold]`의 역할을 설명하세요.**

```cpp
int threshold{60};
const auto is_high = [threshold](int value) {
    return value > threshold;
};
```

<details>
<summary>정답 및 해설</summary>

**정답:** 바깥 변수 `threshold`의 값을 람다 내부로 복사하는 **값 캡처(Value Capture)** 입니다. 이 람다는 전달받은 값이 60보다 큰지 판단합니다. `[&threshold]`는 원본을 참조하는 캡처로, 원본 변수의 수명에 주의해야 합니다.

</details>

**Q12. 헤더에 함수가 선언되어 있지만 링크 단계에서 해당 함수의 정의를 찾지 못했습니다. 가장 먼저 확인할 사항은 무엇인가요?**

A. 출력에 `std::boolalpha`를 사용했는지  
B. 함수가 선언된 헤더의 글꼴 설정  
C. 함수가 정의된 `.cpp` 파일이 빌드 명령어에 포함되어 있는지  
D. 변수 이름이 전부 대문자인지

<details>
<summary>정답 및 해설</summary>

**정답: C**

함수 선언만으로 실행 코드가 생성되지는 않습니다. 별도의 `.cpp`에 정의되어 있다면 해당 파일도 컴파일·링크해야 합니다. 예제의 `inventory.cpp`가 빠지면 `remaining_stock()`의 정의를 찾을 수 없어 링크 오류가 발생할 수 있습니다.

</details>

### Summary

- **함수(Function):** 이름 있는 작업 단위. 선언·정의·호출로 사용
- **매개변수(Parameter) / 인수(Argument):** 함수 내부에서 받는 이름과 호출 시 전달하는 값
- **값 전달(Pass by Value):** 인수의 값을 복사하여 전달
- **반환값(Return Value):** `return`으로 돌려주는 결과, `void`는 반환값 없음
- **읽기 전용 참조:** `const T&`로 원본을 수정하지 않고 접근
- **`std::string_view`:** 소유하지 않는 읽기 전용 문자열 뷰
- **기본 인수 / 오버로딩:** 인수 생략 시 기본값 사용, 매개변수 차이로 동일 이름 함수 구분
- **범위와 수명:** 지역 이름이 보이는 영역과 객체가 존재하는 기간 구분
- **`std::optional`:** 정상 결과의 유무 표현
- **`constexpr` / `[[nodiscard]]` / `noexcept`:** 계산 가능성·반환값 사용·예외 계약 표현
- **람다:** 이름 없는 함수 객체와 바깥 변수 캡처
- **파일 분리:** 헤더에 선언, `.cpp`에 정의, 빌드 과정에서 연결
- **함수 테스트:** 정상값·경계값·오류 입력 검증

### References

- [cppreference — Functions](https://en.cppreference.com/w/cpp/language/functions)
- [cppreference — Default arguments](https://en.cppreference.com/w/cpp/language/default_arguments)
- [cppreference — Function overloading](https://en.cppreference.com/w/cpp/language/overload_resolution)
- [cppreference — Reference declaration](https://en.cppreference.com/w/cpp/language/reference)
- [cppreference — `std::string_view`](https://en.cppreference.com/w/cpp/string/basic_string_view)
- [cppreference — `std::optional`](https://en.cppreference.com/w/cpp/utility/optional)
- [cppreference — Lambda expressions](https://en.cppreference.com/w/cpp/language/lambda)
- [cppreference — `constexpr`](https://en.cppreference.com/w/cpp/language/constexpr)
- [cppreference — `std::expected` (C++23)](https://en.cppreference.com/w/cpp/utility/expected)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

---

[← C++ 목차](../README.md#contents)
