# Chapter 13. Templates & Generic Programming

C++23을 기준으로 Function Template, Concept, Constraint, Class Template, Ranges 및 Generic Library 설계를 다룹니다. 단순한 문법 소개에서 벗어나 **재사용 가능한 인터페이스를 어떻게 정의하고 검증하는지**를 중심으로 학습합니다.

본 자료는 **C++23(ISO/IEC 14882:2024)** 을 기준으로 작성되었습니다. 현재 출판된 표준을 기준으로 예제를 제공하며, C++26의 제안·초안 기능을 필수 코드에 사용하지 않습니다. GCC 14 이상 또는 필요한 C++23 표준 라이브러리를 지원하는 개발 환경을 권장합니다.

**선행 학습:** [Chapter 05 — Functions](../Chapter-05/) · [Chapter 10 — Standard Library (STL)](../Chapter-10/) · [Chapter 12 — Modern C++ & Resource Management](../Chapter-12/)

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [13.1](#section-13-1) | Templates와 Generic Programming의 목표 |
| [13.2](#section-13-2) | Function Template와 타입 추론 |
| [13.3](#section-13-3) | 표준 Concept과 Constraint |
| [13.4](#section-13-4) | Requires Expression과 사용자 정의 Concept |
| [13.5](#section-13-5) | Constraint와 Overload Resolution |
| [13.6](#section-13-6) | Class Template와 Generic Container |
| [13.7](#section-13-7) | Non-Type Template Parameter |
| [13.8](#section-13-8) | Class Template Argument Deduction (CTAD) |
| [13.9](#section-13-9) | Variadic Template와 Fold Expression |
| [13.10](#section-13-10) | Generic Lambda |
| [13.11](#section-13-11) | Compile-Time 분기 — if constexpr |
| [13.12](#section-13-12) | Type Traits와 Compile-Time 검사 |
| [13.13](#section-13-13) | Perfect Forwarding과 std::invoke |
| [13.14](#section-13-14) | Ranges와 Generic Algorithm |
| [13.15](#section-13-15) | Projection과 정렬 Customization |
| [13.16](#section-13-16) | SFINAE와 Modern Constraints |
| [13.17](#section-13-17) | Template Specialization과 타입 정책 |
| [13.18](#section-13-18) | C++23 Explicit Object Parameter |
| [13.19](#section-13-19) | Generic Error Handling — std::expected |
| [13.20](#section-13-20) | Mini Project — Generic Telemetry Pipeline |
| [13.21](#section-13-21) | 설계 시 참고 사항 |
| [13.22](#section-13-22) | Coding Practice |
| [13.23](#section-13-23) | Quiz & Summary |

---

<a id="section-13-1"></a>

## 13.1. Templates와 Generic Programming의 목표

템플릿(Template)은 자료형이나 컴파일 시점 상수를 매개변수로 받아, 여러 타입에서 재사용할 코드를 정의하는 기능입니다. 제네릭 프로그래밍(Generic Programming)은 특정 타입보다 **타입이 만족해야 할 연산과 계약**을 중심으로 코드를 설계하는 접근입니다.

- **일반 함수:** 매개변수의 자료형을 구체적으로 고정
- **Function Template:** 호출 시 타입을 추론하거나 명시적으로 지정
- **Class Template:** 자료형·크기 등을 전달받는 재사용 가능한 자료구조
- **Concept / Constraint:** 사용할 타입이 만족해야 하는 조건을 컴파일 시점에 명시
- **Instantiation:** 템플릿이 사용될 때 구체적인 타입에 맞는 선언·정의가 만들어지는 과정

템플릿이 모든 코드에서 바람직한 것은 아닙니다. 입력 자료형이 고정된 간단한 기능에는 일반 함수를 사용하고, 서로 다른 타입에서 같은 동작이 필요할 때 템플릿을 검토합니다. 인터페이스의 요구사항이 복잡해질 때는 Concept으로 계약을 표현할 수 있습니다.

| 방식 | 적합한 상황 | 고려 사항 |
|---|---|---|
| 일반 함수 | 입력 타입과 동작이 일정 | 명확한 API, 컴파일 메시지 단순 |
| 함수 템플릿 | 여러 타입에 동일 연산 적용 | 타입 추론, Instantiation 비용 |
| 클래스 템플릿 | 컨테이너·자료형 정책 재사용 | 템플릿 정의의 가시성 |
| Virtual Interface | 실행 시 구현 교체 | Runtime Dispatch와 객체 수명 |

**연결:** Chapter 09의 동적 다형성은 실행 시 구현을 선택하는 방식이고, 이 Chapter의 템플릿은 컴파일 시점에 타입을 기준으로 구현이 선택되는 경우가 많습니다. 목적에 따라 함께 사용할 수도 있습니다.

---

<a id="section-13-2"></a>

## 13.2. Function Template와 타입 추론

함수 템플릿(Function Template)은 함수의 입력 타입을 템플릿 매개변수로 선언합니다. 같은 정의로 정수와 실수 등 여러 자료형을 처리할 수 있습니다.

타입 추론(Template Argument Deduction)은 함수 인수로부터 템플릿 매개변수를 결정하는 과정입니다. 서로 다른 타입을 하나의 `T`로 추론해야 하는 호출은 실패할 수 있으므로, 암묵적 변환에 의존하지 않는 인터페이스가 더 명확할 때가 많습니다.

- **`template <typename T>`:** `T`를 타입 매개변수로 선언
- **`max_value(12, 19)`:** `T = int`로 추론
- **`max_value<double>(1, 2.5)`:** `T`를 명시하고 인수 변환 허용
- **주의:** 예제의 `<`는 비교가 가능한 타입에서만 사용 가능. 복잡한 라이브러리 API는 이 요구를 Concept 등으로 명시

**예제 코드 — [01_function_templates.cpp](./examples/01_function_templates.cpp)**

```cpp
#include <concepts>
#include <print>

template <typename T>
[[nodiscard]] constexpr T max_value(const T& left, const T& right) {
    return left < right ? right : left;
}

int main() {
    std::println("Maximum int: {}", max_value(12, 19));
    std::println("Maximum double: {}", max_value(1.5, 2.75));
    // max_value(1, 2.0); // T를 하나로 추론할 수 없음
    std::println("Explicit T: {}", max_value<double>(1, 2.5));
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/01_function_templates.cpp -o example
./example
```


**실행 결과**

```text
Maximum int: 19
Maximum double: 2.75
Explicit T: 2.5
```

---

<a id="section-13-3"></a>

## 13.3. 표준 Concept과 Constraint

컨셉(Concept)은 타입이 충족해야 하는 컴파일 시점의 조건을 나타냅니다. 제약 조건(Constraint)은 템플릿을 특정 타입이나 식에만 적용하도록 제한하는 규칙입니다.

`<concepts>`에는 `std::integral`, `std::floating_point`, `std::same_as`, `std::convertible_to`, `std::regular`처럼 재사용 가능한 표준 Concept이 정의되어 있습니다. 동일한 요구를 새 Concept으로 중복 선언하기보다 표준 기능부터 검토합니다.

| Concept | 의미 | 참고 |
|---|---|---|
| `std::integral<T>` | 정수 타입 | `bool`도 포함. 정수 범위/부호는 별도 고려 |
| `std::floating_point<T>` | 부동소수점 타입 | NaN·Infinity 등 입력값 검증은 별도 수행 |
| `std::same_as<A, B>` | 두 타입 일치 | 변환 가능 여부와는 다름 |
| `std::regular<T>` | 값 타입에 필요한 여러 연산 | 의미적 요구까지 컴파일러가 완전히 확인하지는 못함 |

Concept은 **컴파일 시점에 확인할 수 있는 성질**을 기술합니다. 숫자의 실제 범위처럼 실행 시 데이터에 따라 달라지는 조건까지 대체하지는 않습니다.

**예제 코드 — [02_standard_concepts.cpp](./examples/02_standard_concepts.cpp)**

```cpp
#include <concepts>
#include <print>

template <std::integral T>
[[nodiscard]] constexpr bool is_even(T value) noexcept {
    return value % 2 == 0;
}

template <std::floating_point T>
[[nodiscard]] constexpr T average(T left, T right) noexcept {
    return left / T{2} + right / T{2};
}

static_assert(is_even(42));
static_assert(average(2.0, 4.0) == 3.0);

int main() {
    std::println("Even: {}", is_even(42));
    std::println("Average: {}", average(2.0, 4.0));
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/02_standard_concepts.cpp -o example
./example
```


**실행 결과**

```text
Even: true
Average: 3
```

---

<a id="section-13-4"></a>

## 13.4. Requires Expression과 사용자 정의 Concept

요구식(Requires Expression)은 어떤 타입에 대해 멤버 함수 호출이나 반환값 변환이 가능한지 검사합니다. 외부 장치 SDK·프로토콜 모델·사용자 정의 자료형처럼 공통 멤버 계약이 필요한 경우 유용합니다.

`requires(const T& value)` 블록은 검증용 구문입니다. 실제 장치 객체를 생성하거나 메서드를 실행하지 않습니다. 다음 예제는 `name()`의 반환값이 `std::string_view`로 변환될 수 있는지만 확인합니다.

- **Simple Requirement:** 식이 문법적으로 유효한지 확인
- **Compound Requirement:** `{ expression } -> Concept;` 형태로 결과 타입 제약 추가
- **Nested Requirement:** `requires 조건식;`으로 추가 제약 표현
- **주의:** `name()`의 반환 문자열이 얼마나 오래 살아 있는지와 같은 Lifetime 조건은 별도 계약과 테스트가 필요

**예제 코드 — [03_requires_expression.cpp](./examples/03_requires_expression.cpp)**

```cpp
#include <concepts>
#include <print>
#include <string>
#include <string_view>

// 장치 이름을 문자열 뷰로 읽을 수 있는지만 컴파일 시점에 검사
template <typename T>
concept NamedDevice = requires(const T& value) {
    { value.name() } -> std::convertible_to<std::string_view>;
};

struct Device {
    std::string label{"Motor-A"};
    [[nodiscard]] std::string_view name() const noexcept { return label; }
};

struct AnonymousDevice { int id{1}; };
static_assert(NamedDevice<Device>);
static_assert(!NamedDevice<AnonymousDevice>);

template <NamedDevice T>
void print_name(const T& value) {
    std::println("Device: {}", value.name());
}

int main() {
    print_name(Device{});
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/03_requires_expression.cpp -o example
./example
```


**실행 결과**

```text
Device: Motor-A
```

---

<a id="section-13-5"></a>

## 13.5. Constraint와 Overload Resolution

함수 오버로딩(Overloading)은 함수 이름이 같더라도 매개변수 목록이나 Constraints에 따라 적절한 후보를 선택하는 기능입니다. `requires`는 템플릿 후보가 참여할 수 있는 조건을 명시합니다.

다음 예제에서는 정수, 부동소수점 및 텍스트를 구분합니다. 함수의 의미가 실제로 다르고 타입별 동작을 구분해야 하는 경우에 적합합니다.

**주의:** 서로 다른 Constraints의 포함 관계가 불분명하면 호출이 모호해질 수 있습니다. 지나치게 많은 오버로드보다 별도의 함수 이름이 더 명확한 경우도 있습니다.

**예제 코드 — [04_constraints_overloads.cpp](./examples/04_constraints_overloads.cpp)**

```cpp
#include <concepts>
#include <print>
#include <string_view>

template <std::integral T>
void show_type(T) { std::println("Integer input"); }

template <std::floating_point T>
void show_type(T) { std::println("Floating-point input"); }

void show_type(std::string_view) { std::println("Text input"); }

int main() {
    show_type(7);
    show_type(2.5);
    show_type(std::string_view{"ready"});
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/04_constraints_overloads.cpp -o example
./example
```


**실행 결과**

```text
Integer input
Floating-point input
Text input
```

---

<a id="section-13-6"></a>

## 13.6. Class Template와 Generic Container

클래스 템플릿(Class Template)은 자료형이나 크기를 매개변수로 받아 여러 타입의 객체를 동일한 구조로 관리합니다. 표준 라이브러리의 `std::vector<T>`나 `std::array<T, N>`가 대표적인 사례입니다.

예제 `FixedBuffer<T, Capacity>`는 타입과 고정 용량을 외부에서 지정하는 간단한 버퍼입니다. `push()`가 성공했는지 반환하므로 범위 초과를 조용히 무시하지 않습니다.

- **`T`:** 저장할 요소 자료형
- **`Capacity`:** 컴파일 시점에 결정할 최대 요소 개수
- **`static_assert`:** 잘못된 템플릿 인수의 사용을 컴파일 단계에서 차단
- **주의:** `std::array<T, Capacity>`로 요소를 미리 생성하므로 `T`의 기본 생성 가능성에 의존. 모든 타입에 일반화하려면 별도 저장 전략 필요

**예제 코드 — [05_class_templates.cpp](./examples/05_class_templates.cpp)**

```cpp
#include <array>
#include <cstddef>
#include <print>
#include <string>

template <typename T, std::size_t Capacity>
class FixedBuffer {
    static_assert(Capacity > 0, "Capacity must be positive");
public:
    [[nodiscard]] bool push(const T& value) {
        if (size_ == Capacity) return false;
        data_[size_++] = value;
        return true;
    }
    [[nodiscard]] std::size_t size() const noexcept { return size_; }
    [[nodiscard]] const T& at(std::size_t index) const { return data_.at(index); }
private:
    std::array<T, Capacity> data_{};
    std::size_t size_{};
};

int main() {
    FixedBuffer<std::string, 2> names;
    const bool first = names.push("front");
    const bool second = names.push("rear");
    const bool third = names.push("extra");
    std::println("Inserted: {} {} {}", first, second, third);
    std::println("Size: {}, First: {}", names.size(), names.at(0));
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/05_class_templates.cpp -o example
./example
```


**실행 결과**

```text
Inserted: true true false
Size: 2, First: front
```

---

<a id="section-13-7"></a>

## 13.7. Non-Type Template Parameter

비타입 템플릿 매개변수(Non-Type Template Parameter, NTTP)는 타입이 아니라 컴파일 시점에 결정되는 값을 템플릿 인수로 전달합니다. 배열 크기, 격자 크기, 정책 플래그 등에 사용합니다.

아래 `Grid<Rows, Columns>`은 크기를 타입에 포함해 일정한 크기의 데이터를 안전하게 다룹니다. 크기가 자주 달라지거나 실행 중에 결정된다면 일반적인 동적 컨테이너를 검토합니다.

- **장점:** 고정 크기 제약과 메모리 크기를 컴파일 시점에 표현
- **한계:** 서로 다른 크기의 템플릿 인스턴스는 서로 다른 타입
- **검증:** 인덱스의 실제 값은 실행 시 `at()`으로 검사

**예제 코드 — [06_non_type_parameters.cpp](./examples/06_non_type_parameters.cpp)**

```cpp
#include <array>
#include <cstddef>
#include <print>

template <std::size_t Rows, std::size_t Columns>
struct Grid {
    static_assert(Rows > 0 && Columns > 0);
    std::array<int, Rows * Columns> cells{};

    [[nodiscard]] int& at(std::size_t row, std::size_t column) {
        return cells.at(row * Columns + column);
    }
};

int main() {
    Grid<3, 4> grid;
    grid.at(1, 2) = 9;
    std::println("Cell: {}", grid.at(1, 2));
    std::println("Elements: {}", grid.cells.size());
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/06_non_type_parameters.cpp -o example
./example
```


**실행 결과**

```text
Cell: 9
Elements: 12
```

---

<a id="section-13-8"></a>

## 13.8. Class Template Argument Deduction (CTAD)

클래스 템플릿 인수 추론(Class Template Argument Deduction, CTAD)은 생성자 인수를 바탕으로 클래스 템플릿의 타입 매개변수를 추론하는 기능입니다.

`std::pair{std::string{"A"}, 10}`처럼 타입을 반복하지 않아도 됩니다. 사용자 정의 클래스에서는 추론 가이드(Deduction Guide)로 추론 규칙을 명확하게 지정할 수 있습니다.

**주의:** 타입 추론이 의도와 다른 자료형을 선택할 수 있으므로 정밀도, 소유권, 단위가 중요한 경우 타입을 명시하는 편이 안전합니다.

**예제 코드 — [07_ctad_deduction_guides.cpp](./examples/07_ctad_deduction_guides.cpp)**

```cpp
#include <print>
#include <string>
#include <type_traits>
#include <utility>

template <typename T>
struct Reading {
    T value;
};

template <typename T>
Reading(T) -> Reading<T>;  // 사용자 정의 Deduction Guide

int main() {
    std::pair item{std::string{"Motor-A"}, 125}; // CTAD
    Reading temperature{23.5};                  // CTAD
    static_assert(std::is_same_v<decltype(temperature.value), double>);
    std::println("{}: {} RPM", item.first, item.second);
    std::println("Temperature: {}", temperature.value);
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/07_ctad_deduction_guides.cpp -o example
./example
```


**실행 결과**

```text
Motor-A: 125 RPM
Temperature: 23.5
```

---

<a id="section-13-9"></a>

## 13.9. Variadic Template와 Fold Expression

가변 인자 템플릿(Variadic Template)은 `T...`처럼 개수가 일정하지 않은 타입 인수를 처리합니다. 폴드 표현식(Fold Expression)은 매개변수 팩(Parameter Pack)의 요소에 연산자를 반복 적용합니다.

예제에서는 숫자 입력의 합을 계산하고, `0.0`을 초기값으로 사용해 빈 팩도 처리합니다. 모든 값이 `double`로 변환 가능해야 한다는 Constraint를 명시합니다.

- **`T...`:** 타입 매개변수 팩
- **`(0.0 + ... + values)`:** 초기값을 포함한 Fold
- **주의:** 모든 연산자와 모든 자료형에서 결합 법칙이 보장되는 것은 아님. 부동소수점 합계는 계산 순서에 따라 반올림 결과가 달라질 수 있음

**예제 코드 — [08_variadic_fold.cpp](./examples/08_variadic_fold.cpp)**

```cpp
#include <concepts>
#include <print>

template <typename... T>
    requires (std::convertible_to<T, double> && ...)
[[nodiscard]] double sum_readings(T... values) {
    return (0.0 + ... + static_cast<double>(values));
}

int main() {
    std::println("Total: {}", sum_readings(3, 4.5, 2));
    std::println("Empty total: {}", sum_readings());
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/08_variadic_fold.cpp -o example
./example
```


**실행 결과**

```text
Total: 9.5
Empty total: 0
```

---

<a id="section-13-10"></a>

## 13.10. Generic Lambda

제네릭 람다(Generic Lambda)는 매개변수에 `auto`를 사용해 다양한 타입을 받는 함수 객체를 만들 수 있습니다. 람다의 함수 호출 연산자는 템플릿처럼 동작합니다.

다음 예제에서는 임계값을 값으로 캡처하고, `std::ranges::count_if`를 이용해 조건을 만족하는 센서 측정값 개수를 계산합니다.

- **값 캡처 `[limit]`:** 람다 생성 시점의 값을 보관
- **참조 캡처 `[&limit]`:** 원본에 접근하므로 Lifetime 관리 필요
- **Generic Lambda:** 한정된 범위의 반복 알고리즘에서 간결한 형태로 사용

**예제 코드 — [09_generic_lambda.cpp](./examples/09_generic_lambda.cpp)**

```cpp
#include <algorithm>
#include <array>
#include <print>

int main() {
    const std::array readings{42, 75, 63, 18};
    const int limit{60};

    const auto above = [limit](const auto& value) {
        return value >= limit;
    };
    const auto count = std::ranges::count_if(readings, above);
    std::println("High readings: {}", count);
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/09_generic_lambda.cpp -o example
./example
```


**실행 결과**

```text
High readings: 2
```

---

<a id="section-13-11"></a>

## 13.11. Compile-Time 분기 — if constexpr

`if constexpr`는 컴파일 시점에 조건을 평가해 템플릿 정의 안에서 타입에 따른 분기를 처리할 수 있습니다. 선택되지 않은 분기의 코드는 해당 템플릿 인스턴스에서 사용되지 않습니다.

일반 `if`와 달리 `if constexpr`은 타입별로 성립하지 않는 코드를 분리할 때 유용합니다. 하지만 분기 조건이 지나치게 많다면 별도 오버로드나 함수 분리가 더 읽기 좋습니다.

다음 예제는 정수, 실수, 기타 타입의 로그 출력 형식을 구분합니다.

**예제 코드 — [10_if_constexpr.cpp](./examples/10_if_constexpr.cpp)**

```cpp
#include <concepts>
#include <print>
#include <string_view>

template <typename T>
void log_value(const T& value) {
    if constexpr (std::integral<T>) {
        std::println("Integer: {}", value);
    } else if constexpr (std::floating_point<T>) {
        std::println("Decimal: {:.2f}", value);
    } else {
        std::println("Other value");
    }
}

int main() {
    log_value(12);
    log_value(3.25);
    log_value(std::string_view{"ready"});
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/10_if_constexpr.cpp -o example
./example
```


**실행 결과**

```text
Integer: 12
Decimal: 3.25
Other value
```

---

<a id="section-13-12"></a>

## 13.12. Type Traits와 Compile-Time 검사

타입 특성(Type Traits)은 자료형의 분류, 타입 변환 여부, Const·참조 등의 속성을 컴파일 시점에 검사하거나 변형하는 도구입니다. `<type_traits>`에서 제공합니다.

`std::remove_cvref_t<T>`는 `const`, `volatile`, 참조 한정자를 제거한 타입을 얻는 별칭입니다. API의 정책을 비교할 때 활용할 수 있습니다.

- **`std::is_same_v<A, B>`:** 타입이 같은지 확인
- **`std::remove_cvref_t<T>`:** 최상위 cv 한정자와 참조 제거
- **`std::is_nothrow_move_constructible_v<T>`:** 예외 없는 Move 생성 가능 여부 조회
- **권장:** 단순한 타입 제약에서는 대응하는 표준 Concept을 우선 검토

Variable Template은 변수 선언이므로 `[[nodiscard]]`를 적용할 수 없습니다. `[[nodiscard]]`는 함수 또는 클래스·열거형 타입 등에 적용하는 속성입니다.

**예제 코드 — [11_type_traits.cpp](./examples/11_type_traits.cpp)**

```cpp
#include <concepts>
#include <print>
#include <type_traits>

// 함수 인수의 참조/const를 제거한 타입을 기준으로 검사
template <typename T>
constexpr bool is_numeric_v =
    std::integral<std::remove_cvref_t<T>> ||
    std::floating_point<std::remove_cvref_t<T>>;

int main() {
    const int value{7};
    static_assert(is_numeric_v<decltype((value))>);
    static_assert(!is_numeric_v<const char*>);
    std::println("Value: {}, numeric: {}", value, is_numeric_v<decltype((value))>);
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/11_type_traits.cpp -o example
./example
```


**실행 결과**

```text
Value: 7, numeric: true
```

---

<a id="section-13-13"></a>

## 13.13. Perfect Forwarding과 std::invoke

완벽 전달(Perfect Forwarding)은 전달받은 인수의 값 범주(Value Category)를 유지하면서 다른 함수에 전달하는 패턴입니다. 전달 참조(Forwarding Reference) `T&&`와 `std::forward<T>()`를 사용합니다.

`std::invoke`는 일반 함수, 람다, 멤버 함수 포인터처럼 호출 가능한 대상(Callable)을 공통 방식으로 실행합니다.

**주의:** `std::forward`는 어느 곳에서나 사용하는 이동 연산이 아닙니다. `T`가 템플릿 추론으로 결정되는 전달 참조 맥락에서 의도대로 활용해야 하며, 보관할 인수의 Lifetime과 소유권도 함께 검토해야 합니다.

**예제 코드 — [12_forwarding_invoke.cpp](./examples/12_forwarding_invoke.cpp)**

```cpp
#include <functional>
#include <print>
#include <string>
#include <utility>

template <typename F, typename... Args>
decltype(auto) call(F&& function, Args&&... args) {
    return std::invoke(std::forward<F>(function),
                       std::forward<Args>(args)...);
}

struct Logger {
    void show(const std::string& text) const { std::println("Log: {}", text); }
};

int main() {
    Logger logger;
    call(&Logger::show, logger, std::string{"ready"});
    const auto result = call([](int a, int b) { return a + b; }, 3, 5);
    std::println("Result: {}", result);
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/12_forwarding_invoke.cpp -o example
./example
```


**실행 결과**

```text
Log: ready
Result: 8
```

---

<a id="section-13-14"></a>

## 13.14. Ranges와 Generic Algorithm

범위(Range)는 순회 가능한 데이터 구간을 의미합니다. C++20부터 표준화된 Ranges는 Container뿐 아니라 View에도 동일한 인터페이스를 적용할 수 있게 해 줍니다.

이 예제는 `std::ranges::input_range`를 받아 임계값 이상의 입력을 필터링하고 두 배로 변환한 뒤 `std::vector`로 구체화합니다. `std::ranges::to`는 **C++23 기능**입니다.

- **`std::views::filter`:** 지연 평가되는 필터 View 생성
- **`std::views::transform`:** 각 요소를 변환하는 View 생성
- **`std::ranges::to<std::vector>()`:** 최종 결과를 소유하는 `vector`로 생성
- **대안:** C++23 `ranges::to` 미지원 시 `std::ranges::copy`와 `std::back_inserter` 등으로 구현 가능

View는 원본 데이터의 Lifetime과 요소 무효화(Invalidation)에 영향을 받을 수 있습니다. 위 함수는 결과를 `vector`로 만들어 반환하므로 원본 View를 외부에 보관하지 않습니다.

**예제 코드 — [13_ranges_generic.cpp](./examples/13_ranges_generic.cpp)**

```cpp
#include <array>
#include <concepts>
#include <print>
#include <ranges>
#include <utility>
#include <vector>

template <std::ranges::input_range R>
    requires std::ranges::viewable_range<R> &&
             std::convertible_to<std::ranges::range_reference_t<R>, int>
[[nodiscard]] std::vector<int> high_values(R&& readings, int threshold) {
    auto selected = std::forward<R>(readings)
                  | std::views::filter([threshold](int value) { return value >= threshold; })
                  | std::views::transform([](int value) { return value * 2; });
    return selected | std::ranges::to<std::vector>(); // C++23
}

int main() {
    const std::array readings{10, 25, 40, 15};
    const auto result = high_values(readings, 20);
    std::println("Selected: {}, first: {}", result.size(), result.front());
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/13_ranges_generic.cpp -o example
./example
```


**실행 결과**

```text
Selected: 2, first: 50
```

---

<a id="section-13-15"></a>

## 13.15. Projection과 정렬 Customization

투영(Projection)은 복합 객체에서 비교에 사용할 값을 추출하는 기능입니다. `std::ranges::sort`는 Comparator와 Projection을 별도로 받을 수 있습니다.

예를 들어 장치 구조체 전체의 `<` 연산자를 정의하지 않아도 `&Device::priority`를 지정해 우선순위 기준으로 정렬할 수 있습니다. Comparator는 엄격 약순서(Strict Weak Ordering)를 충족해야 합니다.

- **Comparator:** 값 사이의 순서 정의
- **Projection:** 실제 비교에 사용할 값 추출
- **주의:** 정렬은 원본 Container의 요소 순서를 변경. 원본 순서를 유지하려면 복사본 정렬 등을 검토

**예제 코드 — [14_projections.cpp](./examples/14_projections.cpp)**

```cpp
#include <algorithm>
#include <print>
#include <string>
#include <vector>

struct Device {
    std::string id;
    int priority;
};

int main() {
    std::vector<Device> devices{{"motor", 2}, {"camera", 3}, {"radar", 1}};
    std::ranges::sort(devices, std::ranges::greater{}, &Device::priority);
    for (const auto& device : devices) {
        std::println("{}: {}", device.id, device.priority);
    }
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/14_projections.cpp -o example
./example
```


**실행 결과**

```text
camera: 3
motor: 2
radar: 1
```

---

<a id="section-13-16"></a>

## 13.16. SFINAE와 Modern Constraints

대체 실패는 오류가 아님(Substitution Failure Is Not An Error, SFINAE)은 템플릿 인수를 대입하는 과정에서 특정 후보가 유효하지 않으면, 모든 컴파일을 중단하는 대신 해당 후보를 제외하는 원리입니다.

과거에는 `std::enable_if`로 타입 제약을 작성하는 경우가 많았습니다. 새 API에서는 동일한 의도를 `requires`, 표준 Concept으로 더 명확하게 표현할 수 있습니다.

| 구분 | 전통적인 방식 | 권장 고려 대상 |
|---|---|---|
| 정수 타입 제약 | `std::enable_if_t<std::is_integral_v<T>>` | `requires std::integral<T>` |
| 타입 속성 확인 | `std::is_same_v` | `std::same_as` 등 표준 Concept |
| 복잡한 유효 식 확인 | Detection Idiom | Requires Expression |

**유의:** 기존 SFINAE 코드는 호환성 차원에서 이해할 필요가 있지만, 모든 오래된 구현을 무조건 교체해야 하는 것은 아닙니다.

**예제 코드 — [15_constraints_vs_sfinae.cpp](./examples/15_constraints_vs_sfinae.cpp)**

```cpp
#include <concepts>
#include <print>
#include <type_traits>

// 구형 코드에서 흔히 보이는 형태
template <typename T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
[[nodiscard]] bool old_even(T value) { return value % 2 == 0; }

// 새 API에서 읽기 쉬운 제약 조건
template <typename T>
    requires std::integral<T>
[[nodiscard]] bool new_even(T value) { return value % 2 == 0; }

int main() {
    std::println("Old: {}, New: {}", old_even(6), new_even(7));
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/15_constraints_vs_sfinae.cpp -o example
./example
```


**실행 결과**

```text
Old: true, New: false
```

---

<a id="section-13-17"></a>

## 13.17. Template Specialization과 타입 정책

템플릿 특수화(Template Specialization)는 특정 템플릿 인수에 대해 별도 구현이나 정책을 지정하는 기능입니다. 다음 예제에서는 자료형에 따라 단위 표기를 선택합니다.

- **Primary Template:** 일반적인 구현
- **Explicit Specialization:** 특정 타입에 대한 별도 정의
- **Partial Specialization:** 일부 템플릿 인수만 패턴에 맞게 특수화. 함수 템플릿은 부분 특수화를 지원하지 않음

단순한 타입별 동작 차이는 `if constexpr`나 오버로드가 더 자연스러운 경우도 있습니다. 특수화는 외부에서 보이는 타입 계약을 명확하게 유지할 수 있을 때 선택합니다.

**예제 코드 — [16_specialization.cpp](./examples/16_specialization.cpp)**

```cpp
#include <print>
#include <string_view>

template <typename T>
struct UnitLabel { static constexpr std::string_view value = "units"; };

template <>
struct UnitLabel<double> { static constexpr std::string_view value = "C"; };

template <typename T>
void show_measurement(const T& value) {
    std::println("{} {}", value, UnitLabel<T>::value);
}

int main() {
    show_measurement(5);
    show_measurement(22.5);
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/16_specialization.cpp -o example
./example
```


**실행 결과**

```text
5 units
22.5 C
```

---

<a id="section-13-18"></a>

## 13.18. C++23 Explicit Object Parameter

명시적 객체 매개변수(Explicit Object Parameter)는 C++23의 기능으로, 멤버 함수 선언에 `this Self&& self` 형태의 객체 매개변수를 지정할 수 있습니다. **Deducing this**라는 이름으로도 알려져 있습니다.

예제에서는 하나의 `get()` 정의로 `const` 객체와 수정 가능한 객체의 값을 다룹니다. `decltype(auto)`를 사용할 때 반환 표현식의 괄호에 따라 참조가 유지되는지 달라질 수 있으므로 주의해야 합니다.

- **`this Self&& self`:** 객체의 cv/ref 속성을 템플릿으로 추론
- **`decltype(auto)`:** 반환 표현식에 따른 타입·참조 유지
- **컴파일러:** C++23 모드만 활성화했다고 모든 구현에서 지원하는 것은 아님. 지원 현황 확인 필요

이 기능은 유용하지만 단순한 Getter마다 적용할 필요는 없습니다. 중복되는 Ref-Qualified 멤버 함수를 줄이는 등 이점이 분명할 때 활용합니다.

**예제 코드 — [17_explicit_object_parameter.cpp](./examples/17_explicit_object_parameter.cpp)**

```cpp
#include <print>
#include <utility>

struct Counter {
    int value{};

    template <typename Self>
    [[nodiscard]] decltype(auto) get(this Self&& self) noexcept {
        return (std::forward<Self>(self).value);
    }
};

int main() {
    Counter counter{7};
    counter.get() = 9;  // lvalue 객체는 수정 가능한 참조로 반환
    const Counter fixed{4};
    std::println("Mutable: {}, const: {}", counter.get(), fixed.get());
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/17_explicit_object_parameter.cpp -o example
./example
```


**실행 결과**

```text
Mutable: 9, const: 4
```

---

<a id="section-13-19"></a>

## 13.19. Generic Error Handling — std::expected

`std::expected<T, E>`는 성공 결과 `T` 또는 오류 `E`를 전달하는 C++23 타입입니다. 다음 예제는 `std::integral`로 정수 타입을 제한하고 `std::from_chars`를 이용해 문자열을 파싱(Parsing)합니다.

숫자 변환에서는 값 범위 오류뿐 아니라 **입력 문자열을 끝까지 소비했는지** 확인해야 합니다. `"10ms"`처럼 일부만 변환되는 입력을 정상 처리하면 상위 로직에서 잘못된 데이터를 사용할 수 있습니다.

- **`std::unexpected(error)`:** 실패 결과 생성
- **`std::errc`:** 오류 종류 표현
- **제한:** 예제는 정수 Parsing에 집중. 부호, 공백, 로케일, API 계약은 필요에 따라 별도 정의

**예제 코드 — [18_expected_generic_parser.cpp](./examples/18_expected_generic_parser.cpp)**

```cpp
#include <charconv>
#include <concepts>
#include <expected>
#include <print>
#include <string_view>
#include <system_error>

template <std::integral T>
[[nodiscard]] std::expected<T, std::errc> parse_integer(std::string_view text) {
    T value{};
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    if (error != std::errc{}) return std::unexpected(error);
    if (end != text.data() + text.size()) return std::unexpected(std::errc::invalid_argument);
    return value;
}

int main() {
    const auto good = parse_integer<int>("2048");
    const auto bad = parse_integer<int>("10ms");
    if (good) std::println("Value: {}", *good);
    std::println("Invalid input: {}", !bad);
}
```

**실행 방법** — `Chapter-13/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror examples/18_expected_generic_parser.cpp -o example
./example
```


**실행 결과**

```text
Value: 2048
Invalid input: true
```

---

<a id="section-13-20"></a>

## 13.20. Mini Project — Generic Telemetry Pipeline

센서 데이터의 타입이 서로 달라도 공통 속성을 만족하면 같은 알고리즘으로 집계하는 프로젝트입니다. **ReadingLike Concept + Range 제약 + 테스트 가능한 템플릿 API**를 연결합니다.

```text
examples/19_telemetry_pipeline/
├── CMakeLists.txt
├── include/
│   └── telemetry/
│       └── pipeline.hpp
├── src/
│   ├── main.cpp
│   └── report.cpp
└── tests/
    └── test_pipeline.cpp
```

**핵심 설계**

- `ReadingLike`: 장치 이름, 값, 유효 상태에 대한 컴파일 시점 요구
- `summarize(R&&)`: `std::ranges::input_range`를 입력받고 정상 측정값만 집계
- `std::optional<Summary>`: 유효한 데이터가 없을 때 결과 없음 표현
- `report.cpp`: 출력 로직 분리. 템플릿 본문은 Header에 유지
- `test_pipeline.cpp`: 서로 다른 구조체 타입·빈 Range·잘못된 측정값 검증

**빌드 및 테스트** — `Chapter-13/` 경로에서 실행

```bash
cmake -S examples/19_telemetry_pipeline -B build/ch13 -DCMAKE_BUILD_TYPE=Release
cmake --build build/ch13 --parallel
ctest --test-dir build/ch13 --output-on-failure
./build/ch13/telemetry_demo
```

**예상 출력**

```text
Array average: 31.3
Valid: 3
Min: 28.0, max: 34.0, avg: 31.3
```

프로젝트 소스: [CMakeLists.txt](./examples/19_telemetry_pipeline/CMakeLists.txt), [pipeline.hpp](./examples/19_telemetry_pipeline/include/telemetry/pipeline.hpp), [report.cpp](./examples/19_telemetry_pipeline/src/report.cpp), [main.cpp](./examples/19_telemetry_pipeline/src/main.cpp), [test_pipeline.cpp](./examples/19_telemetry_pipeline/tests/test_pipeline.cpp).

**주의:** 이 예제는 정상적이고 유한한 소규모 센서값을 가정합니다. 긴 시간 누적되는 데이터에서는 합계의 수치 안정성, 단위, 타임스탬프, 장애 데이터 정책 등을 별도로 설계해야 합니다.

---

<a id="section-13-21"></a>

## 13.21. 설계 시 참고 사항

템플릿은 코드 재사용뿐 아니라 인터페이스의 계약을 컴파일 시점에 표현하는 도구입니다. 하지만 복잡한 템플릿은 진단 메시지, 바이너리 크기, 빌드 시간과 유지보수에 비용을 발생시킬 수 있습니다.

| 고려 항목 | 선택 기준 |
|---|---|
| 일반 함수 vs Template | 타입이 하나로 고정되면 일반 함수 우선 |
| 표준 Concept vs 사용자 정의 Concept | 의미가 같은 표준 Concept을 우선 검토 |
| Compile-Time vs Runtime | 실행 중 바뀌는 조건은 런타임 검증 필요 |
| 타입별 Overload vs Specialization | 적은 수의 타입별 동작은 오버로드가 단순할 수 있음 |
| Range 입력 | 필요한 최소 Range Category만 요구 |
| View 반환 | 원본 Lifetime과 Invalidation 고려 |
| Header와 구현 분리 | 템플릿 정의가 Instantiation 지점에서 보이도록 관리 |
| 진단과 테스트 | `static_assert`, 컴파일 실패 테스트, 경계값 테스트 활용 |

**Template Definition Visibility:** 일반적인 함수 템플릿의 정의는 사용 위치에서 보여야 합니다. 보통 Header 또는 Header가 포함하는 구현 파일에 정의합니다. 명시적 인스턴스화(Explicit Instantiation)를 사용하는 경우에는 `.cpp`에 분리할 수 있지만 허용할 타입 조합을 관리해야 합니다.

**라이브러리 설계:** Concepts와 Constraints는 템플릿 사용의 진단을 개선할 수 있지만, 필요하지 않은 타입 제한을 추가하면 오히려 재사용성을 떨어뜨립니다. C++ Core Guidelines와 코드베이스의 규칙을 참고해 요구 수준을 선택합니다.

**최신 흐름:** 2026년 11월 기준 C++23은 출판된 최신 ISO 표준이며 C++26은 표준화 작업 중입니다. C++26에서 논의·채택되는 새 기능은 이 장의 기본 실행 코드에 섞지 않고, 사용 도구의 지원 여부가 확인되면 별도로 학습하는 것이 좋습니다.

---

<a id="section-13-22"></a>

## 13.22. Coding Practice

연습문제는 **요구사항 확인 → 직접 코드 작성 → 컴파일·실행 → 정답 비교** 순서로 진행합니다. `exercises/`는 미완성 코드이고, `solutions/`에 모범답안이 있습니다. 문제별 정답은 별도 링크에서 확인합니다.

### 실습 ① — Generic Range Average

**문제:** Range의 평균을 계산하는 템플릿 함수를 구현합니다.

- `std::ranges::input_range` 적용
- `double` 변환 가능한 입력으로 제한
- 빈 Range이면 `std::nullopt` 반환
- 정수와 실수 Container 모두 처리

**시작 코드:** [01_range_average.cpp](./exercises/01_range_average.cpp) · **정답:** [01_range_average.cpp](./solutions/01_range_average.cpp)

### 실습 ② — Fixed Capacity Queue

**문제:** `T`와 `Capacity`를 템플릿 인수로 받는 고정 크기 FIFO Queue를 구현합니다.

- 정원 초과 시 `push()`는 `false` 반환
- 요소가 없을 때 `pop()`은 `false` 반환
- 제거 후 다시 삽입해도 입력 순서를 유지하는 순환 인덱스 구현
- `Capacity > 0` 컴파일 시점 검증

**시작 코드:** [02_fixed_capacity_queue.cpp](./exercises/02_fixed_capacity_queue.cpp) · **정답:** [02_fixed_capacity_queue.cpp](./solutions/02_fixed_capacity_queue.cpp)

### 실습 ③ — Device Filter & Projection

**문제:** 장치 우선순위에 따라 정렬하고, 일정 우선순위 이상만 별도 Container에 저장합니다.

- `std::ranges::sort`와 Projection 사용
- `std::views::filter`로 우선순위 3 이상 추출
- `std::ranges::to<std::vector>()`로 결과 생성
- 원본은 정렬되지만 필터 결과는 독립된 `vector`

**시작 코드:** [03_filter_devices.cpp](./exercises/03_filter_devices.cpp) · **정답:** [03_filter_devices.cpp](./solutions/03_filter_devices.cpp)

### 실습 ④ — Strict Numeric Parser

**문제:** 정수 타입을 템플릿 매개변수로 받는 Parser를 구현합니다.

- `std::integral`을 이용한 타입 제한
- `std::from_chars`로 문자열을 정수로 변환
- 일부만 읽힌 문자열을 실패 처리
- 값 범위 초과 및 형식 오류 구분

**시작 코드:** [04_strict_numeric_parser.cpp](./exercises/04_strict_numeric_parser.cpp) · **정답:** [04_strict_numeric_parser.cpp](./solutions/04_strict_numeric_parser.cpp)

### 컴파일 및 실행

```bash
# Chapter-13/ 경로 기준
# 연습문제 ①

g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror \
  exercises/01_range_average.cpp -o average
./average

# 정답 확인
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror \
  solutions/01_range_average.cpp -o average_solution
./average_solution
```

MSVC에서는 설치된 컴파일러에 따라 `/std:c++23` 또는 `/std:c++23preview`를 선택합니다. 특정 C++23 표준 라이브러리의 지원 범위는 별도 확인이 필요합니다.

---

<a id="section-13-23"></a>

## 13.23. Quiz & Summary

### Quiz

**1.** Function Template와 일반 함수의 중요한 차이점은 무엇인가요?

<details>
<summary>정답 확인</summary>

Function Template는 자료형 등의 템플릿 인수에 따라 함수를 Instantiation할 수 있으며, 일반 함수는 구체적인 매개변수 타입과 구현을 가짐.

</details>

**2.** `std::integral<T>`가 충족된다고 해서 정수 오버플로까지 방지되나요?

<details>
<summary>정답 확인</summary>

아니요. Concept은 타입의 성질을 검사하며 실제 값의 범위 검증은 별도로 필요함.

</details>

**3.** `std::vector<int>`와 `std::vector<double>`은 같은 타입인가요?

<details>
<summary>정답 확인</summary>

아니요. 같은 Class Template의 서로 다른 Instantiation으로 만들어진 별개 타입임.

</details>

**4.** `if constexpr`를 사용하는 목적은 무엇인가요?

<details>
<summary>정답 확인</summary>

컴파일 시점 조건에 따라 템플릿의 타입별 분기를 구성하고 선택되지 않은 분기의 코드가 해당 Instantiation에서 사용되지 않도록 함.

</details>

**5.** `std::forward<T>(value)`를 사용할 때 주의할 점은 무엇인가요?

<details>
<summary>정답 확인</summary>

Forwarding Reference와 타입 추론 맥락에서 값 범주를 보존할 때 사용하며, 무조건적인 Move 대체 수단이 아님.

</details>

**6.** `std::views::filter`와 `std::ranges::to<std::vector>()`의 핵심 차이는 무엇인가요?

<details>
<summary>정답 확인</summary>

`filter`는 지연 평가되는 View를 만들고, `ranges::to`는 결과 Container를 실제로 생성함.

</details>

**7.** `std::ranges::sort`에서 Projection은 어떤 역할을 하나요?

<details>
<summary>정답 확인</summary>

구조체 등에서 비교에 사용할 값을 추출하여 Comparator가 해당 값을 기준으로 순서를 결정하도록 함.

</details>

**8.** `std::enable_if`와 `requires`를 모두 알아야 하는 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

기존 Template 코드에는 SFINAE 형태가 존재하며, 새 코드에서는 Concepts와 Constraints로 의도를 더 명확하게 표현할 수 있기 때문임.

</details>

**9.** 함수 템플릿의 정의를 보통 Header에 작성하는 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

대부분의 경우 사용 지점에서 템플릿 정의를 확인할 수 있어야 원하는 타입으로 Instantiation할 수 있기 때문임.

</details>

**10.** Explicit Object Parameter는 C++의 어느 표준부터 제공하나요?

<details>
<summary>정답 확인</summary>

C++23. 컴파일러의 기능 지원 여부는 별도로 확인 필요.

</details>

### Summary

- **Template:** 여러 자료형이나 상수 인수에 대해 재사용 가능한 코드 정의
- **Concept / Constraint:** 템플릿 사용에 필요한 컴파일 시점 계약 명시
- **Requires Expression:** 타입의 멤버·연산·반환값 요구 검증
- **NTTP:** 컴파일 시점 상수를 템플릿 인수로 전달
- **CTAD:** 생성자 인수를 이용한 클래스 템플릿 타입 추론
- **Variadic Template / Fold Expression:** 여러 템플릿 인수에 동일 연산 적용
- **Generic Lambda / `if constexpr`:** 간결한 Generic 코드와 타입별 분기
- **Perfect Forwarding:** 호출자의 Value Category 유지
- **Ranges & Views:** Container에 독립적인 범위 기반 처리
- **`std::ranges::to`:** C++23 결과 Container 생성
- **SFINAE:** 기존 Template 코드를 읽기 위한 핵심 개념
- **Explicit Object Parameter:** C++23의 명시적 객체 매개변수
- **Template Definition Visibility:** Instantiation 시점에 정의 가시성 확보

### References

- [ISO/IEC 14882:2024 — C++23](https://www.iso.org/standard/83626.html)
- [WG21 — C++ Standards Committee](https://www.open-std.org/jtc1/sc22/wg21/)
- [C++ Core Guidelines — Templates and Generic Programming](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#t-templates-and-generic-programming)
- [Google C++ Style Guide — Concepts and Constraints](https://google.github.io/styleguide/cppguide.html#Concepts_and_Constraints)
- [cppreference — Concepts](https://en.cppreference.com/w/cpp/language/constraints)
- [cppreference — C++23 Compiler Support](https://en.cppreference.com/w/cpp/compiler_support/23)
- [cppreference — `std::ranges::to`](https://en.cppreference.com/w/cpp/ranges/to)
- [cppreference — Explicit Object Parameter](https://en.cppreference.com/w/cpp/language/member_functions#Explicit_object_member_functions)

---

[← C++ 목차](../README.md) · [Chapter 12 — Modern C++ & Resource Management](../Chapter-12/)
