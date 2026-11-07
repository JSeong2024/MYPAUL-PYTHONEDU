# Chapter 09. Object-Oriented Programming

상속, 다형성, 가상 함수, 추상 클래스, 소유권 관리, 인터페이스 분리 및 테스트 가능한 객체 설계를 다룹니다. 센서·로봇 제어 시뮬레이션을 통해 **확장 가능한 구조와 안전한 객체 수명 관리**를 학습합니다.

본 자료는 **C++23(ISO/IEC 14882:2024)** 을 기준으로 작성되었습니다. 예제는 GCC 14 이상 및 C++23 표준 라이브러리 기능을 지원하는 개발 환경을 권장합니다.

**선행 학습:** Chapter 05 — Functions, Chapter 07 — Pointers & References, Chapter 08 — Structs & Classes

## Contents

| Section | Topic |
|:---:|---|
| 9.1 | 객체지향 프로그래밍과 설계 목표 |
| 9.2 | 기본 클래스와 파생 클래스 |
| 9.3 | 접근 제어와 상속 관계 |
| 9.4 | 가상 함수와 Dynamic Dispatch |
| 9.5 | `override`, `final`과 정확한 재정의 |
| 9.6 | Abstract Class와 Interface |
| 9.7 | Virtual Destructor와 객체의 수명 |
| 9.8 | Ownership과 다형적 객체 컨테이너 |
| 9.9 | Object Slicing과 값 전달 |
| 9.10 | 타입 변환과 `dynamic_cast` |
| 9.11 | Inheritance보다 Composition이 적절한 경우 |
| 9.12 | Interface Segregation과 역할 분리 |
| 9.13 | Non-Virtual Interface와 검증 |
| 9.14 | Dependency Injection과 테스트 대역 |
| 9.15 | 동적 다형성과 `std::variant` 비교 |
| 9.16 | 생성자·소멸자에서 Virtual Function 호출 |
| 9.17 | Mini Project — Robot Sensor Monitor |
| 9.18 | 성능·안전성·설계 점검 |
| 9.19 | Coding Practice |
| 9.20 | Quiz & Summary |

---

## 9.1. 객체지향 프로그래밍과 설계 목표

객체지향 프로그래밍(Object-Oriented Programming, OOP)은 데이터를 객체에 묶는 것만을 의미하지 않습니다. 책임을 나누고, 변경 가능한 구현 세부사항을 숨기며, 서로 다른 구현을 공통된 계약으로 교체할 수 있도록 설계하는 방법입니다.

Chapter 08에서 클래스의 생성과 초기화, 캡슐화(Encapsulation), 합성(Composition)을 다뤘습니다. 이번 Chapter에서는 **상속(Inheritance)**, **다형성(Polymorphism)**, 그리고 인터페이스(Interface) 설계를 연결합니다.

| 개념 | 역할 | 대표 사례 |
|---|---|---|
| Encapsulation | 데이터와 상태 변경 규칙 보호 | 모터 속도 변경 범위 제한 |
| Inheritance | 공통 성격의 타입 관계 표현 | `Device`에서 `TemperatureSensor` 파생 |
| Polymorphism | 공통 인터페이스로 서로 다른 구현 실행 | 동일한 `read()` 호출로 센서별 데이터 취득 |
| Composition | 객체가 다른 객체를 구성 요소로 소유 | `Robot` 내부에 `Motor` 보유 |
| Interface | 외부에 필요한 동작만 노출 | `IReadingSource::read()` |

C++의 OOP는 상속만으로 구현되지 않습니다. 값 타입(Value Type), 함수, 템플릿, Composition으로도 충분한 경우가 많습니다. **상속은 실제로 대체 가능한 타입 관계가 있을 때 선택**하는 것이 좋습니다.

---

## 9.2. 기본 클래스와 파생 클래스

기본 클래스(Base Class)는 공통 상태와 기능을 정의하고, 파생 클래스(Derived Class)는 이를 확장할 수 있습니다. `class Derived : public Base`는 공개 상속(Public Inheritance)을 의미합니다.

아래 예제에서 `TemperatureSensor`는 `Device`의 `id()` 기능을 재사용합니다. 공통 식별자를 새로 복사해 관리하지 않으므로 데이터의 중복을 줄일 수 있습니다.

- **`public` 상속:** `Base`의 공개 인터페이스를 `Derived`의 공개 인터페이스로 유지
- **기본 클래스 생성자:** 파생 클래스 본문보다 먼저 실행
- **멤버 접근:** 기본 클래스의 `private` 멤버는 파생 클래스에서 직접 접근 불가
- **관계 판단:** `TemperatureSensor`는 `Device`의 한 종류인가?라는 질문에 자연스럽게 답할 수 있어야 함

기능을 단순히 재사용하려는 이유만으로 상속하는 것은 피합니다. `Robot`과 `Motor`처럼 포함 관계라면 뒤에서 다룰 Composition이 더 적절합니다.

**예제 코드 — [01_inheritance_basics.cpp](./examples/01_inheritance_basics.cpp)**

```cpp
#include <print>
#include <string>
#include <string_view>
#include <utility>

class Device {
public:
    explicit Device(std::string id) : id_(std::move(id)) {}
    [[nodiscard]] std::string_view id() const noexcept { return id_; }

private:
    std::string id_;
};

class TemperatureSensor : public Device {
public:
    TemperatureSensor(std::string id, double celsius)
        : Device(std::move(id)), celsius_(celsius) {}

    [[nodiscard]] double read_celsius() const noexcept { return celsius_; }

private:
    double celsius_{};
};

int main() {
    const TemperatureSensor sensor{"TEMP-01", 24.5};
    std::println("{}: {:.1f} C", sensor.id(), sensor.read_celsius());
}
```

**실행 결과**

```text
TEMP-01: 24.5 C
```

`Device`의 식별자를 반환하는 메서드가 공개되어 있어도 `id_` 자체는 `private`입니다. 파생 클래스에서 공통 상태를 임의로 변경하는 대신 기본 클래스가 제공하는 인터페이스를 사용합니다.

---

## 9.3. 접근 제어와 상속 관계

상속 관계에서 `public`, `protected`, `private`은 **멤버에 대한 접근**을 제어합니다. `protected`는 해당 클래스와 파생 클래스 내부에서 접근 가능하지만 외부에서는 접근할 수 없습니다.

| 접근 지정자 | 클래스 내부 | 파생 클래스 | 외부 코드 |
|---|:---:|:---:|:---:|
| `public` | O | O | O |
| `protected` | O | O | X |
| `private` | O | X | X |

아래 예제는 `FanController`에 허용된 조작 함수만 노출하고, 실제 상태 변경은 `Controller`의 `protected` 메서드로 제한합니다. `using Controller::Controller;`는 기반 클래스의 생성자를 상속받는 문법입니다.

**주의:** `protected`는 구현 세부사항을 파생 클래스에 노출합니다. 외부 확장을 허용해야 할 근거가 없다면 `private`과 공개 또는 제한된 인터페이스를 우선 고려합니다.

**예제 코드 — [02_access_control.cpp](./examples/02_access_control.cpp)**

```cpp
#include <print>
#include <string>
#include <string_view>
#include <utility>

class Controller {
public:
    explicit Controller(std::string name) : name_(std::move(name)) {}
    [[nodiscard]] std::string_view name() const noexcept { return name_; }
    [[nodiscard]] bool enabled() const noexcept { return enabled_; }

protected:
    void set_enabled(bool value) noexcept { enabled_ = value; }

private:
    std::string name_;
    bool enabled_{false};
};

class FanController final : public Controller {
public:
    using Controller::Controller;
    void start() noexcept { set_enabled(true); }
    void stop() noexcept { set_enabled(false); }
};

int main() {
    FanController fan{"Fan-A"};
    fan.start();
    std::println("{} enabled: {}", fan.name(), fan.enabled());
}
```

**실행 결과**

```text
Fan-A enabled: true
```

---

## 9.4. 가상 함수와 Dynamic Dispatch

가상 함수(Virtual Function)는 기본 클래스의 포인터나 참조로 호출해도 실제 객체 타입의 재정의된 함수를 실행할 수 있게 합니다. 이러한 실행 시점 선택을 **동적 디스패치(Dynamic Dispatch)**라고 합니다.

일반적인 비가상 함수는 정적 타입에 따라 호출 대상이 결정됩니다. 반면 Virtual Function은 기반 클래스 참조로 `OnlineSensor`를 전달해도 실제 객체의 `status()`가 호출됩니다.

**동작 순서**

1. `report(const StatusSource&)`가 기반 클래스 참조를 받음
2. `source.status()`에서 Virtual Function 호출
3. 실제 객체 `OnlineSensor`의 재정의된 구현 실행

일부 구현체는 가상 함수 테이블(Virtual Function Table, VTable)로 이를 구현하지만, **C++ 표준이 VTable이라는 특정 자료구조를 요구하지는 않습니다.** 가상 호출에는 간접 호출 비용과 최적화 제약이 생길 수 있으므로, 대체 가능한 구현이 필요할 때 사용하는 것이 좋습니다.

**예제 코드 — [03_virtual_dispatch.cpp](./examples/03_virtual_dispatch.cpp)**

```cpp
#include <print>
#include <string_view>

class StatusSource {
public:
    virtual ~StatusSource() = default;
    [[nodiscard]] virtual std::string_view status() const noexcept {
        return "unknown";
    }
};

class OnlineSensor final : public StatusSource {
public:
    [[nodiscard]] std::string_view status() const noexcept override {
        return "online";
    }
};

void report(const StatusSource& source) {
    std::println("Sensor status: {}", source.status());
}

int main() {
    const OnlineSensor sensor;
    report(sensor);  // 기반 클래스 참조로 전달
}
```

**실행 결과**

```text
Sensor status: online
```

---

## 9.5. `override`, `final`과 정확한 재정의

오버라이딩(Overriding)은 파생 클래스가 기반 클래스의 Virtual Function을 다시 구현하는 동작입니다. `override`는 의도한 재정의가 실제로 성립하는지 컴파일러가 확인하도록 합니다.

- **`virtual`:** 기반 클래스에서 가상 동작을 선언
- **`override`:** 기반 클래스의 가상 함수를 정확히 재정의했는지 검사
- **`final`:** 해당 메서드의 추가 재정의 또는 클래스의 추가 상속을 차단
- **반환 자료형만 변경:** 일반적으로 같은 함수의 Overriding이 되지 않음. 일부 포인터·참조 반환에는 공변 반환형(Covariant Return Type) 예외 존재

```cpp
class Base {
public:
    virtual ~Base() = default;
    virtual void start() const {}
};

class Derived : public Base {
public:
    // void start() override {}  // const가 달라 컴파일 오류
    void start() const override {}
};
```

`override`를 생략하면 의도하지 않은 함수 숨김이나 잘못된 재정의를 놓칠 수 있습니다. 재정의 함수에는 `override`를 명시하고, `final`은 **추가 상속 또는 재정의를 제한해야 할 때** 사용합니다.

**예제 코드 — [04_override_and_final.cpp](./examples/04_override_and_final.cpp)**

```cpp
#include <print>
#include <string_view>

class Alarm {
public:
    virtual ~Alarm() = default;
    [[nodiscard]] virtual std::string_view message() const = 0;
};

class TemperatureAlarm final : public Alarm {
public:
    [[nodiscard]] std::string_view message() const override {
        return "Temperature limit exceeded";
    }
};

int main() {
    const TemperatureAlarm alarm;
    const Alarm& base = alarm;
    std::println("{}", base.message());
}
```

**실행 결과**

```text
Temperature limit exceeded
```

---

## 9.6. Abstract Class와 Interface

추상 클래스(Abstract Class)는 하나 이상의 순수 가상 함수(Pure Virtual Function)를 포함하는 클래스입니다. `= 0`으로 선언한 순수 가상 함수가 있으면 해당 추상 클래스는 직접 인스턴스를 만들 수 없습니다.

인터페이스(Interface)는 호출자가 의존할 **기능의 계약**을 표현합니다. C++에는 `interface` 전용 키워드가 없지만, 순수 가상 함수로 구성된 클래스를 관례적으로 Interface로 사용합니다.

아래 `IReadingSource`는 센서의 종류와 관계없이 `read()` 결과를 받을 수 있게 합니다.

- **계약:** `read()`는 값이 존재할 때 `double`, 읽기 실패 시 `std::nullopt`를 표현
- **구현:** `SimulatedTemperature`가 데이터 취득 동작을 제공
- **사용자:** `display()`는 구체적인 센서 타입을 몰라도 동작

`std::optional`이 실패 이유까지 전달하지는 않습니다. 연결 실패·형식 오류 등 원인이 필요하다면 `std::expected<T, E>` 또는 별도 오류 모델을 고려합니다.

**예제 코드 — [05_abstract_interface.cpp](./examples/05_abstract_interface.cpp)**

```cpp
#include <optional>
#include <print>

class IReadingSource {
public:
    virtual ~IReadingSource() = default;
    [[nodiscard]] virtual std::optional<double> read() const = 0;
};

class SimulatedTemperature final : public IReadingSource {
public:
    explicit SimulatedTemperature(double value) : value_(value) {}
    [[nodiscard]] std::optional<double> read() const override {
        return value_;
    }

private:
    double value_;
};

void display(const IReadingSource& source) {
    if (const auto result = source.read()) {
        std::println("Reading: {:.1f} C", *result);
    } else {
        std::println("Reading unavailable");
    }
}

int main() {
    const SimulatedTemperature sensor{22.5};
    display(sensor);
}
```

**실행 결과**

```text
Reading: 22.5 C
```

---

## 9.7. Virtual Destructor와 객체의 수명

소멸자(Destructor)는 객체의 수명(Lifetime)이 끝날 때 호출됩니다. **기반 클래스 포인터로 파생 객체를 삭제하는 경우**, 기반 클래스의 소멸자는 일반적으로 가상 소멸자(Virtual Destructor)여야 합니다.

`std::unique_ptr<Base>`가 파생 객체를 소유하고 기본 삭제자를 사용한다면, 기반 클래스에 적절한 Virtual Destructor가 없을 때 삭제 과정이 **미정의 동작(Undefined Behavior, UB)**에 해당할 수 있습니다.

```cpp
class Interface {
public:
    virtual ~Interface() = default;
    virtual void run() = 0;
};
```

아래 예제에서 실제 소멸 순서는 `SerialConnection` → `Connection`입니다. 동적 메모리 관리에 `delete`를 직접 쓰지 않고 스마트 포인터(Smart Pointer)로 객체의 수명을 관리합니다.

**참고:** 기반 클래스 소멸자는 보통 `public virtual`로 선언합니다. 다만 기반 클래스 포인터를 통한 삭제를 허용하지 않는 설계라면 `protected` 비가상 소멸자도 고려할 수 있습니다. 상속이 가능하다는 이유만으로 모든 클래스에 Virtual Destructor를 추가할 필요는 없습니다.

**예제 코드 — [06_virtual_destructor.cpp](./examples/06_virtual_destructor.cpp)**

```cpp
#include <memory>
#include <print>

class Connection {
public:
    virtual ~Connection() { std::println("Connection closed"); }
    virtual void send() const = 0;
};

class SerialConnection final : public Connection {
public:
    ~SerialConnection() override { std::println("Serial resource released"); }
    void send() const override { std::println("Sending packet"); }
};

int main() {
    std::unique_ptr<Connection> connection =
        std::make_unique<SerialConnection>();
    connection->send();
}  // 파생 클래스 소멸자부터 순서대로 호출
```

**실행 결과**

```text
Sending packet
Serial resource released
Connection closed
```

---

## 9.8. Ownership과 다형적 객체 컨테이너

소유권(Ownership)은 객체를 누가 생성하고 수명을 끝낼 책임이 있는지에 대한 개념입니다. 여러 종류의 객체를 하나의 컬렉션에 보관하면서 소유해야 한다면 `std::vector<std::unique_ptr<Base>>`가 자주 사용됩니다.

- `std::make_unique<Derived>()` — 파생 객체 생성 및 단독 소유
- `std::unique_ptr<Base>` — 기반 클래스 포인터로 파생 객체 수명 관리
- `std::move` — Ownership 이전 시 사용
- `const Base&` — 객체를 소유하지 않고 읽거나 호출하는 경우 사용

아래 명령 실행 예제는 `ICommand`에 의존하므로 명령 종류가 추가되어도 반복 실행 코드를 변경하지 않아도 됩니다.

**주의:** `std::shared_ptr`은 실제 공유 Ownership이 필요한 상황에서만 사용합니다. 단순한 함수 호출이나 임시 접근에는 참조·비소유 포인터를 우선 고려합니다.

**예제 코드 — [07_polymorphic_collection.cpp](./examples/07_polymorphic_collection.cpp)**

```cpp
#include <memory>
#include <print>
#include <vector>

class ICommand {
public:
    virtual ~ICommand() = default;
    virtual void execute() const = 0;
};

class StopMotor final : public ICommand {
public:
    void execute() const override { std::println("Motor: stop"); }
};

class TurnOnLight final : public ICommand {
public:
    void execute() const override { std::println("Light: on"); }
};

int main() {
    std::vector<std::unique_ptr<ICommand>> commands;
    commands.push_back(std::make_unique<StopMotor>());
    commands.push_back(std::make_unique<TurnOnLight>());

    for (const auto& command : commands) {
        command->execute();
    }
}
```

**실행 결과**

```text
Motor: stop
Light: on
```

---

## 9.9. Object Slicing과 값 전달

객체 슬라이싱(Object Slicing)은 파생 객체를 **기반 클래스 값 객체로 복사**하면서 파생 클래스에 해당하는 정보가 잘리는 현상입니다.

```cpp
void process(Device device);         // Object Slicing 발생 가능
void process(const Device& device);  // 원본 객체의 동적 타입 유지
```

컴파일이 성공하더라도 프로그램이 기대한 파생 동작을 실행하지 않을 수 있습니다. 여러 타입을 공통 인터페이스로 다루려면 값 전달 대신 참조·포인터를 사용합니다.

값 타입의 복사가 필요하다면 파생 클래스까지 복제할 수 있는 별도의 `clone()` 계약을 설계할 수 있으나, 복제 비용과 Ownership을 함께 고려해야 합니다.

**예제 코드 — [08_object_slicing.cpp](./examples/08_object_slicing.cpp)**

```cpp
#include <print>
#include <string_view>

class Device {
public:
    virtual ~Device() = default;
    [[nodiscard]] virtual std::string_view type() const noexcept {
        return "Device";
    }
};

class Camera final : public Device {
public:
    [[nodiscard]] std::string_view type() const noexcept override {
        return "Camera";
    }
};

void by_value(Device device) {
    std::println("By value: {}", device.type());
}

void by_reference(const Device& device) {
    std::println("By reference: {}", device.type());
}

int main() {
    const Camera camera;
    by_value(camera);      // 파생 클래스 부분이 복사되지 않음
    by_reference(camera);  // 원본의 실제 타입 유지
}
```

**실행 결과**

```text
By value: Device
By reference: Camera
```

---

## 9.10. 타입 변환과 `dynamic_cast`

파생 클래스 객체를 기반 클래스 포인터 또는 참조로 취급하는 변환을 업캐스팅(Upcasting)이라고 합니다. 공개 상속에서 일반적으로 암묵적 변환이 가능합니다.

반대로 기반 클래스 포인터로부터 파생 클래스 타입을 확인하려는 동작을 다운캐스팅(Downcasting)이라고 합니다. `dynamic_cast`는 실행 시간 타입 식별(Runtime Type Information, RTTI)을 활용해 지원되는 타입 관계인지 검사합니다.

- **포인터 대상:** 실패하면 `nullptr` 반환
- **참조 대상:** 실패하면 `std::bad_cast` 예외 발생
- **전제:** 검사 대상 기반 타입은 일반적으로 다형적이어야 하며, RTTI 지원이 필요함

가능하면 Downcasting에 의존하지 않는 공통 Interface를 설계합니다. 특정 디버깅 기능처럼 파생 타입의 추가 기능이 꼭 필요할 때 제한적으로 사용합니다.

`static_cast<Derived*>`로 검사 없이 잘못된 Downcasting을 수행한 뒤 접근하면 UB가 발생할 수 있습니다.

**예제 코드 — [09_dynamic_cast.cpp](./examples/09_dynamic_cast.cpp)**

```cpp
#include <print>
#include <string_view>

class Device {
public:
    virtual ~Device() = default;
    [[nodiscard]] virtual std::string_view type() const noexcept = 0;
};

class DebugSensor final : public Device {
public:
    [[nodiscard]] std::string_view type() const noexcept override {
        return "DebugSensor";
    }
    [[nodiscard]] int error_count() const noexcept { return 2; }
};

class SimpleSensor final : public Device {
public:
    [[nodiscard]] std::string_view type() const noexcept override {
        return "SimpleSensor";
    }
};

void report(const Device& device) {
    if (const auto* debug = dynamic_cast<const DebugSensor*>(&device)) {
        std::println("{} errors: {}", device.type(), debug->error_count());
    } else {
        std::println("{} has no debug details", device.type());
    }
}

int main() {
    const DebugSensor debug;
    const SimpleSensor simple;
    report(debug);
    report(simple);
}
```

**실행 결과**

```text
DebugSensor errors: 2
SimpleSensor has no debug details
```

---

## 9.11. Inheritance보다 Composition이 적절한 경우

`Robot`은 `Motor`의 한 종류가 아니라 `Motor`를 **가지고 있는 객체**입니다. 이러한 포함 관계에는 Composition을 사용합니다.

| 관계 | 선택 | 예시 |
|---|---|---|
| 'A는 B의 한 종류' | Inheritance 검토 | `TemperatureSensor` → `ISensor` |
| 'A는 B를 포함' | Composition 권장 | `Robot` → `Motor` |
| 'A가 B의 기능을 잠시 사용' | 매개변수로 의존성 전달 | `Monitor::collect(const ISensor&)` |

아래 `Robot`은 모터 속도를 직접 구현하지 않고 `Motor`에 위임합니다. 내부 상태의 불변식(Class Invariant)은 `Motor`가 책임지므로 로봇 클래스가 불필요하게 복잡해지지 않습니다.

**핵심:** 상속이 코드 재사용의 기본 수단은 아닙니다. 변경 가능성이 높은 구현 세부사항은 Composition으로 분리하는 편이 유리할 수 있습니다.

**예제 코드 — [10_composition_vs_inheritance.cpp](./examples/10_composition_vs_inheritance.cpp)**

```cpp
#include <algorithm>
#include <print>
#include <string>
#include <string_view>
#include <utility>

class Motor {
public:
    void set_rpm(int requested) noexcept {
        rpm_ = std::clamp(requested, 0, 3'000);
    }
    [[nodiscard]] int rpm() const noexcept { return rpm_; }

private:
    int rpm_{};
};

class Robot {
public:
    explicit Robot(std::string name) : name_(std::move(name)) {}
    void move(int requested_rpm) noexcept { motor_.set_rpm(requested_rpm); }
    [[nodiscard]] std::string_view name() const noexcept { return name_; }
    [[nodiscard]] int motor_rpm() const noexcept { return motor_.rpm(); }

private:
    std::string name_;
    Motor motor_;  // Robot은 Motor를 소유함
};

int main() {
    Robot robot{"Cleaner-A"};
    robot.move(3'500);
    std::println("{} motor: {} RPM", robot.name(), robot.motor_rpm());
}
```

**실행 결과**

```text
Cleaner-A motor: 3000 RPM
```

---

## 9.12. Interface Segregation과 역할 분리

인터페이스 분리 원칙(Interface Segregation Principle, ISP)은 사용하지 않는 기능까지 객체에 의존하도록 강제하지 말라는 원칙입니다.

센서가 모두 교정(Calibration) 기능을 제공하는 것은 아닙니다. 그래서 `IReadable`과 `ICalibratable`을 나누면, 읽기만 가능한 장치는 교정 기능을 억지로 구현할 필요가 없습니다.

여기서는 두 개의 작은 Interface를 함께 구현하므로 다중 상속(Multiple Inheritance)을 사용합니다. **상태나 구현을 가진 클래스의 다중 상속**은 충돌·모호성·다이아몬드 상속 문제를 일으킬 수 있어 신중하게 설계해야 합니다.

장치 제어 과정에서는 하드웨어 상태에 따라 Calibration이 실패할 수 있습니다. 실패 원인을 전달해야 한다면 반환 타입에 오류 정보를 포함합니다.

**예제 코드 — [11_interface_segregation.cpp](./examples/11_interface_segregation.cpp)**

```cpp
#include <print>

struct IReadable {
    virtual ~IReadable() = default;
    [[nodiscard]] virtual double read() const = 0;
};

struct ICalibratable {
    virtual ~ICalibratable() = default;
    virtual void calibrate(double offset) = 0;
};

class AdjustableSensor final : public IReadable, public ICalibratable {
public:
    explicit AdjustableSensor(double raw) : raw_(raw) {}
    [[nodiscard]] double read() const override { return raw_ + offset_; }
    void calibrate(double offset) override { offset_ = offset; }

private:
    double raw_{};
    double offset_{};
};

class FixedSensor final : public IReadable {
public:
    [[nodiscard]] double read() const override { return 20.0; }
};

void display(const IReadable& sensor) {
    std::println("Reading: {:.1f}", sensor.read());
}

int main() {
    AdjustableSensor adjustable{21.0};
    adjustable.calibrate(1.5);
    const FixedSensor fixed;
    display(adjustable);
    display(fixed);
}
```

**실행 결과**

```text
Reading: 22.5
Reading: 20.0
```

---

## 9.13. Non-Virtual Interface와 검증

비가상 인터페이스(Non-Virtual Interface, NVI)는 공개 메서드에서 공통 검증 및 흐름을 처리하고, 실제 확장 지점만 Virtual Function으로 분리하는 설계 방식입니다.

아래 `apply()`는 유한한 숫자이고 0~100 범위인지 검사한 뒤 내부의 `transform()`을 호출합니다. 파생 클래스가 입력값 검증을 누락하더라도 공개 계약이 일관되게 유지됩니다.

- **공개 메서드 `apply()`:** 입력값 검증, 오류 반환, 호출 흐름 보장
- **비공개 `transform()`:** 파생 클래스별 실제 계산
- **`std::expected`:** 정상 결과와 오류 이유 분리

공통 검증 이후에도 파생 구현이 추가로 실패할 수 있다면, 내부 함수의 반환 타입도 이에 맞게 설계해야 합니다.

**예제 코드 — [12_nonvirtual_interface.cpp](./examples/12_nonvirtual_interface.cpp)**

```cpp
#include <cmath>
#include <expected>
#include <print>
#include <string_view>

class Controller {
public:
    virtual ~Controller() = default;

    [[nodiscard]] std::expected<double, std::string_view>
    apply(double requested) const {
        if (!std::isfinite(requested) || requested < 0.0 || requested > 100.0) {
            return std::unexpected("Input must be from 0 to 100");
        }
        return transform(requested);
    }

private:
    [[nodiscard]] virtual double transform(double value) const = 0;
};

class ScaleController final : public Controller {
private:
    [[nodiscard]] double transform(double value) const override {
        return value * 0.8;
    }
};

int main() {
    const ScaleController controller;
    for (const double requested : {75.0, 150.0}) {
        if (const auto result = controller.apply(requested)) {
            std::println("Output: {:.1f}", *result);
        } else {
            std::println("Error: {}", result.error());
        }
    }
}
```

**실행 결과**

```text
Output: 60.0
Error: Input must be from 0 to 100
```

---

## 9.14. Dependency Injection과 테스트 대역

의존성 주입(Dependency Injection, DI)은 클래스나 함수가 필요한 구체 객체를 내부에서 직접 만들기보다 외부로부터 전달받는 방식입니다.

네트워크나 센서에 연결하지 않고 테스트하려면 **테스트 대역(Test Double)**을 주입할 수 있습니다. 아래 `FakeTransport`는 메시지를 외부로 전송하는 대신 메모리에 기록해 전송 요청을 검증합니다.

- **외부 통신 구현:** 시리얼 포트·네트워크 등과 데이터 교환
- **Fake 구현:** 같은 Interface를 구현하지만 메모리에서 동작
- **테스트 대상:** 전송 호출 여부, 데이터 내용, 실패 처리

`assert`에만 의존한 테스트는 `NDEBUG` 빌드에서 검사가 비활성화될 수 있습니다. 아래 예제는 검사 결과로 종료 코드를 반환해 실행 환경에서 성공 여부를 확인할 수 있습니다.

**예제 코드 — [13_dependency_injection_test.cpp](./examples/13_dependency_injection_test.cpp)**

```cpp
#include <print>
#include <string>
#include <string_view>
#include <vector>

class ITransport {
public:
    virtual ~ITransport() = default;
    virtual bool send(std::string_view message) = 0;
};

class FakeTransport final : public ITransport {
public:
    bool send(std::string_view message) override {
        messages_.emplace_back(message);
        return true;
    }
    [[nodiscard]] const std::vector<std::string>& messages() const noexcept {
        return messages_;
    }

private:
    std::vector<std::string> messages_;
};

[[nodiscard]] bool send_alarm(ITransport& transport, std::string_view text) {
    return !text.empty() && transport.send(text);
}

int main() {
    FakeTransport fake;
    const bool sent = send_alarm(fake, "OVERHEAT");
    const bool correct = sent && fake.messages().size() == 1 &&
                         fake.messages().front() == "OVERHEAT";
    std::println("Transport test: {}", correct ? "PASS" : "FAIL");
    return correct ? 0 : 1;
}
```

**실행 결과**

```text
Transport test: PASS
```

---

## 9.15. 동적 다형성과 `std::variant` 비교

Dynamic Dispatch가 항상 최적의 선택은 아닙니다. 처리할 자료형이 고정되어 있다면 `std::variant`와 `std::visit`으로 **닫힌 타입 집합(Closed Set)**을 명시할 수 있습니다.

| 비교 | Virtual Function | `std::variant` |
|---|---|---|
| 타입 추가 | 새로운 파생 클래스로 확장 용이 | Variant 타입 목록 수정 필요 |
| 호출 방식 | 실행 시점의 가상 함수 호출 | 타입 분기 및 Visitor 실행 |
| 저장 방식 | 기반 포인터·참조로 다루는 경우가 많음 | Variant 객체에 선택된 대안 저장 |
| 적합한 상황 | 플러그인·장치 구현 교체 | 고정된 종류의 이벤트·메시지 |

`std::variant` 자체가 반드시 동적 할당을 필요로 하지는 않습니다. 반면 Virtual Function이라고 해서 모든 경우에 힙 할당이 필수인 것도 아닙니다. **선택 기준은 성능만이 아니라 확장 방식과 모델의 의미**입니다.

아래 예제는 서로 다른 측정 자료형을 하나의 Variant로 표현합니다.

**예제 코드 — [14_variant_alternative.cpp](./examples/14_variant_alternative.cpp)**

```cpp
#include <format>
#include <print>
#include <string>
#include <type_traits>
#include <variant>

struct Temperature { double celsius; };
struct Battery { int percent; };

using Reading = std::variant<Temperature, Battery>;

[[nodiscard]] std::string describe(const Reading& reading) {
    return std::visit([](const auto& item) -> std::string {
        using T = std::decay_t<decltype(item)>;
        if constexpr (std::is_same_v<T, Temperature>) {
            return std::format("Temperature: {:.1f} C", item.celsius);
        } else {
            return std::format("Battery: {}%", item.percent);
        }
    }, reading);
}

int main() {
    const Reading first{Temperature{23.5}};
    const Reading second{Battery{87}};
    std::println("{}", describe(first));
    std::println("{}", describe(second));
}
```

**실행 결과**

```text
Temperature: 23.5 C
Battery: 87%
```

---

## 9.16. 생성자·소멸자에서 Virtual Function 호출

생성자(Constructor)와 소멸자(Destructor)가 실행되는 동안에는 객체가 완전한 최종 파생 타입으로 동작하지 않습니다. 기반 클래스 생성자 안에서 호출한 Virtual Function은 **그 생성자에 해당하는 클래스 단계의 구현**을 사용합니다.

따라서 생성자에서 Virtual Function을 호출해 파생 클래스의 초기화 작업을 대신 수행하는 설계는 피해야 합니다. 생성과 검증을 마친 뒤 별도 초기화 메서드를 호출하거나 Factory를 사용해 완성된 객체를 생성하는 방법이 있습니다.

아래 예제에서는 생성자 내부에서 `Base`, 생성이 끝난 후에는 `Derived`가 출력됩니다.

**예제 코드 — [15_constructor_dispatch.cpp](./examples/15_constructor_dispatch.cpp)**

```cpp
#include <print>
#include <string_view>

class Base {
public:
    Base() { std::println("During Base construction: {}", name()); }
    virtual ~Base() = default;
    [[nodiscard]] virtual std::string_view name() const noexcept {
        return "Base";
    }
};

class Derived final : public Base {
public:
    [[nodiscard]] std::string_view name() const noexcept override {
        return "Derived";
    }
};

int main() {
    const Derived derived;
    std::println("After construction: {}", derived.name());
}
```

**실행 결과**

```text
During Base construction: Base
After construction: Derived
```

---

## 9.17. Mini Project — Robot Sensor Monitor

여러 종류의 센서를 하나의 Monitor에 등록하고 측정 결과를 수집하는 **시뮬레이션 프로젝트**입니다. 실제 하드웨어의 드라이버 구현은 포함하지 않습니다.

```text
examples/16_robot_monitor/
├── CMakeLists.txt
├── monitor.hpp
├── monitor.cpp
└── main.cpp
```

| 구성 요소 | 역할 |
|---|---|
| `ISensor` | `id()`, `unit()`, `read()` 공통 Interface |
| `TemperatureSensor` | 온도 측정 데이터 제공 |
| `BatterySensor` | 배터리 비율 확인 및 유효 범위 검사 |
| `Monitor` | 센서 Ownership 관리, 중복 ID 거부, 결과 수집 |
| `Sample` | 결과값과 단위를 묶는 데이터 타입 |
| `main.cpp` | 장치 등록과 결과 출력 담당 |

`Monitor::add()`는 `std::unique_ptr<ISensor>`를 전달받아 소유합니다. `collect()`는 센서의 데이터만 반환하므로 출력 방식에 영향을 받지 않습니다. 새로운 센서를 추가할 때는 `ISensor`를 구현하고 `Monitor`에 등록하면 됩니다.

**구현 파일**

- [monitor.hpp](./examples/16_robot_monitor/monitor.hpp)
- [monitor.cpp](./examples/16_robot_monitor/monitor.cpp)
- [main.cpp](./examples/16_robot_monitor/main.cpp)
- [CMakeLists.txt](./examples/16_robot_monitor/CMakeLists.txt)

`Monitor`와 센서의 인터페이스를 선언한 `monitor.hpp`의 핵심 부분은 다음과 같습니다.

```cpp
class ISensor {
public:
    virtual ~ISensor() = default;
    [[nodiscard]] virtual std::string_view id() const noexcept = 0;
    [[nodiscard]] virtual std::string_view unit() const noexcept = 0;
    [[nodiscard]] virtual std::optional<double> read() const noexcept = 0;
};

class Monitor {
public:
    [[nodiscard]] bool add(std::unique_ptr<ISensor> sensor);
    [[nodiscard]] std::vector<Sample> collect() const;
private:
    std::vector<std::unique_ptr<ISensor>> sensors_;
};
```

### GCC

`Chapter-09/`에서 다음 명령어를 실행합니다.

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic \
  examples/16_robot_monitor/main.cpp \
  examples/16_robot_monitor/monitor.cpp -o robot_monitor
./robot_monitor
```

### Clang

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic \
  examples/16_robot_monitor/main.cpp \
  examples/16_robot_monitor/monitor.cpp -o robot_monitor
./robot_monitor
```

### CMake

```bash
cmake -S examples/16_robot_monitor -B build/robot_monitor
cmake --build build/robot_monitor
./build/robot_monitor/robot_monitor
```

`CMakeLists.txt`는 C++23을 요청합니다. 다만 설치한 컴파일러와 표준 라이브러리가 `std::println` 및 다른 C++23 기능을 지원해야 합니다. Visual Studio·Windows 환경에서는 빌드 출력 파일의 실제 경로가 구성(Debug/Release)에 따라 달라집니다.

**실행 결과**

```text
TEMP-A: 23.5 C
BAT-A: 87.0 %
BAT-B: unavailable
```

`BAT-B`의 입력 `150.0`은 배터리 비율 범위를 벗어나므로 `std::nullopt`를 반환합니다. 잘못된 측정값을 임의로 정상 범위에 맞추지 않고 **사용 불가 상태**로 구분합니다.

**확장 과제:** 중복 ID 등록 테스트, 센서 연결 실패 구현, 측정 시각 추가, 결과 로깅 분리 등을 구현해 볼 수 있습니다.

---

## 9.18. 성능·안전성·설계 점검

객체 간 관계, Lifetime, 오류 처리 방식에 따라 코드의 안전성과 확장성이 달라집니다. 다음 항목을 점검합니다.

| 점검 항목 | 위험 사례 | 권장 방식 |
|---|---|---|
| 기반 클래스 삭제 | 비가상 소멸자를 가진 기반 포인터로 파생 객체 삭제 | `public virtual` 소멸자 등 적절한 삭제 계약 |
| 객체 전달 | 기반 클래스 값 전달로 Object Slicing 발생 | 기반 타입의 참조 또는 포인터 전달 |
| 타입 변환 | 검증 없는 Downcasting | 공통 Interface 또는 `dynamic_cast` 검사 |
| 객체 수명 | 수명이 끝난 대상을 참조 | 명확한 Ownership과 객체 Lifetime 관리 |
| 설계 결합 | 세부 구현을 기반 클래스에 고정 | 작은 Interface 또는 Composition |
| 성능 | 모든 호출을 불필요하게 Virtual Function으로 설계 | 측정 후 필요한 경로에만 적용 |
| 상태 불변식 | 파생 구현에 동일한 입력 검증을 반복 | 공통 진입점에 검증 집약 |
| 테스트 | 실물 장치가 있어야만 실행 가능 | Fake 기반 검증, 결과와 출력 분리 |

Virtual Function 호출 비용은 추측보다 측정을 통해 판단합니다. 최적화 옵션(`-O2`)을 적용한 빌드에서 프로파일링(Profiling)을 수행하고 대표 입력 데이터로 결과를 비교합니다. 메모리 접근 오류와 일부 UB 검출에는 AddressSanitizer(ASan), UndefinedBehaviorSanitizer(UBSan)를 활용할 수 있습니다.

**GCC 또는 Clang 검사 예시**

```bash
g++ -std=c++23 -g -O1 -Wall -Wextra -Wpedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  examples/07_polymorphic_collection.cpp -o check_ownership
./check_ownership
```

Sanitizer 사용 가능 여부는 컴파일러와 운영체제에 따라 다릅니다. 도구가 모든 종류의 UB를 탐지하는 것은 아닙니다.

---

## 9.19. Coding Practice

연습문제의 시작 코드는 `exercises/`에, 정답 코드는 `solutions/`에 있습니다. 먼저 문제를 해결한 다음 정답과 결과를 비교합니다. 시작 코드는 `TODO`를 남겨두어 컴파일은 가능하지만 요구 동작을 완성하지 않은 상태입니다.

### 실습 ① — Alarm Channels

[연습문제](./exercises/01_alarm_channels.cpp) · [정답 코드](./solutions/01_alarm_channels.cpp)

`IAlarmChannel`을 구현하는 `ConsoleAlarm`, `SilentAlarm`을 작성합니다.

- `ConsoleAlarm`: `ALARM: <message>` 출력
- `SilentAlarm`: 출력하지 않는 구현
- 두 구현 모두 기반 클래스 참조로 사용

**기대 출력**

```text
ALARM: High temperature
```

### 실습 ② — Robot Motor

[연습문제](./exercises/02_robot_motor.cpp) · [정답 코드](./solutions/02_robot_motor.cpp)

`Robot`이 `Motor`를 멤버로 소유하도록 작성합니다. 속도는 0~3000 RPM으로 제한하고, 외부에서는 `Robot::drive()`를 통해서만 변경합니다.

**검증 조건**

- `drive(3500)` → `3000` RPM
- `drive(-100)` → `0` RPM

### 실습 ③ — Sensor Registry

[연습문제](./exercises/03_sensor_registry.cpp) · [정답 코드](./solutions/03_sensor_registry.cpp)

`std::vector<std::unique_ptr<ISensor>>` 기반 레지스트리를 구현합니다.

- 정상 ID를 처음 등록할 때만 `true`
- 이미 등록된 ID, 빈 ID, `nullptr`는 `false`
- 성공적으로 등록한 센서의 Ownership은 `Registry`로 이전
- 중복 거부 후 등록된 객체 수는 변경되지 않음

**기대 결과**

```text
First: true, duplicate: false, empty: false, null: false, count: 1
```

### 실습 ④ — Fault Detector

[연습문제](./exercises/04_fault_detector.cpp) · [정답 코드](./solutions/04_fault_detector.cpp)

`IReadingSource`를 이용해 고온 상태 여부를 확인하는 함수를 작성합니다.

- 유효한 온도가 임계값보다 크면 `true`
- 측정값이 없거나 NaN·Infinity 등의 유효하지 않은 값이면 `false`
- 임계값 자체가 유효하지 않을 때도 `false`
- 실제 센서 없이 `FakeReading`으로 정상·오류 사례를 검증

**기대 결과**

```text
Hot: true
Normal: false
Missing: false
Invalid: false
```

### 컴파일 및 실행

**GCC** — `Chapter-09/` 폴더 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic \
  solutions/03_sensor_registry.cpp -o sensor_registry
./sensor_registry
```

**Clang** — 사용 중인 표준 라이브러리의 C++23 지원 확인

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic \
  solutions/03_sensor_registry.cpp -o sensor_registry
./sensor_registry
```

**MSVC** — Developer Command Prompt

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 solutions\03_sensor_registry.cpp /Fe:sensor_registry.exe
sensor_registry.exe
```

MSVC에서 `/std:c++23preview`는 지원 버전에 따라 제공 여부가 다릅니다. 표준 라이브러리 구현 범위 역시 별도로 확인해야 합니다.

---

## 9.20. Quiz & Summary

### Quiz

1. `virtual`과 `override`는 각각 어떤 역할을 하나요?
2. `std::unique_ptr<Base>`로 `Derived` 객체를 관리할 때 기반 클래스 소멸자는 보통 어떻게 선언해야 하나요?
3. 파생 객체를 `void process(Base)`에 전달하면 어떤 문제가 발생할 수 있나요?
4. `dynamic_cast<Derived*>(base)` 실패 결과는 무엇인가요?
5. `Robot`이 `Motor`를 내부에 포함한다면 Inheritance와 Composition 중 무엇이 적절한가요?
6. 기반 클래스 생성자에서 재정의된 Virtual Function을 호출하면 파생 클래스 구현이 실행되나요?
7. 구현 종류가 고정된 값의 집합이라면 Virtual Function 대신 고려할 수 있는 표준 기능은 무엇인가요?

<details>
<summary>정답 확인</summary>

1. `virtual`은 Dynamic Dispatch가 가능한 함수를 선언하고, `override`는 정확한 재정의를 컴파일 시점에 확인함.
2. 일반적으로 `public virtual ~Base() = default;`처럼 가상 소멸자를 제공해야 함.
3. Object Slicing으로 파생 객체 부분이 잘려 Dynamic Dispatch 대상이 바뀔 수 있음.
4. 변환이 실패한 포인터는 `nullptr`을 반환함.
5. 포함 관계이므로 Composition이 적절함.
6. 아니요. 생성 중 해당 기본 클래스 단계의 구현이 호출됨.
7. `std::variant`와 `std::visit`을 검토할 수 있음.

</details>

### Summary

- **Inheritance:** 타입 간 관계를 정의하며 단순한 코드 재사용 목적으로 남용하지 않음
- **Polymorphism:** 기반 포인터·참조를 통한 구현 교체
- **Virtual Function:** 호출 대상의 Dynamic Dispatch 지원
- **`override` / `final`:** 재정의 검증 및 확장 제한
- **Abstract Class / Interface:** 구현과 사용 코드를 분리하는 계약
- **Virtual Destructor:** 기반 포인터를 통한 삭제 시 객체 수명 안전성 확보
- **Ownership:** `std::unique_ptr`과 참조를 구분해 수명 관리
- **Object Slicing:** 기반 클래스 값 전달 시 파생 객체 정보 손실
- **Downcasting:** 필요할 때 `dynamic_cast`로 검사하되 Interface 설계 우선
- **Composition / ISP:** 포함 관계와 작은 역할 단위로 책임 분리
- **NVI / DI:** 공통 검증, 구현 주입, Fake 기반 테스트 지원
- **`std::variant`:** 정해진 타입 집합을 다룰 때 고려하는 대안

### References

- [cppreference — Virtual Function](https://en.cppreference.com/w/cpp/language/virtual)
- [cppreference — Derived Classes](https://en.cppreference.com/w/cpp/language/derived_class)
- [cppreference — `dynamic_cast`](https://en.cppreference.com/w/cpp/language/dynamic_cast)
- [cppreference — `std::unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [cppreference — `std::variant`](https://en.cppreference.com/w/cpp/utility/variant)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [C++23 Compiler Support](https://en.cppreference.com/w/cpp/compiler_support/23)

---

[← C++ 목차](../README.md) · [Chapter 08 — Structs & Classes](../Chapter-08/)
