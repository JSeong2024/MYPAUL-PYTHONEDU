# Chapter 14. Concurrency & Multithreading

여러 작업이 동시에 진행되는 프로그램에서 **공유 데이터의 일관성, 작업 종료, 오류 전달**을 안전하게 다루는 방법을 학습합니다. `std::thread`의 수명 관리부터 C++20의 `std::jthread`, 동기화 객체, 원자 연산과 메모리 순서를 거쳐 작업 큐를 사용하는 Mini Project까지 연결합니다.

**기준 표준:** C++20 (ISO/IEC 14882:2020)  
**개발 환경:** GCC, Clang, MSVC  
**실행 조건:** C++20 스레드 라이브러리를 지원하는 컴파일러 및 운영체제. GCC·Clang에서는 `-pthread` 사용

<details>
<summary>선행 학습</summary>

- [Chapter 05. Functions](../Chapter-05/README.md) — 함수 객체와 람다
- [Chapter 07. Pointers & References](../Chapter-07/README.md) — 참조와 객체 수명
- [Chapter 08. Structs & Classes](../Chapter-08/README.md) — 상태와 캡슐화
- [Chapter 10. Standard Library (STL)](../Chapter-10/README.md) — 컨테이너와 알고리즘
- [Chapter 12. Modern C++ & Resource Management](../Chapter-12/README.md) — RAII, Ownership, 예외 안전성
- [Chapter 13. Templates & Generic Programming](../Chapter-13/README.md) — 타입 계약과 범용 설계

</details>

## Contents

| Section | Topic |
|:---:|---|
| [14.1](#section-14-1) | Concurrency와 Parallelism — 실행 순서와 공유 상태 |
| [14.2](#section-14-2) | `std::thread` — 생성, `join`과 수명 |
| [14.3](#section-14-3) | `std::jthread`와 `std::stop_token` — 협력적 종료 |
| [14.4](#section-14-4) | Data Race와 Happens-Before — 무엇이 정의되지 않은 동작인가 |
| [14.5](#section-14-5) | `std::mutex`와 `std::lock_guard` — 불변 조건 보호 |
| [14.6](#section-14-6) | `std::unique_lock`과 `std::scoped_lock` — 다중 잠금과 교착 상태 |
| [14.7](#section-14-7) | `std::condition_variable` — 작업이 올 때까지 대기 |
| [14.8](#section-14-8) | 중단 가능한 대기 — `condition_variable_any` |
| [14.9](#section-14-9) | `std::atomic` — 단일 값에 대한 원자 연산 |
| [14.10](#section-14-10) | Memory Ordering — Relaxed, Release, Acquire |
| [14.11](#section-14-11) | `atomic::wait` / `notify_one` — C++20 대기 |
| [14.12](#section-14-12) | `std::async`와 `std::future` — 작업 결과 받기 |
| [14.13](#section-14-13) | `std::promise` — 결과·예외의 전달 |
| [14.14](#section-14-14) | `std::shared_mutex` — 읽기와 쓰기 구분 |
| [14.15](#section-14-15) | `std::latch`와 `std::barrier` — 단계별 동기화 |
| [14.16](#section-14-16) | `thread_local` — 스레드별 저장 공간 |
| [14.17](#section-14-17) | Thread-Safe Design — 수명과 동기화 설계 |
| [14.18](#section-14-18) | Coding Practice — 4개 실습 |
| [14.19](#section-14-19) | Mini Project — Sensor Dispatcher |
| [14.20](#section-14-20) | Quiz & Summary |

## Getting Started

다음 명령어는 **`Chapter-14/` 폴더에서** 실행합니다.

**GCC**

```bash
g++ -std=c++20 -pthread -Wall -Wextra -Wpedantic examples/01_thread_basics.cpp -o thread_demo
./thread_demo
```

**Clang**

```bash
clang++ -std=c++20 -pthread -Wall -Wextra -Wpedantic examples/01_thread_basics.cpp -o thread_demo
./thread_demo
```

**MSVC — Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_thread_basics.cpp /Fe:thread_demo.exe
thread_demo.exe
```

자동 검증은 다음과 같이 실행합니다. Python 표준 라이브러리만 사용하며, 모범답안을 기본으로 검사합니다.

```bash
python3 tests/check.py --compiler g++-14
python3 tests/check.py --compiler clang++
python3 tests/check.py --mode student --only exercise-02
```

학생용 `exercises/`, `project/`에는 미완성 부분이 남아 있습니다. 실습 완료 전에는 해당 항목이 테스트를 통과하지 않는 것이 정상입니다. 비결정적인 스레드 실행 순서를 비교하는 대신, **동기화가 끝난 뒤의 결과와 불변 조건**을 검사합니다.

---

<a id="section-14-1"></a>
## 14.1. Concurrency와 Parallelism — 실행 순서와 공유 상태

동시성(Concurrency)은 여러 작업의 진행을 겹쳐 관리하는 구조이고, 병렬성(Parallelism)은 여러 작업이 실제로 동시에 실행되는 상태입니다. 스레드를 여러 개 만들었다고 항상 병렬 실행되는 것은 아닙니다. CPU 자원, 운영체제의 스케줄링, 잠금 대기 등에 따라 실행이 달라집니다.

하나의 스레드에서 처리하던 코드를 나누기 전에 **어떤 데이터를 공유하고, 누가 그 데이터의 수명을 책임지는지** 결정해야 합니다. 같은 함수를 여러 스레드에서 실행하더라도 입력과 결과가 독립적이면 동기화 부담이 작아집니다.

| 구분 | 설명 | 예시 |
|---|---|---|
| 동시성 | 여러 작업의 진행을 교대로 관리 | 네트워크 요청 다수 처리 |
| 병렬성 | 여러 작업을 물리적으로 겹쳐 실행 | 다중 코어에서 배열 구간별 합산 |
| 공유 상태 | 둘 이상의 스레드가 접근하는 데이터 | 카운터, 큐, 장치 상태 |
| 동기화 | 접근 순서와 메모리 가시성을 규정 | `join`, Mutex, Atomic |

이 예제의 `result`는 일반 정수지만, 작업 스레드가 쓰기를 마친 뒤 `join()`으로 종료를 확인하므로 호출 스레드가 안전하게 읽을 수 있습니다. 이처럼 **스레드 완료를 기다리는 것 자체가 동기화**가 될 수 있습니다.

**예제 코드 — [01_thread_basics.cpp](./examples/01_thread_basics.cpp)**

```cpp
#include <iostream>
#include <thread>

int main() {
    int result = 0;
    std::thread worker{[&result] { result = 21 * 2; }};
    worker.join(); // join 후에만 result를 읽는다.
    std::cout << "Result: " << result << '\n';
}
```

**실행 결과**

```text
Result: 42
```

---

<a id="section-14-2"></a>
## 14.2. `std::thread` — 생성, `join`과 수명

`std::thread`는 실행할 함수를 전달받아 스레드를 시작합니다. 스레드 객체의 `joinable()`이 `true`인 상태에서 소멸자가 실행되면 **`std::terminate()`가 호출**됩니다. 따라서 정상 흐름과 예외 경로를 모두 고려하여 `join()` 또는 소유권 이동을 설계해야 합니다.

`join()`은 대상 스레드가 완료될 때까지 호출 스레드를 기다리게 합니다. `detach()`는 스레드 객체와 실행 스레드의 연결을 끊지만, 참조 중인 지역 데이터의 수명을 보장하지 않습니다. 그래서 본 학습에서는 `detach()`를 문제 해결의 기본 방법으로 사용하지 않습니다.

- `joinable()`: 스레드 객체가 실행 스레드를 소유하고 있는지 확인
- `join()`: 완료를 기다린 후 연결 해제. 동일 객체에 두 번 호출 불가
- `std::move(thread)`: 스레드 실행 자체가 아닌 **스레드 소유권**을 이전
- `std::thread::hardware_concurrency()`: 논리적 동시 실행 가능 수에 대한 *힌트*. `0`이 반환될 수도 있음

예외가 발생할 수 있는 범위에서 직접 `std::thread`를 소유해야 한다면 RAII를 고려하세요. C++20에서는 `std::jthread`가 기본 선택지인 경우가 많습니다.

**예제 코드 — [02_thread_lifecycle.cpp](./examples/02_thread_lifecycle.cpp)**

```cpp
#include <iostream>
#include <thread>
#include <utility>

int main() {
    std::thread first{[] { /* 독립 작업 */ }};
    std::thread owner = std::move(first);
    std::cout << "Old joinable: " << std::boolalpha << first.joinable() << '\n';
    owner.join();
    std::cout << "Joined: " << !owner.joinable() << '\n';
}
```

**실행 결과**

```text
Old joinable: false
Joined: true
```

---

<a id="section-14-3"></a>
## 14.3. `std::jthread`와 `std::stop_token` — 협력적 종료

C++20의 `std::jthread`는 소멸 시, 연결된 스레드가 있으면 중단을 요청하고 완료될 때까지 기다립니다. 수명 관리의 실수를 줄일 수 있지만 **중단 요청이 작업을 강제로 종료하지는 않습니다.** 작업 함수가 `std::stop_token`을 확인하고 빠져나와야 합니다.

`stop_requested()`는 요청 상태를 확인합니다. `request_stop()`은 같은 중단 상태에 중단을 요청하며, 이미 중단이 요청된 경우에도 안전하게 호출할 수 있습니다. 다만 차단된 I/O나 일반 `std::condition_variable`의 대기를 자동으로 깨우지는 않습니다. 중단 가능한 조건 변수 대기는 14.8에서 확인합니다.

> 실무에서는 바쁜 반복문 대신 조건 변수, 이벤트, 작업 큐 등 대기 수단을 사용하고, 종료 시 처리 중인 데이터를 버릴지 끝까지 처리할지 명시해야 합니다.

**예제 코드 — [03_jthread_cancel.cpp](./examples/03_jthread_cancel.cpp)**

```cpp
#include <iostream>
#include <stop_token>
#include <thread>

int main() {
    bool observed_stop = false;
    std::jthread worker{[&](std::stop_token stop) {
        // 중단 토큰을 확인하는 최소 예제. 실무에서는 바쁜 대기 대신 대기 객체 사용.
        while (!stop.stop_requested()) std::this_thread::yield();
        observed_stop = true;
    }};
    worker.request_stop();
    worker.join();
    std::cout << "Stop observed: " << std::boolalpha << observed_stop << '\n';
    std::cout << "Joined: " << !worker.joinable() << '\n';
}
```

**실행 결과**

```text
Stop observed: true
Joined: true
```

---

<a id="section-14-4"></a>
## 14.4. Data Race와 Happens-Before — 무엇이 정의되지 않은 동작인가

둘 이상의 스레드가 같은 메모리 위치에 동기화 없이 접근하고, 그중 적어도 하나가 쓰기이며, 접근들이 정해진 *happens-before* 관계로 정렬되지 않으면 데이터 경쟁(Data Race)이 발생합니다. C++에서 데이터 경쟁은 **정의되지 않은 동작(Undefined Behavior)** 입니다. 값이 가끔 틀리는 정도로만 한정할 수 없습니다.

`++count`는 일반 정수에 대해 원자적 연산이 아닙니다. 여러 스레드가 동시에 수행하면 증가분을 잃어버릴 수 있습니다. 예제에서는 `std::mutex`로 모든 증가를 보호하고, 모든 작업을 `join()`한 뒤 결과를 출력합니다.

- `volatile`을 붙여도 데이터 경쟁이 해결되지 않습니다.
- 스레드마다 다른 `std::vector` 원소에 값을 쓰는 것은, 구조 변경 없이 해당 원소의 충돌이 없을 때 별개로 검토할 수 있습니다.
- 실행 결과가 여러 번 맞더라도 동기화가 올바르다는 증거는 아닙니다. 테스트와 별개로 코드의 공유 접근을 분석해야 합니다.

**예제 코드 — [04_race_free_counter.cpp](./examples/04_race_free_counter.cpp)**

```cpp
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

int main() {
    int count = 0;
    std::mutex mutex;
    std::vector<std::jthread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&] {
            for (int j = 0; j < 1000; ++j) {
                std::lock_guard lock{mutex};
                ++count;
            }
        });
    }
    for (auto& worker : workers) worker.join();
    std::cout << "Count: " << count << '\n';
}
```

**실행 결과**

```text
Count: 4000
```

---

<a id="section-14-5"></a>
## 14.5. `std::mutex`와 `std::lock_guard` — 불변 조건 보호

Mutex는 한 번에 하나의 스레드만 보호 구역에 들어오게 하는 동기화 수단입니다. 중요한 점은 변수 하나가 아니라 **함께 유지해야 하는 불변 조건(Invariant)** 을 보호하는 것입니다.

예제의 합계와 측정 건수는 한 번의 데이터 추가에서 동시에 바뀝니다. 두 필드를 다른 잠금으로 보호하면 읽는 스레드가 서로 맞지 않는 상태를 볼 수 있습니다. `std::lock_guard`는 생성 시 잠금을 획득하고 스코프 종료 시 해제하므로, 도중에 예외나 `return`이 발생해도 잠금 누락을 막습니다.

`const` 멤버 함수에서 내부 동기화를 수행하기 위해 `mutable std::mutex`를 사용했습니다. 이는 사용자 관점의 데이터 값이 변경되지 않는다는 계약과 내부 잠금 동작을 구분한 것입니다.

**예제 코드 — [05_lock_guard.cpp](./examples/05_lock_guard.cpp)**

```cpp
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

class Meter {
public:
    void add(int value) {
        std::lock_guard lock{mutex_};
        sum_ += value;
        ++count_; // sum_과 count_는 같은 잠금으로 보호한다.
    }
    void print() const {
        std::lock_guard lock{mutex_};
        std::cout << "Samples: " << count_ << ", Sum: " << sum_ << '\n';
    }
private:
    mutable std::mutex mutex_;
    int sum_{};
    int count_{};
};

int main() {
    Meter meter;
    std::vector<std::jthread> workers;
    for (int i = 0; i < 4; ++i) workers.emplace_back([&] { meter.add(5); });
    for (auto& worker : workers) worker.join();
    meter.print();
}
```

**실행 결과**

```text
Samples: 4, Sum: 20
```

---

<a id="section-14-6"></a>
## 14.6. `std::unique_lock`과 `std::scoped_lock` — 다중 잠금과 교착 상태

교착 상태(Deadlock)는 서로가 가진 잠금을 기다리느라 작업을 진행하지 못하는 상황입니다. 예를 들어 A는 첫 번째 Mutex를 획득하고 두 번째를 기다리는 동시에, B는 두 번째를 획득하고 첫 번째를 기다릴 수 있습니다.

`std::scoped_lock`에 여러 Mutex를 전달하면 표준 잠금 알고리즘을 사용하여 교착 상태를 피하도록 잠금을 획득합니다. 서로 연관된 계좌 잔액처럼 **여러 자원을 하나의 거래로 변경**할 때 유용합니다.

`std::unique_lock`은 필요한 때 잠금을 해제하거나 다시 잠글 수 있어 조건 변수 대기에 적합합니다. 일반적인 작은 임계 구역에서는 `std::lock_guard`가 간결하고, 여러 잠금을 함께 획득할 때는 `std::scoped_lock`을 우선 검토합니다.

> `std::scoped_lock`이 모든 교착 상태를 막는 것은 아닙니다. 서로 다른 코드 경로, 잠금 중 호출하는 함수, 외부 자원 대기 등도 설계해야 합니다.

**예제 코드 — [06_scoped_lock.cpp](./examples/06_scoped_lock.cpp)**

```cpp
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

struct Accounts {
    std::mutex left_mutex;
    std::mutex right_mutex;
    int left{100};
    int right{50};
    void transfer(int amount) {
        std::scoped_lock lock{left_mutex, right_mutex};
        if (amount >= 0 && left >= amount) {
            left -= amount;
            right += amount;
        }
    }
};

int main() {
    Accounts accounts;
    std::vector<std::jthread> workers;
    for (int i = 0; i < 5; ++i) workers.emplace_back([&] { accounts.transfer(10); });
    for (auto& worker : workers) worker.join();
    std::cout << "Balances: " << accounts.left << ", " << accounts.right << '\n';
}
```

**실행 결과**

```text
Balances: 50, 100
```

---

<a id="section-14-7"></a>
## 14.7. `std::condition_variable` — 작업이 올 때까지 대기

생산자(Producer)가 데이터를 넣을 때마다 소비자(Consumer)가 반복문으로 큐를 확인하면 CPU를 낭비할 수 있습니다. `std::condition_variable`은 조건이 만족될 때까지 스레드를 대기시킵니다.

대기할 때는 `std::unique_lock<std::mutex>`과 **조건을 다시 검사하는 predicate**를 사용합니다. 조건 변수는 이유 없이 깨어날 수 있고(Spurious Wakeup), 알림을 받았더라도 다른 소비자가 데이터를 먼저 가져갔을 수 있기 때문입니다.

```text
공유 큐 확인 → 비어 있으면 잠금 해제와 대기를 원자적으로 수행
알림 수신 → 잠금 재획득 → 조건 재검사 → 작업 처리
```

종료 가능한 큐에서는 `닫힘` 상태도 predicate에 포함해야 대기 중인 소비자가 영원히 잠들지 않습니다. 상태 변경은 Mutex로 보호하고, 상태 변경 뒤 `notify_one()` 또는 `notify_all()`을 호출합니다.

**예제 코드 — [07_condition_queue.cpp](./examples/07_condition_queue.cpp)**

```cpp
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

int main() {
    std::mutex mutex;
    std::condition_variable ready;
    std::queue<int> queue;
    bool closed = false;
    int received = 0;
    std::jthread consumer{[&] {
        std::unique_lock lock{mutex};
        ready.wait(lock, [&] { return closed || !queue.empty(); });
        if (!queue.empty()) {
            received = queue.front();
            queue.pop();
        }
    }};
    {
        std::lock_guard lock{mutex};
        queue.push(42);
        closed = true;
    }
    ready.notify_one();
    consumer.join();
    std::cout << "Received: " << received << '\n';
}
```

**실행 결과**

```text
Received: 42
```

---

<a id="section-14-8"></a>
## 14.8. 중단 가능한 대기 — `condition_variable_any`

C++20의 `std::condition_variable_any`는 `std::stop_token`을 받는 `wait` 오버로드를 제공합니다. 작업자가 일반적인 조건을 기다리는 도중 중단 요청이 들어오면 대기를 벗어나도록 만들 수 있습니다.

`wait(lock, token, predicate)`는 predicate가 참이면 `true`를 반환하고, 조건이 만족되지 않은 채 중단 요청으로 대기를 마치면 `false`를 반환합니다. 반환값을 확인해야 정상 처리와 취소 처리를 구별할 수 있습니다.

- 일반 `std::condition_variable`에는 이 C++20 중단 토큰 대기 오버로드가 없습니다.
- 중단 가능 여부는 해당 대기 함수의 계약에 달려 있으며, 임의의 시스템 호출을 강제로 취소하지는 못합니다.
- 스레드 종료 설계에는 큐에 남은 데이터를 끝까지 처리할지 여부도 포함해야 합니다.

**예제 코드 — [08_stoppable_wait.cpp](./examples/08_stoppable_wait.cpp)**

```cpp
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <stop_token>
#include <thread>

int main() {
    std::mutex mutex;
    std::condition_variable_any ready;
    bool has_work = false;
    bool stopped = false;
    std::jthread worker{[&](std::stop_token token) {
        std::unique_lock lock{mutex};
        const bool got_work = ready.wait(lock, token, [&] { return has_work; });
        stopped = !got_work;
    }};
    worker.request_stop(); // stop_token 지원 wait는 이 요청에 반응한다.
    worker.join();
    std::cout << "Stopped waiting: " << std::boolalpha << stopped << '\n';
}
```

**실행 결과**

```text
Stopped waiting: true
```

---

<a id="section-14-9"></a>
## 14.9. `std::atomic` — 단일 값에 대한 원자 연산

`std::atomic<T>`는 지원되는 타입의 값을 여러 스레드가 데이터 경쟁 없이 읽고 변경하도록 합니다. 처리 건수 같은 **독립적인 카운터**는 Mutex 대신 원자 연산을 사용할 수 있습니다.

`fetch_add(1, std::memory_order_relaxed)`는 증가 연산의 원자성은 보장하지만, 다른 일반 메모리 접근에 대한 추가 동기화 관계를 만들지 않습니다. 예제는 모든 스레드가 끝난 뒤 카운터만 읽으므로 이러한 용도에 맞습니다.

그러나 잔액과 거래 건수처럼 여러 값의 관계를 동시에 보존해야 한다면 **Atomic 변수 여러 개를 만드는 것만으로 거래의 원자성이 생기지 않습니다.** 먼저 Mutex를 이용해 올바른 구현을 완성하고, 병목이 확인된 범위에서 Atomic을 고려하세요.

**예제 코드 — [09_atomic_counter.cpp](./examples/09_atomic_counter.cpp)**

```cpp
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

int main() {
    std::atomic<int> processed{0};
    std::vector<std::jthread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&] {
            for (int j = 0; j < 500; ++j)
                processed.fetch_add(1, std::memory_order_relaxed);
        });
    }
    for (auto& worker : workers) worker.join();
    std::cout << "Processed: " << processed.load() << '\n';
}
```

**실행 결과**

```text
Processed: 2000
```

---

<a id="section-14-10"></a>
## 14.10. Memory Ordering — Relaxed, Release, Acquire

원자 연산의 메모리 순서(Memory Order)는 다른 메모리 접근과의 순서 관계를 정의합니다. 기본값인 `memory_order_seq_cst`는 강한 전역 순서 모델을 제공하지만, 모든 원자 사용에 무조건 가장 빠르거나 적합하다고 볼 수는 없습니다.

| 순서 | 핵심 의미 | 대표 용도 |
|---|---|---|
| `relaxed` | 해당 원자 객체의 연산 원자성 보장 | 독립 카운터 |
| `release` | 앞선 일반 쓰기를 다른 스레드에 게시 | 준비 상태 변경 |
| `acquire` | 대응되는 release가 게시한 데이터를 읽도록 동기화 | 준비 상태 확인 |
| `seq_cst` | 원자 연산 사이에 순차 일관성 순서를 추가 | 단순하고 강한 기본 규칙 |

예제에서 생산자는 `payload`를 먼저 쓰고 `ready.store(true, release)`로 공개합니다. 소비자가 그 값을 `acquire` 읽기로 확인하면 생산자의 선행 쓰기가 소비자에게 보입니다. **동기화에 성공했다는 조건**이 중요합니다. 일치하지 않는 원자 변수에 다른 순서를 붙인다고 자동으로 일반 데이터가 안전해지지는 않습니다.

락 없는 자료구조(Lock-free)는 메모리 재배치와 수명 문제까지 포함하므로 이 Chapter에서는 원리를 이해하는 수준으로 다룹니다.

**예제 코드 — [10_memory_order.cpp](./examples/10_memory_order.cpp)**

```cpp
#include <atomic>
#include <iostream>
#include <thread>

int main() {
    int payload = 0; // 원자 변수는 아니지만 release/acquire로 동기화한다.
    std::atomic<bool> ready{false};
    std::jthread producer{[&] {
        payload = 42;
        ready.store(true, std::memory_order_release);
    }};
    std::jthread consumer{[&] {
        while (!ready.load(std::memory_order_acquire)) std::this_thread::yield();
        std::cout << "Payload: " << payload << '\n';
    }};
    producer.join();
    consumer.join();
}
```

**실행 결과**

```text
Payload: 42
```

---

<a id="section-14-11"></a>
## 14.11. `atomic::wait` / `notify_one` — C++20 대기

C++20부터 일부 원자 타입은 `wait(old)`와 `notify_one()` / `notify_all()`을 제공합니다. `wait`는 원자 값이 주어진 기존 값과 같으면 대기하며, 값이 달라졌음을 확인하면 반환합니다. 즉, **알림만 보내고 값을 바꾸지 않으면 대기가 끝난다고 보장할 수 없습니다.**

예제에서는 생산자가 일반 데이터 `payload`를 작성한 뒤 `phase.store(1, release)`로 상태를 바꾸고 소비자에게 알립니다. 소비자는 `phase.wait(0, acquire)`로 준비 상태를 기다립니다. release/acquire 연결을 통해 `payload`를 안전하게 읽을 수 있습니다.

단, 대기 중에 값이 A→B→A로 되돌아가는 이른바 ABA 상황에서는 중간 변경을 놓칠 수 있습니다. 복잡한 프로토콜은 별도 상태 설계가 필요합니다.

**예제 코드 — [11_atomic_wait.cpp](./examples/11_atomic_wait.cpp)**

```cpp
#include <atomic>
#include <iostream>
#include <thread>

int main() {
    std::atomic<int> phase{0};
    int payload = 0;
    std::jthread consumer{[&] {
        phase.wait(0, std::memory_order_acquire);
        std::cout << "Payload: " << payload << '\n';
    }};
    payload = 73;
    phase.store(1, std::memory_order_release);
    phase.notify_one();
    consumer.join();
}
```

**실행 결과**

```text
Payload: 73
```

---

<a id="section-14-12"></a>
## 14.12. `std::async`와 `std::future` — 작업 결과 받기

스레드 생성과 결과 보관을 직접 관리하지 않아도 되는 작업이라면 `std::async`가 간편합니다. 비동기 작업의 반환값이나 예외는 `std::future`를 통해 전달됩니다.

`std::async(std::launch::async, work)`는 비동기 실행 정책을 명시합니다. 기본 정책을 생략하면 구현이 지연 실행(`deferred`)을 선택할 수 있으므로, 병렬 실행이 필요한 예제에서는 명시하는 편이 좋습니다.

- `future.get()`은 결과를 가져오며 필요할 경우 완료를 기다립니다. 일반적인 `future`에서는 한 번만 호출합니다.
- 작업 함수에서 발생한 예외는 `get()`에서 다시 발생합니다.
- `std::async(std::launch::async, ...)`로 생성한 공유 상태를 마지막으로 해제하는 `future`의 소멸자는 실행 완료까지 대기할 수 있습니다. 임시 `future`를 바로 버리지 않습니다.

작업마다 스레드를 생성하면 오히려 느려질 수 있습니다. 대량의 짧은 작업은 작업 큐나 별도 스케줄러가 더 적합할 수 있습니다.

**예제 코드 — [12_async_future.cpp](./examples/12_async_future.cpp)**

```cpp
#include <future>
#include <iostream>

int main() {
    auto future = std::async(std::launch::async, [] { return 6 * 7; });
    std::cout << "Result: " << future.get() << '\n';
    // get()은 결과를 한 번 가져오며 예외도 호출자에게 전달한다.
}
```

**실행 결과**

```text
Result: 42
```

---

<a id="section-14-13"></a>
## 14.13. `std::promise` — 결과·예외의 전달

`std::promise<T>`는 작업 결과를 공급하고, 짝이 되는 `std::future<T>`는 그 값을 소비합니다. 직접 구성한 스레드에서 결과를 전달하거나 **실패 원인을 호출자에게 전파**할 때 사용할 수 있습니다.

`set_value()`는 정상 결과를, `set_exception()`은 예외 정보를 공유 상태에 저장합니다. 아직 결과를 설정하지 않은 Promise가 파괴되면 연관된 Future는 일반적으로 `broken_promise` 오류를 받습니다.

직접 Promise를 사용하는 경우에는 `set_value()`를 여러 번 호출하거나, 이미 결과를 가져간 Future를 다시 사용하지 않도록 계약을 명확히 해야 합니다. 단순한 비동기 함수 호출은 앞의 `std::async`가 더 짧을 수 있습니다.

**예제 코드 — [13_promise_exception.cpp](./examples/13_promise_exception.cpp)**

```cpp
#include <future>
#include <iostream>
#include <stdexcept>
#include <thread>
#include <utility>

int main() {
    std::promise<int> promise;
    auto result = promise.get_future();
    std::jthread producer{[p = std::move(promise)]() mutable {
        p.set_exception(std::make_exception_ptr(std::runtime_error{"sensor offline"}));
    }};
    try {
        (void)result.get();
    } catch (const std::runtime_error& error) {
        std::cout << "Error: " << error.what() << '\n';
    }
}
```

**실행 결과**

```text
Error: sensor offline
```

---

<a id="section-14-14"></a>
## 14.14. `std::shared_mutex` — 읽기와 쓰기 구분

데이터 변경은 드물지만 읽는 작업이 많은 자료구조에서는 `std::shared_mutex`를 검토할 수 있습니다. `std::shared_lock`은 여러 독자(Reader)가 동시에 읽도록 하고, `std::unique_lock`은 작성자(Writer)가 배타적으로 변경하도록 합니다.

예제에서는 레지스트리를 업데이트한 다음 읽기 작업 네 개를 시작합니다. 읽기만 수행하는 동안에는 여러 스레드가 공유 잠금을 얻을 수 있습니다.

하지만 **읽기 편향이 항상 더 빠른 것은 아닙니다.** 보호 구역이 짧거나 쓰기가 잦다면 일반 Mutex가 단순하고 유리할 수도 있습니다. 독자·작성자 간 공정성 및 기아 상태(Starvation)는 구현과 부하에 영향을 받으므로 별도 측정이 필요합니다.

**예제 코드 — [14_shared_mutex.cpp](./examples/14_shared_mutex.cpp)**

```cpp
#include <iostream>
#include <mutex>
#include <shared_mutex>
#include <thread>
#include <vector>

class Registry {
public:
    void update(int value) {
        std::unique_lock lock{mutex_};
        value_ = value;
    }
    [[nodiscard]] int read() const {
        std::shared_lock lock{mutex_};
        return value_;
    }
private:
    mutable std::shared_mutex mutex_;
    int value_{};
};

int main() {
    Registry registry;
    registry.update(31);
    std::vector<int> readings(4);
    std::vector<std::jthread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&, i] { readings[i] = registry.read(); });
    }
    for (auto& worker : workers) worker.join();
    std::cout << "Reads: " << readings[0] + readings[1]
              + readings[2] + readings[3] << '\n';
}
```

**실행 결과**

```text
Reads: 124
```

---

<a id="section-14-15"></a>
## 14.15. `std::latch`와 `std::barrier` — 단계별 동기화

C++20의 `std::latch`는 정해진 건수의 도착을 한 번 기다리는 **일회성 동기화** 도구입니다. 초기화, 리소스 준비, 여러 작업의 종료 대기 등에 사용할 수 있습니다.

`std::barrier`는 모든 참여자가 도착할 때마다 함께 다음 단계로 진행하는 **반복 가능한 단계 동기화** 도구입니다. 한 단계에서 작성한 데이터를 다음 단계에서 소비하는 계산에 적합합니다.

| 도구 | 재사용 | 주된 용도 |
|---|---|---|
| `std::latch` | 불가 | 준비 완료 또는 작업 완료 카운트 |
| `std::barrier` | 가능 | 단계별 집단 진행 |

참여자 수를 잘못 설정하거나 도착해야 할 스레드가 예외로 종료되면 기다림이 끝나지 않을 수 있습니다. 완료를 기다리는 구조에서는 스레드 생성 실패와 오류 전파 경로까지 고려해야 합니다.

**예제 코드 — [15_latch_barrier.cpp](./examples/15_latch_barrier.cpp)**

```cpp
#include <barrier>
#include <iostream>
#include <latch>
#include <thread>

int main() {
    std::latch ready{2};
    std::barrier sync_point{2};
    int first = 0;
    int second = 0;
    std::jthread a{[&] {
        first = 10;
        ready.count_down();
        sync_point.arrive_and_wait();
        first += second;
    }};
    std::jthread b{[&] {
        second = 20;
        ready.count_down();
        sync_point.arrive_and_wait();
        // 이 단계에서는 공유 데이터를 추가로 쓰지 않는다.
    }};
    ready.wait(); // 준비가 끝났지만 각 스레드는 barrier에서 서로를 기다린다.
    a.join();
    b.join();
    std::cout << "Values: " << first << ", " << second << '\n';
}
```

**실행 결과**

```text
Values: 30, 20
```

---

<a id="section-14-16"></a>
## 14.16. `thread_local` — 스레드별 저장 공간

`thread_local`로 선언한 객체는 각 스레드에 별도의 인스턴스를 가집니다. 스레드별 파서 상태나 임시 집계 버퍼처럼 다른 스레드와 공유할 필요가 없는 값에 사용할 수 있습니다.

예제의 `local_sequence`는 두 작업 스레드에서 각각 0으로 시작하므로 서로의 증가값에 영향을 주지 않습니다. 단, `thread_local` 객체 안에 **다른 스레드와 공유하는 포인터나 외부 자원**을 보관한다면 그 자원까지 자동으로 안전해지는 것은 아닙니다.

스레드 풀에서는 작업 하나가 끝나도 스레드 자체는 계속 살아 있을 수 있습니다. 따라서 `thread_local` 상태가 여러 작업 사이에 남을 수 있다는 점도 주의하세요.

**예제 코드 — [16_thread_local.cpp](./examples/16_thread_local.cpp)**

```cpp
#include <iostream>
#include <thread>

thread_local int local_sequence = 0;

int main() {
    int left = 0;
    int right = 0;
    std::jthread a{[&] { ++local_sequence; ++local_sequence; left = local_sequence; }};
    std::jthread b{[&] { ++local_sequence; right = local_sequence; }};
    a.join();
    b.join();
    std::cout << "Local counters: " << left << ", " << right << '\n';
}
```

**실행 결과**

```text
Local counters: 2, 1
```

---

<a id="section-14-17"></a>
## 14.17. Thread-Safe Design — 수명과 동기화 설계

동시성 코드는 **공유 상태를 줄이는 설계**에서 출발하는 것이 좋습니다. 각 스레드가 독립된 값을 계산한 뒤 최종 결과만 합칠 수 있다면 공유 메모리를 직접 변경하는 것보다 검증이 쉽습니다.

| 상황 | 우선 고려할 방법 | 확인 사항 |
|---|---|---|
| 작업 완료와 객체 수명 연결 | `std::jthread` | 취소 요청과 실제 종료는 다름 |
| 서로 연관된 여러 상태 수정 | Mutex + RAII 잠금 | 한 임계 구역에서 불변 조건 유지 |
| 단일 진행 건수 집계 | `std::atomic` | 다른 데이터까지 동기화한다고 가정하지 않음 |
| 생산자·소비자 | 큐 + Mutex + Condition Variable | 대기 조건, 종료 플래그, 남은 작업 처리 |
| 비동기 결과 또는 예외 수신 | `std::async` + `std::future` | 실행 정책, `get()`, Future 수명 |
| 독립 작업의 부분 합 | 스레드별 결과 보관 후 합산 | 공유 쓰기 최소화, 최종 합산 순서 |

### 설계 및 검증 순서

1. **데이터 소유권:** 각 값이 생성·파괴되는 위치를 먼저 정합니다. 캡처한 참조가 스레드보다 먼저 사라지지 않도록 합니다.
2. **공유 상태:** 동시에 읽고 쓰는 값과 반드시 함께 바뀌어야 하는 값을 구별합니다.
3. **종료 정책:** 새 작업 차단, 남은 작업 처리, 작업자 깨우기, `join()` 순서를 명시합니다.
4. **오류 정책:** 예외는 스레드 경계를 자동으로 넘어가지 않습니다. Future나 별도 공유 결과 등으로 전달합니다. 스레드 함수 밖으로 예외가 전파되면 `std::terminate()`가 호출될 수 있습니다.
5. **성능 검증:** 정확한 단일 스레드 구현을 만든 뒤 데이터 크기와 스레드 수를 변경해 측정합니다. 짧은 작업에 스레드를 많이 생성하면 관리 비용이 더 클 수 있습니다.

### 흔한 문제

- **Data Race:** 동기화 없는 동일 메모리 접근은 UB. 실제로 몇 번 성공했는지와 무관함
- **Deadlock:** 서로 다른 잠금 획득 순서, 잠금 보유 중 외부 호출 등의 상황
- **Lost Notification:** 조건을 검사하지 않고 알림만 믿거나, 조건 변경이 잠금 규약을 따르지 않는 경우
- **False Sharing:** 서로 다른 변수라도 동일 캐시 라인에 놓이면 성능 간섭이 발생할 수 있음. 기능 오류와는 구별
- **Oversubscription:** CPU 자원에 비해 지나치게 많은 실행 스레드를 생성하면 처리량이 감소할 수 있음

`std::thread`나 Mutex를 사용하는 함수가 반드시 모든 호출 순서에서 안전한 것은 아닙니다. **공개 API의 스레드 안전성 계약**을 명시해야 합니다.

---

<a id="section-14-18"></a>
## 14.18. Coding Practice

앞서 배운 RAII, 잠금, 조건 변수, Future를 활용하는 실습입니다. 학생용 파일에는 구현해야 할 부분만 남겨 두었고, 정답 코드는 `solutions/`에 분리했습니다. 각 문제에서 출력 예제만 맞추는 대신, **동시에 호출할 때에도 같은 불변 조건을 유지하는지** 확인합니다.

### 실습 ① — Parallel Sum

**문제**

측정값 배열의 합계를 여러 작업자로 나누어 계산하는 프로그램입니다. 작업자는 서로의 부분 합을 수정하지 않아야 하며, 모든 작업자가 종료된 뒤 최종 합계를 구해야 합니다. 입력이 비어 있으면 `0`을 반환합니다.

**구현 조건**

1. `parallel_sum(std::span<const int>, std::size_t)` 함수를 완성합니다.
2. 작업자 수가 1~32 범위를 벗어나면 `std::invalid_argument` 예외를 발생시킵니다.
3. 데이터의 연속 구간을 나누고, 작업자별 `long long` 부분 합을 계산합니다.
4. 작업자를 모두 `join()`한 뒤 부분 합을 합칩니다. 각 값은 한 번만 합산해야 합니다.

**예제 출력**

```text
Sum: 150
```

[학생용 코드](./exercises/01_parallel_sum.cpp) · [모범답안](./solutions/01_parallel_sum.cpp)

<details>
<summary>구현 가이드</summary>

**STEP 01 — 구간 분할**  
`i`번째 작업자가 처리할 범위는 `[i * n / count, (i + 1) * n / count)` 형태로 계산할 수 있습니다.

**STEP 02 — 독립된 부분 합**  
서로 다른 작업자가 같은 부분 합 변수에 쓰지 않도록 합니다.

```cpp
std::vector<long long> partial(count, 0);
std::vector<std::jthread> workers;
```

**STEP 03 — 완료 후 합산**  
작업자와 입력 데이터가 살아 있는 동안 스레드가 작업을 마치게 합니다.

</details>

**검증 사항:** 음수·0 포함 배열, 원소보다 많은 작업자, 빈 배열, 잘못된 작업자 수, `int` 범위를 넘는 합계

### 실습 ② — Safe Inventory

**문제**

온라인 판매 시스템에서 여러 구매 요청이 동시에 들어옵니다. 각 요청은 판매 가능한 재고가 있을 때만 확정되어야 하며, 어느 시점에서도 재고는 음수가 될 수 없습니다. 구매 성공 수량과 남은 재고를 관리하는 클래스를 작성하세요.

**구현 조건**

1. `StockLedger` 생성자는 음수 초기 재고를 거부합니다.
2. `purchase(quantity)`는 수량이 양수이고 잔여 재고 이하일 때만 구매를 처리합니다.
3. 재고 확인과 차감을 **같은 잠금 구간**에서 수행합니다.
4. `remaining()` 및 `sold_units()`는 서로 데이터 경쟁을 일으키지 않아야 합니다.

**예제 출력**

```text
Sold: 150, Remaining: 0
```

[학생용 코드](./exercises/02_safe_inventory.cpp) · [모범답안](./solutions/02_safe_inventory.cpp)

<details>
<summary>구현 가이드</summary>

**STEP 01 — 데이터 보호**  
잠금을 클래스 안에 배치하고 모든 공개 메서드에서 같은 잠금 규약을 사용합니다.

```cpp
mutable std::mutex mutex_;
// std::lock_guard lock{mutex_};
```

**STEP 02 — 거래의 원자성**  
재고를 먼저 읽고 잠금을 풀었다가 나중에 차감하면, 그사이에 다른 스레드가 재고를 구매할 수 있습니다.

</details>

**검증 사항:** 0·음수 주문, 초기 재고 0, 동일 재고를 초과하는 동시 구매, 판매량 + 잔여량 = 초기 재고

### 실습 ③ — Closing Queue

**문제**

작업 큐에는 여러 스레드가 데이터를 제출하고 소비합니다. 종료 요청 이후에는 새 작업을 받지 않되, 큐에 남은 데이터는 끝까지 처리해야 합니다. 모든 데이터를 꺼내고 나서야 소비자가 정상 종료될 수 있는 큐를 구현하세요.

**구현 조건**

1. `push(value)`는 열려 있을 때만 추가하고 `true`를 반환합니다.
2. `pop()`은 데이터가 들어올 때까지 대기합니다. 큐가 닫히고 비었다면 `std::nullopt`를 반환합니다.
3. `close()`는 추가 제출을 막고 대기 중인 모든 소비자를 깨웁니다.
4. 큐와 종료 플래그는 동일한 Mutex로 보호합니다.

**예제 출력**

```text
Values: 11, 22, Closed: true
```

[학생용 코드](./exercises/03_closing_queue.cpp) · [모범답안](./solutions/03_closing_queue.cpp)

<details>
<summary>구현 가이드</summary>

**STEP 01 — 대기 조건**  
종료되었거나 데이터가 생겼을 때만 대기에서 깨어나게 합니다.

```cpp
std::unique_lock lock{mutex_};
changed_.wait(lock, [&] { return closed_ || !data_.empty(); });
```

**STEP 02 — 종료 후 잔여 작업**  
`closed_ == true`여도 데이터가 남았다면 먼저 반환합니다. `close()` 뒤에는 `notify_all()`을 호출합니다.

</details>

**검증 사항:** 빈 큐에서 종료, 종료 직전 제출, 남은 항목 전부 소비, 다수 생산자, 닫힌 뒤 추가 제출 거부

### 실습 ④ — Async Results

**문제**

서로 독립적인 정수 계산을 비동기 작업으로 실행합니다. 각 계산은 입력값의 제곱을 반환하며, 음수 입력은 오류로 처리해야 합니다. 완료 순서는 달라도 **반환 결과의 순서는 입력 순서와 같아야** 합니다.

**구현 조건**

1. `evaluate_in_parallel()` 함수를 완성합니다.
2. 각 입력에 대해 `std::async(std::launch::async, ...)`를 실행합니다.
3. 음수 입력은 작업 안에서 `std::invalid_argument`를 발생시킵니다.
4. Future를 입력 순서대로 `get()`하여 결과를 수집합니다. 합산 시 `int` 오버플로를 피하도록 `long long`을 사용합니다.

**예제 출력**

```text
Results: 4, 16, 36
```

[학생용 코드](./exercises/04_async_results.cpp) · [모범답안](./solutions/04_async_results.cpp)

<details>
<summary>구현 가이드</summary>

**STEP 01 — 작업 실행**  
각 입력에 대응하는 Future를 순서대로 보관합니다.

```cpp
std::vector<std::future<long long>> pending;
pending.reserve(inputs.size());
```

**STEP 02 — 오류 전달**  
작업 내부에서 예외를 던지고, 호출자에서 `future.get()`으로 그 예외를 받습니다.

</details>

**검증 사항:** 빈 입력, 0, 큰 정수의 제곱, 중간 음수 입력 시 예외, 반환 순서 유지

**실습 검증**

```bash
python3 tests/check.py --mode student --only exercise-01
python3 tests/check.py --mode student --only exercise-02
python3 tests/check.py --mode student --only exercise-03
python3 tests/check.py --mode student --only exercise-04
```

---

<a id="section-14-19"></a>
## 14.19. Mini Project — Sensor Dispatcher

### 프로젝트 배경

공장 설비에서 장치별 센서 측정값이 계속 들어옵니다. 입출력 스레드가 센서 데이터를 접수하는 동안, 별도 작업자들은 제출된 데이터를 검사하고 경보 여부와 합계 정보를 계산해야 합니다.

작업자를 늘리면 실제 처리 순서는 달라질 수 있습니다. 그러나 **유효한 입력 집합이 같다면 최종 보고서의 건수와 합계는 같아야** 합니다. 프로그램 종료 시에는 추가 접수를 중단하고, 이미 접수된 데이터는 모두 처리해야 합니다.

### 요구사항

1. `Dispatcher`는 생성 시 작업자 수 1~32를 받아 작업자 스레드를 시작합니다. 범위 밖 값은 예외 처리합니다.
2. `submit(Sample)`은 여러 생산자 스레드에서 동시에 호출될 수 있습니다.
3. 장치 ID는 1~10,000, 측정값은 0~100입니다. 범위를 벗어난 제출은 `false`를 반환하고 거부 건수에 반영합니다.
4. 유효한 데이터는 큐에 기록하고 접수 건수를 증가시킵니다. 여러 작업자가 큐에서 데이터를 꺼내 병렬로 처리합니다.
5. 측정값이 80 이상이면 경보 건수를 증가시킵니다. Checksum은 `device_id × 1000 + value`의 합으로 정의합니다.
6. `finish()`는 새 제출을 차단하고, 남은 큐가 모두 처리될 때까지 기다린 뒤 정산 결과를 반환합니다. 종료 후 제출은 `false`를 반환하며 거부 건수에는 추가하지 않습니다.
7. 집계값은 잠금으로 보호합니다. 작업 완료 순서에 상관없이 최종 합계가 동일해야 합니다.

### 제공 코드

| 위치 | 구성 |
|---|---|
| [`project/`](./project/) | 학생용 시작 프로젝트. `src/dispatcher.cpp`에 TODO 포함 |
| [`solutions/sensor_dispatcher/`](./solutions/sensor_dispatcher/) | 모범 구현과 검증 코드 |
| [`examples/17_sensor_dispatcher/`](./examples/17_sensor_dispatcher/) | 실행 가능한 다중 파일 예제 및 CI 연동용 프로젝트 |
| [`tests/check.py`](./tests/check.py) | 단일 예제·실습·프로젝트 동작 검사 |

주요 인터페이스:

```cpp
namespace dispatch {
struct Sample { int device_id; int value; };
struct Summary { /* accepted, processed, rejected, alerts, checksum */ };
class Dispatcher {
public:
    explicit Dispatcher(std::size_t worker_count);
    bool submit(Sample sample);
    Summary finish();
    Summary snapshot() const;
};
}
```

### 출력 예시

```text
Accepted: 4
Processed: 4
Rejected: 1
Alerts: 2
Checksum: 10252
```

### CMake 빌드 및 테스트

`Chapter-14/` 폴더 기준입니다.

```bash
cmake -S examples/17_sensor_dispatcher -B build/ch14 -DCMAKE_CXX_STANDARD=20 -DCMAKE_BUILD_TYPE=Debug
cmake --build build/ch14
ctest --test-dir build/ch14 --output-on-failure
```

학생용 프로젝트를 완성한 뒤에는 `-S project`로 변경하여 동일한 테스트를 실행합니다. 모범답안은 `-S solutions/sensor_dispatcher`로 빌드할 수 있습니다. Windows에서는 CMake의 컴파일러 설정과 `std::thread` 지원 환경을 확인합니다.

<details>
<summary>구현 가이드</summary>

**STEP 01 — 잠금과 큐**  
`std::deque<Sample>`, `std::mutex`, `std::condition_variable`을 사용합니다. 큐가 비어 있더라도 접수 중이면 기다려야 하며, 종료 요청과 빈 큐가 함께 확인된 경우만 소비자 스레드를 종료합니다.

**STEP 02 — 제출 처리**  
유효하지 않은 입력과 종료 후 제출을 구분합니다. 큐 삽입 과정에서 메모리 할당이 실패한다면 접수 건수를 먼저 증가시키지 않아야 합니다.

**STEP 03 — 종료 처리**  
`finish()`에서 새 제출을 차단하고 모든 작업자를 깨운 뒤 `join()`을 수행합니다. `std::jthread` 소멸자가 중단 요청을 할 수 있다는 이유로, 남은 데이터 처리를 생략해서는 안 됩니다.

**STEP 04 — 검증**  
한 작업자와 여러 작업자에서 동일 입력 결과를 비교합니다. 결과를 작업 완료 순서대로 출력하지 않고 처리 후 Summary로 출력하면 순서 차이의 영향을 줄일 수 있습니다.

</details>

### 검증 사항

- 모든 작업 완료 시 `accepted == processed` 확인
- 잘못된 장치 ID·금액 범위와 종료 후 제출 처리
- 1개·4개 작업자 설정의 결과 동등성
- 여러 생산자의 동시 제출, 종료 직전 데이터 유실 여부
- 같은 입력을 반복 실행했을 때 건수 및 Checksum 일치

**설계 범위:** 이번 구현의 큐는 무제한 저장 방식입니다. 운영 환경에서는 최대 대기량, Backpressure, 작업자 장애 처리, 대량 합계의 오버플로 가능성 등을 추가 검토해야 합니다. `submit()`은 동시 호출할 수 있지만, **`finish()`는 제출을 마친 소유 스레드가 단독으로 호출**한다는 계약을 둡니다.

---

<a id="section-14-20"></a>
## 14.20. Quiz & Summary

### Quiz

<details>
<summary>Q1. 동시성(Concurrency)과 병렬성(Parallelism)은 항상 같은 의미인가요?</summary>

아닙니다. 동시성은 작업의 진행을 함께 관리하는 구조이고, 병렬성은 실제 작업 실행이 물리적으로 겹치는 상태입니다. 여러 스레드를 만든다고 병렬성이 자동 보장되지는 않습니다.

</details>

<details>
<summary>Q2. `joinable()`인 `std::thread` 객체가 소멸되면 어떻게 되나요?</summary>

자동 `join()`이 아니라 `std::terminate()`가 호출됩니다. 작업 완료를 기다리거나, 소유권을 명시적으로 이동하는 설계가 필요합니다.

</details>

<details>
<summary>Q3. `std::jthread` 소멸자는 작업 스레드를 강제 종료하나요?</summary>

아닙니다. 중단을 요청하고 `join()`을 수행합니다. 작업자가 요청을 관찰하고 종료해야 합니다.

</details>

<details>
<summary>Q4. 여러 스레드에서 일반 정수에 `++count`를 수행하면 왜 위험한가요?</summary>

동기화 없는 읽기·쓰기 접근이 겹치면 Data Race가 발생하고 C++에서는 정의되지 않은 동작입니다. Mutex나 Atomic을 사용합니다.

</details>

<details>
<summary>Q5. `std::lock_guard`와 `std::unique_lock`의 주된 차이는 무엇인가요?</summary>

lock_guard는 스코프 기반 잠금 관리에 집중하고, unique_lock은 지연 잠금·해제·재잠금 등 유연한 제어를 지원하여 조건 변수 대기에 적합합니다.

</details>

<details>
<summary>Q6. Condition Variable의 `wait`에서 predicate가 필요한 이유는 무엇인가요?</summary>

허위 깨움이 발생할 수 있고, 알림 이후 다른 작업자가 먼저 자원을 소비했을 수도 있어, 잠금을 다시 얻은 상태에서 조건을 재검사해야 합니다.

</details>

<details>
<summary>Q7. Atomic 카운터 여러 개로 다중 필드의 불변 조건까지 보장할 수 있나요?</summary>

일반적으로 아닙니다. 각 변수의 원자성만으로 여러 값의 일관된 묶음 변경이 보장되지는 않으며, Mutex 또는 별도 프로토콜이 필요합니다.

</details>

<details>
<summary>Q8. `memory_order_relaxed`가 다른 일반 변수의 쓰기까지 동기화하나요?</summary>

아닙니다. 해당 원자 객체 연산의 원자성을 보장할 뿐, 다른 메모리 접근의 동기화 관계를 추가하지 않습니다.

</details>

<details>
<summary>Q9. `atomic::wait`에 알림을 보내기만 하면 대기가 끝날까요?</summary>

보장되지 않습니다. 대기하는 원자 값이 지정한 이전 값과 달라져야 반환됩니다.

</details>

<details>
<summary>Q10. `std::async` 작업에서 발생한 예외는 어디에서 확인하나요?</summary>

연관된 std::future의 get()을 호출할 때 예외가 다시 발생합니다.

</details>

<details>
<summary>Q11. `std::latch`와 `std::barrier`는 어떻게 다른가요?</summary>

latch는 일회성 도착 카운터이고 barrier는 여러 단계에 반복 사용할 수 있는 동기화 객체입니다.

</details>

<details>
<summary>Q12. Mini Project에서 `finish()`가 작업자를 바로 종료시키지 않는 이유는 무엇인가요?</summary>

접수된 작업을 버리지 않고 큐를 끝까지 처리한 다음 집계를 완료해야 하기 때문입니다. 새 접수 차단과 남은 작업 처리, 스레드 join 순서가 필요합니다.

</details>

### Summary

- `std::thread`는 직접 완료를 관리하고, `std::jthread`는 수명과 협력적 종료 관리를 쉽게 합니다.
- Data Race는 단순히 출력이 틀리는 현상이 아니라 **정의되지 않은 동작**입니다.
- Mutex는 여러 값의 불변 조건을 보호하고, Atomic은 독립된 값의 원자적 연산에 적합합니다.
- 조건 변수는 **공유 조건 + Mutex + Predicate**를 함께 설계해야 합니다.
- `release`와 `acquire`는 특정 원자 상태를 통해 일반 데이터의 공개·관찰 관계를 구성할 수 있습니다.
- Future는 비동기 반환값과 예외를 전달하며, 작업 실행 정책과 객체 수명을 함께 이해해야 합니다.
- 올바른 종료는 새 작업 차단, 대기 중인 작업자 깨우기, 남은 작업 처리, `join()`을 모두 고려합니다.

### References

- [cppreference — Concurrency Support Library](https://en.cppreference.com/w/cpp/thread)
- [cppreference — `std::jthread`](https://en.cppreference.com/w/cpp/thread/jthread)
- [cppreference — `std::stop_token`](https://en.cppreference.com/w/cpp/thread/stop_token)
- [cppreference — `std::atomic::wait`](https://en.cppreference.com/w/cpp/atomic/atomic/wait)
- [cppreference — `std::async`](https://en.cppreference.com/w/cpp/thread/async)
- [ISO C++ — The Standard](https://isocpp.org/std/the-standard)

---

[← C++ 목차](../README.md) · [← Chapter 13](../Chapter-13/README.md)
