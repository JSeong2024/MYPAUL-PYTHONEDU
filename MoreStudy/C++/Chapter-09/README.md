# Chapter 09. Object-Oriented Programming

상속(Inheritance)과 다형성(Polymorphism)의 동작 원리를 이해하고, 가상 함수(Virtual Function)와 추상 클래스(Abstract Class)로 공통 인터페이스(Interface)를 설계하는 방법을 학습합니다. 객체 수명(Lifetime)과 소유권(Ownership), 합성(Composition)과 상속의 선택 기준을 함께 다루며, 센서 모니터 예제로 개념을 연결합니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다.

<details>
<summary>선행 학습</summary>

- [Chapter 05 — Functions](../Chapter-05/) : 함수, 매개변수와 반환값
- [Chapter 07 — Pointers & References](../Chapter-07/) : 포인터, 참조와 객체 수명
- [Chapter 08 — Structs & Classes](../Chapter-08/) : 클래스, 생성자와 캡슐화

</details>

## Contents

| Section | Topic |
|:---:|---|
| [9.1](#section-9-1) | Object-Oriented Design — 객체지향 설계의 기본 |
| [9.2](#section-9-2) | Inheritance — 기본 클래스와 파생 클래스 |
| [9.3](#section-9-3) | Access Control — 상속과 접근 지정자 |
| [9.4](#section-9-4) | Virtual Functions — 가상 함수와 동적 디스패치 |
| [9.5](#section-9-5) | `override` & `final` — 재정의 검증과 확장 제한 |
| [9.6](#section-9-6) | Abstract Classes — 추상 클래스와 인터페이스 |
| [9.7](#section-9-7) | Virtual Destructors — 다형적 객체의 소멸 |
| [9.8](#section-9-8) | Polymorphic Collections — 서로 다른 객체 함께 관리하기 |
| [9.9](#section-9-9) | Object Slicing — 객체 슬라이싱 |
| [9.10](#section-9-10) | `dynamic_cast` — 실행 시점의 타입 확인 |
| [9.11](#section-9-11) | Composition — 상속보다 합성이 적합한 관계 |
| [9.12](#section-9-12) | Interface Segregation — 인터페이스 역할 분리 |
| [9.13](#section-9-13) | Non-Virtual Interface — 공통 검증을 한 곳에서 |
| [9.14](#section-9-14) | Dependency Injection — 의존성 주입과 테스트 대역 |
| [9.15](#section-9-15) | `std::variant` — 상속 없이 여러 타입 표현하기 |
| [9.16](#section-9-16) | Construction & Dispatch — 생성 중 가상 함수 호출 |
| [9.17](#section-9-17) | Coding Practice |
| [9.18](#section-9-18) | Mini Project — Robot Sensor Monitor |
| [9.19](#section-9-19) | Quiz & Summary |

## Getting Started

아래 명령어는 `Chapter-09/` 폴더에서 실행하는 경우를 기준으로 합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/03_virtual_dispatch.cpp -o virtual_dispatch
./virtual_dispatch
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/03_virtual_dispatch.cpp -o virtual_dispatch
./virtual_dispatch
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /utf-8 examples\03_virtual_dispatch.cpp /Fe:virtual_dispatch.exe
virtual_dispatch.exe
```

Windows PowerShell에서는 `./virtual_dispatch` 대신 `.\virtual_dispatch.exe`로 실행합니다. 컴파일러의 기본 설치·설정은 Chapter 01을 참고할 수 있습니다.

다중 파일 CMake 예제와 자동 테스트 실행 방법은 [9.18절](#section-9-18)에 있습니다.

<a id="section-9-1"></a>

## 9.1. Object-Oriented Design — 객체지향 설계의 기본

객체지향 프로그래밍(Object-Oriented Programming, OOP)은 관련 데이터와 동작을 객체 단위로 조직하는 방법입니다. Chapter 08에서는 `struct`, `class`, 생성자, 캡슐화(Encapsulation)를 통해 객체의 내부 상태를 관리했습니다. 여기서는 서로 다른 객체가 **같은 인터페이스를 통해 서로 다른 동작을 수행하는 방법**을 학습합니다.
| 개념 | 핵심 역할 | 예시 |
|:---|:---|:---|
| 상속(Inheritance) | 기존 클래스와 새로운 클래스 사이의 타입 관계 표현 | `Sensor` → `DistanceSensor` |
| 다형성(Polymorphism) | 동일한 호출 방식으로 실제 객체에 맞는 동작 수행 | `sensor.read()` |
| 추상화(Abstraction) | 구현 세부사항 대신 사용자가 필요한 동작 제공 | `ReadingSource` 인터페이스 |
| 합성(Composition) | 객체가 다른 객체를 구성 요소로 보유 | `Robot`이 `Battery`를 멤버로 보유 |

상속을 사용하지 않아도 객체지향 설계는 가능합니다. 실제로는 **종류를 나타내는 관계**인지, **부품을 포함하는 관계**인지 먼저 구분하는 편이 중요합니다. 파생 클래스가 기본 클래스 대신 사용될 수 없다면 상속 구조를 다시 검토해야 합니다.

---

<a id="section-9-2"></a>

## 9.2. Inheritance — 기본 클래스와 파생 클래스

**기본 클래스(Base Class)** 는 공통된 인터페이스나 데이터를 정의합니다. **파생 클래스(Derived Class)** 는 이를 상속받아 기능을 추가하거나 변경할 수 있습니다. `class TemperatureSensor : public Device`는 `TemperatureSensor`가 `Device`를 공개 상속한다는 뜻입니다.

이 예제에서 `TemperatureSensor`는 `Device`의 식별자를 사용하면서 자신만의 온도 측정값을 보관합니다. 기본 클래스의 `private` 멤버는 파생 클래스가 직접 접근할 수 없으므로 `id()`를 통해 읽습니다. 또한 파생 객체를 생성할 때는 기본 클래스 부분이 먼저 초기화됩니다.

**구분할 점:** 상속만 했다고 모든 멤버 함수가 가상 함수가 되지는 않습니다. 실제 객체 종류에 따라 호출할 구현을 선택하는 기능은 9.4절에서 다룹니다.

**예제 코드 — [01_inheritance_basics.cpp](./examples/01_inheritance_basics.cpp)**

```cpp
#include <iostream>
#include <string>
#include <utility>

class Device {
public:
    explicit Device(std::string id) : id_{std::move(id)} {}
    [[nodiscard]] const std::string& id() const noexcept { return id_; }
private:
    std::string id_;
};

class TemperatureSensor : public Device {
public:
    TemperatureSensor(std::string id, double celsius)
        : Device{std::move(id)}, celsius_{celsius} {}
    [[nodiscard]] double celsius() const noexcept { return celsius_; }
private:
    double celsius_{};
};

int main() {
    const TemperatureSensor sensor{"TEMP-01", 24.5};
    std::cout << sensor.id() << ": " << sensor.celsius() << " C\n";
}
```

**실행 결과**

```text
TEMP-01: 24.5 C
```

---

<a id="section-9-3"></a>

## 9.3. Access Control — 상속과 접근 지정자

상속 관계에서도 접근 지정자(Access Specifier)의 의미는 유지됩니다. `public`은 외부에 공개하는 기능, `private`은 클래스 내부의 구현, `protected`는 해당 클래스와 파생 클래스의 구현에서 접근할 수 있는 멤버를 나타냅니다.
| 지정자 | 일반 외부 코드 | 파생 클래스 멤버 함수 |
|:---|:---:|:---:|
| `public` | 접근 가능 | 접근 가능 |
| `protected` | 접근 불가 | 접근 가능 |
| `private` | 접근 불가 | 직접 접근 불가 |

`FanController`는 기본 클래스의 보호된 `set_speed_unchecked()`를 사용하지만, 외부에는 범위를 검사하는 `request_speed()`만 제공합니다. 이처럼 검증되지 않은 상태 변경 기능을 외부로 공개하지 않으면 잘못된 요청이 객체 상태에 반영되는 것을 줄일 수 있습니다.

다만 `protected` 데이터 멤버를 지나치게 늘리면 파생 클래스가 기본 클래스의 내부 구현에 강하게 의존합니다. 가능하면 멤버 변수는 `private`으로 두고 필요한 동작만 제공하는 방식부터 고려합니다.

**예제 코드 — [02_access_control.cpp](./examples/02_access_control.cpp)**

```cpp
#include <iostream>

class Controller {
public:
    [[nodiscard]] int speed() const noexcept { return speed_; }
protected:
    void set_speed_unchecked(int speed) noexcept { speed_ = speed; }
private:
    int speed_{};
};

class FanController final : public Controller {
public:
    [[nodiscard]] bool request_speed(int rpm) noexcept {
        if (rpm < 0 || rpm > 3000) return false;
        set_speed_unchecked(rpm);
        return true;
    }
};

int main() {
    FanController fan;
    const bool accepted = fan.request_speed(1200);
    const bool rejected = fan.request_speed(-1);
    std::cout << std::boolalpha << "Accepted: " << accepted
              << ", rejected: " << rejected << ", speed: " << fan.speed() << '\n';
}
```

**실행 결과**

```text
Accepted: true, rejected: false, speed: 1200
```

---

<a id="section-9-4"></a>

## 9.4. Virtual Functions — 가상 함수와 동적 디스패치

**가상 함수(Virtual Function)** 는 파생 클래스에서 재정의할 수 있는 멤버 함수입니다. 기본 클래스의 포인터나 참조를 통해 호출하더라도 **실제 객체의 타입**에 따라 실행할 구현이 결정됩니다. 이를 **동적 디스패치(Dynamic Dispatch)** 라고 합니다.

예제의 `print_kind(const Sensor&)`는 `Sensor` 타입만 알고 있습니다. 그런데 `DistanceSensor` 객체를 전달하면 재정의한 `kind()`가 실행됩니다. 즉, 호출 함수는 센서별 구체적인 클래스를 직접 구분할 필요가 없습니다.

반대로 가상 함수가 아닌 일반 멤버 함수는 이 방식으로 재정의된 함수를 선택하지 않습니다. 또한 **기본 클래스 객체 그 자체**와 **파생 객체를 기본 클래스 참조로 접근하는 경우**를 혼동하지 않아야 합니다.

**예제 코드 — [03_virtual_dispatch.cpp](./examples/03_virtual_dispatch.cpp)**

```cpp
#include <iostream>

class Sensor {
public:
    virtual ~Sensor() = default;
    [[nodiscard]] virtual const char* kind() const noexcept { return "generic"; }
};

class DistanceSensor final : public Sensor {
public:
    [[nodiscard]] const char* kind() const noexcept override { return "distance"; }
};

void print_kind(const Sensor& sensor) {
    std::cout << "Sensor: " << sensor.kind() << '\n';
}

int main() {
    const Sensor basic;
    const DistanceSensor distance;
    print_kind(basic);
    print_kind(distance);
}
```

**실행 결과**

```text
Sensor: generic
Sensor: distance
```

---

<a id="section-9-5"></a>

## 9.5. `override` & `final` — 재정의 검증과 확장 제한

**재정의(Overriding)** 는 파생 클래스가 기본 클래스의 가상 함수에 해당하는 구현을 제공하는 것입니다. `override`를 적으면 컴파일러가 올바른 재정의인지 검사합니다. 함수 이름이 같아도 매개변수나 `const` 지정 등이 일치하지 않으면 재정의가 되지 않을 수 있으므로, 파생 클래스의 가상 함수에는 `override`를 붙이는 편이 안전합니다.

`final`은 클래스에 붙이면 더 이상 파생 클래스를 만들 수 없도록 하고, 가상 함수에 붙이면 추가 재정의를 막습니다. 예제의 `HighAlarm final`은 별도의 파생 클래스를 만들 필요가 없는 완성형 규칙을 나타냅니다.

`virtual bool triggered(...) = 0`의 `= 0`은 순수 가상 함수(Pure Virtual Function)를 뜻합니다. 이 경우 파생 클래스가 필요한 동작을 구현해야 실제 객체를 만들 수 있습니다.

**예제 코드 — [04_override_and_final.cpp](./examples/04_override_and_final.cpp)**

```cpp
#include <iostream>

class Alarm {
public:
    virtual ~Alarm() = default;
    [[nodiscard]] virtual bool triggered(int reading) const noexcept = 0;
};

class HighAlarm final : public Alarm {
public:
    [[nodiscard]] bool triggered(int reading) const noexcept override {
        return reading >= 80;
    }
};

int main() {
    const HighAlarm alarm;
    std::cout << std::boolalpha << "79: " << alarm.triggered(79)
              << ", 80: " << alarm.triggered(80) << '\n';
}
```

**실행 결과**

```text
79: false, 80: true
```

---

<a id="section-9-6"></a>

## 9.6. Abstract Classes — 추상 클래스와 인터페이스

**추상 클래스(Abstract Class)** 는 순수 가상 함수가 있어 직접 객체를 만들 수 없는 클래스입니다. 서로 다른 구현이 공통으로 제공해야 할 기능을 정의하는 데 적합합니다. C++에는 별도의 `interface` 키워드가 없으며, 추상 클래스를 인터페이스(Interface)처럼 사용할 수 있습니다.

`ReadingSource`는 읽는 방법을 지정하지 않고 `read()`가 제공되어야 한다는 계약만 표현합니다. `FixedReading`이 값을 반환하도록 구현하므로 `is_critical()`은 센서의 구체적인 종류를 몰라도 동작합니다.

인터페이스는 필요한 기능이 명확할수록 사용하기 쉽습니다. 모든 장치에 무관한 동작을 한꺼번에 요구하는 거대한 인터페이스는 구현을 어렵게 할 수 있습니다. 또한 인터페이스를 통한 다형적 삭제가 예상되므로 공개 가상 소멸자 `virtual ~ReadingSource() = default;`를 제공합니다.

**예제 코드 — [05_abstract_interface.cpp](./examples/05_abstract_interface.cpp)**

```cpp
#include <iostream>

class ReadingSource {
public:
    virtual ~ReadingSource() = default;
    [[nodiscard]] virtual int read() const noexcept = 0;
};

class FixedReading final : public ReadingSource {
public:
    explicit FixedReading(int value) : value_{value} {}
    [[nodiscard]] int read() const noexcept override { return value_; }
private:
    int value_{};
};

[[nodiscard]] bool is_critical(const ReadingSource& source) {
    return source.read() >= 80;
}

int main() {
    const FixedReading source{85};
    std::cout << std::boolalpha << "Critical: " << is_critical(source) << '\n';
}
```

**실행 결과**

```text
Critical: true
```

---

<a id="section-9-7"></a>

## 9.7. Virtual Destructors — 다형적 객체의 소멸

소멸자(Destructor)는 객체의 수명이 끝날 때 실행됩니다. 파생 객체를 **기본 클래스 포인터를 통해 삭제하는 구조**에서는 일반적으로 기본 클래스에 **가상 소멸자(Virtual Destructor)** 가 필요합니다. 그래야 파생 부분의 소멸자부터 기본 부분의 소멸자까지 올바른 순서로 실행됩니다.

`<memory>`는 Chapter 07에서 소개한 스마트 포인터를 제공하는 헤더입니다. `std::make_unique<Camera>()`로 만든 객체를 `std::unique_ptr<Device>`에 보관하면 포인터의 소유권은 `unique_ptr`가 관리합니다. 이 예제는 파생 클래스와 기본 클래스의 소멸 순서를 직접 출력합니다.

**주의:** 기본 클래스 소멸자가 가상이 아니면, 기본 클래스 포인터를 통한 일반적인 파생 객체 삭제는 정의되지 않은 동작(Undefined Behavior)이 될 수 있습니다. 소멸자 본문에 자원 해제 코드가 없다는 이유로 안전해지는 것은 아닙니다. 단, 모든 클래스가 반드시 가상 소멸자를 가져야 하는 것은 아닙니다. 다형적 삭제를 허용할 설계인지가 판단 기준입니다.

**예제 코드 — [06_virtual_destructor.cpp](./examples/06_virtual_destructor.cpp)**

```cpp
#include <iostream>
#include <memory>

class Device {
public:
    virtual ~Device() { std::cout << "Device closed\n"; }
};

class Camera final : public Device {
public:
    ~Camera() override { std::cout << "Camera closed\n"; }
};

int main() {
    std::unique_ptr<Device> device = std::make_unique<Camera>();
    std::cout << "Using camera\n";
}
```

**실행 결과**

```text
Using camera
Camera closed
Device closed
```

---

<a id="section-9-8"></a>

## 9.8. Polymorphic Collections — 서로 다른 객체 함께 관리하기

다양한 파생 객체를 하나의 컨테이너로 관리하려면 기본 클래스의 포인터를 저장할 수 있습니다. 이 예제는 소유권이 명확한 `std::vector<std::unique_ptr<Sensor>>`를 사용합니다.

- `std::vector`는 여러 포인터를 보관합니다.
- `std::unique_ptr<Sensor>`는 각 센서 객체의 독점 소유권을 관리합니다.
- `sensor->read()`는 실제 파생 객체의 `read()`를 호출합니다.

반환되는 값이 달라도 순회 코드는 하나입니다. 등록된 센서가 늘어날수록 이 장점이 커집니다. 다만 단순 데이터 목록이라면 가상 함수 계층 없이 `std::vector<Reading>` 같은 값 타입만으로 충분할 수도 있습니다.

**예제 코드 — [07_polymorphic_collection.cpp](./examples/07_polymorphic_collection.cpp)**

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Sensor {
public:
    virtual ~Sensor() = default;
    [[nodiscard]] virtual int read() const noexcept = 0;
};

class FixedSensor final : public Sensor {
public:
    explicit FixedSensor(int value) : value_{value} {}
    [[nodiscard]] int read() const noexcept override { return value_; }
private:
    int value_{};
};

int main() {
    std::vector<std::unique_ptr<Sensor>> sensors;
    sensors.push_back(std::make_unique<FixedSensor>(12));
    sensors.push_back(std::make_unique<FixedSensor>(25));
    int total{};
    for (const auto& sensor : sensors) total += sensor->read();
    std::cout << "Sensors: " << sensors.size() << ", total: " << total << '\n';
}
```

**실행 결과**

```text
Sensors: 2, total: 37
```

---

<a id="section-9-9"></a>

## 9.9. Object Slicing — 객체 슬라이싱

**객체 슬라이싱(Object Slicing)** 은 파생 객체를 기본 클래스 타입의 **값으로 복사할 때**, 기본 클래스 부분만 새 객체에 복사되는 현상입니다. 복사된 객체에는 파생 클래스 부분이 없으므로 원래 객체의 동적 타입과 동작이 유지되지 않습니다.

`by_value(Device copy)`는 독립된 `Device` 객체를 만듭니다. 반면 `by_reference(const Device& device)`는 원래의 `Camera` 객체를 참조하므로 가상 함수 호출 시 `Camera::kind()`가 실행됩니다.

다형성을 유지하려면 일반적으로 `Base&`, `const Base&`, `Base*` 또는 소유권을 나타내는 스마트 포인터를 이용합니다. 값 복사가 꼭 필요한 경우에는 객체가 어떻게 복제되어야 하는지 별도의 설계가 필요합니다.

**예제 코드 — [08_object_slicing.cpp](./examples/08_object_slicing.cpp)**

```cpp
#include <iostream>

class Device {
public:
    virtual ~Device() = default;
    [[nodiscard]] virtual const char* kind() const noexcept { return "device"; }
};
class Camera final : public Device {
public:
    [[nodiscard]] const char* kind() const noexcept override { return "camera"; }
};

void by_value(Device copy) { std::cout << "By value: " << copy.kind() << '\n'; }
void by_reference(const Device& device) {
    std::cout << "By reference: " << device.kind() << '\n';
}
int main() {
    const Camera camera;
    by_value(camera);  // 파생 부분이 복사되지 않는 객체 슬라이싱
    by_reference(camera);
}
```

**실행 결과**

```text
By value: device
By reference: camera
```

---

<a id="section-9-10"></a>

## 9.10. `dynamic_cast` — 실행 시점의 타입 확인

`dynamic_cast`는 다형적 클래스 계층에서 실행 시점의 객체 타입을 확인하면서 변환할 때 사용합니다. 예제의 `Device`에는 가상 소멸자가 있으므로 다형적 타입입니다. `dynamic_cast<const Camera*>(&device)`는 실제 객체가 `Camera`라면 주소를 반환하고, 그렇지 않으면 `nullptr`을 반환합니다.

- **포인터 변환 실패:** `nullptr` 반환
- **참조 변환 실패:** `std::bad_cast` 예외 발생
- **필요 조건:** 이러한 다운캐스팅에는 일반적으로 다형적 기반 타입이 필요

이 기능으로 타입을 안전하게 확인할 수 있지만, 매번 구체적 타입을 검사해야 한다면 인터페이스 설계가 충분한지 먼저 살펴봅니다. `dynamic_cast`는 가상 함수를 대체하는 기본 수단이 아니라, 구체적인 파생 기능이 꼭 필요할 때 고려할 도구입니다.

**예제 코드 — [09_dynamic_cast.cpp](./examples/09_dynamic_cast.cpp)**

```cpp
#include <iostream>

class Device {
public:
    virtual ~Device() = default;
};
class Camera final : public Device {
public:
    [[nodiscard]] int frames_per_second() const noexcept { return 60; }
};
class Motor final : public Device {};

void inspect(const Device& device) {
    const auto* camera = dynamic_cast<const Camera*>(&device);
    if (camera == nullptr) {
        std::cout << "Not a camera\n";
        return;
    }
    std::cout << "Camera FPS: " << camera->frames_per_second() << '\n';
}
int main() {
    const Camera camera;
    const Motor motor;
    inspect(camera);
    inspect(motor);
}
```

**실행 결과**

```text
Camera FPS: 60
Not a camera
```

---

<a id="section-9-11"></a>

## 9.11. Composition — 상속보다 합성이 적합한 관계

**합성(Composition)** 은 한 객체가 다른 객체를 자신의 멤버로 포함하는 방식입니다. `Robot`과 `Battery`는 종류 관계가 아니라 구성 관계이므로 `Robot : public Battery`보다 `Robot` 안에 `Battery`를 멤버로 두는 편이 자연스럽습니다.

예제에서 `Robot::move()`는 배터리에 필요한 전력 소비를 요청합니다. 배터리 잔량의 검사와 변경은 `Battery`가 책임지므로 두 클래스의 역할이 분명합니다.
| 관계 | 적합한 설계 | 판단 기준 |
|---|---|---|
| `Camera`는 `Device`의 한 종류 | 공개 상속 고려 | 기본 타입 대신 사용 가능 |
| `Robot`은 `Battery`를 가진다 | 합성 고려 | 포함 관계·기능 위임 |
| `Robot`이 여러 모터를 관리 | 합성 고려 | 부품의 개수와 수명 관리 |

상속은 코드 재사용만을 위해 선택하지 않습니다. 변경이 자주 발생하는 구현 세부사항은 합성으로 분리하는 편이 구조를 단순하게 만들 수 있습니다.

**예제 코드 — [10_composition_vs_inheritance.cpp](./examples/10_composition_vs_inheritance.cpp)**

```cpp
#include <iostream>

class Battery {
public:
    explicit Battery(int percent) : percent_{percent} {}
    [[nodiscard]] bool consume(int amount) noexcept {
        if (amount < 0 || amount > percent_) return false;
        percent_ -= amount;
        return true;
    }
    [[nodiscard]] int percent() const noexcept { return percent_; }
private:
    int percent_{};
};
class Robot {
public:
    explicit Robot(int battery_percent) : battery_{battery_percent} {}
    [[nodiscard]] bool move() noexcept { return battery_.consume(10); }
    [[nodiscard]] int battery() const noexcept { return battery_.percent(); }
private:
    Battery battery_;
};
int main() {
    Robot robot{35};
    const bool moved = robot.move();
    std::cout << std::boolalpha << "Moved: " << moved << ", battery: "
              << robot.battery() << "%\n";
}
```

**실행 결과**

```text
Moved: true, battery: 25%
```

---

<a id="section-9-12"></a>

## 9.12. Interface Segregation — 인터페이스 역할 분리

**인터페이스 분리 원칙(Interface Segregation Principle, ISP)** 은 사용하지 않는 기능에 대한 의존을 강요하지 않도록 인터페이스를 작게 구분하자는 설계 원칙입니다.

예제에서는 측정값을 읽는 `Reader`와 상태를 초기화하는 `Resettable`을 나눴습니다. `CounterSensor`는 두 역할을 구현하지만, 읽기만 하는 함수는 `Reader&`만 받으면 됩니다. 실제로 초기화할 권한이 필요하지 않다면 `Resettable`을 노출할 이유가 없습니다.

C++은 여러 기본 클래스를 상속할 수 있습니다. 하지만 다중 상속을 무분별하게 사용하면 상태 소유와 이름 충돌 문제가 복잡해질 수 있습니다. 이 예제처럼 **상태가 없는 작은 인터페이스를 조합**하는 경우부터 이해하는 것이 좋습니다.

**예제 코드 — [11_interface_segregation.cpp](./examples/11_interface_segregation.cpp)**

```cpp
#include <iostream>

class Reader {
public:
    virtual ~Reader() = default;
    [[nodiscard]] virtual int read() const noexcept = 0;
};
class Resettable {
public:
    virtual ~Resettable() = default;
    virtual void reset() noexcept = 0;
};
class CounterSensor final : public Reader, public Resettable {
public:
    [[nodiscard]] int read() const noexcept override { return count_; }
    void reset() noexcept override { count_ = 0; }
    void tick() noexcept { ++count_; }
private:
    int count_{};
};
int main() {
    CounterSensor counter;
    counter.tick();
    const Reader& reader = counter;
    Resettable& control = counter;
    std::cout << "Before: " << reader.read() << '\n';
    control.reset();
    std::cout << "After: " << reader.read() << '\n';
}
```

**실행 결과**

```text
Before: 1
After: 0
```

---

<a id="section-9-13"></a>

## 9.13. Non-Virtual Interface — 공통 검증을 한 곳에서

**비가상 인터페이스(Non-Virtual Interface, NVI)** 패턴은 외부에 공개한 일반 멤버 함수에서 공통 처리를 수행한 뒤, 내부 가상 함수에 실제 구현을 맡기는 방식입니다.

`AlarmRule::check()`는 모든 알람 규칙에 공통인 입력 범위 `0~100`을 확인합니다. 파생 클래스가 구현하는 `check_valid()`는 이미 유효하다고 판정된 값만 받습니다. 따라서 파생 클래스마다 같은 범위 검증을 반복하지 않아도 됩니다.

여기서 `check_valid()`는 `private virtual`입니다. C++에서는 `private` 가상 함수도 파생 클래스에서 재정의할 수 있습니다. 접근 제어와 가상 함수 재정의 가능 여부를 같은 개념으로 혼동하지 않아야 합니다.

**예제 코드 — [12_nonvirtual_interface.cpp](./examples/12_nonvirtual_interface.cpp)**

```cpp
#include <iostream>

class AlarmRule {
public:
    virtual ~AlarmRule() = default;
    [[nodiscard]] bool check(int reading) const noexcept {
        if (reading < 0 || reading > 100) return false;
        return check_valid(reading);
    }
private:
    [[nodiscard]] virtual bool check_valid(int reading) const noexcept = 0;
};
class HighAlarm final : public AlarmRule {
private:
    [[nodiscard]] bool check_valid(int reading) const noexcept override {
        return reading >= 80;
    }
};
int main() {
    const HighAlarm alarm;
    std::cout << std::boolalpha << "Invalid: " << alarm.check(110)
              << ", high: " << alarm.check(90) << '\n';
}
```

**실행 결과**

```text
Invalid: false, high: true
```

---

<a id="section-9-14"></a>

## 9.14. Dependency Injection — 의존성 주입과 테스트 대역

**의존성 주입(Dependency Injection, DI)** 은 함수나 객체가 필요한 외부 기능을 직접 생성하지 않고 인수 등으로 전달받는 설계 방식입니다. 테스트에서는 실제 네트워크나 하드웨어 대신 동작을 제어할 수 있는 **테스트 대역(Test Double)** 을 전달할 수 있습니다.

`Transport`는 메시지 전송 기능을 정의하고, `FakeTransport`는 실제 전송 대신 문자열을 메모리에 기록합니다. 테스트는 `send_alarm()`을 호출한 뒤 기록된 메시지가 정확한지 확인합니다.

이 예제는 별도의 네트워크 연결 없이 실행됩니다. `FakeTransport`는 메시지를 저장하는 단순한 **페이크(Fake)** 이며, 실패한 전송 상황을 시험하려면 실패를 반환하는 별도의 구현을 전달하면 됩니다. 실제 외부 의존성을 분리하면 테스트의 실행 환경과 결과를 더 쉽게 통제할 수 있습니다.

**예제 코드 — [13_dependency_injection_test.cpp](./examples/13_dependency_injection_test.cpp)**

```cpp
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

class Transport {
public:
    virtual ~Transport() = default;
    virtual bool send(std::string_view text) = 0;
};
class FakeTransport final : public Transport {
public:
    bool send(std::string_view text) override {
        messages_.emplace_back(text);
        return true;
    }
    [[nodiscard]] const std::vector<std::string>& messages() const noexcept {
        return messages_;
    }
private:
    std::vector<std::string> messages_;
};
[[nodiscard]] bool send_alarm(Transport& transport, std::string_view message) {
    return !message.empty() && transport.send(message);
}
int main() {
    FakeTransport fake;
    const bool sent = send_alarm(fake, "OVERHEAT");
    const bool blocked = !send_alarm(fake, "");
    const bool correct = sent && blocked && fake.messages().size() == 1 &&
                         fake.messages().front() == "OVERHEAT";
    std::cout << "Transport test: " << (correct ? "PASS" : "FAIL") << '\n';
    return correct ? 0 : 1;
}
```

**실행 결과**

```text
Transport test: PASS
```

---

<a id="section-9-15"></a>

## 9.15. `std::variant` — 상속 없이 여러 타입 표현하기

동적 다형성이 항상 필요한 것은 아닙니다. **가능한 타입 종류가 미리 정해져 있다면** `std::variant`를 고려할 수 있습니다. `<variant>` 헤더는 여러 지정된 타입 중 하나의 값을 담는 `std::variant`와 현재 보유한 타입을 확인하는 `std::get_if` 등을 제공합니다. 이 기능은 C++17부터 사용할 수 있습니다.

예제의 `reading`에는 `Temperature` 또는 `Distance` 값이 저장됩니다. `std::get_if<Distance>(&reading)`는 현재 보관된 값이 `Distance`라면 그 주소를, 아니면 `nullptr`를 반환합니다.
| 구분 | 가상 함수 기반 | `std::variant` 기반 |
|---|---|---|
| 새로운 타입 추가 | 파생 클래스 정의 | `variant` 타입 목록 수정 |
| 값 저장 | 포인터·참조를 사용하는 경우 많음 | 값 자체를 보관 |
| 실행할 동작 선택 | 가상 함수 호출 | `std::get_if`, `std::visit` 등 |
| 적합한 상황 | 구현 종류가 열려 있는 구조 | 구현 종류가 제한된 구조 |

`std::variant`가 언제나 더 빠르거나 적절하다고 단정할 수는 없습니다. 타입 집합이 자주 바뀌는지, 저장 형태와 인터페이스가 무엇인지에 따라 선택합니다.

**예제 코드 — [14_variant_alternative.cpp](./examples/14_variant_alternative.cpp)**

```cpp
#include <iostream>
#include <variant>

struct Temperature { int celsius{}; };
struct Distance { int centimeters{}; };

int main() {
    const std::variant<Temperature, Distance> reading{Distance{35}};
    if (const auto* distance = std::get_if<Distance>(&reading)) {
        std::cout << "Distance: " << distance->centimeters << " cm\n";
    } else if (const auto* temperature = std::get_if<Temperature>(&reading)) {
        std::cout << "Temperature: " << temperature->celsius << " C\n";
    }
}
```

**실행 결과**

```text
Distance: 35 cm
```

---

<a id="section-9-16"></a>

## 9.16. Construction & Dispatch — 생성 중 가상 함수 호출

기본 클래스 생성자에서 가상 함수를 호출한다고 해서 **아직 생성되지 않은 파생 클래스의 재정의 함수**가 실행되지는 않습니다. 객체가 생성되는 동안에는 현재 생성 중인 클래스 단계의 가상 함수 구현이 사용됩니다. 소멸 과정에서도 같은 종류의 제약이 있습니다.

예제의 `Base()` 생성자 안에서 `label()`은 `"base"`를 반환합니다. 이후 `Derived()` 생성자에서는 `"derived"`가 출력되고, 완전히 생성된 다음에는 파생 구현이 호출됩니다.

따라서 파생 클래스의 상태에 의존하는 초기화 작업을 기본 클래스 생성자에서 가상 함수로 호출하도록 설계하지 않는 것이 좋습니다. 필요한 값은 생성자 매개변수로 전달하거나, 객체 생성이 완료된 뒤 명시적으로 초기화 작업을 수행하는 방법을 고려할 수 있습니다.

**예제 코드 — [15_constructor_dispatch.cpp](./examples/15_constructor_dispatch.cpp)**

```cpp
#include <iostream>

class Base {
public:
    Base() { std::cout << "Base constructor: " << label() << '\n'; }
    virtual ~Base() = default;
    [[nodiscard]] virtual const char* label() const noexcept { return "base"; }
};
class Derived final : public Base {
public:
    Derived() { std::cout << "Derived constructor: " << label() << '\n'; }
    [[nodiscard]] const char* label() const noexcept override { return "derived"; }
};
int main() {
    const Derived item;
    std::cout << "After construction: " << item.label() << '\n';
}
```

**실행 결과**

```text
Base constructor: base
Derived constructor: derived
After construction: derived
```

---

<a id="section-9-17"></a>

## 9.17. Coding Practice

`exercises/`에는 주요 구현이 비어 있는 시작 코드가 있고, `solutions/`에는 모범답안이 있습니다. 실습 파일은 컴파일되지만, TODO를 완성하기 전에는 정답 결과가 나오지 않습니다.
| 번호 | 실습 | 시작 코드 | 모범답안 |
|:---:|---|---|---|
| 01 | Alarm Channels | [01_alarm_channels.cpp](./exercises/01_alarm_channels.cpp) | [정답](./solutions/01_alarm_channels.cpp) |
| 02 | Robot Motor | [02_robot_motor.cpp](./exercises/02_robot_motor.cpp) | [정답](./solutions/02_robot_motor.cpp) |
| 03 | Sensor Registry | [03_sensor_registry.cpp](./exercises/03_sensor_registry.cpp) | [정답](./solutions/03_sensor_registry.cpp) |
| 04 | Fault Detector | [04_fault_detector.cpp](./exercises/04_fault_detector.cpp) | [정답](./solutions/04_fault_detector.cpp) |

### Exercise 01 — Alarm Channels

`Alarm` 인터페이스를 상속한 `HighAlarm`의 `triggered()`를 완성합니다. 기본 클래스 참조를 통해 호출하더라도 파생 클래스의 판정 결과가 반환되어야 합니다.

**구현 조건**

- 판정값이 임계값 이상이면 `true`, 그렇지 않으면 `false` 반환
- 임계값과 정확히 같은 경계값도 경보에 포함
- 반환값만 계산하며 함수 내부에서 출력하지 않음

**기대 출력**

```text
79: false, 80: true
```

### Exercise 02 — Robot Motor

`Motor` 인터페이스를 구현한 `ElectricMotor`에서 속도 설정을 완성합니다.

**구현 조건**

- 요청 속도 `0~3000` RPM만 허용하며 성공 시 `true` 반환
- 허용 범위가 아닌 요청은 거절하고 이전 속도 유지
- `Motor&`를 통한 호출에서도 같은 결과가 나와야 함

**기대 출력**

```text
First: true, second: false, RPM: 2000
```

### Exercise 03 — Sensor Registry

서로 다른 센서를 `std::unique_ptr<Sensor>`로 보관하는 컨테이너에서 임계값 이상인 센서의 수를 계산합니다.

**구현 조건**

- `read()`는 기본 클래스 포인터를 통해 호출
- 임계값 이상인 센서만 개수에 포함
- 포인터가 `nullptr`인 요소는 건너뜀
- 컨테이너가 비어 있으면 `0` 반환

**기대 출력**

```text
High: 2
```

### Exercise 04 — Fault Detector

`Transport` 인터페이스로 전송 기능을 전달받는 `report_fault()`를 완성합니다.

**구현 조건**

- 오류 코드가 양수일 때만 `FAULT:<code>` 문자열 전송
- 오류 코드가 0 이하이면 전송하지 않고 `false` 반환
- 정상 코드에서는 `transport.send()`의 성공 여부 반환
- 실제 네트워크 대신 `FakeTransport`의 메시지 기록으로 검증

**기대 출력**

```text
Sent: true, rejected: false, messages: 1
```

**컴파일 및 실행** — `Chapter-09/` 폴더 기준

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/01_alarm_channels.cpp -o alarm_channels
./alarm_channels
```

모범답안을 실행할 때는 `exercises/`를 `solutions/`로 바꾸면 됩니다.

<a id="section-9-18"></a>

## 9.18. Mini Project — Robot Sensor Monitor

온도 센서와 거리 센서의 측정값을 입력받아 각 센서의 경고 상태와 전체 경고 수를 출력하는 콘솔 프로그램입니다. 두 센서의 임계값은 서로 다르지만, `Sensor` 추상 클래스를 사용해 공통 방식으로 처리합니다.

**구현할 부분**

- `TemperatureSensor::alert()` : 온도 `80` 이상이면 `ALERT`
- `DistanceSensor::alert()` : 거리 `30` 이하이면 `ALERT`
- `count_alerts()` : 기본 클래스 포인터를 순회하며 경고 센서 수 계산

**입력 조건**
| 항목 | 유효 범위 |
|---|---|
| 센서 수 | 정수 `1~5` |
| 타입 | `TEMP`, `DIST` 중 하나 |
| 온도(`TEMP`) | 정수 `-40~125` |
| 거리(`DIST`) | 정수 `0~400` |

입력의 타입 또는 값이 올바르지 않으면 오류 메시지를 `std::cerr`에 출력하고 종료합니다. 센서 종류는 대문자로 입력합니다.

**실행 예시**

```text
Sensors (1-5): 3
Sensor 1 (TEMP/DIST value): TEMP 75
Sensor 2 (TEMP/DIST value): DIST 22
Sensor 3 (TEMP/DIST value): TEMP 85
--- Robot Sensor Monitor ---
TEMP 75: CLEAR
DIST 22: ALERT
TEMP 85: ALERT
Total: 3
Alerts: 2
```

**프로젝트 파일**

- [시작 코드 — `project/robot_monitor.cpp`](./project/robot_monitor.cpp)
- [모범답안 — `solutions/robot_monitor.cpp`](./solutions/robot_monitor.cpp)

**완료 기준**

1. 각 파생 클래스의 `alert()`가 자기 기준으로 경보를 판정합니다.
2. `std::unique_ptr<Sensor>`로 객체를 보관하고, 가상 함수로 상태를 조회합니다.
3. 정상 입력, 경계값, 잘못된 센서 타입을 구분하여 처리합니다.
4. 정답을 복사하지 않고 작성한 코드가 프로젝트 테스트를 통과합니다.

**시작 코드 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/robot_monitor.cpp -o robot_monitor
./robot_monitor
```

### 다중 파일 예제 — CMake

앞서 학습한 내용을 함수와 클래스별 파일로 분리한 완성 예제를 `examples/16_robot_monitor/`에 제공합니다. 이 예제는 고정된 데이터를 사용하므로 입력 없이 실행할 수 있으며, GitHub CI에서도 같은 경로를 빌드합니다.

```text
examples/16_robot_monitor/
├── CMakeLists.txt
├── monitor.hpp
├── monitor.cpp
└── main.cpp
```

- [`monitor.hpp`](./examples/16_robot_monitor/monitor.hpp) : 클래스 선언 및 공개 인터페이스
- [`monitor.cpp`](./examples/16_robot_monitor/monitor.cpp) : 멤버 함수와 집계 구현
- [`main.cpp`](./examples/16_robot_monitor/main.cpp) : 센서 등록과 출력
- [`CMakeLists.txt`](./examples/16_robot_monitor/CMakeLists.txt) : 빌드·테스트 설정

**직접 컴파일**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic \
  examples/16_robot_monitor/main.cpp examples/16_robot_monitor/monitor.cpp -o robot_monitor_demo
./robot_monitor_demo
```

**CMake 빌드 및 테스트**

```bash
cmake -S examples/16_robot_monitor -B build/chapter09 -DCMAKE_CXX_STANDARD=20
cmake --build build/chapter09
ctest --test-dir build/chapter09 --output-on-failure
```

CMake는 여러 소스 파일의 빌드 설정을 관리하는 도구입니다. `CTest`는 CMake 프로젝트에 등록된 테스트를 실행합니다. 여기서는 `--self-test`로 세 센서에 대한 예상 집계 결과를 검사합니다.

### 자동 테스트

Python 3가 설치되어 있다면 `Chapter-09/`에서 다음 명령어로 실행할 수 있습니다.

```bash
python tests/check.py
python tests/check.py --mode student --only exercise-01
python tests/check.py --mode student --only project
```

**첫 번째 명령어**는 예제·모범답안·프로젝트 정답을 검사합니다. **두 번째 명령어**는 직접 수정한 Exercise 01을, **세 번째 명령어**는 프로젝트 시작 코드를 검사합니다. 실습 코드가 미완성인 초기 상태에서는 FAIL이 발생하는 것이 정상입니다. 테스트 실행기(Test Runner)는 내부에서 C++ 소스를 컴파일하고 실행 결과와 함수 동작을 확인합니다.

컴파일러가 `g++`가 아닌 경우 `--compiler g++-14` 또는 `--compiler clang++` 옵션으로 지정할 수 있습니다.

<a id="section-9-19"></a>

## 9.19. Quiz & Summary

### Quiz

**Q1.** **`virtual`과 `override`의 역할로 올바른 것은 무엇인가요?**

A. `virtual`은 동적 디스패치를 지원하고 `override`는 재정의를 검사합니다.
B. `override`는 함수 호출을 막는 키워드입니다.
C. `virtual`은 모든 함수를 자동으로 `static`으로 만듭니다.
D. 두 키워드는 같은 의미입니다.

<details>
<summary>정답 및 해설</summary>

**정답: A**

`virtual`은 기본 클래스의 멤버 함수를 가상 함수로 선언합니다. `override`는 파생 클래스 함수가 실제로 기본 클래스의 가상 함수를 재정의하는지 확인하므로 이름·매개변수·`const` 지정 등의 실수를 발견하는 데 도움이 됩니다.

</details>

**Q2.** **기본 클래스 참조를 이용한 가상 함수 호출은 어떤 구현을 실행하나요?**

A. 항상 기본 클래스 구현
B. 실제 객체 타입의 최종 재정의 구현
C. 가장 먼저 선언한 구현
D. 무작위 구현

<details>
<summary>정답 및 해설</summary>

**정답: B**

기본 클래스 참조가 `Derived` 객체를 가리킨다면, 가상 함수는 실제 객체의 최종 재정의 구현을 호출합니다. 일반 멤버 함수와 구별해야 합니다.

</details>

**Q3.** **파생 객체를 `void process(Base value)`에 전달할 때 발생할 수 있는 문제를 설명하세요.**

<details>
<summary>정답 및 해설</summary>

파생 클래스 부분이 잘리는 객체 슬라이싱이 발생할 수 있습니다. `value`는 독립적인 기본 클래스 객체가 되므로 원본 파생 객체의 다형적 동작이 유지되지 않습니다. 다형성이 필요하면 `const Base&` 또는 `Base&`를 고려합니다.

</details>

**Q4.** **파생 객체를 `std::unique_ptr<Base>`로 소유할 때 기본 클래스의 소멸자는 어떻게 설계하는 것이 일반적인가요?**

<details>
<summary>정답 및 해설</summary>

기본 클래스에서 `public virtual ~Base() = default;`와 같은 공개 가상 소멸자를 제공하는 것이 일반적입니다. 그래야 기본 클래스 포인터를 통해 삭제할 때 파생 객체와 기본 객체 부분이 올바르게 소멸합니다.

</details>

**Q5.** **`dynamic_cast<Derived*>(pointer)`가 실패하면 무엇을 반환하나요?**

A. 빈 객체
B. `false`
C. `nullptr`
D. `std::nullopt`

<details>
<summary>정답 및 해설</summary>

**정답: C**

다형적 기본 클래스로부터 파생 클래스로 포인터를 검사 변환할 때 실패하면 `nullptr`가 반환됩니다. 참조로 변환하는 경우에는 실패 시 `std::bad_cast` 예외가 발생한다는 점도 함께 구분합니다.

</details>

**Q6.** **`Robot`이 `Battery`를 구성 요소로 가진다면 어떤 설계가 더 적절한가요? 그 이유는 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

일반적으로 합성(Composition)이 적합합니다. `Robot`은 `Battery`의 한 종류가 아니라 배터리를 포함하는 객체이기 때문입니다. 배터리의 소비·잔량 관리는 `Battery`에 맡길 수 있어 책임이 구분됩니다.

</details>

**Q7.** **`final`을 클래스 선언에 붙이면 어떤 효과가 있나요?**

A. 모든 멤버가 자동으로 `private`이 됩니다.
B. 해당 클래스를 더 이상 상속할 수 없습니다.
C. 모든 함수가 자동으로 가상 함수가 됩니다.
D. 생성자가 호출되지 않습니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

`class HighAlarm final`처럼 선언하면 `HighAlarm`을 기본 클래스로 하는 추가 파생 클래스를 정의할 수 없습니다. 가상 함수에 `final`을 붙이면 그 함수를 추가로 재정의하는 것을 막습니다.

</details>

**Q8.** **추상 클래스로 직접 객체를 만들 수 없는 이유는 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

추상 클래스에는 최종 재정의되지 않은 순수 가상 함수가 남아 있기 때문입니다. 인터페이스로 설계한 추상 클래스는 파생 클래스가 필요한 함수를 구현한 뒤 인스턴스화합니다.

</details>

**Q9.** **생성 중인 기본 클래스에서 가상 함수를 호출하면 가장 아래 파생 클래스 구현이 실행되나요?**

A. 항상 실행됨
B. 실행 순서는 컴파일러마다 임의로 다름
C. 현재 생성 중인 클래스 단계의 구현이 사용됨
D. `override`가 있으면 반드시 파생 구현이 실행됨

<details>
<summary>정답 및 해설</summary>

**정답: C**

기본 클래스 생성 중에는 파생 클래스 부분이 아직 완성되지 않았으므로 해당 기본 클래스 단계의 최종 재정의 구현이 호출됩니다. 파생 상태를 전제하는 가상 함수 호출로 초기화하지 않는 편이 안전합니다.

</details>

**Q10.** **`std::unique_ptr<Sensor>`와 `Sensor&`의 차이를 소유권 관점에서 설명하세요.**

<details>
<summary>정답 및 해설</summary>

`std::unique_ptr<Sensor>`는 객체의 독점 소유권을 관리하고 소유자가 소멸하면 객체의 소멸도 처리합니다. `Sensor&`는 기존 객체를 참조할 뿐 소유권을 갖거나 수명을 연장하지 않습니다.

</details>

**Q11.** **센서 종류가 고정된 몇 가지 값 타입뿐이라면 가상 함수 대신 무엇을 고려할 수 있나요?**

A. `std::variant`
B. `std::thread`
C. `std::fstream`
D. `std::mutex`

<details>
<summary>정답 및 해설</summary>

**정답: A**

`std::variant`는 미리 지정한 타입 중 하나의 값을 보관할 수 있습니다. 모든 경우에 가상 함수보다 낫다는 의미는 아니며, 타입 집합이 제한되어 있고 값으로 다루는 것이 적합할 때 검토합니다.

</details>

**Q12.** **`FakeTransport`를 이용한 테스트에서 무엇을 검증해야 하나요?**

<details>
<summary>정답 및 해설</summary>

`send_alarm()`의 성공 여부뿐 아니라 실제로 기록된 메시지의 개수와 내용, 빈 메시지 전달 시 전송하지 않는 정책 등을 확인해야 합니다. 외부 통신 없이도 의도한 동작을 검증하는 것이 목적입니다.

</details>

### Summary

- **상속(Inheritance):** 기본 클래스와 파생 클래스의 타입 관계를 표현합니다.
- **동적 다형성(Dynamic Polymorphism):** 가상 함수를 기본 클래스 포인터·참조를 통해 호출하고, 실제 객체에 맞는 구현을 실행합니다.
- **`override` / `final`:** 재정의의 정확성을 검사하거나 추가 상속·재정의를 제한합니다.
- **추상 클래스(Abstract Class):** 순수 가상 함수로 공통 인터페이스를 표현합니다.
- **가상 소멸자(Virtual Destructor):** 기본 포인터를 통한 다형적 객체 삭제의 올바른 소멸 동작을 지원합니다.
- **소유권(Ownership):** `std::unique_ptr`는 객체의 수명을 관리하고 참조·일반 포인터는 대체로 비소유 접근에 사용합니다.
- **객체 슬라이싱(Object Slicing):** 파생 객체를 기본 클래스 값으로 복사하면서 파생 부분이 손실될 수 있습니다.
- **합성(Composition):** 구성 요소를 멤버로 포함할 때 상속보다 자연스러울 수 있습니다.
- **의존성 주입(DI):** 구현을 외부에서 전달받아 실제 장치 없이도 테스트할 수 있게 합니다.
- **`std::variant`:** 가능한 값의 타입이 미리 정해진 경우 고려할 수 있는 대안입니다.

### References

- [cppreference — Derived classes](https://en.cppreference.com/w/cpp/language/derived_class)
- [cppreference — Virtual functions](https://en.cppreference.com/w/cpp/language/virtual)
- [cppreference — Abstract classes](https://en.cppreference.com/w/cpp/language/abstract_class)
- [cppreference — `dynamic_cast`](https://en.cppreference.com/w/cpp/language/dynamic_cast)
- [cppreference — `std::unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [cppreference — `std::variant`](https://en.cppreference.com/w/cpp/utility/variant)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

---

[← C++ 목차](../README.md#contents) · [이전 Chapter — Structs & Classes](../Chapter-08/) · [다음 Chapter — Standard Library (STL)](../Chapter-10/)
