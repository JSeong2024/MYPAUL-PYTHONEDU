# Chapter 08. Structs & Classes

구조체와 클래스의 기본 구조, 생성자와 초기화, 접근 제어, 객체의 유효성 관리, 합성(Composition) 및 파일 단위 설계를 다룹니다. 데이터를 묶는 수준에서 벗어나 **잘못된 상태를 방지하고 유지보수할 수 있는 자료형**을 작성하는 것이 목표입니다.

본 자료는 **C++23(ISO/IEC 14882:2024)**을 기준으로 작성되었습니다. 예제는 GCC 14 이상 또는 필요한 C++23 표준 라이브러리를 지원하는 컴파일러 환경을 권장합니다.

## Contents

| Section | Topic |
|:---:|---|
| 8.1 | Struct와 Class의 역할 및 차이 |
| 8.2 | 구조체와 멤버 데이터 |
| 8.3 | Aggregate Initialization과 Designated Initializer |
| 8.4 | 접근 제어와 Encapsulation |
| 8.5 | Constructor와 `explicit` |
| 8.6 | 기본 멤버 값과 Member Initializer List |
| 8.7 | `const` 멤버 함수 |
| 8.8 | Class Invariant와 Factory Method |
| 8.9 | Delegating Constructor |
| 8.10 | Composition과 객체 간 관계 |
| 8.11 | Static Member와 객체 수명 |
| 8.12 | 객체 비교와 `operator==` |
| 8.13 | `this`와 Method Chaining |
| 8.14 | 헤더·구현 파일 분리 |
| 8.15 | Copy, Move와 Rule of Zero |
| 8.16 | 실무 설계 원칙 및 오류 사례 |
| 8.17 | Coding Practice |
| 8.18 | Quiz & Summary |

---

## 8.1. Struct와 Class의 역할 및 차이

구조체(`struct`)와 클래스(`class`)는 여러 데이터와 동작을 하나의 사용자 정의 자료형으로 묶습니다. 두 문법은 **기본 접근 권한**을 제외하면 멤버 함수, 생성자, 상속 등 대부분의 언어 기능을 동일하게 지원합니다.

| 구분 | `struct` | `class` |
|---|---|---|
| 기본 멤버 접근 권한 | `public` | `private` |
| 기본 상속 접근 권한 | `public` | `private` |
| 생성자·멤버 함수 | 사용 가능 | 사용 가능 |
| 관례적인 사용 | 데이터 전달, 단순한 값 묶음 | 상태 보호, 동작과 규칙을 함께 제공 |

```cpp
struct Position {
    int x{};
    int y{};
};

class Counter {
public:
    void increment() noexcept { ++value_; }
    [[nodiscard]] int value() const noexcept { return value_; }

private:
    int value_{};
};
```

`Position`은 좌표값을 그대로 노출해도 문제가 없는 단순 자료입니다. 반면 `Counter`는 외부에서 값을 마음대로 수정하지 않고 제공된 멤버 함수를 통해 상태를 변경하게 합니다.

**선택 기준:** 공개 데이터가 곧 올바른 객체 상태인 경우 `struct`를, 값 변경에 검증이나 규칙이 필요하면 `class`를 우선 고려합니다. `struct`가 반드시 C 언어와 같은 메모리 구조나 Binary 호환성을 보장하는 것은 아닙니다.

---

## 8.2. 구조체와 멤버 데이터

구조체의 내부 변수는 멤버(Member)라고 부릅니다. 실제 센서 측정값처럼 서로 관계있는 값을 하나의 단위로 전달할 때 유용합니다.

별도의 생성자를 정의하지 않아도 중괄호 초기화로 각 멤버에 값을 지정할 수 있습니다. 기본 멤버 초기화자(Default Member Initializer)를 사용하면 일부 값을 생략했을 때의 기본 상태를 지정할 수 있습니다.

**예제 코드 — [01_struct_record.cpp](./examples/01_struct_record.cpp)**

```cpp
#include <print>
#include <string>

struct SensorReading {
    std::string device_id;
    double temperature_c{};
    bool online{};
};

int main() {
    const SensorReading reading{"TEMP-A", 23.5, true};
    std::println("{}: {:.1f} C (online: {})",
                 reading.device_id, reading.temperature_c, reading.online);
}
```

**실행 결과**

```text
TEMP-A: 23.5 C (online: true)
```

- **`device_id`:** 장치 식별 문자열
- **`temperature_c`:** 섭씨 온도 측정값
- **`online`:** 장치 연결 여부
- **`.` 연산자:** 객체의 멤버에 접근하는 방법

`SensorReading`은 값의 집합을 나타내므로 공개 멤버를 사용해도 무방합니다. 단, 실제 서비스에서 장치 식별자 중복이나 온도 범위 검증이 필요하다면 검증 함수 또는 별도 클래스로 역할을 분리해야 합니다.

---

## 8.3. Aggregate Initialization과 Designated Initializer

집합체 초기화(Aggregate Initialization)는 조건을 만족하는 배열·클래스 형태의 객체를 멤버 순서에 맞춰 초기화하는 방식입니다. 일반적인 데이터 전용 `struct`에서 자주 사용합니다.

C++20부터는 지정 초기화자(Designated Initializer)를 사용해 `.멤버명 = 값` 형태로 의도를 표현할 수 있습니다. C++23에서도 동일하게 사용합니다.

**예제 코드 — [02_designated_initializers.cpp](./examples/02_designated_initializers.cpp)**

```cpp
#include <cstdint>
#include <print>

struct PacketHeader {
    std::uint32_t message_id{};
    std::uint16_t payload_bytes{};
    bool encrypted{false};
};

int main() {
    const PacketHeader header{
        .message_id = 42,
        .payload_bytes = 128,
        .encrypted = true,
    };
    std::println("Packet {}: {} bytes, encrypted: {}",
                 header.message_id, header.payload_bytes, header.encrypted);
}
```

**실행 결과**

```text
Packet 42: 128 bytes, encrypted: true
```

C++의 Designated Initializer는 C 언어의 유사 문법과 규칙이 다릅니다.

- **멤버 선언 순서 준수:** `.message_id` → `.payload_bytes` → `.encrypted` 순서
- **Aggregate 대상:** 일반 생성자가 선언된 클래스 등은 이 구문으로 초기화할 수 없음
- **일부 멤버 생략:** 기본 멤버 초기화자 또는 규칙에 따른 초기화 적용
- **위치 기반 초기화:** 멤버 개수가 많다면 이름을 명시하는 방식이 실수를 줄일 수 있음

```cpp
// C++에서 유효하지 않은 순서: 선언된 멤버 순서를 위반
// PacketHeader invalid{.encrypted = true, .message_id = 42};
```

**주의:** 외부 바이너리 프로토콜의 필드 순서나 네트워크 패킷을 메모리 배치에 그대로 의존하여 처리해서는 안 됩니다. 패딩(Padding), 정렬(Alignment), 바이트 순서(Byte Order) 등을 고려한 직렬화가 필요합니다.

---

## 8.4. 접근 제어와 Encapsulation

접근 지정자(Access Specifier)는 코드가 객체의 멤버에 접근할 수 있는 범위를 정합니다. 캡슐화(Encapsulation)는 내부 상태를 보호하고, 필요한 동작만 공개하는 설계 방식입니다.

| 지정자 | 접근 범위 |
|---|---|
| `public` | 객체 사용자에게 제공하는 인터페이스 |
| `private` | 해당 클래스 및 허용된 코드에서만 접근 |
| `protected` | 해당 클래스 및 파생 클래스에서 접근 — Chapter 09에서 자세히 설명 |

예를 들어 모터 회전수를 제한해야 하는데 `public int rpm;`으로 공개하면 사용자가 `rpm = -500`처럼 잘못된 값을 설정할 수 있습니다. setter를 통해 범위를 검증할 수 있습니다.

**예제 코드 — [03_encapsulation.cpp](./examples/03_encapsulation.cpp)**

```cpp
#include <print>

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
    int rpm_{0};
};

int main() {
    Motor motor;
    const bool accepted = motor.set_rpm(1'500);
    const bool rejected = motor.set_rpm(4'000);
    std::println("Accepted: {}, rejected: {}, RPM: {}",
                 accepted, rejected, motor.rpm());
}
```

**실행 결과**

```text
Accepted: true, rejected: false, RPM: 1500
```

`Motor::set_rpm()`은 범위를 벗어난 요청을 거절하며 기존 상태를 변경하지 않습니다. `rpm()`은 읽기 전용 접근을 제공합니다.

- **인터페이스:** `set_rpm()`, `rpm()`
- **내부 구현:** `rpm_`
- **검증 규칙:** `0 <= rpm <= 3000`

실제 하드웨어를 다룰 때는 값 검증과 별개로 장치 통신 성공 여부도 처리해야 합니다. 단순히 범위가 올바르다고 모터 제어가 성공한 것은 아닙니다.

---

## 8.5. Constructor와 `explicit`

생성자(Constructor)는 객체가 생성될 때 초기 상태를 설정하는 멤버 함수입니다. 클래스 이름과 같으며 반환형이 없습니다.

단일 인수로 호출할 수 있는 생성자는 원하지 않는 암묵적 변환(Implicit Conversion)의 경로가 될 수 있으므로, 변환을 의도하지 않는다면 `explicit` 사용을 고려합니다.

**예제 코드 — [04_explicit_constructor.cpp](./examples/04_explicit_constructor.cpp)**

```cpp
#include <cstdint>
#include <print>

class DeviceId {
public:
    explicit DeviceId(std::uint32_t value) noexcept : value_{value} {}
    [[nodiscard]] std::uint32_t value() const noexcept { return value_; }

private:
    std::uint32_t value_{};
};

void print_device(DeviceId id) {
    std::println("Device ID: {}", id.value());
}

int main() {
    const DeviceId id{1'024};
    print_device(id);
    // print_device(1024); // explicit 생성자이므로 암묵적 변환 불가
}
```

**실행 결과**

```text
Device ID: 1024
```

`DeviceId`는 원시 정수와 구분되는 자료형입니다. `print_device(1024)`는 `explicit` 생성자 때문에 암묵적으로 변환되지 않으며, `print_device(DeviceId{1024})`처럼 의도를 명시해야 합니다.

**실무 기준:** 생성자에 전달된 값의 유효성이 중요하다면 생성자에 검증 계약을 두거나, 아래 8.8절처럼 생성이 실패할 수 있는 Factory Method를 사용합니다. `explicit` 자체가 입력값을 검증하는 기능은 아닙니다.

---

## 8.6. 기본 멤버 값과 Member Initializer List

멤버 초기화 목록(Member Initializer List)은 생성자 본문이 실행되기 **전에** 멤버를 초기화합니다. 기본 멤버 초기화자와 함께 사용하면 객체의 초기 상태를 명확히 표현할 수 있습니다.

특히 `const` 멤버, 참조 멤버, 기본 생성자가 없는 멤버 객체는 생성자 본문에서 대입하는 방식으로 초기화할 수 없습니다.

**예제 코드 — [05_member_initialization.cpp](./examples/05_member_initialization.cpp)**

```cpp
#include <print>
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
        std::println("{} on channel {}", name_, channel_);
    }

private:
    std::string name_;
    int channel_{};
};

int main() {
    const RetryOptions options{};
    const Device sensor{"LIDAR", 2};
    std::println("Retries: {}, delay: {} ms", options.attempts, options.delay_ms);
    sensor.print();
}
```

**실행 결과**

```text
Retries: 3, delay: 250 ms
LIDAR on channel 2
```

- **`attempts{3}`:** 기본 생성 시 재시도 횟수 설정
- **`name_{std::move(name)}`:** 전달받은 문자열을 멤버로 이동
- **`channel_{channel}`:** 멤버를 생성자에서 직접 초기화

**초기화 순서(Initialization Order)**는 `:` 뒤의 나열 순서가 아니라 **클래스 내 멤버 선언 순서**에 의해 결정됩니다. 서로 다른 멤버를 사용해 초기화할 때는 순서 의존성을 피해야 합니다.

```cpp
class Example {
    int first_{};
    int second_{};

public:
    Example(int first, int second) : first_{first}, second_{second} {}
};
```

선언 순서와 Member Initializer List 순서를 동일하게 작성하면 코드를 읽기 쉽고 경고를 줄일 수 있습니다.

---

## 8.7. `const` 멤버 함수

`const` 멤버 함수는 해당 함수를 통해 객체의 일반적인 상태를 변경하지 않겠다는 약속을 표현합니다. `const` 객체 또는 `const T&` 참조를 통해 호출하려면 접근에 필요한 멤버 함수도 적절히 `const`로 선언해야 합니다.

**예제 코드 — [06_const_member_functions.cpp](./examples/06_const_member_functions.cpp)**

```cpp
#include <print>

class SampleCounter {
public:
    void record() noexcept { ++count_; }
    [[nodiscard]] int count() const noexcept { return count_; }

private:
    int count_{};
};

void print_count(const SampleCounter& counter) {
    std::println("Samples: {}", counter.count());
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

- **`record()`:** 상태를 변경하므로 일반 멤버 함수
- **`count() const`:** 상태를 읽기만 하는 함수
- **`const SampleCounter&`:** 복사 없이 기존 객체를 조회

`const`는 객체가 참조하는 외부 자원까지 자동으로 불변으로 만드는 기능은 아닙니다. 포인터 멤버나 외부 리소스가 있다면 의도와 별도의 제약을 함께 고려해야 합니다.

---

## 8.8. Class Invariant와 Factory Method

클래스 불변식(Class Invariant)은 객체가 외부에 제공되는 동안 유지해야 하는 유효 상태의 조건입니다. 예를 들어 `min <= max`인 온도 범위만 허용하려면 객체 생성 단계에서 검증할 필요가 있습니다.

객체 생성에 실패할 수 있다면 정적 생성 함수인 팩토리 메서드(Factory Method)를 사용할 수 있습니다. C++23의 `std::expected<T, E>`는 생성 결과 또는 실패 이유를 반환할 때 유용합니다.

**예제 코드 — [07_expected_factory.cpp](./examples/07_expected_factory.cpp)**

```cpp
#include <cmath>
#include <expected>
#include <print>
#include <string>

class TemperatureWindow {
public:
    [[nodiscard]] static std::expected<TemperatureWindow, std::string>
    create(double low, double high);

    [[nodiscard]] bool contains(double value) const noexcept {
        return std::isfinite(value) && low_ <= value && value <= high_;
    }

private:
    TemperatureWindow(double low, double high) noexcept : low_{low}, high_{high} {}
    double low_{};
    double high_{};
};

std::expected<TemperatureWindow, std::string>
TemperatureWindow::create(double low, double high) {
    if (!std::isfinite(low) || !std::isfinite(high) || low > high) {
        return std::unexpected("Invalid temperature range");
    }
    return TemperatureWindow{low, high};
}

int main() {
    const auto window = TemperatureWindow::create(18.0, 28.0);
    if (!window) {
        std::println("Error: {}", window.error());
        return 1;
    }
    std::println("23 C accepted: {}", window->contains(23.0));
    std::println("31 C accepted: {}", window->contains(31.0));
}
```

**실행 결과**

```text
23 C accepted: true
31 C accepted: false
```

- **`private` 생성자:** 검증되지 않은 경로로 객체를 만들지 못하도록 제한
- **`create()`:** 입력 범위 및 `NaN`, 무한대 검사
- **`std::unexpected`:** 생성 실패 원인 전달
- **`contains()`:** 유효한 객체의 상태를 이용해 입력값 검사

온도 범위 객체를 성공적으로 얻었다면 이후에 `low > high` 상태를 처리할 필요가 없도록 설계한 것입니다. 실무에서는 사용자가 객체를 수정할 수 있는 모든 공개 메서드도 Class Invariant를 보존하도록 설계해야 합니다.

**주의:** 생성 실패를 표현하는 방법으로 `std::expected`만 사용해야 하는 것은 아닙니다. 문맥에 따라 예외(Exception), `std::optional`, 오류 코드 등을 선택할 수 있습니다.

---

## 8.9. Delegating Constructor

위임 생성자(Delegating Constructor)는 한 생성자가 같은 클래스의 다른 생성자를 호출하는 방식입니다. 초기화 로직을 여러 곳에 반복하지 않도록 할 때 사용합니다.

**예제 코드 — [08_delegating_constructor.cpp](./examples/08_delegating_constructor.cpp)**

```cpp
#include <algorithm>
#include <print>

class RetryPolicy {
public:
    RetryPolicy() : RetryPolicy(3, 250) {}

    RetryPolicy(int attempts, int delay_ms) noexcept
        : attempts_{std::clamp(attempts, 1, 10)},
          delay_ms_{std::clamp(delay_ms, 0, 5'000)} {}

    [[nodiscard]] int attempts() const noexcept { return attempts_; }
    [[nodiscard]] int delay_ms() const noexcept { return delay_ms_; }

private:
    int attempts_{};
    int delay_ms_{};
};

int main() {
    const RetryPolicy defaults;
    const RetryPolicy custom{20, 600};
    std::println("Default: {} times, {} ms", defaults.attempts(), defaults.delay_ms());
    std::println("Custom: {} times, {} ms", custom.attempts(), custom.delay_ms());
}
```

**실행 결과**

```text
Default: 3 times, 250 ms
Custom: 10 times, 600 ms
```

`RetryPolicy()`는 `RetryPolicy(3, 250)`으로 초기화를 위임합니다. 다른 생성자에서는 `std::clamp`로 요청값을 허용 범위로 제한합니다.

이처럼 **값을 자동 보정할지, 입력 자체를 거부할지**는 정책에 따라 결정해야 합니다. 예상하지 못한 설정이 오류를 나타낸다면 조용히 보정하기보다 오류를 반환하는 것이 적절할 수 있습니다.

---

## 8.10. Composition과 객체 간 관계

합성(Composition)은 클래스가 다른 객체를 멤버로 포함해 기능을 구성하는 방식입니다. `Monitor`가 `SensorLog`를 소유하는 관계처럼 **포함하는 객체와 포함된 객체의 수명(Lifetime)이 연결**될 때 유용합니다.

상속을 사용하지 않아도 작은 역할의 클래스를 조합해 시스템을 만들 수 있습니다.

**예제 코드 — [09_composition.cpp](./examples/09_composition.cpp)**

```cpp
#include <cmath>
#include <optional>
#include <print>
#include <vector>

class SensorLog {
public:
    [[nodiscard]] bool add(double value) {
        if (!std::isfinite(value)) {
            return false;
        }
        samples_.push_back(value);
        return true;
    }

    [[nodiscard]] std::optional<double> average() const noexcept {
        if (samples_.empty()) {
            return std::nullopt;
        }
        double total{};
        for (const double value : samples_) {
            total += value;
        }
        return total / static_cast<double>(samples_.size());
    }

private:
    std::vector<double> samples_;
};

class Monitor {
public:
    [[nodiscard]] bool record(double value) { return log_.add(value); }
    [[nodiscard]] std::optional<double> average() const noexcept { return log_.average(); }

private:
    SensorLog log_;
};

int main() {
    Monitor monitor;
    const bool first = monitor.record(20.0);
    const bool second = monitor.record(24.0);
    if (!first || !second) {
        std::println("Invalid sample");
        return 1;
    }
    if (const auto avg = monitor.average()) {
        std::println("Average: {:.1f} C", *avg);
    }
}
```

**실행 결과**

```text
Average: 22.0 C
```

`SensorLog`는 검증과 데이터 저장을 담당하고, `Monitor`는 이를 호출자에게 제공하는 역할을 합니다.

- **`SensorLog`:** 측정값 저장 및 평균 계산
- **`Monitor`:** 외부에 제공하는 작업 인터페이스
- **`std::optional`:** 측정값이 없을 때 평균값이 존재하지 않음을 표현

`SensorLog`에서 측정값 합산은 `double`을 사용합니다. 입력 규모나 정밀도 요구가 큰 시스템에서는 누적 오차와 최대값을 고려한 별도의 계산 정책이 필요합니다.

---

## 8.11. Static Member와 객체 수명

정적 멤버(Static Member)는 객체마다 별도로 존재하는 멤버와 달리 클래스 단위로 공유되는 상태 또는 동작을 표현합니다. C++17부터 `inline static` 데이터 멤버를 클래스 내부에서 정의할 수 있습니다.

다음 예제는 객체가 생성되면 활성 개수를 늘리고 소멸하면 줄입니다.

**예제 코드 — [10_static_members.cpp](./examples/10_static_members.cpp)**

```cpp
#include <print>

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
    std::println("Before: {}", Connection::active_count());
    {
        Connection first;
        Connection second;
        std::println("Inside: {}", Connection::active_count());
    }
    std::println("After: {}", Connection::active_count());
}
```

**실행 결과**

```text
Before: 0
Inside: 2
After: 0
```

- **`inline static int active_`:** 클래스 전체에서 공유하는 카운터
- **생성자:** 객체가 만들어지면 1 증가
- **소멸자(Destructor):** 객체 Lifetime이 끝나면 1 감소
- **복사·이동 삭제:** 객체가 중복으로 계산되는 실수를 예방하기 위한 예제의 단순화

위 코드는 단일 스레드를 전제로 합니다. 여러 스레드에서 동시에 객체를 생성·삭제한다면 공유 상태를 동기화해야 하며, 이러한 동시성 처리는 별도 고급 과정에서 다룹니다.

**주의:** 소멸자에서 자원을 정리하는 원칙은 중요하지만, 모든 클래스에 소멸자를 직접 작성하는 것은 권장하지 않습니다. 대부분은 `std::vector`, `std::string`, 스마트 포인터 등의 소유 객체에 맡기는 편이 안전합니다.

---

## 8.12. 객체 비교와 `operator==`

서로 다른 두 객체가 같은 값으로 판단되어야 한다면 비교 연산자를 정의할 수 있습니다. C++20부터는 조건을 충족하는 클래스에서 `operator==`를 `= default`로 선언해 멤버별 동등 비교를 생성할 수 있습니다.

**예제 코드 — [11_defaulted_comparison.cpp](./examples/11_defaulted_comparison.cpp)**

```cpp
#include <print>

struct DeviceKey {
    int rack{};
    int slot{};

    [[nodiscard]] bool operator==(const DeviceKey&) const = default;
};

int main() {
    const DeviceKey a{2, 7};
    const DeviceKey b{2, 7};
    const DeviceKey c{2, 8};
    std::println("a == b: {}", a == b);
    std::println("a == c: {}", a == c);
}
```

**실행 결과**

```text
a == b: true
a == c: false
```

기본 비교는 멤버에 대한 동등 비교에 기반합니다. 따라서 **모든 필드가 같으면 같은 객체로 볼 것인지** 먼저 결정해야 합니다. 예를 들어 장치 ID만으로 동일성을 판단해야 하는 모델에는 모든 멤버 비교가 적절하지 않을 수 있습니다.

부동소수점 값은 반올림 오차가 있으므로 `==`로 비교하기 전에 해당 데이터의 의미와 정확도 요구를 검토해야 합니다.

---

## 8.13. `this`와 Method Chaining

멤버 함수 안에서 `this`는 현재 객체를 가리키는 포인터입니다. `*this`를 참조로 반환하면 메서드 체이닝(Method Chaining) 형태로 설정을 이어서 호출할 수 있습니다.

**예제 코드 — [12_this_and_fluent_api.cpp](./examples/12_this_and_fluent_api.cpp)**

```cpp
#include <algorithm>
#include <print>

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
    std::println("Alarm at 70: {}", config.triggered(70));
}
```

**실행 결과**

```text
Alarm at 70: true
```

`set_threshold()`와 `enable()`은 `AlarmConfig&`를 반환하므로 `config.set_threshold(65).enable(true)`처럼 사용할 수 있습니다.

반환된 참조는 원본 객체의 Lifetime에 의존합니다. 일시 객체나 종료된 객체의 참조를 장기간 보관하는 설계는 피해야 합니다. Fluent API는 호출 문장을 읽기 쉽게 만들지만, 순서에 따라 부수 효과가 큰 메서드에서는 오히려 혼동을 초래할 수 있습니다.

---

## 8.14. 헤더·구현 파일 분리

규모가 커지면 인터페이스와 구현을 구분하는 것이 유리합니다. 일반적으로 `.hpp`에는 클래스 선언을, `.cpp`에는 멤버 함수 정의를 배치합니다. 사용자는 헤더를 포함하고 구현 소스는 빌드 단계에서 함께 컴파일·링크합니다.

| 파일 | 역할 |
|---|---|
| `13_device_registry.hpp` | 공개 인터페이스, 멤버 선언 |
| `13_device_registry.cpp` | 멤버 함수 정의 및 내부 알고리즘 |
| `13_device_registry_main.cpp` | 클래스 사용 예시 |

아래 파일은 단독으로 각각 실행할 수 없으며, 구현 파일과 `main()` 파일을 함께 빌드해야 합니다.

**[13_device_registry.hpp](./examples/13_device_registry.hpp)**

```cpp
#pragma once

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
```

**[13_device_registry.cpp](./examples/13_device_registry.cpp)**

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

**[13_device_registry_main.cpp](./examples/13_device_registry_main.cpp)**

```cpp
#include "13_device_registry.hpp"

#include <print>

int main() {
    DeviceRegistry registry;
    const bool first = registry.add("CAM-01");
    const bool duplicate = registry.add("CAM-01");
    const bool second = registry.add("LIDAR-02");
    std::println("First: {}, duplicate: {}, second: {}", first, duplicate, second);
    std::println("Registered: {}", registry.size());
}
```

**컴파일 및 실행 — GCC / Clang**

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic \
  examples/13_device_registry.cpp examples/13_device_registry_main.cpp -o registry
./registry
```

**MSVC — Developer Command Prompt**

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 examples\13_device_registry.cpp examples\13_device_registry_main.cpp /Fe:registry.exe
registry.exe
```

**실행 결과**

```text
First: true, duplicate: false, second: true
Registered: 2
```

- **`#pragma once`:** 중복 포함 방지를 위한 널리 지원되는 확장 문법. 표준 문법만으로 처리하려면 Include Guard 사용
- **`DeviceRegistry::add`:** 클래스 외부에서 멤버 함수 구현
- **`std::move(id)`:** 등록 문자열을 내부 컨테이너로 이동
- **단일 정의 규칙(One Definition Rule, ODR):** ODR은 함수와 객체의 정의 배치에 관련된 규칙. 헤더에 일반 함수 정의를 반복해서 넣으면 링크 문제가 발생할 수 있음

실제 프로젝트에서는 여러 소스 파일을 CMake 등의 빌드 시스템으로 관리하는 편이 편리합니다. 프로젝트 구성과 빌드 자동화는 이후 고급 과정에서 다룹니다.

---

## 8.15. Copy, Move와 Rule of Zero

일반적인 클래스는 멤버 객체들이 복사(Copy)·이동(Move)할 수 있는 경우 별도 코드를 작성하지 않아도 기본 복사·이동 동작을 활용할 수 있습니다.

제로의 규칙(Rule of Zero)은 가능하면 소멸자, 복사 생성자, 이동 생성자, 대입 연산자를 직접 관리하지 않고 자원 관리를 표준 라이브러리 객체에 맡기는 설계 원칙입니다.

**예제 코드 — [14_rule_of_zero.cpp](./examples/14_rule_of_zero.cpp)**

```cpp
#include <print>
#include <string>
#include <utility>
#include <vector>

class JobQueue {
public:
    void add(std::string job) {
        jobs_.push_back(std::move(job));
    }

    [[nodiscard]] std::size_t size() const noexcept {
        return jobs_.size();
    }

private:
    std::vector<std::string> jobs_;
};

int main() {
    JobQueue original;
    original.add("Scan");

    JobQueue copied = original;
    JobQueue moved = std::move(original);

    std::println("Copied: {}, moved: {}", copied.size(), moved.size());
    // 이동 후 original은 유효하지만 내부 요소 개수를 가정하지 않음.
}
```

**실행 결과**

```text
Copied: 1, moved: 1
```

- **Copy:** `JobQueue copied = original;` — `std::vector`와 문자열들이 별도로 복사됨
- **Move:** `JobQueue moved = std::move(original);` — 이동 생성자의 사용을 허용함
- **이동 후 객체:** 유효하지만 내부에 남은 요소 개수 등은 가정하지 않음

`std::move()`는 데이터를 강제로 이동하는 함수가 아니라 이동 가능한 표현식으로 바꾸는 도구입니다. 실제 이동 여부는 해당 자료형의 생성자·대입 동작에 따릅니다.

특별한 자원 관리 규칙이 필요하다면 직접 복사/이동 정책을 설계할 수 있지만, 포인터를 수동으로 `new`·`delete`하는 코드를 기본 패턴으로 삼지 않습니다. 명시적 소유권(Ownership)이 필요하면 Chapter 07의 `std::unique_ptr`와 `std::shared_ptr`를 참고합니다.

---

## 8.16. 실무 설계 원칙 및 오류 사례

| 상황 | 권장 접근 | 주의점 |
|---|---|---|
| 단순 측정값 묶음 | `struct` + 기본 멤버 초기화 | 유효하지 않은 데이터가 외부로 전달되지 않도록 계약 명시 |
| 범위 제한이 필요한 상태 | `class` + 검증 메서드 | 공개 필드로 Class Invariant 우회 금지 |
| 생성 자체가 실패할 수 있음 | Factory Method + `std::expected` | 실패 원인 구분 및 원자적인 상태 변경 |
| 부품을 포함하는 시스템 | Composition | 소유 객체와 비소유 참조의 Lifetime 구분 |
| 문자열·배열 보유 | `std::string`, `std::vector` | 불필요한 수동 메모리 관리 지양 |
| 조회 전용 API | `const` 멤버 함수, `std::string_view` | 비소유 뷰(View)의 원본 Lifetime 확인 |
| 여러 구현 파일 | 헤더 선언과 `.cpp` 정의 | ODR 및 링크 오류 예방 |
| 공유 상태 | Static Member 또는 명시적 공유 객체 | 전역 상태와 동시성 문제 고려 |

### 흔한 오류

```cpp
// 1) 생성 전에 범위 검증이 필요한 상태를 public으로 노출
struct UnsafeMotor { int rpm; };
UnsafeMotor motor{-200};

// 2) 생성자 본문 안에서 객체 초기화와 대입을 혼동
// 실제 멤버는 본문 진입 전에 이미 초기화됨.

// 3) 원본보다 오래 살아남는 View 또는 참조를 멤버에 보관
// 반환·이동·컨테이너 재할당 시 Lifetime 확인 필요.
```

**성능 관련 참고:** `struct`가 `class`보다 본질적으로 빠르거나 작지는 않습니다. 메모리 배치, 동적 할당, 복사 비용, 알고리즘, 최적화 설정 등 실제 사용 조건에 따라 성능이 달라집니다. 성능 개선은 측정 결과에 근거해 진행하는 것이 좋습니다.

**Chapter 09와의 구분:** 본 Chapter는 객체의 데이터·상태·생성과 Composition에 집중합니다. 상속, 가상 함수, 런타임 다형성 등은 Chapter 09에서 학습합니다.

---

## 8.17. Coding Practice

문제별 기본 코드는 `exercises/`에, 모범답안은 `solutions/`에 저장되어 있습니다. 기본 코드는 `TODO`를 완성하도록 작성되어 있으며, 그대로 실행해도 정답 동작을 보장하지 않습니다.

### 실습 ① — Device Profile Validation

**목표:** 장치 프로필의 기본 입력값 검증

**조건**

- `DeviceProfile`의 `name`은 비어 있으면 안 됨
- 소비 전력 `power_w`는 0~2000W 허용
- `online` 여부는 유효성 조건에 포함하지 않음

**입력 예시 / 기대 결과**

| 장치 이름 | 전력(W) | 결과 |
|---|---:|---|
| `Vacuum-A` | 850 | `true` |
| 빈 문자열 | 850 | `false` |
| `Vacuum-A` | -1 | `false` |
| `Vacuum-A` | 2001 | `false` |

[연습문제 — 01_device_profile.cpp](./exercises/01_device_profile.cpp) · [정답 코드 — 01_device_profile.cpp](./solutions/01_device_profile.cpp)

### 실습 ② — Bank Account

**목표:** 금액을 정수 단위로 저장하는 클래스 설계

**조건**

- `balance_cents_`는 `private` 멤버
- 입금·출금은 양수 금액만 허용
- 출금 금액이 잔액보다 크면 거절
- 입금 시 `std::int64_t` 범위 초과를 검사
- 실패 시 기존 잔액 유지

**기대 결과** (`10000`센트에서 시작해 `2500` 입금, `4000` 출금)

```text
Deposit: true, withdraw: true, balance: 8500 cents
```

[연습문제 — 02_bank_account.cpp](./exercises/02_bank_account.cpp) · [정답 코드 — 02_bank_account.cpp](./solutions/02_bank_account.cpp)

### 실습 ③ — Temperature Window

**목표:** Factory Method와 Class Invariant 적용

**조건**

- `lower`, `upper`가 유한한 숫자인지 확인
- `lower <= upper`인 경우에만 객체 생성
- 잘못된 경우 `std::unexpected("Invalid temperature range")` 반환
- `contains()` 역시 유한한 값만 허용

**정상 실행 결과**

```text
23 C allowed: true
```

[연습문제 — 03_temperature_window.cpp](./exercises/03_temperature_window.cpp) · [정답 코드 — 03_temperature_window.cpp](./solutions/03_temperature_window.cpp)

### 실습 ④ — Robot Battery System

**목표:** Composition으로 로봇 이동과 배터리 상태 관리

**조건**

- 1~1000m 사이의 이동 요청만 허용
- 이동 거리 5m마다 배터리 1% 소모, 나머지가 있으면 올림
- 배터리가 부족한 경우 요청 거절 및 기존 잔량 유지
- 배터리 잔량은 직접 수정하지 않고 `Battery`의 메서드 사용

**기대 결과** (25m 이동 후 1000m 이동 요청)

```text
Short: true, long: false, battery: 95%
```

[연습문제 — 04_robot_battery.cpp](./exercises/04_robot_battery.cpp) · [정답 코드 — 04_robot_battery.cpp](./solutions/04_robot_battery.cpp)

### 컴파일 및 실행

`Chapter-08/` 폴더에서 실행합니다. `exercises/`에 있는 파일은 `TODO` 미완성 상태이므로 정답 코드의 출력과 다를 수 있습니다.

**GCC**

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -O2 \
  solutions/01_device_profile.cpp -o device_profile
./device_profile
```

**Clang** — C++23 표준 라이브러리 기능 지원 환경

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic -O2 \
  solutions/01_device_profile.cpp -o device_profile
./device_profile
```

**MSVC** — Developer Command Prompt

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 solutions\01_device_profile.cpp /Fe:device_profile.exe
device_profile.exe
```

`/std:c++23` 또는 `/std:c++23preview` 지원 여부는 MSVC 도구 집합 버전에 따라 다릅니다. 특히 `<print>` 및 `<expected>`의 지원 범위도 확인해야 합니다.

---

## 8.18. Quiz & Summary

### Quiz

1. C++에서 `struct`와 `class`의 기본 멤버 접근 권한은 어떻게 다른가요?
2. Designated Initializer를 사용할 때 C++에서 멤버 순서를 바꿔도 되나요?
3. `explicit` 생성자를 사용하는 목적은 무엇인가요?
4. Member Initializer List의 나열 순서와 실제 멤버 초기화 순서는 항상 같은가요?
5. `const` 멤버 함수는 어떤 접근을 제한하나요?
6. Class Invariant를 유지하는 데 Factory Method가 유용한 이유는 무엇인가요?
7. Composition과 상속은 같은 개념인가요?
8. Static Member는 각 객체마다 별도로 존재하나요?
9. `std::move()`를 호출하면 항상 데이터를 실제로 이동하나요?
10. 헤더에 일반 함수 정의를 무분별하게 넣으면 어떤 문제가 생길 수 있나요?

<details>
<summary>정답 확인</summary>

1. `struct`는 기본 `public`, `class`는 기본 `private`임.
2. 아니요. C++에서는 멤버 선언 순서를 따라야 함.
3. 의도하지 않은 암묵적 변환을 방지하기 위해 사용.
4. 아니요. 실제 순서는 클래스 내 멤버 선언 순서에 따름.
5. 해당 함수를 통한 일반적인 멤버 상태 변경을 제한함.
6. 객체 생성 전에 입력값을 검증하고 실패 이유를 반환할 수 있기 때문.
7. 아니요. Composition은 다른 객체를 멤버로 포함하는 관계이고, 상속은 별도 관계임.
8. 아니요. 클래스 수준에서 공유되는 데이터임.
9. 아니요. 이동 가능한 표현식으로 만드는 도구이며 실제 동작은 자료형에 따름.
10. ODR 위반 또는 중복 정의로 인한 링크 오류 등이 발생할 수 있음.

</details>

### Summary

- **`struct`와 `class`:** 기본 접근 권한이 다른 사용자 정의 자료형
- **Aggregate Initialization:** 조건에 맞는 자료형을 멤버 단위로 초기화
- **Designated Initializer:** 이름을 사용한 명시적 멤버 초기화
- **Encapsulation:** 내부 상태와 공개 인터페이스 구분
- **Constructor / `explicit`:** 객체 초기 상태 설정과 암묵적 변환 제어
- **Member Initializer List:** 생성자 본문 전에 멤버 직접 초기화
- **Class Invariant:** 객체가 유지해야 하는 유효 상태의 규칙
- **Factory Method / `std::expected`:** 검증된 객체 생성 및 실패 이유 반환
- **Composition:** 작은 역할의 객체를 합쳐 시스템 구성
- **Static Member:** 클래스 단위의 공유 데이터와 메서드
- **Rule of Zero:** 자원 수명 관리를 표준 객체에 위임
- **헤더·구현 분리:** 인터페이스와 구현을 구분하고 빌드 단위 관리

### References

- [cppreference — Classes](https://en.cppreference.com/w/cpp/language/classes)
- [cppreference — Aggregate Initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization)
- [cppreference — Constructors](https://en.cppreference.com/w/cpp/language/constructor)
- [cppreference — Access Specifiers](https://en.cppreference.com/w/cpp/language/access)
- [cppreference — `std::expected`](https://en.cppreference.com/w/cpp/utility/expected)
- [cppreference — Member Functions](https://en.cppreference.com/w/cpp/language/member_functions)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

---

[← C++ 목차](../README.md) · [Chapter 07 — Pointers & References](../Chapter-07/)
