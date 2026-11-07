# Chapter 12. Modern C++ & Resource Management

C++23의 Resource Management, 객체 수명, Ownership, RAII, Move Semantics, Copy/Move 설계와 Exception Safety를 다룹니다. Chapter 07의 포인터·참조와 Chapter 08의 클래스 설계를 바탕으로 **자원 획득부터 해제까지의 책임을 코드에 명확하게 표현하는 방법**을 학습합니다.

본 자료는 **C++23(ISO/IEC 14882:2024)**을 기준으로 작성되었습니다. 일부 예제는 `<print>`, `<expected>`를 사용하므로 해당 C++23 표준 라이브러리를 지원하는 컴파일러가 필요합니다. GCC 14 이상 환경을 권장합니다.

**선행 학습:** [Chapter 05 — Functions](../Chapter-05/) · [Chapter 07 — Pointers & References](../Chapter-07/) · [Chapter 08 — Structs & Classes](../Chapter-08/) · [Chapter 11 — File I/O](../Chapter-11/)

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [12.1](#section-12-1) | Resource Management와 객체 수명 |
| [12.2](#section-12-2) | RAII와 자원 정리 |
| [12.3](#section-12-3) | Ownership과 Borrowing |
| [12.4](#section-12-4) | `std::unique_ptr` — 단일 소유권 |
| [12.5](#section-12-5) | Custom Deleter — 외부 자원 관리 |
| [12.6](#section-12-6) | Value Category와 이동 참조 |
| [12.7](#section-12-7) | Move Semantics와 `std::move` |
| [12.8](#section-12-8) | Move-Only Type과 소유권 이전 |
| [12.9](#section-12-9) | Copy/Move Constructor와 Special Member Function |
| [12.10](#section-12-10) | Rule of Zero — 자동 자원 관리 |
| [12.11](#section-12-11) | Rule of Five — 직접 관리해야 하는 경우 |
| [12.12](#section-12-12) | `std::exchange`와 이동 후 상태 |
| [12.13](#section-12-13) | Copy Elision과 NRVO |
| [12.14](#section-12-14) | `noexcept`와 `std::move_if_noexcept` |
| [12.15](#section-12-15) | Exception Safety — 상태 변경의 원자성 |
| [12.16](#section-12-16) | Borrowed View와 Dangling Reference |
| [12.17](#section-12-17) | `std::expected`로 전달하는 소유권과 오류 |
| [12.18](#section-12-18) | Perfect Forwarding — 다음 Chapter 연결 |
| [12.19](#section-12-19) | Mini Project — Device Session Manager |
| [12.20](#section-12-20) | 설계 시 참고 사항 |
| [12.21](#section-12-21) | Coding Practice |
| [12.22](#section-12-22) | Quiz & Summary |

---

<a id="section-12-1"></a>

## 12.1. Resource Management와 객체 수명


리소스 관리(Resource Management)는 파일, 메모리, 잠금, 장치 연결처럼 **획득과 반환이 필요한 자원**을 다루는 작업입니다. 일반 객체의 저장 공간도 자원이지만, 메모리 외에 운영체제가 제공하는 Handle이나 네트워크 연결 등도 포함됩니다.

객체 수명(Object Lifetime, Lifetime)은 객체가 생성되어 사용할 수 있는 기간을 의미합니다. 객체가 유효한 범위와 자원을 소유한 기간은 일치할 수도, 다를 수도 있습니다.

| 개념 | 의미 | 예시 |
|---|---|---|
| 스코프(Scope) | 이름을 참조할 수 있는 코드 범위 | 중괄호 `{}` |
| Lifetime | 객체가 존재하는 기간 | 지역 변수 생성부터 소멸까지 |
| 자원(Resource) | 획득·해제가 필요한 대상 | 파일 Handle, 메모리, Mutex |
| 소유권(Ownership) | 자원 해제 책임 | `std::unique_ptr` 소유자 |
| 대여(Borrowing) | 해제 책임 없이 일시적으로 접근 | `const T&`, `std::span` |

지역 객체는 자신이 속한 블록을 벗어날 때 **생성 순서의 역순으로 소멸**합니다. 동적 할당 자원의 경우에도 이를 관리하는 객체를 스코프에 배치하면 해제 시점을 자동으로 제어할 수 있습니다.

**예제 코드 — [01_scope_lifetime.cpp](./examples/01_scope_lifetime.cpp)**

```cpp
#include <print>
#include <string_view>

class Trace {
public:
    explicit Trace(std::string_view name) : name_(name) {
        std::println("Open: {}", name_);
    }
    ~Trace() { std::println("Close: {}", name_); }
    Trace(const Trace&) = delete;
    Trace& operator=(const Trace&) = delete;
private:
    std::string_view name_;  // 호출 중 유효한 문자열 리터럴을 참조
};

int main() {
    Trace outer{"outer"};
    {
        Trace inner{"inner"};
        std::println("Working");
    }
    std::println("End of main");
}
```

**실행 결과**

```text
Open: outer
Open: inner
Working
Close: inner
End of main
Close: outer
```

`inner` 객체는 내부 블록이 끝나는 시점에 먼저 소멸하고, `outer`는 `main()`을 빠져나갈 때 소멸합니다. `Trace`에 보관한 `std::string_view`는 이 예제에서 프로그램 전체에 걸쳐 유효한 문자열 리터럴만 참조합니다.

---

<a id="section-12-2"></a>

## 12.2. RAII와 자원 정리


자원 획득 즉 초기화(Resource Acquisition Is Initialization, RAII)는 자원을 객체의 생성과 연결하고, 소멸자를 통해 해제하는 설계 방식입니다. 자원을 얻은 직후 소유 객체에 맡겨 **함수의 여러 반환 경로와 예외 발생 시에도 정리**되도록 하는 것이 핵심입니다.

```text
자원 획득 → RAII 객체 생성 → 자원 사용 → Scope 종료 → 소멸자에 의한 반환
```

- **획득 시점:** 생성자 또는 Factory Method로 유효한 자원 확보
- **사용 기간:** 소유 객체가 자원의 유효성을 관리
- **종료 시점:** 정상 반환이나 예외 처리 과정에서 객체 소멸
- **주의:** 프로세스 강제 종료·전원 차단 등에서는 일반적인 소멸자 실행을 보장하지 않음

잠금 가드(Lock Guard)는 RAII의 대표 사례입니다. `std::lock_guard`는 생성 시 Mutex를 잠그고 소멸 시 잠금을 해제합니다. 실제 여러 Thread를 사용하는 환경에서는 데이터 경쟁(Data Race)과 잠금 순서도 별도로 고려해야 합니다.

**예제 코드 — [02_raii_lock_guard.cpp](./examples/02_raii_lock_guard.cpp)**

```cpp
#include <mutex>
#include <print>

class Counter {
public:
    void increment() {
        std::lock_guard<std::mutex> lock{mutex_};
        ++value_;
    }
    [[nodiscard]] int read() const {
        std::lock_guard<std::mutex> lock{mutex_};
        return value_;
    }
private:
    mutable std::mutex mutex_;
    int value_{0};
};

int main() {
    Counter counter;
    counter.increment();
    counter.increment();
    std::println("Count: {}", counter.read());
}
```

**실행 결과**

```text
Count: 2
```

`read()`에서도 동일한 Mutex를 사용하므로 값을 읽는 동안 쓰기 작업과의 충돌을 막습니다. `mutable`은 논리적으로 읽기 전용인 멤버 함수에서 내부 동기화용 Mutex를 잠글 수 있도록 사용합니다. Concurrency의 세부 내용은 Chapter 14에서 다룹니다.

---

<a id="section-12-3"></a>

## 12.3. Ownership과 Borrowing


Ownership은 **누가 자원을 반환해야 하는지**에 관한 계약입니다. 반면 Borrowing은 자원을 소유하지 않고 제한된 기간에 접근하는 방식입니다.

| 전달 방법 | Ownership 이전 | 주된 의미 |
|---|:---:|---|
| `T` 값 전달 | 타입에 따라 복사·이동 | 독립적인 값을 받음 |
| `const T&` | X | 읽기 전용 Borrowing |
| `T&` | X | 변경 가능한 Borrowing |
| `T*` | 일반적으로 X | nullable 대상을 나타낼 수 있음 |
| `std::span<T>` | X | 연속 데이터의 Borrowing |
| `std::unique_ptr<T>` 값 전달 | O | 단일 소유권 이전 |
| `std::shared_ptr<T>` 값 전달 | 공유 | 공동 소유권 참여 |

**핵심:** Raw Pointer를 전달한다고 자동으로 Ownership이 이전되는 것은 아닙니다. 호출자가 삭제해야 하는지 불분명한 API보다 소유권 타입이 드러나는 API가 좋습니다.

`std::shared_ptr`는 여러 객체가 같은 자원을 함께 소유할 필요가 있을 때 사용합니다. 단순히 객체를 읽는다는 이유로 공유 소유권을 도입할 필요는 없습니다. 순환 참조는 `std::weak_ptr`로 끊을 수 있지만, 가능하면 Ownership 관계 자체를 단순하게 설계합니다.

---

<a id="section-12-4"></a>

## 12.4. `std::unique_ptr` — 단일 소유권


`std::unique_ptr<T>`는 동적으로 생성한 객체를 **하나의 소유자**가 관리하도록 하는 Smart Pointer입니다. `std::make_unique<T>(...)`를 사용하면 소유 객체를 간단하게 만들 수 있습니다.

- `*owner`, `owner->member` — 소유한 객체 접근
- `owner.get()` — Ownership을 넘기지 않고 Raw Pointer만 조회
- `std::move(owner)` — 소유권을 이전할 수 있도록 rvalue로 변환
- `owner.reset()` — 현재 소유 자원 해제 또는 다른 자원으로 변경
- `owner.release()` — 해제 없이 Ownership 포기. 반환된 Raw Pointer를 관리할 명확한 주체가 필요함

일시적으로 객체를 관찰하는 함수에는 `const T&` 등 Borrowing 타입을 우선 고려합니다.

**예제 코드 — [03_unique_ownership.cpp](./examples/03_unique_ownership.cpp)**

```cpp
#include <memory>
#include <print>
#include <string>
#include <utility>

struct Device {
    std::string name;
    explicit Device(std::string value) : name(std::move(value)) {}
};

void inspect(const Device& device) {
    std::println("Device: {}", device.name);
}

int main() {
    auto owner = std::make_unique<Device>("Motor-A");
    inspect(*owner); // 대여: Ownership 이동 없음

    auto next_owner = std::move(owner);
    std::println("Old owner empty: {}", owner == nullptr);
    inspect(*next_owner);
}
```

**실행 결과**

```text
Device: Motor-A
Old owner empty: true
Device: Motor-A
```

`inspect()`는 `Device`를 빌려 읽으므로 Ownership을 변경하지 않습니다. `next_owner`가 소유권을 받은 뒤 원래 `unique_ptr`는 `nullptr` 상태가 됩니다. 이는 `std::unique_ptr`에서 보장하는 Move 이후 상태입니다.

---

<a id="section-12-5"></a>

## 12.5. Custom Deleter — 외부 자원 관리


외부 라이브러리의 자원은 반드시 `delete`로 해제하는 것이 아닙니다. 예를 들어 C API의 `std::FILE*`는 `std::fclose()`로 닫아야 합니다. 이러한 해제 규칙을 사용자 정의 삭제자(Custom Deleter)에 넣을 수 있습니다.

`std::unique_ptr<T, Deleter>`는 종료 시 지정한 Deleter를 호출합니다. 다만 자원 해제 함수가 오류를 반환하는 경우, **소멸자가 그 오류를 사용자에게 전달하지는 못합니다.** 중요한 저장 작업은 명시적으로 `flush`·`close`의 성공 여부를 확인하는 별도 인터페이스가 필요할 수 있습니다.

**예제 코드 — [04_custom_deleter.cpp](./examples/04_custom_deleter.cpp)**

```cpp
#include <cstdio>
#include <memory>
#include <print>

struct FileCloser {
    void operator()(std::FILE* file) const noexcept {
        if (file != nullptr) {
            (void)std::fclose(file);
        }
    }
};

int main() {
    std::unique_ptr<std::FILE, FileCloser> file{std::tmpfile()};
    if (!file) {
        std::println(stderr, "Cannot create temporary file");
        return 1;
    }
    if (std::fputs("sample=42\n", file.get()) < 0 || std::fflush(file.get()) != 0) {
        std::println(stderr, "Write failed");
        return 1;
    }
    std::println("Temporary file written");
    // fclose 결과 검증·저장 내구성이 중요하면 별도의 명시적 처리 필요
}
```

**실행 결과**

```text
Temporary file written
```

임시 파일 생성에 실패하면 즉시 종료합니다. 쓰기 후 `std::fflush()`의 실패 여부를 확인하고, Scope 종료 시 Custom Deleter가 파일을 닫습니다. 이 예제는 파일 저장 내구성(Durability)이나 `fclose()` 실패 검증까지 보장하지는 않습니다.

---

<a id="section-12-6"></a>

## 12.6. Value Category와 이동 참조


값 범주(Value Category)는 표현식이 어떤 종류의 값을 나타내는지 구분하는 C++ 언어 규칙입니다. **타입과 Value Category는 서로 다른 개념**입니다.

| 분류 | 의미 | 예시 |
|---|---|---|
| `lvalue` | 식별 가능한 객체를 나타내는 표현식 | 이름 있는 변수 `value` |
| `prvalue` | 값을 계산하거나 결과 객체를 초기화하는 표현식 | `Device{...}`, 정수 리터럴 `42` |
| `xvalue` | 자원을 재사용할 수 있는 객체를 나타내는 표현식 | `std::move(value)` |

`T&`는 보통 lvalue를 참조하고, `T&&`는 rvalue 참조(Rvalue Reference)를 나타냅니다. **이름이 있는 `T&&` 변수 자체는 lvalue 표현식**이라는 점에 주의해야 합니다.

```cpp
#include <string>
#include <utility>

std::string text{"ABC"};  // text는 lvalue
std::string&& ref = std::move(text);
// ref라는 이름을 사용하는 표현식은 lvalue
// std::move(ref)는 xvalue 표현식
```

`std::move`는 데이터 복사를 수행하거나 실제 이동을 강제하는 함수가 아닙니다. 이어지는 Section에서 구분합니다.

---

<a id="section-12-7"></a>

## 12.7. Move Semantics와 `std::move`


이동 의미론(Move Semantics)은 자원을 복사하는 대신, 기존 객체에서 새 객체로 **자원을 이전할 수 있도록** 하는 C++ 기능입니다. `std::move`는 인수를 rvalue로 취급하도록 캐스팅하여 Move Constructor 등의 호출 가능성을 열어 줍니다.

`std::move` 자체는 메모리를 옮기지 않습니다. 대상 타입에 이동 연산이 없으면 복사가 선택될 수도 있습니다. 특히 `const` 객체는 일반적으로 이동을 통해 자원을 넘길 수 없으므로 `std::move(const_object)`를 남용하지 않습니다.

**Move 이후 상태:** 표준 라이브러리 객체는 일반적으로 유효하지만 값이 특정되지 않을 수 있습니다. `std::unique_ptr`처럼 상태가 따로 명시된 타입을 제외하면, Move 이후 내용이 비어 있다고 가정하지 않습니다.

**예제 코드 — [05_move_semantics.cpp](./examples/05_move_semantics.cpp)**

```cpp
#include <print>
#include <string>
#include <utility>

int main() {
    std::string source{"sensor-packet"};
    std::string target = std::move(source);
    std::println("Target: {}", target);
    // 이동 후 source는 유효하지만 내용은 특정하지 않음
    source = "reused";
    std::println("Source: {}", source);
}
```

**실행 결과**

```text
Target: sensor-packet
Source: reused
```

`source`는 Move 이후 다시 문자열을 대입한 뒤 사용합니다. 기존 내용이 남았는지 검사하거나 비어 있다고 가정하는 코드는 작성하지 않습니다.

---

<a id="section-12-8"></a>

## 12.8. Move-Only Type과 소유권 이전


이동 전용 타입(Move-Only Type)은 복사는 허용하지 않고 Move만 허용하는 타입입니다. 예를 들어 `std::unique_ptr`는 Exclusive Ownership을 나타내므로 복사 생성자가 삭제되어 있습니다.

Move-Only Type을 Container에 보관하려면 `emplace_back()`으로 직접 구성하거나 `std::move()`를 이용해 이전해야 합니다. 매개변수로 단일 소유권을 받는 함수에서도 Move를 사용합니다.

**예제 코드 — [06_move_only.cpp](./examples/06_move_only.cpp)**

```cpp
#include <memory>
#include <print>
#include <utility>
#include <vector>

struct Job {
    explicit Job(int value) : id(std::make_unique<int>(value)) {}
    std::unique_ptr<int> id;
};

int main() {
    std::vector<Job> jobs;
    jobs.emplace_back(10);
    Job task{20};
    jobs.push_back(std::move(task));
    std::println("Jobs: {} / {}", *jobs[0].id, *jobs[1].id);
}
```

**실행 결과**

```text
Jobs: 10 / 20
```

`jobs.push_back(std::move(task))`에서 `task`의 Ownership이 Container의 요소로 이전됩니다. 새 작업을 만들 때는 `emplace_back()`이 불필요한 임시 객체 생성을 줄일 수 있지만, 항상 더 빠르다고 가정해서는 안 됩니다.

---

<a id="section-12-9"></a>

## 12.9. Copy/Move Constructor와 Special Member Function


클래스의 복사 생성자(Copy Constructor), 이동 생성자(Move Constructor), 대입 연산자, 소멸자(Destructor)는 객체 수명과 자원 관리에 직접 관여합니다. 이를 특수 멤버 함수(Special Member Function)라고 합니다.

| 동작 | 대표 선언 | 사용 상황 |
|---|---|---|
| 복사 생성 | `T(const T&)` | 다른 객체에서 새 객체 생성 |
| 복사 대입 | `T& operator=(const T&)` | 기존 객체에 복사 |
| 이동 생성 | `T(T&&)` | rvalue에서 새 객체 생성 |
| 이동 대입 | `T& operator=(T&&)` | 기존 객체에 자원 이전 |
| 소멸 | `~T()` | 객체 종료 시 정리 |

`= default`는 컴파일러가 제공할 수 있는 기본 구현을 요청하며, `= delete`는 해당 연산을 금지합니다. 다른 Special Member Function을 직접 선언하면 암시적 Move 생성 여부 등이 달라질 수 있으므로, **기본 생성 규칙을 고려하지 않은 소멸자 선언**은 주의가 필요합니다.

**예제 코드 — [07_copy_move_tracing.cpp](./examples/07_copy_move_tracing.cpp)**

```cpp
#include <print>
#include <utility>

struct Probe {
    Probe() = default;
    Probe(const Probe&) { std::println("Copy"); }
    Probe(Probe&&) noexcept { std::println("Move"); }
};

int main() {
    Probe source;
    Probe copied{source};
    Probe moved{std::move(source)};
    (void)copied;
    (void)moved;
}
```

**실행 결과**

```text
Copy
Move
```

출력되는 `Copy`와 `Move`는 명시적으로 각 생성자를 선택한 결과입니다. **모든 C++ 객체 생성마다 복사·이동이 반드시 일어나는 것은 아닙니다.** Copy Elision은 12.13에서 다룹니다.

---

<a id="section-12-10"></a>

## 12.10. Rule of Zero — 자동 자원 관리


제로 규칙(Rule of Zero)은 클래스가 자원 관리 자체를 담당하지 않는다면 복사·이동·소멸자를 직접 구현하지 않는 설계 원칙입니다. `std::string`, `std::vector`, `std::unique_ptr`처럼 이미 자원을 관리하는 멤버를 사용하면 다수의 클래스가 이 규칙을 따를 수 있습니다.

```text
비즈니스 데이터와 로직을 가진 클래스 → 표준 Container·Smart Pointer 활용 → Special Member Function의 자동 생성 활용
```

멤버의 복사 가능 여부에 따라 바깥 클래스의 복사 가능 여부도 결정됩니다. 예를 들어 `std::unique_ptr` 멤버를 가진 클래스는 특별한 구현이 없으면 복사할 수 없습니다.

**예제 코드 — [08_rule_of_zero.cpp](./examples/08_rule_of_zero.cpp)**

```cpp
#include <print>
#include <string>
#include <utility>
#include <vector>

struct SensorBatch {
    std::string source;
    std::vector<int> readings;
};

int main() {
    SensorBatch first{"sensor-A", {12, 15, 14}};
    SensorBatch copied = first;
    SensorBatch moved = std::move(first);
    std::println("Copy samples: {}", copied.readings.size());
    std::println("Move samples: {}", moved.readings.size());
}
```

**실행 결과**

```text
Copy samples: 3
Move samples: 3
```

`SensorBatch`는 소멸자나 Copy/Move Constructor를 정의하지 않았습니다. 두 멤버가 자원을 직접 관리하므로 간결하게 설계할 수 있습니다.

---

<a id="section-12-11"></a>

## 12.11. Rule of Five — 직접 관리해야 하는 경우


파이브 규칙(Rule of Five)은 자원 소유 클래스를 직접 구현해야 할 때 **소멸·복사·이동의 계약을 함께 검토**해야 한다는 원칙입니다. 직접 작성이 필요한 특별한 API를 제외하면 Rule of Zero를 우선 고려합니다.

다음 예제에서는 단순한 배열 Buffer를 예시로 복사 시 Deep Copy를 수행하고, Move 시 자원을 이전합니다. 별도 메모리 관리 코드를 학습하기 위한 예제이며, 실제 데이터 저장에는 `std::vector` 등이 일반적으로 더 적합합니다.

- **Deep Copy:** 소유 데이터의 새로운 저장 공간 확보
- **Copy-and-Swap:** 먼저 복사본 구성 후 `swap`으로 교체하여 예외 시 기존 객체 보호
- **Move Constructor:** 기존 자원을 새 객체에 이전
- **Self-assignment:** 자기 자신에 대한 대입 방어

**예제 코드 — [09_rule_of_five.cpp](./examples/09_rule_of_five.cpp)**

```cpp
#include <algorithm>
#include <cstddef>
#include <memory>
#include <print>
#include <stdexcept>
#include <utility>

class IntBuffer {
public:
    explicit IntBuffer(std::size_t size)
        : data_(size ? std::make_unique<int[]>(size) : nullptr), size_(size) {}

    ~IntBuffer() = default;

    IntBuffer(const IntBuffer& other) : IntBuffer(other.size_) {
        if (size_ != 0) std::copy_n(other.data_.get(), size_, data_.get());
    }
    IntBuffer& operator=(const IntBuffer& other) {
        if (this != &other) {
            IntBuffer copy{other};
            swap(copy);
        }
        return *this;
    }
    IntBuffer(IntBuffer&& other) noexcept
        : data_(std::move(other.data_)), size_(std::exchange(other.size_, 0)) {}
    IntBuffer& operator=(IntBuffer&& other) noexcept {
        if (this != &other) {
            data_ = std::move(other.data_);
            size_ = std::exchange(other.size_, 0);
        }
        return *this;
    }
    void swap(IntBuffer& other) noexcept {
        data_.swap(other.data_);
        std::swap(size_, other.size_);
    }
    [[nodiscard]] std::size_t size() const noexcept { return size_; }
    [[nodiscard]] int& at(std::size_t index) {
        if (index >= size_) throw std::out_of_range("invalid index");
        return data_[index];
    }
private:
    std::unique_ptr<int[]> data_;
    std::size_t size_{};
};

int main() {
    IntBuffer first{2};
    first.at(0) = 7;
    first.at(1) = 9;
    IntBuffer copy{first};
    copy.at(0) = 50;
    IntBuffer moved{std::move(first)};
    std::println("Copy: {}, Moved: {}, Old size: {}",
                 copy.at(0), moved.at(0), first.size());
}
```

**실행 결과**

```text
Copy: 50, Moved: 7, Old size: 0
```

이 예제는 내부 버퍼를 `std::unique_ptr<int[]>`로 보관하되, 값 타입으로 복사할 수 있도록 복사 기능을 직접 정의합니다. `at()`은 잘못된 인덱스에 `std::out_of_range` 예외를 발생시킵니다. `size_`가 `0`일 때는 배열을 사용하지 않습니다.

---

<a id="section-12-12"></a>

## 12.12. `std::exchange`와 이동 후 상태


`std::exchange(object, new_value)`는 이전 값을 반환하고 대상에 새로운 값을 대입합니다. Move Constructor에서 원래 객체를 **문서화된 유효 상태**로 돌려놓을 때 유용합니다.

Resource Handle을 `-1`과 같은 무효 값으로 관리하면 두 객체가 같은 Handle을 소유하는 상황을 방지할 수 있습니다. 단, 실제 파일이나 Socket Handle의 특수한 무효 값은 해당 플랫폼 API에 따라 결정해야 합니다.

**예제 코드 — [10_exchange_state.cpp](./examples/10_exchange_state.cpp)**

```cpp
#include <print>
#include <utility>

class Handle {
public:
    explicit Handle(int id) noexcept : id_(id) {}
    Handle(const Handle&) = delete;
    Handle& operator=(const Handle&) = delete;
    Handle(Handle&& other) noexcept : id_(std::exchange(other.id_, -1)) {}
    Handle& operator=(Handle&& other) noexcept {
        if (this != &other) id_ = std::exchange(other.id_, -1);
        return *this;
    }
    [[nodiscard]] int id() const noexcept { return id_; }
private:
    int id_{-1};
};

int main() {
    Handle first{42};
    Handle second{std::move(first)};
    std::println("New: {}, Old: {}", second.id(), first.id());
}
```

**실행 결과**

```text
New: 42, Old: -1
```

이 예제의 `Handle`은 실제 OS 자원을 소유하지 않는 상태 모델입니다. 실제 자원 소유 타입에서는 소멸자가 반환 책임을 수행하도록 만들어야 합니다.

---

<a id="section-12-13"></a>

## 12.13. Copy Elision과 NRVO


복사 생략(Copy Elision)은 객체의 불필요한 중간 복사·이동을 생략하거나, C++17 이후 특정 경우에 **최종 목적지에 직접 객체를 구성**하는 언어 규칙입니다.

- **Guaranteed Copy Elision:** 같은 타입의 prvalue를 반환하는 경우 등에서 직접 구성. C++17부터 보장되는 경우 존재
- **이름 있는 반환값 최적화(Named Return Value Optimization, NRVO):** 지역 변수 이름을 반환하는 경우 컴파일러가 생략할 수 있는 최적화. 항상 보장되지는 않음
- **주의:** 반환문에 습관적으로 `std::move(local)`을 붙이면 NRVO 적용 기회를 방해할 수 있음

```cpp
T make_direct() { return T{}; } // 보장되는 직접 구성 조건
T make_named() { T value; return value; } // NRVO 후보
```

**예제 코드 — [11_copy_elision.cpp](./examples/11_copy_elision.cpp)**

```cpp
#include <print>

class Token {
public:
    explicit Token(int id) : id_(id) {}
    Token(const Token&) = delete;
    Token(Token&&) = delete;
    [[nodiscard]] int id() const noexcept { return id_; }
private:
    int id_;
};

[[nodiscard]] Token make_token(int id) {
    return Token{id}; // 같은 타입의 prvalue: C++17부터 직접 구성
}

int main() {
    Token value = make_token(27);
    std::println("Token: {}", value.id());
}
```

**실행 결과**

```text
Token: 27
```

`Token`은 복사와 이동 생성자가 모두 삭제되어 있지만 예제의 반환 방식은 C++17 이후의 직접 구성이 가능하므로 정상 컴파일됩니다. 이 동작을 일반적인 `return local;` 모든 경우에 그대로 적용해서는 안 됩니다.

---

<a id="section-12-14"></a>

## 12.14. `noexcept`와 `std::move_if_noexcept`


`noexcept`는 함수가 예외를 외부로 전파하지 않는다는 계약을 나타냅니다. 처리하지 못한 예외가 `noexcept` 함수 밖으로 나가면 `std::terminate()`가 호출됩니다. 따라서 단순한 속도 최적화 목적으로 붙이지 않습니다.

`std::move_if_noexcept`는 Move Constructor가 `noexcept`이거나 복사할 수 없는 타입이면 rvalue 참조를 반환하고, 그렇지 않으면 `const` lvalue 참조를 반환해 복사가 선택될 수 있도록 합니다. `std::vector`의 재할당 시 예외 보장과 관련된 기능입니다.

| 타입의 조건 | `std::move_if_noexcept`의 선택 |
|---|---|
| Move가 `noexcept` | Move가 가능한 rvalue 참조 |
| 복사 불가 | 예외 가능성이 있어도 rvalue 참조 |
| 복사 가능 + Move에서 예외 가능 | Copy가 가능한 `const` lvalue 참조 |

**예제 코드 — [12_move_if_noexcept.cpp](./examples/12_move_if_noexcept.cpp)**

```cpp
#include <print>
#include <utility>

struct MightThrow {
    MightThrow() = default;
    MightThrow(const MightThrow&) { std::println("Copy selected"); }
    MightThrow(MightThrow&&) noexcept(false) { std::println("Move selected"); }
};
struct SafeMove {
    SafeMove() = default;
    SafeMove(const SafeMove&) { std::println("Copy selected"); }
    SafeMove(SafeMove&&) noexcept { std::println("Move selected"); }
};

int main() {
    MightThrow a;
    SafeMove b;
    [[maybe_unused]] MightThrow a2{std::move_if_noexcept(a)};
    [[maybe_unused]] SafeMove b2{std::move_if_noexcept(b)};
}
```

**실행 결과**

```text
Copy selected
Move selected
```

첫 번째 객체에서는 복사가 선택되고, 두 번째 객체에서는 Move가 선택됩니다. Copy와 Move가 모두 예외를 던질 수 있다는 상황에서도 모든 Container 연산이 동일한 예외 보장을 제공하는 것은 아닙니다.

---

<a id="section-12-15"></a>

## 12.15. Exception Safety — 상태 변경의 원자성


예외 안전성(Exception Safety)은 실패하거나 예외가 발생한 뒤 **프로그램 상태가 어떤 조건을 유지하는지** 설명하는 계약입니다.

| 보장 | 의미 |
|---|---|
| 기본 보장(Basic Guarantee) | 객체가 유효한 상태를 유지하며 자원 누수 없음. 기존 값은 바뀔 수 있음 |
| 강한 보장(Strong Guarantee) | 실패 시 관찰 가능한 상태가 기존과 동일하게 유지됨 |
| 예외 없음 보장(No-Throw Guarantee) | 해당 연산이 예외를 외부로 던지지 않음 |

**Transactional Update:** 새로운 데이터를 임시 객체에 구성 → 전체 검증 → 최종 `swap`으로 교체. 이러한 방식은 기존 상태를 중간에 부분 수정하는 오류를 줄일 수 있습니다. 단, 교체 대상 외부에 이미 부수 효과가 생겼다면 전체 시스템에 대한 Strong Guarantee가 성립한다고 단정할 수 없습니다.

**예제 코드 — [13_exception_safety.cpp](./examples/13_exception_safety.cpp)**

```cpp
#include <algorithm>
#include <print>
#include <span>
#include <stdexcept>
#include <vector>
#include <utility>

class Readings {
public:
    explicit Readings(std::vector<int> values) : values_(std::move(values)) {}
    void replace(std::span<const int> values) {
        std::vector<int> staged{values.begin(), values.end()};
        if (std::ranges::any_of(staged, [](int x) { return x < 0; })) {
            throw std::invalid_argument("negative reading");
        }
        values_.swap(staged); // 검증이 끝난 뒤 한번에 교체
    }
    [[nodiscard]] int first() const { return values_.at(0); }
private:
    std::vector<int> values_;
};

int main() {
    Readings batch{{10, 20}};
    try {
        const int invalid[] = {3, -4};
        batch.replace(invalid);
    } catch (const std::invalid_argument&) {
        std::println("Rejected");
    }
    std::println("First unchanged: {}", batch.first());
}
```

**실행 결과**

```text
Rejected
First unchanged: 10
```

유효하지 않은 값 `-4`로 교체를 시도해도 `Readings`의 기존 데이터 `10, 20`은 유지됩니다. 먼저 임시 `std::vector`를 완성한 뒤 교체하기 때문입니다.

---

<a id="section-12-16"></a>

## 12.16. Borrowed View와 Dangling Reference


빌려온 뷰(Borrowed View)는 원본 데이터를 소유하지 않고 읽거나 변경할 수 있는 범위를 나타냅니다. `std::string_view`, `std::span`, `T&`는 원본 객체의 Lifetime을 넘겨 저장하면 안 됩니다.

댕글링 참조(Dangling Reference)는 이미 Lifetime이 끝난 객체를 참조하는 상태입니다. 해당 참조를 잘못 사용하면 미정의 동작(Undefined Behavior, UB)이 발생할 수 있습니다.

```cpp
// 잘못된 코드: 지역 문자열 소멸 후 View가 남음
// std::string_view bad() {
//     std::string local{"temporary"};
//     return local;
// }
```

호출자가 원본 데이터를 오래 유지할 수 없다면 `std::string`처럼 자체 데이터를 소유하는 반환값을 선택합니다. Raw Pointer·View는 사용 편의성보다 **원본 Lifetime과 Invalidation 규칙**을 우선 확인해야 합니다.

**예제 코드 — [14_borrowed_view.cpp](./examples/14_borrowed_view.cpp)**

```cpp
#include <print>
#include <string>
#include <string_view>

[[nodiscard]] std::string_view first_word(std::string_view input) {
    const auto pos = input.find(' ');
    return input.substr(0, pos);
}

int main() {
    const std::string message{"sensor ready"};
    const std::string_view borrowed = first_word(message);
    std::println("Borrowed: {}", borrowed);
    const std::string owned{borrowed}; // 별도 수명이 필요하면 복사하여 소유
    std::println("Owned: {}", owned);
}
```

**실행 결과**

```text
Borrowed: sensor
Owned: sensor
```

`first_word()`는 전달받은 문자열의 일부를 가리키는 View를 반환합니다. 호출자가 원본을 유지하는 동안에만 사용해야 하며, 독립적인 보관이 필요하면 `std::string`으로 복사합니다.

---

<a id="section-12-17"></a>

## 12.17. `std::expected`로 전달하는 소유권과 오류


Factory Function은 유효한 객체를 구성하거나 실패 이유를 반환할 때 유용합니다. C++23의 `std::expected<T, E>`는 성공값과 오류를 명확히 구분할 수 있습니다.

```cpp
std::expected<std::unique_ptr<Device>, std::string>
```

이 반환형은 성공 시 `Device`의 Exclusive Ownership을 돌려주고, 실패 시 오류 문자열을 전달합니다. `std::expected` 자체는 동적 메모리 할당 실패 등의 모든 예외를 자동으로 오류 값으로 변환하지는 않습니다.

**예제 코드 — [15_expected_factory.cpp](./examples/15_expected_factory.cpp)**

```cpp
#include <expected>
#include <memory>
#include <print>
#include <string>
#include <string_view>
#include <utility>

struct Device {
    std::string id;
    explicit Device(std::string value) : id(std::move(value)) {}
};

[[nodiscard]] std::expected<std::unique_ptr<Device>, std::string>
connect(std::string_view id) {
    if (id.empty()) return std::unexpected("empty id");
    return std::make_unique<Device>(std::string{id});
}

int main() {
    auto result = connect("camera-A");
    if (result) std::println("Connected: {}", (*result)->id);
    auto failed = connect("");
    if (!failed) std::println("Rejected: {}", failed.error());
}
```

**실행 결과**

```text
Connected: camera-A
Rejected: empty id
```

`std::unexpected(...)`는 실패 결과를 만들고, `*result`는 성공값인 `std::unique_ptr<Device>`에 접근합니다. 성공 확인 없이 값을 꺼내지 않도록 합니다.

---

<a id="section-12-18"></a>

## 12.18. Perfect Forwarding — 다음 Chapter 연결


완벽 전달(Perfect Forwarding)은 템플릿으로 받은 인수의 Value Category를 유지하며 다른 함수에 전달하는 기법입니다. `std::forward<T>`와 전달 참조(Forwarding Reference)를 사용합니다.

이 Chapter에서는 사용 형태만 확인합니다. 템플릿 매개변수 추론, Reference Collapsing, Constraints 및 Generic Programming의 세부 원리는 **Chapter 13**에서 다룹니다.

**예제 코드 — [16_perfect_forwarding_preview.cpp](./examples/16_perfect_forwarding_preview.cpp)**

```cpp
#include <memory>
#include <print>
#include <string>
#include <utility>

struct Device {
    explicit Device(std::string name) : name(std::move(name)) {}
    std::string name;
};

template <typename T, typename... Args>
[[nodiscard]] std::unique_ptr<T> create_owned(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}

int main() {
    std::string name{"camera-A"};
    const auto device = create_owned<Device>(name);
    std::println("Created: {}", device->name);
}
```

**실행 결과**

```text
Created: camera-A
```

`std::forward<Args>(args)...`는 호출자가 전달한 인수의 속성을 유지하려는 의도를 표현합니다. 직접 템플릿 Factory를 작성할 필요가 없다면 `std::make_unique`를 바로 사용하는 편이 간결합니다.

---

<a id="section-12-19"></a>

## 12.19. Mini Project — Device Session Manager


센서 연결을 관리하는 간단한 시뮬레이션입니다. 실제 하드웨어와 연결하지 않으며, 외부 C API가 반환하는 Raw Pointer를 RAII 객체가 관리하는 구조를 학습합니다.

```text
examples/17_device_session/
├── CMakeLists.txt
├── session.hpp
├── session.cpp
└── main.cpp
```

| 구성 요소 | 역할 |
|---|---|
| `RawPort` | 외부 장치 Handle을 흉내 낸 객체 |
| `close_port()` | RawPort의 해제 함수 |
| `Session::Closer` | Custom Deleter로 해제 규칙 전달 |
| `Session` | 복사 금지, 이동 허용하는 Exclusive Owner |
| `Session::open()` | `std::expected` 기반 Factory |
| `main.cpp` | 연결·측정·자동 정리 시나리오 |

**컴파일 및 실행** — `Chapter-12/` 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic \
  examples/17_device_session/main.cpp \
  examples/17_device_session/session.cpp -o device_session
./device_session
```

**CMake**

```bash
cmake -S examples/17_device_session -B build/ch12-device-session
cmake --build build/ch12-device-session
./build/ch12-device-session/device_session
```

**실행 결과**

```text
Connected: sensor-A
Samples: 21, 24, 22
Closed sessions: 1
Rejected: device id is empty
```

`Session`의 Scope가 끝나면 Custom Deleter가 호출되어 Handle이 반환됩니다. `Session::open("")`는 생성하지 않고 오류를 반환합니다. `next_reading()`은 이동 후 비어 있는 객체에서 호출하면 예외를 던지도록 구현했습니다.

> 이 예제의 `open_port()`는 외부 API를 모사하기 위해 직접 `new`를 사용합니다. 일반적인 동적 객체 생성은 `std::make_unique` 등을 우선 사용합니다.

---

<a id="section-12-20"></a>

## 12.20. 설계 시 참고 사항


다음 항목을 확인하면 Ownership과 수명 관리 실수를 줄일 수 있습니다.

| 질문 | 확인 사항 |
|---|---|
| 누가 자원을 해제하나요? | Ownership을 특정 객체로 한정할 수 있는지 |
| Copy가 필요한가요? | 값 복사가 의미 있는지, Move-Only Type이 적절한지 |
| Move 후 상태는 무엇인가요? | 타입이 보장하는 상태만 사용하고 있는지 |
| 반환 형식은 명확한가요? | 값·Borrowing·Exclusive Ownership을 구분하는지 |
| 실패하면 이전 상태가 보존되나요? | 필요한 Exception Guarantee가 무엇인지 |
| Custom Deleter가 필요한가요? | 외부 API의 해제 함수와 매칭되는지 |
| Container에서 이동하나요? | `noexcept` 및 Reallocation의 영향을 이해하는지 |
| View가 안전한가요? | 원본 Lifetime과 Invalidation 여부를 확인했는지 |

**피해야 할 패턴**

```cpp
// new로 만든 자원을 모든 반환 경로에서 수동으로 delete
// Copy와 Move를 고려하지 않고 소유 Raw Pointer를 얕게 복사
// std::move 이후 표준 컨테이너가 반드시 비어 있다고 가정
// 원본 지역 변수보다 오래 살아 있는 string_view 반환
// 모든 함수에 근거 없이 noexcept 선언
```

Chapter 12는 자원의 소유 방식과 수명 계약에 집중합니다. Memory Allocation 및 성능 측정은 Chapter 15, 빌드 환경은 Chapter 16, 테스트·프로파일링은 Chapter 17에서 확장합니다.

---

<a id="section-12-21"></a>

## 12.21. Coding Practice


연습문제는 `exercises/`에서 미완성 코드를 수정하고, 구현한 프로그램의 출력 결과를 확인하는 방식으로 진행합니다. 모범답안은 `solutions/`에 별도 보관되어 있습니다.

### 실습 ① — Transactional Sensor Update

**파일:** [exercises/01_transactional_update.cpp](./exercises/01_transactional_update.cpp) · [모범답안](./solutions/01_transactional_update.cpp)

기존 센서 데이터 `{10, 20}`을 새로운 입력으로 교체하는 `replace()` 함수를 완성합니다.

- 입력값 범위: `0~100`
- 유효하지 않은 입력은 `std::invalid_argument`로 거부
- 실패한 경우 기존 데이터 유지
- 정상 입력 `{60, 80}`으로 교체되는지 확인

**모범답안 실행 결과**

```text
Rejected
First: 10
Updated: 60
```

### 실습 ② — Unique Ownership Transfer

**파일:** [exercises/02_unique_owner.cpp](./exercises/02_unique_owner.cpp) · [모범답안](./solutions/02_unique_owner.cpp)

`std::unique_ptr<Camera>`의 Ownership을 다른 변수에 이전합니다.

- `std::move()`를 이용한 이전
- 원래 소유자가 `nullptr`인지 확인
- 새로운 소유자로 Camera ID 출력

**모범답안 실행 결과**

```text
Source exists: false
Camera: cam-01
```

### 실습 ③ — Move-Only Packet

**파일:** [exercises/03_move_only_packet.cpp](./exercises/03_move_only_packet.cpp) · [모범답안](./solutions/03_move_only_packet.cpp)

`Packet`을 Move-Only Type으로 변경하고 전달 후 재사용을 구현합니다.

- 복사 생성·대입 금지
- Move Constructor·Move Assignment 허용
- 데이터를 Move한 뒤 새 값 대입으로 원본 재사용

**모범답안 실행 결과**

```text
Delivered bytes: 4
Reused bytes: 1
```

### 실습 ④ — Device Factory

**파일:** [exercises/04_device_factory.cpp](./exercises/04_device_factory.cpp) · [모범답안](./solutions/04_device_factory.cpp)

`std::expected<std::unique_ptr<Device>, std::string>`을 반환하는 Factory를 완성합니다.

- 장치 이름은 빈 문자열이 아니어야 함
- 측정 주기는 `1~1000ms`
- 정상 입력은 Exclusive Ownership으로 반환
- 실패 시 원인별 오류 메시지 반환

**모범답안 실행 결과**

```text
Device: lidar (50 ms)
Error: empty device name
```

### 컴파일 및 실행

**GCC** — `Chapter-12/` 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic \
  solutions/01_transactional_update.cpp -o transactional_update
./transactional_update
```

**Clang** — 지원되는 C++23 표준 라이브러리 환경

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic \
  solutions/01_transactional_update.cpp -o transactional_update
./transactional_update
```

**MSVC** — Developer Command Prompt

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 solutions\01_transactional_update.cpp /Fe:transactional_update.exe
transactional_update.exe
```

MSVC는 설치 버전에 따라 `/std:c++23` 또는 `/std:c++23preview` 지원 여부를 확인해야 합니다. C++23 언어 모드와 개별 표준 라이브러리 기능의 지원 수준은 다를 수 있습니다.

---

<a id="section-12-22"></a>

## 12.22. Quiz & Summary


### Quiz

**1.** RAII를 사용하는 가장 중요한 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

자원 해제를 객체 Lifetime에 연결하여 정상 반환과 예외 발생 경로에서 누락 없이 정리하기 위함.

</details>

**2.** `std::move(object)`를 호출하는 순간 실제로 자원이 반드시 이동하나요?

<details>
<summary>정답 확인</summary>

아니요. `std::move`는 rvalue로 취급하도록 캐스팅하며 실제 Move 또는 Copy 여부는 타입과 이후 연산에 따라 결정됨.

</details>

**3.** `std::unique_ptr<T>`를 다른 소유자에게 전달할 때 주로 사용하는 연산은 무엇인가요?

<details>
<summary>정답 확인</summary>

`std::move(owner)`를 이용한 Move Constructor 또는 Move Assignment.

</details>

**4.** Rule of Zero가 권장하는 클래스 설계 방식은 무엇인가요?

<details>
<summary>정답 확인</summary>

표준 Container와 RAII 타입에 자원 관리를 맡기고 특별한 이유가 없으면 Special Member Function을 직접 구현하지 않는 방식.

</details>

**5.** `return T{};`와 `return local;`의 Copy Elision 보장은 동일한가요?

<details>
<summary>정답 확인</summary>

아니요. 특정한 `return T{};` 형태는 C++17 이후 직접 구성이 보장되지만, 이름 있는 지역 변수를 반환할 때의 NRVO는 허용되더라도 일반적으로 보장되지 않음.

</details>

**6.** `std::move_if_noexcept`가 Copy를 선택할 수 있는 조건은 무엇인가요?

<details>
<summary>정답 확인</summary>

Copy가 가능하고 Move Constructor가 `noexcept`가 아닐 때 Copy가 가능한 참조를 반환함.

</details>

**7.** Strong Guarantee는 실패 시 어떤 상태를 보장하나요?

<details>
<summary>정답 확인</summary>

실패 전과 동일한 관찰 가능한 상태를 유지함. 필요한 Resource를 임시로 준비한 후 안전하게 교체하는 방식 등이 활용됨.

</details>

**8.** 지역 `std::string`에서 얻은 `std::string_view`를 함수 밖으로 반환하면 어떤 문제가 생길 수 있나요?

<details>
<summary>정답 확인</summary>

원본 문자열이 소멸하여 Dangling View가 될 수 있음. 그 View를 잘못 접근하면 UB가 발생할 수 있음.

</details>

### Summary

- **Lifetime:** 자원과 객체가 유효하게 존재하는 기간
- **Ownership:** 자원 반환 책임의 명확한 표현
- **RAII:** 객체의 소멸과 자원 정리를 연결
- **`std::unique_ptr`:** Exclusive Ownership을 갖는 Smart Pointer
- **Move Semantics:** 자원을 복사하는 대신 이전할 수 있도록 하는 기능
- **Rule of Zero:** 기본 자원 관리 타입을 활용하고 불필요한 특수 멤버 구현 방지
- **Rule of Five:** 직접 자원을 관리할 때 Copy·Move·Destructor의 계약 함께 검토
- **Copy Elision:** 특정 상황에서 불필요한 객체 구성·Copy/Move 제거
- **`std::move_if_noexcept`:** Exception Guarantee를 고려한 Copy/Move 선택
- **Exception Safety:** 실패 후 상태 보존 수준의 명시
- **Borrowed View:** 원본 Lifetime과 Invalidation에 의존하는 비소유 참조

### References

- [cppreference — RAII](https://en.cppreference.com/w/cpp/language/raii)
- [cppreference — Move Constructor](https://en.cppreference.com/w/cpp/language/move_constructor)
- [cppreference — `std::move`](https://en.cppreference.com/w/cpp/utility/move)
- [cppreference — `std::move_if_noexcept`](https://en.cppreference.com/w/cpp/utility/move_if_noexcept)
- [cppreference — Copy Elision](https://en.cppreference.com/w/cpp/language/copy_elision)
- [cppreference — `std::unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [cppreference — `std::expected`](https://en.cppreference.com/w/cpp/utility/expected)
- [C++ Core Guidelines — Resource Management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource)

---

[← C++ 목차](../README.md) · [Chapter 11 — File I/O](../Chapter-11/)
