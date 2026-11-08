# Chapter 07. Pointers & References

**포인터(Pointer)** 와 **참조(Reference)** 를 이용하여 기존 객체에 접근하는 방법을 학습합니다. 메모리 주소, `nullptr`, `const` 정확성, 객체 수명과 참조 무효화를 다루고, RAII 및 스마트 포인터로 소유권을 안전하게 표현하는 방법까지 확장합니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서 도입된 기능을 함께 활용하며, C++23은 필수로 요구하지 않습니다.

<details>
<summary>선행 학습</summary>

- [Chapter 02. Variables & Data Types](../Chapter-02/) — 변수·자료형·`const`
- [Chapter 03. Operators & Conditions](../Chapter-03/) — 조건문·`nullptr` 검사에 필요한 논리 연산
- [Chapter 05. Functions](../Chapter-05/) — 참조 매개변수·`std::optional`·함수 반환
- [Chapter 06. Arrays & Strings](../Chapter-06/) — `std::array`, `std::vector`, `std::span`, `std::string_view`

</details>

## Contents

| Section | Topic |
|:---:|---|
| [7.1](#section-7-1) | Objects, Addresses & Lifetime — 객체·주소·수명 |
| [7.2](#section-7-2) | Pointers & Dereferencing — 포인터와 역참조 |
| [7.3](#section-7-3) | Nullable Pointers — `nullptr` |
| [7.4](#section-7-4) | References & Function Parameters — 참조 매개변수 |
| [7.5](#section-7-5) | Const Correctness — `const` 포인터 |
| [7.6](#section-7-6) | Pointer-Based Lookup — 검색 결과 포인터 |
| [7.7](#section-7-7) | Span & Borrowed Data — `std::span` |
| [7.8](#section-7-8) | Invalidation & Dangling — 무효화와 댕글링 |
| [7.9](#section-7-9) | RAII & Unique Ownership — 자원 수명과 독점 소유권 |
| [7.10](#section-7-10) | Shared & Weak Ownership — 공유 소유와 관찰 |
| [7.11](#section-7-11) | Pointer & Length — 외부 API 경계 |
| [7.12](#section-7-12) | Reference Wrappers — 참조 래퍼 |
| [7.13](#section-7-13) | Pointer Arithmetic — 포인터 산술 |
| [7.14](#section-7-14) | Memory Diagnostics — Sanitizers |
| [7.15](#section-7-15) | API Design — 매개변수와 소유권 선택 |
| [7.16](#section-7-16) | Coding Practice |
| [7.17](#section-7-17) | Mini Project — Channel Report |
| [7.18](#section-7-18) | Quiz & Summary |


## Getting Started

명령어는 **`Chapter-07/` 폴더**에서 실행하는 경우를 기준으로 합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_addresses_and_dereference.cpp -o pointers
./pointers
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_addresses_and_dereference.cpp -o pointers
./pointers
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_addresses_and_dereference.cpp /Fe:pointers.exe
pointers.exe
```

Windows PowerShell에서는 `./pointers` 대신 `.\pointers.exe`로 실행합니다. 개발 환경 설정은 [Chapter 01](../Chapter-01/)을 참고할 수 있습니다.

**학습 목표**

1. 객체의 주소와 포인터·참조의 차이를 설명하고 안전하게 접근할 수 있습니다.
2. `nullptr`와 `const`를 이용해 함수의 입력 조건을 표현할 수 있습니다.
3. 객체 수명 및 컨테이너 재할당에 따른 포인터·참조 무효화를 설명할 수 있습니다.
4. 독점 소유와 공유 소유, 비소유 관찰을 구분할 수 있습니다.
5. `std::span`과 스마트 포인터를 적절한 상황에 선택할 수 있습니다.

---

<a id="section-7-1"></a>
## 7.1. Objects, Addresses & Lifetime — 객체·주소·수명

C++에서 **객체(Object)** 는 자료형을 가진 저장 영역으로, 생성되어 사용할 수 있는 기간을 **객체 수명(Object Lifetime)** 이라고 합니다. 객체가 있는 동안에는 주소를 이용해 접근할 수 있지만, 객체의 수명이 끝나면 그 주소를 저장한 포인터나 참조로 접근해서는 안 됩니다.

```cpp
int temperature{24};
int* pointer{&temperature};
int& reference{temperature};
```

| 표현 | 의미 |
|---|---|
| `temperature` | 정수 객체와 그 값을 사용하는 이름 |
| `&temperature` | 객체의 주소(Address)를 구하는 표현식 |
| `int* pointer` | `int`를 가리킬 수 있는 포인터 변수 |
| `int& reference` | 기존 `int` 객체에 결합한 참조 |
| `*pointer` | 포인터가 가리키는 객체에 접근하는 역참조(Dereference) |

```text
temperature ── [24]  ← int 객체
                  ↑
pointer ─────────┘      주소를 저장
reference ───────┘      같은 객체를 다른 이름으로 참조
```

포인터와 참조는 **원본 객체를 자동으로 소유하거나 원본 수명을 연장하지 않습니다.** 이 Chapter의 중요한 기준은 단순히 주소를 얻는 방법이 아니라 **언제까지 접근해도 되는지** 판단하는 것입니다.

참고로 실제 주소는 실행마다 달라질 수 있으므로 주소의 숫자 자체에 의미를 부여하지 않습니다.

<a id="section-7-2"></a>
## 7.2. Pointers & Dereferencing — 포인터와 역참조

포인터는 **대상이 되는 객체의 주소를 담는 값**입니다. 선언에서는 `*`가 포인터 타입을 나타내고, 표현식에서는 `*`가 가리키는 객체에 접근하는 연산자로 쓰입니다. 같은 기호라도 위치에 따라 역할이 다릅니다.

```cpp
int value{10};
int* ptr{&value};  // 포인터 선언 및 주소 저장
*ptr = 20;        // 역참조를 통한 원본 변경
```

`ptr`에 다른 주소를 대입하면 포인터가 가리키는 대상이 바뀌지만, `*ptr = 20`은 **포인터가 아니라 원본 객체**를 변경합니다. 여러 포인터 선언은 `int* first, second;`처럼 쓰면 `second`만 정수 타입이므로, 각각 한 줄씩 선언하는 편이 오해를 줄입니다.

**예제 코드 — [01_addresses_and_dereference.cpp](./examples/01_addresses_and_dereference.cpp)**

```cpp
#include <iostream>

int main() {
    int temperature{24};
    int* reading{&temperature};
    std::cout << "Original: " << temperature << " C\n";
    *reading = 26;
    std::cout << "Updated: " << temperature << " C\n";
    std::cout << std::boolalpha;
    std::cout << "Same object: " << (reading == &temperature) << '\n';
}
```

**실행 결과**

```text
Original: 24 C
Updated: 26 C
Same object: true
```

`reading`과 `temperature`는 별개 정수를 저장하는 관계가 아닙니다. `reading`이 `temperature`를 가리키므로 역참조를 통해 수정한 값이 원본에도 반영됩니다. `std::boolalpha`는 `bool` 결과를 `1`·`0` 대신 `true`·`false`로 출력합니다(Chapter 02 참고).

**주의:** 초기화하지 않은 포인터를 역참조하면 안 됩니다. 즉시 연결할 객체가 없다면 `int* p{nullptr};`로 시작합니다.

<a id="section-7-3"></a>
## 7.3. Nullable Pointers — `nullptr`

**널 포인터(Null Pointer)** 는 가리키는 대상이 없음을 나타내며, C++에서는 `nullptr`로 표현합니다. 장치 검색 실패처럼 결과가 없을 수 있는 함수에는 포인터가 자연스러운 선택입니다.

- `ptr == nullptr`: 대상이 없다고 명시한 경우
- `ptr != nullptr`: 널 포인터는 아님. 그러나 원본의 **수명이 유효하다는 보장까지 의미하지는 않음**
- `*nullptr`: 허용되지 않는 역참조

필수 인수처럼 대상이 반드시 존재해야 하는 경우에는 `T&` 또는 `const T&`가 더 적절할 수 있습니다.

**예제 코드 — [02_nullable_pointer.cpp](./examples/02_nullable_pointer.cpp)**

```cpp
#include <iostream>

void print_temperature(const int* reading) {
    if (reading == nullptr) {
        std::cout << "No sensor reading\n";
        return;
    }
    std::cout << "Sensor: " << *reading << " C\n";
}

int main() {
    const int measured{23};
    print_temperature(&measured);
    print_temperature(nullptr);
}
```

**실행 결과**

```text
Sensor: 23 C
No sensor reading
```

`print_temperature()`는 대상을 읽기만 하므로 `const int*`를 받습니다. 함수가 `nullptr`을 처리한 후에만 역참조하는 순서를 확인하세요. `nullptr`이 아닌 **댕글링 포인터(Dangling Pointer)** 는 이 검사만으로 걸러지지 않습니다.

<a id="section-7-4"></a>
## 7.4. References & Function Parameters — 참조 매개변수

**참조(Reference)** 는 이미 존재하는 객체에 결합한 이름입니다. 일반적인 `T&` 참조는 선언 시 초기화해야 하며, 포인터처럼 `nullptr`을 저장하거나 다른 객체로 다시 결합할 수 없습니다.

```cpp
int first{10};
int second{20};
int& ref{first};
ref = second;  // ref가 second를 가리키게 되는 것이 아니라 first에 20을 대입함
```

함수의 인수 전달 방식은 목적에 따라 선택합니다.

| 매개변수 | 사용 목적 | 호출자 원본 변경 |
|---|---|:---:|
| `int value` | 작은 값 복사 | X |
| `const int& value` | 원본을 읽되 수정하지 않음 | X |
| `int& value` | 반드시 존재하는 원본 수정 | O |
| `int* value` | 수정할 대상이 없을 수도 있음 | 가능 |

`int&`는 값 전달과 달리 원본을 수정할 수 있다는 장점이 있지만, 변경이 필요한 작업에만 사용해야 함수의 동작을 예측하기 쉽습니다.

**예제 코드 — [03_reference_parameters.cpp](./examples/03_reference_parameters.cpp)**

```cpp
#include <iostream>

[[nodiscard]] bool try_set_rpm(int& current, int requested) noexcept {
    if (requested < 0 || requested > 3'000) {
        return false;
    }
    current = requested;
    return true;
}

int main() {
    int rpm{1'200};
    const bool first{try_set_rpm(rpm, 2'500)};
    const bool second{try_set_rpm(rpm, 4'000)};
    std::cout << std::boolalpha;
    std::cout << "First: " << first << '\n';
    std::cout << "Second: " << second << '\n';
    std::cout << "Motor: " << rpm << " RPM\n";
}
```

**실행 결과**

```text
First: true
Second: false
Motor: 2500 RPM
```

`try_set_rpm(int& current, int requested)`는 허용 범위인 `0~3000`일 때만 원본 값을 갱신합니다. 두 번째 요청이 실패해도 처음 성공한 `2500`이 유지됩니다. `[[nodiscard]]`는 반환값을 무시할 때 컴파일러 진단을 유도하는 속성으로, Chapter 05에서 학습했습니다.

<a id="section-7-5"></a>
## 7.5. Const Correctness — `const` 포인터

`const`는 타입을 통해 **어떤 경로에서 객체를 수정할 수 있는지** 표현합니다. 포인터에서 `const`가 가리키는 대상에 적용되는지, 포인터 변수 자체에 적용되는지 구분해야 합니다.

| 선언 | `*p`를 통한 값 수정 | `p`에 새 주소 대입 |
|---|:---:|:---:|
| `int* p` | 가능 | 가능 |
| `const int* p` | 불가능 | 가능 |
| `int* const p` | 가능 | 불가능 |
| `const int* const p` | 불가능 | 불가능 |

`const int*`가 반드시 `const` 객체만 가리킬 수 있다는 뜻은 아닙니다. **그 포인터를 통해서는 수정하지 못한다**는 뜻입니다. 반대로 `int* const`는 포인터가 **다른 대상을 가리키지 못하지만**, 현재 대상의 값은 수정할 수 있습니다.

**예제 코드 — [04_const_correctness.cpp](./examples/04_const_correctness.cpp)**

```cpp
#include <iostream>

int main() {
    int speed{120};
    int backup{80};
    const int* read_only{&speed};
    read_only = &backup;
    int* const fixed_target{&speed};
    *fixed_target = 130;
    const int* const fixed_read_only{&speed};

    std::cout << "Backup: " << *read_only << '\n';
    std::cout << "Speed: " << *fixed_target << '\n';
    std::cout << "Read-only speed: " << *fixed_read_only << '\n';
}
```

**실행 결과**

```text
Backup: 80
Speed: 130
Read-only speed: 130
```

`read_only`는 `backup`으로 대상을 바꾸고, `fixed_target`은 `speed`를 130으로 변경합니다. `fixed_read_only`는 대상을 바꿀 수도 없고 해당 포인터를 통해 값을 바꿀 수도 없습니다.

`const`를 제거하기 위한 무리한 형변환보다 처음부터 함수의 읽기·쓰기 요구사항에 맞춰 타입을 선언하는 편이 안전합니다.

<a id="section-7-6"></a>
## 7.6. Pointer-Based Lookup — 검색 결과 포인터

함수가 **기존 컨테이너의 요소를 찾아 반환**할 때, 새 객체를 복사하지 않고 해당 요소의 주소를 반환할 수 있습니다. 검색 결과가 없다면 `nullptr`을 반환하도록 합니다.

```cpp
const std::string* found = find_device(devices, "camera");
```

이러한 반환 포인터는 **비소유(Non-Owning)** 입니다. 문자열을 새로 생성하지 않고, 원본 `std::vector`와 요소의 수명에 의존합니다. 함수 호출 직후에는 유효하더라도 벡터를 파괴하거나 재할당하면 기존 주소를 사용할 수 없을 수 있습니다.

**예제 코드 — [05_pointer_lookup.cpp](./examples/05_pointer_lookup.cpp)**

```cpp
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

[[nodiscard]] const std::string* find_device(
    const std::vector<std::string>& devices, std::string_view target) {
    for (const auto& device : devices) {
        if (device == target) {
            return &device;
        }
    }
    return nullptr;
}

int main() {
    const std::vector<std::string> devices{"lidar", "camera", "imu"};
    if (const auto* found = find_device(devices, "camera")) {
        std::cout << "Found: " << *found << '\n';
    }
    std::cout << std::boolalpha;
    std::cout << "Missing: " << (find_device(devices, "gps") == nullptr) << '\n';
}
```

**실행 결과**

```text
Found: camera
Missing: true
```

반환형이 `const std::string*`이므로 호출자는 발견한 문자열을 읽을 수 있지만 그 포인터를 통해 수정하지는 못합니다. 검색 실패 시 `nullptr`을 반환하며, 호출자는 이를 검사한 뒤에만 역참조합니다.

여기서 `<string_view>`는 비교용 문자열을 소유하지 않고 전달하는 `std::string_view`를 제공하며, `<vector>`는 장치 목록을 소유하는 `std::vector`를 제공합니다(Chapter 06).

<a id="section-7-7"></a>
## 7.7. Span & Borrowed Data — `std::span`

**`std::span<T>`** 는 연속된 요소들의 시작 위치와 길이를 묶어서 전달하는 C++20의 비소유 뷰입니다. 데이터는 복사하거나 소유하지 않지만, 호출자가 길이를 따로 전달하는 포인터 기반 인터페이스보다 범위의 의미를 명확하게 표현할 수 있습니다.

| 타입 | 의미 |
|---|---|
| `std::span<int>` | 기존 연속 데이터의 값을 수정할 수 있는 뷰 |
| `std::span<const int>` | 기존 연속 데이터를 읽는 뷰 |
| `samples.size()` | 요소의 개수 확인 |
| `samples.empty()` | 빈 범위인지 확인 |

**`#include <span>`** 은 `std::span`을 선언하며, `std::optional`이 필요한 경우 **`#include <optional>`** 을 사용합니다. `std::optional<T>`는 정상 값의 유무를 구분하는 반환 타입으로 Chapter 05에서 다뤘습니다.

**예제 코드 — [06_span_parameter.cpp](./examples/06_span_parameter.cpp)**

```cpp
#include <array>
#include <iomanip>
#include <iostream>
#include <optional>
#include <span>
#include <vector>

[[nodiscard]] std::optional<double> average(std::span<const int> values) {
    if (values.empty()) {
        return std::nullopt;
    }
    double total{};
    for (const int value : values) {
        total += value;
    }
    return total / static_cast<double>(values.size());
}

int main() {
    const std::array fixed{10, 20, 30};
    const std::vector dynamic{40, 50, 60};
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Fixed: " << *average(fixed) << '\n';
    std::cout << "Dynamic: " << *average(dynamic) << '\n';
    std::cout << std::boolalpha;
    std::cout << "Empty: " << !average(std::span<const int>{}) << '\n';
}
```

**실행 결과**

```text
Fixed: 20.0
Dynamic: 50.0
Empty: true
```

동일한 `average()` 함수에 `std::array`와 `std::vector`를 전달합니다. 빈 구간에서는 평균이 정의되지 않으므로 임의의 0 대신 `std::nullopt`를 반환합니다. `*average(fixed)`는 해당 배열이 비어 있지 않아 결과가 존재한다는 전제에서만 사용합니다.

`std::span`은 수명을 관리하지 않으며, C++20의 `operator[]`는 자동으로 범위를 검사하지 않습니다. 전달하는 데이터가 살아 있는지, 인덱스가 유효한지를 별도로 보장해야 합니다.

<a id="section-7-8"></a>
## 7.8. Invalidation & Dangling — 무효화와 댕글링

**댕글링(Dangling)** 은 포인터나 참조가 가리키던 객체가 이미 사라졌거나 더 이상 유효하지 않은 상태를 말합니다. null 상태와는 다릅니다. 원본이 없어진 후에도 포인터에 과거 주소값이 남아 있을 수 있습니다.

```cpp
// 잘못된 예시: 지역 변수의 주소를 반환하면 수명 종료 후 무효화됨.
int* invalid_address() {
    int local{10};
    return &local;
}
```

위 코드는 **실행하면 안 되는 반례**입니다. 주소를 반환하는 대신 `int` 값을 반환하는 식으로 설계를 변경해야 합니다.

또한 `std::vector`가 내부 저장 공간을 재할당(Reallocation)하면 기존 요소의 주소·참조·반복자가 무효화됩니다. `push_back()`이 매번 재할당하는 것은 아니지만, **재할당이 일어나지 않는다고 가정하면 안 됩니다.**

**예제 코드 — [07_vector_invalidation.cpp](./examples/07_vector_invalidation.cpp)**

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings{10, 20};
    const std::size_t selected_index{1};
    readings.push_back(30);
    if (selected_index < readings.size()) {
        // Do not reuse pointers or references saved before a possible reallocation.
        std::cout << "Selected: " << readings.at(selected_index) << '\n';
    }
    std::cout << "Size: " << readings.size() << '\n';
}
```

**실행 결과**

```text
Selected: 20
Size: 3
```

이 예제는 요소를 추가하기 전에 저장한 포인터를 계속 사용하지 않습니다. 인덱스 `selected_index`를 보관하고, 추가 작업 이후 `at()`으로 다시 접근합니다. 단, 중간 삽입·삭제로 요소 순서가 바뀌면 같은 인덱스가 다른 요소를 가리킬 수 있으므로 **인덱스는 영구적인 객체 ID가 아닙니다.**

**정의되지 않은 동작(Undefined Behavior, UB)** 은 프로그램의 결과가 언어 표준에 의해 보장되지 않는 상황을 뜻합니다. 실행 중 바로 오류가 발생하지 않더라도 안전하다는 증거는 아닙니다.

<a id="section-7-9"></a>
## 7.9. RAII & Unique Ownership — 자원 수명과 독점 소유권

**RAII(Resource Acquisition Is Initialization)** 는 자원을 획득한 객체의 수명에 맞춰 자원이 해제되도록 설계하는 방식입니다. 메모리뿐 아니라 파일, 잠금, 네트워크 연결 등 다양한 자원을 다룰 때 중요합니다. 자세한 예외 안전성과 자원 관리 설계는 Chapter 12에서 확장합니다.

`std::unique_ptr<T>`는 관리 대상 객체에 대한 **독점 소유권(Unique Ownership)** 을 표현합니다. 일반적으로 `std::make_unique<T>(...)`로 생성하며, 소유자가 사라지면 관리 대상 객체가 정리됩니다.

- **`#include <memory>`**: `std::unique_ptr`, `std::shared_ptr`, `std::weak_ptr` 등 스마트 포인터 제공
- **`#include <utility>`**: `std::move()` 제공
- **`std::move(x)`**: 객체를 곧바로 이동시키는 함수가 아니라, 이동을 허용하도록 표현식을 변환하는 기능. 실제 이동은 받는 타입의 이동 연산으로 수행

`unique_ptr`는 복사할 수 없으나 이동할 수 있습니다. 이동한 후 원래 `unique_ptr`는 비어 있습니다.

**예제 코드 — [08_unique_ptr.cpp](./examples/08_unique_ptr.cpp)**

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <utility>

int main() {
    auto owner = std::make_unique<std::string>("sensor-A");
    std::unique_ptr<std::string> current{std::move(owner)};
    std::cout << std::boolalpha;
    std::cout << "Previous owner empty: " << (owner == nullptr) << '\n';
    if (current) {
        std::cout << "Current device: " << *current << '\n';
    }
}
```

**실행 결과**

```text
Previous owner empty: true
Current device: sensor-A
```

`std::move(owner)`를 사용해 관리 대상의 소유권을 `current`로 이전합니다. 이후 `owner`는 `nullptr`이므로 역참조할 수 없습니다. 대상 `std::string`은 여전히 `current`가 소유하고 있으며, `current`가 수명을 마치면 정리됩니다.

```cpp
// 일반적인 C++ 코드에서는 아래처럼 수동 삭제를 직접 관리하기보다
// auto owner = std::make_unique<int>(42);  // 이 방식을 우선 고려합니다.
int* raw = new int{42};
delete raw;
```

`new`와 `delete` 자체가 잘못된 문법은 아니지만, 여러 종료 경로에서 정리를 누락하거나 중복 해제하는 문제가 생기기 쉽습니다. 일반적인 자원 소유 표현에는 스마트 포인터·표준 컨테이너·지역 객체를 먼저 고려합니다.

<a id="section-7-10"></a>
## 7.10. Shared & Weak Ownership — 공유 소유와 관찰

`std::shared_ptr<T>`는 여러 소유자가 **동일한 객체의 수명**을 관리해야 할 때 사용합니다. 마지막 공유 소유자가 사라지면 관리 대상이 정리됩니다. 반면 `std::weak_ptr<T>`는 공유 소유 대상의 **비소유 관찰(Weak Observation)** 에 사용합니다.

| 타입 | 대상 수명에 대한 책임 | 대표 사용 상황 |
|---|---|---|
| `std::unique_ptr<T>` | 한 소유자만 관리 | 단일 소유자가 명확할 때 |
| `std::shared_ptr<T>` | 여러 소유자가 공동 관리 | 실제로 공동 수명 보장이 필요할 때 |
| `std::weak_ptr<T>` | 소유권 추가하지 않음 | 이미 공유된 객체를 관찰할 때 |
| `T*`, `T&` | 보통 소유하지 않음 | 이미 수명이 보장된 객체를 잠시 사용할 때 |

`weak_ptr.lock()`은 대상이 살아 있으면 `shared_ptr`를 반환하여 **그 `shared_ptr`가 살아 있는 동안** 수명을 보장합니다. 이미 소멸했으면 비어 있는 `shared_ptr`를 반환합니다.

**예제 코드 — [09_shared_and_weak_ptr.cpp](./examples/09_shared_and_weak_ptr.cpp)**

```cpp
#include <iostream>
#include <memory>
#include <string>

int main() {
    auto owner = std::make_shared<std::string>("navigation-map");
    std::weak_ptr<std::string> observer{owner};
    if (const auto active = observer.lock()) {
        std::cout << "Active: " << *active << '\n';
    }
    owner.reset();
    std::cout << std::boolalpha;
    std::cout << "Expired: " << observer.expired() << '\n';
}
```

**실행 결과**

```text
Active: navigation-map
Expired: true
```

`observer.lock()`의 결과로 만든 `active`가 `if` 블록 끝에서 소멸합니다. 이후 유일한 소유자인 `owner`에 `reset()`을 호출하면 대상 문자열이 정리되고 `expired()`는 `true`입니다.

**주의:** 두 객체가 서로를 `shared_ptr`로 소유하면 참조 횟수가 0이 되지 않는 **소유권 순환(Ownership Cycle)** 이 생길 수 있습니다. 소유하지 않아야 할 역방향 관계에 `weak_ptr`를 고려하세요. `shared_ptr`는 비용이 없는 만능 포인터가 아니므로 실제 공유 소유가 필요한 경우에 선택합니다.

<a id="section-7-11"></a>
## 7.11. Pointer & Length — 외부 API 경계

C 라이브러리나 일부 외부 장치 API는 버퍼를 **포인터와 길이(Pointer + Length)** 로 전달합니다. 이때 `data != nullptr`라는 사실만으로 실제 버퍼가 해당 길이만큼 유효하다고 판단할 수는 없습니다.

```cpp
void process(const unsigned char* data, std::size_t length);
```

호출자가 해당 개수의 요소를 제공하고 함수가 접근하는 동안 메모리가 유효하다는 **호출 계약(Contract)** 이 필요합니다. C++ 코드 내부에서는 유효성이 보장된 뒤 `std::span`으로 묶어 다룰 수 있습니다.

- **`#include <cstdint>`**: `std::uint8_t` 등 고정 폭 정수형 제공(해당 폭을 지원하는 환경)
- **`#include <cstddef>`**: 배열 길이에 사용하는 `std::size_t` 제공
- **`#include <iterator>`**: C 배열의 요소 수를 구하는 `std::size()` 제공

아래 예제는 **정상적인 고정 배열에서 호출한 짧은 버퍼**를 전제로 합계를 계산합니다. 큰 버퍼의 누적값 오버플로를 고려해야 하는 경우에는 별도 범위 검사 또는 더 적합한 계산 정책이 필요합니다.

**예제 코드 — [10_pointer_and_length_boundary.cpp](./examples/10_pointer_and_length_boundary.cpp)**

```cpp
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <iterator>
#include <optional>
#include <span>

[[nodiscard]] std::optional<unsigned long long> sum_bytes(
    const std::uint8_t* data, std::size_t length) {
    if (data == nullptr && length != 0) {
        return std::nullopt;
    }
    if (length == 0) {
        return 0ULL;
    }
    // Caller must guarantee a valid buffer with at least 'length' elements.
    const std::span<const std::uint8_t> bytes{data, length};
    unsigned long long total{};
    for (const std::uint8_t value : bytes) {
        total += value;
    }
    return total;
}

int main() {
    const std::uint8_t bytes[]{1, 2, 3, 4};
    std::cout << "Checksum sum: " << *sum_bytes(bytes, std::size(bytes)) << '\n';
    std::cout << std::boolalpha;
    std::cout << "Invalid: " << !sum_bytes(nullptr, 4) << '\n';
}
```

**실행 결과**

```text
Checksum sum: 10
Invalid: true
```

`nullptr`과 4라는 길이를 함께 전달하는 호출은 실패 결과로 처리합니다. 길이 0은 유효한 빈 입력으로 정의합니다. 하지만 널이 아닌 **잘못된 주소나 거짓 길이**를 받으면 함수 내부에서 안전성을 알아서 복원할 수 없습니다. 따라서 원본 버퍼의 유효성은 호출자가 보장해야 합니다.

여기서 출력한 값은 바이트의 단순 합계이며, 네트워크 오류 탐지에 사용하는 완전한 체크섬(Checksum) 알고리즘은 아닙니다.

<a id="section-7-12"></a>
## 7.12. Reference Wrappers — 참조 래퍼

일반적인 참조는 변수를 선언할 때 결합해야 하고, 다른 대상에 재결합할 수 없습니다. 참조 자체를 `std::vector<int&>`의 요소로 직접 저장할 수도 없습니다. 대신 `std::reference_wrapper<T>`로 **참조를 보관할 수 있는 객체**를 만들 수 있습니다.

- **`#include <functional>`**: `std::reference_wrapper`, `std::ref()` 제공
- **`std::ref(value)`**: 기존 객체를 소유하지 않는 참조 래퍼 생성
- **`wrapper.get()`**: 래퍼가 결합한 원본 객체에 접근

참조 래퍼도 원본 객체의 수명에 의존합니다.

**예제 코드 — [11_reference_wrapper.cpp](./examples/11_reference_wrapper.cpp)**

```cpp
#include <functional>
#include <iostream>
#include <vector>

int main() {
    int front_rpm{1'000};
    int rear_rpm{1'200};
    std::vector<std::reference_wrapper<int>> motors{
        std::ref(front_rpm), std::ref(rear_rpm)
    };
    for (int& rpm : motors) {
        rpm += 100;
    }
    std::cout << "Front: " << front_rpm << '\n';
    std::cout << "Rear: " << rear_rpm << '\n';
}
```

**실행 결과**

```text
Front: 1100
Rear: 1300
```

`motors`는 RPM 값 자체를 복사해서 저장한 배열이 아니라, `front_rpm`과 `rear_rpm`에 결합된 참조 래퍼의 벡터입니다. 반복문에서 수정한 값이 원본 두 변수에 반영됩니다.

### 선택적 참조(Optional Reference)

C++20에서는 `std::optional<T&>`를 사용할 수 없습니다. 검색 성공 시 **원본을 수정할 수 있는 참조**를 선택적으로 반환하려면 `T*` 또는 `std::optional<std::reference_wrapper<T>>`를 고려할 수 있습니다. 후자는 단순한 `T*`보다 타입이 길지만 값의 유무를 `std::optional`로 표현합니다.

**예제 코드 — [12_optional_reference.cpp](./examples/12_optional_reference.cpp)**

```cpp
#include <functional>
#include <iostream>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

[[nodiscard]] std::optional<std::reference_wrapper<std::string>>
find_mutable(std::vector<std::string>& devices, std::string_view target) {
    for (auto& device : devices) {
        if (device == target) {
            return std::ref(device);
        }
    }
    return std::nullopt;
}

int main() {
    std::vector<std::string> devices{"camera", "lidar"};
    if (auto found = find_mutable(devices, "lidar")) {
        found->get() = "lidar-front";
    }
    std::cout << "Renamed: " << devices.at(1) << '\n';
}
```

**실행 결과**

```text
Renamed: lidar-front
```

일치하는 원본 문자열을 래퍼로 반환하고, `found->get()`을 통해 기존 벡터 요소를 수정합니다. 이 결과를 벡터의 재할당이나 삭제 이후까지 보관하면 무효화될 수 있으므로 장기 보관용 식별자와 혼동하지 마세요.

<a id="section-7-13"></a>
## 7.13. Pointer Arithmetic — 포인터 산술

포인터 산술(Pointer Arithmetic)은 배열 안의 요소를 순서대로 가리키는 저수준 연산입니다.

```cpp
int values[]{10, 20, 30};
int* first{values};       // 첫 요소
int* second{first + 1};  // 두 번째 요소
int* end{first + 3};     // 끝 바로 다음 위치

// *second == 20
// *end는 허용되지 않는 역참조입니다.
```

`first + 3`은 같은 배열의 **끝 바로 다음 위치(One-Past-the-End)** 로서 비교 등에 사용할 수 있지만, 그 위치를 역참조하면 안 됩니다. **유효한 배열의 범위를 벗어나는 포인터 산술 자체도 일반적으로 허용되지 않습니다.**

포인터끼리 빼서 거리를 계산하는 경우에도 동일한 배열 범위를 전제로 합니다. 대부분의 데이터 처리는 직접 산술을 작성하는 것보다 범위 기반 `for`, `std::span`, 표준 알고리즘을 사용하는 편이 읽기 쉽고 안전합니다.

<a id="section-7-14"></a>
## 7.14. Memory Diagnostics — Sanitizers

컴파일이 성공했다고 해서 객체 수명이나 버퍼 접근이 항상 안전한 것은 아닙니다. 메모리 오류를 찾기 위해 **AddressSanitizer(ASan)**, 일부 정의되지 않은 동작을 찾기 위해 **UndefinedBehaviorSanitizer(UBSan)** 를 활용할 수 있습니다.

정상 동작하는 예제로도 Sanitizer가 활성화된 빌드를 확인해 볼 수 있습니다.

**예제 코드 — [13_sanitizer_safe_example.cpp](./examples/13_sanitizer_safe_example.cpp)**

```cpp
#include <array>
#include <iostream>
#include <span>

[[nodiscard]] int first_or_default(std::span<const int> samples,
                                   int fallback) noexcept {
    return samples.empty() ? fallback : samples.front();
}

int main() {
    const std::array<int, 3> samples{10, 20, 30};
    const std::span<const int> empty{};
    std::cout << "First: " << first_or_default(samples, -1) << '\n';
    std::cout << "Empty: " << first_or_default(empty, -1) << '\n';
}
```

**실행 결과**

```text
First: 10
Empty: -1
```

비어 있는 `std::span`에 `front()`를 호출하지 않고, `empty()`를 검사해 기본값을 반환합니다. `front()`는 비어 있는 범위에서 사용할 수 없습니다.

**GCC / Clang — 메모리 검사**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic \
  -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer \
  examples/13_sanitizer_safe_example.cpp -o sanitizer_demo
./sanitizer_demo
```

| 옵션 | 역할 |
|---|---|
| `-g` | 오류 위치를 확인하기 위한 디버그 정보 포함 |
| `-O1` | 낮은 수준의 최적화 적용 |
| `-fsanitize=address,undefined` | ASan 및 UBSan 검사 코드 추가 |
| `-fno-omit-frame-pointer` | 호출 경로 추적에 도움 |

Sanitizer는 **모든** 수명 오류나 논리 오류를 발견하는 것은 아닙니다. 지원 여부와 실행 환경도 다르므로 컴파일러와 운영체제에 맞는 옵션을 확인해야 합니다.

| 잘못된 상황 | 가능한 문제 | 예방 방법 |
|---|---|---|
| `nullptr` 역참조 | 잘못된 메모리 접근 | 사용 전 확인 및 필수 인수 설계 |
| 지역 변수 주소를 함수 밖으로 반환 | 댕글링 포인터 | 값 반환·수명 보장된 객체 사용 |
| 벡터 재할당 후 기존 요소 주소 사용 | 무효화된 객체 접근 | 재할당 후 주소 다시 획득 |
| `new` 후 `delete` 누락·중복 | 누수·이중 해제 | RAII·스마트 포인터 |
| `span`에서 잘못된 인덱스 사용 | 범위 밖 접근 | 인덱스와 길이 검증 |
| `shared_ptr`끼리 순환 소유 | 자원 정리 실패 | 비소유 관계에 `weak_ptr` 사용 |

<a id="section-7-15"></a>
## 7.15. API Design — 매개변수와 소유권 선택

함수를 설계할 때 **대상이 필수인지**, **원본을 수정하는지**, **함수가 소유권을 가지는지**를 구분하면 적절한 매개변수와 반환형을 선택하기 쉽습니다.

| 요구사항 | 우선 고려할 타입 | 예시 |
|---|---|---|
| 작은 값을 독립적으로 전달 | `T` | `int rpm` |
| 필수 객체를 읽기만 함 | `const T&` | `const Config& config` |
| 필수 객체를 수정 | `T&` | `int& current_rpm` |
| 대상이 없어도 됨 | `T*`, `const T*` | 선택된 센서 포인터 |
| 연속된 데이터를 읽음 | `std::span<const T>` | `std::span<const int> samples` |
| 연속된 데이터를 수정 | `std::span<T>` | `std::span<int> readings` |
| 문자열을 짧게 읽음 | `std::string_view` | `std::string_view name` |
| 객체의 독점 소유권 | `std::unique_ptr<T>` | 단독 소유 장치 자원 |
| 여러 주체의 공유 소유 | `std::shared_ptr<T>` | 실제 공유 수명 관리 |
| 공유 객체를 비소유 관찰 | `std::weak_ptr<T>` | 등록된 객체의 상태 관찰 |

일반적인 값·컨테이너를 무조건 포인터로 바꾸는 것이 목적은 아닙니다. **누가 객체를 생성·보관하고 언제까지 접근하는가**가 자료형 선택의 핵심 기준입니다.

---

<a id="section-7-16"></a>
## 7.16. Coding Practice

`exercises/`에는 함수의 핵심 로직을 직접 구현하도록 일부가 비어 있는 시작 코드가 있습니다. `solutions/`에는 모범답안을 제공합니다. 입력과 출력 부분은 제공되므로 **포인터·참조·소유권 개념의 구현**에 집중하세요.

| 번호 | 실습 | 시작 코드 | 모범답안 |
|:---:|---|---|---|
| 01 | Motor Limit — 참조로 모터 속도 변경 | [01_motor_limit.cpp](./exercises/01_motor_limit.cpp) | [01_motor_limit.cpp](./solutions/01_motor_limit.cpp) |
| 02 | Sensor Average — `std::span`으로 평균 계산 | [02_sensor_average.cpp](./exercises/02_sensor_average.cpp) | [02_sensor_average.cpp](./solutions/02_sensor_average.cpp) |
| 03 | Device Lookup — 검색 결과 포인터 | [03_device_lookup.cpp](./exercises/03_device_lookup.cpp) | [03_device_lookup.cpp](./solutions/03_device_lookup.cpp) |
| 04 | Shared Observer — 공유 소유권과 관찰 | [04_shared_observer.cpp](./exercises/04_shared_observer.cpp) | [04_shared_observer.cpp](./solutions/04_shared_observer.cpp) |

### Exercise 01 — Motor Limit

`try_set_rpm(int& current, int requested)` 함수를 완성합니다.

**구현 조건**

1. 요청 RPM이 `0~3000`이면 참조로 전달된 원본을 변경하고 `true` 반환
2. 범위를 벗어나면 원본 값을 변경하지 않고 `false` 반환
3. `2500`과 `4000` 요청을 연속으로 적용한 후 상태 확인

**기대 출력**

```text
First: true, Second: false, RPM: 2500
```

**학습 포인트:** 함수 인수 `int&`를 통한 수정, 실패 시 원본 상태 보존.

### Exercise 02 — Sensor Average

`average(std::span<const int>)` 함수를 완성합니다.

**구현 조건**

1. 비어 있으면 `std::nullopt` 반환
2. 유효한 값이 있다면 `double` 평균 반환
3. 원본 배열을 수정하지 않고 평균 계산

**기대 출력**

```text
Average: 25.0
Empty: true
```

**학습 포인트:** 연속 데이터의 비소유 읽기와 결과가 없는 경우의 처리.

### Exercise 03 — Device Lookup

`find_device()`에서 벡터의 문자열을 찾아 기존 요소의 주소를 반환합니다.

**구현 조건**

1. 이름이 처음 일치하는 요소의 주소 반환
2. 검색 결과가 없으면 `nullptr` 반환
3. 원본 컨테이너를 복사하거나 변경하지 않음

**기대 출력**

```text
Found: imu
Missing: true
```

**학습 포인트:** 주소 반환과 결과 포인터의 수명.

### Exercise 04 — Shared Observer

`std::shared_ptr`가 소유하는 객체를 `std::weak_ptr`로 관찰합니다.

**구현 조건**

1. `sensor-hub` 문자열을 공유 소유하는 객체 생성(시작 코드 제공)
2. `std::weak_ptr`를 이용해 소유권을 추가하지 않고 관찰
3. `lock()`으로 접근한 문자열 출력
4. 마지막 공유 소유자를 `reset()`으로 해제
5. `expired()`로 소멸 여부 출력

**기대 출력**

```text
Active: sensor-hub
Expired: true
```

**학습 포인트:** `lock()`의 반환값도 객체를 소유하므로 임시 `shared_ptr`의 수명을 고려해야 함.

### Coding Practice 실행 및 검사

`Chapter-07/` 위치에서 직접 작성한 파일을 컴파일할 수 있습니다.

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/01_motor_limit.cpp -o motor_limit
./motor_limit
```

모범답안은 `exercises/`를 `solutions/`로 바꿔 컴파일합니다. 아래 테스트 실행기는 **Python 3**로 실행하며, 테스트하는 C++ 파일은 설정된 컴파일러로 실제 컴파일합니다.

```bash
python tests/check.py
python tests/check.py --exercise 01
```

첫 번째 명령어는 전체 예제·모범답안·완성 프로젝트를 검증합니다. 두 번째 명령어는 수정한 Exercise 01을 검사합니다. 실습 파일을 아직 완성하지 않았다면 일부 검증이 실패하는 것이 정상입니다.

---

<a id="section-7-17"></a>
## 7.17. Mini Project — Channel Report

### Channel Report — 채널 측정값 검사

3개 채널의 측정값을 배열에 저장하고 사용자가 선택한 채널을 수정한 뒤 통계를 출력하는 프로그램을 구현합니다. **주소 반환·참조 매개변수·`std::span`** 을 하나의 프로젝트에서 연결합니다.

**파일 구성**

- [시작 코드 — channel_report.cpp](./project/channel_report.cpp)
- [모범답안 — channel_report.cpp](./solutions/channel_report.cpp)

시작 코드에는 입력 및 범위 검증과 출력 구조가 제공됩니다. 다음 세 함수를 직접 완성합니다.

| 함수 | 구현 내용 |
|---|---|
| `select_channel(std::span<int>, int)` | `1~3` 채널의 원본 요소 주소 반환, `0` 또는 잘못된 채널은 `nullptr` |
| `apply_adjustment(int&, int)` | 변경 결과가 `0~100` 범위 안이면 원본 수정·`true` 반환, 아니면 변경하지 않고 `false` 반환 |
| `average_reading(std::span<const int>)` | 원본을 수정하지 않고 평균 계산. 빈 범위는 이 프로젝트에서 `0.0`으로 정의 |

**입력 조건**

- 측정값: 3개, 각각 정수 `0~100`
- 선택 채널: `0~3` (`0`은 선택하지 않음)
- 보정값: 정수 `-20~20`
- 보정 후에도 측정값은 `0~100` 이내여야 함

**실행 예시 — 정상 보정**

```text
Readings (3 values, 0-100): 25 83 47
Channel (0-3): 2
Adjustment (-20 to 20): -5

--- Channel Report ---
Selected: 2
Before: 83
After: 78
Average: 50.00
Status: NORMAL
```

선택한 두 번째 채널은 `83 → 78`로 변경됩니다. 평균은 **보정 후** 세 측정값의 평균인 `(25 + 78 + 47) / 3 = 50.00`입니다. 선택한 채널이 `80` 이상이면 `ALERT`, 그렇지 않으면 `NORMAL`을 출력합니다.

**실행 예시 — 채널 미선택**

```text
Readings (3 values, 0-100): 20 30 40
Channel (0-3): 0
Adjustment (-20 to 20): 10

--- Channel Report ---
Selected: NONE
Average: 30.00
Status: NO CHANNEL
```

채널 `0`은 보정하지 않고 평균만 계산합니다. 인덱스 `0`인 첫 번째 채널과 혼동하지 마세요.

**오류 사례**

| 입력 조건 | 처리 |
|---|---|
| 측정값이 `-1` 또는 `101` | `Error: reading out of range.` |
| 채널이 `-1` 또는 `4` | `Error: invalid channel.` |
| 보정값이 `-21` 또는 `21` | `Error: invalid adjustment.` |
| 보정 후 채널 값이 `0~100`을 벗어남 | `Error: adjusted reading out of range.` |
| 필요한 위치에 숫자가 아닌 값 입력 | 해당 단계에서 오류 출력 및 종료 |

각 오류는 `std::cerr`로 출력하고 `1`을 반환합니다. 입력 단계의 검증은 시작 코드에서 제공하므로 세 함수의 올바른 동작에 집중합니다. 위 프로그램은 장치와 실제 통신하지 않는 콘솔 시뮬레이션입니다.

**컴파일 및 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/channel_report.cpp -o channel_report
./channel_report
```

**완료 기준**

1. 잘못된 채널 번호를 역참조하지 않고 `nullptr`로 구분합니다.
2. 보정 실패 시 원본 값을 변경하지 않습니다.
3. 평균이 모든 채널의 보정 후 상태를 반영합니다.
4. `0~100` 경계값과 선택 채널이 없는 경우를 처리합니다.
5. 다음 명령어로 실습 파일을 검증합니다.

```bash
python tests/check.py --project
```

완성된 정답과 전체 예제만 검증하려면 `python tests/check.py`를 실행합니다.

---

<a id="section-7-18"></a>
## 7.18. Quiz & Summary

### Quiz

각 문제의 정답과 해설을 펼쳐서 확인할 수 있습니다.

**Q1.** 다음 중 `int* p{&value};`의 `p`에 대한 설명으로 올바른 것은 무엇인가요?

- A. `value`의 사본을 담은 정수 변수입니다.
- B. `value` 객체의 주소를 담는 포인터 변수입니다.
- C. `value`와 같은 이름을 갖는 참조 변수입니다.
- D. `value`의 수명을 자동으로 연장합니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

`p`는 `value`를 가리킬 수 있는 포인터로, 주소를 저장합니다. `*p`로 접근하면 원본 객체를 읽거나 수정할 수 있습니다. 값 복사(A)나 참조 선언(C)과 다르며, 포인터는 원본의 수명을 관리하지 않으므로 D도 틀립니다.

</details>

**Q2.** `int value{10}; int* p{&value}; *p = 20;`을 실행하면 `value`는 얼마가 되나요? 왜 그런가요?

<details>
<summary>정답 및 해설</summary>

**정답: 20**

`*p`는 포인터가 가리키는 원본 객체를 나타내는 역참조 표현식입니다. `p`가 `value`를 가리키므로 `*p = 20;`은 `value = 20;`과 동일한 객체를 수정합니다.

</details>

**Q3.** `p != nullptr`이면 반드시 `*p`를 안전하게 사용할 수 있나요?

- A. 그렇습니다. 널 검사로 모든 수명 오류가 사라집니다.
- B. 아닙니다. 객체가 이미 소멸한 포인터도 널이 아닐 수 있습니다.
- C. 그렇습니다. 포인터가 널이 아니라면 항상 소유권도 있습니다.
- D. 널 포인터는 언제나 안전하게 역참조할 수 있습니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

널 검사는 **대상이 없음을 나타내는 값**을 걸러내는 데 필요합니다. 하지만 객체 수명이 끝났거나 컨테이너 재할당으로 무효화된 주소가 널이 아닐 수도 있습니다. A·C·D는 수명·소유권·역참조의 조건을 혼동한 선택지입니다.

</details>

**Q4.** `const int* p`와 `int* const p`의 차이를 설명해 보세요.

<details>
<summary>정답 및 해설</summary>

**모범답안:** `const int* p`는 `p`를 통해 원본 값을 수정할 수 없지만, 다른 객체를 가리키게 변경할 수 있습니다. `int* const p`는 포인터 자체가 고정되어 다른 주소로 변경할 수 없지만, `*p`로 원본 값을 수정할 수 있습니다.

`const int* const p`는 두 제한을 모두 갖습니다. 포인터의 `const`는 **수정하려는 대상이 포인터 자체인지 가리키는 값인지** 구분해서 읽어야 합니다.

</details>

**Q5.** `try_set_rpm(int& rpm, int requested)`에서 범위 검사에 실패한 경우 원본 `rpm`을 보존하려면 어떤 순서로 작성하는 것이 좋은가요?

<details>
<summary>정답 및 해설</summary>

**모범답안:** 요청값의 범위를 먼저 검사하고, 유효하지 않다면 `return false;`로 종료한 뒤 **성공 경로에서만** `rpm = requested;`를 실행합니다.

참조 매개변수는 원본을 직접 변경하므로 검증 전에 대입하면 실패 시에도 호출자의 상태가 바뀔 수 있습니다. 범위 검사를 먼저 하는 가드 절 방식이 이 경우에 적합합니다.

</details>

**Q6.** `std::span<const int>`에 관한 설명 중 옳은 것은 무엇인가요?

- A. 전달받은 배열을 항상 복사합니다.
- B. 원본 데이터를 자동으로 소유합니다.
- C. 요소 수 정보를 포함하는 비소유 연속 데이터 뷰입니다.
- D. 인덱스의 범위를 벗어나도 항상 예외가 발생합니다.

<details>
<summary>정답 및 해설</summary>

**정답: C**

`std::span`은 연속 데이터의 범위를 비소유 방식으로 표현하며, 값들을 복사해 저장하지 않습니다. `const int`는 해당 뷰를 통한 요소 수정을 제한합니다. C++20의 `operator[]`는 범위 검사를 보장하지 않으므로 D도 틀립니다.

</details>

**Q7.** `std::vector`의 `push_back()` 이후 이전에 저장한 요소 포인터를 바로 쓰면 위험할 수 있는 이유는 무엇인가요?

<details>
<summary>정답 및 해설</summary>

**모범답안:** 요소를 추가하는 과정에서 벡터 내부 저장 공간이 **재할당(Reallocation)** 될 수 있기 때문입니다. 재할당이 발생하면 기존 요소의 주소가 바뀌고 이전 포인터·참조·반복자가 무효화됩니다.

항상 재할당하는 것은 아니지만 코드가 이를 가정해서는 안 됩니다. 필요한 경우 변경 이후 유효한 인덱스를 검증해 다시 접근할 수 있습니다.

</details>

**Q8.** `std::unique_ptr<T>`에 대해 올바른 설명은 무엇인가요?

- A. 복사와 이동이 모두 기본적으로 허용됩니다.
- B. 반드시 수동으로 `delete` 해야 합니다.
- C. 독점 소유권을 나타내고, `std::move`를 이용해 소유권 이전에 사용할 수 있습니다.
- D. 여러 소유자가 참조 횟수를 공동 관리합니다.

<details>
<summary>정답 및 해설</summary>

**정답: C**

`unique_ptr`는 독점 소유권을 표현합니다. 복사는 허용되지 않고 이동은 가능합니다. 관리 객체의 자원 정리는 소유자의 수명과 연동됩니다. D는 `shared_ptr`의 특징입니다.

</details>

**Q9.** `std::move(owner)`를 호출한 것만으로 자원 이동이 반드시 수행되나요?

<details>
<summary>정답 및 해설</summary>

**정답: 아니요.**

`std::move` 자체는 이동을 허용하도록 표현식을 변환하는 역할을 합니다. 실제 이동은 해당 값을 받는 객체의 이동 생성자 또는 이동 대입 연산이 수행합니다. 예를 들어 `std::unique_ptr<T> next{std::move(owner)};`에서 소유권이 이전됩니다.

</details>

**Q10.** `std::weak_ptr`로 관찰한 객체를 사용하기 위한 안전한 방법은 무엇인가요?

- A. `weak_ptr`를 직접 역참조합니다.
- B. `lock()`으로 `shared_ptr`를 얻고, 유효한 경우 사용합니다.
- C. 항상 원시 포인터로 변환한 뒤 사용합니다.
- D. `expired()`가 `true`일 때 역참조합니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

`weak_ptr`는 소유권을 갖지 않으므로 객체가 이미 정리되었을 수 있습니다. `lock()`이 반환하는 `shared_ptr`가 유효하면 그 객체를 사용하는 동안 수명이 보장됩니다. `expired()`가 `true`이면 대상이 소멸한 상태입니다.

</details>

**Q11.** 외부 함수에 `const unsigned char* data, std::size_t length`를 전달할 때 `data != nullptr`라는 사실만으로 안전성을 확인할 수 있나요?

<details>
<summary>정답 및 해설</summary>

**정답: 확인할 수 없습니다.**

주소가 널이 아니어도 실제 버퍼가 존재하는지, 전달한 길이만큼의 요소를 포함하는지, 접근하는 동안 수명이 유지되는지까지 자동으로 알 수는 없습니다. 포인터와 길이를 올바르게 제공한다는 호출 계약이 필요합니다. `std::span`으로 변환하는 것만으로 외부의 잘못된 주소가 안전해지는 것도 아닙니다.

</details>

**Q12.** Mini Project의 `select_channel()` 함수가 채널 번호 `0`을 받았습니다. 어떤 결과를 반환하는 것이 적절하며, 그 후 어떤 접근을 피해야 하나요?

<details>
<summary>정답 및 해설</summary>

**모범답안:** 채널 `0`은 **선택하지 않음**을 의미하므로 `nullptr`을 반환합니다. 호출자는 결과가 널인지 확인하고, 널인 경우에는 `*selected` 같은 역참조를 수행하면 안 됩니다.

유효한 채널 `1~3`은 배열 인덱스 `0~2`와 대응되므로, 선택 범위를 확인한 후 `&readings[channel - 1]` 형태로 해당 요소의 주소를 반환합니다.

</details>

### Summary

| 핵심 개념 | 요약 |
|---|---|
| 포인터 `T*` | 객체 주소를 가리키며 `nullptr`을 표현할 수 있음 |
| 참조 `T&` | 기존 객체에 결합하여 원본에 접근함 |
| `const` 정확성 | 읽기 전용 접근과 포인터 자체 변경 제한을 구분함 |
| 객체 수명 | 원본 소멸 또는 재할당 후 포인터·참조를 재사용하지 않음 |
| `std::span` | 연속 데이터의 비소유 뷰, 크기와 수명을 따로 고려함 |
| RAII | 자원을 소유하는 객체의 수명과 정리를 연결함 |
| `std::unique_ptr` | 하나의 소유자가 관리, 소유권 이동 가능 |
| `std::shared_ptr` | 여러 소유자가 대상 수명을 공동 관리함 |
| `std::weak_ptr` | 공유 소유권을 늘리지 않고 존재 여부를 관찰함 |
| Sanitizer | 특정 메모리 오류·정의되지 않은 동작을 찾는 보조 도구 |

### References

- [cppreference — Pointers](https://en.cppreference.com/w/cpp/language/pointer)
- [cppreference — References](https://en.cppreference.com/w/cpp/language/reference)
- [cppreference — Object lifetime](https://en.cppreference.com/w/cpp/language/lifetime)
- [cppreference — `std::span`](https://en.cppreference.com/w/cpp/container/span)
- [cppreference — `std::unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [cppreference — `std::shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr)
- [cppreference — `std::weak_ptr`](https://en.cppreference.com/w/cpp/memory/weak_ptr)
- [C++ Core Guidelines — Resource management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource)
- [Clang — AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)

---

[← C++ 목차](../README.md#contents) · [이전 Chapter — Arrays & Strings](../Chapter-06/) · [다음 Chapter — Classes](../Chapter-08/)

