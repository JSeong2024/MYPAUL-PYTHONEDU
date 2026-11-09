# Chapter 17. Testing, Debugging & Profiling

C++20을 기준으로 **오류를 재현하고 원인을 찾은 뒤, 자동 테스트로 재발을 막는 개발 과정**을 학습합니다. 단위·통합 테스트, CMake/CTest, GDB·LLDB, Sanitizer, 성능 프로파일링을 실제 C++ 프로젝트와 연결합니다. Chapter 14의 동시성, Chapter 15의 성능 측정, Chapter 16의 빌드 시스템을 활용합니다.

- **기준 표준:** C++20 (ISO/IEC 14882:2020)
- **개발 환경:** GCC 14 또는 Clang 17, CMake 3.21+, Python 3 (표준 라이브러리)
- **권장 사전 학습:** [Chapter 12](../Chapter-12/) · [Chapter 14](../Chapter-14/) · [Chapter 15](../Chapter-15/) · [Chapter 16](../Chapter-16/)
- **자료 구성:** 예제 16개, Coding Practice 4문제, Basic·Advanced·Pro 프로젝트, 자동 검증 스크립트

**학습 목표:** 테스트가 통과했다는 사실을 넘어, *무엇을 검사했으며 무엇을 아직 검증하지 않았는지* 설명할 수 있도록 하는 것.

## Contents

| Section | Topic |
|:---:|---|
| [17.1](#section-17-1) | Software Quality와 테스트 전략 |
| [17.2](#section-17-2) | 단위 테스트와 명시적 실패 처리 |
| [17.3](#section-17-3) | 경계값·오류 입력 검증 |
| [17.4](#section-17-4) | 의존성 주입과 Test Double |
| [17.5](#section-17-5) | 결정론적 테스트 |
| [17.6](#section-17-6) | Parameterized Test |
| [17.7](#section-17-7) | 불변식과 속성 기반 테스트 |
| [17.8](#section-17-8) | 회귀 테스트와 결함 수정 |
| [17.9](#section-17-9) | 예외·오류 반환 계약 |
| [17.10](#section-17-10) | CMake와 CTest 통합 |
| [17.11](#section-17-11) | Debug Build와 GDB·LLDB |
| [17.12](#section-17-12) | AddressSanitizer |
| [17.13](#section-17-13) | UndefinedBehaviorSanitizer |
| [17.14](#section-17-14) | ThreadSanitizer와 Race |
| [17.15](#section-17-15) | `steady_clock`을 사용한 시간 측정 |
| [17.16](#section-17-16) | Benchmark 설계 |
| [17.17](#section-17-17) | Profiling과 병목 분석 |
| [17.18](#section-17-18) | CI와 품질 게이트 |
| [17.19](#section-17-19) | Coding Practice |
| [17.20](#section-17-20) | Basic Mini Project — Device Validator |
| [17.21](#section-17-21) | Advanced Project — Event Audit |
| [17.22](#section-17-22) | Pro Project — QualityGate SDK |
| [17.23](#section-17-23) | Quiz & Summary |

---

## Getting Started

먼저 `Chapter-17/` 폴더에서 실행합니다. Python 자동 검증 스크립트는 외부 Python 패키지를 요구하지 않습니다.

**GCC**

```bash
g++-14 -std=c++20 -Wall -Wextra -Wpedantic -pthread examples/01_explicit_checks.cpp -o example
./example
python3 tests/check.py --compiler g++-14
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic -pthread examples/01_explicit_checks.cpp -o example
./example
python3 tests/check.py --compiler clang++
```

**MSVC — Developer Command Prompt (예제 실행)**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_explicit_checks.cpp /Fe:example.exe
example.exe
```

MSVC는 환경별 라이브러리와 디버거 구성이 다르므로 실제 컴파일 검증 대상에는 포함하지 않았습니다. Windows에서는 출력 실행 파일 이름과 경로를 적절히 변경합니다.

프로젝트 전체 빌드는 CMake로 수행합니다. `tests/check.py`는 기본적으로 **예제·모범답안**을 검사하며, 학생용 TODO 파일은 검증 대상이 아닙니다.

---

<a id="section-17-1"></a>

## 17.1. Software Quality와 테스트 전략

소프트웨어 검증은 코드의 모든 결함이 없음을 증명하는 작업이 아니라, 명시한 **동작 계약을 깨는 사례를 발견**하는 작업입니다. 성능이 빠른 구현이라도 잘못된 결과를 만들면 성공으로 취급할 수 없습니다.

| 검사 구분 | 질문 | 실습 대상 |
|---|---|---|
| 단위 테스트(Unit Test) | 작은 함수가 정확하게 동작하는가? | `parse_count()`, `is_valid()` |
| 통합 테스트(Integration Test) | 파일·라이브러리·컴포넌트가 함께 동작하는가? | Advanced CSV 처리 |
| 회귀 테스트(Regression Test) | 수정한 결함이 다시 나타나지 않는가? | 빈 목록 처리 |
| 시스템 검증 | 실제 실행 파일이 입력·출력 규격을 지키는가? | CTest CLI 실행 |
| 성능 검증 | 결과를 보존하면서 실제로 개선했는가? | Pro Benchmark |

검증은 정상 입력만 확인하지 않습니다. **정상·경계·오류·반복·복수 실행** 사례를 구분하고, 어떤 입력을 검사했는지 기록해야 합니다. 테스트가 많다는 이유만으로 검증 범위가 충분하다고 단정할 수 없습니다.

---

---

<a id="section-17-2"></a>

## 17.2. 단위 테스트와 명시적 실패 처리

단위 테스트는 범위가 작은 로직을 독립적으로 검증합니다. `if (!조건) throw std::runtime_error(...)`처럼 실패를 명확히 표현하면 Release 빌드에서도 검사가 남아 있습니다.

`assert()`는 개발 중 조건 확인에 도움이 되지만, **`NDEBUG`가 정의된 빌드에서는 비활성화될 수 있기 때문에** 자동 테스트의 필수 검증에만 의존하지 않습니다.

**예제 코드 — [`01_explicit_checks.cpp`](./examples/01_explicit_checks.cpp)**

```cpp
#include <iostream>
#include <stdexcept>
int clamp_reading(int value) {
    if (value < 0 || value > 100) throw std::invalid_argument("out of range");
    return value;
}
void expect(bool condition, const char* description) {
    if (!condition) throw std::runtime_error(description);
}
int main() {
    expect(clamp_reading(0) == 0, "lower boundary");
    expect(clamp_reading(100) == 100, "upper boundary");
    std::cout << "PASS: 2 checks\n";
}
```

**실행 결과**

```text
PASS: 2 checks
```

이 예제는 0과 100 두 경계값을 확인합니다. 오류 입력에 대한 별도 케이스는 다음 Section에서 추가합니다.

---

<a id="section-17-3"></a>

## 17.3. 경계값·오류 입력 검증

입력 규격이 `0 ≤ x ≤ 100`이면 `0`, `100`만 아니라 `-1`, `101`도 시험해야 합니다. 경계 바로 바깥의 값이 가장 간단하면서도 유효한 오류 사례가 될 수 있습니다.

**검사 조합:** 최소 바로 아래 · 최소 · 최소 바로 위 · 최대 바로 아래 · 최대 · 최대 바로 위.

**예제 코드 — [`02_boundary_tests.cpp`](./examples/02_boundary_tests.cpp)**

```cpp
#include <array>
#include <iostream>
#include <stdexcept>
bool valid_percent(int value) noexcept { return value >= 0 && value <= 100; }
int main() {
    struct Case { int input; bool expected; };
    const std::array cases{Case{-1,false}, Case{0,true}, Case{1,true},
                           Case{99,true}, Case{100,true}, Case{101,false}};
    for (const auto& c: cases) {
        if (valid_percent(c.input) != c.expected) throw std::runtime_error("boundary");
    }
    std::cout << "PASS: 6 boundaries\n";
}
```

**실행 결과**

```text
PASS: 6 boundaries
```

정상 처리한 사례 개수만 보는 대신 각 사례의 기대 참·거짓을 함께 검사합니다.

---

<a id="section-17-4"></a>

## 17.4. 의존성 주입과 Test Double

실제 센서, 파일 또는 서버를 테스트마다 호출하면 결과가 환경에 좌우될 수 있습니다. **의존성 주입(Dependency Injection)** 으로 읽기 동작을 분리하면 테스트에서는 고정값을 반환하는 **가짜 구현(Fake)** 을 전달할 수 있습니다.

Mock은 기대 호출 횟수와 인수를 확인하는 방식 등에 사용합니다. 이 자료에서는 별도 Mocking 라이브러리 없이 Fake 객체만 사용합니다.

**예제 코드 — [`03_test_double.cpp`](./examples/03_test_double.cpp)**

```cpp
#include <iostream>
#include <stdexcept>
struct Source { virtual ~Source() = default; virtual int read() = 0; };
struct FakeSource final : Source { int read() override { return 85; } };
bool is_alert(Source& source) { return source.read() >= 80; }
int main() {
    FakeSource fake;
    if (!is_alert(fake)) throw std::runtime_error("fake input");
    std::cout << "Alert: true\n";
}
```

**실행 결과**

```text
Alert: true
```

`is_alert()`는 실제 하드웨어 없이 동작 계약을 검증할 수 있습니다.

---

<a id="section-17-5"></a>

## 17.5. 결정론적 테스트

현재 시간이나 난수에 직접 의존하는 테스트는 일관되지 않게 실패할 수 있습니다. 시간을 제공하는 인터페이스를 주입하면 시간 경계값도 반복해서 검증할 수 있습니다.

**예제 코드 — [`04_deterministic_dependency.cpp`](./examples/04_deterministic_dependency.cpp)**

```cpp
#include <iostream>
#include <stdexcept>
struct Clock { virtual ~Clock() = default; virtual int tick() const = 0; };
struct FixedClock final : Clock { int tick() const override { return 120; } };
bool expired(const Clock& clock,int deadline) { return clock.tick() >= deadline; }
int main() {
    FixedClock clock;
    if (!expired(clock,100) || expired(clock,130)) throw std::runtime_error("clock");
    std::cout << "Clock tests: PASS\n";
}
```

**실행 결과**

```text
Clock tests: PASS
```

동일한 Fake Clock을 사용하므로 실행 환경의 실제 시각과 무관하게 결과가 재현됩니다.

---

<a id="section-17-6"></a>

## 17.6. Parameterized Test

같은 함수를 여러 입력·기대 결과 조합으로 검증하는 방식입니다. 반복되는 테스트 코드를 줄일 수 있지만, **서로 다른 입력에 같은 잘못된 결과를 기대하는 오류**가 없는지도 검토해야 합니다.

**예제 코드 — [`05_parameterized_tests.cpp`](./examples/05_parameterized_tests.cpp)**

```cpp
#include <array>
#include <iostream>
#include <stdexcept>
int shipping(int weight) {
    if (weight <= 0) throw std::invalid_argument("weight");
    return 2000 + (weight-1)/500 * 500;
}
int main() {
    struct Case {int weight; int price;};
    constexpr std::array samples{Case{1,2000},Case{500,2000},Case{501,2500},Case{1000,2500}};
    for (auto c: samples) if(shipping(c.weight)!=c.price) throw std::runtime_error("case");
    std::cout << "Shipping cases: 4\n";
}
```

**실행 결과**

```text
Shipping cases: 4
```

`500g` 경계값과 `501g`의 차이를 명확하게 검증합니다. 문제의 가격 정책은 이 예제에서 정의한 규칙입니다.

---

<a id="section-17-7"></a>

## 17.7. 불변식과 속성 기반 테스트

반환값 하나보다 여러 입력에서 항상 성립해야 하는 **불변식(Invariant)** 을 검증할 수도 있습니다. 예를 들어 정렬은 원소의 총합과 개수를 바꾸지 않으며 출력은 정렬되어야 합니다.

**예제 코드 — [`06_invariant_tests.cpp`](./examples/06_invariant_tests.cpp)**

```cpp
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <stdexcept>
int main() {
    std::array values{9,2,5,2,7};
    const auto sum=std::accumulate(values.begin(),values.end(),0);
    std::sort(values.begin(),values.end());
    if(sum!=std::accumulate(values.begin(),values.end(),0) ||
       !std::is_sorted(values.begin(),values.end())) throw std::runtime_error("invariant");
    std::cout << "Invariant: preserved\n";
}
```

**실행 결과**

```text
Invariant: preserved
```

Pro 프로젝트에서는 고정 시드로 만든 1,200개의 측정값을 검증하고, 입력 순서를 반대로 바꿔도 집계 결과가 같은지 확인합니다. 이 방식은 다양한 입력을 점검하지만 모든 경우를 증명하지는 않습니다.

---

<a id="section-17-8"></a>

## 17.8. 회귀 테스트와 결함 수정

기존에 실패했던 입력을 테스트에 남기는 것이 회귀 테스트의 핵심입니다. 예를 들어 빈 Container에서 `.back()`을 호출하면 정의되지 않은 동작을 일으킬 수 있으므로, 빈 입력을 먼저 확인합니다.

**결함 수정 순서:** 실패하는 테스트 작성 → 원인 재현 → 수정 → 전체 테스트 실행 → 동일 사례 유지.

**예제 코드 — [`07_regression_test.cpp`](./examples/07_regression_test.cpp)**

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>
int last_or_zero(const std::vector<int>& data) {
    return data.empty() ? 0 : data.back();
}
int main() {
    if(last_or_zero({})!=0 || last_or_zero({4,7})!=7) throw std::runtime_error("regression");
    std::cout << "Regression: PASS\n";
}
```

**실행 결과**

```text
Regression: PASS
```

결함의 증상만 가리는 대신 입력 계약을 문서화해야 합니다.

---

<a id="section-17-9"></a>

## 17.9. 예외·오류 반환 계약

테스트에서는 정상 출력뿐 아니라 예외의 **종류**, 반환 상태, 원본 데이터 보존을 확인해야 합니다. 예외를 잡기만 하고 예상한 예외인지 검사하지 않으면 잘못된 오류를 놓칠 수 있습니다.

**예제 코드 — [`08_exception_tests.cpp`](./examples/08_exception_tests.cpp)**

```cpp
#include <iostream>
#include <stdexcept>
int parse_port(int port) {
    if (port < 1 || port > 65535) throw std::out_of_range("port");
    return port;
}
int main() {
    bool caught=false;
    try { (void)parse_port(0); }
    catch(const std::out_of_range&) { caught=true; }
    if (!caught || parse_port(8080)!=8080) throw std::runtime_error("error contract");
    std::cout << "Error contract: PASS\n";
}
```

**실행 결과**

```text
Error contract: PASS
```

`std::out_of_range` 발생 여부와 정상 값 반환을 함께 확인합니다.

---

<a id="section-17-10"></a>

## 17.10. CMake와 CTest 통합

Chapter 16에서 만든 CMake Target에 `enable_testing()` 또는 `include(CTest)`를 적용하면 명령줄에서 테스트를 실행할 수 있습니다. **테스트의 성공 여부는 프로세스 종료 코드**를 기준으로 판단하며, 필요하면 `PASS_REGULAR_EXPRESSION`을 추가합니다.

```cmake
include(CTest)
if(BUILD_TESTING)
  add_executable(unit_tests tests/device_tests.cpp)
  target_link_libraries(unit_tests PRIVATE device_core)
  add_test(NAME device_unit COMMAND unit_tests)
endif()
```

```bash
cmake -S examples/17_device_validator -B build-device -DCMAKE_BUILD_TYPE=Debug
cmake --build build-device
ctest --test-dir build-device --output-on-failure --no-tests=error
```

**예제 코드 — [`09_ctest_exit_status.cpp`](./examples/09_ctest_exit_status.cpp)**

```cpp
#include <iostream>
#include <string_view>
int main(int argc,char** argv) {
    if(argc>1 && std::string_view{argv[1]}=="--self-test") {
        const int actual=2+3;
        if(actual!=5) return 1;
        std::cout << "Self-test: PASS\n";
        return 0;
    }
    std::cout << "Use --self-test\n";
}
```

**실행 결과**

```text
Use --self-test
```

`./실행파일 --self-test`로 실행하면 `Self-test: PASS`를 출력합니다. 일반 CTest에서는 별도 테스트 Target을 사용합니다.

---

<a id="section-17-11"></a>

## 17.11. Debug Build와 GDB·LLDB

디버깅에서는 프로그램을 중단해 **호출 스택(Call Stack), 지역 변수, 분기 조건**을 확인합니다. GCC·Clang에서 `-g -O0`는 소스 수준 탐색을 수월하게 하지만 배포 성능과 실행 순서가 같다고 보장하지는 않습니다.

```bash
g++-14 -std=c++20 -g -O0 examples/10_debugger_repro.cpp -o debug_sample
gdb --args ./debug_sample
# GDB 안에서: break sum_positive / run / next / print total / backtrace
```

LLDB는 `lldb ./debug_sample`, `breakpoint set --name sum_positive`, `frame variable`, `bt` 등을 사용합니다. 자세한 절차는 [Debugging 실습 문서](./docs/DEBUGGING.md)에 정리했습니다.

**예제 코드 — [`10_debugger_repro.cpp`](./examples/10_debugger_repro.cpp)**

```cpp
#include <array>
#include <iostream>
#include <stdexcept>
int sum_positive(const std::array<int,4>& values) {
    int total=0;
    for(int value:values) if(value>0) total+=value;
    return total;
}
int main() {
    const std::array readings{-3,5,0,7};
    const int total=sum_positive(readings);
    if(total!=12) throw std::runtime_error("sum mismatch");
    std::cout << "Positive sum: " << total << '\n';
}
```

**실행 결과**

```text
Positive sum: 12
```

디버거로 `value>0` 조건의 처리 과정을 살펴보세요.

---

<a id="section-17-12"></a>

## 17.12. AddressSanitizer — 메모리 접근 오류

AddressSanitizer(ASan)는 배열 범위 초과, 해제 후 접근, 잘못된 해제 등 여러 메모리 오류를 탐지합니다. 단, **모든 오류를 발견하는 도구는 아니며** 별도 런타임과 빌드 옵션이 필요합니다.

```bash
clang++ -std=c++20 -O1 -g -fsanitize=address -fno-omit-frame-pointer \
  buglab/01_out_of_bounds.cpp -o bad_asan
./bad_asan
```

`buglab/`은 고의로 결함을 만든 학습 파일이며 자동 테스트 대상이 아닙니다. 오류 메시지를 읽은 후 안전한 구현으로 고쳐 재실행합니다.

**예제 코드 — [`11_address_sanitizer_fix.cpp`](./examples/11_address_sanitizer_fix.cpp)**

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>
int checked_element(const std::vector<int>& values,std::size_t index) {
    return values.at(index);
}
int main() {
    const std::vector readings{10,20,30};
    bool caught=false;
    try { (void)checked_element(readings,3); }
    catch(const std::out_of_range&) { caught=true; }
    if (!caught) throw std::runtime_error("missing bounds check");
    std::cout << "Bounds: handled\n";
}
```

**실행 결과**

```text
Bounds: handled
```

이 예제는 `.at()`과 `std::out_of_range`를 통해 범위 오류를 명시적으로 처리합니다. [Sanitizer 실습](./docs/SANITIZERS.md) 참조.

---

<a id="section-17-13"></a>

## 17.13. UndefinedBehaviorSanitizer — 정의되지 않은 동작

UndefinedBehaviorSanitizer(UBSan)는 부호 있는 정수 오버플로, 잘못된 포인터 접근 등 특정 정의되지 않은 동작을 탐지합니다. 정수 오버플로는 우연히 원하는 숫자가 나왔다고 안전한 코드가 되는 것이 아닙니다.

```bash
clang++ -std=c++20 -O1 -g -fsanitize=undefined \
  -fno-sanitize-recover=undefined buglab/02_signed_overflow.cpp -o bad_ubsan
./bad_ubsan
```

**예제 코드 — [`12_undefined_behavior_fix.cpp`](./examples/12_undefined_behavior_fix.cpp)**

```cpp
#include <iostream>
#include <limits>
#include <optional>
std::optional<int> checked_add(int a,int b) {
    if ((b>0 && a>std::numeric_limits<int>::max()-b) ||
        (b<0 && a<std::numeric_limits<int>::min()-b)) return std::nullopt;
    return a+b;
}
int main() {
    const auto safe=checked_add(10,20);
    const auto invalid=checked_add(std::numeric_limits<int>::max(),1);
    if(!safe || *safe!=30 || invalid) return 1;
    std::cout << "Overflow: rejected\n";
}
```

**실행 결과**

```text
Overflow: rejected
```

안전한 구현은 정수 범위를 **연산 전에** 검사합니다. `std::numeric_limits<int>`는 플랫폼의 `int` 크기를 고려합니다.

---

<a id="section-17-14"></a>

## 17.14. ThreadSanitizer와 Data Race

두 스레드가 같은 메모리에 접근하고 그중 하나 이상이 쓰기를 수행하면서 적절한 동기화가 없으면 **Data Race**가 생길 수 있습니다. 단순히 실행할 때마다 결과가 같았다는 이유로 안전하다고 판단할 수 없습니다.

ThreadSanitizer(TSan)는 Data Race 검출에 사용하지만 환경·런타임 의존성이 큽니다. 특히 **ASan과 TSan을 동시에 켜지 않습니다.** CI의 필수 경로에는 안정적인 동기화 구현을 넣고, TSan은 지원되는 환경에서 별도로 실행합니다.

**예제 코드 — [`13_thread_sanitizer_fix.cpp`](./examples/13_thread_sanitizer_fix.cpp)**

```cpp
#include <iostream>
#include <mutex>
#include <thread>
int main() {
    int counter=0;
    std::mutex guard;
    auto worker=[&]{for(int i=0;i<1000;++i){std::lock_guard lock{guard};++counter;}};
    std::thread a{worker}, b{worker};
    a.join();b.join();
    if(counter!=2000)return 1;
    std::cout << "Counter: " << counter << '\n';
}
```

**실행 결과**

```text
Counter: 2000
```

`std::lock_guard`를 사용해 공유 카운터를 보호합니다. 성능이 중요한 경우 Atomic으로 대체할 수 있는지도 별도의 계약 검토가 필요합니다.

---

<a id="section-17-15"></a>

## 17.15. `steady_clock`을 사용한 시간 측정

소요 시간은 시스템 시각이 변경되어도 뒤로 가지 않는 `std::chrono::steady_clock`으로 측정합니다. 출력한 한 번의 경과 시간은 **측정 환경에 종속**됩니다. 짧은 함수는 시스템 잡음의 영향이 커서 여러 번 측정해야 합니다.

**예제 코드 — [`14_steady_clock.cpp`](./examples/14_steady_clock.cpp)**

```cpp
#include <chrono>
#include <iostream>
#include <stdexcept>
int main() {
    const auto started=std::chrono::steady_clock::now();
    volatile int marker=0;
    (void)marker;
    const auto elapsed=std::chrono::steady_clock::now()-started;
    if(elapsed<decltype(elapsed)::zero())throw std::runtime_error("timer");
    std::cout << "Timer: monotonic\n"; // 실제 시간은 출력하지 않음
}
```

**실행 결과**

```text
Timer: monotonic
```

실제 경과 시간을 정답 문자열로 고정하지 않고, 시간 값이 음수가 아니라는 기본 성질을 확인합니다.

---

<a id="section-17-16"></a>

## 17.16. Benchmark 설계

Benchmark는 최적화 대상의 실행 비용을 반복 측정하는 작업입니다. 성능 비교 전에 먼저 두 구현의 **출력 결과가 같은지** 검사합니다.

- **빌드:** Release 모드의 컴파일 옵션을 동일하게 유지
- **입력:** 데이터 크기와 분포를 고정
- **워밍업:** 초기 할당·캐시 영향을 구별
- **반복:** 여러 번 측정하고 분산 확인
- **결과 활용:** 계산 결과를 실제로 사용해 불필요한 코드 제거 가능성을 낮춤

**예제 코드 — [`15_benchmark_checks.cpp`](./examples/15_benchmark_checks.cpp)**

```cpp
#include <chrono>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
int main() {
    const std::vector values(1000,3);
    const auto begin=std::chrono::steady_clock::now();
    const int total=std::accumulate(values.begin(),values.end(),0);
    const auto elapsed=std::chrono::steady_clock::now()-begin;
    if(total!=3000 || elapsed<decltype(elapsed)::zero())throw std::runtime_error("benchmark");
    std::cout << "Result: 3000\n"; // 측정 시간은 환경에 따라 다름
}
```

**실행 결과**

```text
Result: 3000
```

예제는 연산 결과를 검증하지만 이것만으로 정밀 Benchmark가 완성되는 것은 아닙니다. 상세 측정은 [Profiling 문서](./docs/PROFILING.md)를 따릅니다.

---

<a id="section-17-17"></a>

## 17.17. Profiling과 병목 분석

Benchmark가 *얼마나 오래 걸렸는지* 측정한다면, Profiling은 *어디에서 비용이 발생했는지* 찾는 데 사용됩니다. 실제 병목을 확인하지 않고 자료구조를 변경하면 코드만 복잡해질 수 있습니다.

```bash
# Linux에서 perf가 설치되어 있고 권한이 허용되는 경우
perf stat ./build-release/quality_gate_bench 1000000
perf record -g -- ./build-release/quality_gate_bench 1000000
perf report
```

`perf`는 환경에 따라 설치·권한 설정이 필요합니다. Windows에서는 Visual Studio Profiler 등 플랫폼별 도구를 고려합니다.

**예제 코드 — [`16_profiling_baseline.cpp`](./examples/16_profiling_baseline.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
int main() {
    std::vector<std::string> ids{"D3","D1","D2","D1"};
    std::sort(ids.begin(),ids.end());
    const auto matches=std::count(ids.begin(),ids.end(),"D1");
    if(matches!=2)throw std::runtime_error("baseline");
    std::cout << "Matches: " << matches << '\n';
}
```

**실행 결과**

```text
Matches: 2
```

측정할 연산과 기대 결과를 먼저 정의해, 프로파일링 이후 수정이 정확성을 깨지 않았는지 확인합니다.

---

<a id="section-17-18"></a>

## 17.18. CI와 품질 게이트

자동화된 검증은 사람이 실행한 환경에서만 확인되는 문제를 줄여줍니다. 다만 테스트 스크립트의 품질과 CI 실행 환경에 따라 확인할 수 있는 범위가 달라집니다.

**권장 품질 게이트**

1. GCC와 Clang에서 C++20 컴파일 및 경고 확인
2. 정상·경계·오류 입력에 대한 기능 테스트
3. CMake·CTest 및 실제 CLI 통합 테스트
4. 의존 패키지 설치·이동 후 외부 소비자 재빌드(Pro)
5. 로컬 Sanitizer 검사 및 문제 재현 문서화
6. 성능 측정은 별도 작업으로 관리(공유 CI의 절대 시간 기준 남용 금지)

`NDEBUG`가 정의되는 Release에서도 기능 검증이 사라지지 않도록 테스트에는 명시적 오류를 사용합니다. 학생용 미완성 코드와 의도적으로 오류가 있는 `buglab/` 코드는 기본 CI에서 제외합니다.

실제 검증 정책과 명령어는 [CI_WORKFLOW.md](./docs/CI_WORKFLOW.md)를 참고하세요.

---

---

<a id="section-17-19"></a>

## 17.19. Coding Practice

다음 네 문제는 [학생용 코드](./exercises/)의 TODO를 구현하는 실습입니다. 완성 전에는 테스트가 실패하는 것이 정상입니다. 코드를 수정한 뒤 해당 검증 스크립트를 실행합니다.

| 실습 | 요구사항 | 주요 검증 |
|---|---|---|
| [① Strict Parser](./exercises/01_strict_parser.cpp) | 전체 문자열이 0 이상의 정수인지 검사 | 빈 문자열, 공백, 범위 초과, 부호 |
| [② Batch Total](./exercises/02_batch_total.cpp) | 0~100 값만 합산 | 빈 목록, 범위 초과, 정확한 합계 |
| [③ Rolling Max](./exercises/03_rolling_max.cpp) | 고정 크기 연속 구간별 최댓값 | 창 크기 0, 1, 전체 길이, 초과 |
| [④ Sensor Fake](./exercises/04_sensor_fake.cpp) | Fake Source에서 경보 개수 집계 | 결측값, 경보 경계, 호출 횟수 |

```bash
# C++ Chapter-17/ 위치에서 실행
python3 tests/check.py --compiler g++-14 --mode student --only exercise-01
# 완성된 모범답안 검증
python3 tests/check.py --compiler g++-14 --mode solutions --only exercise-01
```

<details>
<summary>실습별 구현 힌트</summary>

- **①** `std::from_chars`의 오류 코드와 반환 포인터를 함께 검사합니다.
- **②** 먼저 모든 값의 유효성을 판단한 뒤 합계를 구합니다. 최대 10,000행의 조건을 지킵니다.
- **③** 창 시작 위치를 하나씩 이동하고 `std::max_element`로 구간을 확인할 수 있습니다.
- **④** `ReadingSource::next()`를 사용하여 호출된 만큼만 값을 읽습니다. `std::nullopt`는 결측값입니다.

</details>

<details>
<summary>모범답안 파일 확인</summary>

[실습 ①](./solutions/01_strict_parser.cpp) · [실습 ②](./solutions/02_batch_total.cpp) · [실습 ③](./solutions/03_rolling_max.cpp) · [실습 ④](./solutions/04_sensor_fake.cpp)

</details>

---

---

<a id="section-17-20"></a>

## 17.20. Basic Mini Project — Device Validator

측정값을 받아 유효 범위를 검사하는 프로그램을 작성합니다. Chapter 16의 Target 분리 개념을 그대로 활용해 **라이브러리·CLI·테스트 실행 파일**을 나눕니다.

**문제:** 센서 측정값은 0~100 범위에서만 유효합니다. 여러 개의 측정값을 입력받아 유효한 값의 개수를 반환하는 함수를 만들고, 경계값과 빈 데이터에 대한 테스트를 작성합니다.

**구현 조건**

1. `is_valid(int)`는 범위 안의 값을 `true`로 반환합니다.
2. `count_valid(std::span<const int>)`는 유효한 측정값의 개수를 구합니다.
3. 테스트는 `-1`, `0`, `100`, `101`, 빈 목록을 모두 검사합니다.
4. CMake Target을 `device_core`, `device_demo`, `device_tests`로 분리합니다.

```bash
cmake -S examples/17_device_validator -B build-device -DCMAKE_BUILD_TYPE=Release
cmake --build build-device
ctest --test-dir build-device --output-on-failure
```

**입출력 예시** (`device_demo`)

```text
Valid: 2
```

관련 자료: [`CMakeLists.txt`](./examples/17_device_validator/CMakeLists.txt) · [테스트 코드](./examples/17_device_validator/tests/device_tests.cpp) · [프로젝트 시작 파일](./examples/17_device_validator/)

---

---

<a id="section-17-21"></a>

## 17.21. Advanced Project — Event Audit

### 상황 및 배경

현장의 장치별 재고 변화가 여러 시스템에서 기록되어 있습니다. 로그에는 중복 이벤트, 잘못된 금액, 잔액보다 큰 차감 명령이 포함되어 있어 운영팀이 집계 결과를 신뢰하지 못하고 있습니다.

기록 순서를 보존하여 이벤트를 하나씩 처리하고, 거부된 행이 다른 정상 이벤트의 결과에 영향을 주지 않도록 하는 **감사 프로그램**을 작성하세요. 정상 데이터의 처리 결과와 오류 보고서를 각각 CSV로 저장해야 합니다.

### 구현 조건

1. 헤더 없는 `events.csv`를 읽습니다. 각 행은 `event_id,device_id,ADD|REMOVE,amount` 네 필드입니다. 이 과제에서는 따옴표와 필드 내부 쉼표를 지원하지 않습니다.
2. 이벤트 ID와 장치 ID는 비어 있으면 안 됩니다. 금액은 1~1,000,000의 정수만 허용합니다.
3. 먼저 데이터 형식을 검증한 뒤 중복 ID를 검사합니다. **성공적으로 적용한 이벤트 ID만 중복 목록에 추가**합니다.
4. `REMOVE` 금액이 기존 잔액을 초과하면 `INSUFFICIENT_BALANCE`로 거부합니다. 실패한 이벤트는 잔액을 바꾸지 않습니다.
5. 장치별 잔액은 ID 오름차순으로 `balances.csv`에 기록하고, 오류는 원본 행번호 순서로 `rejected.csv`에 기록합니다.
6. 파일 열기·쓰기 실패를 명시적으로 처리합니다. 파일 간 원자적 교체까지는 요구하지 않습니다.

### INPUT

`events.csv`: 헤더 없는 UTF-8 텍스트. 필드 순서 `event_id,device_id,kind,amount`. 입력 파일은 장치·이벤트 ID에 쉼표가 없는 형식으로 제공됩니다. 총 행 수와 유효 금액 합계가 `long long` 범위에 들어간다고 가정합니다.

### OUTPUT

- `balances.csv`: `device_id,balance` — 장치 ID 오름차순
- `rejected.csv`: `line_number,error_code` — 1부터 시작하는 원본 행 번호 순서
- 표준 출력: 성공·거부 건수 `Accepted: X, Rejected: Y`

### 입출력 예시

**입력** (`data/events.csv`)

```text
e1,D1,ADD,10
e2,D1,REMOVE,3
e2,D1,ADD,20
e3,D2,ADD,6
e4,D1,REMOVE,11
e5,D2,ADD,bad
e6,D2,UNKNOWN,4
```

**정산 결과 (`balances.csv`)**

```text
D1,7
D2,6
```

**거부 결과 (`rejected.csv`)**

```text
3,DUPLICATE_EVENT
5,INSUFFICIENT_BALANCE
6,BAD_AMOUNT
7,UNKNOWN_KIND
```

**표준 출력**

```text
Accepted: 3, Rejected: 4
```

### 구현 가이드

<details><summary>STEP 01 — 검사 순서와 중복 제어</summary>

형식 → 금액 → 이벤트 유형 → 중복 ID → 차감 가능 여부 순으로 검사하세요. `std::set<std::string>` 또는 `std::unordered_set<std::string>`으로 성공한 이벤트 ID를 보관할 수 있습니다.

```cpp
std::set<std::string> applied_ids;
// 이벤트를 완전히 검증하고 적용한 뒤에만 applied_ids.insert(id);
```

</details>

<details><summary>STEP 02 — 결과 비교</summary>

`std::map<std::string, long long>`을 사용하면 장치 ID 오름차순 출력이 간단합니다. 테스트에서는 거부 행의 번호와 코드까지 비교하세요.

</details>

### 검증 사항

- 동일 이벤트 ID가 재등장했을 때 원본 상태 보존
- 불충분한 잔액·잘못된 금액·알 수 없는 유형·빈 필드
- 빈 파일과 정상 입력만 있는 경우
- 동일 파일 재실행 시 결과 완전 일치
- CMake·CTest 및 실행 파일 통합 테스트

[학생용 프로젝트](./projects/advanced_event_audit/) · [모범답안](./solutions/advanced_event_audit/) · [프로젝트 안내](./projects/advanced_event_audit/README.md)

---

---

<a id="section-17-22"></a>

## 17.22. Pro Project — QualityGate SDK

### 의뢰 배경

여러 현장 시스템에서 센서 측정값을 집계하는 라이브러리를 배포하려 합니다. 단순히 한 번 올바른 값을 반환하는 것만으로는 충분하지 않습니다. 새 기능이 추가되거나 컴파일러가 바뀌어도 집계 규칙이 유지되고, 다른 프로젝트가 라이브러리를 설치해 사용할 수 있어야 합니다.

외부 프로젝트에서 재사용할 수 있는 **QualityGate SDK**를 구성하고, 기능·경계값·불변식·배포 가능성에 대한 자동 검증을 마련하세요. 성능 데이터도 수집하되 특정 컴퓨터에서 얻은 시간을 합격 기준으로 고정하지 않습니다.

### 요구사항 및 작업 범위

1. 공개 API `summarize(std::span<const Reading>)`는 장치별 `count`, `total`, `minimum`, `maximum`을 구합니다.
2. `valid=false`인 측정은 제외합니다. `valid=true`인데 장치 ID가 비었거나 값이 0~100 밖이면 `std::invalid_argument`를 발생시킵니다.
3. 출력은 장치 ID 오름차순으로 반환하며, 입력 순서 변경에 따른 집계 결과 변화를 허용하지 않습니다.
4. 단위 테스트에서 빈 입력·경계값·비정상 값·정렬을 검사합니다.
5. 고정 시드의 테스트 데이터를 만들고, **원본과 역순 입력의 집계 결과가 일치**하는지 검사합니다.
6. CTest에서 단위·속성 기반·CLI 테스트를 구분하여 실행합니다.
7. `QualityGateConfig.cmake`와 Export Target을 설치해 외부 프로젝트가 `find_package(QualityGate 1 CONFIG REQUIRED)`로 사용하도록 합니다.
8. SDK를 설치한 폴더를 다른 경로로 옮긴 뒤에도 소비자 프로젝트를 빌드해야 합니다.
9. 별도 `quality_gate_bench`를 실행해 측정 데이터를 기록합니다. `checksum`을 통해 측정 중 결과가 사라지지 않도록 합니다.
10. GCC·Clang의 지원되는 환경에서 선택적으로 ASan/UBSan 검증을 수행합니다. 실패 시 실제 결함과 도구 환경 문제를 구분합니다.

### 입력 및 출력

**입력 — C++ API**

```cpp
struct Reading {
    std::string device;
    int value{};
    bool valid{true};
};
```

**출력 — C++ API**

```cpp
struct Summary {
    std::string device;
    std::size_t count{};
    std::int64_t total{};
    int minimum{};
    int maximum{};
};
```

**실행 예시 (`quality_gate_cli`)**

```text
Devices: 2
D1,1,10
D2,2,70
```

### 구현 가이드

<details><summary>STEP 01 — 참조 결과와 불변식</summary>

먼저 `std::map<std::string, Summary>`으로 정확한 집계를 구현하세요. `valid=false`는 건너뛰고, 유효 측정값만 검사합니다.

</details>

<details><summary>STEP 02 — 패키지·검증</summary>

CMake의 Build Interface와 Install Interface를 구분하고, `install(EXPORT ...)`를 사용해 공개 Target을 제공합니다. 외부 소비자 CMake 프로젝트는 별도 빌드 디렉터리를 사용합니다.

</details>

### 납품 항목

- `quality_gate` 라이브러리 및 공개 헤더
- CLI, Benchmark, CTest 테스트 코드
- 설치 가능한 CMake 패키지 및 소비자 프로젝트
- 테스트 결과와 재현 가능한 빌드 명령어
- 오류·경계값 및 성능 측정 기록

### 검증 사항

- 정상·오류 입력에 대한 정확성
- 입력 재배열과 집계 결과의 불변성
- CMake Release 빌드에서도 테스트가 수행되는지
- SDK 설치·경로 이동·외부 프로젝트 빌드
- Sanitizer 지원 환경에서의 결함 유무와 측정 재현성

```bash
cmake -S solutions/pro_quality_gate -B build-pro -DCMAKE_BUILD_TYPE=Release
cmake --build build-pro --parallel 2
ctest --test-dir build-pro --output-on-failure
./build-pro/quality_gate_bench 100000
```

학생용 파일은 [`projects/pro_quality_gate/`](./projects/pro_quality_gate/)에서, 모범답안은 [`solutions/pro_quality_gate/`](./solutions/pro_quality_gate/)에서 확인할 수 있습니다. 상세 실행 명령은 각 프로젝트의 README를 참고하세요.

---

---

<a id="section-17-23"></a>

## 17.23. Quiz & Summary

**Quiz**

각 문항의 답을 먼저 생각한 다음 해설을 확인하세요.

**Q-01.** Release 빌드에서 `assert()`만으로 필수 테스트를 구성하면 안 되는 이유는?

<details><summary>정답 및 해설</summary>

`NDEBUG`가 정의된 빌드에서 `assert`가 비활성화될 수 있기 때문입니다. 반드시 확인할 조건은 실패 시 종료 코드가 바뀌는 검사를 사용합니다.

</details>

**Q-02.** 단위 테스트에서 실제 서버 대신 Fake 객체를 전달하는 주된 이유는?

<details><summary>정답 및 해설</summary>

외부 환경을 통제하여 동일한 입력과 결과를 반복해서 검증하기 위해서입니다.

</details>

**Q-03.** 유효 범위가 0~100일 때 최소한 점검할 대표 경계값은?

<details><summary>정답 및 해설</summary>

-1, 0, 1, 99, 100, 101 등 경계의 안팎입니다.

</details>

**Q-04.** 회귀 테스트는 버그를 수정한 후 왜 유지해야 합니까?

<details><summary>정답 및 해설</summary>

동일한 입력에서 그 버그가 다시 발생하지 않는지 후속 변경마다 검사하기 위해서입니다.

</details>

**Q-05.** CTest는 실행 파일의 성공 여부를 기본적으로 무엇으로 판단합니까?

<details><summary>정답 및 해설</summary>

프로세스 종료 코드입니다. 0이 일반적으로 성공이며, CTest 설정으로 추가 조건을 둘 수 있습니다.

</details>

**Q-06.** GDB에서 함수 호출 경로를 살펴보려면 어떤 명령어를 사용합니까?

<details><summary>정답 및 해설</summary>

`backtrace` 또는 `bt`입니다.

</details>

**Q-07.** ASan은 어떤 범주의 오류를 찾는 데 유용합니까?

<details><summary>정답 및 해설</summary>

힙·스택 경계 초과, 해제 후 접근 등 메모리 접근 오류입니다. 모든 결함을 찾는 것은 아닙니다.

</details>

**Q-08.** UBSan에서 탐지할 수 있는 대표적인 정수 관련 오류는 무엇입니까?

<details><summary>정답 및 해설</summary>

부호 있는 정수 오버플로입니다.

</details>

**Q-09.** 멀티스레드 프로그램이 매번 같은 값을 출력하면 Data Race가 없다고 결론 내릴 수 있습니까?

<details><summary>정답 및 해설</summary>

아니요. 테스트 실행에서 문제가 관찰되지 않았다는 사실만으로 동기화가 안전하다는 것을 증명할 수 없습니다.

</details>

**Q-10.** 성능 측정에 `steady_clock`을 사용하는 이유는?

<details><summary>정답 및 해설</summary>

시스템 시각 조정으로 측정 시간이 뒤로 가는 문제를 피하기 위한 단조 시계이기 때문입니다.

</details>

**Q-11.** Profiling과 Benchmark의 핵심 차이는 무엇입니까?

<details><summary>정답 및 해설</summary>

Benchmark는 실행 비용을 비교하고, Profiling은 비용이 발생하는 위치를 찾습니다.

</details>

**Q-12.** Pro SDK 검증에서 설치 폴더를 이동한 다음 소비자를 다시 빌드하는 이유는?

<details><summary>정답 및 해설</summary>

설치한 라이브러리가 개발자의 원래 소스·빌드 경로에 의존하지 않고 재사용 가능한지 확인하기 위해서입니다.

</details>

### Summary

- 테스트는 **기대 결과, 오류 계약, 경계값**을 명시하는 과정입니다.
- 입력 환경을 통제하고, 결함을 재현할 수 있는 최소 조건을 확보합니다.
- 디버깅으로 원인을 찾고, Sanitizer로 일부 런타임 오류를 탐지합니다.
- 성능 측정 전에는 결과 정확성을 먼저 확인하고, 수치는 동일 환경에서 비교합니다.
- CI에서는 예제·모범답안·CMake·CTest를 반복 검증하고, 학생용 TODO와 의도적인 결함 파일은 분리합니다.

### References

- [CMake — Testing With CTest](https://cmake.org/cmake/help/latest/manual/ctest.1.html)
- [CMake — add_test()](https://cmake.org/cmake/help/latest/command/add_test.html)
- [Clang — AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)
- [Clang — UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)
- [Clang — ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html)
- [GNU GDB — Debugging with GDB](https://sourceware.org/gdb/documentation/)

---

[← C++ 목차](../README.md) · [Chapter 16 — CMake, Libraries & Project Structure](../Chapter-16/)

