# Chapter 10. Standard Library (STL)

C++ 표준 라이브러리의 컨테이너(Container), 반복자(Iterator), 알고리즘(Algorithm)을 이용해 데이터를 저장하고 처리하는 방법을 학습합니다. 순차·연관 컨테이너의 선택 기준부터 정렬, 검색, 집계, 범위(Ranges)와 뷰(View), 반복자 무효화까지 다룹니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다.

<details>
<summary>선행 학습</summary>

- [Chapter 05 — Functions](../Chapter-05/) — 함수, 람다와 매개변수
- [Chapter 06 — Arrays & Strings](../Chapter-06/) — 배열, `std::vector`와 문자열
- [Chapter 07 — Pointers & References](../Chapter-07/) — 참조, 객체 수명과 무효화

</details>

## Contents

| Section | Topic |
|:---:|---|
| [10.1](#section-10-1) | Standard Library & STL — 표준 라이브러리의 구성 |
| [10.2](#section-10-2) | Container Selection — 컨테이너 선택과 시간 복잡도 |
| [10.3](#section-10-3) | Sequence Containers — 순차 컨테이너 |
| [10.4](#section-10-4) | Ordered Associative Containers — 정렬된 연관 컨테이너 |
| [10.5](#section-10-5) | Unordered Containers — 해시 기반 컨테이너 |
| [10.6](#section-10-6) | Container Adaptors — 처리 순서를 위한 어댑터 |
| [10.7](#section-10-7) | Iterators & Ranges — 반복자와 반열린 구간 |
| [10.8](#section-10-8) | Search & Predicates — 검색과 조건 검사 |
| [10.9](#section-10-9) | Stable Sorting — 정렬과 비교 규칙 |
| [10.10](#section-10-10) | Erase & Remove — 조건에 따른 요소 삭제 |
| [10.11](#section-10-11) | Transform & Aggregate — 변환과 집계 |
| [10.12](#section-10-12) | Numeric Algorithms — 수치 알고리즘 |
| [10.13](#section-10-13) | Ranges & Views — 필터와 변환 뷰 |
| [10.14](#section-10-14) | Materializing Views — 뷰 결과를 컨테이너로 복사 |
| [10.15](#section-10-15) | Binary Search — 정렬된 데이터 검색 |
| [10.16](#section-10-16) | Transparent Lookup — 다른 키 타입으로 조회 |
| [10.17](#section-10-17) | Iterator Invalidation — 무효화된 반복자 피하기 |
| [10.18](#section-10-18) | Priority Scheduling — 우선순위에 따른 처리 |
| [10.19](#section-10-19) | Coding Practice |
| [10.20](#section-10-20) | Mini Project — Device Event Summary |
| [10.21](#section-10-21) | Quiz & Summary |

## Getting Started

아래 명령어는 `Chapter-10/` 폴더에서 실행하는 경우를 기준으로 합니다. `-std=c++20`을 지정하면 컴파일러의 기본 표준 버전에 관계없이 C++20을 사용합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_sequence_containers.cpp -o containers
./containers
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_sequence_containers.cpp -o containers
./containers
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /utf-8 examples\01_sequence_containers.cpp /Fe:containers.exe
containers.exe
```

Windows PowerShell에서는 `./containers` 대신 `.\containers.exe`로 실행합니다.

**학습 목표**

1. 데이터의 순서·중복·검색 요구사항에 맞춰 컨테이너를 선택할 수 있습니다.
2. 반복자와 `[begin, end)` 구간의 의미를 설명할 수 있습니다.
3. 검색·정렬·삭제·집계 작업을 표준 알고리즘으로 구현할 수 있습니다.
4. 뷰의 지연 평가와 객체 수명, 반복자 무효화에 따른 제약을 이해할 수 있습니다.

<a id="section-10-1"></a>

## 10.1. Standard Library & STL — 표준 라이브러리의 구성

**C++ 표준 라이브러리(C++ Standard Library)** 는 컨테이너뿐 아니라 문자열, 입출력, 메모리 관리, 스레드 등 다양한 기능을 포함합니다. **표준 템플릿 라이브러리(Standard Template Library, STL)** 는 그중 컨테이너·반복자·알고리즘을 연결하는 범용 프로그래밍 방식과 밀접하게 관련된 이름입니다. 둘은 정확히 같은 범위를 가리키는 말은 아닙니다.

| 구성 요소 | 역할 | 대표 예시 |
|---|---|---|
| 컨테이너(Container) | 여러 요소를 저장하고 관리 | `std::vector`, `std::map` |
| 반복자(Iterator) | 요소의 위치를 나타내고 순회 | `begin()`, `end()` |
| 알고리즘(Algorithm) | 검색·정렬·변환 등의 처리 | `std::ranges::sort`, `std::ranges::find` |
| 조건자(Predicate) | 참·거짓을 반환하는 검사 함수 | `[](int x) { return x > 0; }` |
| 범위(Range) | 순회 가능한 요소들의 구간 | `std::vector`, `std::span` |
| 뷰(View) | 원본 요소를 필요한 방식으로 관찰 | `std::views::filter` |

C++에서는 데이터를 저장하는 방식과 데이터를 처리하는 방식을 분리할 수 있습니다. 예를 들어 `std::ranges::sort()`는 특정 프로그램의 센서 목록만을 위해 작성된 함수가 아닙니다. 정렬에 필요한 조건을 만족하는 범위라면 다양한 자료형에 재사용할 수 있습니다.

<a id="section-10-2"></a>

## 10.2. Container Selection — 컨테이너 선택과 시간 복잡도

컨테이너는 데이터가 저장되는 구조와 접근 방법이 서로 다릅니다. **시간 복잡도(Time Complexity)** 는 데이터 크기가 커질 때 연산 비용이 증가하는 정도를 표현합니다. `O(1)`은 일정한 비용, `O(log n)`은 로그 형태, `O(n)`은 요소 수에 비례하는 비용을 나타냅니다. 이 표기는 실제 실행 시간을 초 단위로 보장하지 않습니다.

| 컨테이너 | 특징 | 대표 연산의 복잡도 | 적합한 상황 |
|---|---|---|---|
| `std::vector` | 연속 저장, 인덱스 접근 | 끝 추가 분할 상환 `O(1)`, 중간 삽입 `O(n)` | 순서대로 모으는 측정값 |
| `std::deque` | 양끝에 효율적으로 요소 추가·삭제 | 양끝 추가·삭제 `O(1)`, 인덱스 접근 `O(1)` | 작업 대기열의 앞·뒤 변경 |
| `std::list` | 양방향 연결 리스트 | 위치를 알면 삽입·삭제 `O(1)`, 검색 `O(n)` | 기존 반복자 위치에서 연결 변경 |
| `std::map` | 키 정렬, 중복 키 불가 | 검색·삽입 `O(log n)` | 정렬된 장치별 통계 |
| `std::set` | 중복 없는 정렬 값 | 검색·삽입 `O(log n)` | 고유한 채널 번호 |
| `std::unordered_map` | 해시 기반, 순서 보장 없음 | 평균 `O(1)`, 최악 `O(n)` | 이벤트 빈도 집계 |
| `std::unordered_set` | 해시 기반 고유 값 | 평균 `O(1)`, 최악 `O(n)` | 중복 ID 확인 |
| `std::priority_queue` | 우선순위가 높은 요소부터 조회 | `top()` `O(1)`, 추가·삭제 `O(log n)` | 긴급 작업 처리 |

**분할 상환(Amortized)** `O(1)`은 여러 번의 연산에 걸쳐 평균 비용을 나눈 결과입니다. `std::vector::push_back()`은 저장 공간이 부족할 때 기존 요소를 옮겨야 하므로, 모든 호출이 개별적으로 `O(1)`인 것은 아닙니다.

`std::list`는 중간 삭제가 빠르다고 해서 모든 상황에 적합한 것은 아닙니다. 삭제할 위치를 찾는 데 드는 비용과 메모리 배치까지 고려해야 합니다. 단순한 순차 처리에서는 `std::vector`가 더 나은 경우도 많습니다.

<a id="section-10-3"></a>

## 10.3. Sequence Containers — 순차 컨테이너

**순차 컨테이너(Sequence Container)** 는 요소를 일정한 순서로 관리합니다. `<vector>`, `<deque>`, `<list>` 헤더는 각각 `std::vector`, `std::deque`, `std::list`를 제공합니다. `<iterator>`는 반복자를 이동시키는 `std::next()` 등을 정의합니다.

`std::vector`는 연속된 저장 공간을 사용하고, `std::deque`는 양끝에서 요소를 추가·삭제하기 좋습니다. `std::list`는 노드가 연결된 형태이며 인덱스로 임의 접근할 수 없습니다.

**예제 코드 — [01_sequence_containers.cpp](./examples/01_sequence_containers.cpp)**

```cpp
#include <deque>
#include <iostream>
#include <iterator>
#include <list>
#include <vector>

int main() {
    std::vector<int> samples{20, 22, 19};
    samples.push_back(21);

    std::deque<int> pending{2, 3};
    pending.push_front(1);

    std::list<int> checkpoints{10, 30};
    checkpoints.insert(std::next(checkpoints.begin()), 20);

    std::cout << "Samples: " << samples.size() << '\n';
    std::cout << "First task: " << pending.front() << '\n';
    for (const int point : checkpoints) {
        std::cout << "Checkpoint: " << point << '\n';
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

`samples.push_back(21)`은 벡터 끝에 요소를 하나 추가합니다. `pending.push_front(1)`은 덱의 앞쪽에 작업을 넣습니다. `std::next(checkpoints.begin())`는 첫 요소 다음 위치를 나타내며, `insert()`는 그 위치 앞에 `20`을 삽입합니다.

`std::list`의 삽입 자체는 위치가 주어졌다면 효율적이지만, 반복자를 이동해 원하는 위치를 찾는 비용은 별개입니다.

<a id="section-10-4"></a>

## 10.4. Ordered Associative Containers — 정렬된 연관 컨테이너

**정렬된 연관 컨테이너(Ordered Associative Container)** 는 키 또는 값을 비교 규칙에 맞춰 관리합니다. `<map>`의 `std::map`은 `키 → 값` 쌍을, `<set>`의 `std::set`은 중복 없는 값을 저장합니다.

C++17의 **구조적 바인딩(Structured Binding)** 인 `[name, quantity]`를 사용하면 키와 값을 이름으로 받아 처리할 수 있습니다. `std::map`을 기본 비교 규칙으로 순회하면 키가 오름차순으로 나타납니다.

**예제 코드 — [02_ordered_containers.cpp](./examples/02_ordered_containers.cpp)**

```cpp
#include <iostream>
#include <map>
#include <set>
#include <string>

int main() {
    std::map<std::string, int> inventory{{"battery", 4}, {"camera", 2}};
    inventory.insert_or_assign("battery", 5);
    std::set<int> channel_ids{8, 3, 8, 5};

    for (const auto& [name, quantity] : inventory) {
        std::cout << name << ": " << quantity << '\n';
    }
    std::cout << "Unique channels: " << channel_ids.size() << '\n';
    if (const auto it = channel_ids.lower_bound(4); it != channel_ids.end()) {
        std::cout << "First channel >= 4: " << *it << '\n';
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

`insert_or_assign()`은 키가 존재하면 값을 갱신합니다. `std::set{8, 3, 8, 5}`의 요소는 중복을 제거한 `3, 5, 8`이 됩니다. `lower_bound(4)`는 **4 이상인 첫 요소**를 가리키는 반복자를 반환합니다.

읽기만 할 때 `map[key]`를 사용하면 없는 키가 새로 삽입될 수 있습니다. 존재 여부에는 `find()` 또는 C++20의 `contains()`를, 이미 존재함이 보장된 키의 값에는 `at()`을 고려합니다.

<a id="section-10-5"></a>

## 10.5. Unordered Containers — 해시 기반 컨테이너

**해시(Hash)** 는 키를 계산된 값으로 바꾸어 저장 위치를 찾는 방식입니다. `<unordered_map>`의 `std::unordered_map`은 평균적으로 빠른 조회가 가능하지만 **순회 순서를 보장하지 않습니다.**

이벤트 종류별 횟수를 집계할 때 `counts[event]`는 해당 키가 없으면 기본값 `0`을 생성하고, 이후 `++`로 횟수를 늘립니다. `reserve()`는 미리 예상한 요소 수에 맞춰 버킷 공간 확보를 요청합니다.

**예제 코드 — [03_unordered_frequency.cpp](./examples/03_unordered_frequency.cpp)**

```cpp
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    const std::vector<std::string> events{"WARN", "INFO", "WARN", "ERROR", "INFO"};
    std::unordered_map<std::string, int> counts;
    counts.reserve(3);
    for (const auto& event : events) {
        ++counts[event];
    }

    // 해시 테이블의 순회 순서는 보장되지 않으므로 키를 지정해 출력합니다.
    std::cout << "INFO: " << counts.at("INFO") << '\n';
    std::cout << "WARN: " << counts.at("WARN") << '\n';
    std::cout << "ERROR: " << counts.at("ERROR") << '\n';
    std::cout << std::boolalpha << "Contains DEBUG: " << counts.contains("DEBUG") << '\n';
}
```

**실행 결과**

```text
INFO: 2
WARN: 2
ERROR: 1
Contains DEBUG: false
```

출력은 해시 테이블을 그대로 순회하지 않고 `INFO`, `WARN`, `ERROR` 키를 직접 조회합니다. 따라서 구현 환경에 따른 버킷 순서 변화가 출력에 영향을 주지 않습니다.

**리해싱(Rehashing)** 은 버킷 배치를 다시 구성하는 작업입니다. 리해싱은 반복자를 무효화할 수 있지만, 삭제되지 않은 요소의 참조·포인터까지 리해싱만으로 무효화하지는 않습니다. 키 정렬 출력이 필요하면 `std::map`이 더 간단할 수 있습니다.

<a id="section-10-6"></a>

## 10.6. Container Adaptors — 처리 순서를 위한 어댑터

**컨테이너 어댑터(Container Adaptor)** 는 기존 컨테이너에 특정 접근 방식만 제공하는 자료구조입니다. `<queue>`의 `std::queue`는 먼저 들어간 요소를 먼저 처리하는 FIFO(First In, First Out) 방식이고, `<stack>`의 `std::stack`은 마지막에 들어간 요소를 먼저 처리하는 LIFO(Last In, First Out) 방식입니다.

`std::priority_queue`는 삽입 순서가 아니라 비교 규칙상 가장 높은 우선순위의 요소를 `top()`으로 조회합니다.

**예제 코드 — [04_container_adaptors.cpp](./examples/04_container_adaptors.cpp)**

```cpp
#include <iostream>
#include <queue>
#include <stack>

int main() {
    std::queue<int> pending;
    pending.push(101);
    pending.push(102);
    std::cout << "Next queue item: " << pending.front() << '\n';
    pending.pop();

    std::stack<int> history;
    history.push(1);
    history.push(2);
    std::cout << "Latest history item: " << history.top() << '\n';
    history.pop();

    std::priority_queue<int> priorities;
    priorities.push(20);
    priorities.push(90);
    priorities.push(40);
    std::cout << "Highest priority: " << priorities.top() << '\n';
}
```

**실행 결과**

```text
Next queue item: 101
Latest history item: 2
Highest priority: 90
```

`front()`와 `top()`은 요소를 **조회**하고, `pop()`은 요소를 **제거**합니다. `pop()` 자체가 제거한 값을 반환하지는 않습니다. 또한 빈 컨테이너에서 `front()`·`top()`·`pop()`을 호출해서는 안 되므로 먼저 `empty()`를 확인합니다.

<a id="section-10-7"></a>

## 10.7. Iterators & Ranges — 반복자와 반열린 구간

**반복자(Iterator)** 는 컨테이너의 요소 위치를 나타내는 객체입니다. `begin()`은 첫 요소, `end()`는 마지막 요소가 아닌 **끝 바로 다음 위치**를 나타냅니다. `[begin, end)`처럼 시작을 포함하고 끝을 제외하는 범위를 **반열린 구간(Half-Open Range)** 이라고 합니다.

`cbegin()`과 `cend()`는 요소를 수정하지 않는 반복자를 반환합니다. `<iterator>`의 `std::distance()`는 두 반복자 사이의 거리를 계산합니다.

**예제 코드 — [05_iterator_ranges.cpp](./examples/05_iterator_ranges.cpp)**

```cpp
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    const std::vector<int> readings{12, 15, 19, 24};
    auto first = readings.cbegin();
    auto last = readings.cend();
    std::cout << "First: " << *first << '\n';
    std::cout << "Distance: " << std::distance(first, last) << '\n';

    int sum{};
    for (; first != last; ++first) {
        sum += *first;
    }
    std::cout << "Sum: " << sum << '\n';
}
```

**실행 결과**

```text
First: 12
Distance: 4
Sum: 70
```

반복 조건 `first != last`를 먼저 검사하기 때문에 마지막 반복자가 끝 위치에 도달한 뒤 역참조하지 않습니다. `*end()`처럼 끝 반복자를 역참조하면 안 됩니다.

`std::vector`는 임의 접근 반복자를 제공하므로 두 위치의 거리를 빠르게 계산할 수 있지만, `std::list` 같은 다른 종류의 반복자에서는 `distance()`가 요소를 따라 이동해야 할 수 있습니다.

<a id="section-10-8"></a>

## 10.8. Search & Predicates — 검색과 조건 검사

`<algorithm>`의 **알고리즘(Algorithm)** 은 검색·정렬·조건 검사 등 재사용 가능한 연산을 제공합니다. C++20의 `std::ranges` 알고리즘은 반복자 쌍 대신 컨테이너나 범위 자체를 전달할 수 있습니다.

**조건자(Predicate)** 는 조건 충족 여부를 `bool`로 반환하는 호출 가능한 객체입니다. Chapter 05에서 배운 람다(Lambda)를 조건자로 사용할 수 있습니다.

**예제 코드 — [06_search_predicates.cpp](./examples/06_search_predicates.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> response_ms{18, 45, 22, 90};
    const auto slow = std::ranges::find_if(response_ms, [](int value) {
        return value >= 80;
    });
    const bool valid = std::ranges::all_of(response_ms, [](int value) {
        return value >= 0;
    });
    const auto high_count = std::ranges::count_if(response_ms, [](int value) {
        return value >= 40;
    });

    if (slow != response_ms.end()) {
        std::cout << "First slow: " << *slow << " ms\n";
    }
    std::cout << std::boolalpha << "All valid: " << valid << '\n';
    std::cout << "At least 40 ms: " << high_count << '\n';
}
```

**실행 결과**

```text
First slow: 90 ms
All valid: true
At least 40 ms: 2
```

`find_if()`는 조건을 만족하는 **첫 위치**를 반환하며, 찾지 못하면 끝 반복자를 반환합니다. `all_of()`는 모든 값이 조건을 만족하는지 판단하고, `count_if()`는 조건을 만족하는 요소 수를 계산합니다.

검색 결과를 역참조하기 전에 `slow != response_ms.end()`를 확인해야 합니다. 컨테이너가 비어 있어도 이 검사는 안전합니다.

<a id="section-10-9"></a>

## 10.9. Stable Sorting — 정렬과 비교 규칙

**정렬(Sorting)** 은 주어진 비교 규칙으로 요소의 순서를 바꾸는 작업입니다. `<algorithm>`의 `std::sort()`는 일반적으로 `O(n log n)` 복잡도의 비교 정렬을 제공하며, `std::stable_sort()`는 비교 결과가 동등한 요소의 **원래 상대 순서**도 유지합니다.

여기서는 높은 우선순위를 먼저 배치하지만, 같은 우선순위를 가진 작업의 입력 순서는 유지하고 싶으므로 `stable_sort()`를 사용합니다.

**예제 코드 — [07_stable_sort.cpp](./examples/07_stable_sort.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Task {
    std::string name;
    int priority{};
};

int main() {
    std::vector<Task> tasks{{"scan", 2}, {"save", 1}, {"upload", 2}};
    std::stable_sort(tasks.begin(), tasks.end(), [](const Task& a, const Task& b) {
        return a.priority > b.priority;
    });

    for (const auto& task : tasks) {
        std::cout << task.name << ": " << task.priority << '\n';
    }
}
```

**실행 결과**

```text
scan: 2
upload: 2
save: 1
```

`scan`과 `upload`는 모두 우선순위가 `2`입니다. 동등한 작업이므로 입력된 순서 그대로 출력됩니다.

비교 함수는 **엄격 약순서(Strict Weak Ordering)** 를 만족해야 합니다. 예를 들어 `a.priority >= b.priority`는 같은 값에 대해 참이 되므로 정렬용 비교 함수로 부적절합니다. 이 예제는 `>`만 사용합니다.

<a id="section-10-10"></a>

## 10.10. Erase & Remove — 조건에 따른 요소 삭제

`std::vector`에서 특정 조건의 요소를 삭제하려면 요소의 **이동**과 컨테이너의 **크기 변경**을 구분해야 합니다. 기존의 `remove`·`erase` 관용구를 간단히 작성할 수 있도록 C++20은 `std::erase()`와 `std::erase_if()`를 제공합니다.

이 예제의 `std::erase(readings, -1)`은 값이 `-1`인 요소를 삭제하고, 실제 삭제 개수를 반환합니다. `<algorithm>`은 이런 알고리즘을 제공하고, `std::erase(vector, ...)`는 `<vector>`에 선언되어 있습니다.

**예제 코드 — [08_erase_remove.cpp](./examples/08_erase_remove.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> readings{20, -1, 18, -1, 25};
    const auto removed = std::erase(readings, -1);  // C++20

    std::cout << "Removed: " << removed << '\n';
    std::cout << "Remaining:";
    for (const int value : readings) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
```

**실행 결과**

```text
Removed: 2
Remaining: 20 18 25
```

삭제 후 `readings.size()`는 실제로 감소합니다. 반면 `std::ranges::remove_if()`는 요소를 재배치하고 **논리적 끝 위치를 반환**할 뿐, 컨테이너 크기를 줄이지 않습니다. 그 경우 반환된 범위를 `erase()`로 지워야 합니다.

삭제 작업 이후에는 기존 벡터 반복자가 무효화될 수 있으므로 이전 위치를 계속 사용하지 않습니다.

<a id="section-10-11"></a>

## 10.11. Transform & Aggregate — 변환과 집계

**변환(Transformation)** 은 각 요소에 일정한 규칙을 적용하여 새 값을 만드는 작업입니다. `std::ranges::transform()`은 입력 범위의 요소를 변환하고 출력 반복자에 기록합니다. `<iterator>`의 `std::back_inserter()`는 출력값을 컨테이너의 끝에 `push_back()`하는 반복자 어댑터입니다.

`<numeric>`의 `std::accumulate()`는 반복자 범위와 초기값을 받아 합계를 계산합니다.

**예제 코드 — [09_transform_and_aggregate.cpp](./examples/09_transform_and_aggregate.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> raw{10, 20, 30};
    std::vector<int> calibrated;
    calibrated.reserve(raw.size());
    std::ranges::transform(raw, std::back_inserter(calibrated), [](int value) {
        return value + 2;
    });

    const long long total = std::accumulate(calibrated.begin(), calibrated.end(), 0LL);
    std::cout << "Calibrated:";
    for (const int value : calibrated) {
        std::cout << ' ' << value;
    }
    std::cout << "\nTotal: " << total << '\n';
}
```

**실행 결과**

```text
Calibrated: 12 22 32
Total: 66
```

`raw`의 값 `10, 20, 30`에 각각 `2`를 더해 새 벡터를 만들었습니다. 원본을 수정하지 않는 방식이므로 원본 데이터가 필요한 경우에도 활용할 수 있습니다.

`0LL`은 누적값을 `long long`으로 시작하라는 뜻입니다. 일반적인 `0`을 사용하면 누적 계산의 타입이 `int`가 될 수 있습니다. `long long`도 표현 범위가 유한하므로 실제 데이터 범위는 확인해야 합니다.

<a id="section-10-12"></a>

## 10.12. Numeric Algorithms — 수치 알고리즘

`<numeric>`에는 단순 합계 이외에도 여러 수치 알고리즘이 있습니다. `std::inner_product()`는 두 범위의 대응하는 값을 곱한 뒤 합치며, `std::partial_sum()`은 각 위치까지의 누적합을 계산합니다.

다음 예제는 하나의 벡터를 두 번 전달해 제곱합을 구합니다. 이 연산은 정수값의 크기에 따라 오버플로가 발생할 수 있으므로 실제로는 자료형의 한계를 고려해야 합니다.

**예제 코드 — [10_numeric_algorithms.cpp](./examples/10_numeric_algorithms.cpp)**

```cpp
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> values{2, 4, 6, 8};
    const int total = std::accumulate(values.begin(), values.end(), 0);
    const int squared_sum = std::inner_product(values.begin(), values.end(),
                                               values.begin(), 0);
    std::vector<int> prefix(values.size());
    std::partial_sum(values.begin(), values.end(), prefix.begin());

    std::cout << "Total: " << total << '\n';
    std::cout << "Squared sum: " << squared_sum << '\n';
    std::cout << "Prefix:";
    for (const int value : prefix) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
```

**실행 결과**

```text
Total: 20
Squared sum: 120
Prefix: 2 6 12 20
```

`2² + 4² + 6² + 8² = 120`이므로 제곱합은 `120`입니다. 누적합 `2, 6, 12, 20`은 원래 데이터의 첫 요소부터 해당 위치까지 더한 결과입니다.

`std::inner_product()`는 두 번째 입력 범위에 접근하기 전에 충분한 요소가 있는지 보장해야 합니다. 여기서는 같은 벡터를 두 번 사용하므로 길이가 같습니다.

<a id="section-10-13"></a>

## 10.13. Ranges & Views — 필터와 변환 뷰

**범위(Range)** 는 처음부터 끝까지 순회할 수 있는 요소들의 집합입니다. C++20의 `<ranges>`에는 `std::views::filter`와 `std::views::transform`처럼 범위를 다른 방식으로 관찰하는 **뷰(View)** 가 포함됩니다.

`|` 기호는 여기에서 비트 OR 연산이 아니라 범위 어댑터를 연결하는 파이프 표현식으로 사용됩니다. 뷰는 일반적으로 결과 컨테이너를 즉시 새로 만드는 대신, 순회할 때 필요한 계산을 수행하는 **지연 평가(Lazy Evaluation)** 를 활용합니다.

**예제 코드 — [11_ranges_views.cpp](./examples/11_ranges_views.cpp)**

```cpp
#include <iostream>
#include <ranges>
#include <vector>

int main() {
    std::vector<int> readings{10, 21, 30, 42, 50};
    auto selected = readings
        | std::views::filter([](int value) { return value >= 20; })
        | std::views::transform([](int value) { return value / 2; });

    std::cout << "Half of >=20:";
    for (const int value : selected) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
```

**실행 결과**

```text
Half of >=20: 10 15 21 25
```

먼저 `20` 이상인 값을 선택한 뒤 각각 `2`로 나눕니다. 결과를 저장하기 위해 새로운 벡터를 생성하지 않습니다.

**수명 주의:** `selected`는 원본 `readings`에 의존합니다. 원본이 사라지거나 요소가 변경되어 반복자가 무효화되면 이전 뷰를 안전하게 사용할 수 없을 수 있습니다. `filter`의 내부 상태와 캐싱 때문에 원본을 수정한 후 동일 뷰를 재사용하는 것도 주의해야 합니다.

<a id="section-10-14"></a>

## 10.14. Materializing Views — 뷰 결과를 컨테이너로 복사

뷰에서 계산한 결과를 나중에도 **독립적으로 보관**하려면 소유하는 컨테이너로 복사할 수 있습니다. C++20에서는 `std::ranges::copy()`와 `std::back_inserter()`를 조합해 `std::vector`에 요소를 추가합니다.

이 예제는 원래 C++23의 `std::ranges::to`를 설명하던 파일 이름을 유지합니다. 하지만 실제 코드는 C++20의 표준 라이브러리만 사용합니다.

**예제 코드 — [12_ranges_to.cpp](./examples/12_ranges_to.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <ranges>
#include <vector>

int main() {
    const std::vector<int> readings{8, 15, 23, 4, 19};
    auto high_values = readings | std::views::filter([](int value) {
        return value >= 15;
    });

    // C++20에서는 ranges::copy와 back_inserter로 뷰를 소유 컨테이너에 복사합니다.
    std::vector<int> selected;
    std::ranges::copy(high_values, std::back_inserter(selected));
    std::cout << "Selected:";
    for (const int value : selected) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
```

**실행 결과**

```text
Selected: 15 23 19
```

`selected`는 결과값을 **소유**하므로 `high_values`와 달리 원본 벡터의 수명에 의존하지 않습니다. 결과를 장기간 보관하거나 다른 함수로 전달할 때 유용합니다.

C++23에는 `std::ranges::to<std::vector<int>>(range)` 같은 변환 기능이 추가되었습니다. 다만 이 구문은 **C++20에서 사용할 수 없으므로** 여기서는 참고 기능으로만 구분합니다.

<a id="section-10-15"></a>

## 10.15. Binary Search — 정렬된 데이터 검색

**이진 탐색(Binary Search)** 은 정렬된 데이터에서 검색 범위를 반복적으로 줄여 원하는 값을 찾습니다. `<algorithm>`의 `std::ranges::binary_search()`는 값의 존재 여부를 반환합니다. 원소가 `n`개인 임의 접근 범위에서 일반적으로 `O(log n)`번의 비교가 필요합니다.

`std::ranges::lower_bound()`는 지정한 값보다 작지 않은 **첫 위치**를 반환합니다. 이 반복자는 요소의 존재 여부와 삽입 위치를 판단할 때 사용할 수 있습니다.

**예제 코드 — [13_binary_search.cpp](./examples/13_binary_search.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> channels{9, 2, 7, 2, 5};
    std::ranges::sort(channels);

    const bool has_seven = std::ranges::binary_search(channels, 7);
    const auto first_two = std::ranges::lower_bound(channels, 2);
    std::cout << std::boolalpha << "Has 7: " << has_seven << '\n';
    std::cout << "First 2 index: " << (first_two - channels.begin()) << '\n';
}
```

**실행 결과**

```text
Has 7: true
First 2 index: 0
```

원래 입력 순서는 정렬되지 않았으므로 먼저 `std::ranges::sort()`를 실행합니다. 그 결과 `2, 2, 5, 7, 9`가 되어 `7`을 찾을 수 있고, `2`의 첫 위치 인덱스는 `0`입니다.

**전제 조건:** 이진 탐색에 사용하는 비교 기준과 정렬 기준이 일치해야 합니다. 정렬되지 않은 데이터를 그대로 전달해서는 올바른 결과를 기대할 수 없습니다.

<a id="section-10-16"></a>

## 10.16. Transparent Lookup — 다른 키 타입으로 조회

연관 컨테이너를 `std::map<std::string, int>`로 정의하면 `std::string_view` 키를 조회하기 위해 불필요한 문자열 생성이 발생할 수 있습니다. `<functional>`의 `std::less<>`는 **투명 비교(Transparent Comparison)** 를 지원하여 서로 비교할 수 있는 다른 키 타입으로 검색하는 방법을 제공합니다.

`std::map<std::string, int, std::less<>>`는 문자열을 보관하되 `find(std::string_view)`로 조회할 수 있습니다.

**예제 코드 — [14_transparent_lookup.cpp](./examples/14_transparent_lookup.cpp)**

```cpp
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <string_view>

int main() {
    const std::map<std::string, int, std::less<>> inventory{{"camera", 2}, {"lidar", 4}};
    const std::string_view key{"lidar"};
    const auto found = inventory.find(key);  // string 임시 객체 없이 조회
    if (found != inventory.end()) {
        std::cout << found->first << ": " << found->second << '\n';
    }
    std::cout << std::boolalpha << "Has imu: " << inventory.contains("imu") << '\n';
}
```

**실행 결과**

```text
lidar: 4
Has imu: false
```

`found->first`와 `found->second`는 각각 키와 값을 나타냅니다. `find()`가 `end()`를 반환할 수 있으므로 결과를 먼저 검사했습니다.

투명 조회를 지원하려면 비교 함수가 두 타입의 조합을 올바르게 비교할 수 있어야 합니다. 모든 연관 컨테이너에서 모든 키 타입의 변환이 자동으로 지원되는 것은 아닙니다.

<a id="section-10-17"></a>

## 10.17. Iterator Invalidation — 무효화된 반복자 피하기

**반복자 무효화(Iterator Invalidation)** 는 컨테이너를 변경한 뒤 이전 반복자가 더 이상 유효한 요소 위치를 나타내지 못하는 상황입니다. `std::vector::erase()`는 삭제 위치 이후의 반복자와 과거 `end()` 반복자를 무효화할 수 있습니다.

반복문 중 삭제해야 한다면 `erase()`가 반환하는 반복자를 다음 위치로 사용합니다.

**예제 코드 — [15_invalidation_safe_erase.cpp](./examples/15_invalidation_safe_erase.cpp)**

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> samples{10, -1, 20, -1, 30};
    for (auto it = samples.begin(); it != samples.end();) {
        if (*it < 0) {
            it = samples.erase(it);  // 삭제 후 반환된 유효한 반복자 사용
        } else {
            ++it;
        }
    }

    std::cout << "Valid:";
    for (const int value : samples) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
```

**실행 결과**

```text
Valid: 10 20 30
```

삭제한 뒤 `++it`를 무조건 실행하지 않고 `it = samples.erase(it)`로 반환된 위치를 사용합니다. 반대로 요소를 유지할 때만 `++it`를 실행합니다.

| 상황 | 주의할 점 |
|---|---|
| `vector` 재할당 | 모든 요소 반복자·참조·포인터가 무효화될 수 있음 |
| `vector`에서 요소 삭제 | 삭제 위치와 그 뒤의 반복자가 무효화됨 |
| `map`에 요소 삽입 | 기존 요소의 반복자는 일반적으로 유지됨 |
| `unordered_map` 리해싱 | 반복자는 무효화되지만 기존 요소 참조·포인터는 유지됨 |

빈 컨테이너의 `front()`·`back()` 호출이나 무효화된 반복자 역참조는 피해야 합니다.

<a id="section-10-18"></a>

## 10.18. Priority Scheduling — 우선순위에 따른 처리

작업을 우선순위에 따라 처리하려면 `<queue>`의 `std::priority_queue`를 활용할 수 있습니다. 기본 설정은 큰 값을 먼저 꺼내지만, `Task`처럼 여러 필드로 된 객체에서는 **비교 함수 객체(Function Object)** 로 우선순위를 정의해야 합니다.

이 예제는 우선순위 숫자가 큰 작업을 먼저 처리하고, 숫자가 같으면 이름의 사전순 오름차순으로 처리합니다.

**예제 코드 — [16_priority_scheduling.cpp](./examples/16_priority_scheduling.cpp)**

```cpp
#include <iostream>
#include <queue>
#include <string>
#include <vector>

struct Task {
    std::string name;
    int priority{};
};

struct LowerPriority {
    bool operator()(const Task& a, const Task& b) const {
        if (a.priority != b.priority) {
            return a.priority < b.priority;
        }
        return a.name > b.name;  // 동점이면 이름 오름차순
    }
};

int main() {
    std::priority_queue<Task, std::vector<Task>, LowerPriority> tasks;
    tasks.push({"scan", 70});
    tasks.push({"upload", 90});
    tasks.push({"navigate", 90});

    while (!tasks.empty()) {
        const Task& next = tasks.top();
        std::cout << next.name << ": " << next.priority << '\n';
        tasks.pop();
    }
}
```

**실행 결과**

```text
navigate: 90
upload: 90
scan: 70
```

비교 함수 `LowerPriority`가 `true`를 반환하면 첫 번째 작업이 두 번째 작업보다 우선순위가 낮다는 뜻으로 해석됩니다. 서로 다른 우선순위에서는 숫자가 작은 작업이 뒤로 가고, 동점일 때는 이름이 사전순으로 더 뒤인 작업이 밀립니다.

`top()`을 읽는 동안 큐를 변경하지 않고, 이후 `pop()`으로 해당 작업을 제거합니다. 고정된 입력에 항상 같은 결과가 필요하다면 **동점 처리 규칙**까지 명시해야 합니다.

<a id="section-10-19"></a>

## 10.19. Coding Practice

`exercises/`는 핵심 함수 구현이 비어 있는 시작 코드, `solutions/`는 모범답안입니다. 입력 확인과 출력 코드는 제공하므로 지정된 함수의 자료구조와 알고리즘을 완성하면 됩니다.

| 번호 | 실습 | 문제 파일 | 정답 코드 |
|:---:|---|---|---|
| 01 | Event Frequency — 이벤트 종류별 횟수 | [실습](./exercises/01_event_frequency.cpp) | [정답](./solutions/01_event_frequency.cpp) |
| 02 | Top-K Tasks — 우선순위 상위 K개 | [실습](./exercises/02_top_k_tasks.cpp) | [정답](./solutions/02_top_k_tasks.cpp) |
| 03 | Clean Readings — 무효값 및 중복 제거 | [실습](./exercises/03_clean_readings.cpp) | [정답](./solutions/03_clean_readings.cpp) |
| 04 | Device Summary — 장치별 통계 | [실습](./exercises/04_device_summary.cpp) | [정답](./solutions/04_device_summary.cpp) |

### Exercise 01 — Event Frequency

공백 없는 이벤트 이름 `n`개를 읽고 이름별 횟수를 **이름 오름차순**으로 출력합니다. `count_events(const std::vector<std::string>&)` 함수에 `std::map`을 사용해 횟수를 누적합니다.

**조건:** `1 ≤ n ≤ 10000`, 대소문자 구분, 중복 허용. 입력 개수 부족과 잘못된 `n`은 오류입니다.

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

빈 벡터를 함수에 전달하면 빈 `map`을 반환해야 합니다.

### Exercise 02 — Top-K Tasks

작업 이름과 우선순위를 받아 가장 높은 작업 `k`개를 출력합니다. `top_k()` 함수에서 `std::priority_queue`를 사용합니다.

**조건:** `1 ≤ k ≤ n ≤ 10000`, 우선순위 `0~100`, 높은 값 우선, 동점이면 **이름 사전순 오름차순**.

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

함수에 빈 벡터가 전달된 경우 빈 결과를 반환하도록 작성합니다.

### Exercise 03 — Clean Readings

측정값에서 무효값 `-1`을 제거하고, 나머지 값을 오름차순으로 정렬한 후 중복을 제거합니다. `clean_readings()`를 완성합니다.

**조건:** `1 ≤ n ≤ 10000`, 각 값은 `-1` 또는 `0~1000`. 결과가 비어 있다면 `EMPTY`를 출력합니다.

**입력**

```text
8
12 -1 7 12 30 -1 7 10
```

**출력**

```text
7 10 12 30
```

`std::ranges::unique()`는 논리적으로 중복을 제거할 위치를 반환합니다. 실제 벡터 크기를 줄이는 `erase()`까지 구현해야 합니다.

### Exercise 04 — Device Summary

장치 이름과 지연 시간 목록을 받아 장치별 건수와 평균 지연 시간을 계산합니다. `summarize()` 함수에서 `std::map<std::string, Stats>`로 통계를 누적합니다.

**조건:** `1 ≤ n ≤ 10000`, 지연 시간 `0~1000000`, 장치 이름 오름차순 출력, 평균 소수 첫째 자리.

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

지연 시간 합계는 여러 값을 더하므로 `long long`으로 저장합니다. `<iomanip>`의 `std::fixed`·`std::setprecision(1)`은 출력 소수 자리수를 지정합니다.

### 실습 컴파일과 자동 검사

`Chapter-10/` 폴더에서 실행합니다.

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/01_event_frequency.cpp -o event_frequency
./event_frequency
```

**예제와 모범답안 전체 검사**

```bash
python tests/check.py
```

**직접 작성한 Exercise 03 검사**

```bash
python tests/check.py --mode student --only exercise-03
```

첫 번째 명령어는 제공된 예제와 정답 코드의 동작을 확인합니다. 두 번째 명령어는 수정한 Exercise 03을 검사합니다. 시작 코드에서 `TODO`를 구현하지 않은 상태라면 테스트가 실패하는 것이 정상입니다. Clang을 사용하려면 `--compiler clang++`를 추가할 수 있습니다.

<a id="section-10-20"></a>

## 10.20. Mini Project — Device Event Summary

장치에서 수집한 이벤트를 분류하고 통계 보고서를 생성하는 콘솔 프로그램을 작성합니다. `std::map`의 정렬된 출력, 장치별 집계, 반복문, 함수 분리를 함께 사용합니다.

**프로젝트 파일**

- [시작 코드 — `project/device_event_summary.cpp`](./project/device_event_summary.cpp)
- [모범답안 — `solutions/device_event_summary.cpp`](./solutions/device_event_summary.cpp)

**입력 형식:** 첫 줄에 레코드 수 `n(1~100)`, 다음 `n`줄에 `장치명 수준 지연시간`을 입력합니다. 장치명은 공백 없는 1~20바이트 문자열, 수준은 `INFO`·`WARN`·`ERROR` 중 하나, 지연 시간은 `0~1000000`ms 정수입니다.

**구현할 함수**

```cpp
void add_record(Report& report, const std::string& device,
                const std::string& level, int latency);
```

이 함수에서 장치별 이벤트 수·지연 시간 합계와 전체 이벤트 수·지연 시간 합계, `WARN`·`ERROR` 발생 횟수를 갱신합니다. 입력과 출력은 제공된 `main()`에서 처리합니다.

**입력**

```text
6
CAM INFO 12
LIDAR WARN 80
CAM ERROR 24
CAM WARN 36
LIDAR INFO 20
IMU INFO 5
```

**출력** (입력 안내 문구 제외)

```text
--- Device Event Summary ---
Events: 6
Devices: 3
Warnings: 2
Errors: 1
Average latency: 29.50 ms
CAM: 3 events, avg 24.0 ms
IMU: 1 events, avg 5.0 ms
LIDAR: 2 events, avg 50.0 ms
Top device: CAM (3)
```

**처리 규칙**

1. 장치별 보고서는 이름 오름차순으로 출력합니다.
2. 전체 평균은 소수 둘째 자리, 장치별 평균은 소수 첫째 자리로 표시합니다.
3. 최다 이벤트 장치는 이벤트 수가 가장 큰 장치입니다. 동률이면 이름이 사전순으로 앞선 장치를 선택합니다.
4. 입력 오류가 있으면 표준 오류에 메시지를 출력하고 종료 코드 `1`을 반환합니다.
5. 합계에는 `long long`을 사용합니다. 이벤트 수는 최대 100개이므로 문제에서 지정한 범위 내의 합계를 안전하게 표현할 수 있습니다.

**완료 기준:** 정상 입력·1개 입력·동점·잘못된 이벤트 수준·범위 밖 지연 시간을 처리하고, 보고서의 통계와 출력 순서가 일치해야 합니다.

**프로젝트 검사**

```bash
python tests/check.py --mode student --only project
```

모범답안 테스트를 실행하려면 `--mode student`를 제외하면 됩니다.

### Multi-File Example — Event Summary

같은 주제를 파일 단위로 나눈 예제도 제공합니다. `summary.hpp`에 함수 선언과 `Summary` 자료형을 두고, `summary.cpp`에 구현, `main.cpp`에 호출 코드를 작성했습니다. Chapter 05에서 학습한 헤더·구현 분리를 표준 컨테이너에 적용한 사례입니다.

```text
examples/17_event_summary/
├── CMakeLists.txt
├── summary.hpp
├── summary.cpp
├── main.cpp
└── summary_tests.cpp
```

**CMake 빌드 및 테스트**

```bash
cmake -S examples/17_event_summary -B build/event_summary -DCMAKE_CXX_STANDARD=20
cmake --build build/event_summary
ctest --test-dir build/event_summary --output-on-failure
```

`CMakeLists.txt`에서 C++20을 요구하고 두 가지 검증을 CTest에 등록했습니다. 저장소 전체 GitHub CI의 기존 프로젝트 경로 `examples/17_event_summary/`도 유지했습니다.

<a id="section-10-21"></a>

## 10.21. Quiz & Summary

### Quiz

**1.** 장치 ID의 정렬 순서대로 결과를 출력해야 합니다. 어떤 컨테이너가 적절한가요?

A. `std::unordered_map`
B. `std::map`
C. `std::stack`
D. `std::queue`

<details>
<summary>정답 및 해설</summary>

**정답: B. `std::map`**

`std::map`은 키의 비교 순서로 요소를 관리합니다. `unordered_map`은 빠른 평균 조회가 가능하지만 출력 순서를 보장하지 않습니다.

</details>

**2.** `std::vector<int> v; v.reserve(100);` 다음에 `v[0]`을 사용할 수 있나요?

<details>
<summary>정답 및 해설</summary>

**정답: 사용할 수 없습니다.**

`reserve()`는 용량(`capacity`) 확보 요청일 뿐 요소 수(`size`)를 늘리지 않습니다. 요소는 `push_back()`으로 추가하거나 `resize()`로 생성해야 합니다.

</details>

**3.** `std::ranges::find_if()`가 검색에 실패하면 무엇을 반환하나요?

A. `nullptr`
B. `-1`
C. 끝 반복자
D. 예외

<details>
<summary>정답 및 해설</summary>

**정답: C. 끝 반복자**

컨테이너에서 검색한 경우 `container.end()`와 비교한 뒤 역참조해야 합니다. `end()` 자체를 역참조해서는 안 됩니다.

</details>

**4.** `std::stable_sort()`는 `std::sort()`와 무엇이 다른가요?

<details>
<summary>정답 및 해설</summary>

**정답: 비교 결과가 동등한 요소의 기존 상대 순서를 보존합니다.**

우선순위가 같은 작업을 입력된 순서대로 유지해야 할 때 적합합니다. 일반 정렬은 동등한 요소의 순서 보존을 보장하지 않습니다.

</details>

**5.** `std::priority_queue`에서 `top()`과 `pop()`의 동작을 올바르게 설명한 것은?

A. 둘 다 최우선 요소를 반환합니다.
B. `top()`은 조회, `pop()`은 제거합니다.
C. `top()`은 제거, `pop()`은 조회합니다.
D. 둘 다 첫 삽입 요소를 처리합니다.

<details>
<summary>정답 및 해설</summary>

**정답: B.**

`top()`은 최우선 요소를 참조하고, `pop()`은 해당 요소를 제거하지만 값을 반환하지는 않습니다. 사용 전 `empty()` 확인이 필요합니다.

</details>

**6.** `std::map`과 `std::unordered_map`의 조회 시간 복잡도를 비교해 보세요.

<details>
<summary>정답 및 해설</summary>

**모범답안:** `std::map`은 일반적으로 `O(log n)`입니다. `std::unordered_map`은 평균 `O(1)`이지만 해시 충돌 등의 영향으로 최악에는 `O(n)`까지 증가할 수 있습니다.

실제 성능은 요소 수, 해시 함수, 키 분포, 메모리 접근 특성에도 영향을 받습니다.

</details>

**7.** 다음 중 C++20에서 바로 사용할 수 없는 코드는 무엇인가요?

A. `std::ranges::sort(values)`
B. `std::views::filter(predicate)`
C. `std::ranges::to<std::vector<int>>(range)`
D. `std::erase(values, -1)`

<details>
<summary>정답 및 해설</summary>

**정답: C. `std::ranges::to`**

`std::ranges::to`는 C++23에 추가되었습니다. C++20에서는 `std::ranges::copy()`와 `std::back_inserter()` 등을 조합해 복사할 수 있습니다.

</details>

**8.** `std::ranges::remove_if()`만 호출하면 `std::vector`의 `size()`가 줄어드나요?

<details>
<summary>정답 및 해설</summary>

**정답: 아닙니다.**

제거 대상이 아닌 요소를 앞쪽으로 이동하고 논리적인 새 끝 위치를 반환합니다. 실제 크기를 변경하려면 뒤에 남은 범위를 `erase()`로 삭제해야 합니다. C++20의 `std::erase_if()`는 이를 한 번에 수행할 수 있습니다.

</details>

**9.** 이진 탐색을 수행하기 전에 필요한 조건은 무엇인가요?

A. 중복 값이 없어야 합니다.
B. 값이 모두 양수여야 합니다.
C. 데이터가 검색 비교 기준에 맞게 정렬되어 있어야 합니다.
D. 컨테이너가 반드시 `std::list`여야 합니다.

<details>
<summary>정답 및 해설</summary>

**정답: C.**

이진 탐색은 정렬된 데이터에서 검색 영역을 줄이는 알고리즘입니다. 중복은 허용할 수 있으며, `vector`처럼 임의 접근이 가능한 범위가 효율적입니다.

</details>

**10.** `std::views::filter`로 만든 뷰를 저장할 때 원본 데이터에 대해 무엇을 확인해야 하나요?

<details>
<summary>정답 및 해설</summary>

**모범답안:** 뷰가 원본을 참조하는 경우 원본의 수명이 뷰 사용 기간보다 길어야 하고, 컨테이너 변경으로 참조·반복자가 무효화되지 않아야 합니다.

뷰를 만들었다고 항상 결과 데이터가 별도로 복사되는 것은 아닙니다.

</details>

**11.** `std::vector`를 순회하면서 `erase(it)`를 호출했습니다. 다음 반복에서 사용하기 좋은 반복자는?

A. 삭제에 사용한 기존 `it`
B. `erase()`가 반환한 반복자
C. 반드시 `begin()` 이전의 반복자
D. `end()`를 역참조한 값

<details>
<summary>정답 및 해설</summary>

**정답: B.**

벡터에서 삭제 위치 이후의 기존 반복자는 무효화될 수 있습니다. 반환된 유효한 다음 위치를 사용해야 안전하게 순회를 계속할 수 있습니다.

</details>

**12.** `std::unordered_map`을 이용해 빈도를 집계했는데 출력 순서가 실행 환경마다 다릅니다. 어떻게 해결할 수 있을까요?

<details>
<summary>정답 및 해설</summary>

**모범답안:** 결과를 키 기준으로 정렬해 출력하거나, 처음부터 `std::map`에 집계합니다.

`unordered_map`의 내부 순서에 의존하지 않는 것이 중요합니다. 정렬된 출력을 얻기 위한 비용과 데이터 크기를 함께 고려해 선택합니다.

</details>

### Summary

- **컨테이너:** 삽입 순서, 정렬 여부, 키 중복, 검색 비용에 따라 선택합니다.
- **반복자:** `[begin, end)` 구간을 사용하며 끝 위치를 역참조하지 않습니다.
- **연관 컨테이너:** `map`·`set`은 정렬 순서, `unordered_map`·`unordered_set`은 해시 기반 조회에 적합합니다.
- **컨테이너 어댑터:** `queue`는 FIFO, `stack`은 LIFO, `priority_queue`는 비교 규칙에 따른 우선순위로 처리합니다.
- **표준 알고리즘:** 검색·정렬·삭제·변환·누적 계산을 명확한 함수 호출로 표현합니다.
- **Ranges & Views:** C++20에서 필터와 변환을 조합할 수 있으며, 원본의 수명과 지연 평가 특성을 고려해야 합니다.
- **반복자 무효화:** 컨테이너를 변경한 뒤 기존 위치를 재사용할 수 있는지 확인합니다.
- **C++23 구분:** `std::ranges::to`는 C++20 범위에 포함되지 않습니다.

### References

- [cppreference — Containers](https://en.cppreference.com/w/cpp/container)
- [cppreference — Iterators](https://en.cppreference.com/w/cpp/iterator)
- [cppreference — Algorithms](https://en.cppreference.com/w/cpp/algorithm)
- [cppreference — Ranges](https://en.cppreference.com/w/cpp/ranges)
- [cppreference — `std::erase` / `std::erase_if`](https://en.cppreference.com/w/cpp/container/vector/erase2)
- [cppreference — `std::ranges::to` (C++23)](https://en.cppreference.com/w/cpp/ranges/to)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

---

[← C++ 목차](../README.md#contents) · [이전 Chapter — Object-Oriented Programming](../Chapter-09/) · [다음 Chapter — Error Handling](../Chapter-11/)
