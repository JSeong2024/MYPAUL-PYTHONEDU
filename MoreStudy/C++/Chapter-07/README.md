# Chapter 07. Pointers & References

포인터와 참조의 기본 개념부터 `const`, 매개변수 설계, 객체 수명, 동적 메모리 및 스마트 포인터까지 다룹니다. 기존 Chapter에서 사용한 배열과 함수가 메모리의 객체를 어떻게 참조하는지 확인하고, 실제 프로젝트에서 잘못된 메모리 접근을 예방하는 방법을 학습합니다.

본 자료는 **C++23(ISO/IEC 14882:2024)**을 기준으로 작성되었습니다. 예제는 GCC 14 이상 또는 C++23 표준 라이브러리 지원이 충분한 컴파일러 환경을 권장합니다.

## Contents

| Section | Topic |
|:---:|---|
| 7.1 | 객체, 주소와 수명 |
| 7.2 | 포인터 선언과 역참조 |
| 7.3 | `nullptr`와 선택적인 대상 |
| 7.4 | 참조와 함수 매개변수 |
| 7.5 | `const`와 포인터의 읽기·쓰기 권한 |
| 7.6 | 포인터 반환과 검색 API |
| 7.7 | 연속 데이터와 `std::span` |
| 7.8 | 포인터·참조 무효화와 댕글링 |
| 7.9 | 동적 메모리, RAII와 `std::unique_ptr` |
| 7.10 | 공유 소유권과 `std::weak_ptr` |
| 7.11 | 외부 API 경계의 포인터와 길이 |
| 7.12 | `std::reference_wrapper`와 선택적 참조 |
| 7.13 | 포인터 연산과 범위 제한 |
| 7.14 | 메모리 오류 탐지 및 디버깅 |
| 7.15 | 실무에서의 매개변수·소유권 선택 |
| 7.16 | Coding Practice |
| 7.17 | Quiz & Summary |

---

## 7.1. 객체, 주소와 수명

C++에서 변수는 자료형에 따른 객체를 저장하거나 참조하는 이름으로 사용할 수 있습니다. 객체는 메모리의 일정 영역에 존재하며, **주소(address)**와 **수명(lifetime)**이라는 특징이 있습니다. 메모리 주소는 실행 환경에 따라 달라지므로 출력된 주소 자체를 고정된 값으로 사용해서는 안 됩니다.

```cpp
int temperature{24};
int* pointer{&temperature};
int& reference{temperature};
```

| 표현 | 의미 |
|---|---|
| `temperature` | `int` 객체 |
| `&temperature` | 객체의 주소를 얻는 표현식 |
| `int* pointer` | `int` 객체를 가리킬 수 있는 포인터 변수 |
| `int& reference` | 기존 `int` 객체에 결합되는 참조 |
| `*pointer` | 포인터가 가리키는 객체에 접근하는 역참조 표현식 |

**중요한 구분**

- **포인터:** 대상을 가리키거나 `nullptr`로 비워 둘 수 있음. 다른 대상으로 변경 가능
- **참조:** 선언 시 유효한 대상에 결합해야 함. 일반적인 참조는 다른 대상으로 재결합할 수 없음
- **소유권:** 포인터나 참조가 객체의 존재 기간을 자동으로 연장하지 않음
- **수명:** 원본 객체가 파괴된 뒤 이를 참조하면 잘못된 메모리 접근이 발생할 수 있음

참조를 사용할 때 문법상 포인터 연산을 직접 작성하지 않더라도, 실제로 접근하는 객체가 존재해야 한다는 규칙은 같습니다.

---

## 7.2. 포인터 선언과 역참조

포인터는 특정 자료형의 객체를 가리킬 수 있습니다. `&`로 주소를 얻고, `*`로 그 주소의 객체를 읽거나 수정합니다. 포인터를 사용하기 전에는 **유효한 객체를 가리키는지** 보장해야 합니다.

**예제 코드 — [01_addresses_and_dereference.cpp](./examples/01_addresses_and_dereference.cpp)**

```cpp
#include <print>

int main() {
    int temperature{24};
    int* reading{&temperature};

    std::println("Original: {} C", temperature);
    *reading = 26;
    std::println("Updated: {} C", temperature);
    std::println("Same object: {}", reading == &temperature);
}
```

**실행 결과**

```text
Original: 24 C
Updated: 26 C
Same object: true
```

`reading`은 `temperature`와 동일한 객체를 가리킵니다. `*reading = 26`은 포인터 변수 자체를 변경하는 것이 아니라 포인터가 가리키는 정수 객체를 수정합니다.

주소 비교는 같은 객체를 가리키는지 확인하기 위한 용도로 사용할 수 있습니다. 단, 주소 숫자를 가정해서 처리하는 방식은 피해야 합니다.

**주의:** `int* pointer;`처럼 초기화하지 않은 포인터를 역참조하는 코드는 잘못된 접근으로 이어질 수 있습니다. 즉시 연결할 객체가 없다면 `int* pointer{nullptr};`로 초기화합니다.

---

## 7.3. `nullptr`와 선택적인 대상

검색 결과나 선택적인 장치처럼 **대상이 없을 수 있다면** 포인터로 이를 표현할 수 있습니다. `nullptr`는 아무 객체도 가리키지 않는 포인터 값입니다.

```cpp
const int* reading{nullptr};
if (reading != nullptr) {
    // 이 경로에서는 객체가 유효하다는 별도의 수명 보장도 필요
}
```

`nullptr` 여부를 검사하면 null 포인터 역참조를 막을 수 있지만, **null이 아니라고 반드시 유효한 포인터는 아닙니다.** 이미 파괴된 객체를 가리키는 포인터도 null이 아닐 수 있습니다.

**예제 코드 — [02_nullable_pointer.cpp](./examples/02_nullable_pointer.cpp)**

```cpp
#include <print>

void print_temperature(const int* reading) {
    if (reading == nullptr) {
        std::println("No sensor reading");
        return;
    }
    std::println("Sensor: {} C", *reading);
}

int main() {
    const int measured{23};
    print_temperature(&measured);
    print_temperature(nullptr);
}
```

**실행 결과**

```text
Sensor: 23 C
No sensor reading
```

장치가 연결되지 않거나 값이 아직 도착하지 않은 상황을 예로 들었습니다. 포인터를 역참조하기 전 `nullptr`을 확인하고, 해당 함수 호출 동안 원본 정수가 살아 있어야 한다는 계약을 유지합니다.

**실무 기준:** null이 허용되지 않는 필수 인수라면 참조를 우선 고려합니다. null이 업무적으로 의미 있는 경우에만 포인터나 `std::optional` 같은 표현을 사용합니다.

---

## 7.4. 참조와 함수 매개변수

참조(`T&`)는 호출자가 가진 객체를 함수에서 직접 다룰 수 있도록 합니다. `const T&`는 원본을 복사하지 않고 읽을 때 사용하며, 해당 참조를 통해 객체를 수정하지 못하도록 제한합니다.

```cpp
void read_only(const int& value);
void update(int& value);
```

| 매개변수 | 용도 | 호출자 수정 |
|---|---|:---:|
| `int value` | 작은 값을 복사하여 계산 | X |
| `const std::string& text` | 기존 큰 객체를 복사 없이 읽기 | X |
| `int& current` | 기존 객체를 반드시 수정 | O |
| `int* current` | 대상이 없을 수도 있거나 C API와 연동 | 조건부 |
| `std::string_view text` | 문자열을 소유하지 않고 읽기 | X |

`int&` 매개변수를 사용했다면 함수명과 설명에서 **입력 객체를 수정한다는 사실**을 명확히 드러내는 것이 좋습니다.

**예제 코드 — [03_reference_parameters.cpp](./examples/03_reference_parameters.cpp)**

```cpp
#include <algorithm>
#include <print>

[[nodiscard]] int clamp_rpm(int requested) noexcept {
    return std::clamp(requested, 0, 3'000);
}

void update_rpm(int& current, int requested) noexcept {
    current = clamp_rpm(requested);
}

int main() {
    int motor_rpm{1'200};
    update_rpm(motor_rpm, 3'500);
    std::println("Motor: {} RPM", motor_rpm);
}
```

**실행 결과**

```text
Motor: 3000 RPM
```

`update_rpm()`은 참조 매개변수로 기존 모터 회전수를 변경합니다. 허용 범위를 판단하는 계산은 별도 함수로 분리해 검증을 단순화했습니다.

센서나 모터 장치 자체를 직접 제어하는 코드는 아니며, 요청값을 프로그램 내부 상태로 반영하는 예제입니다.

**참고:** 반환값만 필요하다면 `[[nodiscard]] int clamp_rpm(int)`처럼 값을 반환하는 방식이 더 명확할 수 있습니다. 참조를 사용했다고 항상 성능이 좋아지는 것은 아닙니다.

---

## 7.5. `const`와 포인터의 읽기·쓰기 권한

`const`가 어디에 붙는지에 따라 **가리키는 객체의 수정 가능 여부**와 **포인터의 대상 변경 가능 여부**가 다릅니다.

| 선언 | 값 수정 | 대상 변경 | 의미 |
|---|:---:|:---:|---|
| `int* p` | O | O | 수정 가능한 객체를 가리키는 포인터 |
| `const int* p` | X | O | 읽기 전용 경로로 접근하는 포인터 |
| `int* const p` | O | X | 다른 대상으로 바꿀 수 없는 포인터 |
| `const int* const p` | X | X | 읽기 전용 경로이며 대상 고정 |

`const int*`가 가리키는 원본이 반드시 `const` 객체라는 뜻은 아닙니다. 다른 경로에서는 원본을 수정할 수도 있습니다. 여기서 제한하는 것은 해당 포인터 표현식을 통한 수정입니다.

**예제 코드 — [04_const_correctness.cpp](./examples/04_const_correctness.cpp)**

```cpp
#include <print>

int main() {
    int speed{120};
    int backup{80};

    const int* read_only{&speed};
    read_only = &backup;  // 다른 객체를 가리킬 수 있음

    int* const fixed_target{&speed};
    *fixed_target = 130; // 가리키는 값은 수정 가능

    const int* const fixed_read_only{&speed};

    std::println("Backup: {}", *read_only);
    std::println("Speed: {}", *fixed_target);
    std::println("Read-only speed: {}", *fixed_read_only);
}
```

**실행 결과**

```text
Backup: 80
Speed: 130
Read-only speed: 130
```

`read_only`는 다른 정수를 가리킬 수 있지만 해당 경로를 통해 값을 수정할 수 없습니다. `fixed_target`은 포인터 자체가 고정되어 있지만 원본 값은 수정할 수 있습니다.

---

## 7.6. 포인터 반환과 검색 API

검색 함수가 결과를 찾을 수도 있고 찾지 못할 수도 있다면, 기존 객체의 주소를 반환하는 간단한 API를 구성할 수 있습니다.

```cpp
[[nodiscard]] const std::string* find_device(
    const std::vector<std::string>& devices,
    std::string_view target);
```

이 함수는 문자열을 새로 만들거나 소유하지 않습니다. **호출자가 소유한 컨테이너의 요소를 빌려주는 방식**이므로 반환된 포인터의 수명은 원본 컨테이너와 그 요소의 유효성에 의존합니다.

**예제 코드 — [05_pointer_lookup.cpp](./examples/05_pointer_lookup.cpp)**

```cpp
#include <print>
#include <string>
#include <string_view>
#include <vector>

[[nodiscard]] const std::string* find_device(
    const std::vector<std::string>& devices, std::string_view target) {
    for (const auto& device : devices) {
        if (device == target) {
            return &device;
        }
    }
    return nullptr;
}

int main() {
    const std::vector<std::string> devices{"lidar", "camera", "imu"};
    if (const auto* result = find_device(devices, "camera")) {
        std::println("Found: {}", *result);
    }
    std::println("Missing: {}", find_device(devices, "gps") == nullptr);
}
```

**실행 결과**

```text
Found: camera
Missing: true
```

검색 성공 시 기존 `std::string` 요소를 가리키는 포인터를 반환하고, 실패 시 `nullptr`를 반환합니다. 입력 벡터가 `const`이므로 결과도 `const std::string*`로 표현합니다.

**주의:** 원본 벡터를 파괴하거나 재할당하는 변경을 수행한 뒤에는 기존 요소 포인터를 재사용하지 않습니다.

---

## 7.7. 연속 데이터와 `std::span`

기존 C 스타일 인터페이스는 흔히 `pointer + length`로 배열을 전달합니다. 하지만 두 정보가 별개이기 때문에 길이를 잘못 전달하면 범위를 벗어난 메모리에 접근할 위험이 있습니다.

`std::span<T>`은 **연속된 요소의 시작 위치와 개수**를 하나의 뷰로 표현합니다. `std::array`, `std::vector` 등 다양한 연속 저장소를 동일한 인터페이스로 받을 수 있습니다.

| 표현 | 의미 |
|---|---|
| `std::span<const int>` | 원본 소유권 없이 정수 요소 읽기 |
| `std::span<int>` | 원본 소유권 없이 정수 요소 수정 가능 |
| `values.size()` | 요소 개수 조회 |
| `values.empty()` | 빈 구간 검사 |
| `values[i]` | 지정 인덱스 접근. C++23에서 자동 범위 검사 보장 안 됨 |

`std::span`도 **소유권을 가지지 않습니다.** 반환값이나 필드로 저장한다면 원본 객체의 수명을 따로 보장해야 합니다.

**예제 코드 — [06_span_parameter.cpp](./examples/06_span_parameter.cpp)**

```cpp
#include <array>
#include <print>
#include <span>
#include <vector>

[[nodiscard]] double average(std::span<const int> values) noexcept {
    if (values.empty()) {
        return 0.0; // 이 API에서는 빈 구간을 0으로 정의
    }

    double sum{0.0};
    for (const int value : values) {
        sum += value;
    }
    return sum / static_cast<double>(values.size());
}

int main() {
    const std::array fixed{10, 20, 30};
    const std::vector dynamic{40, 50, 60};
    std::println("Fixed: {:.1f}", average(fixed));
    std::println("Dynamic: {:.1f}", average(dynamic));
}
```

**실행 결과**

```text
Fixed: 20.0
Dynamic: 50.0
```

하나의 `average()` 함수로 `std::array`와 `std::vector`를 모두 처리합니다. 빈 구간을 0으로 처리하는 것은 이 예제의 설계 정책일 뿐이며, 일반적으로는 `std::optional<double>`을 반환해 **결과 없음**을 별도로 표현할 수도 있습니다.

**실무 기준:** 외부 입력의 인덱스로 접근할 때는 먼저 크기를 비교합니다. `std::span`만 사용한다고 범위 오류가 자동으로 사라지지는 않습니다.

---

## 7.8. 포인터·참조 무효화와 댕글링

**댕글링 포인터(dangling pointer)** 또는 **댕글링 참조**는 원본 객체가 사라졌거나 참조 대상이 유효하지 않은데도 과거의 주소·참조를 계속 사용하는 경우입니다.

대표적인 원인은 다음과 같습니다.

- 함수 내부 지역 변수의 주소나 참조 반환
- `std::vector`의 재할당 후 기존 요소의 포인터·참조 사용
- 파괴된 `std::string`을 참조하는 `std::string_view` 사용
- `std::unique_ptr`가 소유한 객체 파괴 후 기존 비소유 포인터 사용

아래 코드는 **실행하면 안 되는 잘못된 예**입니다.

```cpp
// 잘못된 예 — 지역 변수의 수명이 끝남
int* invalid_address() {
    int local{42};
    return &local;
}

// 잘못된 예 — vector 재할당 시 기존 포인터가 무효화될 수 있음
std::vector<int> values{10, 20};
int* previous = &values[0];
values.push_back(30);
// *previous 사용 금지: 재할당이 발생했다면 무효한 포인터
```

`std::vector::push_back()`이 **항상** 기존 포인터를 무효화하는 것은 아닙니다. `capacity()`를 초과하여 재할당이 발생할 때 기존 요소를 가리키던 포인터·참조·반복자가 무효화됩니다. `erase()`처럼 다른 동작도 무효화 규칙이 있으므로 해당 API 문서를 확인해야 합니다.

**예제 코드 — [07_vector_invalidation.cpp](./examples/07_vector_invalidation.cpp)**

```cpp
#include <print>
#include <vector>

int main() {
    std::vector<int> samples{10, 20};
    const std::size_t index{1};

    // push_back 과정에서 재할당되면 기존 포인터가 무효화될 수 있음.
    // 요소의 인덱스만 보관하고 변경 후 다시 접근함.
    samples.push_back(30);

    if (index < samples.size()) {
        std::println("Sample: {}", samples[index]);
    }
    std::println("Count: {}", samples.size());
}
```

**실행 결과**

```text
Sample: 20
Count: 3
```

변경 후에도 필요한 것은 특정 인덱스의 값이므로, 포인터 대신 인덱스를 보관합니다. 요소를 추가한 다음 다시 범위를 확인하고 `samples[index]`로 접근합니다. 이 방법도 요소 삭제·재정렬로 인덱스가 가리키는 **논리적 대상**이 달라지는 경우에는 별도 처리가 필요합니다.

---

## 7.9. 동적 메모리, RAII와 `std::unique_ptr`

C++에서는 객체의 저장 기간과 실제 메모리 할당 방식을 구분해야 합니다. 함수의 지역 객체처럼 블록 범위에서 수명이 관리되는 객체도 있고, 실행 중 동적으로 메모리를 확보해 만드는 객체도 있습니다.

과거에는 `new`와 `delete`를 직접 작성했지만, 일반적인 애플리케이션 개발에서는 객체 수명을 **RAII(Resource Acquisition Is Initialization)** 및 표준 라이브러리 타입으로 관리하는 방식이 더 안전합니다.

- **지역 객체:** 특정 범위를 벗어날 때 자동 정리
- **`std::vector`, `std::string`:** 내부 동적 메모리를 컨테이너가 소유 및 관리
- **`std::unique_ptr<T>`:** 하나의 소유자가 객체 수명을 관리하는 스마트 포인터
- **`std::make_unique<T>()`:** 동적 객체를 만들고 소유권을 즉시 `unique_ptr`에 연결
- **`std::move()`:** 이동을 허용하는 표현식. 실제 이동 여부와 동작은 해당 타입에 의해 결정

단일 객체를 동적으로 만들고 독점적으로 소유해야 하는 경우에 `std::unique_ptr`를 고려합니다. 항상 동적 할당이 필요한 것은 아니며, 충분하다면 지역 객체나 표준 컨테이너가 더 단순합니다.

**예제 코드 — [08_unique_ptr.cpp](./examples/08_unique_ptr.cpp)**

```cpp
#include <memory>
#include <print>
#include <string>
#include <utility>

void consume_config(std::unique_ptr<std::string> config) {
    if (config) {
        std::println("Loaded config: {}", *config);
    }
}

int main() {
    auto config = std::make_unique<std::string>("motor.max_rpm=3000");
    consume_config(std::move(config));
    std::println("Ownership transferred: {}", config == nullptr);
}
```

**실행 결과**

```text
Loaded config: motor.max_rpm=3000
Ownership transferred: true
```

`consume_config()`는 `std::unique_ptr<std::string>`을 값으로 받아 소유권을 이전받습니다. 호출자는 `std::move()`로 이전 의도를 명시합니다. 이 예제에서 이동 후 원래 `unique_ptr`는 비어 있습니다.

소유권 이전이 필요 없는 단순 읽기 함수라면 `const std::string&`이나 `std::string_view`를 사용하는 편이 적절합니다.

**피해야 할 방식**

```cpp
// 일반적인 새 코드에서 불필요한 직접 소유권 관리
int* value = new int{10};
// ... 많은 실행 경로 ...
delete value;
```

위 코드가 무조건 틀린 것은 아니지만 예외나 조기 반환에서 정리 누락이 발생하기 쉽습니다. **`new`/`delete`를 직접 관리해야 하는 저수준 코드와 일반적인 애플리케이션 코드를 구분**합니다.

---

## 7.10. 공유 소유권과 `std::weak_ptr`

여러 객체가 **하나의 자원의 수명을 공동으로 관리해야 한다면** `std::shared_ptr<T>`를 고려할 수 있습니다. 마지막 `shared_ptr` 소유자가 사라질 때 관리 대상 객체가 정리됩니다.

반대로 객체를 **소유하지 않고 관찰만 해야 하는 경우**에는 `std::weak_ptr<T>`를 사용합니다. `weak_ptr`는 객체가 살아 있는지 직접 보장하지 않으므로 `lock()`으로 유효한 `shared_ptr`를 얻은 뒤 접근합니다.

| 타입 | 소유권 | 주요 용도 |
|---|---|---|
| `std::unique_ptr<T>` | 독점 | 단일 소유자가 명확한 자원 |
| `std::shared_ptr<T>` | 공유 | 여러 소유자가 함께 수명을 보장해야 하는 자원 |
| `std::weak_ptr<T>` | 비소유 관찰 | 공유 소유 대상의 존재 여부 확인, 순환 소유 방지 |
| `T*`, `T&` | 보통 비소유 | 이미 수명이 보장된 객체에 일시적으로 접근 |

`shared_ptr`는 참조 횟수 관리의 비용이 있으므로 아무 객체에나 적용하지 않습니다. 특히 `shared_ptr`끼리 서로를 소유하는 구조에서는 **순환 참조**로 인해 객체가 정리되지 않을 수 있습니다.

**예제 코드 — [09_shared_and_weak_ptr.cpp](./examples/09_shared_and_weak_ptr.cpp)**

```cpp
#include <memory>
#include <print>
#include <string>

int main() {
    auto owner = std::make_shared<std::string>("navigation-map");
    std::weak_ptr<std::string> observer{owner};

    if (const auto locked = observer.lock()) {
        std::println("Active: {}", *locked);
    }

    owner.reset();
    std::println("Expired: {}", observer.expired());
}
```

**실행 결과**

```text
Active: navigation-map
Expired: true
```

`observer.lock()`이 성공하면 그 구간 동안 대상 객체의 수명이 유지됩니다. 내부에서 만든 임시 `shared_ptr`가 소멸한 뒤 `owner.reset()`을 호출하므로, 다음 `observer.expired()`는 `true`가 됩니다.

---

## 7.11. 외부 API 경계의 포인터와 길이

C 라이브러리나 장치 드라이버에서는 `(pointer, length)` 형태로 데이터를 전달하는 경우가 많습니다. 이런 API를 호출할 때는 **포인터와 길이를 함께 검증하는 계약**이 중요합니다.

다만 `data != nullptr`와 `length > 0`이라는 조건만으로 원본 버퍼가 실제로 그 길이만큼 유효한지는 알아낼 수 없습니다. **호출자와 API 사이에 올바른 길이 및 수명 계약이 있어야 합니다.**

**예제 코드 — [10_pointer_and_length_boundary.cpp](./examples/10_pointer_and_length_boundary.cpp)**

```cpp
#include <cstddef>
#include <cstdint>
#include <optional>
#include <print>
#include <span>

[[nodiscard]] std::optional<std::uint32_t> sum_bytes(
    const std::uint8_t* data, std::size_t length) {
    if (data == nullptr && length != 0) {
        return std::nullopt;
    }
    if (length == 0) {
        return std::uint32_t{0};
    }
    // 유효한 원본 버퍼와 길이라는 호출 계약이 충족된 경우에만 실행함.
    const std::span<const std::uint8_t> bytes{data, length};
    std::uint32_t total{0};
    for (const std::uint8_t value : bytes) {
        total += value;
    }
    return total;
}

int main() {
    const std::uint8_t bytes[]{1, 2, 3, 4};
    if (const auto total = sum_bytes(bytes, std::size(bytes))) {
        std::println("Checksum sum: {}", *total);
    }
    std::println("Invalid: {}", !sum_bytes(nullptr, 4));
}
```

**실행 결과**

```text
Checksum sum: 10
Invalid: true
```

외부 경계에서 null 포인터와 비어 있지 않은 길이의 조합을 거부한 다음, 내부 계산에서는 `std::span`으로 범위를 표현합니다. 합산 값은 `std::uint32_t`이고, 이 예제에서는 크기가 작은 고정 버퍼를 사용합니다.

**주의:** 알 수 없는 외부 주소와 길이를 임의로 `span`에 넣어도 안전해지는 것은 아닙니다. 실제 버퍼의 크기·유효성은 별도로 보장해야 합니다.

---

## 7.12. `std::reference_wrapper`와 선택적 참조

일반적인 참조(`T&`)는 선언 시 대상에 결합되어야 하며 다른 대상으로 바꾸는 참조 변수가 될 수 없습니다. 또한 `std::vector<int&>`처럼 참조 자체를 요소로 가지는 표준 컨테이너는 사용할 수 없습니다.

필요한 경우 `std::reference_wrapper<T>`를 이용해 **복사 가능한 참조형 래퍼**로 보관할 수 있습니다. 래퍼 역시 원본 객체를 소유하지 않습니다.

**예제 코드 — [11_reference_wrapper.cpp](./examples/11_reference_wrapper.cpp)**

```cpp
#include <functional>
#include <print>
#include <vector>

int main() {
    int front_rpm{1'000};
    int rear_rpm{1'200};

    std::vector<std::reference_wrapper<int>> motors{
        std::ref(front_rpm), std::ref(rear_rpm)
    };
    for (int& rpm : motors) {
        rpm += 100;
    }

    std::println("Front: {}", front_rpm);
    std::println("Rear: {}", rear_rpm);
}
```

**실행 결과**

```text
Front: 1100
Rear: 1300
```

`std::ref()`로 기존 모터 속도 변수의 참조를 저장했습니다. 반복문에서 수정한 값은 원본 `front_rpm`, `rear_rpm`에 반영됩니다. 실제 설계에서는 가능한 한 데이터를 하나의 컨테이너에서 직접 소유하는 편이 수명 관리가 단순할 수 있습니다.

`std::optional<T&>`는 C++23 표준에서 지원되지 않습니다. 반환값이 있을 수도 없는 경우에 참조를 표현하려면, 상황에 따라 `T*` 또는 `std::optional<std::reference_wrapper<T>>`를 사용할 수 있습니다.

**예제 코드 — [12_optional_reference.cpp](./examples/12_optional_reference.cpp)**

```cpp
#include <functional>
#include <optional>
#include <print>
#include <string>
#include <string_view>
#include <vector>

[[nodiscard]] std::optional<std::reference_wrapper<std::string>>
find_mutable(std::vector<std::string>& devices, std::string_view target) {
    for (auto& device : devices) {
        if (device == target) {
            return std::ref(device);
        }
    }
    return std::nullopt;
}

int main() {
    std::vector<std::string> devices{"camera", "lidar"};
    if (auto found = find_mutable(devices, "lidar")) {
        found->get() = "lidar-front";
    }
    std::println("Renamed: {}", devices.at(1));
}
```

**실행 결과**

```text
Renamed: lidar-front
```

검색된 요소를 `std::optional<std::reference_wrapper<std::string>>`로 반환합니다. 값이 있는 경우 `get()`을 통해 기존 문자열을 수정합니다.

반환한 참조 래퍼도 원본 벡터가 재할당되거나 요소가 제거되면 무효가 될 수 있습니다.

---

## 7.13. 포인터 연산과 범위 제한

C 스타일 배열에서 포인터를 증가시키면 다음 요소의 주소로 이동할 수 있습니다. 하지만 **포인터 산술은 유효한 배열 및 끝 바로 다음 위치 범위 안에서만** 수행해야 합니다. 범위를 벗어난 메모리에 접근하면 정의되지 않은 동작(Undefined Behavior, UB)이 발생할 수 있습니다.

```cpp
int values[]{10, 20, 30};
int* first = values;
int* second = first + 1;   // 두 번째 요소
int* end = first + 3;      // 끝 바로 다음 위치: 역참조 금지

// *second == 20
// *end 는 잘못된 접근
```

실무에서 대부분의 배열 처리는 포인터 산술을 직접 작성하기보다 **범위 기반 `for`**, `std::span`, `std::ranges` 및 표준 컨테이너를 사용하는 편이 가독성과 유지보수에 유리합니다.

외부 메모리 구조, 바이너리 프로토콜, 시스템 API를 다룰 때는 포인터 산술이 필요할 수 있으나, 그 경우에도 처리할 바이트 수와 정렬 요구사항을 명확히 확인해야 합니다.

---

## 7.14. 메모리 오류 탐지 및 디버깅

일부 포인터 오류는 컴파일만으로 찾을 수 없습니다. 코드가 컴파일되고 몇 번 정상 실행되더라도 잘못된 메모리 접근이 숨어 있을 수 있습니다.

**AddressSanitizer(ASan)**는 use-after-free, 범위 밖 접근 등 메모리 오류 탐지에 도움이 됩니다. **UndefinedBehaviorSanitizer(UBSan)**는 특정 정의되지 않은 동작을 감지합니다. 두 도구가 모든 오류를 증명하거나 보장하지는 않습니다.

**예제 코드 — [13_sanitizer_safe_example.cpp](./examples/13_sanitizer_safe_example.cpp)**

```cpp
#include <array>
#include <print>
#include <span>

[[nodiscard]] int first_or_default(std::span<const int> samples,
                                   int fallback) noexcept {
    return samples.empty() ? fallback : samples.front();
}

int main() {
    const std::array<int, 3> samples{10, 20, 30};
    const std::span<const int> empty{};
    std::println("First: {}", first_or_default(samples, -1));
    std::println("Empty: {}", first_or_default(empty, -1));
}
```

**실행 결과**

```text
First: 10
Empty: -1
```

비어 있는 `span`에 `front()`로 접근하지 않고, 별도의 기본값을 반환하는 간단한 안전성 예제입니다. 정상 실행 여부와 별개로 개발 과정에서 Sanitizer를 활성화하여 검사하는 습관이 중요합니다.

**GCC / Clang — 예제 검사**

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic \
  -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer \
  examples/13_sanitizer_safe_example.cpp -o sanitizer_safe
./sanitizer_safe
```

- **`-g`:** 디버깅 심볼 포함
- **`-O1`:** 디버깅과 실행 속도를 고려한 낮은 최적화 수준
- **`-fsanitize=address,undefined`:** ASan 및 UBSan 계측
- **`-fno-omit-frame-pointer`:** 오류 발생 위치 추적 지원

Sanitizer가 활성화된 바이너리는 일반 배포용 실행 파일과 분리해서 관리하는 편이 좋습니다. 사용 가능한 옵션과 런타임은 컴파일러·운영체제에 따라 달라질 수 있습니다.

### 검사 시 주의할 상황

| 실수 | 위험 | 예방 방향 |
|---|---|---|
| `nullptr` 역참조 | 잘못된 메모리 접근 | 사용 전 검사 및 계약 정리 |
| 지역 객체의 주소 반환 | 댕글링 포인터 | 값 반환 또는 명확한 소유권 관리 |
| `vector` 재할당 후 포인터 사용 | 무효한 요소 접근 | 변경 뒤 주소 재획득 |
| `delete` 누락·중복 | 누수·이중 해제 | RAII 및 스마트 포인터 |
| `span` 범위 초과 | 정의되지 않은 동작 | 길이 검증, 인덱스 검사 |
| `shared_ptr` 순환 소유 | 자원 정리 지연·누수 | 비소유 관계에 `weak_ptr` 사용 |

---

## 7.15. 실무에서의 매개변수·소유권 선택

API를 작성할 때 **필수 여부, 수정 여부, 소유권 이전 여부**를 순서대로 생각하면 필요한 타입을 고르기 쉽습니다.

| 필요 조건 | 우선 고려할 표현 | 예시 |
|---|---|---|
| 작은 값 전달 | `T` | `int rpm` |
| 필수 객체, 수정 없음 | `const T&` | `const Config& config` |
| 필수 객체, 수정 있음 | `T&` | `int& current_rpm` |
| 대상 부재 허용 | `const T*` 또는 `T*` | 선택적인 센서 읽기 |
| 연속된 데이터 읽기 | `std::span<const T>` | 측정 샘플 처리 |
| 연속된 데이터 수정 | `std::span<T>` | 버퍼에 결과 쓰기 |
| 문자열 읽기 | `std::string_view` | 장치 이름 비교 |
| 독점 소유권 이전 | `std::unique_ptr<T>` | 자원 소유 이전 |
| 공유 소유권 | `std::shared_ptr<T>` | 실제로 다중 소유자가 필요한 경우 |
| 공유 객체 관찰 | `std::weak_ptr<T>` | 등록된 작업의 대상 관찰 |

**적용 기준**

1. 소유하지 않는 값은 수명을 보장하는 상위 객체와의 관계를 명확히 합니다.
2. `new`/`delete`보다 지역 객체, 컨테이너, RAII를 먼저 고려합니다.
3. 주소 하나로 표현하기 어려운 버퍼는 `std::span`을 고려합니다.
4. 포인터가 null이 될 수 있는지, 참조 대상이 수정되는지 API 계약에 명시합니다.
5. 명확한 근거 없이 모든 객체에 `shared_ptr`를 적용하지 않습니다.

---

## 7.16. Coding Practice

각 문제의 `exercises/` 파일은 일부 로직이 비어 있는 **실습용 코드**입니다. 직접 구현한 뒤 컴파일하고, 필요할 때 `solutions/`에서 모범답안을 확인합니다.

### 7.16.1. Motor Limit — 참조를 통한 모터 속도 검증

**요구사항**

1. `try_set_rpm(int& current, int requested)` 함수 구현
2. 요청값이 0~3000이면 `current`를 갱신하고 `true` 반환
3. 범위를 벗어나면 `current`를 변경하지 않고 `false` 반환
4. 정상 입력과 실패 입력을 연속으로 실행하여 최종 상태 확인

**기대 출력**

```text
First: true, Second: false, RPM: 2500
```

- [연습문제 — 01_motor_limit.cpp](./exercises/01_motor_limit.cpp)
- [정답 코드 — 01_motor_limit.cpp](./solutions/01_motor_limit.cpp)

**확인할 사항:** 참조 매개변수의 변경은 원본에 적용되며, 실패 시 기존 상태가 유지되는지 확인합니다.

### 7.16.2. Sensor Average — `std::span`을 이용한 평균 계산

**요구사항**

1. `average(std::span<const int>)` 함수 구현
2. 입력 데이터가 비어 있으면 `std::nullopt` 반환
3. 값이 있다면 평균을 `double`로 계산해 반환
4. `std::array`를 복사하지 않고 함수로 전달
5. 정상 데이터와 빈 데이터를 각각 검사

**기대 출력**

```text
Average: 25.0
Empty: true
```

- [연습문제 — 02_sensor_average.cpp](./exercises/02_sensor_average.cpp)
- [정답 코드 — 02_sensor_average.cpp](./solutions/02_sensor_average.cpp)

**확인할 사항:** `std::span`은 원본 데이터를 소유하지 않음. 누적 계산은 정수 오버플로를 피하기 위해 `double`을 사용함.

### 7.16.3. Device Lookup — 검색 결과 포인터

**요구사항**

1. `find_device()`에서 장치 이름을 선형 검색
2. 일치하면 기존 문자열 요소의 주소 반환
3. 일치하지 않으면 `nullptr` 반환
4. 호출자는 포인터를 검사한 후 결과 출력

**기대 출력**

```text
Found: imu
Missing: true
```

- [연습문제 — 03_device_lookup.cpp](./exercises/03_device_lookup.cpp)
- [정답 코드 — 03_device_lookup.cpp](./solutions/03_device_lookup.cpp)

**확인할 사항:** 반환된 포인터의 수명은 원본 벡터 및 해당 요소의 유효성에 의존함.

### 7.16.4. Shared Observer — 소유권과 관찰

**요구사항**

1. 문자열 `sensor-hub`를 소유하는 `std::shared_ptr` 생성
2. 소유권을 추가하지 않는 `std::weak_ptr` 생성
3. `lock()`으로 대상에 접근하여 이름 출력
4. 마지막 소유자를 `reset()`으로 해제
5. `expired()`로 대상 소멸 여부 확인

**기대 출력**

```text
Active: sensor-hub
Expired: true
```

- [연습문제 — 04_shared_observer.cpp](./exercises/04_shared_observer.cpp)
- [정답 코드 — 04_shared_observer.cpp](./solutions/04_shared_observer.cpp)

**확인할 사항:** `lock()` 결과를 보관하는 지역 `shared_ptr`의 수명도 객체의 소멸 시점에 영향을 줌.

### 컴파일 및 실행

**GCC** — `Chapter-07/` 폴더에서 실행

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -O2 \
  solutions/01_motor_limit.cpp -o motor_limit
./motor_limit
```

**Clang** — 지원되는 C++ 표준 라이브러리를 사용하는 환경

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic -O2 \
  solutions/01_motor_limit.cpp -o motor_limit
./motor_limit
```

**MSVC** — Developer Command Prompt

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 solutions\01_motor_limit.cpp /Fe:motor_limit.exe
motor_limit.exe
```

MSVC의 C++23 지원 범위는 설치된 버전에 따라 다를 수 있으며, `/std:c++23`이 제공되는 환경에서는 해당 옵션을 사용할 수 있습니다.

---

## 7.17. Quiz & Summary

### Quiz

1. `int* pointer`와 `int& reference`의 가장 큰 차이는 무엇인가요?
2. 포인터가 `nullptr`이 아니면 언제나 역참조해도 안전한가요?
3. `const int* p`와 `int* const p`는 어떻게 다른가요?
4. `std::vector`의 `push_back()` 이후 기존 포인터가 무효화되는 대표적인 조건은 무엇인가요?
5. `std::span<const int>`은 원본 배열을 소유하나요?
6. `std::unique_ptr<T>`를 다른 함수로 소유권 이전할 때 어떤 표현을 사용하나요?
7. `std::shared_ptr`와 `std::weak_ptr`의 소유권 차이는 무엇인가요?
8. `std::optional<T&>`를 C++23에서 직접 사용할 수 있나요?
9. 어떤 이유로 `std::span`을 사용해도 외부 버퍼가 자동으로 안전해지지는 않나요?

<details>
<summary>정답 확인</summary>

1. 포인터는 null을 표현하고 대상을 바꿀 수 있지만, 참조는 유효한 대상에 결합되며 일반적으로 재결합할 수 없음.
2. 아니요. 원본 객체가 파괴된 댕글링 포인터는 null이 아닐 수 있음.
3. 전자는 해당 포인터를 통한 값 수정이 불가능하고, 후자는 다른 대상으로 포인터를 변경할 수 없음.
4. `capacity()`를 초과하는 삽입 등으로 내부 저장소가 재할당된 경우.
5. 아니요. 연속된 데이터의 비소유 뷰이며 원본 수명에 의존함.
6. `std::move()`를 사용해 이동을 허용하는 표현식으로 전달함.
7. `shared_ptr`는 공유 소유권을 추가하며 `weak_ptr`는 소유권 없이 관찰함.
8. 아니요. `T*` 또는 `std::optional<std::reference_wrapper<T>>` 등을 고려할 수 있음.
9. 원본 버퍼의 유효한 범위·수명과 전달된 길이를 `span`이 독자적으로 확인할 수 없기 때문.

</details>

### Summary

- **포인터(`T*`):** 객체 주소를 보관하며 null 상태와 대상 변경을 표현할 수 있음
- **참조(`T&`, `const T&`):** 기존 객체에 결합해 읽기 또는 수정을 수행
- **`const` 정확성:** 읽기 전용 접근과 포인터 대상 변경 가능성을 구분
- **객체 수명:** 포인터·참조·뷰를 사용하는 동안 원본의 유효성 유지
- **`std::span`:** 연속 데이터 범위의 비소유 표현, 사용 전 크기·수명 검증 필요
- **RAII:** 객체 수명에 맞춰 자원을 정리하도록 설계
- **`std::unique_ptr`:** 명확한 독점 소유권 관리
- **`std::shared_ptr` / `std::weak_ptr`:** 공유 소유권과 비소유 관찰 구분
- **참조 래퍼:** 참조를 일반 객체처럼 보관하되 원본 수명 보장 필요
- **Sanitizer:** 컴파일러 경고만으로 찾기 어려운 메모리 오류 탐지 보조

### References

- [cppreference — Pointers](https://en.cppreference.com/w/cpp/language/pointer)
- [cppreference — References](https://en.cppreference.com/w/cpp/language/reference)
- [cppreference — Object lifetime](https://en.cppreference.com/w/cpp/language/lifetime)
- [cppreference — `std::span`](https://en.cppreference.com/w/cpp/container/span)
- [cppreference — Smart pointers](https://en.cppreference.com/w/cpp/memory)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Clang AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)

---

[← C++ 목차](../README.md) · [Chapter 06 — Arrays & Strings](../Chapter-06/)

