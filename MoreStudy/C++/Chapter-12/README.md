# Chapter 12. Modern C++ & Resource Management

객체의 수명과 자원의 소유권을 연결하여, 정상 종료와 오류 발생 상황 모두에서 자원을 안전하게 관리하는 방법을 학습합니다. Chapter 07의 포인터·참조, Chapter 08의 클래스, Chapter 09의 다형성, Chapter 11의 파일 입출력을 바탕으로 소유권 이전과 복사·이동 설계까지 확장합니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서 도입된 유용한 문법도 사용합니다. C++23의 `std::expected`는 마지막 부분에서 비교하되 기본 예제와 프로젝트에서는 사용하지 않습니다.

<details>
<summary>선행 학습</summary>

- [Chapter 05. Functions](../Chapter-05/) — 함수 계약, 값·참조 매개변수, `std::optional`
- [Chapter 07. Pointers & References](../Chapter-07/) — 주소, 객체 수명, 스마트 포인터의 기초
- [Chapter 08. Structs & Classes](../Chapter-08/) — 생성자·소멸자, 합성, Rule of Zero의 기초
- [Chapter 09. Object-Oriented Programming](../Chapter-09/) — 다형성과 소유권을 가진 객체 집합
- [Chapter 11. File I/O](../Chapter-11/) — 파일 스트림의 RAII와 오류 처리

</details>

## Contents

| Section | Topic |
|:---:|---|
| [12.1](#section-12-1) | Object Lifetime — 객체 수명과 스코프 |
| [12.2](#section-12-2) | RAII — 객체 수명으로 자원 관리 |
| [12.3](#section-12-3) | Ownership & Borrowing — 소유권과 대여 |
| [12.4](#section-12-4) | Unique Ownership — `std::unique_ptr` |
| [12.5](#section-12-5) | Custom Deleter — 외부 자원 해제 |
| [12.6](#section-12-6) | Shared & Weak Ownership — 공유 소유와 관찰 |
| [12.7](#section-12-7) | Value Categories — 값 범주와 rvalue 참조 |
| [12.8](#section-12-8) | Move Semantics — 이동과 이동 전용 타입 |
| [12.9](#section-12-9) | Special Member Functions — 복사·이동 생성자와 대입 |
| [12.10](#section-12-10) | Rule of Zero — 특별 멤버 함수가 필요 없는 설계 |
| [12.11](#section-12-11) | Rule of Three & Five — 직접 자원을 관리하는 클래스 |
| [12.12](#section-12-12) | `std::exchange` & Moved-from State — 이동 후 상태 |
| [12.13](#section-12-13) | Copy Elision & NRVO — 불필요한 복사·이동 생략 |
| [12.14](#section-12-14) | `noexcept` & `std::move_if_noexcept` — 이동과 예외 |
| [12.15](#section-12-15) | Exception Safety — 실패에도 상태 유지 |
| [12.16](#section-12-16) | Non-owning Views — 수명과 무효화 |
| [12.17](#section-12-17) | Error Handling — C++20 결과 표현 |
| [12.18](#section-12-18) | Coding Practice — 연습문제 |
| [12.19](#section-12-19) | Mini Project — Device Session Manager |
| [12.20](#section-12-20) | Quiz & Summary — 최종 점검 |

## Getting Started

다음 명령어는 `MoreStudy/C++/Chapter-12/` 폴더에서 실행합니다. `examples/` 아래의 단일 `.cpp` 파일은 각각 독립적으로 컴파일할 수 있습니다.

**GCC — Git Bash**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/03_unique_ownership.cpp -o unique_ownership
./unique_ownership
```

GCC 14가 설치되어 있고 실행 파일 이름이 `g++-14`라면 `g++` 대신 `g++-14`를 사용해도 됩니다. 아래의 모든 예제는 GCC 14에서 별도로 검증했습니다.

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/03_unique_ownership.cpp -o unique_ownership
./unique_ownership
```

**MSVC — Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /utf-8 examples\03_unique_ownership.cpp /Fe:unique_ownership.exe
unique_ownership.exe
```

Windows PowerShell에서는 `./unique_ownership` 대신 `.\unique_ownership.exe` 형태로 실행 파일을 호출할 수 있습니다. 빌드 명령어는 VS Code의 실행 버튼 대신 사용할 수도 있으며, 실제로 어떤 C++ 표준을 사용했는지 확인하는 데 유용합니다.

**학습 목표**

1. 객체 수명과 자원 수명 사이의 관계를 구분합니다.
2. RAII와 스마트 포인터로 자원 반환 책임을 표현합니다.
3. 복사와 이동의 차이를 설명하고 필요한 상황에 `std::move()`를 사용할 수 있습니다.
4. Rule of Zero를 기본 설계로 삼고 직접 복사·이동을 구현해야 하는 경우를 구분합니다.
5. 예외나 실패가 일어나더라도 프로그램 상태를 복구 가능한 형태로 유지합니다.

<a id="section-12-1"></a>

## 12.1. Object Lifetime — 객체 수명과 스코프

**객체 수명(Object Lifetime)**은 어떤 객체가 존재하며 유효하게 사용될 수 있는 기간을 의미합니다. 이름을 코드에서 찾을 수 있는 범위인 **스코프(Scope)** 와 관련이 있지만 동일한 뜻은 아닙니다. 포인터를 변수 밖으로 전달했다고 해서 가리키는 객체의 수명까지 연장되는 것은 아닙니다.

| 구분 | 의미 | 예시 |
|---|---|---|
| Scope | 식별자를 참조할 수 있는 코드의 범위 | `{}` 블록 안의 변수 이름 |
| Object Lifetime | 객체가 유효하게 존재하는 기간 | 지역 객체의 생성부터 소멸까지 |
| Resource Lifetime | 파일·메모리·장치 같은 자원이 확보된 기간 | 파일 열기부터 닫기까지 |

지역 객체는 일반적으로 선언된 블록을 벗어날 때 소멸하며, 같은 블록의 객체는 생성 순서의 역순으로 정리됩니다. 생성자(Constructor)에서 수행한 작업과 소멸자(Destructor)에서 수행한 작업의 순서를 출력해 확인해 봅니다.

`<iostream>`의 `std::cout`은 콘솔 출력에, `<string_view>`의 `std::string_view`는 문자열을 복사하지 않고 읽는 데 사용합니다. 이 예제에서는 `Trace`가 프로그램 종료까지 살아 있는 문자열 리터럴만 참조합니다.


**예제 코드 — [01_scope_lifetime.cpp](./examples/01_scope_lifetime.cpp)**

```cpp
#include <iostream>
#include <string_view>

class Trace {
public:
    explicit Trace(std::string_view name) : name_(name) {
        std::cout << "Open: " << name_ << '\n';
    }
    ~Trace() { std::cout << "Close: " << name_ << '\n'; }
    Trace(const Trace&) = delete;
    Trace& operator=(const Trace&) = delete;
private:
    std::string_view name_;
};

int main() {
    Trace outer{"outer"};
    {
        Trace inner{"inner"};
        std::cout << "Working\n";
    }
    std::cout << "End of main\n";
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

`inner`가 포함된 블록이 끝나면 먼저 소멸하고, `outer`는 `main()`이 끝날 때 정리됩니다. 객체를 사용 가능한 기간과 스코프 종료 순서를 연결해 보세요.

<a id="section-12-2"></a>

## 12.2. RAII — 객체 수명으로 자원 관리

**자원 획득 즉 초기화(Resource Acquisition Is Initialization, RAII)** 는 자원을 획득한 직후 관리 객체에 맡기고, 그 객체가 소멸할 때 자원을 반환하도록 하는 설계 방식입니다. 핵심은 `close()`나 `delete`를 함수의 모든 탈출 경로마다 직접 반복하지 않는다는 점입니다.

```text
자원 획득 → 관리 객체 구성 → 자원 사용 → 스코프 종료 → 자원 반환
```

Chapter 11의 `std::ifstream`도 RAII 객체입니다. 파일 스트림을 소멸하면 열린 파일이 정리됩니다. 잠금 역시 RAII가 유용한데, `<mutex>`의 `std::mutex`는 배타적 잠금을 제공하고 `std::lock_guard`는 스코프가 끝나면 자동으로 잠금 해제를 수행합니다. 예제는 단일 스레드로 사용법을 살펴보며, 다중 스레드와 데이터 경쟁은 Chapter 14에서 다룹니다.

**주의:** 소멸자는 정상적인 스코프 종료와 예외로 인한 스택 되감기(Stack Unwinding) 과정에서 호출되지만, 비정상적인 프로세스 강제 종료나 전원 장애까지 보장하지는 않습니다.


**예제 코드 — [02_raii_lock_guard.cpp](./examples/02_raii_lock_guard.cpp)**

```cpp
#include <iostream>
#include <mutex>

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
    std::cout << "Count: " << counter.read() << '\n';
}
```

**실행 결과**

```text
Count: 2
```

`read()`는 값을 읽는 함수이지만 내부 동기화용 `mutex_`를 잠급니다. `mutable`은 이런 논리적 읽기 전용 함수에서 동기화 멤버를 변경하도록 허용합니다.

<a id="section-12-3"></a>

## 12.3. Ownership & Borrowing — 소유권과 대여

**소유권(Ownership)** 은 자원을 누가 반환할 책임이 있는지를 나타내는 계약입니다. 반면 **대여(Borrowing)** 는 소유권을 넘기지 않고 필요한 동안만 객체를 참조하는 접근 방식입니다. 두 역할을 함수의 매개변수 타입에서 구분하면 자원을 중복 해제하거나 누락할 가능성을 줄일 수 있습니다.

| 매개변수 표현 | 소유권 변화 | 대표적인 용도 |
|---|---|---|
| `const T&` | 없음 | 변경 없이 객체 관찰 |
| `T&` | 없음 | 호출자의 객체 수정 |
| `T*` | 보통 없음 | `nullptr`을 허용할 수 있는 비소유 접근 |
| `std::span<T>` | 없음 | 연속된 요소들을 대여 |
| `std::unique_ptr<T>`를 값으로 받기 | 독점 소유권 인수 | 자원 소유자를 함수 안으로 이전 |
| `std::shared_ptr<T>`를 값으로 받기 | 공유 소유권 참여 | 수명을 공동으로 관리 |

아래 예제의 `inspect()`는 읽기만 수행하지만 `register_device()`는 독점 소유권을 값으로 전달받습니다. `std::move(device)` 이후에는 원래 포인터의 소유권이 넘어갔으므로, 포인터가 비어 있는지 확인한 뒤에는 역참조하지 않습니다.

`<memory>`에는 `std::unique_ptr`와 `std::make_unique`가, `<utility>`에는 `std::move`가 정의되어 있습니다.


**예제 코드 — [16_resource_contracts.cpp](./examples/16_resource_contracts.cpp)**

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <utility>

struct Device { std::string name; };

void inspect(const Device& value) { // 접근만 수행: 비소유
    std::cout << "Inspect: " << value.name << '\n';
}

void register_device(std::unique_ptr<Device> device) { // 소유권 인수
    inspect(*device);
    std::cout << "Registered\n";
}

int main() {
    auto device = std::make_unique<Device>(Device{"Pump-A"});
    inspect(*device);
    register_device(std::move(device));
    std::cout << std::boolalpha << "Owner empty: " << (device == nullptr) << '\n';
}
```

**실행 결과**

```text
Inspect: Pump-A
Inspect: Pump-A
Registered
Owner empty: true
```

`register_device()`는 `std::unique_ptr`를 값으로 받으므로 소유권을 인수합니다. 원래 소유자는 더 이상 관리 중인 객체를 역참조하면 안 됩니다.

<a id="section-12-4"></a>

## 12.4. Unique Ownership — `std::unique_ptr`

**스마트 포인터(Smart Pointer)** `std::unique_ptr<T>`는 동적 자원의 소유자를 한 명으로 제한합니다. 소유 객체가 스코프를 벗어나면 관리 중인 자원이 정리되므로 일반적인 경우 `new`와 `delete`를 직접 호출할 필요가 없습니다. 객체 생성에는 `<memory>`의 `std::make_unique<T>(...)`를 우선 사용합니다.

| 연산 | 의미 |
|---|---|
| `*owner`, `owner->member` | 관리하는 객체에 접근 (비어 있으면 안 됨) |
| `owner.get()` | 소유권을 이전하지 않고 원시 포인터 조회 |
| `std::move(owner)` | 이전 대상이 이동을 선택하도록 rvalue로 변환 |
| `owner.reset()` | 현재 자원 정리 또는 새 자원으로 교체 |
| `owner.release()` | 자동 해제 없이 소유권 포기. 반환된 포인터 관리 책임을 별도로 인수해야 함 |

아래 코드는 `inspect(*owner)`로 읽기만 한 뒤 소유권을 다른 `unique_ptr`에 이전합니다. 이동 이후 원래 `unique_ptr`가 `nullptr`이 되는 상태는 이 타입이 명시적으로 보장하는 동작입니다.


**예제 코드 — [03_unique_ownership.cpp](./examples/03_unique_ownership.cpp)**

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <utility>

struct Device {
    std::string name;
    explicit Device(std::string value) : name(std::move(value)) {}
};

void inspect(const Device& device) {
    std::cout << "Device: " << device.name << '\n';
}

int main() {
    auto owner = std::make_unique<Device>("Motor-A");
    inspect(*owner);
    auto next_owner = std::move(owner);
    std::cout << std::boolalpha << "Old owner empty: " << (owner == nullptr) << '\n';
    inspect(*next_owner);
}
```

**실행 결과**

```text
Device: Motor-A
Old owner empty: true
Device: Motor-A
```

`owner`는 이동 뒤 비어 있지만 `next_owner`가 자원을 관리합니다. 두 포인터가 같은 자원을 동시에 독점 소유하지 않습니다.

<a id="section-12-5"></a>

## 12.5. Custom Deleter — 외부 자원 해제

자원은 반드시 `delete`로 반환하는 것이 아닙니다. C 라이브러리의 파일 핸들 `std::FILE*`는 `std::fclose()`로 닫아야 합니다. **사용자 정의 삭제자(Custom Deleter)** 는 자원별 반환 규칙을 `std::unique_ptr<T, Deleter>`에 전달합니다.

`<cstdio>`는 C 스타일 파일 함수(`std::tmpfile`, `std::fputs`, `std::fflush`, `std::fclose`)를, `<memory>`는 소유권 관리자를 제공합니다. 예제에서는 임시 파일을 열고 출력한 뒤, 관리 객체의 소멸자가 파일을 닫도록 합니다. 임시 파일 생성 가능 여부는 실행 환경에 따라 다를 수 있습니다.

**해제 실패와 저장 실패는 구분해야 합니다.** 삭제자 안에서 무시한 `fclose()`의 오류는 사용자에게 전달되지 않습니다. 중요한 파일 저장에서는 기록 후 스트림 상태와 `close()`의 성공 여부를 명시적으로 확인해야 합니다. RAII는 자원 반환을 쉽게 하지만 영구 저장의 내구성까지 보장하지는 않습니다.


**예제 코드 — [04_custom_deleter.cpp](./examples/04_custom_deleter.cpp)**

```cpp
#include <cstdio>
#include <iostream>
#include <memory>

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
        std::cerr << "Cannot create temporary file\n";
        return 1;
    }
    if (std::fputs("sample=42\n", file.get()) < 0 || std::fflush(file.get()) != 0) {
        std::cerr << "Write failed\n";
        return 1;
    }
    std::cout << "Temporary file written\n";
}
```

**실행 결과**

```text
Temporary file written
```

출력 직전 파일 생성에 실패하면 에러 스트림으로 메시지를 기록하고 `1`을 반환합니다. `std::tmpfile()`이 만드는 임시 파일은 일반 파일과 이름·삭제 동작이 다를 수 있습니다.

<a id="section-12-6"></a>

## 12.6. Shared & Weak Ownership — 공유 소유와 관찰

`std::shared_ptr<T>`는 여러 소유자가 같은 자원을 함께 관리할 때 사용합니다. **참조 계수(Reference Count)** 가 마지막 소유자까지 사라졌을 때 관리하는 자원을 정리합니다. 공동 소유권이 필요하지 않은 값에는 `std::unique_ptr`나 일반 값 타입을 사용하는 편이 의도가 명확합니다.

`std::weak_ptr<T>`는 참조 계수를 증가시키지 않는 **비소유 관찰자(Non-owning Observer)** 입니다. 다른 객체가 이미 해제되었을 수 있으므로 `lock()`으로 잠시 `shared_ptr`를 확보한 후 접근해야 합니다. 두 객체가 서로를 `shared_ptr`로 소유하는 **순환 참조(Cyclic Reference)** 를 만들면 자원이 해제되지 않을 수 있는데, 한쪽 관계를 `weak_ptr`로 표현하여 방지할 수 있습니다.

아래 예제에서는 `owner`와 `second`가 동시에 소유할 때 참조 계수가 2이고, 마지막 소유자가 정리되면 관찰자는 만료 상태가 됩니다. `lock()`이 만들어 내는 임시 소유자도 존재하는 동안에는 수명에 영향을 줍니다.


**예제 코드 — [06_shared_weak.cpp](./examples/06_shared_weak.cpp)**

```cpp
#include <iostream>
#include <memory>

int main() {
    auto owner = std::make_shared<int>(42);
    std::weak_ptr<int> observer = owner;
    {
        auto second = owner;
        std::cout << "Owners: " << owner.use_count() << '\n';
        if (auto borrowed = observer.lock()) {
            std::cout << "Value: " << *borrowed << '\n';
        }
    }
    owner.reset();
    std::cout << std::boolalpha << "Expired: " << observer.expired() << '\n';
}
```

**실행 결과**

```text
Owners: 2
Value: 42
Expired: true
```

`observer.lock()`이 성공한 동안에는 일시적인 공유 소유자가 생깁니다. `owner.reset()` 이후에는 살아 있는 공유 소유자가 없어 `expired()`가 참입니다.

<a id="section-12-7"></a>

## 12.7. Value Categories — 값 범주와 rvalue 참조

C++ 표현식은 타입뿐 아니라 **값 범주(Value Category)** 도 가집니다. 간단히 구분하면 `lvalue`는 식별 가능한 기존 객체를 나타내고, `prvalue`는 값을 생성하는 표현식, `xvalue`는 자원을 이전할 수 있음을 나타내는 표현식입니다.

| 표현식 | 값 범주 | 설명 |
|---|---|---|
| `value` | lvalue | 이름 있는 기존 객체 |
| `std::string{"abc"}` | prvalue | 임시 값을 생성하는 표현식 |
| `std::move(value)` | xvalue | 기존 객체를 이동 후보로 표시 |

`T&`와 `T&&`를 각각 좌값 참조(Lvalue Reference), 우값 참조(Rvalue Reference)라고 부릅니다. 주의할 점은 **이름이 있는 우값 참조 변수도 이름으로 사용할 때에는 lvalue** 라는 사실입니다. 예제는 동일한 `inspect()` 함수의 `const std::string&`와 `std::string&&` 오버로드 중 어떤 것이 선택되는지 보여 줍니다. 여기서 `std::move`는 실제 복사를 수행하지 않고 표현식의 값 범주를 바꾸기만 합니다.


**예제 코드 — [07_value_categories.cpp](./examples/07_value_categories.cpp)**

```cpp
#include <iostream>
#include <string>
#include <utility>

void inspect(const std::string&) { std::cout << "Lvalue\n"; }
void inspect(std::string&&) { std::cout << "Rvalue\n"; }

int main() {
    std::string text{"abc"};
    inspect(text);
    inspect(std::move(text));
    std::string&& named_reference = std::string{"temporary"};
    inspect(named_reference); // 이름을 가진 rvalue 참조 표현식은 lvalue
}
```

**실행 결과**

```text
Lvalue
Rvalue
Lvalue
```

세 번째 호출의 `named_reference`는 선언 타입이 `std::string&&`이더라도 표현식 자체는 lvalue이므로 `const std::string&` 오버로드가 선택됩니다.

<a id="section-12-8"></a>

## 12.8. Move Semantics — 이동과 이동 전용 타입

**이동 의미론(Move Semantics)** 은 객체가 소유한 자원을 필요할 때 다른 객체로 이전할 수 있게 합니다. `std::move(x)`는 곧바로 데이터를 옮기는 함수가 아니라, 이동 생성자 등 이동 연산이 선택될 수 있도록 `x`를 xvalue로 표현하는 캐스트입니다. 대상 타입이 이동을 제공하지 않으면 복사가 선택될 수도 있습니다.

```text
복사: 원본을 보존하면서 대상 객체의 값 구성
이동: 원본이 소유한 자원을 대상에 이전할 수 있음
```

`const` 객체에 `std::move()`를 적용하더라도 일반적으로 이동 생성자가 아닌 복사가 선택될 수 있습니다. 이동 대상 타입이 실제로 무엇을 지원하는지 확인해야 합니다.

이동된 표준 라이브러리 객체는 일반적으로 유효하지만 값이 특정되지 않는 경우가 많습니다. 따라서 `std::string`의 이동 이후 내용이 반드시 비어 있다고 가정하지 않고, 새 값을 대입한 후 재사용합니다. **이동 전용 타입(Move-only Type)** 은 복사를 허용하지 않고 이동만 허용하는 타입으로 `std::unique_ptr`가 대표적입니다. `std::vector`에 이동 전용 객체를 추가할 때는 `emplace_back()`으로 제자리 생성하거나, 이미 존재하는 객체를 `std::move()`로 이전합니다.


**예제 ① 이동 후 재사용 — [05_move_semantics.cpp](./examples/05_move_semantics.cpp)**

```cpp
#include <iostream>
#include <string>
#include <utility>

int main() {
    std::string source{"sensor-packet"};
    std::string target = std::move(source);
    std::cout << "Target: " << target << '\n';
    // 이동 이후의 source 내용은 가정하지 않고 새 값을 대입합니다.
    source = "reused";
    std::cout << "Source: " << source << '\n';
}
```

**실행 결과**

```text
Target: sensor-packet
Source: reused
```


**예제 ② 이동 전용 객체 — [06_move_only.cpp](./examples/06_move_only.cpp)**

```cpp
#include <iostream>
#include <memory>
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
    std::cout << "Jobs: " << *jobs.at(0).id << " / " << *jobs.at(1).id << '\n';
}
```

**실행 결과**

```text
Jobs: 10 / 20
```

`Job`에 `std::unique_ptr` 멤버가 있으므로 기본 복사는 불가능합니다. `emplace_back(10)`은 새 요소를 직접 생성하고 `push_back(std::move(task))`는 이동을 허용합니다.

<a id="section-12-9"></a>

## 12.9. Special Member Functions — 복사·이동 생성자와 대입

복사·이동의 구체적인 동작은 클래스의 **특수 멤버 함수(Special Member Functions)** 로 정의할 수 있습니다. 기존 객체에서 새 객체를 만드는 생성과 이미 존재하는 객체의 상태를 바꾸는 대입은 서로 다른 연산입니다.

| 동작 | 선언 형태 |
|---|---|
| 복사 생성 | `T(const T&)` |
| 복사 대입 | `T& operator=(const T&)` |
| 이동 생성 | `T(T&&)` |
| 이동 대입 | `T& operator=(T&&)` |
| 소멸 | `~T()` |

`= default`는 컴파일러가 제공할 수 있는 구현을 사용하겠다는 뜻이고 `= delete`는 해당 연산을 금지합니다. **사용자 선언 소멸자나 복사 관련 멤버는 암시적 이동 멤버의 생성 규칙에 영향을 줄 수 있습니다.** 따라서 소멸자만 가볍게 추가했다고 가정해 이동 가능성을 단정해서는 안 됩니다. 다음 예제는 복사 생성자와 이동 생성자가 각각 호출되는 상황을 확인합니다.


**예제 코드 — [07_copy_move_tracing.cpp](./examples/07_copy_move_tracing.cpp)**

```cpp
#include <iostream>
#include <utility>

struct Probe {
    Probe() = default;
    Probe(const Probe&) { std::cout << "Copy\n"; }
    Probe(Probe&&) noexcept { std::cout << "Move\n"; }
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

`copied`는 이름 있는 `source`에서 구성하므로 복사 생성자가, `moved`는 이동 후보 표현식에서 구성하므로 이동 생성자가 선택됩니다.

<a id="section-12-10"></a>

## 12.10. Rule of Zero — 특별 멤버 함수가 필요 없는 설계

**제로 규칙(Rule of Zero)** 은 직접 자원을 해제하는 역할이 없는 클래스에서는 복사·이동·소멸자를 직접 구현하지 않는 설계 원칙입니다. 이미 자원 관리를 수행하는 `std::string`, `std::vector`, `std::unique_ptr`를 멤버로 두고, 클래스는 도메인 데이터와 규칙을 처리하도록 분리합니다.

예제의 `SensorBatch`는 자원 관리 특별 멤버 함수를 구현하지 않았어도 표준 라이브러리 멤버의 복사·이동 동작을 활용할 수 있습니다. 단, 모든 클래스가 복사 가능한 것은 아닙니다. 예를 들어 `std::unique_ptr`를 멤버로 가진 타입은 명시적 깊은 복사 구현이 없으면 복사가 제한됩니다.

실무에서는 직접 메모리를 관리하는 클래스를 만들어 특별 멤버 함수 다섯 개를 늘리는 것보다, **소유권을 담당하는 표준 타입을 합성(Composition)** 해서 불필요한 구현을 줄이는 편이 우선입니다.


**예제 코드 — [08_rule_of_zero.cpp](./examples/08_rule_of_zero.cpp)**

```cpp
#include <iostream>
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
    std::cout << "Copy samples: " << copied.readings.size() << '\n';
    std::cout << "Move samples: " << moved.readings.size() << '\n';
}
```

**실행 결과**

```text
Copy samples: 3
Move samples: 3
```

복사본과 이동된 객체 모두 3개의 읽기 값을 보유합니다. 이동 이전의 `first`에 어떤 내용이 남았는지는 출력하거나 검사하지 않습니다.

<a id="section-12-11"></a>

## 12.11. Rule of Three & Five — 직접 자원을 관리하는 클래스

**세 가지 규칙(Rule of Three)** 은 직접 자원을 관리하는 타입에서 소멸·복사 생성·복사 대입을 함께 고려해야 한다는 원칙입니다. 이동 의미론까지 포함하면 **다섯 가지 규칙(Rule of Five)** 으로 확장됩니다. 그러나 모든 클래스에 이 함수 다섯 개를 작성하라는 뜻은 아닙니다. Rule of Zero가 기본이고, 직접 자원을 관리하거나 복사 동작을 맞춤 정의해야 할 때만 검토합니다.

여기서는 `std::unique_ptr<int[]>`로 배열의 수명을 관리하되, 값을 복사할 수 있는 `IntBuffer`를 만들기 위해 복사 생성·복사 대입을 직접 구현합니다. `<algorithm>`의 `std::copy_n`은 지정한 개수의 요소를 복사하고, `<stdexcept>`의 `std::out_of_range`는 유효하지 않은 인덱스를 알릴 때 사용합니다.

- **깊은 복사(Deep Copy):** 다른 배열 저장 공간을 만들어 내용을 복사합니다. 단순 포인터 복사로 두 객체가 같은 배열을 해제하지 않게 합니다.
- **복사 후 교환(Copy-and-Swap):** 먼저 복사본을 완성한 뒤 기존 데이터와 교환합니다. 복사 실패 시 기존 상태를 변경하지 않습니다.
- **이동:** 자원 관리자를 이전하고 원래 객체의 크기를 `0`으로 돌립니다.
- **자기 대입(Self-assignment):** `this != &other`로 불필요한 처리와 자원 손상을 피합니다.

직접 관리한 배열의 크기와 반환 규칙을 비교해 보면 왜 특별 멤버 함수가 서로 연결되는지 알 수 있습니다. 실제 배열 데이터 저장에는 먼저 `std::vector`를 고려하세요.


**예제 코드 — [09_rule_of_five.cpp](./examples/09_rule_of_five.cpp)**

```cpp
#include <algorithm>
#include <cstddef>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <utility>

class IntBuffer {
public:
    explicit IntBuffer(std::size_t size)
        : data_(size ? std::make_unique<int[]>(size) : nullptr), size_(size) {}
    ~IntBuffer() = default;

    IntBuffer(const IntBuffer& other) : IntBuffer(other.size_) {
        if (size_ != 0) {
            std::copy_n(other.data_.get(), size_, data_.get());
        }
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
    IntBuffer copied{first};
    copied.at(0) = 50;
    IntBuffer moved{std::move(first)};
    std::cout << "Copy: " << copied.at(0) << ", Moved: " << moved.at(0)
              << ", Old size: " << first.size() << '\n';
}
```

**실행 결과**

```text
Copy: 50, Moved: 7, Old size: 0
```

복사본의 첫 번째 값을 수정해도 이동한 원본 데이터의 값은 바뀌지 않습니다. 두 객체가 서로 다른 배열을 소유하기 때문입니다.

<a id="section-12-12"></a>

## 12.12. `std::exchange` & Moved-from State — 이동 후 상태

`std::exchange(object, new_value)`는 기존 값을 반환하면서 대상에 새 값을 대입하는 `<utility>`의 함수입니다. 이동 생성자에서 원본 객체를 명시적 무효 상태로 바꿀 때 활용할 수 있습니다.

예제의 `OwnedHandle`은 실제 OS 핸들이 아니라 **반환 횟수를 관찰하기 위한 시뮬레이션** 입니다. 정수 `-1`을 소유하지 않은 상태로 사용합니다. `OwnedHandle`을 이동하면 원본 ID가 `-1`로 바뀌고, 종료할 때 유효한 ID를 가진 소유자만 반환 횟수를 증가시킵니다.

**중요:** `std::move` 자체는 원본을 `-1`로 만드는 함수가 아닙니다. 여기서는 `OwnedHandle`의 이동 생성자에 `std::exchange(other.id_, -1)`를 직접 작성했기 때문에 그 상태가 보장됩니다. 실제 운영체제의 핸들은 플랫폼별 무효 값과 해제 함수를 정확히 따라야 합니다.


**예제 코드 — [10_exchange_state.cpp](./examples/10_exchange_state.cpp)**

```cpp
#include <iostream>
#include <utility>

// 실제 장치 대신, 정리 횟수를 세는 가상의 자원 식별자를 사용합니다.
class OwnedHandle {
public:
    explicit OwnedHandle(int id) noexcept : id_(id) {}
    ~OwnedHandle() { release(); }
    OwnedHandle(const OwnedHandle&) = delete;
    OwnedHandle& operator=(const OwnedHandle&) = delete;
    OwnedHandle(OwnedHandle&& other) noexcept
        : id_(std::exchange(other.id_, -1)) {}
    OwnedHandle& operator=(OwnedHandle&& other) noexcept {
        if (this != &other) {
            release();
            id_ = std::exchange(other.id_, -1);
        }
        return *this;
    }
    [[nodiscard]] int id() const noexcept { return id_; }
    [[nodiscard]] static int released() noexcept { return released_; }
private:
    void release() noexcept {
        if (id_ != -1) {
            ++released_;
            id_ = -1;
        }
    }
    int id_{-1};
    inline static int released_{0};
};

int main() {
    {
        OwnedHandle first{42};
        OwnedHandle second{std::move(first)};
        std::cout << "New: " << second.id() << ", Old: " << first.id() << '\n';
    }
    std::cout << "Released: " << OwnedHandle::released() << '\n';
}
```

**실행 결과**

```text
New: 42, Old: -1
Released: 1
```

원본이 이동 후 `-1`이 되므로 이중 반환이 일어나지 않습니다. 소멸 시점의 반환 횟수는 1회입니다.

<a id="section-12-13"></a>

## 12.13. Copy Elision & NRVO — 불필요한 복사·이동 생략

**복사 생략(Copy Elision)** 은 불필요한 중간 객체의 복사·이동을 피하는 규칙입니다. C++17부터 같은 타입의 prvalue를 반환하는 특정 경우에는 최종 대상에 바로 객체를 생성하므로 복사 생성자와 이동 생성자가 없어도 가능합니다.

```cpp
Token make_token(int id) { return Token{id}; }  // 같은 타입 prvalue: 직접 구성 보장
```

반대로 이름이 붙은 지역 변수를 `return local;`로 반환할 때는 **이름 있는 반환값 최적화(Named Return Value Optimization, NRVO)** 가 적용될 *수* 있지만 보장되지는 않습니다. 함수의 지역 객체에 습관적으로 `return std::move(local);`을 붙이면 NRVO 적용 기회를 방해할 수 있습니다. 성능이 중요한 경우에는 컴파일러 동작을 가정하기보다 프로파일링하고 측정해야 합니다.


**예제 코드 — [11_copy_elision.cpp](./examples/11_copy_elision.cpp)**

```cpp
#include <iostream>

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
    return Token{id}; // 같은 타입 prvalue: C++17부터 직접 구성 보장
}

int main() {
    Token token = make_token(27);
    std::cout << "Token: " << token.id() << '\n';
}
```

**실행 결과**

```text
Token: 27
```

`Token`은 복사·이동 생성자가 모두 삭제되어 있지만 `return Token{id};` 형태는 C++20에서 동작합니다. NRVO가 가능한 경우와 혼동하지 마세요.

<a id="section-12-14"></a>

## 12.14. `noexcept` & `std::move_if_noexcept` — 이동과 예외

`noexcept`는 함수가 예외를 던지지 않는다는 계약을 표시합니다. 특히 이동 생성자에 `noexcept`가 붙어 있으면 `std::vector` 같은 컨테이너가 재할당 과정에서 이동을 선택하는 데 유리할 수 있습니다. 다만 실제로 예외가 밖으로 전파된다면 `std::terminate()`가 호출될 수 있으므로 무조건 붙여서는 안 됩니다.

`<utility>`의 `std::move_if_noexcept()`는 이동이 예외를 던질 수 있고 복사가 가능한 타입에서는 복사를 선택할 수 있게 합니다. 아래 예제의 `Fragile`은 이동 생성자에 `noexcept(false)`를 선언했고 복사가 가능하므로 `Copy`가 출력됩니다.

**주의:** 이동 전용 타입처럼 복사할 수 없는 경우에는 이동이 예외를 던질 수 있더라도 이동이 선택될 수 있습니다. 이 기능이 모든 컨테이너 연산의 강한 예외 보장을 자동으로 보장하는 것은 아닙니다.


**예제 코드 — [12_move_if_noexcept.cpp](./examples/12_move_if_noexcept.cpp)**

```cpp
#include <iostream>
#include <utility>

struct Fragile {
    Fragile() = default;
    Fragile(const Fragile&) { std::cout << "Copy\n"; }
    Fragile(Fragile&&) noexcept(false) { std::cout << "Move\n"; }
};

int main() {
    Fragile source;
    Fragile target{std::move_if_noexcept(source)};
    (void)target;
}
```

**실행 결과**

```text
Copy
```

이 예제에서는 복사 생성자가 호출됩니다. 컨테이너 내부 재배치를 설명하기 위한 단순화된 함수 호출입니다.

<a id="section-12-15"></a>

## 12.15. Exception Safety — 실패에도 상태 유지

**예외 안전성(Exception Safety)** 은 동작 도중 예외가 발생해도 프로그램의 자원과 상태가 어떤 조건을 유지하는지를 설명합니다. 단순히 `try`/`catch`로 오류 메시지를 출력하는 것과는 다릅니다.

| 수준 | 보장 내용 |
|---|---|
| No-throw Guarantee | 해당 연산이 예외를 밖으로 내보내지 않음 |
| Strong Guarantee | 실패 시 관찰 가능한 기존 상태가 유지됨 |
| Basic Guarantee | 실패해도 객체의 유효한 상태와 자원 누수 방지 등을 유지함 |

`ReadingStore::replace()`는 새 값을 임시 벡터에 넣고 **모든 검증을 완료한 후에만** 기존 벡터와 교환합니다. 입력값에 오류가 있거나 임시 벡터 복사에서 예외가 발생하면 기존 객체가 바뀌지 않습니다. 이 패턴은 임시 상태 구성 후 확정(Commit)하는 **트랜잭션 형태의 상태 갱신**입니다.

이 예제의 `swap()`은 기본 `std::allocator`를 사용하는 벡터 사이의 교환이며 예외를 던지지 않습니다. 다른 사용자 정의 자원이나 외부 파일에까지 같은 보장이 자동 적용된다고 생각하면 안 됩니다.


**예제 코드 — [13_exception_safety.cpp](./examples/13_exception_safety.cpp)**

```cpp
#include <iostream>
#include <span>
#include <stdexcept>
#include <utility>
#include <vector>

class ReadingStore {
public:
    explicit ReadingStore(std::vector<int> values) : values_(std::move(values)) {}
    void replace(std::span<const int> incoming) {
        std::vector<int> staged{incoming.begin(), incoming.end()};
        for (int value : staged) {
            if (value < 0 || value > 100) {
                throw std::invalid_argument("reading outside 0..100");
            }
        }
        values_.swap(staged); // 검증이 끝나면 한 번에 교체
    }
    [[nodiscard]] int first() const { return values_.at(0); }
private:
    std::vector<int> values_;
};

int main() {
    ReadingStore store{{10, 20}};
    const int incoming[]{30, 130};
    try {
        store.replace(incoming);
    } catch (const std::invalid_argument&) {
        std::cout << "Rejected\n";
    }
    std::cout << "First: " << store.first() << '\n';
}
```

**실행 결과**

```text
Rejected
First: 10
```

검증에 실패하더라도 `readings_` 대신 `values_`가 기존 값 10을 유지합니다. 오류를 감지할 수 있다는 사실만으로 Strong Guarantee를 얻는 것은 아닙니다.

<a id="section-12-16"></a>

## 12.16. Non-owning Views — 수명과 무효화

`std::span<T>`는 연속된 요소들의 구간을, `std::string_view`는 문자열 구간을 **소유하지 않고 관찰**합니다. 이들은 Chapter 06~07에서 다룬 뷰(View)의 연장선입니다. `std::span`은 `<span>`에서, `std::string_view`는 `<string_view>`에서 제공합니다.

`std::vector`가 요소를 추가하면서 재할당하면 기존 포인터·참조·반복자가 무효화될 수 있습니다. 같은 이유로 저장 공간을 관찰하던 `std::span`도 더는 안전하지 않을 수 있습니다. `std::string_view` 역시 원본 문자열이 소멸·변경되어 저장 공간이 바뀌면 댕글링 뷰(Dangling View)가 될 수 있습니다.

예제에서는 소유자 `readings`, `name`이 살아 있는 동안만 뷰를 매개변수로 사용합니다. 아래 코드는 안전한 접근의 예지만, 함수가 이 뷰를 보관하거나 나중에 반환한다면 수명 계약을 별도로 검토해야 합니다.


**예제 코드 — [14_borrowed_view.cpp](./examples/14_borrowed_view.cpp)**

```cpp
#include <iostream>
#include <span>
#include <string>
#include <string_view>
#include <vector>

void inspect(std::span<const int> values, std::string_view source) {
    std::cout << source << ": " << values.front() << '\n';
}

int main() {
    std::vector<int> readings{12, 14, 18};
    std::string name{"sensor-A"};
    inspect(readings, name);
    // readings/name이 살아 있는 동안에만 span/string_view가 유효합니다.
}
```

**실행 결과**

```text
sensor-A: 12
```

`inspect()`가 뷰를 저장하거나 반환하지 않기 때문에 이 예제에서는 소유자의 수명이 충분합니다.

<a id="section-12-17"></a>

## 12.17. Error Handling — C++20 결과 표현

자원 생성이 실패할 수 있다면 반환형에 실패 가능성을 표현해야 합니다. C++17부터 사용할 수 있는 `<optional>`의 `std::optional<T>`는 **값이 있거나 없는 상태**를 나타냅니다. 실패 원인을 구분할 필요가 없을 때는 충분하지만, 이유가 여러 개인 경우에는 별도 오류 타입이 필요합니다.

아래 예제의 `create_device()`는 장치 ID가 비어 있으면 `std::nullopt`를 반환하고, 성공하면 값 타입 `Device`를 반환합니다. 상세 오류가 필요한 `Device Session Manager` 프로젝트에서는 Chapter 09에서 다룬 `std::variant<Session, OpenError>`를 사용해 성공값과 실패 원인을 구분합니다. `std::variant`는 `<variant>` 헤더에 정의되어 있습니다.

<details>
<summary>C++23 이후 참고 — `std::expected`</summary>

C++23의 `<expected>`에는 `std::expected<T, E>`가 도입되어 성공값 `T`와 오류값 `E`를 함께 표현할 수 있습니다. **이 타입은 C++20 표준 라이브러리에 포함되지 않으므로** 이번 Chapter의 기본 소스에서는 사용하지 않습니다. 오류가 없다는 것만 알아도 된다면 `std::optional`, 원인을 명확히 전달해야 한다면 C++20의 `std::variant`나 전용 결과 구조체를 사용할 수 있습니다.

</details>


**예제 코드 — [15_optional_factory.cpp](./examples/15_optional_factory.cpp)**

```cpp
#include <iostream>
#include <optional>
#include <string>
#include <string_view>

struct Device {
    std::string id;
};

[[nodiscard]] std::optional<Device> create_device(std::string_view id) {
    if (id.empty()) return std::nullopt;
    return Device{std::string{id}};
}

int main() {
    auto device = create_device("sensor-A");
    if (device) std::cout << "Created: " << device->id << '\n';
    if (!create_device("")) std::cout << "Rejected empty id\n";
}
```

**실행 결과**

```text
Created: sensor-A
Rejected empty id
```

`std::optional`은 성공 여부만 전달합니다. 입력 형식 오류와 시스템 장치 미연결을 구별하려면 에러 정보를 따로 설계합니다.

<a id="section-12-18"></a>

## 12.18. Coding Practice — 연습문제

각 문제에는 학생용 시작 코드와 독립적으로 실행 가능한 모범답안이 있습니다. **입력은 표준 입력이 아니라 명시된 함수 인수 또는 객체 생성 인수**이며, `main()`은 이를 보여 주는 데모입니다. 실제 검증에서는 여러 인수를 직접 전달해 결과와 내부 상태를 검사합니다.

| Exercise | 핵심 주제 | 학생용 코드 | 모범답안 |
|:---:|---|---|---|
| 01 | Transactional Update — 검증 후 일괄 교체 | [시작 코드](./exercises/01_transactional_update.cpp) | [정답](./solutions/01_transactional_update.cpp) |
| 02 | Unique Owner — 소유권 이전 | [시작 코드](./exercises/02_unique_owner.cpp) | [정답](./solutions/02_unique_owner.cpp) |
| 03 | Move-only Packet — 이동 후 유효 상태 | [시작 코드](./exercises/03_move_only_packet.cpp) | [정답](./solutions/03_move_only_packet.cpp) |
| 04 | Device Factory — 실패하는 생성 | [시작 코드](./exercises/04_device_factory.cpp) | [정답](./solutions/04_device_factory.cpp) |

### Exercise 01 — Transactional Update

센서 측정값 전체를 새 묶음으로 바꾸는 `SensorStore::replace(std::span<const int>)`를 완성합니다. 부분 갱신이 아니라 **모든 검증을 통과한 후 한 번에 교체**해야 합니다.

- **입력:** 정수 구간. 값은 0~100을 허용하며 빈 구간은 거부합니다.
- **출력 및 처리:** 성공하면 이전 값을 대체합니다. 실패하면 `std::invalid_argument`를 던지고 기존 값은 그대로 유지합니다.
- **구현 조건:** 임시 벡터 구성 → 전체 검증 → `swap()` 순서로 구현합니다.
- **완료 기준:** 0·100 경계값, 비어 있는 입력, 음수·101 이상의 값, 기존 상태 보존을 검증합니다.

**데모 실행 결과 (모범답안)**

```text
Rejected
First: 10
Updated: 60
```

### Exercise 02 — Unique Owner

장치 한 개만 보관하는 `DeviceRegistry::install(std::unique_ptr<Device>)`를 완성합니다. 새 장치를 설치할 때 기존 장치는 정리되고 새 장치의 독점 소유권을 Registry로 이전합니다.

- **입력:** `std::unique_ptr<Device>` (이름이 있는 장치 또는 비어 있는 포인터).
- **출력 및 처리:** `name()`, `has_device()`로 상태를 조회합니다. 비어 있거나 이름이 없는 장치는 `std::invalid_argument`로 거부합니다.
- **구현 조건:** 검증 실패 시 기존 장치 유지, 성공 시 `std::move()`로 소유권 이전.
- **완료 기준:** 설치·교체·`nullptr`·빈 이름과 원래 소유자의 빈 상태를 검증합니다.

**데모 실행 결과**

```text
Device: Motor-A
Old owner empty: true
```

### Exercise 03 — Move-only Packet

`std::unique_ptr<std::vector<int>>`를 멤버로 갖는 `Packet`의 조회 함수를 완성합니다. 복사는 금지하고 이동은 허용합니다.

- **입력:** 생성자에 전달한 정수 묶음.
- **출력:** `size()`는 원소 수, `sum()`은 총합을 반환합니다. `<numeric>`의 `std::accumulate`는 지정한 범위의 값들을 누적하는 데 사용할 수 있습니다.
- **구현 조건:** 이동으로 소유권을 넘긴 원본도 조회 함수에서 안전하게 `0`을 반환해야 합니다.
- **완료 기준:** 복사 금지 여부, 이동 생성·이동 대입, 빈 패킷·이동 후 원본 상태를 검사합니다.

**데모 실행 결과**

```text
Size: 3, Sum: 10
Old size: 0
```

### Exercise 04 — Device Factory

유효한 매개변수로만 `Device` 값을 만드는 `make_device()`를 구현합니다. 생성 실패가 예외 상황인지 일반적인 입력 거부인지 구분해 봅니다.

- **입력:** 장치 이름과 정수 제한값(`limit`). 이름은 1~16자, 영문자·숫자·하이픈만 허용합니다. `limit`는 0~100입니다.
- **출력:** 성공하면 `std::optional<Device>`에 값이 있고, 실패하면 `std::nullopt`입니다.
- **완료 기준:** 이름 길이 경계, 허용되지 않은 문자, 음수·101 이상, 0·100을 검사합니다.

**데모 실행 결과**

```text
Created: sensor-A / 80
Rejected empty name
```

**컴파일 및 테스트**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/01_transactional_update.cpp -o transactional_update
./transactional_update

python tests/check.py
python tests/check.py --mode student --only exercise-01
```

첫 번째 검증 명령은 전체 예제·모범답안을 검사합니다. `--mode student`는 학생 파일을 검증합니다. `TODO`를 완료하지 않았다면 해당 테스트의 실패가 정상적인 시작 상태입니다. 테스트는 정답 문자열뿐 아니라 함수 반환값과 객체 상태도 검사합니다.

<a id="section-12-19"></a>

## 12.19. Mini Project — Device Session Manager

가상의 장치 SDK에서 장치를 열고, 측정값을 읽고, 연결을 종료하는 작은 프로그램을 만듭니다. Chapter 11의 파일 스트림과 비슷하게, 장치 연결도 **획득한 자원을 반드시 한 번 반환해야 하는 대상**으로 취급합니다. 실제 하드웨어나 드라이버를 설치하지 않고 테스트할 수 있도록 장치 연결을 `RawPort` 구조체로 시뮬레이션합니다.

### 상황 및 요구사항

운영 프로그램이 장치 연결을 요청할 때 빈 ID나 연결할 수 없는 장치를 구분해야 합니다. 성공적으로 연결된 장치는 측정값을 반복해서 읽을 수 있어야 하고, 작업이 끝나거나 중간에 예외가 발생하면 자원이 정확히 한 번 정리되어야 합니다.

1. `Session::open(id)`는 성공 시 `Session`, 실패 시 `OpenError`를 나타냅니다. 반환형은 `std::variant<Session, OpenError>`입니다.
2. 빈 ID는 `OpenError::empty_id`, `offline`은 `OpenError::unavailable`로 구분합니다.
3. 정상 연결의 측정값은 `21, 24, 22` 순서로 반복됩니다.
4. `Session`은 복사할 수 없고 이동만 가능합니다. 이동 이후 원래 객체의 `name()`은 빈 문자열 뷰를 반환합니다.
5. 소유권이 없는 객체에서 `next_reading()`을 호출하면 `std::logic_error`를 발생시킵니다.
6. 관리 중인 자원은 소멸 시 `close_port()`로 한 번만 해제되어야 합니다. `closed_count()`로 이를 확인합니다.
7. `RawPort`의 자원 해제는 `std::unique_ptr<RawPort, Closer>`가 담당합니다. `Session` 외부에서는 원시 포인터를 삭제하지 않습니다.

**공개 데모의 출력**

```text
Connected: sensor-A
Samples: 21, 24, 22
Closed sessions: 1
Rejected: empty id
```

**학생용 프로젝트**

- [main.cpp](./project/main.cpp) — 호출 및 결과 확인
- [session.hpp](./project/session.hpp) — 공개 API와 소유권 계약
- [session.cpp](./project/session.cpp) — 미완성 구현 (`TODO`)
- [CMakeLists.txt](./project/CMakeLists.txt) — 독립 빌드 구성

**완성 예제 / 모범답안**

- [완성된 다중 파일 예제](./examples/17_device_session/) — 기존 GitHub Actions가 참조하는 경로 유지
- [모범답안 폴더](./solutions/device_session/) — 독립적으로 빌드 가능한 정답 프로젝트

**프로젝트 컴파일 — GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/main.cpp project/session.cpp -o device_session_student
./device_session_student
```

**완성 예제 — CMake**

```bash
cmake -S examples/17_device_session -B build/ch12 -DCMAKE_CXX_STANDARD=20
cmake --build build/ch12
ctest --test-dir build/ch12 --output-on-failure
```

**학생용 전체 검사**

```bash
python tests/check.py --mode student --only project
```

완료 기준은 정상 연결·오류 식별·이동 후 접근 검사·반복 읽기·정확한 자원 정리입니다. 테스트는 해당 동작을 별도로 확인하므로 출력만 흉내 내서는 통과하지 않습니다. 이 프로젝트의 `RawPort`는 교육용 가짜 장치이며, 실제 장치 SDK에서는 `close_port`의 실패 규칙과 스레드 안전성, 장치 재연결 정책 등을 별도로 다뤄야 합니다.

<a id="section-12-20"></a>

## 12.20. Quiz & Summary — 최종 점검

### Quiz

**1.** 스코프를 벗어날 때 객체가 생성된 순서의 역순으로 소멸하는 경우는 무엇입니까?

- A. 같은 블록에서 만든 지역 객체
- B. 모든 동적 할당 객체
- C. 전원 차단으로 강제 종료된 모든 객체

<details>
<summary>정답 및 해설</summary>

A. 같은 블록에서 정상적으로 생성·소멸하는 지역 객체는 생성 순서의 역순으로 소멸합니다. 동적 자원은 소유자의 수명과 반환 규칙에 따라 달라집니다.

</details>

**2.** RAII가 파일 처리 중 예외가 발생했을 때 유용한 이유를 설명하세요.

<details>
<summary>정답 및 해설</summary>

`std::ifstream`, `std::unique_ptr` 등 관리 객체의 소멸자가 자원 반환을 수행하므로 여러 실패 경로마다 해제 코드를 반복할 필요가 없습니다. 다만 강제 종료나 영구 저장 내구성은 별도 문제입니다.

</details>

**3.** 읽기만 하는 함수에 소유권을 이전하지 않으려면 어떤 매개변수가 적절합니까?

- A. `std::unique_ptr<T>` 값 전달
- B. `const T&`
- C. 반환된 원시 포인터에 `delete` 호출

<details>
<summary>정답 및 해설</summary>

B. `const T&`는 비소유 읽기 접근을 표현합니다. 소유권 이전이 필요한 함수에서만 `unique_ptr` 값 전달을 고려합니다.

</details>

**4.** `std::move(source)`가 실제로 데이터를 복사하거나 이동하는지 설명하세요.

<details>
<summary>정답 및 해설</summary>

`std::move`는 표현식을 xvalue로 바꾸는 캐스트이며 자체적으로 메모리를 옮기지 않습니다. 이후 선택되는 이동 생성자·이동 대입 등이 자원 이전을 수행할 수 있습니다. 대상 타입에 따라 복사가 일어날 수도 있습니다.

</details>

**5.** `std::unique_ptr<T>`를 이동한 직후 원래 포인터의 보장된 상태는 무엇입니까?

- A. 원래 객체를 계속 소유
- B. `nullptr`
- C. 반드시 예외 발생

<details>
<summary>정답 및 해설</summary>

B. `std::unique_ptr`에서 이동으로 소유권이 이전되면 원래 포인터는 비어 있게 됩니다. 일반 `std::string`의 이동 후 값까지 이 규칙으로 판단하면 안 됩니다.

</details>

**6.** `std::shared_ptr`와 `std::weak_ptr`의 수명 관리 차이를 설명하세요.

<details>
<summary>정답 및 해설</summary>

`shared_ptr`는 소유자로 참조 계수에 참여하지만 `weak_ptr`는 관리 대상의 수명을 연장하지 않습니다. 사용 시 `lock()`으로 잠시 공유 소유자를 얻고 만료 여부를 확인합니다.

</details>

**7.** 다음 중 이름이 있는 `T&& ref`를 표현식 `ref`로 사용했을 때의 값 범주는?

- A. lvalue
- B. prvalue
- C. xvalue

<details>
<summary>정답 및 해설</summary>

A. 우값 참조 타입이라도 이름으로 평가한 변수 표현식은 lvalue입니다. `std::move(ref)`와 구분해야 합니다.

</details>

**8.** Rule of Zero를 우선하라는 이유와 Rule of Five를 고려하는 상황을 설명하세요.

<details>
<summary>정답 및 해설</summary>

표준 라이브러리 타입으로 소유권을 관리하면 직접 복사·이동·소멸을 구현할 필요가 줄어 오류 가능성이 낮아집니다. 별도의 자원 관리 규칙이나 깊은 복사가 필요한 타입을 직접 만들 때 Rule of Five를 검토합니다.

</details>

**9.** `return T{};`에서 C++17 이후 조건을 충족하는 prvalue 반환은 어떻게 처리됩니까?

- A. 복사 생성자 필수
- B. 이동 생성자 필수
- C. 최종 대상에 직접 구성될 수 있으며 해당 경우 복사·이동이 필요 없음

<details>
<summary>정답 및 해설</summary>

C. 같은 타입 prvalue 반환 등 일부 경우에는 직접 구성이 보장됩니다. 지역 변수 이름을 반환하는 NRVO는 별개의, 보장되지 않는 경우입니다.

</details>

**10.** `std::move_if_noexcept()`가 복사를 선택할 수 있는 조건을 설명하세요.

<details>
<summary>정답 및 해설</summary>

이동 생성자가 예외를 던질 수 있고 복사가 가능한 경우 등에 복사를 선택할 수 있습니다. 복사가 불가능한 이동 전용 타입까지 항상 복사를 선택하는 것은 아닙니다.

</details>

**11.** 임시 벡터에 검증 후 `swap`하여 최종 갱신할 때 목표하는 예외 보장은 무엇입니까?

- A. Strong Guarantee
- B. 오류 발생 즉시 모든 파일 자동 복구
- C. 메모리 사용량 항상 0

<details>
<summary>정답 및 해설</summary>

A. 갱신 전 모든 처리를 임시 상태에서 수행하고 비예외 교환으로 확정하면 실패 시 원래 상태를 보존할 수 있습니다.

</details>

**12.** `std::span`이 `std::vector`의 재할당 이후 안전하지 않을 수 있는 이유를 설명하세요.

<details>
<summary>정답 및 해설</summary>

span은 원소 메모리를 소유하지 않습니다. vector가 용량을 늘리며 새 저장 공간으로 재할당하면 원래 메모리에 대한 관찰이 무효화될 수 있습니다.

</details>

### Summary

- **Lifetime:** 객체를 사용할 수 있는 기간과 이름의 유효 범위는 구분합니다.
- **RAII:** 자원 관리 객체의 소멸자에 해제 책임을 연결합니다.
- **Ownership:** 읽기·수정·소유권 이전을 함수 인터페이스에서 명시합니다.
- **Smart Pointer:** 독점 소유는 `unique_ptr`, 반드시 필요한 공유 소유는 `shared_ptr`, 비소유 관찰은 `weak_ptr`입니다.
- **Move:** `std::move()`는 이동 후보 표현식을 만들며 실제 이동 동작은 타입이 결정합니다.
- **Rule of Zero/Five:** 자동 관리 타입을 우선 사용하고 직접 소유 규칙을 만들 때만 특별 멤버를 설계합니다.
- **Exception Safety:** 실패 시 기존 상태를 유지하려면 임시 결과를 완성하고 마지막에 상태를 확정합니다.
- **Borrowing:** `std::span`, `std::string_view`, 참조·포인터가 소유자보다 오래 살아남지 않도록 합니다.

### References

- [C++ Core Guidelines — Resource Management](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource)
- [cppreference — `std::unique_ptr`](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [cppreference — `std::shared_ptr`](https://en.cppreference.com/w/cpp/memory/shared_ptr)
- [cppreference — `std::move`](https://en.cppreference.com/w/cpp/utility/move)
- [cppreference — Copy elision](https://en.cppreference.com/w/cpp/language/copy_elision)
- [cppreference — `std::move_if_noexcept`](https://en.cppreference.com/w/cpp/utility/move_if_noexcept)
- [cppreference — `std::expected` (C++23 참고)](https://en.cppreference.com/w/cpp/utility/expected)

[← C++ 목차](../README.md#contents) · [이전 Chapter — File I/O](../Chapter-11/)
