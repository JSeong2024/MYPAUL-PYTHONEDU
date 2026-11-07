# Chapter 10. Standard Library (STL)

C++ 표준 라이브러리의 Container, Iterator, Algorithm, Ranges를 활용한 데이터 관리와 처리 방법을 다룹니다. 순서가 있는 데이터와 Key 기반 조회, 정렬·검색, 집계, View와 메모리 안전성을 함께 살펴봅니다.

본 자료는 **C++23(ISO/IEC 14882:2024)** 을 기준으로 작성되었습니다. 일부 C++23 표준 라이브러리 기능은 컴파일러 및 구현 버전에 따라 지원 범위가 다를 수 있습니다.

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [10.1](#section-10-1) | 표준 라이브러리와 STL |
| [10.2](#section-10-2) | Container 선택과 시간 복잡도 |
| [10.3](#section-10-3) | Sequence Containers — `vector`, `deque`, `list` |
| [10.4](#section-10-4) | Ordered Associative Containers — `map`, `set` |
| [10.5](#section-10-5) | Unordered Containers — Hash 기반 조회 |
| [10.6](#section-10-6) | Container Adaptors — Queue, Stack, Priority Queue |
| [10.7](#section-10-7) | Iterator와 Half-Open Range |
| [10.8](#section-10-8) | 검색과 조건 검사 — `find_if`, `all_of` |
| [10.9](#section-10-9) | 정렬과 비교 규칙 — `sort`, `stable_sort` |
| [10.10](#section-10-10) | 조건부 삭제 — `erase_if`, Erase–Remove |
| [10.11](#section-10-11) | 변환과 수치 집계 — `transform`, `accumulate` |
| [10.12](#section-10-12) | Ranges & Views — 필터·변환·슬라이싱 |
| [10.13](#section-10-13) | C++23 — `std::ranges::to` |
| [10.14](#section-10-14) | 정렬된 데이터 검색 — Binary Search |
| [10.15](#section-10-15) | Transparent Lookup — 불필요한 Key 생성 방지 |
| [10.16](#section-10-16) | Iterator Invalidation과 메모리 안전 |
| [10.17](#section-10-17) | Mini Project — Device Event Summary |
| [10.18](#section-10-18) | 설계 시 참고 사항 |
| [10.19](#section-10-19) | Coding Practice |
| [10.20](#section-10-20) | Quiz & Summary |

---

<a id="section-10-1"></a>

## 10.1. 표준 라이브러리와 STL

C++의 표준 라이브러리(Standard Library)는 자료구조, 알고리즘, 입력·출력, 문자열, 메모리, 시간 처리 등 재사용 가능한 기능을 제공합니다. 표준 템플릿 라이브러리(Standard Template Library, STL)는 원래 **컨테이너(Container)·반복자(Iterator)·알고리즘(Algorithm)** 등을 중심으로 한 범용 라이브러리를 가리키며, 현대 C++ 표준 라이브러리 전체와 완전히 같은 뜻은 아닙니다.

| 구성 요소 | 역할 | 대표 요소 |
|---|---|---|
| Container | 데이터를 저장·관리 | `std::vector`, `std::map`, `std::unordered_map` |
| Iterator | 요소를 가리키고 순회 | `begin()`, `end()`, `std::back_inserter` |
| Algorithm | 검색·정렬·변환 등 | `std::ranges::sort`, `std::ranges::find_if` |
| 함수 객체(Function Object) | 호출 가능한 객체로 동작 | 람다, `std::less<>` |
| 범위(Range) | 순회 가능한 요소의 범위 | `std::vector`, `std::span`, View |
| 뷰(View) | 원본을 복사하지 않고 범위를 변형·관찰 | `std::views::filter`, `std::views::transform` |

**기본 원칙:** 저장에는 적절한 Container를 선택하고, 반복적인 데이터 처리에는 표준 Algorithm과 Range를 우선 검토합니다. 모든 작업에 새 자료구조를 직접 구현할 필요는 없습니다.

이 Chapter는 Chapter 06에서 다룬 `std::array`, `std::vector`, 문자열의 기본 조작을 확장하여 **컨테이너 선택, 반복자 사용 규칙, 알고리즘 조합과 자료구조의 성능 특성**을 중점적으로 다룹니다.

---

<a id="section-10-2"></a>

## 10.2. Container 선택과 시간 복잡도

Container는 요소 저장 방식, 순서 보장, 검색 비용, 요소 추가·삭제 방식이 다릅니다. 시간 복잡도(Time Complexity)는 입력 크기를 `n`이라고 했을 때 수행 비용이 증가하는 양상을 나타냅니다.

| Container | 순서·중복 | 주요 연산의 일반적 복잡도 | 선택 기준 |
|---|---|---|---|
| `std::vector` | 삽입 순서, 중복 허용 | 끝 추가 상각 평균(Amortized) `O(1)`, 중간 삽입 `O(n)` | 연속 메모리, 순차 접근 |
| `std::deque` | 순서, 중복 허용 | 양끝 추가·삭제 `O(1)`, 임의 접근 `O(1)` | 앞뒤에서 자주 작업 |
| `std::list` | 순서, 중복 허용 | 위치가 주어지면 삽입·삭제 `O(1)`, 탐색 `O(n)` | 노드 간 이동·연결 변경 |
| `std::map` | Key 정렬, 중복 Key 불가 | 검색·삽입·삭제 `O(log n)` | 정렬된 Key, 범위 검색 |
| `std::set` | 값 정렬, 중복 불가 | 검색·삽입·삭제 `O(log n)` | 중복 없는 정렬 데이터 |
| `std::unordered_map` | 순서 미보장, 중복 Key 불가 | 평균 `O(1)`, 최악 `O(n)` | Key 기반 조회·집계 |
| `std::unordered_set` | 순서 미보장, 중복 불가 | 평균 `O(1)`, 최악 `O(n)` | 빠른 중복 검사 |
| `std::queue` | FIFO | 앞 요소 조회·삭제 및 끝 추가 `O(1)` | 입력 순서대로 처리 |
| `std::stack` | LIFO | 끝 요소 조회·삭제 및 추가 `O(1)` | 최근 작업 먼저 처리 |
| `std::priority_queue` | 우선순위 | 최상위 조회 `O(1)`, 추가·삭제 `O(log n)` | 우선순위 기반 작업 |

`std::vector`의 amortized `O(1)`은 개별 `push_back()`이 항상 상수 시간이 걸린다는 뜻은 아닙니다. 저장 공간이 부족하면 더 큰 공간을 확보하고 기존 요소를 이동하는 재할당(Reallocation)이 발생할 수 있습니다.

`std::list`는 삽입 위치를 이미 알고 있을 때 유리할 수 있으나, 노드 탐색과 메모리 접근 특성 때문에 `std::vector`보다 항상 빠른 것은 아닙니다. 성능을 결정해야 한다면 실제 데이터 크기와 접근 패턴에서 측정해야 합니다.

---

<a id="section-10-3"></a>

## 10.3. Sequence Containers — `vector`, `deque`, `list`

**예제 코드 — [01_sequence_containers.cpp](./examples/01_sequence_containers.cpp)**

```cpp
#include <iterator>
#include <deque>
#include <list>
#include <print>
#include <vector>

int main() {
    std::vector<int> samples{20, 22, 19};
    samples.push_back(21);
    std::deque<int> pending{2, 3};
    pending.push_front(1);
    std::list<int> checkpoints{10, 30};
    checkpoints.insert(std::next(checkpoints.begin()), 20);

    std::println("Samples: {}", samples.size());
    std::println("First task: {}", pending.front());
    for (const int point : checkpoints) {
        std::println("Checkpoint: {}", point);
    }
}
```

**실행 결과**

```text
Samples: 4
First task: 1
Checkpoint: 10
Checkpoint: 20
Checkpoint: 30
```

순차 컨테이너(Sequence Container)는 요소의 순서를 유지합니다.

- **`vector`:** 연속 저장, 인덱스 접근 가능, 끝에서의 추가에 적합
- **`deque`:** 인덱스 접근 가능, 양끝 요소 추가·삭제에 적합
- **`list`:** 양방향 연결 리스트, 임의 인덱스 접근 불가

`std::list::insert`에는 삽입할 위치를 나타내는 Iterator를 전달합니다. Iterator를 찾는 과정까지 반드시 `O(1)`인 것은 아닙니다.

데이터가 연속 메모리에 있어야 하는 센서 버퍼·바이너리 데이터라면 일반적으로 `vector`가 우선 후보입니다. `list`는 사용 조건이 명확할 때 선택합니다.

---

<a id="section-10-4"></a>

## 10.4. Ordered Associative Containers — `map`, `set`

**예제 코드 — [02_ordered_containers.cpp](./examples/02_ordered_containers.cpp)**

```cpp
#include <map>
#include <print>
#include <set>
#include <string>

int main() {
    std::map<std::string, int> inventory{{"battery", 4}, {"camera", 2}};
    inventory.insert_or_assign("battery", 5);
    std::set<int> channel_ids{8, 3, 8, 5};

    for (const auto& [name, quantity] : inventory) {
        std::println("{}: {}", name, quantity);
    }
    std::println("Unique channels: {}", channel_ids.size());
    if (const auto it = channel_ids.lower_bound(4); it != channel_ids.end()) {
        std::println("First channel >= 4: {}", *it);
    }
}
```

**실행 결과**

```text
battery: 5
camera: 2
Unique channels: 3
First channel >= 4: 5
```

연관 컨테이너(Associative Container)는 Key 또는 값에 기반해 요소를 관리합니다. `std::map`은 Key와 Value를, `std::set`은 중복 없는 값을 저장합니다.

- **`insert_or_assign(key, value)`:** Key가 없으면 삽입, 이미 있으면 값 갱신
- **`at(key)`:** Key가 없으면 `std::out_of_range` 예외 발생
- **`find(key)`:** Key를 찾지 못하면 `end()` 반환
- **`lower_bound(key)`:** 정렬 순서상 지정한 Key보다 작지 않은 첫 위치 반환

기본 비교 규칙은 `std::less<Key>`입니다. 따라서 순회하면 Key 기준의 정렬 순서로 요소를 확인할 수 있습니다.

`operator[]`는 없는 Key에 접근하면 새 요소를 생성합니다. 조회만 필요할 때는 `find()`, `contains()`, `at()` 등을 사용하여 불필요한 삽입을 방지합니다.

---

<a id="section-10-5"></a>

## 10.5. Unordered Containers — Hash 기반 조회

**예제 코드 — [03_unordered_frequency.cpp](./examples/03_unordered_frequency.cpp)**

```cpp
#include <print>
#include <string>
#include <string_view>
#include <unordered_map>

int main() {
    const std::string_view events[]{"WARN", "INFO", "WARN", "ERROR", "INFO"};
    std::unordered_map<std::string, int> counts;
    counts.reserve(3);
    for (const auto event : events) {
        ++counts[std::string{event}];
    }
    std::println("INFO: {}", counts.at("INFO"));
    std::println("WARN: {}", counts.at("WARN"));
    std::println("ERROR: {}", counts.at("ERROR"));
    std::println("Contains DEBUG: {}", counts.contains("DEBUG"));
}
```

**실행 결과**

```text
INFO: 2
WARN: 2
ERROR: 1
Contains DEBUG: false
```

해시(Hash) 기반 Container는 Key를 Hash 값으로 변환하여 조회 위치를 결정합니다. `std::unordered_map`과 `std::unordered_set`은 정렬 순서를 보장하지 않습니다.

- **`contains(key)`:** Key 존재 여부 확인
- **`at(key)`:** 이미 존재하는 Key의 값 조회
- **`operator[]`:** 존재하지 않으면 기본값으로 생성·삽입
- **`reserve(n)`:** 예상 요소 개수에 맞춰 Bucket 용량 확보를 요청

요소 증가로 해시 테이블의 Bucket 구성이 달라지는 작업을 리해싱(Rehashing)이라고 합니다. Rehashing은 기존 Iterator를 무효화할 수 있습니다. 단, 요소가 삭제되지 않았다면 요소를 가리키는 포인터·참조는 Rehashing만으로 무효화되지는 않습니다.

출력 순서가 중요한 보고서라면 Key를 정렬해 출력하거나 `std::map`을 사용합니다. 테스트 코드에서 `unordered_map`의 순회 순서를 고정된 것으로 가정하면 안 됩니다.

---

<a id="section-10-6"></a>

## 10.6. Container Adaptors — Queue, Stack, Priority Queue

**예제 코드 — [04_container_adaptors.cpp](./examples/04_container_adaptors.cpp)**

```cpp
#include <print>
#include <queue>
#include <stack>

int main() {
    std::queue<int> pending;
    pending.push(101);
    pending.push(102);
    std::println("Next queue item: {}", pending.front());
    pending.pop();

    std::stack<int> history;
    history.push(1);
    history.push(2);
    std::println("Latest history item: {}", history.top());
    history.pop();

    std::priority_queue<int> priorities;
    priorities.push(20);
    priorities.push(90);
    priorities.push(40);
    std::println("Highest priority: {}", priorities.top());
}
```

**실행 결과**

```text
Next queue item: 101
Latest history item: 2
Highest priority: 90
```

컨테이너 어댑터(Container Adaptor)는 내부 Container의 일부 동작만 공개하여 특정 사용 패턴을 지원합니다.

- **FIFO(First In, First Out):** `queue` — 먼저 들어온 요소를 먼저 처리
- **LIFO(Last In, First Out):** `stack` — 나중에 들어온 요소를 먼저 처리
- **Priority Queue:** 우선순위가 가장 높은 요소를 먼저 처리

`top()`과 `front()`를 호출하기 전에 `empty()`를 확인합니다. `pop()`은 제거만 수행하므로 값을 확인하려면 제거 전에 조회해야 합니다.

**예제 코드 — [16_priority_scheduling.cpp](./examples/16_priority_scheduling.cpp)**

```cpp
#include <print>
#include <queue>
#include <string_view>
#include <vector>

struct Job {
    std::string_view id;
    int priority;
};

struct LowerPriority {
    bool operator()(const Job& a, const Job& b) const {
        if (a.priority != b.priority) {
            return a.priority < b.priority;
        }
        return a.id > b.id;  // 동점에서는 사전순으로 앞선 ID 우선
    }
};

int main() {
    std::priority_queue<Job, std::vector<Job>, LowerPriority> queue;
    queue.push({"save", 20});
    queue.push({"scan", 90});
    queue.push({"report", 90});
    while (!queue.empty()) {
        std::println("{}: {}", queue.top().id, queue.top().priority);
        queue.pop();
    }
}
```

**실행 결과**

```text
report: 90
scan: 90
save: 20
```

사용자 정의 비교자(Comparator)를 전달하면 작업 우선순위를 직접 정의할 수 있습니다. 위 예제는 우선순위가 큰 작업을 먼저 처리하고, 동점에서는 작업 ID가 사전순으로 앞선 작업을 우선합니다.

Comparator는 엄격 약순서(Strict Weak Ordering)를 만족하도록 설계해야 합니다. 비교 기준이 일관되지 않으면 Container나 Algorithm의 전제가 깨질 수 있습니다.

---

<a id="section-10-7"></a>

## 10.7. Iterator와 Half-Open Range

**예제 코드 — [05_iterator_ranges.cpp](./examples/05_iterator_ranges.cpp)**

```cpp
#include <algorithm>
#include <iterator>
#include <print>
#include <vector>

int main() {
    const std::vector<int> samples{11, 13, 17, 19};
    const auto it = std::ranges::find(samples, 17);
    if (it != samples.end()) {
        const auto position = std::distance(samples.cbegin(), it);
        std::println("Found at index: {}", position);
    }
    std::println("Length: {}", std::ranges::distance(samples));
}
```

**실행 결과**

```text
Found at index: 2
Length: 4
```

Iterator는 Container의 요소를 가리킵니다. 일반적으로 **`[begin, end)` 형태의 반열린 구간(Half-Open Range)** 을 사용합니다. 시작 위치는 포함하고 종료 위치는 포함하지 않습니다.

```cpp
// [begin, end) : end는 마지막 요소의 다음 위치
for (auto it = samples.cbegin(); it != samples.cend(); ++it) {
    // *it로 요소 읽기
}
```

- **`begin()` / `cbegin()`:** 첫 요소를 가리키는 Iterator
- **`end()` / `cend()`:** 마지막 요소 다음 위치를 나타내는 종료 Iterator
- **`std::distance(a, b)`:** 두 Iterator 사이의 이동 거리
- **`std::ranges::distance(range)`:** Range의 길이 계산

`end()`는 실제 요소를 가리키지 않으므로 역참조하면 안 됩니다. 또한 Container마다 Iterator 종류가 달라 임의 접근(`it + n`)이 가능한 경우와 불가능한 경우가 있습니다.

---

<a id="section-10-8"></a>

## 10.8. 검색과 조건 검사 — `find_if`, `all_of`

**예제 코드 — [06_search_predicates.cpp](./examples/06_search_predicates.cpp)**

```cpp
#include <algorithm>
#include <print>
#include <string_view>
#include <vector>

struct Sensor {
    std::string_view id;
    int temperature;
};

int main() {
    const std::vector<Sensor> sensors{{"T-01", 31}, {"T-02", 72}, {"T-03", 42}};
    const auto hot = std::ranges::find_if(sensors, [](const Sensor& sensor) {
        return sensor.temperature >= 70;
    });
    if (hot != sensors.end()) {
        std::println("First alert: {}", hot->id);
    }
    const bool all_normal = std::ranges::all_of(sensors, [](const Sensor& sensor) {
        return sensor.temperature < 70;
    });
    std::println("All normal: {}", all_normal);
}
```

**실행 결과**

```text
First alert: T-02
All normal: false
```

조건자(Predicate)는 요소를 검사하여 `bool`로 해석 가능한 결과를 반환하는 호출 가능한 객체입니다. 주로 람다로 작성합니다.

| Algorithm | 결과 |
|---|---|
| `std::ranges::find` | 일치하는 첫 요소의 Iterator |
| `std::ranges::find_if` | Predicate가 참인 첫 요소의 Iterator |
| `std::ranges::count_if` | 조건을 만족하는 요소 수 |
| `std::ranges::all_of` | 모든 요소가 조건을 만족하는지 확인 |
| `std::ranges::any_of` | 하나 이상 조건을 만족하는지 확인 |
| `std::ranges::none_of` | 조건을 만족하는 요소가 하나도 없는지 확인 |

결과가 `end()`인지 확인한 뒤 요소에 접근해야 합니다. 빈 Range에 대해 `all_of()`와 `none_of()`는 `true`, `any_of()`는 `false`를 반환하므로 빈 데이터 처리가 중요한 경우 별도로 조건을 명시합니다.

---

<a id="section-10-9"></a>

## 10.9. 정렬과 비교 규칙 — `sort`, `stable_sort`

**예제 코드 — [07_stable_sort.cpp](./examples/07_stable_sort.cpp)**

```cpp
#include <algorithm>
#include <print>
#include <string_view>
#include <vector>

struct Task {
    std::string_view name;
    int priority;
};

int main() {
    std::vector<Task> tasks{{"scan", 5}, {"save", 8}, {"report", 5}};
    std::ranges::stable_sort(tasks, [](const Task& a, const Task& b) {
        return a.priority > b.priority;
    });
    for (const auto& task : tasks) {
        std::println("{}: {}", task.name, task.priority);
    }
}
```

**실행 결과**

```text
save: 8
scan: 5
report: 5
```

`std::ranges::sort`는 요소를 정렬하고, `std::ranges::stable_sort`는 비교 결과가 동등한 요소들의 상대적인 기존 순서를 유지합니다.

- **`sort`:** 정렬 순서만 필요할 때 사용
- **`stable_sort`:** 동점인 데이터의 기존 순서도 의미가 있을 때 사용
- **`std::ranges::sort(range, {}, &T::member)`:** 투영(Projection)으로 멤버를 정렬 Key로 활용

기본적으로 비교는 Strict Weak Ordering을 만족해야 합니다. 예를 들어 `a <= b`를 Comparator로 전달하면 `a == b`에서도 참이 되므로 적절하지 않습니다. 부동소수점의 NaN이 포함된 데이터는 일반적인 `<` 관계가 요구 조건을 만족하지 않을 수 있으므로 별도 정책이 필요합니다.

```cpp
// Device의 id 멤버를 기준으로 오름차순 정렬
// std::ranges::sort(devices, {}, &Device::id);
```

정렬의 평균적 시간 복잡도는 비교 정렬에서 일반적으로 `O(n log n)`이며, 표준 `sort`는 최악의 비교 횟수에 대해서도 `O(n log n)` 요구가 있습니다.

---

<a id="section-10-10"></a>

## 10.10. 조건부 삭제 — `erase_if`, Erase–Remove

**예제 코드 — [08_erase_remove.cpp](./examples/08_erase_remove.cpp)**

```cpp
#include <algorithm>
#include <print>
#include <vector>

int main() {
    std::vector<int> measurements{-1, 16, 21, -1, 19};
    const auto removed = std::erase_if(measurements, [](int value) {
        return value < 0;
    });
    std::println("Removed: {}", removed);
    for (const int value : measurements) {
        std::println("Measurement: {}", value);
    }
}
```

**실행 결과**

```text
Removed: 2
Measurement: 16
Measurement: 21
Measurement: 19
```

Iterator로 접근하는 Container에서 요소를 삭제하면 Iterator가 무효화(Invalidation)될 수 있습니다. `std::vector`의 특정 조건을 만족하는 요소를 삭제할 때는 `std::erase_if`가 간결합니다.

```cpp
std::vector<int> values{1, -1, 2};
std::erase_if(values, [](int value) { return value < 0; });
// values == {1, 2}
```

전통적인 제거-삭제 패턴(Erase–Remove Idiom)은 `std::remove_if`로 남길 요소를 앞으로 모으고 `erase()`로 실제 Container의 크기를 줄이는 방식입니다. `std::ranges::remove_if` 역시 요소를 곧바로 삭제하지는 않습니다.

데이터 삭제 도중 직접 Iterator를 순회해야 한다면, `erase()`가 반환하는 다음 Iterator를 사용해야 합니다. 무효화된 Iterator를 다시 사용하면 미정의 동작(Undefined Behavior, UB)이 발생할 수 있습니다.

---

<a id="section-10-11"></a>

## 10.11. 변환과 수치 집계 — `transform`, `accumulate`

**예제 코드 — [09_transform_and_aggregate.cpp](./examples/09_transform_and_aggregate.cpp)**

```cpp
#include <algorithm>
#include <iterator>
#include <numeric>
#include <print>
#include <vector>

int main() {
    const std::vector<int> seconds{2, 3, 5};
    std::vector<int> milliseconds;
    milliseconds.reserve(seconds.size());
    std::ranges::transform(seconds, std::back_inserter(milliseconds), [](int value) {
        return value * 1'000;
    });
    const long long total = std::accumulate(milliseconds.begin(),
                                            milliseconds.end(), 0LL);
    std::println("Total: {} ms", total);
    std::println("Converted items: {}", milliseconds.size());
}
```

**실행 결과**

```text
Total: 10000 ms
Converted items: 3
```

`std::ranges::transform`은 원본 요소에 함수를 적용하여 출력 Iterator에 결과를 기록합니다. `std::back_inserter`는 결과 요소를 Container 끝에 추가할 수 있도록 해 줍니다.

`std::accumulate`의 **초기값 자료형**은 누적 계산의 자료형을 결정합니다. 정수 합계가 커질 가능성이 있다면 `0LL` 같은 넓은 정수형 초기값을 사용하고, 해당 범위를 넘지 않는지 검토해야 합니다.

**예제 코드 — [10_numeric_algorithms.cpp](./examples/10_numeric_algorithms.cpp)**

```cpp
#include <array>
#include <numeric>
#include <print>

int main() {
    constexpr std::array<int, 4> latencies{20, 30, 10, 40};
    const long long sum = std::accumulate(latencies.begin(), latencies.end(), 0LL);
    const double mean = static_cast<double>(sum) / latencies.size();
    constexpr std::array<int, 4> weights{1, 2, 1, 2};
    const int weighted = std::inner_product(latencies.begin(), latencies.end(),
                                            weights.begin(), 0);
    std::println("Mean: {:.1f} ms", mean);
    std::println("Weighted sum: {}", weighted);
}
```

**실행 결과**

```text
Mean: 25.0 ms
Weighted sum: 170
```

`std::inner_product`는 두 입력 Range의 대응 요소를 곱하고 합치는 작업에 사용할 수 있습니다. 예시의 가중치 배열은 정확히 4개 요소이며, 호출자가 두 번째 Range에도 충분한 요소가 있음을 보장해야 합니다.

- **`std::accumulate`:** 입력 순서대로 누적 계산
- **`std::reduce`:** 연산 순서가 달라질 수 있는 축약 계산. 부동소수점은 결과 차이 가능
- **`std::inner_product`:** 대응 요소를 결합하여 누적

합계·평균 계산에서는 빈 데이터 여부와 정수 오버플로, 부동소수점 반올림 차이를 별도로 확인합니다.

---

<a id="section-10-12"></a>

## 10.12. Ranges & Views — 필터·변환·슬라이싱

**예제 코드 — [11_ranges_views.cpp](./examples/11_ranges_views.cpp)**

```cpp
#include <print>
#include <ranges>
#include <vector>

int main() {
    const std::vector<int> readings{12, 4, 20, 15, 8};
    auto processed = readings
        | std::views::filter([](int value) { return value >= 10; })
        | std::views::transform([](int value) { return value * 2; })
        | std::views::take(2);
    for (const int value : processed) {
        std::println("Processed: {}", value);
    }
}
```

**실행 결과**

```text
Processed: 24
Processed: 40
```

C++20부터 도입된 Ranges를 사용하면 데이터를 반복문으로 직접 가공하지 않고 파이프라인으로 표현할 수 있습니다. 아래 예제는 10 이상 값만 선택하고 두 배로 변환한 다음 처음 두 개만 사용합니다.

View의 대표적인 특징은 지연 평가(Lazy Evaluation)입니다. View를 구성하는 즉시 모든 결과가 계산되는 것은 아니며, 실제로 순회할 때 요소가 평가될 수 있습니다.

**수명(Lifetime) 주의:** `std::views::filter` 같은 View는 원본 데이터를 복사하여 소유하는 경우와 그렇지 않은 경우가 있습니다. 원본 Container를 참조하는 View가 원본보다 오래 살아남지 않도록 설계해야 합니다.

또한 `filter_view` 등의 일부 View는 `const` 객체에서 `begin()`을 호출할 수 없습니다. 따라서 예제의 결과는 `const auto`가 아닌 `auto processed`로 선언합니다. `const`가 언제나 읽기 전용 순회를 가능하게 하는 것은 아닙니다.

---

<a id="section-10-13"></a>

## 10.13. C++23 — `std::ranges::to`

**예제 코드 — [12_ranges_to.cpp](./examples/12_ranges_to.cpp)**

```cpp
#include <algorithm>
#include <iterator>
#include <print>
#include <ranges>
#include <vector>

int main() {
    auto squares = std::views::iota(1, 7)
        | std::views::filter([](int value) { return value % 2 == 0; })
        | std::views::transform([](int value) { return value * value; });

#if defined(__cpp_lib_ranges_to_container) && __cpp_lib_ranges_to_container >= 202202L
    const auto result = std::ranges::to<std::vector<int>>(squares);
#else
    std::vector<int> result;
    std::ranges::copy(squares, std::back_inserter(result));
#endif

    for (const int value : result) {
        std::println("Square: {}", value);
    }
}
```

**실행 결과**

```text
Square: 4
Square: 16
Square: 36
```

C++23의 `std::ranges::to`는 Range를 `std::vector` 같은 실제 Container로 변환합니다. View 자체는 연산 정의를 보관하지만, 변환된 `std::vector`는 결과 요소를 소유합니다.

C++23 언어 모드를 지원하더라도 표준 라이브러리 구현에 따라 `std::ranges::to`가 없을 수 있습니다. 예제는 기능 테스트 매크로(Feature-Test Macro) `__cpp_lib_ranges_to_container`를 확인하여, 지원하지 않는 환경에서는 `std::ranges::copy`와 `std::back_inserter`를 사용하는 대체 경로를 제공합니다.

`std::ranges::to`에 전달한 Range는 순회 가능한 형태여야 합니다. `filter_view` 조합에서는 `const` View가 순회 조건을 만족하지 못하는 경우가 있으므로 예제의 `squares`는 `auto`로 선언합니다.

---

<a id="section-10-14"></a>

## 10.14. 정렬된 데이터 검색 — Binary Search

**예제 코드 — [13_binary_search.cpp](./examples/13_binary_search.cpp)**

```cpp
#include <iterator>
#include <algorithm>
#include <print>
#include <vector>

int main() {
    const std::vector<int> codes{10, 20, 20, 30, 40};  // 이미 정렬됨
    const auto lower = std::ranges::lower_bound(codes, 20);
    const auto upper = std::ranges::upper_bound(codes, 20);
    std::println("Has 30: {}", std::ranges::binary_search(codes, 30));
    std::println("Count of 20: {}", std::distance(lower, upper));
}
```

**실행 결과**

```text
Has 30: true
Count of 20: 2
```

이진 탐색(Binary Search)은 정렬된 범위에서 탐색 구간을 반복적으로 좁혀 검색합니다. `std::ranges::binary_search`는 값의 존재 여부를, `lower_bound`와 `upper_bound`는 지정한 값이 나타나는 구간의 양끝을 찾습니다.

| 연산 | 의미 |
|---|---|
| `binary_search` | 값 존재 여부 |
| `lower_bound` | 지정한 값보다 작지 않은 첫 위치 |
| `upper_bound` | 지정한 값보다 큰 첫 위치 |
| `equal_range` | `[lower_bound, upper_bound)` 구간 |

**전제 조건:** 비교 기준에 맞게 정렬되어 있거나, 해당 Algorithm이 요구하는 분할 조건을 만족해야 합니다. 정렬되지 않은 데이터를 그대로 넘기면 원하는 결과를 보장할 수 없습니다.

정렬된 `vector`에 대한 `lower_bound`의 비교 횟수는 `O(log n)`이지만, 임의 접근이 불가능한 Iterator에서는 해당 위치까지의 이동 비용이 추가될 수 있습니다.

---

<a id="section-10-15"></a>

## 10.15. Transparent Lookup — 불필요한 Key 생성 방지

**예제 코드 — [14_transparent_lookup.cpp](./examples/14_transparent_lookup.cpp)**

```cpp
#include <functional>
#include <map>
#include <print>
#include <string>
#include <string_view>

int main() {
    std::map<std::string, int, std::less<>> ports{{"camera", 8001}, {"lidar", 8002}};
    const std::string_view name{"lidar"};
    if (const auto it = ports.find(name); it != ports.end()) {
        std::println("{} port: {}", it->first, it->second);
    }
}
```

**실행 결과**

```text
lidar port: 8002
```

투명 비교(Transparent Comparison)를 지원하도록 `std::less<>`를 지정하면 `std::map<std::string, ...>`에서 `std::string_view`로도 Key를 찾을 수 있습니다. 이를 투명 조회(Transparent Lookup)라고 합니다.

이 방식은 조회 때마다 새 `std::string` 객체를 만들지 않아도 되게 해 줍니다. 단, 어떤 Key 타입 조합이 비교 가능한지는 Comparator 정의에 따라 달라집니다. Hash Container에서의 이종 조회는 Hash와 동등성 판정 함수가 투명 조회를 지원하도록 별도 설계해야 합니다.

---

<a id="section-10-16"></a>

## 10.16. Iterator Invalidation과 메모리 안전

**예제 코드 — [15_invalidation_safe_erase.cpp](./examples/15_invalidation_safe_erase.cpp)**

```cpp
#include <print>
#include <vector>

int main() {
    std::vector<int> values{3, -1, 5, -2, 7};
    for (auto it = values.begin(); it != values.end();) {
        if (*it < 0) {
            it = values.erase(it);  // 반환된 새 Iterator로 갱신
        } else {
            ++it;
        }
    }
    for (const int value : values) {
        std::println("Valid: {}", value);
    }
}
```

**실행 결과**

```text
Valid: 3
Valid: 5
Valid: 7
```

Iterator나 포인터가 유효했던 요소·저장 위치가 변경되어 더 이상 사용할 수 없게 되는 상황을 Invalidation이라고 합니다.

| 작업 | 주의할 상황 |
|---|---|
| `vector::push_back()` | Reallocation 발생 시 모든 요소 Iterator·포인터·참조 무효화 |
| `vector::erase()` | 삭제 지점과 그 뒤 요소의 Iterator·참조 무효화 |
| `unordered_map::rehash()` | Iterator 무효화. 삭제되지 않은 요소의 참조·포인터는 유지 |
| `map::erase()` | 삭제된 요소에 대한 Iterator·참조만 무효화 |
| `list::erase()` | 삭제된 노드에 대한 Iterator·참조만 무효화 |

어떤 Iterator가 여전히 유효한지 Container 종류와 연산별로 구분해야 합니다. 오래 저장한 Iterator를 재사용하거나, 무효화된 포인터를 역참조하는 작업은 UB로 이어질 수 있습니다.

검증 환경에서는 AddressSanitizer와 UndefinedBehaviorSanitizer 등을 이용해 메모리 오류를 확인할 수 있습니다. 다만 모든 UB가 검사 도구로 탐지되는 것은 아닙니다.

---

<a id="section-10-17"></a>

## 10.17. Mini Project — Device Event Summary

장치별 이벤트 데이터를 집계하고, 지연 시간이 기준 이상인 이벤트 개수와 평균 지연 시간을 계산하는 프로그램입니다. `std::unordered_map`으로 집계하고 결과를 `std::vector`로 이동한 뒤, 장치 이름을 기준으로 정렬합니다.

```text
examples/17_event_summary/
├── CMakeLists.txt
├── event_summary.hpp
├── event_summary.cpp
└── main.cpp
```

| 파일 | 역할 |
|---|---|
| [`event_summary.hpp`](./examples/17_event_summary/event_summary.hpp) | Event, DeviceSummary, 함수 인터페이스 선언 |
| [`event_summary.cpp`](./examples/17_event_summary/event_summary.cpp) | 유효성 검사, 그룹별 집계, 정렬 구현 |
| [`main.cpp`](./examples/17_event_summary/main.cpp) | 예제 데이터, 결과 및 오류 출력 |
| [`CMakeLists.txt`](./examples/17_event_summary/CMakeLists.txt) | CMake 빌드 설정 |

**주요 설계**

- **입력:** 장치 이름과 0 이상의 지연 시간, 느린 이벤트 판정 기준
- **검증:** 빈 장치 이름, 음수 측정값, 잘못된 기준값을 오류로 반환
- **집계:** `try_emplace()`로 장치별 값 생성, 건수·합계·기준 이상 건수 누적
- **정렬:** `std::ranges::sort(result, {}, &DeviceSummary::device)` 사용
- **오류 표현:** `std::expected<std::vector<DeviceSummary>, std::string>` 사용

**빌드 및 실행 — GCC / Clang (Chapter-10 폴더 기준)**

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror \
  examples/17_event_summary/main.cpp examples/17_event_summary/event_summary.cpp \
  -o event_summary
./event_summary
```

**CMake**

```bash
cmake -S examples/17_event_summary -B build/event_summary
cmake --build build/event_summary
./build/event_summary/event_summary
```

Windows에서는 생성된 실행 파일의 경로와 확장자가 빌드 방식에 따라 달라질 수 있습니다.


**실행 결과**

```text
CAMERA: count=2, slow=1, mean=61.0 ms
IMU: count=1, slow=0, mean=12.0 ms
LIDAR: count=2, slow=1, mean=79.0 ms
```

사용한 Grouping과 정렬 단계는 서로 다른 목적을 가집니다. Hash Container는 빠른 누적을 위해 사용하고, 최종 출력의 순서를 일정하게 하기 위해 별도 정렬을 수행합니다.

---

<a id="section-10-18"></a>

## 10.18. 설계 시 참고 사항

| 상황 | 권장 접근 | 주의사항 |
|---|---|---|
| 소량의 순차 데이터 | 우선 `std::vector` 검토 | 특별한 이유 없이 노드형 Container 사용 지양 |
| Key 순서가 중요한 조회 | `std::map`, `std::set` | `O(log n)` 특성과 비교 기준 확인 |
| 순서가 필요 없는 빈도 집계 | `std::unordered_map` | 순회 순서에 의존하지 않음 |
| 동점 순서가 중요한 정렬 | `std::ranges::stable_sort` | Comparator의 Strict Weak Ordering 유지 |
| 데이터 필터·변환 | `std::views` 파이프라인 | View의 Lifetime과 Lazy Evaluation 확인 |
| 결과를 장기간 저장 | 실제 Container로 변환 | View가 원본을 소유하는지 확인 |
| 반복 중 삭제 | `std::erase_if`, `erase()` 반환 Iterator | Invalidation된 Iterator 재사용 방지 |
| 여러 Container 혼용 | 데이터 흐름과 소유권(Ownership) 정의 | 중복 데이터·복사·수명 문제 검토 |

### 빌드 환경

**GCC** — Chapter-10 디렉터리에서 실행

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror \
  examples/03_unordered_frequency.cpp -o example
./example
```

**Clang**

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic \
  examples/03_unordered_frequency.cpp -o example
./example
```

**MSVC — Developer Command Prompt**

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 examples\03_unordered_frequency.cpp /Fe:example.exe
example.exe
```

MSVC의 `/std:c++23` 지원 여부는 설치된 버전에 따라 확인합니다. C++23 언어 옵션을 사용할 수 있어도 표준 라이브러리 기능의 구현 범위는 컴파일러·라이브러리마다 다를 수 있습니다.

---

<a id="section-10-19"></a>

## 10.19. Coding Practice

연습문제 파일은 핵심 로직을 작성하지 않은 상태이며, 정답 코드는 `solutions/`에 분리했습니다. 입력은 표준 입력으로 받고, 잘못된 입력은 표준 오류로 출력한 뒤 종료 코드 `1`을 반환하는 방식입니다.

### 실습 ① — Event Frequency

이벤트 이름 `n`개를 입력받아 이벤트별 등장 횟수를 집계합니다.

- 입력: 첫 줄 `n(1~10000)`, 이후 이벤트 이름 `n`개
- 출력: 이벤트 이름 오름차순으로 `이름: 횟수`
- 조건: 이벤트 이름은 공백 없는 문자열이며 대소문자 구분
- 활용: `std::map`, `operator[]`, 구조적 바인딩(Structured Binding)

**입력**

```text
6
WARN INFO WARN ERROR INFO INFO
```

**출력**

```text
ERROR: 1
INFO: 3
WARN: 2
```

[연습문제 — 01_event_frequency.cpp](./exercises/01_event_frequency.cpp) · [정답 코드 — 01_event_frequency.cpp](./solutions/01_event_frequency.cpp)

### 실습 ② — Top-K Tasks

우선순위가 높은 작업 `k`개를 출력합니다.

- 입력: `n k` (`1 ≤ k ≤ n ≤ 10000`), 이후 `작업이름 우선순위` `n`쌍
- 우선순위: `0~100` 정수, 큰 값 우선
- 동점 처리: 작업 이름의 사전순 오름차순
- 활용: `std::priority_queue`와 Comparator

**입력**

```text
5 3
scan 70
save 30
navigate 90
upload 90
idle 10
```

**출력**

```text
navigate 90
upload 90
scan 70
```

[연습문제 — 02_top_k_tasks.cpp](./exercises/02_top_k_tasks.cpp) · [정답 코드 — 02_top_k_tasks.cpp](./solutions/02_top_k_tasks.cpp)

### 실습 ③ — Clean Readings

측정값에서 무효 데이터 `-1`을 제거하고 중복 없는 측정값을 오름차순으로 출력합니다.

- 입력: 첫 줄 `n(1~10000)`, 이후 정수 `n`개
- 범위: `-1` 또는 `0~1000`; 범위 밖 값은 오류 처리
- 결과가 비었으면 `EMPTY` 출력
- 활용: `std::ranges::sort`, `std::ranges::unique`, `erase()`

**입력**

```text
8
12 -1 7 12 30 -1 7 10
```

**출력**

```text
7 10 12 30
```

[연습문제 — 03_clean_readings.cpp](./exercises/03_clean_readings.cpp) · [정답 코드 — 03_clean_readings.cpp](./solutions/03_clean_readings.cpp)

### 실습 ④ — Device Summary

장치 이름별 측정 건수와 평균 지연 시간을 계산합니다.

- 입력: 첫 줄 `n(1~10000)`, 이후 `장치이름 지연시간` `n`쌍
- 지연시간: `0~1000000` 정수
- 출력: 장치 이름 오름차순, 평균 소수 첫째 자리
- 활용: `std::map`, 합계 누적, 구조적 바인딩

**입력**

```text
5
A 10
B 20
A 14
B 30
C 8
```

**출력**

```text
A: count=2, mean=12.0
B: count=2, mean=25.0
C: count=1, mean=8.0
```

[연습문제 — 04_device_summary.cpp](./exercises/04_device_summary.cpp) · [정답 코드 — 04_device_summary.cpp](./solutions/04_device_summary.cpp)

### 정답 코드 컴파일

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -Werror \
  solutions/01_event_frequency.cpp -o event_frequency
./event_frequency
```

---

<a id="section-10-20"></a>

## 10.20. Quiz & Summary

### Quiz

1. `std::map`과 `std::unordered_map` 중 Key 정렬 순서를 보장하는 Container는 무엇인가요?
2. `std::vector::push_back()`이 기존 Iterator를 무효화하는 대표적인 조건은 무엇인가요?
3. `std::ranges::sort`에 전달하는 Comparator가 만족해야 할 주요 규칙은 무엇인가요?
4. `std::ranges::remove_if` 호출만으로 Container 크기가 줄어드나요?
5. `std::views::filter`가 생성하는 View는 원본 데이터의 Lifetime과 어떤 관계가 있나요?
6. `std::ranges::to`가 없는 표준 라이브러리에서는 어떻게 결과를 `std::vector`로 만들 수 있나요?
7. `std::priority_queue`에서 `top()`과 `pop()`의 역할은 무엇인가요?

<details>
<summary>정답 확인</summary>

1. `std::map`. 기본적으로 Key를 정렬된 순서로 순회할 수 있음.
2. 용량이 부족해 Reallocation이 발생하는 경우.
3. Strict Weak Ordering.
4. 아니요. 제거 대상 요소를 뒤쪽으로 모으며 실제 크기 감소에는 `erase()` 필요.
5. 원본 데이터를 참조하는 View는 원본이 유효해야 하며 Invalidation도 고려해야 함.
6. `std::ranges::copy(range, std::back_inserter(vector))` 등을 사용.
7. `top()`은 최우선 요소 조회, `pop()`은 해당 요소 제거.

</details>

### Summary

- **Container:** 데이터 순서·중복·검색·추가·삭제 요구사항에 맞춰 선택
- **Iterator / Range:** `[begin, end)` 범위를 안전하게 순회
- **Algorithm:** `find_if`, `sort`, `transform`, `accumulate` 등을 활용한 데이터 처리
- **Ordered Container:** `map`, `set`의 Key 또는 값 정렬 유지
- **Unordered Container:** Hash 기반 평균 상수 시간 조회. 순서 보장 없음
- **Container Adaptor:** `queue`, `stack`, `priority_queue`를 통한 처리 순서 제어
- **View:** 데이터의 Lazy Evaluation과 Lifetime 고려
- **`std::ranges::to`:** C++23의 Range → Container 변환, 구현 지원 여부 확인
- **Invalidation / UB:** 재할당과 삭제 이후 Iterator·포인터 사용 범위 확인

### References

- [cppreference — Containers](https://en.cppreference.com/w/cpp/container)
- [cppreference — Iterator Library](https://en.cppreference.com/w/cpp/iterator)
- [cppreference — Algorithms Library](https://en.cppreference.com/w/cpp/algorithm)
- [cppreference — Ranges Library](https://en.cppreference.com/w/cpp/ranges)
- [cppreference — `std::ranges::to`](https://en.cppreference.com/w/cpp/ranges/to)
- [cppreference — C++23 Compiler Support](https://en.cppreference.com/w/cpp/compiler_support/23)

---

[← C++ 목차](../README.md) · [Chapter 09 — Object-Oriented Programming](../Chapter-09/)

---
