# Chapter 15. Memory & Performance Optimization

C++20의 메모리 관리와 자료구조를 바탕으로 **측정 가능한 성능 개선**을 설계합니다. 연속 메모리와 캐시, 할당 비용, `std::pmr`, 데이터 배치와 프로파일링을 학습한 뒤, 기준 구현과 최적화 구현을 같은 테스트로 비교하는 Mini Project까지 진행합니다.

**기준 표준:** C++20 (ISO/IEC 14882:2020)  
**개발 환경:** GCC, Clang, MSVC  
**학습 원칙:** 정확성 검증 → 병목 측정 → 변경 → 동일 입력으로 재검증

<details>
<summary>선행 학습</summary>

- [Chapter 06. Arrays & Strings](../Chapter-06/README.md) — 연속 자료 저장
- [Chapter 07. Pointers & References](../Chapter-07/README.md) — 포인터와 객체 수명
- [Chapter 10. Standard Library (STL)](../Chapter-10/README.md) — Container와 Algorithm
- [Chapter 12. Modern C++ & Resource Management](../Chapter-12/README.md) — RAII와 소유권
- [Chapter 13. Templates & Generic Programming](../Chapter-13/README.md) — Ranges 및 타입 계약
- [Chapter 14. Concurrency & Multithreading](../Chapter-14/README.md) — Data Race와 False Sharing

</details>

## Contents

| Section | Topic |
|:---:|---|
| [15.1](#section-15-1) | Performance Engineering — 먼저 측정하기 |
| [15.2](#section-15-2) | 객체 수명과 저장 공간 — Stack / Heap 구분 |
| [15.3](#section-15-3) | `std::vector::reserve()` — 재할당 줄이기 |
| [15.4](#section-15-4) | Cache Locality — 연속 데이터 접근 |
| [15.5](#section-15-5) | `std::span` — 복사 없는 연속 범위 전달 |
| [15.6](#section-15-6) | AoS와 SoA — 데이터 배치 선택 |
| [15.7](#section-15-7) | Alignment와 False Sharing — 데이터 경계 |
| [15.8](#section-15-8) | 메모리 접근 순서 — Row-Major와 Column-Major |
| [15.9](#section-15-9) | `std::pmr::monotonic_buffer_resource` — 일괄 수명 관리 |
| [15.10](#section-15-10) | Pool Allocator — 반복 할당 비용 다루기 |
| [15.11](#section-15-11) | 탐색 자료구조와 계산 복잡도 |
| [15.12](#section-15-12) | 복사, 이동, View — 데이터 전달 비용 |
| [15.13](#section-15-13) | 표준 Algorithm과 Ranges — 명확한 순회 |
| [15.14](#section-15-14) | Benchmark — `std::chrono::steady_clock` |
| [15.15](#section-15-15) | 정수 범위와 검증 — 빠른 코드도 안전해야 함 |
| [15.16](#section-15-16) | 정렬 인덱스와 재사용 — 전처리 비용 계산 |
| [15.17](#section-15-17) | Profiling과 Performance Regression |
| [15.18](#section-15-18) | Coding Practice — 4개 실습 |
| [15.19](#section-15-19) | Mini Project — Sensor Batch Analyzer |
| [15.20](#section-15-20) | Quiz & Summary |

## Getting Started

다음 명령어는 **`Chapter-15/` 폴더 기준**입니다. 예제는 외부 라이브러리 없이 C++20 표준 라이브러리만 사용합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_measure_before_optimizing.cpp -o demo
./demo
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_measure_before_optimizing.cpp -o demo
./demo
```

**MSVC — Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_measure_before_optimizing.cpp /Fe:demo.exe
demo.exe
```

**자동 검증**

```bash
python3 tests/check.py --compiler g++-14
python3 tests/check.py --compiler clang++
python3 tests/check.py --mode student --only exercise-01
```

학생용 `exercises/`와 `project/`는 구현 부분이 비어 있습니다. 완성하기 전에는 테스트 실패가 정상이며, 기본 검증은 `solutions/`를 사용합니다. 성능 측정은 CI의 정확성 검사와 분리합니다.

---

<a id="section-15-1"></a>
## 15.1. Performance Engineering — 먼저 측정하기

성능 최적화는 코드를 무조건 짧게 만들거나 루프를 많이 줄이는 작업이 아닙니다. **정확성, 처리 시간, 메모리 사용량, 유지보수 비용** 가운데 무엇을 개선할지 정하고, 수치를 기록한 뒤 검증하는 과정입니다.

- **Latency:** 요청 한 건이 완료될 때까지 걸린 시간
- **Throughput:** 단위 시간당 처리한 작업 수
- **Peak Memory:** 실행 중 사용한 최대 메모리
- **Correctness:** 최적화 전·후에 입력과 출력의 계약이 유지되는지 여부

입력 크기가 10배가 되어도 처리 시간이 10배로 증가한다고 단정할 수는 없습니다. 데이터 분포, 캐시 적중률, 컴파일러, 실행 환경이 모두 영향을 줍니다. **검증 가능한 기준 구현을 먼저 만든 뒤** 성능 병목을 찾아야 합니다.

**예제 코드 — [01_measure_before_optimizing.cpp](./examples/01_measure_before_optimizing.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> readings{12, 18, 24, 30};
    const int total = std::accumulate(readings.begin(), readings.end(), 0);
    const auto peak = std::ranges::max_element(readings);
    std::cout << "Count: " << readings.size() << "\n";
    std::cout << "Total: " << total << ", Peak: " << *peak << "\n";
}
```

**실행 결과**

```text
Count: 4
Total: 84, Peak: 30
```

최댓값과 합계를 계산하는 기준 동작을 먼저 확인합니다. 입력이 빈 경우에는 `max_element()` 결과가 끝 Iterator이므로 역참조하지 않아야 합니다.

---

<a id="section-15-2"></a>
## 15.2. 객체 수명과 저장 공간 — Stack / Heap 구분

C++ 객체는 자동 저장 기간(Automatic Storage Duration), 동적 저장 기간(Dynamic Storage Duration) 등 다양한 방식으로 존재합니다. 함수의 지역 변수는 일반적으로 자동 저장 기간을 가지지만, 표준은 모든 지역 객체가 물리적인 *스택*에 존재한다고 요구하지 않습니다.

| 표현 | 관리 방식 | 주의점 |
|---|---|---|
| `std::array<int, N>` | 고정 크기 요소가 객체 내부에 포함 | 큰 배열의 자동 저장은 스택 용량 문제를 일으킬 수 있음 |
| `std::vector<int>` | 컨테이너 객체와 별도로 연속 요소 저장소 관리 | 요소 증가 시 재할당 가능 |
| `std::unique_ptr<T>` | 동적 객체에 대한 단일 소유권 관리 | 소유권 이동 후 기존 포인터 사용 금지 |

`new`가 빠를지 느릴지는 호출 횟수와 할당기, 객체 크기에 따라 달라집니다. 여기서 중요한 것은 **불필요한 할당을 줄이되 수명과 소유권을 해치지 않는 설계**입니다.

**예제 코드 — [02_lifetime_and_storage.cpp](./examples/02_lifetime_and_storage.cpp)**

```cpp
#include <array>
#include <iostream>
#include <memory>
#include <vector>

int main() {
    const std::array<int, 3> fixed{2, 4, 6};
    const std::vector<int> dynamic{3, 6, 9};
    auto owned = std::make_unique<int>(12);
    std::cout << "Fixed: " << fixed[0] << ", Dynamic: " << dynamic[1]
              << ", Owned: " << *owned << "\n";
}
```

**실행 결과**

```text
Fixed: 2, Dynamic: 6, Owned: 12
```

`std::vector` 변수 자체가 지역 변수여도 요소 저장소는 별도로 할당될 수 있습니다. 메모리 누수 방지에는 Chapter 12의 RAII가 기본입니다.

---

<a id="section-15-3"></a>
## 15.3. `std::vector::reserve()` — 재할당 줄이기

`std::vector`의 `size()`는 현재 요소 개수이고 `capacity()`는 재할당 없이 저장할 수 있는 요소 수입니다. `push_back()` 중 용량이 부족하면 저장소가 재할당될 수 있고 기존 Iterator, Pointer, Reference가 무효화됩니다.

**추가될 원소 수를 합리적으로 예상할 수 있다면** `reserve()`를 고려할 수 있습니다. 다만 모든 `push_back()` 직전에 `reserve(size()+1)`을 호출하면 성장 전략을 방해하고 성능을 악화시킬 수도 있습니다.

```cpp
std::vector<int> readings;
readings.reserve(expected_count);  // 원소는 아직 0개
```

`reserve()`는 `size()`를 증가시키지 않고, 요청한 용량 *이상*을 확보합니다. 정확한 `capacity()` 수치는 구현마다 다를 수 있습니다.

**예제 코드 — [03_vector_reserve.cpp](./examples/03_vector_reserve.cpp)**

```cpp
#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings;
    readings.reserve(8);
    const int* const initial = readings.data();
    for (int index = 0; index < 8; ++index) readings.push_back(index * 2);
    std::cout << "Size: " << readings.size() << ", Capacity enough: "
              << std::boolalpha << (readings.capacity() >= 8) << "\n";
    std::cout << "Buffer unchanged: " << (readings.data() == initial) << "\n";
}
```

**실행 결과**

```text
Size: 8, Capacity enough: true
Buffer unchanged: true
```

예제는 `reserve(8)` 후 8개 요소만 추가하므로 버퍼 주소가 유지됩니다. `data()` 주소를 확보한 뒤 재할당이 일어나면 기존 주소를 계속 사용해서는 안 됩니다.

---

<a id="section-15-4"></a>
## 15.4. Cache Locality — 연속 데이터 접근

CPU는 메모리의 데이터를 캐시 라인 단위로 가져와 처리할 수 있습니다. 자주 함께 접근하는 값이 가까운 주소에 있으면 캐시를 효율적으로 활용할 가능성이 있습니다.

| 저장 형태 | 특징 | 적합한 상황 |
|---|---|---|
| `std::vector<T>` | 요소가 연속 배치 | 인덱스 접근과 순차 순회 |
| `std::list<T>` | 요소가 노드로 개별 저장 | 특정 위치에 Iterator가 있고 삽입·삭제가 빈번한 경우 |

Big-O만으로 실제 성능이 결정되지는 않습니다. 예를 들어 `std::list`의 중간 요소 삽입이 O(1)이더라도 **삽입 위치를 찾는 비용**과 노드 할당 비용을 함께 봐야 합니다. `std::vector`가 많은 작업에서 유리할 수 있지만 항상 빠르다고 단정하지 않습니다.

**예제 코드 — [04_contiguous_traversal.cpp](./examples/04_contiguous_traversal.cpp)**

```cpp
#include <iostream>
#include <list>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> contiguous{1, 2, 3, 4, 5};
    const std::list<int> linked{1, 2, 3, 4, 5};
    const int vector_total = std::accumulate(contiguous.begin(), contiguous.end(), 0);
    const int list_total = std::accumulate(linked.begin(), linked.end(), 0);
    std::cout << "Vector: " << vector_total << ", List: " << list_total << "\n";
}
```

**실행 결과**

```text
Vector: 15, List: 15
```

두 자료구조에 같은 숫자를 저장해 합계가 동일함을 검증합니다. 시간 차이를 주장하려면 요소 수와 순회 횟수를 키운 별도 벤치마크가 필요합니다.

---

<a id="section-15-5"></a>
## 15.5. `std::span` — 복사 없는 연속 범위 전달

`std::span<T>`는 연속 메모리 구간을 가리키는 **비소유 View**입니다. 배열과 `std::vector` 등에 같은 함수를 적용하기 좋고, 호출할 때 요소 전체를 복사하지 않습니다. 타입에 크기가 포함되지 않는 동적 범위라면 길이도 함께 전달됩니다.

```cpp
[[nodiscard]] long long total(std::span<const int> values);
```

`std::span`은 원본을 소유하지 않습니다. 원본 Container의 수명이 끝나거나 재할당되면 `span`이 무효화될 수 있습니다. `const` 요소를 바라보는 View를 사용하면 함수가 요소를 수정하지 않는다는 의도가 명확해집니다.

**예제 코드 — [05_span_view.cpp](./examples/05_span_view.cpp)**

```cpp
#include <array>
#include <iostream>
#include <span>
#include <vector>

[[nodiscard]] long long total(std::span<const int> values) {
    long long result = 0;
    for (const int value : values) result += value;
    return result;
}
int main() {
    const std::array fixed{3, 5, 7};
    const std::vector dynamic{10, 20};
    std::cout << "Array: " << total(fixed) << ", Vector: " << total(dynamic) << "\n";
}
```

**실행 결과**

```text
Array: 15, Vector: 30
```

같은 `total()` 함수를 `std::array`와 `std::vector`에 적용합니다. View 자체가 데이터를 소유한다고 착각하지 않도록 주의합니다.

---

<a id="section-15-6"></a>
## 15.6. AoS와 SoA — 데이터 배치 선택

**Array of Structures(AoS)**는 레코드별로 값을 묶고, **Structure of Arrays(SoA)**는 필드별로 값을 모아 저장합니다.

```text
AoS: [ID1, 값1] [ID2, 값2] [ID3, 값3]
SoA: ID:  [ID1, ID2, ID3]
     값:  [값1, 값2, 값3]
```

장치 ID와 값이 항상 함께 필요하면 AoS가 구현하기 쉽습니다. 반대로 값 필드만 반복 계산한다면 SoA처럼 필요한 필드만 연속 순회하는 구성이 유리할 수 있습니다. 실제 선택에는 데이터 크기·사용 패턴·구조 변경 비용까지 고려해야 합니다.

**예제 코드 — [06_aos_soa.cpp](./examples/06_aos_soa.cpp)**

```cpp
#include <iostream>
#include <vector>

struct Reading { int device_id; int value; };
int main() {
    const std::vector<Reading> rows{{1, 10}, {2, 20}, {3, 30}};
    std::vector<int> ids;
    std::vector<int> values;
    ids.reserve(rows.size());
    values.reserve(rows.size());
    for (const Reading& item : rows) {
        ids.push_back(item.device_id);
        values.push_back(item.value);
    }
    int sum = 0;
    for (const int value : values) sum += value;
    std::cout << "Rows: " << ids.size() << ", Sum: " << sum << "\n";
}
```

**실행 결과**

```text
Rows: 3, Sum: 60
```

레코드를 필드별 벡터로 변환한 뒤 값의 합계를 구합니다. 자료구조를 바꾸기 전에 정말 특정 필드만 읽는지 프로파일링으로 확인합니다.

---

<a id="section-15-7"></a>
## 15.7. Alignment와 False Sharing — 데이터 경계

서로 다른 스레드가 서로 다른 변수만 수정하더라도 변수가 같은 캐시 라인에 있으면 캐시 일관성 때문에 성능이 떨어질 수 있습니다. 이 현상을 **False Sharing**이라고 부릅니다.

`alignas(64)`는 객체의 정렬 요구사항을 64바이트로 지정합니다. 다만 **실제 CPU 캐시 라인 크기가 반드시 64바이트인 것은 아닙니다.** 정렬만으로 모든 False Sharing 문제가 해결되는 것도 아닙니다.

C++17에는 `std::hardware_destructive_interference_size`가 도입되었으나 지원 여부와 값은 구현별로 다를 수 있습니다. 실제 병렬 처리 최적화는 먼저 Data Race가 없는지 확인하고, 그다음 캐시 관련 성능 지표를 측정합니다.

**예제 코드 — [07_false_sharing_layout.cpp](./examples/07_false_sharing_layout.cpp)**

```cpp
#include <cstddef>
#include <iostream>

// 64바이트는 설명용 정렬 예시이며, CPU의 캐시 라인 크기와 항상 같지는 않음.
struct alignas(64) PaddedCounter { int value{}; };
int main() {
    const PaddedCounter counters[2]{{10}, {20}};
    std::cout << std::boolalpha << "Alignment >= 64: "
              << (alignof(PaddedCounter) >= 64) << "\n";
    std::cout << "Values: " << counters[0].value + counters[1].value << "\n";
}
```

**실행 결과**

```text
Alignment >= 64: true
Values: 30
```

이 예제는 정렬의 의미를 보여주는 **레이아웃 데모**입니다. 두 스레드를 경쟁시키는 성능 실험이 아니며 캐시 적중률을 측정하지 않습니다.

---

<a id="section-15-8"></a>
## 15.8. 메모리 접근 순서 — Row-Major와 Column-Major

2차원 배열에서 C++의 일반적인 `T array[R][C]` 배치는 **행(Row)** 의 요소가 연속인 Row-Major 형태입니다. 따라서 안쪽 반복문이 열 인덱스를 증가시키는 순회는 인접 메모리를 접근합니다.

수학적으로 두 순회는 같은 원소를 방문하므로 합계가 동일하지만, 실제 접근 패턴은 다릅니다. 배열의 크기가 작으면 차이가 거의 없을 수도 있고, 큰 배열에서 차이가 커질 수도 있습니다. 반복 순서를 변경할 때는 계산 의존성과 정수 오버플로 가능성도 확인해야 합니다.

**예제 코드 — [08_row_major_access.cpp](./examples/08_row_major_access.cpp)**

```cpp
#include <array>
#include <iostream>

int main() {
    const std::array<std::array<int, 3>, 2> matrix{{{{1, 2, 3}}, {{4, 5, 6}}}};
    int row_sum = 0;
    for (std::size_t row = 0; row < matrix.size(); ++row)
        for (std::size_t col = 0; col < matrix[row].size(); ++col)
            row_sum += matrix[row][col];
    int column_sum = 0;
    for (std::size_t col = 0; col < matrix[0].size(); ++col)
        for (std::size_t row = 0; row < matrix.size(); ++row)
            column_sum += matrix[row][col];
    std::cout << "Row-first: " << row_sum << ", Column-first: " << column_sum << "\n";
}
```

**실행 결과**

```text
Row-first: 21, Column-first: 21
```

작은 2×3 행렬을 두 순서로 모두 합산합니다. **출력의 일치**는 확인하지만 어느 쪽이 빠른지는 이 데모만으로 판정할 수 없습니다.

---

<a id="section-15-9"></a>
## 15.9. `std::pmr::monotonic_buffer_resource` — 일괄 수명 관리

`std::pmr`(Polymorphic Memory Resource)는 메모리 할당 전략을 Container의 실제 구현에서 분리합니다. `std::pmr::monotonic_buffer_resource`는 여러 할당을 빠르게 제공하고, 개별 블록 해제 대신 **자원 전체의 수명이 끝날 때 일괄 반환**하는 방식입니다.

읽기 전용 데이터 묶음처럼 *함께 생성하고 함께 폐기*하는 작업에 적합할 수 있습니다. 반대로 개별 데이터를 장기간 유지하거나 자주 삭제하는 용도에는 메모리 소비가 커질 수 있습니다.

- 자원(Resource)은 이를 참조하는 `pmr` Container보다 오래 살아 있어야 합니다.
- `release()`를 호출하면 기존 할당 저장소가 무효화되므로, 살아 있는 Container의 요소에 접근해서는 안 됩니다.
- `monotonic_buffer_resource` 자체는 Thread-Safe하지 않습니다. <https://en.cppreference.com/cpp/memory/monotonic_buffer_resource>

**예제 코드 — [09_pmr_monotonic.cpp](./examples/09_pmr_monotonic.cpp)**

```cpp
#include <array>
#include <cstddef>
#include <iostream>
#include <memory_resource>
#include <vector>

int main() {
    alignas(std::max_align_t) std::array<std::byte, 4096> buffer{};
    // 버퍼가 부족하면 예외를 던지도록 업스트림 할당 금지.
    std::pmr::monotonic_buffer_resource arena{
        buffer.data(), buffer.size(), std::pmr::null_memory_resource()};
    std::pmr::vector<int> data{&arena};
    data.reserve(5);
    for (int value = 1; value <= 5; ++value) data.push_back(value);
    std::cout << "Items: " << data.size() << ", Last: " << data.back() << "\n";
    // arena는 data보다 먼저 생성되어 더 늦게 파괴됨.
}
```

**실행 결과**

```text
Items: 5, Last: 5
```

고정된 버퍼와 `null_memory_resource()`를 함께 사용하여 추가 할당이 허용되지 않는 경우를 구성합니다. 버퍼가 부족하다면 할당 실패 예외가 발생할 수 있습니다.

---

<a id="section-15-10"></a>
## 15.10. Pool Allocator — 반복 할당 비용 다루기

Pool 자원은 비슷한 크기의 메모리 블록을 반복해서 사용할 때 검토할 수 있습니다. `std::pmr::unsynchronized_pool_resource`는 동기화 없이 메모리 풀을 관리하며 **여러 스레드에서 같은 자원에 동시에 접근할 목적으로 사용하면 안 됩니다.** 스레드 간 공유가 필요하면 `synchronized_pool_resource` 등 적절한 대안을 검토합니다.

Pool을 도입한다고 반드시 할당이 줄거나 처리 속도가 개선되는 것은 아닙니다. 실제 반복 할당 횟수, 블록 크기, 피크 메모리 사용량을 함께 측정해야 합니다.

**예제 코드 — [10_pmr_pool.cpp](./examples/10_pmr_pool.cpp)**

```cpp
#include <iostream>
#include <memory_resource>
#include <vector>

int main() {
    std::pmr::unsynchronized_pool_resource pool;
    std::pmr::vector<int> first{&pool};
    std::pmr::vector<int> second{&pool};
    first.push_back(7);
    second.push_back(9);
    std::cout << "Pool values: " << first.front() << ", " << second.front() << "\n";
    // Pool은 컨테이너보다 오래 살아야 함. 이 자원은 동시 사용에 안전하지 않음.
}
```

**실행 결과**

```text
Pool values: 7, 9
```

두 `std::pmr::vector`가 하나의 Pool 자원을 사용합니다. Pool과 이를 참조하는 Container의 소멸 순서를 확인합니다.

---

<a id="section-15-11"></a>
## 15.11. 탐색 자료구조와 계산 복잡도

여러 키를 반복 조회할 때는 단일 연산의 비용보다 **전체 작업 횟수**를 먼저 봅니다.

| 접근 방식 | 조회 복잡도 | 메모리 특성 |
|---|---|---|
| `std::vector` 선형 검색 | O(n) | 연속 배치, 상대적으로 작은 오버헤드 |
| 정렬된 `std::vector` + Binary Search | O(log n) | 초기 정렬 O(n log n) 필요 |
| `std::unordered_set` / `unordered_map` | 평균 O(1), 최악 O(n) | 해시 버킷·노드 오버헤드 |
| `std::map` | O(log n) | 정렬된 키 순회 가능, 노드 오버헤드 |

조회가 한 번뿐이라면 Hash Table을 만드는 비용이 더 클 수 있습니다. 입력 데이터의 **중복도, 키 분포, 조회 횟수**에 따라 기준 구현과 대안을 비교해야 합니다.

**예제 코드 — [11_lookup_structure.cpp](./examples/11_lookup_structure.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <unordered_set>
#include <vector>

int main() {
    const std::vector<int> ids{4, 2, 8, 2, 7};
    const std::unordered_set<int> lookup(ids.begin(), ids.end());
    const bool linear = std::find(ids.begin(), ids.end(), 7) != ids.end();
    const bool hashed = lookup.contains(7);  // C++20
    std::cout << std::boolalpha << "Vector found: " << linear
              << ", Hash found: " << hashed << "\n";
}
```

**실행 결과**

```text
Vector found: true, Hash found: true
```

`std::vector`와 `std::unordered_set`에서 같은 키를 찾는 예제입니다. `std::unordered_set::contains()`는 C++20 기능입니다.

---

<a id="section-15-12"></a>
## 15.12. 복사, 이동, View — 데이터 전달 비용

큰 데이터를 읽기만 하는 API는 `const T&` 또는 `std::span<const T>` 같은 비소유 인터페이스를 사용할 수 있습니다. 문자열 구간에는 `std::string_view`가 유용하며 복사 없이 문자 데이터를 바라볼 수 있습니다.

하지만 View는 데이터를 소유하지 않으므로 수명 문제를 만들기 쉽습니다. 반환값으로 새 소유권이 필요하면 값 반환과 Move/Copy Elision을 우선 고려합니다. 단순히 `std::move`를 붙여 **무조건 빠르다고 믿거나, 이미 최적화되는 반환에 불필요하게 추가하는 것**은 피해야 합니다.

**예제 코드 — [12_copy_and_view.cpp](./examples/12_copy_and_view.cpp)**

```cpp
#include <iostream>
#include <string>
#include <string_view>

[[nodiscard]] std::size_t length(std::string_view text) { return text.size(); }
int main() {
    std::string owned{"sensor-name"};
    std::string copied = owned;
    std::string_view borrowed = owned;
    std::cout << "Copy size: " << copied.size()
              << ", View size: " << length(borrowed) << "\n";
    // borrowed는 owned보다 오래 사용하지 않음.
}
```

**실행 결과**

```text
Copy size: 11, View size: 11
```

문자열 복사본과 View의 길이를 비교합니다. `borrowed`는 원본 `owned`의 수명 안에서만 사용합니다.

---

<a id="section-15-13"></a>
## 15.13. 표준 Algorithm과 Ranges — 명확한 순회

C++20 Ranges의 `std::views::filter`, `transform` 등은 기존 입력을 즉시 새 Container로 복사하기보다 필요한 요소를 순회하는 **지연 평가 View**를 만들 수 있습니다.

```cpp
auto nonnegative = data | std::views::filter([](int value) { return value >= 0; });
```

View를 여러 번 순회하거나 기반 Container를 변경하면 예상과 다른 비용·수명 문제가 생길 수 있습니다. 알고리즘 선택은 코드의 의도와 정확성을 먼저 고려하고, **실제 병목이 확인된 부분에서** 최적화해야 합니다.

**예제 코드 — [13_algorithm_pipeline.cpp](./examples/13_algorithm_pipeline.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <ranges>
#include <vector>

int main() {
    const std::vector<int> samples{3, -1, 8, 0, 4};
    auto nonnegative = samples | std::views::filter([](int value) { return value >= 0; });
    int total = 0;
    for (int value : nonnegative) total += value;
    std::cout << "Nonnegative sum: " << total << "\n";
}
```

**실행 결과**

```text
Nonnegative sum: 15
```

음수가 아닌 원소를 Filter View로 순회한 합계를 구합니다. 별도 결과 벡터를 만들지 않는다고 항상 더 빠른 것은 아닙니다.

---

<a id="section-15-14"></a>
## 15.14. Benchmark — `std::chrono::steady_clock`

`std::chrono::steady_clock`은 시간 간격 측정에 사용하기 좋은 단조 시계입니다. 다만 타이머 API를 호출했다고 결과가 곧바로 신뢰할 수 있는 벤치마크가 되는 것은 아닙니다.

**권장 절차:** 동일 환경의 Release 빌드 → 동일 입력 → 워밍업 → 여러 번 반복 → 중앙값 비교 → 출력·Checksum 검증 → 입력 크기별 재측정.

측정 구간 밖에서 데이터 생성과 출력 작업을 수행하는 등 **무엇을 포함할지** 일정하게 유지해야 합니다. 컴파일러가 사용하지 않는 계산을 제거할 수 있으므로 계산 결과는 실제로 관찰 가능한 형태로 사용해야 합니다. 비정상적으로 빠른 측정값만 보고 결론을 내리지 않습니다.

**예제 코드 — [14_steady_clock_benchmark.cpp](./examples/14_steady_clock_benchmark.cpp)**

```cpp
#include <chrono>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> values(1000, 2);
    constexpr int repetitions = 5;
    long long checksum = 0;
    for (int trial = 0; trial < repetitions; ++trial) {
        const auto start = std::chrono::steady_clock::now();
        checksum += std::accumulate(values.begin(), values.end(), 0LL);
        const auto elapsed = std::chrono::steady_clock::now() - start;
        (void)elapsed; // 실제 측정 시 여러 반복의 분포를 기록하고 분석할 것.
    }
    std::cout << "Trials: " << repetitions << ", Checksum: " << checksum << "\n";
}
```

**실행 결과**

```text
Trials: 5, Checksum: 10000
```

시간 측정 구간과 Checksum 유지 방법을 보여줍니다. 테스트의 출력은 재현 가능하도록 횟수와 합계만 표시하고, 나노초/밀리초 수치는 출력하지 않습니다.

---

<a id="section-15-15"></a>
## 15.15. 정수 범위와 검증 — 빠른 코드도 안전해야 함

최적화 과정에서 누적 합계를 좁은 정수형으로 바꾸면 오버플로가 발생할 수 있습니다. 특히 **signed integer overflow는 정의되지 않은 동작**이므로 계산 이전에 범위를 검증해야 합니다.

입력 크기와 값의 상한을 문서화하고, 누적 합계는 `long long`처럼 범위를 고려한 타입을 사용합니다. 그러나 넓은 타입이라도 무한정 안전한 것은 아니므로 상한이 불명확하면 checked arithmetic을 적용합니다.

구현을 빠르게 만드는 것보다 **최적화 전후에 잘못된 입력을 같은 방식으로 처리하는지** 확인하는 일이 더 중요합니다.

**예제 코드 — [15_checked_integer.cpp](./examples/15_checked_integer.cpp)**

```cpp
#include <iostream>
#include <limits>
#include <optional>

[[nodiscard]] std::optional<long long> checked_add(long long a, long long b) {
    constexpr long long highest = std::numeric_limits<long long>::max();
    constexpr long long lowest = std::numeric_limits<long long>::min();
    if ((b > 0 && a > highest - b) || (b < 0 && a < lowest - b))
        return std::nullopt;
    return a + b;
}
int main() {
    const auto safe = checked_add(20, 30);
    const auto overflow = checked_add(std::numeric_limits<long long>::max(), 1);
    std::cout << "Safe: " << *safe << ", Overflow rejected: "
              << std::boolalpha << !overflow.has_value() << "\n";
}
```

**실행 결과**

```text
Safe: 50, Overflow rejected: true
```

덧셈 이전에 상한과 하한을 확인하여 오버플로를 거부하는 `checked_add()` 예제입니다.

---

<a id="section-15-16"></a>
## 15.16. 정렬 인덱스와 재사용 — 전처리 비용 계산

정렬된 시퀀스에서 `std::binary_search`, `std::lower_bound`, `std::equal_range`를 이용하면 조회를 O(log n)으로 처리할 수 있습니다. 다만 **정렬 O(n log n)** 비용을 먼저 치러야 하므로 조회가 거의 없다면 불리할 수 있습니다.

반복 조회가 많은 정적 데이터에는 정렬된 벡터가 공간 효율적인 선택이 될 수 있습니다. 데이터가 빈번히 변경되면 `std::map`·Hash Table 등 대안도 비교합니다. 작은 입력, 이미 정렬된 입력, 중복이 많은 입력을 나누어 테스트합니다.

**예제 코드 — [16_sorted_index.cpp](./examples/16_sorted_index.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> ids{9, 3, 12, 3, 5};
    std::ranges::sort(ids);
    const bool contains = std::binary_search(ids.begin(), ids.end(), 5);
    const auto range = std::equal_range(ids.begin(), ids.end(), 3);
    std::cout << std::boolalpha << "Has 5: " << contains
              << ", Count 3: " << (range.second - range.first) << "\n";
}
```

**실행 결과**

```text
Has 5: true, Count 3: 2
```

중복이 포함된 ID를 정렬하고 존재 여부와 특정 값의 개수를 확인합니다. 결과를 Iterator 차이로 얻기 위해 정렬된 상태가 선행되어야 합니다.

---

<a id="section-15-17"></a>
## 15.17. Profiling과 Performance Regression

Benchmark는 **얼마나 걸리는가**를 측정하고, Profiler는 **어디서 시간이 소비되는가**를 찾는 데 도움을 줍니다. 전체 처리 시간이 긴데도 작은 함수 하나만 최적화한다면 실제 개선 폭은 작을 수 있습니다.

### 성능 측정 순서

1. 기준 구현의 결과를 자동 테스트로 고정합니다. 오류 입력 및 경계값도 함께 검증합니다.
2. Release 빌드를 사용하고 입력 크기, 반복 횟수, 환경을 기록합니다.
3. 처리 시간을 여러 번 재측정하고 중앙값을 비교합니다.
4. Profiler로 시간이 몰리는 함수와 할당 패턴을 확인한 뒤 자료구조나 순회 방식 하나를 변경합니다.
5. 다시 같은 테스트와 성능 측정을 진행합니다. 속도 증가와 메모리 증가를 함께 기록합니다.

### 도구 선택

| 목적 | 도구 예시 | 유의 사항 |
|---|---|---|
| 시간 측정 | `std::chrono::steady_clock` | 반복 측정 및 결과 검증 필요 |
| CPU 병목 분석 | Linux `perf`, Visual Studio Profiler | 운영체제와 권한 설정에 따라 사용 가능 여부 다름 |
| 메모리 오류 검사 | AddressSanitizer, UndefinedBehaviorSanitizer | 성능 벤치마크와 별도 빌드 권장 |
| 메모리 사용량 분석 | Heap Profiler, 운영체제별 프로세스 분석 도구 | RSS·할당량·피크 메모리를 구분 |

GCC 또는 Clang에서 메모리/정의되지 않은 동작 검사를 시도할 수 있습니다.

```bash
g++ -std=c++20 -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer \
    examples/05_span_view.cpp -o sanitize_demo
./sanitize_demo
```

Sanitizer를 적용한 바이너리의 처리 시간을 일반 Release 빌드와 직접 비교해서는 안 됩니다. 다음 장인 Chapter 17에서 테스트와 프로파일링을 더 자세히 다룹니다.

### 병목 비교 예시

센서 입력이 n개이고 서로 다른 장치가 d개인 경우, 장치별 누적 합계를 반복 선형 검색으로 구성하면 최악 O(n·d)번의 탐색이 필요합니다. Hash Index를 사용하면 평균적으로 O(n) 삽입·검색을 기대할 수 있지만, 최종 보고서를 장치 ID 기준으로 정렬하는 O(d log d) 비용이 남습니다.

```text
기준 구현:     O(n·d + d log d)
최적화 구현:   평균 O(n + d log d), 해시 충돌의 최악 비용은 별도
추가 메모리:   두 방식 모두 장치별 집계 O(d), Hash Table은 별도 오버헤드
```

**이것은 알고리즘 비용 분석이지 실측 속도 보장이 아닙니다.** 이 비교를 실제 코드로 검증하는 과제가 15.19 Mini Project입니다.

---

<a id="section-15-18"></a>
## 15.18. Coding Practice

기본 구현을 정확히 완성한 뒤 필요한 메모리 할당이나 복사 횟수를 줄이는 연습입니다. 학생용 파일과 모범답안을 구분하고, 테스트는 함수의 실제 결과와 예외 입력을 검증합니다.

### 실습 ① — Reserve & Squares

**문제**

정수 `count`를 입력받아 `0², 1², 2², ...`의 결과를 순서대로 저장한 `std::vector<int>`를 반환합니다. 입력 범위는 `0 ≤ count ≤ 10,000`입니다.

**구현 조건**

`std::vector<int> make_squares(std::size_t count)`를 작성합니다. 크기가 정해졌다면 `reserve(count)`로 재할당을 줄이고, 원소를 하나씩 추가합니다. `count = 0`일 때 빈 벡터를 반환해야 합니다.

**입출력 예시**

```text
Count: 5
Last: 16
```

[학생용 코드](./exercises/01_reserve_squares.cpp) · [모범답안](./solutions/01_reserve_squares.cpp)

<details>
<summary>구현 가이드</summary>

컨테이너를 만들고 `reserve(count)`를 호출합니다. `reserve()`는 값을 채우지 않으므로 반드시 `push_back()` 등으로 원소를 추가해야 합니다.

</details>

**검증 사항:** 0개, 1개, 1,000개, 순서, 마지막 값, `size()` 확인

### 실습 ② — Span Statistics

**문제**

기존 배열이나 벡터의 값을 복사하지 않고 통계값을 계산합니다. 빈 입력을 별도로 처리하고, 평균은 정수 나눗셈이 되지 않게 합니다.

**구현 조건**

`std::optional<Stats> analyze(std::span<const int> values)`를 작성합니다. `Stats`는 최솟값, 최댓값, 실수 평균을 포함하며 빈 입력은 `std::nullopt`입니다. `long long` 누적 합계로 일반적인 범위 초과 가능성을 줄입니다.

**입출력 예시**

```text
Min: 10, Max: 30, Average: 20
```

[학생용 코드](./exercises/02_span_statistics.cpp) · [모범답안](./solutions/02_span_statistics.cpp)

<details>
<summary>구현 가이드</summary>

`std::minmax_element`로 양 끝 값을 찾고, 합계는 별도로 순회합니다. `values.size()`가 0인지 먼저 확인합니다.

</details>

**검증 사항:** 빈 입력, 하나의 값, 음수 혼합, 큰 정수의 평균

### 실습 ③ — PMR Filtered Buffer

**문제**

이미 생성된 `std::pmr::vector<int>` 뒤에 유효한 측정값만 추가합니다. 기존 데이터와 메모리 자원 연결을 보존해야 합니다.

**구현 조건**

`void append_valid(std::pmr::vector<int>& output, std::span<const int> input)`를 작성합니다. 0~100 범위의 값만 추가하며 기존 값은 제거하지 않습니다.

**입출력 예시**

```text
Accepted: 2
```

[학생용 코드](./exercises/03_pmr_filtered.cpp) · [모범답안](./solutions/03_pmr_filtered.cpp)

<details>
<summary>구현 가이드</summary>

입력 요소를 하나씩 검사한 다음 유효한 값만 `output.push_back(value)`를 호출합니다. 새로운 메모리 자원을 생성할 필요는 없습니다.

</details>

**검증 사항:** 빈 입력, 0과 100 경계, 기존 데이터 보존, Allocator 유지

### 실습 ④ — Sorted Unique Index

**문제**

정수 ID가 중복·무순서로 기록되어 있습니다. 원본 데이터는 변경하지 않고, 오름차순 정렬된 고유 ID 목록을 생성합니다.

**구현 조건**

`std::vector<int> unique_sorted(std::span<const int> input)`를 완성합니다. 복사본을 정렬하고 중복을 제거해 반환합니다.

**입출력 예시**

```text
Unique: 3
```

[학생용 코드](./exercises/04_sorted_unique.cpp) · [모범답안](./solutions/04_sorted_unique.cpp)

<details>
<summary>구현 가이드</summary>

입력을 `std::vector`로 복사한 후 `std::ranges::sort`, `std::unique`와 `erase`를 조합합니다. 정렬 없이 `std::unique`만 사용하면 떨어져 있는 중복은 제거되지 않습니다.

</details>

**검증 사항:** 빈 입력, 모든 값이 동일, 음수 ID, 원본 불변

**실습 검증**

```bash
python3 tests/check.py --mode student --only exercise-01
python3 tests/check.py --mode student --only exercise-02
python3 tests/check.py --mode student --only exercise-03
python3 tests/check.py --mode student --only exercise-04
```

---

<a id="section-15-19"></a>
## 15.19. Mini Project — Sensor Batch Analyzer

### 프로젝트 배경

서로 다른 장치에서 수집된 센서 측정값을 처리하는 프로그램이 있습니다. 기존 코드는 새 데이터가 들어올 때마다 이미 기록된 장치 목록을 처음부터 확인합니다. 장치와 데이터가 적으면 문제가 없지만, 입력 행과 장치 수가 증가하면서 집계 시간이 늘어나고 있습니다.

기존 프로그램의 계산 결과를 유지하면서 탐색 자료구조를 변경하고, 두 구현의 실행 시간을 동일한 입력으로 비교하는 프로그램을 작성하세요. 성능이 좋아졌다는 주장보다 **정확한 결과와 재현 가능한 측정 과정**을 먼저 확보하는 것이 목표입니다.

### 구현 조건

1. 입력 `Reading{device_id, value}`를 원본 순서대로 처리합니다. 장치 ID가 0 이하이거나 측정값이 0~100 범위를 벗어나면 거부 건수에 반영하고 합계에서는 제외합니다.
2. **기준 구현:** `std::vector<DeviceStat>`의 장치 ID를 선형 검색하여 장치별 건수와 합계를 갱신합니다.
3. **최적화 구현:** `std::unordered_map<int, DeviceStat>` 등 장치 ID 기반 인덱스를 사용하여 탐색 비용을 줄입니다.
4. 두 구현 모두 최종 장치별 결과를 **장치 ID 오름차순**으로 정렬합니다. 해시 컨테이너의 순회 순서에 의존하지 않습니다.
5. 출력 보고서는 유효 건수, 거부 건수, 전체 합계, 장치별 건수·합계로 구성합니다. `long long`으로 합산하되 과제의 입력 크기는 최대 1,000,000행, 유효 금액은 행당 최대 100입니다.
6. 동일 입력에서 두 구현의 `Report`가 같아야 합니다. 빈 입력, 잘못된 장치 ID, 음수·101, 0·100 경계값, 중복 장치를 테스트합니다.
7. 10만 행 이상으로 성능을 측정하고 환경·반복 횟수·메모리 비용을 기록합니다. **측정 시간 자체는 정답 조건이나 CI 통과 조건으로 사용하지 않습니다.**

### 제공 파일

| 위치 | 구성 |
|---|---|
| [`project/`](./project/) | 학생용 프로젝트. `src/analyzer.cpp`의 두 함수를 완성 |
| [`solutions/sensor_batch_analyzer/`](./solutions/sensor_batch_analyzer/) | 모범답안과 테스트 |
| [`examples/17_sensor_batch_analyzer/`](./examples/17_sensor_batch_analyzer/) | 실행 가능한 예제 및 CMake·CTest |
| [`PERFORMANCE.md`](./PERFORMANCE.md) | 10만 행 성능 측정 기록 양식 |
| [`tests/check.py`](./tests/check.py) | 단일 예제·실습·프로젝트 기능 검증 |

주요 인터페이스:

```cpp
namespace sensor {
struct Reading { int device_id; int value; };
struct DeviceStat { int device_id; std::size_t count; long long total; };
struct Report { /* 장치별 정렬 목록, accepted, rejected, total */ };
Report analyze_reference(std::span<const Reading>);
Report analyze_optimized(std::span<const Reading>);
}
```

### 입출력 예시

```text
Devices: 3
Accepted: 5, Rejected: 2
Total: 125
Matches: true
```

### CMake 빌드 및 테스트

`Chapter-15/` 기준입니다.

```bash
cmake -S examples/17_sensor_batch_analyzer -B build/ch15 -DCMAKE_CXX_STANDARD=20 -DCMAKE_BUILD_TYPE=Release
cmake --build build/ch15 --parallel 2
ctest --test-dir build/ch15 --output-on-failure
./build/ch15/sensor_batch_analyzer --benchmark 100000
```

학생용 프로젝트를 완성했다면 `-S project`로, 모범답안만 검증하려면 `-S solutions/sensor_batch_analyzer`로 변경할 수 있습니다. Windows Visual Studio 생성기는 `--config Release`와 해당 구성의 실행 파일 경로를 사용합니다.

<details>
<summary>구현 가이드</summary>

**STEP 01 — 기준 구현**

유효성을 검사한 뒤 벡터에서 같은 장치 ID를 찾습니다. 없으면 새로 추가하고, 있으면 건수와 합계를 갱신합니다.

```cpp
auto it = std::find_if(report.devices.begin(), report.devices.end(),
                       [&](const sensor::DeviceStat& item) {
                           return item.device_id == reading.device_id;
                       });
```

**STEP 02 — Hash Index 구성**

`std::unordered_map`에서 장치 ID를 키로 사용합니다. `try_emplace()`로 항목을 생성하거나 조회하고, 결과를 벡터로 옮겨 마지막에 정렬합니다.

```cpp
std::unordered_map<int, sensor::DeviceStat> index;
// 장치 ID별 갱신 후 표준 정렬 알고리즘으로 출력 순서를 통일
```

**STEP 03 — 정확성·성능 비교**

두 결과를 동일한 입력으로 비교한 뒤 시간을 측정합니다. 결과가 다르면 시간 비교보다 오류 원인을 먼저 수정합니다.

</details>

### 검증 사항

- 입력을 뒤집어도 장치별 집계와 정렬된 결과가 유지되는지 확인
- 0 이하 ID, 음수·100 초과 값이 거부 건수에만 반영되는지 확인
- 빈 입력, 유효 값 0과 100, 다수의 중복 장치 검증
- 10만 행 데이터에서 기준 구현과 최적화 구현의 결과 일치 여부 확인
- 측정 환경, 입력 규모와 반복 횟수, 중앙값, 메모리 비용을 구분하여 기록

---

<a id="section-15-20"></a>
## 15.20. Quiz & Summary

### Quiz

<details>
<summary>Q1. `reserve()`와 `resize()`의 가장 큰 차이는?</summary>

`reserve()`는 용량 확보만 하고 크기를 늘리지 않습니다. `resize()`는 원소 수를 바꾸며 필요한 경우 원소를 생성·소멸시킵니다.

</details>

<details>
<summary>Q2. `std::vector`의 요소 주소를 저장한 후 `push_back()`을 계속 호출해도 안전한가요?</summary>

용량 초과로 재할당되면 기존 포인터·참조·Iterator가 무효화될 수 있습니다. 유지가 필요하면 설계를 바꾸거나 용량을 미리 확보합니다.

</details>

<details>
<summary>Q3. 순회만 하는 데이터에서 `std::list`가 `std::vector`보다 항상 빠를까요?</summary>

아닙니다. 연속 메모리 접근과 캐시 효율 때문에 `std::vector`가 유리할 수 있습니다. 실제 조건으로 측정해야 합니다.

</details>

<details>
<summary>Q4. `std::span`에 담긴 원본 데이터는 누가 해제하나요?</summary>

`std::span`은 비소유 View이므로 원본 Container 등 소유자가 수명을 관리합니다. 원본이 소멸하거나 재할당되면 View는 무효화됩니다.

</details>

<details>
<summary>Q5. AoS와 SoA는 어느 상황에서 구분하나요?</summary>

모든 필드를 함께 사용하는지, 특정 필드만 대량 순회하는지에 따라 배치의 캐시 효율이 달라질 수 있습니다.

</details>

<details>
<summary>Q6. `alignas(64)`는 모든 CPU에서 False Sharing을 없애나요?</summary>

아닙니다. 64바이트는 정렬 요구사항일 뿐 실제 캐시 라인 크기와 공유 쓰기 패턴을 보장하지 않습니다.

</details>

<details>
<summary>Q7. `std::pmr::monotonic_buffer_resource::release()` 전에 확인해야 할 것은?</summary>

그 자원에서 할당한 메모리를 참조하는 살아 있는 객체·View가 더 이상 사용되지 않아야 합니다.

</details>

<details>
<summary>Q8. `std::pmr::unsynchronized_pool_resource`를 여러 스레드에서 동시에 사용해도 되나요?</summary>

동시 접근에 대한 동기화를 제공하지 않습니다. 별도 동기화 또는 `synchronized_pool_resource` 등을 검토해야 합니다.

</details>

<details>
<summary>Q9. `std::unordered_map` 조회는 언제나 O(1)인가요?</summary>

평균적으로 상수 시간 조회를 기대하지만, 해시 충돌이 심하면 최악 O(n)까지 증가할 수 있습니다.

</details>

<details>
<summary>Q10. 벤치마크에서 `std::chrono::steady_clock`만 사용하면 정확한 결론이 나오나요?</summary>

아닙니다. 최적화 빌드, 동일 입력, 워밍업, 반복 측정, 결과 사용, 환경 기록이 함께 필요합니다.

</details>

<details>
<summary>Q11. signed integer overflow가 성능 최적화에서 위험한 이유는?</summary>

정의되지 않은 동작이 발생할 수 있어 결과가 잘못되거나 컴파일러의 최적화 가정에 영향을 줍니다. 연산 전에 범위를 검사해야 합니다.

</details>

<details>
<summary>Q12. Sensor Batch Analyzer에서 Hash Index 결과를 다시 정렬하는 이유는?</summary>

`unordered_map`의 순회 순서는 보장되지 않습니다. 장치 ID 기준 오름차순 보고서를 얻으려면 결과를 별도로 정렬해야 합니다.

</details>

### Summary

- 성능 최적화는 **정확성 → 측정 → 개선 → 재검증** 순서로 접근합니다.
- 연속 저장소, 순회 패턴, 할당 횟수는 실제 성능에 영향을 줄 수 있습니다.
- `std::span`과 `std::string_view`는 복사를 줄일 수 있지만 수명 관리가 필요합니다.
- `std::pmr`는 특수한 메모리 사용 패턴에 유용할 수 있지만 자원 수명과 Thread Safety를 검토해야 합니다.
- Big-O는 알고리즘 성장률을 설명할 뿐 실제 시간·메모리 사용량을 보장하지 않습니다.
- 벤치마크 결과를 비교할 때 입력, 컴파일 옵션, 환경, 반복 횟수를 고정하고 중앙값을 기록합니다.

### References

- [cppreference — `std::vector::reserve`](https://en.cppreference.com/w/cpp/container/vector/reserve)
- [cppreference — `std::span`](https://en.cppreference.com/w/cpp/container/span)
- [cppreference — Memory Resources (`std::pmr`)](https://en.cppreference.com/w/cpp/memory)
- [cppreference — `std::chrono::steady_clock`](https://en.cppreference.com/w/cpp/chrono/steady_clock)
- [cppreference — `std::unordered_map`](https://en.cppreference.com/w/cpp/container/unordered_map)
- [ISO C++ — The Standard](https://isocpp.org/std/the-standard)

---

[← C++ 목차](../README.md) · [← Chapter 14](../Chapter-14/README.md)
