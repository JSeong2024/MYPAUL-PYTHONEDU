# Chapter 08. Structs & Classes

**구조체(Struct)** 와 **클래스(Class)** 를 이용해 여러 데이터를 하나의 자료형으로 묶고, 객체가 유효한 상태를 유지하도록 설계하는 방법을 학습합니다. 생성자, 접근 제어, 멤버 함수, 객체 합성, 복사·이동, 헤더와 구현 파일 분리를 통해 기능과 데이터를 함께 관리합니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서 도입된 기능을 함께 사용하며, C++23 기능은 기본 예제의 필수 조건으로 사용하지 않습니다.

<details>
<summary>선행 학습</summary>

- [Chapter 02. Variables & Data Types](../Chapter-02/) — 초기화·`const`·자료형
- [Chapter 05. Functions](../Chapter-05/) — 선언·정의·매개변수·`std::optional`
- [Chapter 06. Arrays & Strings](../Chapter-06/) — `std::string`, `std::vector`, 기본 검색
- [Chapter 07. Pointers & References](../Chapter-07/) — 객체 수명·참조·스마트 포인터·`std::move()`

</details>

## Contents

| Section | Topic |
|:---:|---|
| [8.1](#section-8-1) | Struct vs. Class — 구조체와 클래스의 차이 |
| [8.2](#section-8-2) | Struct & Data Members — 구조체와 멤버 |
| [8.3](#section-8-3) | Aggregate Initialization — 집합체와 지정 초기화자 |
| [8.4](#section-8-4) | Encapsulation & Invariants — 접근 제어와 유효 상태 |
| [8.5](#section-8-5) | Constructors & `explicit` — 생성자와 명시적 변환 |
| [8.6](#section-8-6) | Member Initializer List — 멤버 초기화 목록 |
| [8.7](#section-8-7) | Const Member Functions — 읽기 전용 멤버 함수 |
| [8.8](#section-8-8) | Validated Construction — 팩토리 함수와 `std::optional` |
| [8.9](#section-8-9) | Delegating Constructors — 위임 생성자 |
| [8.10](#section-8-10) | Composition — 객체 합성 |
| [8.11](#section-8-11) | Static Members & Destructors — 정적 멤버와 소멸자 |
| [8.12](#section-8-12) | Defaulted Equality — 객체의 동등 비교 |
| [8.13](#section-8-13) | `this` & Method Chaining — 현재 객체와 연속 호출 |
| [8.14](#section-8-14) | Multi-File Class Design — 헤더와 구현 파일 분리 |
| [8.15](#section-8-15) | Copy, Move & Rule of Zero — 복사·이동과 자원 관리 |
| [8.16](#section-8-16) | Class Design Guidelines — 클래스 설계 원칙 |
| [8.17](#section-8-17) | Coding Practice — 연습문제 |
| [8.18](#section-8-18) | Mini Project — Device Inventory |
| [8.19](#section-8-19) | Quiz & Summary — 점검 및 정리 |

## Getting Started

다음 명령어는 **`Chapter-08/` 폴더**에서 실행하는 경우를 기준으로 합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_struct_record.cpp -o struct_demo
./struct_demo
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_struct_record.cpp -o struct_demo
./struct_demo
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_struct_record.cpp /Fe:struct_demo.exe
struct_demo.exe
```

Windows PowerShell에서는 `./struct_demo` 대신 `.\struct_demo.exe`를 실행합니다. 컴파일러 설정은 [Chapter 01](../Chapter-01/)을 참고할 수 있습니다.

**학습 목표**

1. `struct`와 `class`의 기본 접근 권한 및 용도를 구분할 수 있습니다.
2. 생성자와 멤버 초기화를 통해 올바른 객체 상태를 만들 수 있습니다.
3. `private` 멤버와 공개 멤버 함수로 상태 변경 규칙을 지킬 수 있습니다.
4. 객체 합성과 클래스 기반 API를 구현할 수 있습니다.
5. 헤더·구현 파일을 분리해 컴파일하고, 클래스 메서드를 테스트할 수 있습니다.

---

<a id="section-8-1"></a>
## 8.1. Struct vs. Class — 구조체와 클래스의 차이

C++의 **사용자 정의 자료형(User-Defined Type)** 은 개발자가 여러 데이터와 동작을 하나의 타입으로 정의하는 기능입니다. `struct`와 `class`는 모두 멤버 변수, 멤버 함수, 생성자를 선언할 수 있습니다. 문법적으로 핵심적인 차이는 **기본 접근 권한(Default Access)** 입니다.

| 구분 | `struct` | `class` |
|---|---|---|
| 기본 멤버 접근 권한 | `public` | `private` |
| 기본 상속 접근 권한 | `public` | `private` |
| 멤버 함수·생성자 | 사용 가능 | 사용 가능 |
| 일반적인 사용 | 데이터 묶음·간단한 값 표현 | 상태 보호·검증·동작 제공 |

```cpp
struct Position {
    int x{};
    int y{};
};

class Counter {
public:
    void increment() noexcept { ++count_; }
    [[nodiscard]] int value() const noexcept { return count_; }

private:
    int count_{};
};
```

`Position`은 공개된 두 좌표를 함께 전달하는 데이터 구조이고, `Counter`는 외부에서 `count_`를 직접 수정하지 않고 `increment()`로 변경하도록 설계한 클래스입니다.

**객체(Object)** 는 이러한 자료형으로 생성한 실제 값입니다. `Counter counter;`에서 `Counter`는 타입이고 `counter`는 객체입니다. `struct`가 항상 작거나 빠르거나 C 언어와 바이너리 호환된다는 뜻은 아닙니다.

<a id="section-8-2"></a>
## 8.2. Struct & Data Members — 구조체와 멤버

**멤버(Member)** 는 구조체·클래스에 포함된 변수 또는 함수를 말합니다. 예를 들어 센서 측정 시각, 장치 이름, 측정값, 연결 상태를 함께 묶으면 관련 데이터를 함수에 하나의 객체로 전달할 수 있습니다.

`std::string`은 문자열을 저장하는 표준 라이브러리 타입이고, `<string>` 헤더에서 제공합니다. `.`은 객체의 멤버에 접근하는 **멤버 접근 연산자(Member Access Operator)** 입니다.

다음 `SensorReading`은 데이터를 모으는 구조체이므로, 사용자가 멤버를 직접 읽을 수 있도록 `public` 상태로 둡니다.

**예제 코드 — [01_struct_record.cpp](./examples/01_struct_record.cpp)**

```cpp
#include <iostream>
#include <string>

struct SensorReading {
    std::string device_id;
    double temperature_c{};
    bool online{};
};

int main() {
    const SensorReading reading{"TEMP-A", 23.5, true};
    std::cout << std::boolalpha;
    std::cout << reading.device_id << ": " << reading.temperature_c
              << " C (online: " << reading.online << ")\n";
}
```

**실행 결과**

```text
TEMP-A: 23.5 C (online: true)
```

- `device_id`는 장치 식별자를 보관합니다.
- `temperature_c{}`와 `online{}`은 생략 시 각각 `0.0`, `false`로 초기화됩니다.
- `SensorReading reading{"TEMP-A", 23.5, true};`는 멤버 선언 순서대로 초기화합니다.
- `std::boolalpha`는 `bool` 값을 `1`·`0` 대신 `true`·`false`로 출력합니다. 반대로 `std::noboolalpha`를 사용하면 기본 숫자 출력 방식으로 돌아갑니다.

장치 식별자 중복이나 측정 범위가 중요하다면 단순 공개 구조체만으로는 충분하지 않습니다. 이 경우 검증하는 멤버 함수 또는 별도 클래스를 설계합니다.

<a id="section-8-3"></a>
## 8.3. Aggregate Initialization — 집합체와 지정 초기화자

**집합체 초기화(Aggregate Initialization)** 는 집합체(Aggregate)의 멤버를 중괄호로 초기화하는 방식입니다. 대표적인 예로 공개 데이터 멤버를 가진 단순 구조체가 있습니다.

```cpp
struct Point { int x; int y; };
const Point p{3, 5};
```

C++20의 **지정 초기화자(Designated Initializer)** 는 `.멤버명 = 값` 형태로 어떤 값이 어느 멤버에 들어가는지 명시합니다. 단, C++에서는 **멤버 선언 순서대로** 지정해야 하며, 모든 클래스에 사용할 수 있는 문법은 아닙니다.

`<cstdint>`는 `std::uint32_t`와 `std::uint16_t`처럼 너비가 지정된 정수형을 제공합니다. 해당 타입은 플랫폼이 지원하는 경우 정의됩니다. 아래 예제에서는 메시지 번호와 데이터 크기를 표현합니다.

**예제 코드 — [02_designated_initializers.cpp](./examples/02_designated_initializers.cpp)**

```cpp
#include <cstdint>
#include <iostream>

struct PacketHeader {
    std::uint32_t message_id{};
    std::uint16_t payload_bytes{};
    bool encrypted{false};
};

int main() {
    const PacketHeader header{
        .message_id = 42,
        .payload_bytes = 128,
        .encrypted = true
    };
    std::cout << std::boolalpha;
    std::cout << "Packet " << header.message_id << ": "
              << header.payload_bytes << " bytes, encrypted: "
              << header.encrypted << '\n';
}
```

**실행 결과**

```text
Packet 42: 128 bytes, encrypted: true
```

`message_id`, `payload_bytes`, `encrypted`를 선언 순서대로 지정했으며 `true`는 암호화 여부를 나타내는 학습용 상태값입니다. 이 구조체를 네트워크 패킷의 실제 바이트 배열로 그대로 취급해서는 안 됩니다. 컴파일러의 정렬·패딩, 바이트 순서와 실제 직렬화 형식은 별도로 고려해야 합니다.

```cpp
// 잘못된 지정 순서: encrypted가 message_id보다 먼저 나옵니다.
// PacketHeader wrong{.encrypted = true, .message_id = 42};
```

<a id="section-8-4"></a>
## 8.4. Encapsulation & Invariants — 접근 제어와 유효 상태

**접근 지정자(Access Specifier)** 는 멤버를 외부에서 사용할 수 있는지 결정합니다. **캡슐화(Encapsulation)** 는 데이터와 그 데이터를 처리하는 동작을 하나로 묶고, 불필요한 내부 상태 변경을 제한하는 설계 원칙입니다.

| 지정자 | 역할 |
|---|---|
| `public` | 외부에서 사용할 수 있는 공개 인터페이스 |
| `private` | 클래스 내부와 접근이 허용된 코드에서만 사용할 수 있는 멤버 |
| `protected` | 클래스 및 파생 클래스에서 접근할 수 있는 멤버. 상속은 Chapter 09에서 학습합니다. |

**클래스 불변식(Class Invariant)** 은 객체가 유지해야 하는 유효 상태의 규칙입니다. 모터 RPM이 항상 `0~3000`이어야 한다면, 멤버를 공개하기보다 범위를 확인하는 함수를 제공하는 편이 안전합니다.

**예제 코드 — [03_encapsulation.cpp](./examples/03_encapsulation.cpp)**

```cpp
#include <iostream>

class Motor {
public:
    [[nodiscard]] bool set_rpm(int requested) noexcept {
        if (requested < 0 || requested > 3'000) {
            return false;
        }
        rpm_ = requested;
        return true;
    }

    [[nodiscard]] int rpm() const noexcept { return rpm_; }

private:
    int rpm_{};
};

int main() {
    Motor motor;
    const bool accepted{motor.set_rpm(1'500)};
    const bool rejected{motor.set_rpm(4'000)};
    std::cout << std::boolalpha << "Accepted: " << accepted
              << ", rejected: " << rejected
              << ", RPM: " << motor.rpm() << '\n';
}
```

**실행 결과**

```text
Accepted: true, rejected: false, RPM: 1500
```

`set_rpm(1500)`은 성공하여 상태를 바꾸지만 `set_rpm(4000)`은 실패하고 기존 `1500`을 유지합니다. `[[nodiscard]]`는 반환값을 무시하면 컴파일러가 진단하도록 권고하는 C++ 속성이고, `noexcept`는 함수에서 예외가 밖으로 전파되지 않는다는 계약을 나타냅니다. `rpm() const`는 읽기 전용 멤버 함수입니다.

**중요:** `private`로 숨기는 것만으로 값이 자동 검증되는 것은 아닙니다. 클래스가 공개하는 *모든* 상태 변경 경로에서 동일한 규칙을 지켜야 합니다.

<a id="section-8-5"></a>
## 8.5. Constructors & `explicit` — 생성자와 명시적 변환

**생성자(Constructor)** 는 객체를 만드는 과정에서 초기 상태를 설정하는 특별한 멤버 함수입니다. 클래스 이름과 같고 반환 타입을 작성하지 않습니다. 객체가 처음부터 사용할 수 있는 상태를 갖도록 만들 때 사용합니다.

```cpp
class Sensor {
public:
    explicit Sensor(int id) : id_{id} {}
private:
    int id_{};
};
```

단일 인수로 호출 가능한 생성자는 다른 값에서 해당 클래스로의 암묵적 변환(Implicit Conversion)을 허용할 수 있습니다. 이런 변환을 원하지 않을 때는 **`explicit`** 를 붙입니다. `explicit`는 입력 유효성을 검증하는 기능은 아닙니다.

**예제 코드 — [04_explicit_constructor.cpp](./examples/04_explicit_constructor.cpp)**

```cpp
#include <cstdint>
#include <iostream>

class DeviceId {
public:
    explicit DeviceId(std::uint32_t value) noexcept : value_{value} {}

    [[nodiscard]] std::uint32_t value() const noexcept { return value_; }

private:
    std::uint32_t value_{};
};

void print_device(DeviceId id) {
    std::cout << "Device ID: " << id.value() << '\n';
}

int main() {
    const DeviceId id{1'024};
    print_device(id);
    // print_device(1024); // explicit이므로 암묵적 변환은 허용되지 않음.
}
```

**실행 결과**

```text
Device ID: 1024
```

`DeviceId id{1024};`처럼 타입을 명시해 객체를 생성해야 합니다. `print_device(1024)`는 암묵적 변환이 제한되므로 컴파일되지 않지만, `print_device(DeviceId{1024})`는 허용됩니다.

다른 종류의 값이 같은 정수로 표현되더라도, 타입을 분리하면 잘못된 값 전달을 컴파일 단계에서 줄이는 데 도움이 됩니다.

<a id="section-8-6"></a>
## 8.6. Member Initializer List — 멤버 초기화 목록

**멤버 초기화 목록(Member Initializer List)** 은 생성자 본문보다 먼저 멤버를 직접 초기화합니다. 다음 두 형식을 구분해야 합니다.

```cpp
// 기본 멤버 초기화자: 생성자에서 지정하지 않았을 때 사용할 기본값
int attempts_{3};

// 멤버 초기화 목록: 생성자 호출 시 넘긴 값으로 멤버를 직접 초기화
// Device(int channel) : channel_{channel} {}
```

`const` 멤버, 참조 멤버, 기본 생성자가 없는 멤버 객체 등은 본문에 들어와 대입하는 것으로 초기화를 대신할 수 없으므로 특히 중요합니다. `<utility>`의 `std::move()`는 객체를 이동 가능한 표현식으로 바꾸며, 실제 이동 여부는 해당 타입의 생성자에 따릅니다.

**예제 코드 — [05_member_initialization.cpp](./examples/05_member_initialization.cpp)**

```cpp
#include <iostream>
#include <string>
#include <utility>

struct RetryOptions {
    int attempts{3};
    int delay_ms{250};
};

class Device {
public:
    Device(std::string name, int channel)
        : name_{std::move(name)}, channel_{channel} {}

    void print() const {
        std::cout << name_ << " on channel " << channel_ << '\n';
    }

private:
    std::string name_;
    int channel_{};
};

int main() {
    const RetryOptions options{};
    const Device sensor{"LIDAR", 2};
    std::cout << "Retries: " << options.attempts
              << ", delay: " << options.delay_ms << " ms\n";
    sensor.print();
}
```

**실행 결과**

```text
Retries: 3, delay: 250 ms
LIDAR on channel 2
```

`name_`은 `std::string` 멤버이고 `channel_`은 정수 멤버입니다. `name_{std::move(name)}`으로 전달받은 문자열의 내용을 이동 생성자에 넘길 수 있습니다.

**초기화 순서:** 멤버 초기화 목록에 적힌 순서가 아니라 클래스 내부에서 **멤버가 선언된 순서**로 초기화됩니다. 순서에 의존하는 표현을 피하고, 목록도 선언 순서에 맞게 작성하는 것이 좋습니다.

<a id="section-8-7"></a>
## 8.7. Const Member Functions — 읽기 전용 멤버 함수

멤버 함수 선언 뒤의 `const`는 해당 함수에서 일반적인 비정적 멤버를 수정하지 않겠다는 제한입니다. 이를 **상수 정확성(Const Correctness)** 이라고 합니다. `const T&`로 전달받은 객체에서도 조회용 멤버 함수를 호출할 수 있도록, 상태를 변경하지 않는 메서드에는 `const`를 붙입니다.

```cpp
[[nodiscard]] int count() const noexcept;
```

`const` 멤버 함수와 `const` 매개변수는 다른 개념입니다. 전자는 현재 객체를 통한 수정을 제한하고, 후자는 지정한 인수의 수정을 제한합니다.

**예제 코드 — [06_const_member_functions.cpp](./examples/06_const_member_functions.cpp)**

```cpp
#include <iostream>

class SampleCounter {
public:
    void record() noexcept { ++count_; }
    [[nodiscard]] int count() const noexcept { return count_; }

private:
    int count_{};
};

void print_count(const SampleCounter& counter) {
    std::cout << "Samples: " << counter.count() << '\n';
}

int main() {
    SampleCounter counter;
    counter.record();
    counter.record();
    print_count(counter);
}
```

**실행 결과**

```text
Samples: 2
```

`record()`는 `count_`를 변경하지만 `count() const`는 값을 읽기만 합니다. `print_count(const SampleCounter& counter)`가 원본 객체를 복사하지 않고 조회할 수 있는 이유이기도 합니다.

단, `const`가 객체 밖의 모든 상태나 포인터로 연결된 다른 객체까지 자동으로 변경 불가능하게 만드는 것은 아닙니다.

<a id="section-8-8"></a>
## 8.8. Validated Construction — 팩토리 함수와 `std::optional`

생성자가 유효하지 않은 인수를 받는 상황을 생각해 봅니다. 예를 들어 온도 범위는 하한이 상한보다 클 수 없고, `NaN`이나 무한대는 정상적인 한계값으로 처리해서는 안 됩니다.

**팩토리 함수(Factory Function)** 는 객체를 만드는 과정을 함수로 감싸 검증을 수행하는 방식입니다. 결과가 존재할 수도 없을 수도 있음을 표현하는 **`std::optional<T>`** 는 `<optional>` 헤더에서 제공하는 C++17 기능입니다. 결과가 없을 때는 `std::nullopt`를 반환합니다.

`<cmath>`의 `std::isfinite()`는 실수가 유한한 값인지 검사합니다. C++23의 `std::expected<T, E>`는 실패 사유까지 보관할 수 있지만, 여기서는 C++20에서 사용 가능한 `std::optional`에 집중합니다.

**예제 코드 — [07_optional_factory.cpp](./examples/07_optional_factory.cpp)**

```cpp
#include <cmath>
#include <iostream>
#include <optional>

class TemperatureWindow {
public:
    [[nodiscard]] static std::optional<TemperatureWindow>
    create(double low, double high) noexcept {
        if (!std::isfinite(low) || !std::isfinite(high) || low > high) {
            return std::nullopt;
        }
        return TemperatureWindow{low, high};
    }

    [[nodiscard]] bool contains(double temperature) const noexcept {
        return std::isfinite(temperature) &&
               low_ <= temperature && temperature <= high_;
    }

private:
    TemperatureWindow(double low, double high) noexcept
        : low_{low}, high_{high} {}

    double low_{};
    double high_{};
};

int main() {
    const auto window = TemperatureWindow::create(18.0, 26.0);
    const auto invalid = TemperatureWindow::create(30.0, 10.0);
    std::cout << std::boolalpha;
    std::cout << "23 C allowed: " << (window && window->contains(23.0)) << '\n';
    std::cout << "Invalid range rejected: " << !invalid << '\n';
}
```

**실행 결과**

```text
23 C allowed: true
Invalid range rejected: true
```

- 생성자가 `private`이므로 외부에서 검증을 건너뛰고 임의의 `TemperatureWindow`를 직접 만들 수 없습니다.
- `create()`는 검증에 성공하면 객체를 반환하고, 실패하면 `std::nullopt`를 반환합니다.
- `window && window->contains(23.0)`은 먼저 결과의 존재 여부를 확인합니다. 이때 `->`는 선택적 결과 내부의 객체에 멤버 접근을 수행합니다.
- `contains()`도 검사값의 유한성을 확인하므로 `NaN`을 정상 범위에 포함하지 않습니다.

**주의:** `optional`은 실패했는지 여부는 알 수 있지만, *왜 실패했는지*는 담지 않습니다. 오류 사유가 필요하면 반환 타입을 따로 설계해야 합니다.

<a id="section-8-9"></a>
## 8.9. Delegating Constructors — 위임 생성자

**위임 생성자(Delegating Constructor)** 는 같은 클래스에 정의된 다른 생성자를 호출하여 초기화 로직을 재사용합니다. 기본값만 다른 생성자를 여러 개 만들 때 초기화 작업을 한 곳에 모을 수 있습니다.

```cpp
explicit Sensor(std::string name) : Sensor{std::move(name), 100} {}
```

이 선언은 전달받은 이름과 기본 임계값 `100`을 사용해 두 번째 생성자로 초기화를 위임합니다.

**예제 코드 — [08_delegating_constructor.cpp](./examples/08_delegating_constructor.cpp)**

```cpp
#include <iostream>
#include <string>
#include <utility>

class Sensor {
public:
    explicit Sensor(std::string name) : Sensor{std::move(name), 100} {}

    Sensor(std::string name, int threshold)
        : name_{std::move(name)}, threshold_{threshold} {}

    void print() const {
        std::cout << name_ << ": threshold " << threshold_ << '\n';
    }

private:
    std::string name_;
    int threshold_{};
};

int main() {
    const Sensor first{"Temperature"};
    const Sensor second{"Vibration", 80};
    first.print();
    second.print();
}
```

**실행 결과**

```text
Temperature: threshold 100
Vibration: threshold 80
```

위임하는 생성자의 초기화 목록에는 다른 멤버 초기화를 함께 작성할 수 없습니다. 위임받은 생성자가 객체를 초기화하고 돌아오면 위임하는 생성자의 본문이 실행됩니다.

<a id="section-8-10"></a>
## 8.10. Composition — 객체 합성

**객체 합성(Composition)** 은 하나의 클래스가 다른 클래스의 객체를 멤버로 포함하는 관계입니다. 로봇이 배터리를 **가지고 있다(Has-a)** 라고 설명할 수 있습니다. 이러한 관계는 장치의 구성 요소와 역할을 나누는 데 유용합니다.

`Robot`이 에너지 소비량을 직접 관리하기보다, 배터리 변경 규칙을 가진 `Battery` 객체에 작업을 맡기면 책임이 분명해집니다.

**예제 코드 — [09_composition.cpp](./examples/09_composition.cpp)**

```cpp
#include <iostream>

class Battery {
public:
    explicit Battery(int percent) noexcept : percent_{percent} {}

    [[nodiscard]] bool consume(int amount) noexcept {
        if (amount < 0 || amount > percent_) {
            return false;
        }
        percent_ -= amount;
        return true;
    }

    [[nodiscard]] int percent() const noexcept { return percent_; }

private:
    int percent_{};
};

class Robot {
public:
    explicit Robot(int charge) noexcept : battery_{charge} {}

    [[nodiscard]] bool move(int meters) noexcept {
        if (meters <= 0 || meters > 100) {
            return false;
        }
        return battery_.consume((meters + 4) / 5);
    }

    [[nodiscard]] int battery_percent() const noexcept {
        return battery_.percent();
    }

private:
    Battery battery_;
};

int main() {
    Robot robot{30};
    const bool moved{robot.move(25)};
    std::cout << std::boolalpha << "Moved: " << moved
              << ", battery: " << robot.battery_percent() << "%\n";
}
```

**실행 결과**

```text
Moved: true, battery: 25%
```

- `Robot`은 `Battery battery_`를 멤버로 소유합니다. `Robot` 객체가 소멸하면 멤버인 배터리 객체도 함께 소멸합니다.
- `move(25)`는 5m당 1%를 소모하는 규칙으로 5%를 소비합니다.
- `consume()`은 사용 가능 잔량보다 많은 요청을 거절하고 기존 잔량을 유지합니다.

이 예제는 메모리 안의 상태 변화이며 실제 로봇을 구동하지 않습니다. **합성**은 기존 객체의 기능을 활용하는 것이고, **상속(Inheritance)** 과 런타임 다형성은 Chapter 09에서 다룹니다.

<a id="section-8-11"></a>
## 8.11. Static Members & Destructors — 정적 멤버와 소멸자

**정적 멤버(Static Member)** 는 개별 객체가 아닌 클래스 단위로 존재하는 데이터 또는 함수입니다. `inline static` 데이터 멤버는 C++17부터 클래스 내부에 정의할 수 있습니다.

**소멸자(Destructor)** 는 객체의 수명이 끝날 때 실행되는 특별한 멤버 함수로, `~클래스이름()` 형태를 사용합니다. 이 예제에서는 생성된 연결 객체의 개수를 세기 위해 사용하지만, 일반적인 클래스마다 소멸자를 직접 작성해야 한다는 뜻은 아닙니다.

**예제 코드 — [10_static_members.cpp](./examples/10_static_members.cpp)**

```cpp
#include <iostream>

class Connection {
public:
    Connection() noexcept { ++active_; }
    ~Connection() { --active_; }

    Connection(const Connection&) = delete;
    Connection& operator=(const Connection&) = delete;
    Connection(Connection&&) = delete;
    Connection& operator=(Connection&&) = delete;

    [[nodiscard]] static int active_count() noexcept { return active_; }

private:
    inline static int active_{0};
};

int main() {
    std::cout << "Before: " << Connection::active_count() << '\n';
    {
        Connection first;
        Connection second;
        std::cout << "Inside: " << Connection::active_count() << '\n';
    }
    std::cout << "After: " << Connection::active_count() << '\n';
}
```

**실행 결과**

```text
Before: 0
Inside: 2
After: 0
```

`Connection::active_count()`는 객체를 만들지 않고 호출할 수 있습니다. 중괄호 안에서 객체 두 개를 생성했기 때문에 값이 2로 증가하고, 블록이 끝나면서 소멸자가 호출되어 다시 0이 됩니다.

이 클래스는 예제의 개수 세기 규칙을 단순하게 유지하기 위해 복사·이동을 금지합니다(`= delete`). 여러 스레드가 동시에 접근하는 경우에는 별도의 동기화가 필요합니다.

<a id="section-8-12"></a>
## 8.12. Defaulted Equality — 객체의 동등 비교

객체 두 개가 같다는 의미를 코드에 명시하려면 `operator==`를 정의할 수 있습니다. C++20부터는 조건을 충족하는 클래스에 **기본 동등 비교 연산자(Defaulted Equality Comparison)** 를 `= default`로 선언하여 각 멤버에 대한 비교를 생성할 수 있습니다.

**예제 코드 — [11_defaulted_comparison.cpp](./examples/11_defaulted_comparison.cpp)**

```cpp
#include <iostream>

struct DeviceKey {
    int rack{};
    int slot{};

    [[nodiscard]] bool operator==(const DeviceKey&) const = default;
};

int main() {
    const DeviceKey a{2, 7};
    const DeviceKey b{2, 7};
    const DeviceKey c{2, 8};
    std::cout << std::boolalpha;
    std::cout << "a == b: " << (a == b) << '\n';
    std::cout << "a == c: " << (a == c) << '\n';
}
```

**실행 결과**

```text
a == b: true
a == c: false
```

`DeviceKey{2, 7}` 두 개는 같은 `rack`과 `slot` 값을 가지므로 같고, `slot`이 다르면 같지 않습니다. 단, 모든 멤버가 같아야 같은 객체인지, 특정 ID만 같으면 되는지에 따라 비교 설계가 달라집니다.

**주의:** `double` 멤버가 포함된 자료형은 부동소수점 정밀도·`NaN` 등의 영향을 받으므로 자동 비교가 도메인 요구사항을 충족하는지 검토해야 합니다.

<a id="section-8-13"></a>
## 8.13. `this` & Method Chaining — 현재 객체와 연속 호출

일반적인 비정적 멤버 함수 안에서 **`this` 포인터** 는 함수를 호출한 현재 객체를 가리킵니다. `*this`는 현재 객체 자체에 대한 표현식이며, 이를 참조로 반환하면 같은 객체의 다른 멤버 함수를 이어서 호출할 수 있습니다.

**메서드 체이닝(Method Chaining)** 은 이처럼 설정 메서드를 연속으로 호출하는 패턴입니다. `<algorithm>` 헤더의 `std::clamp()`는 값을 하한·상한 사이로 제한합니다.

**예제 코드 — [12_this_and_fluent_api.cpp](./examples/12_this_and_fluent_api.cpp)**

```cpp
#include <algorithm>
#include <iostream>

class AlarmConfig {
public:
    AlarmConfig& set_threshold(int value) noexcept {
        threshold_ = std::clamp(value, 0, 100);
        return *this;
    }

    AlarmConfig& enable(bool value) noexcept {
        enabled_ = value;
        return *this;
    }

    [[nodiscard]] bool triggered(int reading) const noexcept {
        return enabled_ && reading >= threshold_;
    }

private:
    int threshold_{80};
    bool enabled_{true};
};

int main() {
    AlarmConfig config;
    config.set_threshold(65).enable(true);
    std::cout << std::boolalpha
              << "Alarm at 70: " << config.triggered(70) << '\n';
}
```

**실행 결과**

```text
Alarm at 70: true
```

`set_threshold(65)`가 `AlarmConfig&`를 반환하므로, 같은 객체에 곧바로 `enable(true)`를 호출할 수 있습니다. 이 함수들은 참조를 반환하므로 반환받은 값을 원본 객체의 수명보다 오래 보관하지 않아야 합니다.

값 설정에 실패할 수 있는 API라면 무조건 체이닝하도록 만들기보다 실패 정보를 어떻게 전달할지도 고려해야 합니다.

<a id="section-8-14"></a>
## 8.14. Multi-File Class Design — 헤더와 구현 파일 분리

프로그램이 커지면 클래스 인터페이스와 구현을 별도의 파일로 나누는 편이 좋습니다. **헤더(Header)** 는 선언을 제공하고, **소스 파일(Source File)** 은 실제 멤버 함수 정의를 제공합니다. 다른 코드에서 해당 클래스를 사용하려면 헤더를 포함한 뒤 구현 파일도 함께 컴파일·링크해야 합니다.

`<vector>`의 `std::vector<std::string>`으로 여러 식별자를 저장하고, `<algorithm>`의 `std::ranges::any_of()`로 중복 항목을 검사합니다. `<utility>`의 `std::move()`는 함수가 전달받은 문자열을 벡터에 이동 가능한 형태로 넘깁니다.

**파일 구성**

```text
examples/
├── 13_device_registry.hpp
├── 13_device_registry.cpp
└── 13_device_registry_main.cpp
```

**헤더 — [13_device_registry.hpp](./examples/13_device_registry.hpp)**

```cpp
#ifndef MORESTUDY_CPP_CHAPTER_08_DEVICE_REGISTRY_HPP
#define MORESTUDY_CPP_CHAPTER_08_DEVICE_REGISTRY_HPP

#include <cstddef>
#include <string>
#include <string_view>
#include <vector>

class DeviceRegistry {
public:
    [[nodiscard]] bool add(std::string id);
    [[nodiscard]] bool contains(std::string_view id) const;
    [[nodiscard]] std::size_t size() const noexcept;

private:
    std::vector<std::string> ids_;
};

#endif
```

**구현 — [13_device_registry.cpp](./examples/13_device_registry.cpp)**

```cpp
#include "13_device_registry.hpp"

#include <algorithm>
#include <utility>

bool DeviceRegistry::add(std::string id) {
    if (id.empty() || contains(id)) {
        return false;
    }
    ids_.push_back(std::move(id));
    return true;
}

bool DeviceRegistry::contains(std::string_view id) const {
    return std::ranges::any_of(ids_, [id](const std::string& current) {
        return current == id;
    });
}

std::size_t DeviceRegistry::size() const noexcept {
    return ids_.size();
}
```

**사용 코드 — [13_device_registry_main.cpp](./examples/13_device_registry_main.cpp)**

```cpp
#include "13_device_registry.hpp"

#include <iostream>

int main() {
    DeviceRegistry registry;
    const bool first{registry.add("CAM-01")};
    const bool duplicate{registry.add("CAM-01")};
    const bool second{registry.add("LIDAR-02")};
    std::cout << std::boolalpha
              << "First: " << first << ", duplicate: " << duplicate
              << ", second: " << second << '\n';
    std::cout << "Registered: " << registry.size() << '\n';
}
```

**컴파일 및 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic \
  examples/13_device_registry_main.cpp examples/13_device_registry.cpp -o registry
./registry
```

**실행 결과**

```text
First: true, duplicate: false, second: true
Registered: 2
```

`#ifndef`·`#define`·`#endif`는 헤더 가드(Include Guard)로, 동일 헤더가 한 번의 번역 단위에 중복 포함되어 선언이 반복되지 않도록 합니다. `DeviceRegistry::add`의 `::`는 소속 클래스의 함수를 정의한다는 의미입니다.

**중요:** 헤더만 포함하고 `13_device_registry.cpp`를 빌드에서 누락하면 함수 정의를 찾지 못하는 *링크 오류(Linker Error)* 가 발생합니다. 또 일반 함수의 정의를 아무 조건 없이 헤더에 반복해 넣으면 **단일 정의 규칙(One Definition Rule, ODR)** 과 충돌할 수 있습니다.

<a id="section-8-15"></a>
## 8.15. Copy, Move & Rule of Zero — 복사·이동과 자원 관리

C++ 객체의 **복사(Copy)** 는 다른 객체를 바탕으로 독립적인 새 값을 만드는 동작이고, **이동(Move)** 은 기존 객체의 자원을 새 객체에서 활용할 수 있도록 하는 동작입니다. 실제 동작은 해당 타입의 복사·이동 생성자에 따라 결정됩니다.

**제로의 규칙(Rule of Zero)** 은 자원 관리를 `std::string`, `std::vector`, 스마트 포인터처럼 수명을 스스로 관리하는 멤버 타입에 맡기고, 특별한 사유가 없으면 소멸자·복사·이동 관련 특수 멤버 함수를 직접 작성하지 않는 설계 원칙입니다.

**예제 코드 — [14_rule_of_zero.cpp](./examples/14_rule_of_zero.cpp)**

```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

class JobQueue {
public:
    void add(std::string job) {
        jobs_.push_back(std::move(job));
    }

    [[nodiscard]] std::size_t size() const noexcept { return jobs_.size(); }

private:
    std::vector<std::string> jobs_;
};

int main() {
    JobQueue original;
    original.add("Scan");
    JobQueue copied = original;
    JobQueue moved = std::move(original);
    std::cout << "Copied: " << copied.size()
              << ", moved: " << moved.size() << '\n';
}
```

**실행 결과**

```text
Copied: 1, moved: 1
```

`copied`의 벡터는 원본과 독립된 데이터를 가집니다. `moved`는 이동 생성자를 사용하도록 요청하며, 이동 후 `original`은 **유효하지만 내부 값은 가정하지 않는 상태**로 취급해야 합니다.

`std::move()` 자체가 데이터를 이동시키는 것은 아닙니다. 특별한 자원 관리가 필요한 코드에서는 복사 가능 여부·이동 가능 여부를 명시적으로 정하지만, 일반적인 값 보관 클래스는 Rule of Zero를 먼저 검토합니다.

<a id="section-8-16"></a>
## 8.16. Class Design Guidelines — 클래스 설계 원칙

클래스를 작성할 때는 **어떤 데이터를 저장하는가**뿐 아니라 **어떤 상태가 유효한가**, **누가 상태를 변경할 수 있는가**, **누가 자원을 소유하는가**까지 생각해야 합니다.

| 상황 | 우선 고려할 방법 | 이유 |
|---|---|---|
| 좌표·측정값처럼 단순한 값 묶음 | `struct` + 기본 멤버 초기화 | 데이터가 곧 공개 인터페이스인 경우 적절합니다. |
| 범위 제한이 필요한 내부 상태 | `class` + `private` + 검증 메서드 | 외부에서 상태 검증을 우회하지 못하도록 합니다. |
| 생성 전에 입력 검증이 필요한 객체 | 정적 팩토리 함수 + `std::optional` | 잘못된 객체의 생성을 거절할 수 있습니다. |
| 여러 부분으로 구성된 기능 | 합성(Composition) | 작은 객체의 책임을 나누고 재사용할 수 있습니다. |
| 문자열·배열을 보관하는 클래스 | `std::string`, `std::vector` | 자원 수명을 표준 타입에 맡길 수 있습니다. |
| 여러 파일에서 사용하는 클래스 | `.hpp` 선언 + `.cpp` 정의 | 다른 파일이 사용할 인터페이스와 구현을 구분합니다. |

**흔히 발생하는 실수**

```cpp
// 상태 제한을 외부에서 우회할 수 있습니다.
struct UnsafeMotor { int rpm; };
UnsafeMotor motor{-200};

// 기본 멤버 초기화 없이 읽기 전에 값을 사용하면 잘못된 결과가 날 수 있습니다.
struct Counter { int count; };
// Counter counter;  // count를 초기화하지 않은 상태
```

생성자 본문에서 멤버를 대입하는 것과 멤버 초기화 목록으로 직접 초기화하는 것은 같지 않습니다. `private`로 멤버를 보호한 뒤에도 공개 메서드가 허용 범위를 위반하지 않는지 테스트해야 합니다.

**확장 방향:** 상속, 가상 함수와 런타임 다형성은 클래스 구성과는 별도의 설계 문제이며 Chapter 09에서 학습합니다. 현재 단계에서는 작은 객체를 합성하고 각 클래스의 책임과 상태 규칙을 명확히 하는 데 집중합니다.

<a id="section-8-17"></a>
## 8.17. Coding Practice — 연습문제

`exercises/`에는 멤버 함수의 핵심 구현이 비어 있는 코드가 있습니다. 필요한 `TODO`를 직접 채운 뒤 테스트하고, `solutions/`의 모범답안과 비교합니다. 각 문제는 `main()`의 출력뿐 아니라 **경계값에서 메서드가 올바르게 동작하는지**도 검사합니다.

| 번호 | 실습 | 문제 파일 | 모범답안 |
|:---:|---|---|---|
| 01 | Device Profile Validation | [01_device_profile.cpp](./exercises/01_device_profile.cpp) | [01_device_profile.cpp](./solutions/01_device_profile.cpp) |
| 02 | Bank Account | [02_bank_account.cpp](./exercises/02_bank_account.cpp) | [02_bank_account.cpp](./solutions/02_bank_account.cpp) |
| 03 | Temperature Window | [03_temperature_window.cpp](./exercises/03_temperature_window.cpp) | [03_temperature_window.cpp](./solutions/03_temperature_window.cpp) |
| 04 | Robot Battery | [04_robot_battery.cpp](./exercises/04_robot_battery.cpp) | [04_robot_battery.cpp](./solutions/04_robot_battery.cpp) |

### Exercise 01 — Device Profile Validation

센서의 이름·소비 전력·온라인 여부를 저장하는 `DeviceProfile`의 `valid()` 멤버 함수를 완성합니다.

**구현 조건**

- `name`은 비어 있으면 안 됩니다.
- `power_w`는 유한한 실수이면서 `0~2000` W 범위여야 합니다.
- `online` 값은 유효성 조건에 영향을 주지 않습니다.
- `NaN`, 무한대, 음수 전력, `2000` 초과 전력을 거부합니다.

**정상 실행 결과**

```text
Valid: true, invalid: false
```

### Exercise 02 — Bank Account

`balance_cents_`를 `private`으로 유지하면서 `deposit()`과 `withdraw()` 메서드를 완성합니다. 금액은 정수 센트 단위로 관리합니다.

**구현 조건**

- 입금·출금 금액은 `0`보다 커야 합니다.
- 출금 금액이 잔액보다 크면 실패하고 기존 잔액을 유지합니다.
- 입금하면 `std::int64_t`의 최댓값을 넘는지 **더하기 전에** 검사합니다.
- 성공하면 `true`, 실패하면 `false`를 반환합니다.

**정상 실행 결과**

```text
Deposit: true, withdraw: true, balance: 8500 cents
```

`<limits>`의 `std::numeric_limits<std::int64_t>::max()`로 정수 표현 범위를 확인합니다. 범위 검사 전 덧셈을 해버리면 이미 부호 있는 정수 오버플로가 발생할 수 있습니다.

### Exercise 03 — Temperature Window

`TemperatureWindow::create()`와 `contains()`를 완성합니다. 객체가 생성된 이후 항상 올바른 범위가 유지되도록 생성 경로를 제한합니다.

**구현 조건**

- 상한·하한이 모두 유한한 수이고, `lower <= upper`일 때만 객체를 생성합니다.
- 올바르지 않으면 `std::nullopt`를 반환합니다.
- `contains()`는 유한한 값이 닫힌 구간 `[lower, upper]`에 있는지 검사합니다.
- `private` 생성자는 그대로 유지합니다.

**정상 실행 결과**

```text
23 C allowed: true
```

### Exercise 04 — Robot Battery

`Robot`이 `Battery` 객체를 포함하도록 설계한 상태에서 배터리 소모와 이동 조건을 완성합니다.

**구현 조건**

- 이동은 `1~1000` m의 정수 거리만 허용합니다.
- 5m당 배터리 1%를 소모하며, 5의 배수가 아닌 거리도 **올림** 계산합니다.
- 배터리가 부족하면 이동 실패를 반환하고 기존 잔량을 유지합니다.
- 배터리 값은 `Battery::consume()`을 통해서만 변경합니다.

**정상 실행 결과**

```text
Short: true, long: false, battery: 95%
```

### 실습 및 테스트

`Chapter-08/` 폴더에서 실행합니다.

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/01_device_profile.cpp -o device_profile
./device_profile
```

**전체 모범답안과 예제 검사**

```bash
python tests/check.py
```

**직접 수정한 Exercise 01 검사**

```bash
python tests/check.py --exercise 01
```

첫 번째 검사 명령어는 예제·모범답안·프로젝트 정답을 확인합니다. 두 번째는 직접 수정한 Exercise 01을 검사하므로 `TODO`가 남아 있는 초기 상태에서는 FAIL이 나오는 것이 정상입니다. Exercise 02~04는 `01` 대신 해당 번호를 사용하면 됩니다.

<a id="section-8-18"></a>
## 8.18. Mini Project — Device Inventory

여러 장치를 등록하고 각 장치의 상태 및 소비 전력을 집계하는 **Device Inventory** 콘솔 프로그램을 작성합니다. `struct Device`는 장치 하나의 데이터를 표현하고, `class DeviceInventory`는 목록의 유효성·집계·검색을 담당합니다.

**구현할 멤버 함수**

| 함수 | 역할 |
|---|---|
| `add(id, power_w, online)` | 장치 유효성 검사와 중복 등록 방지 |
| `size()` | 등록된 장치 개수 반환 (제공됨) |
| `online_count()` | 온라인 상태인 장치 수 계산 |
| `total_power()` | 모든 장치의 소비 전력 합산 |
| `active_power()` | 온라인 장치의 소비 전력 합산 |
| `highest_power()` | 가장 큰 소비 전력의 장치 주소 반환 |

**입력 조건**

- 등록할 장치 수는 `1~5`개입니다.
- 장치 ID는 공백이 없는 비어 있지 않은 문자열이며, 동일한 ID를 두 번 등록할 수 없습니다. 대소문자를 구분합니다.
- 소비 전력은 `0~2000` W의 정수입니다.
- 온라인 상태는 `0` 또는 `1`로 입력합니다.
- 잘못된 등록 요청은 실패하고 해당 객체의 기존 목록을 변경하지 않아야 합니다.
- 소비 전력이 같은 장치가 여러 개면 **먼저 등록한 장치**를 선택합니다.

**실행 예시** (사용자가 입력한 값 포함)

```text
Devices (1-5): 3
Device 1 (ID power_W online_0_or_1): CAM-01 12 1
Device 2 (ID power_W online_0_or_1): LIDAR-02 25 0
Device 3 (ID power_W online_0_or_1): IMU-03 8 1

--- Device Inventory ---
Registered: 3
Online: 2
Total power: 45 W
Active power: 20 W
Highest power: LIDAR-02 (25 W)
```

자동 테스트는 입력값을 별도로 전달하므로 표준 출력 비교 시 사용자가 입력한 줄은 포함하지 않습니다.

`highest_power()`는 내부 벡터 요소를 가리키는 비소유 포인터를 반환합니다. **벡터에 요소를 추가하는 중에는 이전 포인터가 무효화될 수 있으므로**, 모든 등록이 끝난 후 포인터를 얻어 즉시 결과를 출력하도록 합니다.

**프로젝트 파일**

- [시작 코드 — project/device_inventory.cpp](./project/device_inventory.cpp)
- [모범답안 — solutions/device_inventory.cpp](./solutions/device_inventory.cpp)

**컴파일 및 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/device_inventory.cpp -o inventory
./inventory
```

**프로젝트 테스트**

```bash
python tests/check.py --project
```

**완료 기준**

1. 유효한 장치 여러 개를 등록하고, 중복된 ID는 거절합니다.
2. 등록 실패 후 기존 목록이 그대로 유지됩니다.
3. 온라인 수와 전력 합계를 정확하게 계산합니다.
4. 동점 최고 전력은 먼저 등록한 장치를 반환합니다.
5. 등록 개수·전력 범위·온라인 값이 잘못된 경우 오류 종료합니다.

프로젝트 시작 코드는 `TODO` 상태이므로 모든 메서드를 작성하기 전에는 프로젝트 테스트가 통과하지 않습니다.

<a id="section-8-19"></a>
## 8.19. Quiz & Summary — 점검 및 정리

### Quiz

**Q1.** C++에서 `struct`와 `class`의 기본 멤버 접근 권한 조합으로 맞는 것은 무엇인가요?

- A. `struct`: `private`, `class`: `public`
- B. 둘 다 `public`
- C. `struct`: `public`, `class`: `private`
- D. 둘 다 `private`

<details>
<summary>정답 및 해설</summary>

**정답: C**

`struct`의 멤버는 기본적으로 공개되고, `class`의 멤버는 기본적으로 비공개입니다. 필요한 경우 둘 다 `public`, `private`을 명시해 접근 권한을 바꿀 수 있습니다. 데이터 전용 객체에 `struct`를 많이 사용하는 것은 관례이지 기능의 제한이 아닙니다.

</details>

**Q2.** 다음 코드에서 `motor.rpm_ = -1;`은 왜 사용할 수 없나요?

```cpp
class Motor {
private:
    int rpm_{};
};
```

<details>
<summary>정답 및 해설</summary>

`rpm_`는 클래스의 `private` 멤버이기 때문입니다. 외부에서 접근할 수 없습니다. 모터 속도 변경이 필요한 경우 `public` 멤버 함수를 제공하고, 그 함수에서 허용 범위를 검사해야 합니다. `private`는 단순히 이름을 숨기는 기능이 아니라 외부의 상태 변경 경로를 제한하는 도구입니다.

</details>

**Q3.** C++20 지정 초기화자에서 올바른 형식은 무엇인가요? 다음 구조체를 기준으로 고르세요.

```cpp
struct Point { int x; int y; };
```

- A. `Point p{.y = 2, .x = 1};`
- B. `Point p{.x = 1, .y = 2};`
- C. `Point p{y: 2, x: 1};`
- D. `Point p{.z = 2};`

<details>
<summary>정답 및 해설</summary>

**정답: B**

C++20의 지정 초기화자는 `.멤버명 = 값`을 사용하고, 멤버가 선언된 순서에 맞춰 지정해야 합니다. A는 순서가 거꾸로이고, C는 C++ 지정 초기화자 문법이 아니며, D는 존재하지 않는 멤버를 지정합니다.

</details>

**Q4.** `explicit` 생성자를 사용할 때 얻는 이점은 무엇인가요?

<details>
<summary>정답 및 해설</summary>

단일 인수 등으로 호출할 수 있는 생성자를 통해 원하지 않는 **암묵적 타입 변환**이 발생하는 것을 막을 수 있습니다. 예를 들어 `DeviceId`를 정수와 구분하려면 `DeviceId{42}`처럼 의도를 명시해 생성합니다. `explicit`가 입력값 범위 자체를 검증해 주는 것은 아니므로 유효성 검사는 별도로 구현해야 합니다.

</details>

**Q5.** 멤버 초기화 목록에서 `second_`를 `first_`보다 먼저 작성하면 `second_`가 먼저 초기화되나요?

- A. 언제나 먼저 초기화됩니다.
- B. 멤버는 클래스 내부의 **선언 순서**대로 초기화됩니다.
- C. 초기화 순서는 실행할 때마다 바뀝니다.
- D. 생성자 본문이 먼저 실행됩니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

초기화 순서는 멤버 초기화 목록의 나열 순서가 아니라 **클래스 내부 선언 순서**를 따릅니다. 생성자 본문은 멤버 초기화가 끝난 뒤 실행됩니다. 따라서 선언 순서와 초기화 목록을 일치시키고, 다른 멤버의 아직 초기화되지 않은 값에 의존하지 않도록 작성해야 합니다.

</details>

**Q6.** `const Counter& counter`에서 `counter.count()`를 호출하려면 `count()`의 선언에 어떤 조건이 필요하나요?

<details>
<summary>정답 및 해설</summary>

조회용 멤버 함수를 `int count() const`와 같이 **`const` 멤버 함수**로 선언해야 합니다. `const` 객체에서는 상태를 변경할 수 있는 일반 비정적 멤버 함수를 호출할 수 없습니다. `const`를 붙인다고 해당 객체가 참조하는 모든 외부 상태까지 자동으로 불변이 되는 것은 아닙니다.

</details>

**Q7.** `TemperatureWindow::create(30.0, 10.0)`처럼 잘못된 범위를 입력했을 때 C++20 예제에서 반환하는 값은 무엇인가요?

- A. `std::nullopt`
- B. `nullptr`
- C. `false` 타입의 객체
- D. 자동으로 상한과 하한이 교환된 객체

<details>
<summary>정답 및 해설</summary>

**정답: A**

`create()`의 반환 타입은 `std::optional<TemperatureWindow>`입니다. 유효한 객체를 생성할 수 없을 때는 `std::nullopt`를 반환합니다. `nullptr`는 포인터의 비어 있는 상태를 나타내며, `optional` 자체와 같은 타입은 아닙니다. 입력값을 임의로 보정하는 것은 명시된 규칙이 아니라면 적절하지 않습니다.

</details>

**Q8.** 위임 생성자(Delegating Constructor)는 어떤 문제를 해결하는 데 도움이 되나요?

<details>
<summary>정답 및 해설</summary>

여러 생성자에 반복되는 초기화 코드를 한 곳으로 모을 수 있습니다. 예를 들어 `Sensor(std::string)`이 기본 임계값을 추가해 `Sensor(std::string, int)`에 위임하면, 주요 초기화 규칙을 두 번째 생성자에서 관리할 수 있습니다. 위임 생성자는 같은 클래스의 다른 생성자를 호출하는 문법입니다.

</details>

**Q9.** 로봇이 배터리 객체를 멤버로 보관하고 배터리 사용을 위임하는 관계는 무엇인가요?

- A. 함수 오버로딩
- B. 상속
- C. 객체 합성(Composition)
- D. 템플릿 특수화

<details>
<summary>정답 및 해설</summary>

**정답: C**

로봇이 배터리를 **가지고 있는 관계(Has-a)** 는 객체 합성입니다. 이 방식은 배터리가 에너지 소비 규칙을 담당하고 로봇은 이동 요청을 담당하도록 책임을 나눌 수 있습니다. 상속은 별도의 타입 관계이며 Chapter 09에서 학습합니다.

</details>

**Q10.** `inline static int active_`와 일반적인 `int active_`는 어떤 차이가 있나요?

<details>
<summary>정답 및 해설</summary>

`inline static` 멤버는 **클래스 단위로 하나의 공유 상태**를 나타냅니다. 일반 비정적 멤버는 각 객체가 자기 값을 갖습니다. 예제에서 생성자·소멸자가 공유 카운터를 증감하면 활성 객체 개수를 계산할 수 있습니다. 복사·이동 동작을 특별히 처리하지 않으면 잘못 집계할 수 있다는 점에도 주의해야 합니다.

</details>

**Q11.** 아래 코드의 출력은 무엇인가요?

```cpp
struct DeviceKey {
    int rack{};
    int slot{};
    bool operator==(const DeviceKey&) const = default;
};

const DeviceKey a{2, 7};
const DeviceKey b{2, 8};
std::cout << std::boolalpha << (a == b) << '\n';
```

<details>
<summary>정답 및 해설</summary>

**정답: `false`**

C++20의 기본 `operator==`는 각 데이터 멤버를 비교합니다. 두 객체는 `rack` 값은 같지만 `slot`이 각각 `7`, `8`로 다르므로 전체 비교 결과는 `false`입니다. `std::boolalpha`는 논리값을 영문 문자열로 출력합니다.

</details>

**Q12.** `DeviceRegistry::add()`의 선언은 헤더에 있지만 정의가 있는 `.cpp` 파일을 빌드에서 빠뜨리면 어떤 문제가 발생할까요?

- A. 데이터가 자동으로 비워집니다.
- B. 컴파일 단계에서 무조건 문법 오류가 납니다.
- C. 사용한 함수 정의를 찾지 못해 링크 오류가 발생할 수 있습니다.
- D. 빈 함수가 자동으로 만들어집니다.

<details>
<summary>정답 및 해설</summary>

**정답: C**

선언을 확인한 소스 파일의 컴파일 자체는 성공할 수 있지만, 프로그램을 연결하는 **링크(Link) 단계**에서 함수 정의를 찾지 못해 실패할 수 있습니다. 따라서 다중 파일 프로그램은 `main.cpp`뿐 아니라 클래스 구현 파일도 함께 빌드해야 합니다.

</details>

### Summary

- **`struct`와 `class`:** 기본 접근 권한이 다른 사용자 정의 자료형입니다.
- **집합체 초기화:** 데이터 멤버를 중괄호로 초기화하며, C++20의 지정 초기화자를 사용할 수 있습니다.
- **캡슐화:** `private` 멤버와 공개 메서드로 유효한 상태 변경을 관리합니다.
- **생성자와 `explicit`:** 객체 초기 상태를 설정하고 의도하지 않은 암묵적 변환을 방지합니다.
- **멤버 초기화 목록:** 멤버 선언 순서에 따라 생성자 본문 전에 초기화합니다.
- **`const` 멤버 함수:** 객체의 일반적인 상태를 수정하지 않는 조회 함수를 표현합니다.
- **팩토리 함수:** 객체를 생성하기 전에 입력을 검증하고 실패 시 결과 없음으로 표현합니다.
- **위임 생성자:** 한 생성자에서 같은 클래스의 다른 생성자로 초기화를 위임합니다.
- **객체 합성:** 다른 객체를 멤버로 포함하여 역할과 책임을 나눕니다.
- **정적 멤버:** 클래스 단위로 공유되는 데이터와 동작을 제공합니다.
- **동등 비교:** C++20의 기본 `operator==`로 멤버별 동등 비교를 정의할 수 있습니다.
- **Rule of Zero:** 문자열·벡터 등 표준 타입에 자원 수명 관리를 맡깁니다.
- **파일 분리:** 헤더와 구현 파일을 함께 빌드해 선언과 정의를 연결합니다.

### References

- [cppreference — Classes](https://en.cppreference.com/w/cpp/language/classes)
- [cppreference — Aggregate Initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization)
- [cppreference — Constructors](https://en.cppreference.com/w/cpp/language/constructor)
- [cppreference — Member Initializer Lists](https://en.cppreference.com/w/cpp/language/initializer_list)
- [cppreference — Access Specifiers](https://en.cppreference.com/w/cpp/language/access)
- [cppreference — `std::optional`](https://en.cppreference.com/w/cpp/utility/optional)
- [cppreference — Defaulted Comparisons](https://en.cppreference.com/w/cpp/language/default_comparisons)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

---

[← C++ 목차](../README.md#contents) · [이전 Chapter — Pointers & References](../Chapter-07/) · [다음 Chapter — Object-Oriented Design](../Chapter-09/)

