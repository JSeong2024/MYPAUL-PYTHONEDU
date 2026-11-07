# Chapter 13. Templates & Generic Programming

C++23의 Function Template, Class Template, Concepts, Constraints, Ranges, Generic Algorithm과 Perfect Forwarding을 다룹니다. Chapter 10의 표준 라이브러리와 Chapter 12의 Move Semantics 및 객체 수명 개념을 확장하여, **표준 기능을 활용하고 다양한 자료형에 적용할 수 있는 코드의 타입 계약을 명확하게 설계하는 방법**을 학습합니다.

본 자료는 **C++23(ISO/IEC 14882:2024)** 을 기준으로 작성되었습니다. 일부 예제는 `<print>`, `<expected>`, `std::ranges::to` 및 Explicit Object Parameter를 사용하므로 해당 기능을 지원하는 컴파일러와 표준 라이브러리가 필요합니다. GCC 14 이상 환경을 권장하며, 기능별 지원 여부는 별도로 확인해야 합니다.

**선행 학습:** [Chapter 05 — Functions](../Chapter-05/) · [Chapter 08 — Structs & Classes](../Chapter-08/) · [Chapter 10 — Standard Library (STL)](../Chapter-10/) · [Chapter 12 — Modern C++ & Resource Management](../Chapter-12/)

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [13.1](#section-13-1) | Templates와 Generic Programming |
| [13.2](#section-13-2) | Function Template와 타입 추론 |
| [13.3](#section-13-3) | 표준 Concept와 Constraint |
| [13.4](#section-13-4) | Requires Expression과 사용자 정의 Concept |
| [13.5](#section-13-5) | Generic Function과 처리 규칙 |
| [13.6](#section-13-6) | Class Template와 타입 안전성 |
| [13.7](#section-13-7) | Non-Type Template Parameter |
| [13.8](#section-13-8) | Class Template Argument Deduction (CTAD) |
| [13.9](#section-13-9) | Variadic Template와 Fold Expression |
| [13.10](#section-13-10) | Type Traits와 Template Specialization |
| [13.11](#section-13-11) | SFINAE와 기존 템플릿 코드 |
| [13.12](#section-13-12) | `if constexpr`와 Compile-Time 분기 |
| [13.13](#section-13-13) | Generic Lambda와 표준 Algorithm |
| [13.14](#section-13-14) | Ranges, Views와 결과 Container |
| [13.15](#section-13-15) | Projection과 정렬 Customization |
| [13.16](#section-13-16) | Perfect Forwarding과 API 설계 |
| [13.17](#section-13-17) | `std::expected`와 Generic Error Handling |
| [13.18](#section-13-18) | C++23 Explicit Object Parameter |
| [13.19](#section-13-19) | Mini Project — Generic Telemetry Pipeline |
| [13.20](#section-13-20) | 설계 시 참고 사항 |
| [13.21](#section-13-21) | Coding Practice |
| [13.22](#section-13-22) | Quiz & Summary |

---

<a id="section-13-1"></a>
## 13.1. Templates와 Generic Programming

템플릿(Template)은 자료형이나 컴파일 시점 상수를 매개변수로 받아, 서로 다른 타입에 적용할 함수를 만들거나 클래스를 정의하는 기능입니다. 제네릭 프로그래밍(Generic Programming)은 특정 타입 이름보다 **필요한 연산과 타입의 계약**을 중심으로 코드를 설계하는 접근입니다.

템플릿을 직접 작성하는 목적은 기존 표준 기능을 다시 구현하는 것이 아닙니다. **서로 다른 타입에서 동일하게 적용할 프로젝트 고유의 규칙이 존재할 때** 특히 가치가 있습니다.

| 요구사항 | 권장 출발점 | 직접 템플릿이 필요한 경우 |
|---|---|---|
| 두 값 중 최댓값 | `std::max` | 별도의 규칙·반환 계약이 필요할 때 |
| 여러 값에서 최댓값 탐색 | `std::ranges::max` / `max_element` | 도메인 제약 및 결과 변환이 필요할 때 |
| 요소 정렬 | `std::ranges::sort` + Comparator / Projection | 표준 정렬과 다른 알고리즘 계약일 때 |
| 고정 크기 배열 | `std::array<T, N>` | 단위·불변식·특수 API를 추가해야 할 때 |
| 동적 시퀀스 | `std::vector<T>` | 저장소 정책 자체가 달라야 할 때 |
| 필터·변환 | `std::views::filter` / `transform` | 여러 처리 단계를 공통 정책으로 묶어야 할 때 |
| 성공 또는 오류 반환 | `std::expected<T, E>` | 애플리케이션 고유의 검증·오류 규칙이 필요할 때 |

새 함수나 클래스를 작성하기 전에 표준 알고리즘 및 Container로 해결할 수 있는지 확인합니다. 입력 타입이 하나로 고정되어 있다면 일반 함수부터 고려하고, 여러 타입에 공통으로 적용할 **별도의 검증·처리 규칙**이 있을 때 템플릿을 검토합니다.

`max_value<T>`는 템플릿 문법을 보여주기에는 적절하지만, 최댓값을 구하는 기능은 `std::max()`를 먼저 사용합니다. 가장 큰 값의 위치까지 필요하면 `std::ranges::max_element()`를 선택합니다.

**예제 코드 — [01_standard_first.cpp](./examples/01_standard_first.cpp)**

동일한 목적의 알고리즘을 새로 구현하지 않고 표준 라이브러리로 처리합니다.

```cpp
#include <algorithm>
#include <array>
#include <print>

int main() {
    std::println("Max: {}", std::max(12, 19));
    std::println("Max double: {}", std::max(1.5, 2.75));
    std::println("Explicit type: {}", std::max<double>(1, 2.5));

    const std::array readings{18, 26, 21, 32, 24};
    const auto highest = std::ranges::max_element(readings);
    std::println("Highest reading: {}", *highest);
}
```

**실행 결과**

```text
Max: 19
Max double: 2.75
Explicit type: 2.5
Highest reading: 32
```

두 값을 비교하는 사용자 정의 템플릿은 문법 학습에 유용하지만, 일반적인 최댓값 계산에는 `std::max`가 더 간결합니다. `max_element`는 가장 큰 원소의 위치(Iterator)도 제공합니다.

- `std::max(1, 2.0)`은 서로 다른 타입에서 `T`를 하나로 추론할 수 없어 컴파일되지 않습니다. `std::max<double>(1, 2.0)`처럼 명시할 수 있으나 형변환 정책을 확인해야 합니다.
- Iterator를 반환하는 `max_element()` 결과는 빈 Range에서 끝 Iterator가 됩니다. 사용 전 데이터 유무를 확인해야 합니다.

---

<a id="section-13-2"></a>
## 13.2. Function Template와 타입 추론

함수 템플릿(Function Template)은 자료형을 매개변수로 받아 여러 타입에서 같은 구현을 사용할 수 있도록 합니다. 호출하면 컴파일러가 인수로부터 템플릿 인수를 **추론(Template Argument Deduction)** 하거나 사용자가 명시적으로 지정합니다. 필요한 구체적 구현을 만드는 과정을 **Instantiation**이라고 합니다.

```cpp
// 문법 이해를 위한 최소 형태. 최댓값 기능은 std::max 사용 권장.
template <typename T>
T max_value(T a, T b) { return a < b ? b : a; }

// max_value(12, 19);          // T = int
// max_value<double>(1, 2.5); // T = double
// max_value(1, 2.5);         // T의 추론 충돌
```

위 `max_value()`는 구조를 이해하기 위한 문법 예제입니다. 실제 예제 파일에서는 **측정 허용 오차**를 검사하는 함수로 타입 추론과 제약 조건을 확인합니다.

- `template <typename T>`: 타입 매개변수 선언
- `std::floating_point<T>`: 실수 타입만 허용하는 표준 Concept
- `constexpr`: 조건을 만족할 때 컴파일 타임 계산 가능
- `[[nodiscard]]`: 반환값을 버리는 호출에 대한 경고 권장
- 실수 비교: NaN, Infinity, 허용 오차 정책 및 단위가 중요한 시스템에서는 별도 검토 필요

**예제 코드 — [02_template_deduction.cpp](./examples/02_template_deduction.cpp)**

온도·압력처럼 동일한 비교 규칙을 적용하지만 자료형이 다른 측정값을 처리합니다.

```cpp
#include <concepts>
#include <print>

// 프로젝트의 측정 규칙: 두 실수 측정값 사이의 오차가 허용 범위 이내인가?
template <std::floating_point T>
[[nodiscard]] constexpr bool within_tolerance(T actual, T target, T tolerance) {
    return tolerance >= T{0} &&
           actual >= target - tolerance && actual <= target + tolerance;
}

static_assert(within_tolerance(10.1, 10.0, 0.2));
static_assert(!within_tolerance(10.5, 10.0, 0.2));

int main() {
    std::println("Temperature OK: {}", within_tolerance(24.7, 25.0, 0.5));
    std::println("Pressure OK: {}", within_tolerance<float>(1.02f, 1.0f, 0.05f));
    // within_tolerance(1.0, 1.0f, 0.1); // T 추론 불일치
}
```

**실행 결과**

```text
Temperature OK: true
Pressure OK: true
```

동일한 오차 검증 규칙을 여러 부동소수점 타입에 적용합니다. 단위와 요구 정확도가 중요한 프로젝트에서는 별도 타입이나 정책으로 관리할 수 있습니다.

**주의:** 이 예제의 오차 검사는 기본적인 절대 허용 오차 검사입니다. 부동소수점 정밀도, 상대 오차, 특수값 정책이 필요한 라이브러리는 별도 명세가 필요합니다.

---

<a id="section-13-3"></a>
## 13.3. 표준 Concept와 Constraint

**Concept**은 템플릿이 사용할 수 있는 타입의 조건을 명시하며, **Constraint**는 해당 조건으로 함수나 타입을 제한합니다. `requires`는 연산이나 반환형이 유효한지 확인하는 구문으로 사용합니다. C++20부터 제공되는 기능입니다.

| 도구 | 의미 | 예시 |
|---|---|---|
| `std::integral<T>` | 정수 타입 | 정수용 파서 |
| `std::floating_point<T>` | 부동소수점 타입 | 측정 오차 계산 |
| `std::same_as<T, U>` | 정확하게 같은 타입 | 타입 정책 검증 |
| `std::convertible_to<T, U>` | 변환 가능한 타입 | 장치 API 결과 변환 |
| `requires(const T& x)` | 요구 연산이 가능한지 검사 | `x.name()` 호출 가능 여부 |
| `static_assert` | 컴파일 시점 조건 검증 | 잘못된 API 사용 조기 발견 |

Concept은 구문·타입의 성질을 제한하지만, **실제 반환 객체의 Lifetime**, 값의 범위, 측정 단위, 비즈니스 규칙까지 자동으로 검증하지는 않습니다. 예를 들어 `name()`이 `std::string_view`로 변환 가능하더라도, 반환된 View가 유효한 메모리를 참조한다는 보장은 별도로 필요합니다.

`std::integral<T>`이나 `std::floating_point<T>`처럼 이미 제공되는 표준 Concept을 우선 검토합니다. 사용자 정의 Concept은 장치 SDK처럼 공통 멤버 함수나 반환형을 요구할 때 사용합니다.

---

<a id="section-13-4"></a>
## 13.4. Requires Expression과 사용자 정의 Concept

요구식(Requires Expression)은 특정 타입에서 **멤버 함수 호출이나 연산이 유효한지**를 컴파일 시점에 검사합니다. `{ expression } -> Concept;` 형태로 반환값의 제약도 지정할 수 있습니다. 아래 예제는 장치 타입에 `name()`이 있고 반환값이 `std::string_view`로 변환되는지만 확인합니다.

**예제 코드 — [03_concepts_and_requires.cpp](./examples/03_concepts_and_requires.cpp)**

서로 다른 장치 타입이 `name()`을 제공하는지 컴파일 시점에 검사합니다.

```cpp
#include <concepts>
#include <print>
#include <string>
#include <string_view>

// name()의 반환값이 string_view로 바뀔 수 있는 장치만 허용.
template <typename T>
concept NamedDevice = requires(const T& device) {
    { device.name() } -> std::convertible_to<std::string_view>;
};

struct Motor {
    std::string label{"motor-A"};
    [[nodiscard]] std::string_view name() const noexcept { return label; }
};
struct AnonymousDevice { int id{1}; };

static_assert(NamedDevice<Motor>);
static_assert(!NamedDevice<AnonymousDevice>);

template <NamedDevice T>
void print_device(const T& device) {
    std::println("Device: {}", device.name());
}

int main() {
    print_device(Motor{});
    // print_device(AnonymousDevice{}); // 제약 조건 불충족
}
```

**실행 결과**

```text
Device: motor-A
```

SDK마다 타입 이름이 다르더라도 같은 사용 계약을 가진 장치를 다룰 수 있습니다. 사용자 정의 Concept은 표준 Concept만으로 요구사항을 충분히 표현하기 어려울 때 작성합니다.

`print_device(AnonymousDevice{})`처럼 조건을 만족하지 않는 타입을 전달하면 해당 함수 템플릿이 호출 후보에서 제외됩니다. 호출 가능한 다른 함수가 없다면 컴파일 오류가 발생하며, 진단 메시지는 컴파일러에 따라 다릅니다.

---

<a id="section-13-5"></a>
## 13.5. Generic Function과 처리 규칙

범용 함수가 실질적으로 필요한 대표 사례는 **여러 제품·장치 타입에 동일한 처리 규칙을 적용하는 경우**입니다. 예를 들어 온도 센서와 압력 센서가 서로 다른 구조체를 사용하더라도 `value()`와 `valid()`를 제공하면 경보 여부를 동일한 함수에서 검사할 수 있습니다.

필요한 제약을 **최소한으로** 설정합니다. 값과 유효 상태만 읽는 함수에 불필요하게 복사 가능성, 정렬 가능성, 기본 생성 가능성을 요구할 이유는 없습니다. 값의 단위와 허용 임계값은 호출자가 올바르게 지정해야 합니다.

**예제 코드 — [04_alert_policy.cpp](./examples/04_alert_policy.cpp)**

`NumericReading` Concept을 통해 공통 측정 인터페이스만 요구합니다.

```cpp
#include <concepts>
#include <print>

// 조직 내 여러 장치가 같은 value()/valid() 계약을 제공한다고 가정.
template <typename T>
concept NumericReading = requires(const T& item) {
    { item.value() } -> std::convertible_to<double>;
    { item.valid() } -> std::convertible_to<bool>;
};

struct Temperature {
    double celsius;
    bool ok;
    [[nodiscard]] double value() const noexcept { return celsius; }
    [[nodiscard]] bool valid() const noexcept { return ok; }
};
struct Pressure {
    float kpa;
    bool ok;
    [[nodiscard]] float value() const noexcept { return kpa; }
    [[nodiscard]] bool valid() const noexcept { return ok; }
};

template <NumericReading T>
[[nodiscard]] bool exceeds(const T& reading, double threshold) {
    return reading.valid() && static_cast<double>(reading.value()) > threshold;
}

int main() {
    std::println("Temperature alarm: {}", exceeds(Temperature{32.1, true}, 30.0));
    std::println("Pressure alarm: {}", exceeds(Pressure{118.0f, false}, 100.0));
}
```

**실행 결과**

```text
Temperature alarm: true
Pressure alarm: false
```

이 예제에는 표준 `std::max`만으로 표현할 수 없는 **경보 판정 규칙**이 있습니다. 서로 다른 센서 타입에 동일한 규칙을 적용하므로 템플릿을 사용할 이유가 분명합니다.

서로 다른 단위를 섞지 않도록 실제 서비스에서는 강한 타입(Strong Type)이나 단위 시스템을 적용할 수 있습니다. 별개 타입을 모두 억지로 하나의 Template에 묶기보다 일반 오버로드가 더 읽기 쉬울 때도 있습니다.

---

<a id="section-13-6"></a>
## 13.6. Class Template와 타입 안전성

클래스 템플릿(Class Template)은 자료형을 매개변수로 받는 클래스입니다. 표준 라이브러리의 `std::vector<T>`, `std::optional<T>`, `std::array<T, N>`가 대표적인 예입니다.

사용자 정의 클래스 템플릿은 수치가 같더라도 서로 다른 측정 단위가 섞이지 않도록 하거나, 특정 API의 불변식(Invariant)을 타입 수준에서 표현할 때 유용합니다.

`Quantity<CelsiusTag, double>`과 `Quantity<KilopascalTag, double>`은 서로 다른 타입입니다. 동일한 구현을 공유하면서도 잘못된 단위 간 연산을 컴파일 시점에 막는 기법입니다. 단, 아래 예제의 `Celsius` 덧셈은 교육용입니다. 실제 물리량 시스템에서는 절대온도와 온도차를 분리해야 합니다.

**예제 코드 — [05_class_templates.cpp](./examples/05_class_templates.cpp)**

측정 단위를 Tag 타입으로 표현합니다.

```cpp
#include <concepts>
#include <print>

// 센서값이 같은 숫자여도 단위가 다르면 서로 다른 타입으로 구분.
struct CelsiusTag {};
struct KilopascalTag {};

template <typename Tag, std::floating_point T>
class Quantity {
public:
    explicit constexpr Quantity(T value) noexcept : value_(value) {}
    [[nodiscard]] constexpr T value() const noexcept { return value_; }
    [[nodiscard]] constexpr Quantity operator+(Quantity other) const noexcept {
        return Quantity{value_ + other.value_};
    }
private:
    T value_;
};

int main() {
    const Quantity<CelsiusTag, double> room{20.0};
    const Quantity<CelsiusTag, double> offset{1.5};
    const Quantity<KilopascalTag, double> pressure{101.3};
    std::println("Temperature: {} C", (room + offset).value());
    std::println("Pressure: {} kPa", pressure.value());
    // room + pressure; // 단위가 다른 타입은 더할 수 없음
}
```

**실행 결과**

```text
Temperature: 21.5 C
Pressure: 101.3 kPa
```

표준 `std::vector`를 재구현하는 것이 아니라, 서로 다른 측정 단위의 혼용을 방지하는 타입 계약을 정의합니다.

---

<a id="section-13-7"></a>
## 13.7. Non-Type Template Parameter

비타입 템플릿 매개변수(Non-Type Template Parameter, NTTP)는 `N`처럼 컴파일 시점에 결정할 수 있는 값을 템플릿 인수로 전달하는 방식입니다. `Window<T, N>`의 `N`은 객체 생성 전부터 고정 크기를 나타냅니다. 크기가 실행 중 바뀌어야 한다면 동적 Container를 고려합니다.

**예제 코드 — [06_nttp_ctad.cpp](./examples/06_nttp_ctad.cpp)**

고정 크기 윈도우와 표준 `std::pair`의 타입 추론을 확인합니다.

```cpp
#include <array>
#include <cstddef>
#include <print>
#include <string>
#include <type_traits>
#include <utility>

// 고정 데이터 윈도우: 측정값 N개를 배열로 보유.
template <typename T, std::size_t N>
struct Window {
    static_assert(N > 0);
    std::array<T, N> values{};
    [[nodiscard]] constexpr std::size_t size() const noexcept { return N; }
};

int main() {
    Window<int, 3> readings{{10, 20, 30}};
    std::pair device{std::string{"motor-A"}, 120}; // CTAD
    static_assert(std::is_same_v<decltype(device.second), int>);
    std::println("Window size: {}", readings.size());
    std::println("{}: {} RPM", device.first, device.second);
}
```

**실행 결과**

```text
Window size: 3
motor-A: 120 RPM
```

단순 고정 배열은 `std::array`로 충분합니다. 사용자 정의 `Window`는 별도의 윈도우 연산이나 정책을 추가할 필요가 있을 때 고려합니다.

---

<a id="section-13-8"></a>
## 13.8. Class Template Argument Deduction (CTAD)

클래스 템플릿 인수 추론(Class Template Argument Deduction, CTAD)은 생성자에 전달한 값을 바탕으로 타입 매개변수를 추론하는 기능입니다. C++17부터 제공되며, 타입을 반복해서 적지 않아도 됩니다.

```cpp
#include <string>
#include <type_traits>
#include <utility>

int main() {
    std::pair device{std::string{"motor-A"}, 120};
    static_assert(std::is_same_v<decltype(device.second), int>);
}
```

`device`의 타입은 컴파일 시점에 `std::pair<std::string, int>`로 결정됩니다. CTAD는 동적 타입 변경 기능이 아니며, 생성 인수에 따라 예상과 다른 타입이 추론될 수 있으므로 **단위·정밀도·소유권이 중요할 때는 명시적인 타입 지정**도 검토합니다.

전체 실행 예제는 [06_nttp_ctad.cpp](./examples/06_nttp_ctad.cpp)에서 확인할 수 있습니다.

---

<a id="section-13-9"></a>
## 13.9. Variadic Template와 Fold Expression

**Variadic Template**은 개수가 정해지지 않은 타입 인수를 처리합니다. **Fold Expression**은 인수 팩에 특정 연산을 적용합니다. 새로 구현하기 전에 `std::accumulate`, `std::ranges` 알고리즘 등 Container 입력에 맞는 표준 기능을 검토합니다.

```cpp
// (0.0 + ... + values)는 초기값을 포함한 Fold Expression.
// 인수가 하나도 없어도 0.0을 반환할 수 있음.
```

아래 함수는 별도 Container 없이 여러 인수를 직접 받는 API의 사용 형태를 보여줍니다. 단순 합계라면 표준 알고리즘이 더 적합할 수도 있습니다.

**예제 코드 — [07_variadic_fold.cpp](./examples/07_variadic_fold.cpp)**

서로 다른 숫자 인수를 `double`로 변환해 합산합니다.

```cpp
#include <concepts>
#include <print>

template <typename... T>
    requires (std::convertible_to<T, double> && ...)
[[nodiscard]] constexpr double sum_samples(T... values) {
    return (0.0 + ... + static_cast<double>(values));
}

int main() {
    std::println("Total: {}", sum_samples(3, 4.5, 2));
    std::println("Empty total: {}", sum_samples());
}
```

**실행 결과**

```text
Total: 9.5
Empty total: 0
```

임의 개수의 인수를 처리하는 문법을 보여주는 예제입니다. 여러 측정값을 전달할 때는 Container를 사용하면 요소 개수와 Lifetime을 더 명확하게 관리할 수 있습니다.

**주의:** 부동소수점 합계는 연산 순서에 따라 오차가 누적됩니다. 긴 데이터 스트림에서는 누적 정확도와 범위 검사 전략을 별도 검토합니다.

---

<a id="section-13-10"></a>
## 13.10. Type Traits와 Template Specialization

- `std::is_same_v<A, B>`: 타입 동일성 검사
- `std::remove_cvref_t<T>`: `const`, `volatile`, 참조 한정자 제거
- **Specialization:** 특정 타입에 대한 별도 정책이나 구현 정의
- **Rule:** 특정 타입 하나를 분기하는 데는 `if constexpr`나 Overload가 더 명료할 수 있음

기존의 `double`을 무조건 섭씨로 해석하는 방식은 부정확합니다. **타입의 물리적 의미를 나타내는 Tag**를 사용해야 올바른 단위를 결정할 수 있습니다.

**예제 코드 — [08_traits_specialization.cpp](./examples/08_traits_specialization.cpp)**

타입 Tag별 출력 단위를 Template Specialization으로 지정합니다.

```cpp
#include <concepts>
#include <print>
#include <string_view>
#include <type_traits>

struct TemperatureTag {};
struct PressureTag {};

// 도메인의 '단위 종류'를 타입으로 구분하고 문자열 정책을 제공.
template <typename Tag>
struct UnitLabel;

template <>
struct UnitLabel<TemperatureTag> {
    static constexpr std::string_view text = "C";
};
template <>
struct UnitLabel<PressureTag> {
    static constexpr std::string_view text = "kPa";
};

template <typename Tag, std::floating_point T>
void show_reading(T value) {
    static_assert(std::is_floating_point_v<T>);
    std::println("{} {}", value, UnitLabel<Tag>::text);
}

int main() {
    show_reading<TemperatureTag>(23.5);
    show_reading<PressureTag>(101.3);
}
```

**실행 결과**

```text
23.5 C
101.3 kPa
```

측정 단위를 별도의 타입 정책으로 구분합니다. 숫자 표현 타입(`double`) 자체가 측정 단위를 의미하지는 않습니다.

---

<a id="section-13-11"></a>
## 13.11. SFINAE와 기존 템플릿 코드

C++20 이전 라이브러리에서는 `std::enable_if`와 SFINAE(Substitution Failure Is Not An Error)를 이용해 템플릿 후보를 제약하는 방식이 많이 사용되었습니다. **기존 구현을 읽기 위해 이해할 가치는 있지만**, 새로 설계하는 C++20/23 API의 단순 타입 제약은 Concept으로 표현하는 것이 대체로 읽기 쉽습니다.

**예제 코드 — [15_legacy_constraints.cpp](./examples/15_legacy_constraints.cpp)**

같은 정수 제약을 레거시 SFINAE와 Modern Concept 방식으로 각각 작성합니다.

```cpp
#include <concepts>
#include <print>
#include <type_traits>

// 레거시 API의 SFINAE 제약 (읽기 위한 예시)
template <typename T, std::enable_if_t<std::is_integral_v<T>, int> = 0>
[[nodiscard]] constexpr bool old_is_even(T value) { return value % 2 == 0; }

// 신규 C++20+ API의 권장 표현
template <std::integral T>
[[nodiscard]] constexpr bool is_even(T value) { return value % 2 == 0; }

int main() {
    std::println("Legacy: {}", old_is_even(6));
    std::println("Modern: {}", is_even(7));
}
```

**실행 결과**

```text
Legacy: true
Modern: false
```

기존 SFINAE 기반 코드를 이해하고, 필요한 부분을 점진적으로 개선하는 데 활용합니다. 기존 코드를 무조건 일괄 교체할 필요는 없습니다.

---

<a id="section-13-12"></a>
## 13.12. `if constexpr`와 Compile-Time 분기

`if constexpr`는 조건이 컴파일 타임에 결정될 때, 템플릿의 타입별 동작을 선택합니다. 일반 `if`와 달리 선택되지 않은 분기의 코드는 해당 인스턴스에서 인스턴스화되지 않을 수 있습니다.

- 정수: 카운트 형식
- 실수: 소수점 두 자리 형식
- 텍스트: 문자열 형식

타입별 행동이 크게 달라진다면 하나의 Template에 모든 분기를 몰아넣기보다 **별도 함수 또는 Overload로 분리**하는 편이 나을 수 있습니다.

**예제 코드 — [09_if_constexpr.cpp](./examples/09_if_constexpr.cpp)**

값 종류에 따라 로그 출력 형식을 달리합니다.

```cpp
#include <concepts>
#include <print>
#include <string_view>

template <typename T>
void log_measurement(const T& value) {
    if constexpr (std::integral<T>) {
        std::println("Count: {}", value);
    } else if constexpr (std::floating_point<T>) {
        std::println("Measurement: {:.2f}", value);
    } else {
        std::println("Text: {}", std::string_view{value});
    }
}

int main() {
    log_measurement(7);
    log_measurement(23.456);
    log_measurement(std::string_view{"ready"});
}
```

**실행 결과**

```text
Count: 7
Measurement: 23.46
Text: ready
```

입력 타입에 따라 사용할 수 있는 표현식이나 처리 형식이 달라질 때 적합합니다. 모든 타입에 같은 동작을 적용한다면 `if constexpr`가 필요하지 않을 수 있습니다.

---

<a id="section-13-13"></a>
## 13.13. Generic Lambda와 표준 Algorithm

람다(Lambda)의 `auto` 매개변수는 여러 타입에 적용할 수 있는 Generic 호출 연산자를 만들어 줍니다. 짧은 범위의 알고리즘에 별도 템플릿 함수를 정의하지 않아도 되므로 간결합니다.

**예제 코드 — [10_generic_lambda.cpp](./examples/10_generic_lambda.cpp)**

`std::ranges::count_if`와 Lambda를 결합해 임계값 이상 항목 수를 계산합니다.

```cpp
#include <algorithm>
#include <array>
#include <print>

int main() {
    const std::array readings{14, 30, 27, 42};
    const int threshold{28};
    const auto count = std::ranges::count_if(readings, [threshold](const auto& value) {
        return value >= threshold;
    });
    std::println("Alerts: {}", count);
}
```

**실행 결과**

```text
Alerts: 2
```

단순한 개수 계산에는 별도의 반복문보다 표준 알고리즘을 우선 검토합니다. 참조 캡처를 사용할 때는 원본 객체의 Lifetime에 주의해야 합니다.

---

<a id="section-13-14"></a>
## 13.14. Ranges, Views와 결과 Container

- **Range:** 순회 가능한 데이터 구간
- **View:** 필요할 때 요소를 계산하는 지연 평가(Lazy Evaluation) 인터페이스
- **`std::views::filter`**: 조건을 충족한 요소만 통과시킴
- **`std::views::transform`**: 각 요소를 변환
- **`std::ranges::to<std::vector>()`**: C++23에서 결과를 소유하는 Container 생성

**Lifetime:** View는 원본을 참조하는 경우가 많으므로 원본이 살아 있고 Iterator 등이 유효한 동안 사용해야 합니다. View 자체가 항상 결과 데이터를 소유하는 것은 아닙니다.

`std::ranges::to` 지원 여부는 `__cpp_lib_ranges_to_container` 기능 검사 매크로로 확인합니다. 미지원 환경은 `std::ranges::copy` + `std::back_inserter`로 변환할 수 있습니다.

**예제 코드 — [11_ranges.cpp](./examples/11_ranges.cpp)**

센서값 필터링과 변환을 파이프라인으로 구성하고 독립된 `std::vector`로 저장합니다.

```cpp
#include <algorithm>
#include <array>
#include <iterator>
#include <print>
#include <ranges>
#include <vector>

int main() {
    const std::array readings{10, 25, 40, 15};
    auto selected = readings
        | std::views::filter([](int x) { return x >= 20; })
        | std::views::transform([](int x) { return x * 2; });

#ifdef __cpp_lib_ranges_to_container
    const auto output = selected | std::ranges::to<std::vector<int>>();
#else
    std::vector<int> output;
    std::ranges::copy(selected, std::back_inserter(output));
#endif
    std::println("Selected: {}", output.size());
    for (int x : output) std::println("{}", x);
}
```

**실행 결과**

```text
Selected: 2
50
80
```

데이터 필터링과 변환은 별도 함수 템플릿을 만들지 않고 표준 View로 표현할 수 있습니다. 결과를 `vector`로 생성하면 반환값이 원본 데이터의 Lifetime에 의존하지 않습니다.

---

<a id="section-13-15"></a>
## 13.15. Projection과 정렬 Customization

Projection은 정렬 대상 객체에서 **비교할 값**을 꺼내는 기능입니다. 모든 장치 타입에 무조건 `<` 연산자를 구현할 필요가 없습니다. `std::ranges::sort(devices, comparator, &Device::priority)` 형태로 명시할 수 있습니다.

Comparator는 **Strict Weak Ordering**을 만족해야 합니다. 정렬은 원본 Container의 순서를 바꾸므로 순서를 보존해야 한다면 복사본에 적용합니다.

**예제 코드 — [12_projection.cpp](./examples/12_projection.cpp)**

장치를 우선순위에 따라 내림차순 정렬합니다.

```cpp
#include <algorithm>
#include <print>
#include <string_view>
#include <vector>

struct Device {
    std::string_view id;
    int priority;
};

int main() {
    std::vector<Device> devices{{"motor", 2}, {"camera", 3}, {"radar", 1}};
    std::ranges::sort(devices, std::ranges::greater{}, &Device::priority);
    for (const auto& item : devices)
        std::println("{}: {}", item.id, item.priority);
}
```

**실행 결과**

```text
camera: 3
motor: 2
radar: 1
```

특정 멤버를 기준으로 한 번 정렬하기 위해 객체 전체의 `operator<`를 정의할 필요는 없습니다. 표준 Projection을 활용하는 편이 간단합니다.

---

<a id="section-13-16"></a>
## 13.16. Perfect Forwarding과 API 설계

**Perfect Forwarding**은 인수의 Value Category를 가능한 한 그대로 다른 호출 대상에 전달하는 기법입니다. `T&&` 형태의 **Forwarding Reference**와 `std::forward<T>(value)`를 사용합니다.

일반적으로 `std::vector::emplace_back`, `std::make_unique` 같은 표준 API가 이미 인수를 전달하므로 래퍼 함수를 굳이 만들 필요는 없습니다. **검증·관찰·도메인 정책 등 기존 API에 없는 동작**을 제공할 때 래퍼가 가치가 있습니다.

`std::move`는 항상 값을 이동시키는 명령이 아니며, `std::forward`는 단순한 `std::move`의 대체 수단이 아닙니다. Forwarding Reference와 Template 인수 추론 규칙이 전제됩니다.

**예제 코드 — [13_forwarding.cpp](./examples/13_forwarding.cpp)**

애플리케이션에 이벤트 저장소 API를 제공하며, 실제 객체 생성은 `std::vector::emplace_back`에 맡깁니다.

```cpp
#include <concepts>
#include <print>
#include <string>
#include <utility>
#include <vector>

struct Event {
    std::string source;
    int code;
    Event(std::string src, int value) : source(std::move(src)), code(value) {}
};

class EventBuffer {
public:
    template <typename... Args>
        requires std::constructible_from<Event, Args...>
    Event& append(Args&&... args) {
        // 검증 정책이 있는 저장 API를 제공; 생성은 vector::emplace_back에 위임.
        return events_.emplace_back(std::forward<Args>(args)...);
    }
    [[nodiscard]] const std::vector<Event>& events() const noexcept { return events_; }
private:
    std::vector<Event> events_;
};

int main() {
    EventBuffer buffer;
    std::string device{"sensor-A"};
    buffer.append(device, 200);     // 문자열 복사
    buffer.append("camera-B", 201); // 임시 문자열 생성
    std::println("Events: {}", buffer.events().size());
    std::println("First source: {}", buffer.events().front().source);
}
```

**실행 결과**

```text
Events: 2
First source: sensor-A
```

이 예제는 저장소 인터페이스를 확장하는 방법을 설명합니다. 단순한 `emplace_back` 호출을 위해 반드시 새 추상화를 만들어야 한다는 뜻은 아닙니다.

`append()`에 큐 크기 제한, 타임스탬프 부여, 메트릭 기록 같은 도메인 규칙이 생길 때 클래스의 가치가 분명해집니다.

---

<a id="section-13-17"></a>
## 13.17. `std::expected`와 Generic Error Handling

C++23의 `std::expected<T, E>`는 성공값 또는 오류값을 반환합니다. `std::from_chars`는 C 스타일 예외 없는 숫자 Parsing API로, 변환 종료 위치와 오류 코드를 함께 제공합니다.

이 예제는 실제 애플리케이션에 필요한 **입력 전체 소비 규칙**을 직접 정의합니다. `"10ms"`를 숫자 10으로 조용히 허용하지 않고 오류로 처리하는 것이 핵심입니다.

- `std::integral<T>`: 정수 타입에만 적용
- `!std::same_as<T, bool>`: `from_chars`가 지원하지 않는 `bool` 제외
- `std::unexpected(error)`: 오류 상태를 생성
- 성공 여부를 확인한 뒤 `.value()` 또는 역참조 사용
- `std::expected`가 모든 예외를 자동으로 오류 값으로 변환하는 것은 아님

**예제 코드 — [14_expected_parser.cpp](./examples/14_expected_parser.cpp)**

정수 Parsing 결과를 `std::expected<T, std::errc>`로 반환합니다.

```cpp
#include <charconv>
#include <concepts>
#include <expected>
#include <print>
#include <string_view>
#include <system_error>

template <std::integral T>
    requires (!std::same_as<T, bool>)
[[nodiscard]] std::expected<T, std::errc> parse_number(std::string_view text) {
    T result{};
    const auto [end, ec] = std::from_chars(text.data(), text.data() + text.size(), result);
    if (ec != std::errc{}) return std::unexpected(ec);
    if (end != text.data() + text.size())
        return std::unexpected(std::errc::invalid_argument);
    return result;
}

int main() {
    const auto ok = parse_number<int>("2048");
    const auto bad = parse_number<int>("10ms");
    std::println("Parsed: {}", ok.value());
    std::println("Rejected suffix: {}", !bad);
}
```

**실행 결과**

```text
Parsed: 2048
Rejected suffix: true
```

입력 전체를 소비해야 한다는 검증 규칙과 오류 반환 계약이 있으므로 범용 Parser를 별도로 정의할 이유가 있습니다.

---

<a id="section-13-18"></a>
## 13.18. C++23 Explicit Object Parameter

C++23의 **Explicit Object Parameter(Deducing this)**는 멤버 함수에서 `this Self&& self` 형태로 객체를 명시적으로 받을 수 있게 합니다. `const`와 비-`const` 객체에 대해 비슷한 멤버 구현을 반복하지 않으려는 경우 유용합니다.

모든 컴파일러·표준 라이브러리에서 동일하게 지원되는 것은 아니므로, 프로젝트 도입 전에 **개별 언어 기능 지원**을 확인합니다. 단순 Getter에는 전통적인 `const`/비-`const` 오버로드가 더 명료할 수 있습니다.

**예제 코드 — [16_explicit_object.cpp](./examples/16_explicit_object.cpp)**

`Counter::get()`을 하나의 정의로 작성하고 반환값의 참조/Const 속성을 보존합니다.

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
    counter.get() = 9;
    const Counter immutable{4};
    std::println("Mutable: {}, const: {}", counter.get(), immutable.get());
}
```

**실행 결과**

```text
Mutable: 9, const: 4
```

Ref-Qualified 멤버 함수의 중복을 줄여야 할 때 유용합니다. 모든 Getter에 적용할 필요는 없습니다.

---

<a id="section-13-19"></a>
## 13.19. Mini Project — Generic Telemetry Pipeline

온도와 압력처럼 **서로 다른 구조체 타입이지만 동일한 데이터 읽기 계약을 제공하는 측정값**을 공통 알고리즘으로 집계합니다. 기존 STL을 활용하면서도 프로젝트 고유의 계약이 필요한 부분에만 사용자 정의 Template와 Concept을 사용합니다.

**구현 목표**

- `ReadingLike` Concept로 `value()`와 `valid()` API 요구
- `std::ranges::input_range`로 Container 종류에 대한 불필요한 제한 제거
- 실패·비정상 측정값은 집계에서 제외
- 유한한 값만 수집하고 최솟값, 최댓값, 평균, 개수 계산
- 유효한 값이 전혀 없으면 `std::nullopt` 반환
- 서로 다른 입력 타입과 경계 상황을 테스트

**프로젝트 구조**

```text
examples/17_telemetry_pipeline/
├── CMakeLists.txt
├── include/
│   └── telemetry/
│       ├── pipeline.hpp
│       └── report.hpp
├── src/
│   ├── main.cpp
│   └── report.cpp
└── tests/
    └── test_pipeline.cpp
```

| 구성 요소 | 목적 |
|---|---|
| [`pipeline.hpp`](./examples/17_telemetry_pipeline/include/telemetry/pipeline.hpp) | `ReadingLike` Concept, Generic 요약 함수 |
| [`report.hpp`](./examples/17_telemetry_pipeline/include/telemetry/report.hpp) | 출력 인터페이스 선언 |
| [`report.cpp`](./examples/17_telemetry_pipeline/src/report.cpp) | 출력 코드 구현 분리 |
| [`main.cpp`](./examples/17_telemetry_pipeline/src/main.cpp) | 온도/압력 입력 및 시연 |
| [`test_pipeline.cpp`](./examples/17_telemetry_pipeline/tests/test_pipeline.cpp) | 타입 계약, 빈 입력, 무효값, NaN 테스트 |
| [`CMakeLists.txt`](./examples/17_telemetry_pipeline/CMakeLists.txt) | C++23 빌드 및 CTest 정의 |

**핵심 코드 — [pipeline.hpp](./examples/17_telemetry_pipeline/include/telemetry/pipeline.hpp)**

집계 알고리즘은 `std::ranges::input_range`를 받고, 요소 타입이 `ReadingLike`를 만족해야 합니다. 별도 Container를 재구현하지 않고 `std::array`나 `std::vector` 입력을 그대로 처리합니다.

```cpp
#pragma once

#include <cmath>
#include <concepts>
#include <cstddef>
#include <optional>
#include <ranges>
#include <type_traits>

namespace telemetry {

template <typename T>
concept ReadingLike = requires(const T& r) {
    { r.value() } -> std::convertible_to<double>;
    { r.valid() } -> std::convertible_to<bool>;
};

struct Summary {
    std::size_t count{};
    double minimum{};
    double maximum{};
    double average{};
};

template <std::ranges::input_range R>
    requires ReadingLike<std::remove_cvref_t<std::ranges::range_reference_t<R>>>
[[nodiscard]] std::optional<Summary> summarize(R&& readings) {
    Summary result{};
    double sum{};

    for (const auto& reading : readings) {
        if (!reading.valid()) continue;
        const double value = static_cast<double>(reading.value());
        if (!std::isfinite(value)) continue;

        if (result.count == 0) {
            result.minimum = value;
            result.maximum = value;
        } else {
            if (value < result.minimum) result.minimum = value;
            if (value > result.maximum) result.maximum = value;
        }
        ++result.count;
        sum += value;
    }
    if (result.count == 0) return std::nullopt;
    result.average = sum / static_cast<double>(result.count);
    return result;
}

} // namespace telemetry
```

**빌드 및 테스트**

`Chapter-13/` 경로에서 실행합니다.

```bash
cmake -S examples/17_telemetry_pipeline -B build/ch13 -DCMAKE_BUILD_TYPE=Debug
cmake --build build/ch13 --parallel
ctest --test-dir build/ch13 --output-on-failure
./build/ch13/telemetry_demo
```

**실행 결과 (GCC 14.2)**

```text
Temperature: count=3, min=28.0, max=34.0, avg=31.3
Pressure: count=2, min=100.0, max=101.0, avg=100.5
```

**설계 검토:**

- 이 프로젝트는 유한한 소규모 측정값을 대상으로 합니다. 긴 기간 누적 데이터는 합계 오차, Overflow, Timestamp, 서로 다른 단위와 출처를 별도로 관리해야 합니다.
- 일반 `for` 루프로 집계하는 이유는 **한 번 순회하면서 개수·최댓값·최솟값·평균을 동시에 계산하기 때문**입니다. 범용 알고리즘을 위한 불필요한 파이프라인을 추가하지 않습니다.
- 실패한 값은 함수의 정의에 따라 제외합니다. 장치 상태를 감시하는 시스템에서는 *제외 건수*와 오류 유형을 별도로 기록할 수도 있습니다.
- Template 정의는 인스턴스화 시점에 보여야 하므로 `pipeline.hpp`에 두고, 비템플릿 출력 구현은 `report.cpp`에 분리했습니다.

---

<a id="section-13-20"></a>
## 13.20. 설계 시 참고 사항

제네릭 코드를 설계할 때는 표준 라이브러리와 일반 함수로 충분한지 먼저 확인합니다. 타입 제약은 필요한 만큼만 추가하고, 원본 객체의 Lifetime과 오류 처리 규칙도 함께 검토합니다.

| 질문 | 판단 기준 |
|---|---|
| 표준 기능으로 해결할 수 있는가? | `std::max`, `std::ranges`, `std::vector` 등부터 검토 |
| 일반 함수로 충분한가? | 처리 타입이 고정되어 있으면 Template 불필요 |
| 도메인 규칙이 있는가? | 단위·장치 인터페이스·검증 규칙을 타입으로 표현할 가치가 있는지 |
| Concept이 너무 강한가? | 필요한 최소 연산만 요구하는지 |
| 원본 수명이 유효한가? | View·Reference·Iterator의 Lifetime과 Invalidation 확인 |
| 런타임 검증도 있는가? | Concept은 데이터 범위·예외 상황까지 보장하지 않음 |
| 컴파일 비용이 적절한가? | 템플릿 중복 인스턴스화와 빌드 시간 고려 |
| 테스트할 수 있는가? | 일반 호출과 실패 입력, 다른 타입, 비어 있는 데이터 테스트 |

**피해야 할 패턴**

```cpp
// std::max 등 표준 기능을 이유 없이 다시 구현
// 단일 타입만 처리하는 함수에 불필요한 Template 추가
// 실제로 필요하지 않은 기본 생성·복사·정렬 제약 강제
// 원본 수명이 끝난 뒤 View나 Reference 사용
// 모든 입력 데이터가 올바르다고 Concept만으로 가정
```

Chapter 13은 **표준 라이브러리의 활용과 범용 API의 타입 계약**에 집중합니다. Concurrency는 Chapter 14, 성능 및 메모리 할당은 Chapter 15에서 확장합니다.

---

<a id="section-13-21"></a>
## 13.21. Coding Practice

연습문제는 `exercises/`의 미완성 코드를 수정하고 출력 결과를 확인하는 방식으로 진행합니다. 모범답안은 `solutions/`에 별도로 보관되어 있습니다.

**시작 코드는 컴파일 가능하지만, TODO를 완성하기 전에는 요구한 결과를 출력하지 않습니다.**

### 실습 ① — Reading Alert

측정값이 유효하고 임계값보다 클 때만 경보를 출력하는 일반 함수를 작성합니다.

- `bool valid`, `double value` 검증
- 왜 이 단계에는 템플릿이 필요 없는지 설명
- 정상 입력과 무효 입력 구분
- **시작 코드:** [01_reading_alert.cpp](./exercises/01_reading_alert.cpp) · **모범답안:** [01_reading_alert.cpp](./solutions/01_reading_alert.cpp)

**모범답안 실행 결과**

```text
High: true
Invalid: false
```

### 실습 ② — Strong Quantity

Class Template와 Tag 타입으로 서로 다른 물리량의 오용을 막습니다.

- `Quantity<Tag, T>` 구현
- 같은 타입끼리 `operator+` 허용
- 다른 Tag끼리 더하려 할 때 컴파일 실패 확인(주석 해제 시)
- **시작 코드:** [02_strong_quantity.cpp](./exercises/02_strong_quantity.cpp) · **모범답안:** [02_strong_quantity.cpp](./solutions/02_strong_quantity.cpp)

**모범답안 실행 결과**

```text
Temperature: 22.5
Pressure: 101.3
```

### 실습 ③ — Device Filter & Projection

표준 Generic Algorithm을 활용해 Priority 3 이상 장치를 추출합니다.

- `std::ranges::sort`와 멤버 Projection 사용
- `std::views::filter`로 우선순위 3 이상만 선택
- `std::ranges::to` 지원 시 `vector`로 변환, 미지원 시 `ranges::copy` 사용
- **시작 코드:** [03_filter_devices.cpp](./exercises/03_filter_devices.cpp) · **모범답안:** [03_filter_devices.cpp](./solutions/03_filter_devices.cpp)

**모범답안 실행 결과**

```text
Selected: 2
lidar: 4
camera: 3
```

### 실습 ④ — Strict Numeric Parser

프로젝트의 정수 입력 규칙을 `std::expected` 기반으로 구현합니다.

- 정수 타입만 허용하는 Concept
- `std::from_chars` 결과 및 전체 문자열 소비 검사
- 잘못된 입력의 `std::errc` 반환
- **시작 코드:** [04_strict_parser.cpp](./exercises/04_strict_parser.cpp) · **모범답안:** [04_strict_parser.cpp](./solutions/04_strict_parser.cpp)

**모범답안 실행 결과**

```text
Parsed: 2048
Rejected: true
```

### 컴파일 및 실행

```bash
# Chapter-13/ 기준. 실습 ①
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror \
  exercises/01_reading_alert.cpp -o reading_alert
./reading_alert

# 모범답안
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror \
  solutions/01_reading_alert.cpp -o reading_alert_solution
./reading_alert_solution
```

**Clang:** 사용 중인 표준 라이브러리가 `<print>`와 `<expected>`를 지원한다면 동일하게 `clang++ -std=c++23`으로 컴파일할 수 있습니다.

**MSVC:** Developer Command Prompt에서 설치 버전에 맞는 C++23 모드를 선택합니다. 언어 모드와 라이브러리 기능 지원 수준이 다를 수 있으므로 개별 기능을 확인해야 합니다.

---

<a id="section-13-22"></a>
## 13.22. Quiz & Summary

### Quiz

**1.** `std::max`가 존재하는데 직접 `max_value<T>`를 작성하는 것이 불필요할 수 있는 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

표준 라이브러리가 이미 동일한 기능을 제공하므로 유지보수 비용을 늘리는 중복 구현이 될 수 있기 때문임. 새로운 도메인 규칙이나 계약이 있을 때 별도 설계를 검토함.

</details>

**2.** `template <typename T>`에서 `T`는 무엇이며, `std::max(1, 2.0)`이 실패할 수 있는 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

`T`는 템플릿 타입 매개변수임. `int`와 `double`을 하나의 `T`로 추론해야 하는 호출에서 타입 충돌이 발생할 수 있음.

</details>

**3.** Concept만으로 센서 측정값의 유효 범위까지 검사할 수 있나요?

<details>
<summary>정답 확인</summary>

아니요. Concept은 컴파일 시점의 타입·연산 요구를 표현하며 실제 측정값의 유효성은 실행 시 별도로 검증해야 함.

</details>

**4.** `Quantity<CelsiusTag, double>`과 `Quantity<KilopascalTag, double>`은 같은 타입인가요?

<details>
<summary>정답 확인</summary>

아니요. 다른 Template 인수로 만들어진 서로 다른 타입이므로 단위 혼합을 타입 수준에서 막을 수 있음.

</details>

**5.** `std::views::filter`와 `std::ranges::to<std::vector>()`는 어떤 차이가 있나요?

<details>
<summary>정답 확인</summary>

`filter`는 조건에 맞는 요소를 지연 평가하는 View를 만들고, `ranges::to`는 요소를 저장하는 새 Container를 구성함.

</details>

**6.** `std::ranges::sort`의 Projection은 어떤 역할을 하나요?

<details>
<summary>정답 확인</summary>

구조체 등에서 실제 비교에 사용할 속성값을 추출함. 전체 객체에 정렬 연산자를 정의하지 않아도 됨.

</details>

**7.** `std::forward`를 사용하는 주된 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

Forwarding Reference로 받은 인수를 다음 호출에 전달할 때 원래 인수의 Value Category를 보존하기 위함.

</details>

**8.** SFINAE와 Concept을 모두 이해해야 하는 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

기존 C++ 코드에서는 `enable_if` 등 SFINAE가 많이 사용되지만, 신규 C++20/23 API에서는 Concept와 `requires`로 의도를 더 명확하게 표현할 수 있기 때문임.

</details>

**9.** `std::expected<T, E>`를 반환하는 Parser가 성공·실패를 구분하는 방법은 무엇인가요?

<details>
<summary>정답 확인</summary>

성공하면 `T` 값을, 실패하면 `std::unexpected(E)`에 담긴 오류를 반환함. 사용 전 `if (result)` 등으로 상태를 확인함.

</details>

**10.** Mini Project의 `summarize()`가 템플릿이어야 하는 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

온도와 압력처럼 서로 다른 요소 타입과 여러 Range를 동일한 읽기 계약(`value()`, `valid()`)으로 처리해야 하기 때문임. Container를 새로 구현하지 않고 표준 Range 개념을 활용함.

</details>

### Summary

- **표준 라이브러리 우선:** `std::max`, `std::ranges`, `std::array`, `std::vector`로 해결 가능한지 검토
- **Function / Class Template:** 여러 타입에 재사용할 코드와 타입별 계약을 정의
- **Concept / Requires:** 필요한 연산과 타입 제약을 컴파일 타임에 명시
- **NTTP / CTAD:** 컴파일 시점 값 전달과 타입 인수 추론
- **Variadic / Fold:** 가변 인수 처리. Container 기반 알고리즘과 선택 기준 비교
- **Type Traits / Specialization:** 타입 특성과 도메인별 정책 구분
- **`if constexpr`:** 타입별 컴파일 시점 분기
- **Generic Lambda / Ranges / Projection:** 직접 반복 구현보다 표준 알고리즘을 활용
- **Perfect Forwarding:** API 래퍼에서 인수의 값 범주 보존
- **`std::expected`:** 성공/실패를 반환형으로 표현
- **SFINAE:** 기존 Template 코드를 이해하기 위한 호환성 지식
- **Explicit Object Parameter:** C++23의 멤버 함수 중복 감소 기능
- **설계 판단:** 직접 템플릿을 정의하기 전에 필요성·표준 라이브러리 대안·제약 조건·테스트 가능성 확인

### References

- [ISO — ISO/IEC 14882:2024, C++23](https://www.iso.org/standard/83626.html)
- [cppreference — C++23 Compiler Support](https://en.cppreference.com/w/cpp/compiler_support/23)
- [cppreference — Templates](https://en.cppreference.com/w/cpp/language/templates)
- [cppreference — Constraints and Concepts](https://en.cppreference.com/w/cpp/language/constraints)
- [cppreference — Ranges](https://en.cppreference.com/w/cpp/ranges)
- [cppreference — `std::expected`](https://en.cppreference.com/w/cpp/utility/expected)
- [C++ Core Guidelines — Templates and Generic Programming](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#t-templates-and-generic-programming)

---

[← C++ 목차](../README.md) · [Chapter 12 — Modern C++ & Resource Management](../Chapter-12/)
