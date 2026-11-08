# Chapter 13. Templates & Generic Programming

하나의 구현을 여러 자료형에 재사용하는 방법을 배우고, 그 과정에서 **어떤 타입을 받아야 하는지, 어떤 연산을 보장해야 하는지**를 명확하게 설계합니다. Chapter 10에서 사용한 표준 알고리즘과 Chapter 12에서 배운 값 범주·이동 의미론을 바탕으로 함수·클래스 템플릿, C++20 Concepts, Ranges와 범용 인터페이스 설계를 학습합니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17의 `if constexpr`와 Fold Expression도 활용합니다. `std::expected`, `std::ranges::to`, Explicit Object Parameter 등 C++23 기능은 개념 비교에만 등장하며 기본 예제 및 프로젝트에서는 사용하지 않습니다.

<details>
<summary>선행 학습</summary>

- [Chapter 05. Functions](../Chapter-05/README.md) — 함수, 반환 타입, 람다
- [Chapter 08. Structs & Classes](../Chapter-08/README.md) — 캡슐화, 클래스, 불변 조건
- [Chapter 10. Standard Library (STL)](../Chapter-10/README.md) — 컨테이너, 반복자, 알고리즘과 Ranges
- [Chapter 12. Modern C++ & Resource Management](../Chapter-12/README.md) — 소유권, 값 범주, `std::move`, `std::forward`와 객체 수명

</details>

## Contents

| Section | Topic |
|:---:|---|
| [13.1](#section-13-1) | Standard Library First — 범용 코드를 작성하기 전에 |
| [13.2](#section-13-2) | Function Template — 함수 템플릿과 인수 추론 |
| [13.3](#section-13-3) | Concepts & Constraints — 타입이 만족해야 하는 조건 |
| [13.4](#section-13-4) | Requires Expression — 사용자 정의 타입 계약 |
| [13.5](#section-13-5) | Class Templates — 타입별 데이터 구조 만들기 |
| [13.6](#section-13-6) | NTTP & CTAD — 값 매개변수와 클래스 인수 추론 |
| [13.7](#section-13-7) | Variadic Templates & Fold Expressions — 여러 인수 처리 |
| [13.8](#section-13-8) | Type Traits & Specialization — 타입 특성과 특수화 |
| [13.9](#section-13-9) | `if constexpr` — 컴파일 시점의 조건 분기 |
| [13.10](#section-13-10) | Generic Lambda — 표준 알고리즘의 사용자 정의 규칙 |
| [13.11](#section-13-11) | Ranges & Views — 지연 평가와 수명 |
| [13.12](#section-13-12) | Projection — 정렬 기준과 데이터 구조 분리 |
| [13.13](#section-13-13) | Perfect Forwarding — 전달 인수의 값 범주 보존 |
| [13.14](#section-13-14) | Result Types — `std::optional`과 파싱 실패 |
| [13.15](#section-13-15) | SFINAE & Legacy Code — 기존 코드와의 연결 |
| [13.16](#section-13-16) | Generic API Design — 필요한 제약만 선언하기 |
| [13.17](#section-13-17) | C++20 & C++23 — 범용 프로그래밍 관련 기능의 구분 |
| [13.18](#section-13-18) | Coding Practice — 연습문제 |
| [13.19](#section-13-19) | Mini Project — Generic Telemetry Pipeline |
| [13.20](#section-13-20) | Quiz & Summary — 점검 및 정리 |
## Getting Started

아래 명령어는 `MoreStudy/C++/Chapter-13/` 폴더에서 실행합니다. 각 단일 예제는 독립적인 `main()` 함수를 포함하므로 **한 번에 하나씩** 컴파일합니다. VS Code의 실행 버튼을 사용할 수도 있지만, 빌드 설정에 따라 적용되는 C++ 표준이 달라질 수 있으므로 다음 명령어로 직접 확인할 수 있습니다.

**GCC (Git Bash)**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/03_concepts_and_requires.cpp -o concepts
./concepts
```

GCC 14가 설치되어 있고 실행 파일 이름이 `g++-14`라면 `g++` 대신 `g++-14`를 사용해도 됩니다.

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/03_concepts_and_requires.cpp -o concepts
./concepts
```

**MSVC (Developer Command Prompt)**

```bat
cl /nologo /std:c++20 /W4 /EHsc /utf-8 examples\03_concepts_and_requires.cpp /Fe:concepts.exe
concepts.exe
```

`<concepts>`는 표준 Concept를, `<ranges>`는 Ranges의 View와 Range 개념을 정의합니다. 새로운 헤더는 각 사용 위치에서 그 역할을 소개합니다. 파일 끝부분의 Mini Project는 여러 `.cpp` 파일을 포함하므로 CMake로 빌드합니다.

**학습 목표**

1. 함수·클래스 템플릿의 역할과 인수 추론 규칙을 설명합니다.
2. Concept와 `requires`로 허용 가능한 타입을 표현합니다.
3. Ranges·Projection·제네릭 람다로 자료를 처리합니다.
4. 이동 의미론과 전달 참조를 구분해 범용 팩토리를 설계합니다.
5. 서로 다른 센서 타입을 공통 처리하는 다중 파일 프로젝트를 구현합니다.

<a id="section-13-1"></a>

## 13.1. Standard Library First — 범용 코드를 작성하기 전에

템플릿(Template)은 타입이나 컴파일 시점의 값을 매개변수로 받아 코드를 정의하는 언어 기능입니다. **제네릭 프로그래밍(Generic Programming)** 은 특정 타입 이름에 종속되지 않고, 여러 타입이 공유하는 연산·규칙을 중심으로 설계하는 접근입니다. C++ 표준 라이브러리의 컨테이너와 알고리즘은 이러한 설계의 대표적인 결과물입니다.

`std::max()`나 정렬 같은 기능이 필요하다면 템플릿을 새로 만드는 것보다 표준 알고리즘을 먼저 살펴보는 것이 좋습니다. 표준 알고리즘은 타입에 대한 요구 조건과 오류가 발생하는 상황을 이미 문서화하고 있으며, 프로젝트별 구현의 중복을 줄입니다.

| 목적 | 우선 고려할 도구 | 새 템플릿을 설계할 이유 |
|---|---|---|
| 두 값 비교 | `std::max`, `std::min` | 프로젝트 고유의 동점 처리·검증 규칙이 필요한 경우 |
| 범위에서 최대 원소 찾기 | `std::ranges::max_element` | 결과를 도메인 객체나 오류 정보로 표현해야 하는 경우 |
| 자료 저장 | `std::array`, `std::vector` | 단위, 크기, 불변 조건을 강제해야 하는 경우 |
| 정렬 | `std::ranges::sort` | 표준 정렬로 표현하기 어려운 특별한 규칙이 필요한 경우 |

`<algorithm>` 헤더는 비교·검색·정렬 알고리즘을, `<array>` 헤더는 고정 크기 배열을 제공합니다. 예제의 `std::ranges::max_element()`는 C++20 Ranges 알고리즘으로, 가장 큰 요소 자체가 아니라 해당 요소를 가리키는 반복자(Iterator)를 반환합니다. 빈 범위에서는 끝 반복자가 반환되므로 사용 전 비교가 필요합니다.

**알아둘 점:** `std::max(1, 2.5)`는 두 인수에서 공통 템플릿 타입을 추론할 수 없어 컴파일되지 않습니다. `std::max<double>(1, 2.5)`로 타입을 지정할 수 있지만, 이러한 형변환이 필요한 이유를 검토해야 합니다.

**예제 코드 — [01_standard_first.cpp](./examples/01_standard_first.cpp)**

```cpp
#include <algorithm>
#include <array>
#include <iostream>

int main() {
    std::cout << "Max: " << std::max(12, 19) << '\n';
    std::cout << "Max double: " << std::max(1.5, 2.75) << '\n';
    std::cout << "Explicit type: " << std::max<double>(1, 2.5) << '\n';
    const std::array readings{18, 26, 21, 32, 24};
    const auto highest = std::ranges::max_element(readings);
    if (highest != readings.end()) {
        std::cout << "Highest reading: " << *highest << '\n';
    }
}
```

**실행 결과**

```text
Max: 19
Max double: 2.75
Explicit type: 2.5
Highest reading: 32
```

실행 결과의 첫 세 줄은 `std::max`가 `int`, `double`, 명시적 `double` 타입에 대해 각각 동작한 결과입니다. 마지막 줄은 `std::array`를 순회하여 최대 요소를 찾은 값입니다.


<a id="section-13-2"></a>

## 13.2. Function Template — 함수 템플릿과 인수 추론

**함수 템플릿(Function Template)** 은 타입 매개변수(Type Parameter)를 이용해 같은 규칙을 여러 타입에 적용합니다. `template <typename T>`에서 `T`는 아직 정해지지 않은 타입이고, 실제 호출 시 컴파일러가 인수로부터 추론합니다. 이렇게 필요한 실제 함수 정의가 만들어지는 과정을 **템플릿 인스턴스화(Template Instantiation)** 라고 부릅니다.

`within_tolerance()`는 측정값이 목표값의 허용 오차 안에 있는지 확인하는 프로젝트 고유 규칙입니다. 인수를 모두 `T`로 받으므로 같은 타입으로 통일해서 호출해야 하며, `within_tolerance(97, 100, 5)`에서는 `T`가 `int`, `within_tolerance(19.8, 20.0, 0.5)`에서는 `double`로 추론됩니다.

| 호출 | 타입 추론 | 결과 |
|---|---|---|
| `within_tolerance(97, 100, 5)` | `T = int` | 호출 가능 |
| `within_tolerance(9.0, 10.0, 0.2)` | `T = double` | 호출 가능 |
| `within_tolerance(9, 10.0, 0.2)` | 충돌 | 호출 불가 |
| `within_tolerance<double>(9, 10.0, 0.2)` | 명시적 `T` | 호출 가능 |

이 예제는 오차가 음수라면 실패하도록 하되, 큰 정수에서 뺄셈·덧셈이 표현 범위를 넘는 상황까지 일반적으로 해결하지는 않습니다. 실제 계측 시스템에서는 입력 범위를 먼저 제한하거나, 더 넓은 타입을 선택해야 합니다. 부동소수점의 NaN과 무한대 정책도 별도로 정의할 수 있습니다.

**반환 타입과 매개변수는 서로 구분해야 합니다.** 템플릿이라고 해서 여러 타입을 한 함수 호출에서 자동으로 안전하게 섞어 주는 것은 아닙니다.

**예제 코드 — [02_template_deduction.cpp](./examples/02_template_deduction.cpp)**

```cpp
#include <iostream>

template <typename T>
[[nodiscard]] bool within_tolerance(T measured, T target, T tolerance) {
    return tolerance >= T{} && measured >= target - tolerance &&
           measured <= target + tolerance;
}

int main() {
    std::cout << std::boolalpha;
    std::cout << "Integer: " << within_tolerance(97, 100, 5) << '\n';
    std::cout << "Double: " << within_tolerance(19.8, 20.0, 0.5) << '\n';
    std::cout << "Explicit: " << within_tolerance<double>(9, 10.0, 0.2) << '\n';
}
```

**실행 결과**

```text
Integer: true
Double: true
Explicit: false
```

세 호출은 모두 동일한 템플릿 본문을 사용합니다. `Explicit` 사례에서는 값 `9`가 `double`로 변환되지만 목표 `10.0`과의 차이가 `0.2`보다 크므로 `false`입니다.


<a id="section-13-3"></a>

## 13.3. Concepts & Constraints — 타입이 만족해야 하는 조건

C++20의 **콘셉트(Concept)** 는 템플릿 인수에 요구하는 조건을 컴파일 시점에 표현하는 기능입니다. 템플릿 본문에서 복잡한 오류가 발생하기 전에 허용할 타입을 인터페이스에 드러낼 수 있습니다. 콘셉트를 이용해 정의한 조건을 **제약 조건(Constraint)** 이라고 합니다.

`<concepts>` 헤더는 `std::integral`, `std::floating_point`, `std::convertible_to` 등의 표준 Concept를 제공합니다. `template <std::integral T>`는 정수 타입에만, `template <std::floating_point T>`는 부동소수점 타입에만 해당 함수를 적용하도록 제한합니다. 이 검사는 실제 함수가 실행될 때가 아니라 **컴파일 시점**에 수행됩니다.

| 개념 | 예 | 주의할 점 |
|---|---|---|
| `std::integral<T>` | `int`, `long long`, `bool` | `bool`도 정수 계열 Concept를 만족합니다. |
| `std::floating_point<T>` | `float`, `double` | 정수 타입은 허용되지 않습니다. |
| `std::same_as<T, U>` | 정확히 같은 타입 | 암시적 변환은 허용하지 않습니다. |
| `std::convertible_to<T, U>` | `T`에서 `U`로 변환 가능 | 실제 값 범위까지 검사하는 것은 아닙니다. |

Concept는 **문법적·타입 수준의 계약**입니다. 예를 들어 부동소수점 타입이라고 하더라도 NaN, 무한대, 허용 범위 초과와 같은 데이터 오류는 실행 시점에 따로 검증해야 합니다.

**예제 코드 — [03_concepts_and_requires.cpp](./examples/03_concepts_and_requires.cpp)**

```cpp
#include <concepts>
#include <iostream>

template <std::integral T>
[[nodiscard]] bool is_even(T value) { return value % 2 == 0; }

template <std::floating_point T>
[[nodiscard]] T midpoint(T left, T right) {
    return left + (right - left) / T{2};
}

int main() {
    std::cout << std::boolalpha << "Even: " << is_even(12) << '\n';
    std::cout << "Midpoint: " << midpoint(1.0, 3.0) << '\n';
    // is_even(2.5); // std::integral 제약을 만족하지 않아 컴파일되지 않음
}
```

**실행 결과**

```text
Even: true
Midpoint: 2
```

`is_even(12)`은 정수 Concept를 만족하고, `midpoint(1.0, 3.0)`은 부동소수점 Concept를 만족합니다. 반면 주석 처리된 `is_even(2.5)`는 의도적으로 컴파일할 수 없는 호출입니다.


<a id="section-13-4"></a>

## 13.4. Requires Expression — 사용자 정의 타입 계약

표준 Concept만으로 프로젝트에서 필요한 데이터 인터페이스를 표현하기 어려울 때 **사용자 정의 Concept(User-defined Concept)** 를 작성할 수 있습니다. **요구 표현식(Requires Expression)** 은 특정 타입에 어떤 멤버 또는 연산이 존재하며, 결과가 어떤 타입 조건을 만족하는지 검사합니다.

`ReadingLike<T>`는 `const T&`로 접근할 때 `value()`가 `double`로 변환 가능하고 `valid()`가 `bool`로 변환 가능하다는 조건을 요구합니다. 이 조건을 만족하면 센서 클래스의 구체적 이름을 몰라도 `needs_attention()`을 작성할 수 있습니다.

| 구성 | 의미 |
|---|---|
| `requires(const T& reading)` | 검사에 사용할 가상 매개변수 선언 |
| `{ reading.value() }` | 해당 표현식을 사용할 수 있는지 검사 |
| `-> std::convertible_to<double>` | 결과 타입이 `double`로 변환 가능한지 검사 |
| `static_assert(ReadingLike<Temperature>)` | 컴파일 중 계약 확인 |

Requires Expression 내부의 표현식은 일반적으로 평가되지 않으므로, 이 코드가 센서를 실제로 읽거나 `valid()`를 실행하는 것은 아닙니다. 호출 후 반환되는 **데이터의 의미와 값 범위**는 프로그램 실행 과정에서 별도로 검증해야 합니다. `static_assert(!ReadingLike<int>)`는 일반 정수에 필요한 멤버 함수가 없음을 검증합니다.

**예제 코드 — [04_reading_contract.cpp](./examples/04_reading_contract.cpp)**

```cpp
#include <concepts>
#include <iostream>

template <typename T>
concept ReadingLike = requires(const T& reading) {
    { reading.value() } -> std::convertible_to<double>;
    { reading.valid() } -> std::convertible_to<bool>;
};

struct Temperature {
    double degrees;
    bool okay;
    [[nodiscard]] double value() const { return degrees; }
    [[nodiscard]] bool valid() const { return okay; }
};

static_assert(ReadingLike<Temperature>);
static_assert(!ReadingLike<int>);

template <ReadingLike T>
[[nodiscard]] bool needs_attention(const T& item) {
    return item.valid() && item.value() >= 80.0;
}

int main() {
    std::cout << std::boolalpha << "Alert: "
              << needs_attention(Temperature{85.0, true}) << '\n';
}
```

**실행 결과**

```text
Alert: true
```

`Temperature{85.0, true}` 객체는 `ReadingLike`를 만족하고 유효한 측정값이 80 이상이므로 `Alert: true`가 출력됩니다.


<a id="section-13-5"></a>

## 13.5. Class Templates — 타입별 데이터 구조 만들기

**클래스 템플릿(Class Template)** 은 객체의 자료형을 외부에서 정하는 클래스 설계 방식입니다. Chapter 08에서 배운 캡슐화(Encapsulation)를 그대로 적용할 수 있으며, 같은 데이터 구조를 정수·실수·문자열 등에 반복해서 구현하지 않아도 됩니다.

`SampleBuffer<T>`는 `std::vector<T>`를 내부 멤버로 가진 간단한 버퍼입니다. `<vector>`는 크기를 변경할 수 있는 연속 컨테이너를 제공하고, `<cstddef>`의 `std::size_t`는 요소 수와 인덱스에 사용합니다. `<stdexcept>`는 아래 예제의 범위 검사에서 발생할 수 있는 예외와 관련된 표준 예외 타입을 선언합니다.

버퍼는 `add()`로 입력을 받아 내부 저장소를 변경하고, `at()`으로 범위를 검사하며 읽습니다. 사용자는 컨테이너의 구현 세부사항이 아니라 `SampleBuffer<int>`와 `SampleBuffer<double>`라는 **공통 인터페이스**를 사용합니다.

`const T&` 매개변수를 받는 방식은 복사 비용을 줄일 수 있으나, 실제 `push_back()`은 요소를 저장하기 위해 복사합니다. Move-only 객체를 효율적으로 저장하려면 rvalue 참조를 받는 오버로드나 `emplace()` 같은 인터페이스가 추가로 필요합니다. Chapter 12의 이동 의미론과 연결되는 부분입니다.

**클래스 템플릿 정의를 헤더에 두는 이유:** 다른 소스 파일에서 `SampleBuffer<double>` 등을 인스턴스화할 때 컴파일러가 구현을 볼 수 있어야 하기 때문입니다. 별도 `.cpp` 구현 파일로 분리하려면 사용 타입에 대한 명시적 인스턴스화 같은 추가 설계가 필요합니다.

**예제 코드 — [05_class_templates.cpp](./examples/05_class_templates.cpp)**

```cpp
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <vector>

template <typename T>
class SampleBuffer {
public:
    void add(const T& item) { samples_.push_back(item); }
    [[nodiscard]] const T& at(std::size_t index) const { return samples_.at(index); }
    [[nodiscard]] std::size_t size() const noexcept { return samples_.size(); }
private:
    std::vector<T> samples_;
};

int main() {
    SampleBuffer<int> integers;
    integers.add(12);
    integers.add(19);
    SampleBuffer<double> decimals;
    decimals.add(2.5);
    std::cout << "Integer samples: " << integers.size() << '\n';
    std::cout << "First double: " << decimals.at(0) << '\n';
}
```

**실행 결과**

```text
Integer samples: 2
First double: 2.5
```

정수 버퍼에는 2개 요소가 저장되었고, 실수 버퍼의 첫 요소는 `2.5`입니다. 두 객체는 템플릿이지만 서로 다른 구체적 타입입니다.


<a id="section-13-6"></a>

## 13.6. NTTP & CTAD — 값 매개변수와 클래스 인수 추론

템플릿은 타입뿐 아니라 **컴파일 시점에 결정되는 값**도 매개변수로 받을 수 있습니다. 이를 **비타입 템플릿 매개변수(Non-Type Template Parameter, NTTP)** 라고 합니다. 고정 크기 배열의 크기처럼 타입의 일부가 되는 값을 전달할 때 유용합니다.

`sum_fixed()`의 `N`은 `std::array<T, N>`의 크기이며, `N`은 런타임 변수처럼 자유롭게 바뀌지 않습니다. 예를 들어 `std::array<int, 3>`과 `std::array<int, 4>`는 서로 다른 타입입니다.

C++17의 **클래스 템플릿 인수 추론(Class Template Argument Deduction, CTAD)** 은 생성자 인수 등으로부터 클래스 템플릿 매개변수를 추론합니다. 예제에서 `std::array numbers{2, 4, 6}`는 `std::array<int, 3>`을 뜻합니다.

| 구분 | 판단 시점 | 예시 |
|---|---|---|
| 타입 매개변수 `T` | 템플릿 인스턴스화 시 | `int`, `double` |
| 값 매개변수 `N` | 컴파일 시 | `3`, `5` |
| CTAD | 생성 구문을 컴파일할 때 | `std::array{1, 2, 3}` |

CTAD가 항상 개발자의 의도에 맞는 타입을 골라 주는 것은 아닙니다. 자료형을 명시해야 하는 공개 API나 서로 다른 수치 타입을 다룰 때는 `std::array<double, 3>`처럼 직접 타입을 적는 편이 더 명확할 수 있습니다.

**예제 코드 — [06_nttp_ctad.cpp](./examples/06_nttp_ctad.cpp)**

```cpp
#include <array>
#include <cstddef>
#include <iostream>

template <typename T, std::size_t N>
[[nodiscard]] T sum_fixed(const std::array<T, N>& items) {
    T sum{};
    for (const auto& item : items) sum += item;
    return sum;
}

int main() {
    const std::array numbers{2, 4, 6}; // CTAD: std::array<int, 3>
    std::cout << "Size: " << numbers.size() << '\n';
    std::cout << "Sum: " << sum_fixed(numbers) << '\n';
}
```

**실행 결과**

```text
Size: 3
Sum: 12
```

세 개 요소가 `std::array<int, 3>`으로 추론되며, `sum_fixed()`는 원소를 순회하여 합계 12를 출력합니다.


<a id="section-13-7"></a>

## 13.7. Variadic Templates & Fold Expressions — 여러 인수 처리

**가변 인수 템플릿(Variadic Template)** 은 개수가 고정되지 않은 타입 또는 함수 인수를 처리합니다. `Ts...`는 **템플릿 매개변수 팩(Template Parameter Pack)** 이며, `values...`는 함수 인수 팩을 뜻합니다.

C++17의 **접기 표현식(Fold Expression)** 은 팩에 포함된 값을 반복적인 재귀 호출 없이 연산자로 결합합니다. 예제의 `(0LL + ... + static_cast<long long>(values))`는 덧셈의 초기값으로 `0LL`을 제공하므로 인수가 하나도 없는 경우에도 0을 반환할 수 있습니다.

인수가 세 개인 경우 개념적으로 `(((0LL + 4) + 7) + 9)`와 같은 누적 연산이 수행됩니다. 하지만 모든 연산자에 대해 같은 결합 순서가 적합한 것은 아니므로, 팩을 사용하는 목적과 연산자의 성질을 확인해야 합니다.

여기서는 `std::integral`을 제약으로 사용해 정수 계열 인수만 허용합니다. `long long`으로 캐스팅해 계산하지만 매우 큰 합에서는 여전히 오버플로가 가능하므로, 서비스 코드에서는 입력 범위 또는 합계 정책을 정의해야 합니다.

**예제 코드 — [07_variadic_fold.cpp](./examples/07_variadic_fold.cpp)**

```cpp
#include <concepts>
#include <iostream>

template <std::integral... Ts>
[[nodiscard]] long long sum_all(Ts... values) {
    return (0LL + ... + static_cast<long long>(values));
}

int main() {
    std::cout << "Total: " << sum_all(4, 7, 9) << '\n';
    std::cout << "Empty: " << sum_all() << '\n';
}
```

**실행 결과**

```text
Total: 20
Empty: 0
```

입력 `4, 7, 9`의 합 20과 빈 팩의 합 0을 확인합니다.


<a id="section-13-8"></a>

## 13.8. Type Traits & Specialization — 타입 특성과 특수화

**타입 특성(Type Traits)** 은 타입이 정수인지, 복사 가능한지, 특정 성질을 가지는지를 컴파일 시점에 확인하는 표준 도구입니다. `<type_traits>` 헤더에서 `std::is_arithmetic_v<T>` 같은 형태로 사용할 수 있습니다.

**템플릿 특수화(Template Specialization)** 는 일반 템플릿의 특정 타입에 대해 다른 정의를 제공하는 기능입니다. `TypeLabel<T>`는 일반적으로 `"other"`를 제공하지만 `TypeLabel<int>`에서는 `"integer"`를 제공합니다.

| 상황 | 우선 고려할 방법 |
|---|---|
| 특정 타입 여부를 질문 | `std::is_*_v<T>` 타입 특성 |
| 타입의 허용 범위를 선언 | C++20 Concept |
| 특정 타입의 다른 구현 | 명시적 특수화 또는 적절한 오버로드 |
| 한 템플릿 내부에서 조건부 처리 | `if constexpr` |

특수화가 늘어나면 타입별 동작을 찾기 어려워질 수 있으므로 일반적인 인터페이스를 먼저 검토합니다. **함수 템플릿은 부분 특수화할 수 없으며**, 함수 오버로딩이나 Concept로 제약을 나누는 것이 일반적인 해결책입니다.

예제의 `constexpr std::string_view`는 컴파일 시점에 결정할 수 있는 문자열 뷰를 저장하며, `<string_view>`는 소유권을 가지지 않는 문자열 조회 타입을 선언합니다.

**예제 코드 — [08_traits_specialization.cpp](./examples/08_traits_specialization.cpp)**

```cpp
#include <iostream>
#include <string_view>
#include <type_traits>

template <typename T>
struct TypeLabel {
    static constexpr std::string_view name = "other";
};

template <>
struct TypeLabel<int> {
    static constexpr std::string_view name = "integer";
};

template <typename T>
constexpr bool arithmetic_value = std::is_arithmetic_v<T>;

int main() {
    std::cout << std::boolalpha;
    std::cout << "Arithmetic: " << arithmetic_value<double> << '\n';
    std::cout << "Label: " << TypeLabel<int>::name << '\n';
    std::cout << "Other: " << TypeLabel<std::string_view>::name << '\n';
}
```

**실행 결과**

```text
Arithmetic: true
Label: integer
Other: other
```

`double`은 산술 타입이므로 `true`, `int`에는 특수화된 레이블이, `std::string_view`에는 기본 레이블이 사용됩니다.


<a id="section-13-9"></a>

## 13.9. `if constexpr` — 컴파일 시점의 조건 분기

`if constexpr`는 C++17부터 제공되는 **컴파일 시점 조건 분기(Compile-Time Conditional)** 문법입니다. 일반 `if`와 달리 템플릿의 구체적인 타입에서 조건을 평가하여 선택되지 않은 분기를 버릴 수 있습니다.

예제의 `clean_reading()`은 실수 타입일 때만 `std::isfinite()`로 NaN과 무한대를 처리하고, 정수 타입일 때는 원래 값을 그대로 반환합니다. `<cmath>`는 `std::isfinite()`와 같은 수학 함수를 제공하고, `<type_traits>`는 실수 타입 여부를 나타내는 `std::is_floating_point_v<T>`를 제공합니다.

일반 `if`로 타입별 구현을 분리하면 선택되지 않은 코드도 컴파일되어 문법 문제가 발생할 수 있지만, `if constexpr`에서는 템플릿 인스턴스화 중 조건에 맞지 않는 분기를 버리는 방식으로 이러한 문제를 줄입니다. 그렇다고 모든 잘못된 코드가 무조건 허용되는 것은 아닙니다. 템플릿과 무관하게 명백히 잘못된 코드는 여전히 컴파일 오류가 될 수 있습니다.

타입별 정책을 아주 많이 분기해야 한다면 하나의 거대한 템플릿보다는 역할에 맞는 오버로드나 별도 함수를 검토하는 편이 읽기 쉽습니다.

**예제 코드 — [09_if_constexpr.cpp](./examples/09_if_constexpr.cpp)**

```cpp
#include <cmath>
#include <iostream>
#include <type_traits>

template <typename T>
[[nodiscard]] T clean_reading(T value) {
    if constexpr (std::is_floating_point_v<T>) {
        return std::isfinite(value) ? value : T{};
    } else {
        return value;
    }
}

int main() {
    std::cout << "Integer: " << clean_reading(12) << '\n';
    std::cout << "Invalid double: " << clean_reading(std::nan("")) << '\n';
}
```

**실행 결과**

```text
Integer: 12
Invalid double: 0
```

정수 12는 그대로 유지되고, 유효하지 않은 부동소수점 측정값은 0으로 치환됩니다. 실제 계측에서는 이러한 치환이 데이터 누락을 숨길 수 있으므로 실무에서는 별도의 오류 상태를 반환하는 방법도 고려합니다.


<a id="section-13-10"></a>

## 13.10. Generic Lambda — 표준 알고리즘의 사용자 정의 규칙

**제네릭 람다(Generic Lambda)** 는 C++14부터 `auto` 매개변수를 사용할 수 있는 람다 표현식입니다. 호출되는 타입에 따라 내부적으로 함수 호출 연산자가 템플릿처럼 동작합니다.

예제의 람다는 `value > 10`을 판정하며, C++20의 `std::ranges::count_if()`가 각 원소에 대해 이를 호출합니다. `<algorithm>`은 해당 알고리즘을 제공하고 `<vector>`는 측정값 저장소를 제공합니다.

람다의 반환 타입이 `bool`처럼 해석되어야 한다는 요구는 알고리즘 인터페이스의 일부입니다. 이 경우 `count_if()`를 사용하므로 직접 루프 카운터를 관리하지 않아도 되고, 비교 규칙만 람다에 남겨 둘 수 있습니다.

조건이 여러 곳에서 공유되고 의미가 중요하다면 람다를 복사해서 사용하는 대신 이름 있는 함수나 함수 객체(Function Object)로 분리할 수 있습니다. 작은 한 번의 조건은 람다로 작성하는 편이 간결합니다.

**예제 코드 — [10_generic_lambda.cpp](./examples/10_generic_lambda.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    const std::vector readings{8, 19, 32, 7};
    const auto over_ten = [](const auto& value) { return value > 10; };
    const auto count = std::ranges::count_if(readings, over_ten);
    std::cout << "Above 10: " << count << '\n';
}
```

**실행 결과**

```text
Above 10: 2
```

측정값 중 10을 초과하는 값은 19와 32이므로 2개가 출력됩니다.


<a id="section-13-11"></a>

## 13.11. Ranges & Views — 지연 평가와 수명

C++20의 **Ranges**는 반복자로 표현된 구간을 컨테이너·뷰 등의 형태로 다룰 수 있도록 개선된 범용 인터페이스입니다. `<ranges>` 헤더는 `std::views::filter` 및 `std::views::transform` 등 **뷰(View)** 를 제공합니다.

뷰는 대개 모든 결과를 미리 저장하지 않고 **지연 평가(Lazy Evaluation)** 방식으로 원본을 순회합니다. 예제는 10 이상인 값만 고르고 두 배로 변환하는 파이프라인을 만듭니다. 최종 결과를 계속 보유해야 하므로 루프를 통해 새 `std::vector<int>`에 복사합니다.

**주의할 점은 뷰가 원본 데이터를 소유하지 않을 수 있다는 것**입니다. 예제의 `readings`는 `selected`를 순회하는 동안 유효하게 존재해야 합니다. 원본 벡터를 변경하면 뷰의 반복자나 내부 상태가 무효화될 수도 있습니다. 또한 일부 `filter_view`·`transform_view` 조합은 C++20에서 `const`로 선언한 뷰를 순회할 수 없으므로, 예제에서는 `auto selected`로 선언합니다.

C++23의 `std::ranges::to<std::vector>()`로 뷰를 바로 컨테이너로 만드는 기능은 **C++20 표준에 포함되어 있지 않습니다**. 여기서는 원소를 순회해서 결과를 저장합니다. Ranges가 언제나 빠르거나 메모리를 절약하는 것은 아니므로 측정 가능한 요구가 있을 때 선택하세요.

**예제 코드 — [11_ranges_views.cpp](./examples/11_ranges_views.cpp)**

```cpp
#include <iostream>
#include <ranges>
#include <vector>

int main() {
    const std::vector readings{5, 12, 19, 20, 7};
    auto selected = readings
        | std::views::filter([](int n) { return n >= 10; })
        | std::views::transform([](int n) { return n * 2; });
    std::vector<int> output;
    for (int value : selected) output.push_back(value);
    std::cout << "Selected:";
    for (int value : output) std::cout << ' ' << value;
    std::cout << '\n';
}
```

**실행 결과**

```text
Selected: 24 38 40
```

10 이상인 원소 12, 19, 20이 각각 24, 38, 40으로 변환됩니다. 원본 벡터는 그대로 유지됩니다.


<a id="section-13-12"></a>

## 13.12. Projection — 정렬 기준과 데이터 구조 분리

**프로젝션(Projection)** 은 원소의 일부 값을 꺼내 알고리즘의 비교·검색 기준으로 사용하는 함수 또는 멤버 포인터입니다. C++20의 Ranges 알고리즘은 비교자(Comparator) 외에 Projection을 전달할 수 있습니다.

`std::ranges::sort(devices, {}, &Device::id)`에서 `{}`는 기본 비교자인 `std::ranges::less{}`를 사용한다는 뜻이고, `&Device::id`는 `id` 멤버를 정렬 기준으로 선택합니다. 따라서 비교용 람다를 직접 작성하지 않아도 장치를 ID 기준 오름차순으로 정렬할 수 있습니다.

| 방법 | 특성 |
|---|---|
| `std::sort` + 람다 | 오래된 표준에서도 사용 가능, 비교 기준 명시 |
| `std::ranges::sort` + Projection | 원소에서 비교할 속성을 분리, C++20 |
| `std::stable_sort` | 비교 기준이 같은 원소의 상대적 순서를 유지 |

`std::ranges::sort()`는 안정 정렬(Stable Sort)을 보장하지 않습니다. 동일한 ID를 가진 원소의 입력 순서를 반드시 보존해야 한다면 안정 정렬 알고리즘이나 별도 순서 키를 사용해야 합니다. `std::ranges::sort`에는 랜덤 접근 반복자(Random-Access Iterator) 등이 필요하므로 모든 Range를 바로 정렬할 수는 없습니다.

**예제 코드 — [12_projection.cpp](./examples/12_projection.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Device {
    std::string id;
    int reading;
};

int main() {
    std::vector<Device> devices{{"B", 4}, {"A", 8}, {"C", 2}};
    std::ranges::sort(devices, {}, &Device::id);
    for (const auto& device : devices) {
        std::cout << device.id << ':' << device.reading << ' ';
    }
    std::cout << '\n';
}
```

**실행 결과**

```text
A:8 B:4 C:2
```

장치 벡터의 입력 순서는 B, A, C이지만 ID 기준으로 정렬한 뒤 A, B, C 순서로 출력됩니다.


<a id="section-13-13"></a>

## 13.13. Perfect Forwarding — 전달 인수의 값 범주 보존

Chapter 12의 이동 의미론을 범용 팩토리 함수에 적용하려면, 전달받은 인수가 **lvalue인지 rvalue인지 유지**해야 합니다. 이를 **완벽 전달(Perfect Forwarding)** 이라고 하며 `<utility>` 헤더의 `std::forward<T>()`를 사용합니다.

`Args&&... args`는 템플릿 인수 추론이 일어나는 문맥에서 **전달 참조(Forwarding Reference)** 로 동작합니다. `std::forward<Args>(args)...`는 호출자에게서 받은 값 범주를 유지한 채 `std::make_unique<T>()`의 생성자 인수로 전달합니다. `std::make_unique`는 `<memory>`에서 제공하는 소유권 생성 함수입니다.

- 이름이 있는 변수 `name`은 lvalue이므로 `std::string` 복사 경로를 사용할 수 있습니다.
- 임시 `std::string{"Pump-B"}`는 rvalue로 전달되어 이동 경로를 사용할 수 있습니다.
- `std::move()`는 **무조건 rvalue로 취급**하도록 바꾸지만, `std::forward<T>()`는 전달된 인수의 원래 값 범주를 보존합니다.

**무조건 `std::forward`를 호출하는 것은 좋은 설계가 아닙니다.** 전달 참조와 타입 추론이라는 조건을 이해해야 하고, 수명·소유권 문제가 있는 API라면 단순히 `const T&` 또는 값 전달을 선택하는 편이 안전할 수 있습니다.

**예제 코드 — [13_forwarding.cpp](./examples/13_forwarding.cpp)**

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <utility>

template <typename T, typename... Args>
[[nodiscard]] std::unique_ptr<T> create(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}

struct Device {
    explicit Device(std::string value) : name(std::move(value)) {}
    std::string name;
};

int main() {
    std::string name{"Pump-A"};
    auto first = create<Device>(name);         // lvalue: 복사 가능
    auto second = create<Device>(std::string{"Pump-B"}); // rvalue: 이동 가능
    std::cout << first->name << ", " << second->name << '\n';
}
```

**실행 결과**

```text
Pump-A, Pump-B
```

`create<Device>()`는 두 인수 형태 모두에서 소유 객체를 안전하게 생성하고 장치 이름을 출력합니다.


<a id="section-13-14"></a>

## 13.14. Result Types — `std::optional`과 파싱 실패

범용 코드를 만들더라도 **실패할 수 있는 계산**의 결과를 어떻게 표현하는지는 명확해야 합니다. Chapter 05와 Chapter 11에서 다룬 `std::optional<T>`는 결과가 있거나 없을 수 있는 경우에 적합합니다. `<optional>`은 이 타입을 선언하고, `<charconv>`의 `std::from_chars()`는 문자열을 숫자로 변환할 때 로케일에 의존하지 않고 실패 여부를 반환합니다.

예제는 포트 번호를 가정해 `1`부터 `65535`까지만 허용합니다. 숫자 변환 자체가 성공해도 문자열 끝까지 읽지 않았다면 실패로 처리합니다. 따라서 `"80x"`처럼 일부만 숫자인 입력을 거부할 수 있습니다.

`std::from_chars`는 `{ptr, ec}` 형태의 결과를 돌려줍니다. `ec`에는 변환 성공/실패 상태가, `ptr`에는 변환이 끝난 위치가 들어 있습니다. `<system_error>`는 `std::errc`의 선언과 관련됩니다.

C++20에는 `std::expected<T, E>`가 표준으로 포함되어 있지 않습니다. 오류 원인을 상세하게 전달해야 한다면 **결과 구조체 + `std::optional`**, 명시적 오류 코드, 예외 등의 C++20 방법을 설계할 수 있습니다. `std::expected` 자체는 C++23에서 다룹니다.

**예제 코드 — [14_optional_parser.cpp](./examples/14_optional_parser.cpp)**

```cpp
#include <charconv>
#include <iostream>
#include <optional>
#include <string_view>
#include <system_error>

[[nodiscard]] std::optional<int> parse_port(std::string_view text) {
    if (text.empty()) return std::nullopt;
    int port{};
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), port);
    if (error != std::errc{} || end != text.data() + text.size() ||
        port < 1 || port > 65535) return std::nullopt;
    return port;
}

int main() {
    std::cout << "Port: " << parse_port("8080").value_or(-1) << '\n';
    std::cout << "Invalid: " << parse_port("80x").has_value() << '\n';
}
```

**실행 결과**

```text
Port: 8080
Invalid: 0
```

정상 입력 `8080`은 값을 반환합니다. `"80x"`는 문자열을 끝까지 소비하지 않았으므로 결과가 없고 `false`가 `0`으로 출력됩니다.


<a id="section-13-15"></a>

## 13.15. SFINAE & Legacy Code — 기존 코드와의 연결

**대입 실패는 오류가 아님(Substitution Failure Is Not An Error, SFINAE)** 은 템플릿 인수를 대입하는 과정에서 특정 후보가 적합하지 않으면 해당 후보를 오버로드 선택에서 제외하는 언어 규칙입니다. C++20 이전의 범용 라이브러리에는 `<type_traits>`의 `std::enable_if_t`를 이용한 코드가 많이 남아 있습니다.

예제의 `legacy_even()`은 `std::is_integral_v<T>`가 참인 경우에만 반환 타입이 형성되도록 만들었습니다. 반면 `modern_even()`은 `template <std::integral T>`로 같은 의도를 직접 표현합니다. 새 코드에서는 대체로 Concept가 읽기 쉽고 오류 메시지도 명확합니다.

| 구분 | `std::enable_if_t` | C++20 Concept |
|---|---|---|
| 제약 조건의 위치 | 반환 타입 또는 템플릿 매개변수 등 | 인터페이스의 선언부 |
| 학습 시점 | 기존 라이브러리를 읽을 때 유용 | 새 범용 API 작성 시 우선 고려 |
| 오류 표현 | 대입·후보 제거 규칙에 의존 | 충족되지 않은 제약 조건이 드러남 |

Concept가 SFINAE의 모든 사용 사례를 한 번에 대체한다고 단정할 수는 없습니다. 다만 같은 의미를 더 분명하게 설명할 수 있다면 새 프로젝트에서는 Concept를 우선 검토합니다.

**예제 코드 — [15_legacy_constraints.cpp](./examples/15_legacy_constraints.cpp)**

```cpp
#include <concepts>
#include <iostream>
#include <type_traits>

template <typename T>
std::enable_if_t<std::is_integral_v<T>, bool> legacy_even(T value) {
    return value % 2 == 0;
}

template <std::integral T>
[[nodiscard]] bool modern_even(T value) { return value % 2 == 0; }

int main() {
    std::cout << std::boolalpha << "Legacy: " << legacy_even(6) << '\n';
    std::cout << "Concept: " << modern_even(6) << '\n';
}
```

**실행 결과**

```text
Legacy: true
Concept: true
```

두 함수 모두 `6`을 짝수로 판정하지만, 제약 조건을 인터페이스에 표현하는 방식이 다릅니다.


<a id="section-13-16"></a>

## 13.16. Generic API Design — 필요한 제약만 선언하기

범용 인터페이스가 안정적이려면 **불필요하게 넓은 타입을 받지 않고, 실제로 사용하는 연산과 값 범위를 문서화**해야 합니다. 템플릿은 타입 안전성을 자동으로 보장하는 마법이 아닙니다.

`SafeReading`은 실수 타입이라는 조건과 덧셈 결과가 정확히 같은 타입인지 확인하는 조건을 함께 정의합니다. `<concepts>`의 `std::same_as`는 암시적 변환만으로 충족되지 않는 엄격한 타입 일치 검증입니다.

`average()`는 `first + (second - first) / 2`를 사용합니다. 이는 일반적인 센서 범위에서 직관적이지만, 매우 큰 절댓값이나 극단적인 부동소수점 값에서 수치 오차가 없음을 보장하지는 않습니다. 실제 API에서는 **허용 범위·NaN/Infinity 처리·오차 허용치·실패 반환 방식**을 추가로 합의해야 합니다.

- 타입 제약은 컴파일 시점에 확인합니다.
- 입력 값의 유효성은 실행 시점에 검증합니다.
- 범용 코드를 읽는 사람이 의미를 파악할 수 있도록 구체적인 함수명과 반환 계약을 작성합니다.
- 과도한 템플릿 추상화는 피하고, 실제로 여러 타입에서 공유하는 처리 규칙에만 사용합니다.

**예제 코드 — [16_api_contracts.cpp](./examples/16_api_contracts.cpp)**

```cpp
#include <concepts>
#include <iostream>
#include <type_traits>

template <typename T>
concept SafeReading = std::floating_point<T> && requires(T value) {
    { value + value } -> std::same_as<T>;
};

template <SafeReading T>
[[nodiscard]] T average(T first, T second) {
    return first + (second - first) / T{2};
}

static_assert(SafeReading<double>);
static_assert(!SafeReading<int>);

int main() {
    std::cout << "Average: " << average(4.0, 8.0) << '\n';
}
```

**실행 결과**

```text
Average: 6
```

`average(4.0, 8.0)`은 타입 제약을 만족하고 결과 6을 출력합니다.


<a id="section-13-17"></a>

## 13.17. C++20 & C++23 — 범용 프로그래밍 관련 기능의 구분

Chapter 13의 기본 컴파일 표준은 C++20입니다. 이후 표준에 포함된 기능을 알고 있으면 기존 코드의 의도를 읽는 데 도움이 되지만, 이번 Chapter의 기본 코드를 작성할 때는 호환성을 먼저 확인해야 합니다.

| 기능 | 표준 | 이번 Chapter에서 사용하는 방법 |
|---|---|---|
| Concepts / Requires Expression | C++20 | 기본 예제에서 사용 |
| Ranges Algorithms / Views | C++20 | `std::ranges::sort`, `views::filter` 등 사용 |
| NTTP / CTAD | NTTP는 오래된 기능 / CTAD는 C++17 | 예제에서 사용 |
| `if constexpr` / Fold Expression | C++17 | 예제에서 사용 |
| `std::expected<T, E>` | C++23 | 비교 설명만 제공. C++20에서는 `std::optional` 등 사용 |
| `std::ranges::to` | C++23 | 비교 설명만 제공. C++20에서는 루프로 결과 컨테이너 생성 |
| Explicit Object Parameter (`this` 매개변수) | C++23 | 별도 참고 개념. 기본 코드에 사용하지 않음 |

**템플릿 구현에서 주의할 사항**

- 여러 번 사용하는 템플릿 구현은 일반적으로 헤더에 정의합니다. 선언만 있고 정의가 보이지 않으면 다른 번역 단위(Translation Unit)에서 인스턴스화하거나 링크하는 과정에 문제가 생길 수 있습니다.
- Concept는 실제 값이 올바르다는 보장이 아니라 타입과 연산에 관한 컴파일 시점의 계약입니다.
- 타입별 구현이 많아진다는 이유만으로 특수화를 반복하지 않습니다. 표준 알고리즘과 일반 함수로 해결할 수 있는지 먼저 판단합니다.
- 범용 코드에서는 복사·이동, 참조 수명, 컨테이너 무효화 문제를 Chapter 12에서 배운 방식으로 확인합니다.

<a id="section-13-18"></a>

## 13.18. Coding Practice — 연습문제

실습은 각 함수가 가져야 하는 **동작 계약**을 직접 구현하는 형태입니다. 학생용 시작 코드는 `exercises/`에, 완성된 모범답안은 `solutions/`에 분리되어 있습니다. 학생용 파일은 TODO를 채우기 전에는 자동 검증에 실패하도록 설계했습니다. 필요한 문법과 표준 라이브러리는 앞선 Section에서 소개했습니다.

### Exercise 01 — Reading Alert

실수형 측정값과 경보 기준값을 받아 위험 여부를 판단하는 `reading_alert()`를 작성합니다.

**요구사항**

- `float`, `double` 등 부동소수점 타입에서만 호출할 수 있도록 제한합니다.
- 두 인수가 모두 유한한 값일 때 `value >= limit`이면 `true`, 그 외에는 `false`를 반환합니다.
- NaN·양/음의 무한대는 유효하지 않은 입력으로 판정합니다.

**입력 조건:** 인수 `value`, `limit`의 타입은 동일한 실수 타입입니다.  **반환:** `bool`.

**예상 결과**

```text
reading_alert(85.0, 80.0) → true
reading_alert(79.9, 80.0) → false
reading_alert(NaN, 80.0) → false
```

**구현 대상:** [exercises/01_reading_alert.cpp](./exercises/01_reading_alert.cpp) · **모범답안:** [solutions/01_reading_alert.cpp](./solutions/01_reading_alert.cpp)

### Exercise 02 — Strong Quantity

거리와 시간을 모두 정수로 저장하더라도, 서로 다른 단위의 수량을 실수로 섞어 계산하지 못하도록 태그 타입(Tag Type)을 적용합니다.

**요구사항**

- `Quantity<DistanceTag>`와 `Quantity<TimeTag>`를 별도 타입으로 유지합니다.
- `value()`는 저장된 정수를 반환합니다.
- `operator+`는 같은 Tag를 가진 두 Quantity만 더하며 새 Quantity를 반환합니다.
- 서로 다른 Tag끼리 암시적으로 변환하거나 덧셈할 수 없어야 합니다.

**입력 조건:** 범위가 작은 정수를 사용하며 덧셈 오버플로 입력은 제공하지 않습니다. **반환:** 같은 Tag를 가진 `Quantity`.

**예상 결과**

```text
Quantity<DistanceTag>{10} + Quantity<DistanceTag>{15} → 25
Quantity<DistanceTag> + Quantity<TimeTag> → 컴파일 불가
```

**구현 대상:** [exercises/02_strong_quantity.cpp](./exercises/02_strong_quantity.cpp) · **모범답안:** [solutions/02_strong_quantity.cpp](./solutions/02_strong_quantity.cpp)

### Exercise 03 — Device Filter & Projection

장치 목록에서 활성화된 항목 중 측정값이 기준 이상인 장치만 선택하고, ID 오름차순으로 출력할 수 있도록 정렬합니다.

**요구사항**

- `active == true`이고 `reading >= threshold`인 장치를 선택합니다.
- 결과는 `Device::id` 기준 오름차순으로 정렬합니다.
- 원본 벡터의 순서 및 내용은 변경하지 않습니다.
- 적합한 요소가 없다면 빈 벡터를 반환합니다.

**입력 조건:** `std::vector<Device>`와 정수 `threshold`. **반환:** 새로운 `std::vector<Device>`.

**예상 결과**

```text
[B(80,true), A(90,true), C(99,false)], threshold=80
→ A, B 순서
```

**구현 대상:** [exercises/03_filter_devices.cpp](./exercises/03_filter_devices.cpp) · **모범답안:** [solutions/03_filter_devices.cpp](./solutions/03_filter_devices.cpp)

### Exercise 04 — Strict Numeric Parser

문자열을 서버 포트 번호로 변환하는 `parse_port()`를 작성합니다. 잘못된 입력은 일부만 변환하지 않고 거부합니다.

**요구사항**

- 입력이 숫자로만 구성되고 모든 문자를 소비한 경우에만 성공합니다.
- `1`부터 `65535`까지 인정하며 그 밖의 값은 거부합니다.
- 빈 문자열, 앞뒤 공백, 부호, 숫자 뒤 문자가 붙은 입력, 범위 초과를 거부합니다.
- 변환 오류에는 예외 대신 `std::nullopt`를 반환합니다.

**입력 조건:** `std::string_view`. **반환:** `std::optional<int>`.

**예상 결과**

```text
"8080" → 8080
"80x" → 없음
"0" → 없음
"65536" → 없음
```

**구현 대상:** [exercises/04_strict_parser.cpp](./exercises/04_strict_parser.cpp) · **모범답안:** [solutions/04_strict_parser.cpp](./solutions/04_strict_parser.cpp)

### 실습 실행 및 검증

`Chapter-13/` 폴더에서 아래 명령어를 실행합니다.

```bash
# 학생용 파일 전체 검증: TODO가 남아 있다면 실패하는 것이 정상입니다.
python tests/check.py --mode student --only exercises

# 모범답안 전체 검증
python tests/check.py --compiler g++-14 --mode solutions

# Clang으로 확인
python tests/check.py --compiler clang++ --mode solutions
```

테스트는 출력값 비교뿐 아니라 함수 반환값, 경계값, 정렬 결과, 타입 간 변환 가능 여부도 검사합니다. 학생용 파일을 수정한 뒤 `--mode student`로 다시 실행하면 됩니다.

<a id="section-13-19"></a>

## 13.19. Mini Project — Generic Telemetry Pipeline

### 문제 배경

서로 다른 센서 제조사에서 전달한 데이터를 한 번에 요약해야 합니다. 온도 센서는 `double`을, 압력 센서는 `float`를 사용하며 데이터 구조의 멤버 이름도 다릅니다. 모든 센서 타입별로 별도의 평균·최소·최대 계산 함수를 복사하는 대신 **공통으로 제공하는 인터페이스를 Concept로 정의하고 하나의 알고리즘으로 요약**합니다.

프로젝트는 `std::array`, `std::vector` 등 입력 Range의 구체적 종류와 센서 타입에 영향을 덜 받도록 구성합니다. 처리 중 유효하지 않은 값이 들어오더라도 해당 레코드만 제외하고 남은 데이터로 결과를 계산합니다.

### 폴더 구성

```text
Chapter-13/
├── examples/
│   └── 17_telemetry_pipeline/       # 기존 CI 호환 완성 예제
│       ├── CMakeLists.txt
│       ├── include/telemetry/
│       │   ├── pipeline.hpp
│       │   └── report.hpp
│       ├── src/
│       │   ├── main.cpp
│       │   └── report.cpp
│       └── tests/test_pipeline.cpp
├── project/                         # 학생용 시작 코드
│   └── (동일한 파일 구조)
└── solutions/telemetry_pipeline/    # 완성된 프로젝트 모범답안
    └── (동일한 파일 구조)
```

원본 GitHub Actions는 `examples/17_telemetry_pipeline/`을 직접 참조하므로 이 경로와 CMake 프로젝트 이름을 그대로 유지했습니다. 학생은 `project/`에서 구현을 시작하고, 완성 후 `solutions/telemetry_pipeline/`과 비교할 수 있습니다.

### 구현 조건

1. `ReadingLike<T>` Concept는 `value()`가 `double`로 변환 가능하고 `valid()`가 `bool`로 변환 가능하도록 정의합니다.
2. `summarize(R&& readings)`는 C++20 `std::ranges::input_range`를 받으며 범위를 한 번 순회합니다.
3. `valid() == false`, NaN, 무한대는 집계에서 제외합니다.
4. 정상 값의 개수, 최솟값, 최댓값, 평균을 계산합니다. 유효한 값이 없다면 `std::nullopt`를 반환합니다.
5. `report()`는 소수 첫째 자리까지 요약을 출력합니다.
6. 별도의 `std::array`·`std::vector` 입력과 두 종류 이상의 센서 타입에서 같은 함수가 동작해야 합니다.
7. 계산에 쓰이는 값은 실습용 센서 범위의 유한한 값으로 가정하며, 극단적인 부동소수점 오차 보정은 범위에서 제외합니다.

**출력 예시**

```text
Temperature: count=3, min=28.0, max=34.0, avg=31.3
Pressure: count=2, min=100.0, max=102.0, avg=101.0
```

### 구현 단계

- **STEP 01 — 타입 계약:** `pipeline.hpp`에서 `ReadingLike`가 요구하는 두 멤버 함수를 확인합니다. `static_assert`로 적합한 타입과 부적합한 타입을 구분합니다.
- **STEP 02 — 입력 필터링:** `summarize()`에서 `valid()`를 검사하고, `std::isfinite()`로 유효하지 않은 실수 데이터를 건너뜁니다.
- **STEP 03 — 집계:** 첫 정상 값을 기준으로 최솟값·최댓값·평균을 초기화합니다. 나머지는 한 번의 순회에서 업데이트합니다.
- **STEP 04 — 실패 표현:** 모두 거부되거나 입력이 비어 있으면 `std::nullopt`를 반환합니다.
- **STEP 05 — 검증:** 서로 다른 센서 타입, 빈 벡터, 전체 오류, NaN 포함 입력에서 테스트합니다.

### 빌드 및 실행

```bash
# 학생용 프로젝트
cmake -S project -B build/ch13-student -DCMAKE_CXX_STANDARD=20
cmake --build build/ch13-student
ctest --test-dir build/ch13-student --output-on-failure

# 완성 예제 (기존 CI 경로)
cmake -S examples/17_telemetry_pipeline -B build/ch13-ci -DCMAKE_CXX_STANDARD=20
cmake --build build/ch13-ci
ctest --test-dir build/ch13-ci --output-on-failure
```

GCC/Clang의 단일 구성 빌드에서는 `./build/ch13-ci/telemetry_demo`로 실행할 수 있습니다. Windows의 다중 구성 빌드에서는 실행 파일이 `Debug/` 또는 `Release/` 하위 폴더에 생성될 수 있고 CTest에 `-C Debug` 등을 지정해야 할 수 있습니다.

### 완료 기준

- 서로 다른 두 센서 타입으로 동일한 요약 함수를 호출할 수 있습니다.
- 유효하지 않은 행은 건수와 평균 계산에 포함되지 않습니다.
- 빈 입력에서는 값을 가진 Summary를 반환하지 않습니다.
- GCC 14·Clang에서 경고 없이 빌드되며 CTest와 자동 검사에 통과합니다.

**모범답안:** [solutions/telemetry_pipeline/](./solutions/telemetry_pipeline/) · **시작 코드:** [project/](./project/) · **기존 CI 경로:** [examples/17_telemetry_pipeline/](./examples/17_telemetry_pipeline/)

### 성능과 설계 관찰

정상 레코드 N개를 처리하는 데 한 번의 순회가 필요하므로 시간 복잡도는 `O(N)`입니다. 요약 결과를 저장하는 공간은 고정된 몇 개의 값이므로 추가 공간 복잡도는 `O(1)`입니다. 센서 데이터 자체를 담은 입력 컨테이너의 저장 공간은 제외한 설명입니다.

실제 센서 로그를 장기간 수집한다면 센서마다 다른 단위와 정상 범위, 타임스탬프, 결측 정책이 필요할 수 있습니다. 이러한 요구를 템플릿 내부에 무분별하게 넣기보다 인터페이스와 처리 정책을 분리해야 유지보수가 편해집니다.

<a id="section-13-20"></a>

## 13.20. Quiz & Summary — 점검 및 정리

### Quiz

**Q01. 함수 템플릿을 만드는 주된 이유로 가장 적절한 것은 무엇입니까?**

① 표준 알고리즘을 모두 직접 대체하기 위해서입니다.

② 여러 타입이 공유하는 처리 규칙을 한 구현으로 표현하기 위해서입니다.

③ 모든 매개변수를 런타임에 검사하기 위해서입니다.

④ 템플릿은 반드시 클래스에만 사용할 수 있기 때문입니다.

<details>
<summary>정답 및 해설</summary>

정답: **②**. 타입별로 반복되는 동작을 공통 구현으로 표현할 수 있습니다. 표준 기능의 재구현은 기본 목적이 아닙니다.

</details>

**Q02. `std::max(1, 2.5)`에 대한 설명 중 맞는 것은 무엇입니까?**

① 자동으로 `double`을 반환합니다.

② 항상 `int`로 잘립니다.

③ 기본 함수 템플릿의 타입 추론이 충돌해 컴파일되지 않습니다.

④ C++20에서만 동작합니다.

<details>
<summary>정답 및 해설</summary>

정답: **③**. 두 인수에서 같은 `T`를 추론해야 하는 기본 `std::max` 호출은 서로 다른 타입을 자동 통합하지 않습니다. `std::max<double>(1, 2.5)`는 가능합니다.

</details>

**Q03. `within_tolerance(9, 10.0, 0.2)`의 타입 추론 결과를 설명하고, 호출 가능하게 수정하세요.**

<details>
<summary>정답 및 해설</summary>

세 인수에서 `T`를 하나로 추론할 수 없으므로 컴파일되지 않습니다. `within_tolerance<double>(9, 10.0, 0.2)`처럼 타입을 지정하거나 모든 인수의 자료형을 통일할 수 있습니다.

</details>

**Q04. `std::floating_point<T>`가 보장하는 것은 무엇입니까?**

① 입력 값이 반드시 0 이상이라는 사실입니다.

② 타입이 부동소수점 계열이라는 사실입니다.

③ 값이 NaN이 아니라는 사실입니다.

④ 함수 호출이 항상 예외 없이 끝난다는 사실입니다.

<details>
<summary>정답 및 해설</summary>

정답: **②**. Concept는 타입의 조건을 표현합니다. NaN이나 허용 범위 등은 별도 데이터 검증 대상입니다.

</details>

**Q05. `ReadingLike<T>`가 `value()`와 `valid()`를 요구하는 이유를 설명하고, 이 조건만으로 센서의 값까지 검증되는지 답하세요.**

<details>
<summary>정답 및 해설</summary>

서로 다른 센서 타입에 같은 요약 함수를 적용하기 위한 호출 계약입니다. `std::convertible_to<double>`나 `std::convertible_to<bool>`는 반환 타입 변환 가능성을 확인하지만 실제 측정값의 정상 범위는 보장하지 않습니다.

</details>

**Q06. `std::array numbers{2, 4, 6}`의 타입으로 가장 알맞은 것은 무엇입니까?**

① `std::array<int, 3>`

② `std::vector<int>`

③ `std::array<double, 3>`

④ `std::array<int, 6>`

<details>
<summary>정답 및 해설</summary>

정답: **①**. CTAD로 원소 자료형 `int`와 크기 3이 추론됩니다. 크기 3은 NTTP입니다.

</details>

**Q07. `(0LL + ... + static_cast<long long>(values))`에서 `0LL`을 두는 이유를 설명하세요.**

<details>
<summary>정답 및 해설</summary>

초기값 역할을 하여 빈 팩에서도 덧셈의 결과를 0으로 정의하고 누적 결과의 시작 타입을 `long long`으로 결정합니다. 이 타입에서도 오버플로는 별도로 고려해야 합니다.

</details>

**Q08. `std::ranges::sort(devices, {}, &Device::id)`에 대한 설명 중 맞는 것은 무엇입니까?**

① 장치의 ID를 정렬 기준으로 사용합니다.

② 정렬이 안정적임을 보장합니다.

③ 원본의 순서를 절대 변경하지 않습니다.

④ 모든 Range에서 작동합니다.

<details>
<summary>정답 및 해설</summary>

정답: **①**. Projection으로 ID를 선택합니다. `std::ranges::sort()`는 안정성을 보장하지 않고, 랜덤 접근 등의 요구 조건도 존재합니다.

</details>

**Q09. `std::views::filter()`를 사용할 때 원본 데이터 수명과 결과 저장을 어떻게 고려해야 합니까?**

<details>
<summary>정답 및 해설</summary>

뷰가 원본을 소유하지 않을 수 있으므로 사용 시점까지 원본의 수명이 유지되어야 합니다. 결과를 독립적으로 보유하려면 C++20에서는 루프 등을 통해 `std::vector`에 복사할 수 있습니다.

</details>

**Q10. 전달 참조를 받는 함수에서 인수의 원래 값 범주를 유지해 다른 함수에 전달할 때 적절한 함수는 무엇입니까?**

① `std::move`

② `std::forward<T>`

③ `std::copy`

④ `std::exchange`

<details>
<summary>정답 및 해설</summary>

정답: **②**. 전달 참조를 통해 추론한 `T`를 `std::forward<T>(value)`에 전달해 lvalue/rvalue 성질을 보존합니다.

</details>

**Q11. `std::optional<int>`를 반환하는 파서가 문자열 `"80x"`를 실패로 처리해야 하는 이유를 설명하세요.**

<details>
<summary>정답 및 해설</summary>

부분적으로 80을 읽더라도 남은 `x`가 있으므로 전체 문자열이 유효한 숫자라는 계약을 만족하지 않습니다. `std::from_chars()`의 끝 포인터가 입력 끝과 같은지 확인해야 합니다.

</details>

**Q12. Mini Project에서 센서 타입이 달라도 `summarize()`를 하나만 구현할 수 있는 이유를 설명하고, 유효하지 않은 데이터 처리 방식을 제시하세요.**

<details>
<summary>정답 및 해설</summary>

Concept가 `value()`와 `valid()`라는 공통 인터페이스를 요구하고, 함수가 Range 안의 요소를 그 계약에 따라 처리하기 때문입니다. `valid()==false`이거나 변환값이 NaN/무한대인 요소를 제외하고 나머지로 최소·최대·평균을 계산합니다. 유효한 요소가 하나도 없다면 `std::nullopt`를 반환합니다.

</details>

### Summary

- 템플릿은 타입이나 컴파일 시점의 값을 받아 같은 로직을 여러 자료형에서 재사용하게 합니다.
- C++20 Concepts와 Requires Expression은 허용 가능한 타입과 연산을 인터페이스에 명확히 나타냅니다.
- Class Template, CTAD, NTTP, Fold Expression, Type Traits를 상황에 맞게 선택합니다.
- `if constexpr`와 제네릭 람다는 타입별 동작 및 표준 알고리즘을 간결하게 작성하는 데 유용합니다.
- Ranges View는 원본 수명에 주의하고, Projection은 정렬·비교 기준을 분리합니다.
- 완벽 전달에는 `std::forward<T>`를 사용하지만, 소유권과 수명에 관한 계약이 먼저입니다.
- 새 템플릿을 작성하기 전에 기존 표준 라이브러리로 해결할 수 있는지 확인합니다.

### References

- ISO/IEC 14882:2020 — *Programming languages — C++* (C++20)
- [cppreference — Templates](https://en.cppreference.com/w/cpp/language/templates)
- [cppreference — Constraints and Concepts](https://en.cppreference.com/w/cpp/language/constraints)
- [cppreference — Requires Expressions](https://en.cppreference.com/w/cpp/language/requires)
- [cppreference — Ranges Library](https://en.cppreference.com/w/cpp/ranges)
- [cppreference — Perfect Forwarding](https://en.cppreference.com/w/cpp/utility/forward)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

[← Chapter 12](../Chapter-12/README.md) · [← C++ 목차](../README.md#contents)
