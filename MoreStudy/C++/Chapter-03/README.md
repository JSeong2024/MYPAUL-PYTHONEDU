# Chapter 03. Operators & Conditions

산술·비교·논리 연산자와 조건문을 활용하여 계산 결과를 판단하고 프로그램의 실행 흐름을 제어합니다. 정상 입력과 잘못된 입력을 구분하고, 경계값과 장치 상태 비트를 검사하는 방법을 학습합니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서 도입된 조건문 초기화 구문도 함께 다룹니다.

<details>
<summary>선행 학습</summary>

- [Chapter 01. Getting Started with C++](../Chapter-01/) — `main()`, 표준 입출력, 컴파일과 실행
- [Chapter 02. Variables & Data Types](../Chapter-02/) — 변수, 정수·실수·`bool`, `enum class`, 형변환

</details>

## Contents

| Section | Topic |
|:---:|---|
| [3.1](#section-3-1) | Arithmetic & Assignment — 산술 연산과 대입 |
| [3.2](#section-3-2) | Comparison — 비교 연산 |
| [3.3](#section-3-3) | Logical Operators — 논리 연산과 단락 평가 |
| [3.4](#section-3-4) | `if`, `else if`, `else` — 조건 분기 |
| [3.5](#section-3-5) | Guard Clauses — 입력 검증과 빠른 종료 |
| [3.6](#section-3-6) | `switch` & `enum class` — 값에 따른 분기 |
| [3.7](#section-3-7) | Conditional Operator & `if` Initializer — 간결한 조건 표현 |
| [3.8](#section-3-8) | Bitwise Operators — 비트 연산과 상태 플래그 |
| [3.9](#section-3-9) | Precedence & Boundary Cases — 우선순위와 경계값 |
| [3.10](#section-3-10) | Coding Practice |
| [3.11](#section-3-11) | Mini Project — Device Health Report |
| [3.12](#section-3-12) | Quiz & Summary |

## Getting Started

아래 명령어는 **`Chapter-03/` 디렉터리**에서 실행하는 경우를 기준으로 합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_arithmetic_and_assignment.cpp -o arithmetic
./arithmetic
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_arithmetic_and_assignment.cpp -o arithmetic
./arithmetic
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_arithmetic_and_assignment.cpp /Fe:arithmetic.exe
arithmetic.exe
```

Windows PowerShell에서는 생성된 파일을 `./arithmetic` 대신 `.\arithmetic.exe`로 실행할 수 있습니다. 개발 환경 설정은 [Chapter 01](../Chapter-01/)에서 확인할 수 있습니다.

**학습 목표**

1. 산술·비교·논리 연산자의 역할과 결과를 설명할 수 있습니다.
2. `if`, `else if`, `else`, `switch`로 실행 경로를 구분할 수 있습니다.
3. 단락 평가와 가드 절로 잘못된 연산이나 입력을 처리할 수 있습니다.
4. 비트 연산으로 상태값을 판정할 수 있습니다.
5. 정상값·경계값·잘못된 값에 따른 출력을 검증할 수 있습니다.

---

<a id="section-3-1"></a>
## 3.1. Arithmetic & Assignment — 산술 연산과 대입

**연산자(Operator)** 는 값에 계산이나 비교 등의 동작을 적용하는 기호입니다. 연산 대상인 값 또는 표현식은 **피연산자(Operand)** 라고 합니다. 예를 들어 `7 + 3`에서 `+`는 연산자이고, `7`과 `3`은 피연산자입니다.

| 연산자 | 의미 | 결과 예시 |
|---|---|---|
| `+` | 덧셈 | `7 + 3` → `10` |
| `-` | 뺄셈 | `7 - 3` → `4` |
| `*` | 곱셈 | `7 * 3` → `21` |
| `/` | 나눗셈 | `7 / 3` → `2` (정수끼리 계산) |
| `%` | 나머지 | `7 % 3` → `1` |
| `=` | 대입 | `count = 5` |
| `+=`, `-=`, `*=`, `/=`, `%=` | 복합 대입 | `count += 2`는 `count = count + 2`와 같은 계산 |
| `++`, `--` | 1 증가·감소 | `++count`, `--count` |

정수끼리 `/`로 나누면 정수 결과를 얻으며, 소수 부분은 **0 방향으로 버립니다**. `-7 / 3`의 결과는 `-2`입니다. `%`는 정수형에만 사용할 수 있으며, 정수 나눗셈 후 나머지를 구할 때 사용합니다.

다음 예제에서는 물품 17개를 박스당 5개씩 포장합니다. 가득 찬 박스 수는 나눗셈으로, 남는 물품 수는 나머지 연산으로 계산합니다.

**예제 코드 — [01_arithmetic_and_assignment.cpp](./examples/01_arithmetic_and_assignment.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int item_count{17};
    constexpr int items_per_box{5};
    const int full_boxes{item_count / items_per_box};
    const int remaining{item_count % items_per_box};

    int packed_items{0};
    packed_items += full_boxes * items_per_box;

    std::cout << "Full boxes: " << full_boxes << '\n';
    std::cout << "Remaining items: " << remaining << '\n';
    std::cout << "Packed items: " << packed_items << '\n';
}
```

**실행 결과**

```text
Full boxes: 3
Remaining items: 2
Packed items: 15
```

- `item_count / items_per_box`: 가득 채울 수 있는 박스의 개수를 구합니다.
- `item_count % items_per_box`: 가득 채운 박스에 넣지 못한 물품의 개수를 구합니다.
- `packed_items += ...`: 기존 값에 계산 결과를 더해 저장합니다. `packed_items`는 변경 가능한 변수입니다.

**주의:** 정수의 `0` 나눗셈은 정의되지 않은 동작이므로 나누기 전에 제수가 0인지 확인해야 합니다. 부호 있는 정수의 표현 범위를 넘어가는 연산도 올바른 결과를 보장하지 않습니다. 실수 몫이 필요하면 Chapter 02에서 학습한 `static_cast<double>()` 등으로 자료형을 적절히 변환합니다.

---

<a id="section-3-2"></a>
## 3.2. Comparison — 비교 연산

**비교 연산자(Comparison Operator)** 는 두 값을 비교하여 `bool` 값인 `true` 또는 `false`를 반환합니다.

| 연산자 | 의미 | 예시 (`a=5`, `b=7`) |
|---|---|---|
| `==` | 같다 | `a == b` → `false` |
| `!=` | 다르다 | `a != b` → `true` |
| `<` | 작다 | `a < b` → `true` |
| `<=` | 작거나 같다 | `a <= 5` → `true` |
| `>` | 크다 | `b > a` → `true` |
| `>=` | 크거나 같다 | `b >= 7` → `true` |

`=`는 오른쪽 값을 변수에 **대입**하는 연산자이고, `==`는 두 값을 **비교**하는 연산자입니다. 두 기호를 혼동하지 않아야 합니다. 수치의 경계값을 포함하려면 `<`와 `<=` 중 어떤 연산자가 맞는지 확인해야 합니다.

아래 예제에서는 배터리 잔량이 정확히 20%인 경우를 검사합니다.

**예제 코드 — [02_comparison_expressions.cpp](./examples/02_comparison_expressions.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int battery_percent{20};
    constexpr int warning_limit{20};

    std::cout << std::boolalpha;
    std::cout << "At warning limit: " << (battery_percent == warning_limit) << '\n';
    std::cout << "Low battery: " << (battery_percent <= warning_limit) << '\n';
    std::cout << "Above limit: " << (battery_percent > warning_limit) << '\n';
}
```

**실행 결과**

```text
At warning limit: true
Low battery: true
Above limit: false
```

`battery_percent <= warning_limit`는 20보다 **작은 경우뿐 아니라 정확히 20인 경우에도** `true`입니다. `std::boolalpha`는 Chapter 02에서 학습한 출력 설정으로, 논리값을 `1`·`0` 대신 `true`·`false`로 표시합니다.

부동소수점 실수의 `==` 비교는 계산 과정에서 생긴 표현 오차를 고려해야 합니다. 수치 허용 오차를 다루는 기본 개념은 Chapter 02의 부동소수점 항목을 참고합니다.

---

<a id="section-3-3"></a>
## 3.3. Logical Operators — 논리 연산과 단락 평가

**논리 연산자(Logical Operator)** 는 하나 이상의 조건을 결합하거나 참·거짓을 반전합니다.

| 연산자 | 의미 | 예시 |
|---|---|---|
| `&&` | AND — 두 조건이 모두 참 | `true && false` → `false` |
| `||` | OR — 하나 이상 참 | `true || false` → `true` |
| `!` | NOT — 조건 반전 | `!true` → `false` |

`&&`와 `||`는 왼쪽 조건을 먼저 평가하며, 결과가 이미 결정되면 오른쪽 조건을 평가하지 않습니다. 이 성질을 **단락 평가(Short-circuit Evaluation)** 라고 합니다.

- `A && B`: `A`가 `false`이면 `B`는 평가되지 않습니다.
- `A || B`: `A`가 `true`이면 `B`는 평가되지 않습니다.

예를 들어 평균을 계산하기 전에 표본 개수가 0인지 검사하면 0으로 나누는 연산을 막을 수 있습니다.

**예제 코드 — [03_logical_short_circuit.cpp](./examples/03_logical_short_circuit.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int samples{0};
    constexpr int total{150};
    constexpr bool connected{true};
    constexpr double temperature_c{78.5};

    const bool high_average = (samples != 0) && (total / samples > 30);
    const bool alarm = connected && (temperature_c >= 75.0);

    std::cout << std::boolalpha;
    std::cout << "High average: " << high_average << '\n';
    std::cout << "Alarm: " << alarm << '\n';
}
```

**실행 결과**

```text
High average: false
Alarm: true
```

`samples != 0`이 `false`이므로 그 뒤의 `total / samples`는 **실행되지 않습니다**. 조건을 뒤집어 `total / samples > 30 && samples != 0`으로 작성하면 안전하지 않습니다.

**주의:** `&`와 `|`는 각각 비트 단위 연산이고, `&&`와 `||`는 논리 연산입니다. 비트 연산은 3.8에서 별도로 다룹니다. 부작용이 있는 연산을 논리식 안에 무리하게 넣기보다는 조건의 의미를 명확하게 작성하는 것이 좋습니다.

---

<a id="section-3-4"></a>
## 3.4. `if`, `else if`, `else` — 조건 분기

**조건문(Conditional Statement)** 은 조건의 결과에 따라 서로 다른 코드를 실행하는 문장입니다. `if`의 조건이 참이면 해당 블록을 실행하고, 거짓이면 `else if` 또는 `else`를 확인합니다.

```cpp
if (조건 A) {
    // A가 참일 때 실행
} else if (조건 B) {
    // A가 거짓이고 B가 참일 때 실행
} else {
    // 앞선 조건이 모두 거짓일 때 실행
}
```

`if`·`else if`·`else`를 하나의 체인으로 구성하면 **처음으로 참이 된 분기 하나만 실행**합니다. 거리는 정수 센티미터 값이며, 다음 규칙을 적용합니다.

| 거리 | 처리 결과 |
|---|---|
| 0~29cm | `STOP` |
| 30~100cm | `SLOW DOWN` |
| 101~400cm | `CLEAR` |
| 음수 또는 400 초과 | `INVALID` |

이 범위에서 29, 30, 100, 101은 판정 결과가 달라지는 경계값입니다.

**예제 코드 — [04_if_else_branches.cpp](./examples/04_if_else_branches.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int distance_cm{30};

    if (distance_cm < 0 || distance_cm > 400) {
        std::cout << "INVALID\n";
    } else if (distance_cm < 30) {
        std::cout << "STOP\n";
    } else if (distance_cm <= 100) {
        std::cout << "SLOW DOWN\n";
    } else {
        std::cout << "CLEAR\n";
    }
}
```

**실행 결과**

```text
SLOW DOWN
```

예제의 거리는 30cm이므로 `distance_cm < 30`은 거짓이고, `distance_cm <= 100`은 참이어서 `SLOW DOWN`을 출력합니다. `else if` 분기의 순서는 결과에 직접 영향을 주므로 범위를 중복 없이 구성해야 합니다.

`if` 문마다 별개의 `{}` 블록을 사용하면, 독립적인 여러 조건을 검사하는 경우와 하나의 결과만 선택해야 하는 경우를 구분하기 쉬워집니다.

---

<a id="section-3-5"></a>
## 3.5. Guard Clauses — 입력 검증과 빠른 종료

**가드 절(Guard Clause)** 은 유효하지 않은 입력이나 처리할 수 없는 상태를 앞에서 검사하고, 더 이상의 처리를 진행하지 않도록 종료하는 방식입니다. 조건을 여러 단계로 중첩하지 않고 정상 흐름을 읽기 쉽게 만들 수 있습니다.

```text
입력 시도 → 입력 실패? → 오류 출력·종료
         → 범위 이탈? → 오류 출력·종료
         → 정상 처리
```

Chapter 01에서 학습한 `std::cin`과 `std::cerr`를 함께 사용할 수 있습니다. `std::cin >> 변수`는 입력에 실패하면 거짓으로 판정할 수 있으며, 실패 시 일반적인 범위 검사를 진행하지 않도록 해야 합니다.

**예제 코드 — [05_guard_clauses.cpp](./examples/05_guard_clauses.cpp)**

```cpp
#include <iostream>

int main() {
    int battery_percent{};
    std::cout << "Battery (0-100): " << std::flush;
    if (!(std::cin >> battery_percent)) {
        std::cerr << "Error: enter a battery percentage.\n";
        return 1;
    }
    if (battery_percent < 0 || battery_percent > 100) {
        std::cerr << "Error: battery percentage must be 0-100.\n";
        return 1;
    }

    std::cout << "Accepted: " << battery_percent << "%\n";
}
```

**실행 결과**

```text
Battery (0-100): Accepted: 35%
```

위 실행 결과는 `35`를 입력한 경우입니다. 입력한 글자는 터미널에서 표시될 수 있지만, 프로그램이 직접 출력한 내용만 결과에 적었습니다.

- `if (!(std::cin >> battery_percent))`: 정수 읽기에 실패하면 오류를 출력하고 종료합니다.
- `battery_percent < 0 || battery_percent > 100`: 정수라도 허용 범위가 아니면 오류로 처리합니다.
- `std::cerr`: 오류 메시지를 표준 오류 스트림으로 출력합니다.
- `return 1;`: `main()`에서 비정상 종료 상태를 반환합니다.

**입력 처리 범위:** 해당 예제는 하나의 숫자를 입력받는 상황을 가정합니다. `std::cin >> int`는 `12abc`의 앞부분인 `12`를 읽고 나머지 문자를 남길 수 있으므로, **문자열 전체의 엄격한 검증을 보장하지 않습니다**. 문자열을 완전히 파싱하는 방법은 후속 문자열·입력 처리 학습에서 다룹니다.

---

<a id="section-3-6"></a>
## 3.6. `switch` & `enum class` — 값에 따른 분기

**`switch` 문(Switch Statement)** 은 정수나 열거형 등의 특정 값을 기준으로 여러 처리 경로 중 하나를 선택합니다. 하나의 값이 여러 고정 상태 중 어디에 해당하는지 판단할 때 유용합니다.

Chapter 02에서 학습한 `enum class`는 `DeviceMode::active`와 같이 상태를 이름으로 구분합니다. 이처럼 가능한 상태가 명확하다면 `switch`와 함께 사용할 수 있습니다.

**예제 코드 — [06_switch_and_enum.cpp](./examples/06_switch_and_enum.cpp)**

```cpp
#include <iostream>

enum class DeviceMode { off, standby, active };

int main() {
    constexpr DeviceMode mode{DeviceMode::standby};

    switch (mode) {
        case DeviceMode::off:
            std::cout << "Power off\n";
            break;
        case DeviceMode::standby:
            std::cout << "Waiting for input\n";
            break;
        case DeviceMode::active:
            std::cout << "Device active\n";
            break;
    }
}
```

**실행 결과**

```text
Waiting for input
```

| 구문 | 의미 |
|---|---|
| `switch (mode)` | `mode` 값에 해당하는 `case` 선택 |
| `case DeviceMode::standby:` | 해당 열거형 값의 처리 시작 |
| `break;` | 현재 `switch` 문을 종료하여 다음 `case` 실행 방지 |
| `default:` | 어떤 `case`에도 해당하지 않을 때 처리하는 선택적 분기 |

`case` 뒤에 `break`가 없으면 **다음 `case`의 코드까지 계속 실행될 수 있습니다(Fallthrough)**. C++17에서는 의도한 경우 `[[fallthrough]];`로 표시할 수 있습니다. 현재 예제는 모든 열거형 항목을 처리하므로 별도의 `default`를 사용하지 않았습니다.

`switch`는 `temperature_c > 75.0`처럼 실수의 범위를 직접 비교하는 데 사용할 수 없습니다. 연속적인 구간 판정은 `if`·`else if`가 더 적절합니다.

---

<a id="section-3-7"></a>
## 3.7. Conditional Operator & `if` Initializer — 간결한 조건 표현

**조건 연산자(Conditional Operator)** `?:`는 조건에 따라 두 표현식 중 하나의 값을 선택합니다. `if`가 여러 문장을 실행할 수 있는 문장이라면, `?:`는 하나의 값을 선택하는 표현식입니다.

```cpp
조건 ? 참일 때 값 : 거짓일 때 값
```

또한 **C++17** 부터 `if (초기화; 조건)`처럼 `if` 안에서 초기화할 수 있습니다. 이때 초기화한 이름의 사용 범위는 해당 `if` 및 연결된 `else` 내부로 제한됩니다. 이를 **`if` 초기화 구문(Init-statement)** 이라고 합니다.

**예제 코드 — [07_if_initializer_and_ternary.cpp](./examples/07_if_initializer_and_ternary.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int response_ms{180};
    constexpr int limit_ms{200};

    std::cout << "Response: "
              << (response_ms > limit_ms ? "SLOW" : "NORMAL") << '\n';

    if (const int retries_left{2}; retries_left > 0) {
        std::cout << "Retries available: " << retries_left << '\n';
    } else {
        std::cout << "No retries left\n";
    }
}
```

**실행 결과**

```text
Response: NORMAL
Retries available: 2
```

- `response_ms > limit_ms ? "SLOW" : "NORMAL"`: 조건이 거짓이므로 `NORMAL`을 선택합니다.
- `if (const int retries_left{2}; retries_left > 0)`: 초기화와 조건 검사를 한 문장에 작성합니다.
- `retries_left`: 해당 `if` 블록과 `else` 블록에서는 사용할 수 있지만 `if` 문 밖에서는 사용할 수 없습니다.

조건 연산자 `?:`를 여러 번 중첩하면 읽기 어려우므로, 다수의 판단 기준이나 복잡한 작업은 `if` 문으로 표현하는 것이 적절합니다.

---

<a id="section-3-8"></a>
## 3.8. Bitwise Operators — 비트 연산과 상태 플래그

**비트 연산자(Bitwise Operator)** 는 정수의 이진수 표현에서 각 비트에 연산을 적용합니다. Chapter 02의 비트(Bit)·바이트(Byte) 설명을 참고하면 이해하기 쉽습니다. **플래그(Flag)** 는 개별 비트에 특정 상태의 의미를 부여한 값입니다.

| 연산자 | 의미 | 간단한 예시 |
|---|---|---|
| `&` | 비트 AND — 두 비트가 모두 1일 때 1 | `0101 & 0011` → `0001` |
| `|` | 비트 OR — 하나 이상 1일 때 1 | `0101 | 0011` → `0111` |
| `^` | 비트 XOR — 두 비트가 다를 때 1 | `0101 ^ 0011` → `0110` |
| `~` | 비트 NOT — 각 비트 반전 | 정수 타입의 전체 비트 폭에 적용 |
| `<<` | 비트 왼쪽 이동 | `1U << 2` → `4` |
| `>>` | 비트 오른쪽 이동 | `4U >> 1` → `2` |

`|=`와 `&=`처럼 비트 연산에도 복합 대입을 사용할 수 있습니다. 예를 들어 `flags |= sensor_ready`는 해당 플래그를 켜고, `flags &= ~fault`는 해당 플래그를 끕니다.

| 비트 위치 | 이진값 | 의미 |
|---|---|---|
| 0번 | `001` (1) | 전원 켜짐 |
| 1번 | `010` (2) | 센서 준비 |
| 2번 | `100` (4) | 오류 발생 |

`std::uint32_t`는 Chapter 02에서 설명한 `<cstdint>` 헤더의 고정 폭 부호 없는 정수 타입입니다. 해당 Chapter에서는 새로운 표준 라이브러리 헤더를 추가하지 않고, 앞에서 배운 `<iostream>`과 `<cstdint>`를 사용합니다.

**예제 코드 — [08_bitwise_status_flags.cpp](./examples/08_bitwise_status_flags.cpp)**

```cpp
#include <cstdint>
#include <iostream>

int main() {
    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};

    std::uint32_t flags{power_on};
    flags |= sensor_ready;
    const bool ready{(flags & (power_on | sensor_ready)) ==
                     (power_on | sensor_ready)};
    flags |= fault;
    flags &= ~fault;

    std::cout << std::boolalpha;
    std::cout << "Ready: " << ready << '\n';
    std::cout << "Flags: " << flags << '\n';
    std::cout << "Fault set: " << ((flags & fault) != 0U) << '\n';
}
```

**실행 결과**

```text
Ready: true
Flags: 3
Fault set: false
```

처음에는 전원 플래그만 켜져 있지만 `flags |= sensor_ready`로 센서 비트를 추가합니다. `flags |= fault`로 오류 비트를 켰다가 `flags &= ~fault`로 지우므로 최종 비트값은 `011`(십진수 3)입니다.

특정 비트가 켜져 있는지는 `(flags & fault) != 0U`처럼 검사합니다. **논리 연산 `&&`와 비트 연산 `&`는 역할이 다르며 서로 대체할 수 없습니다.** 비트 시프트의 양과 결과가 정수 타입의 표현 범위를 벗어나지 않도록 주의해야 합니다.

---

<a id="section-3-9"></a>
## 3.9. Precedence & Boundary Cases — 우선순위와 경계값

**연산자 우선순위(Operator Precedence)** 는 여러 연산자가 하나의 표현식에 있을 때 어떤 부분이 먼저 묶여 해석되는지를 결정합니다. 예를 들어 `2 + 3 * 4`는 `2 + (3 * 4)`로 해석되어 `14`가 됩니다.

| 연산 유형 | 일반적인 상대 우선순위(높음 → 낮음) |
|---|---|
| 곱셈·나눗셈·나머지 | `*`, `/`, `%` |
| 덧셈·뺄셈 | `+`, `-` |
| 비교 | `<`, `<=`, `>`, `>=`, `==`, `!=` (세부 순서 존재) |
| 논리 AND | `&&` |
| 논리 OR | `||` |
| 대입 | `=`, `+=` 등 |

이 표는 주요 연산만 단순화한 것입니다. **괄호 `()`를 사용해 조건을 묶으면** 우선순위 표를 외우지 않아도 의도를 분명하게 전달할 수 있습니다.

**경계값(Boundary Value)** 은 조건 결과가 달라지는 기준점이나 그 바로 앞뒤의 값입니다. 예를 들어 배터리 잔량이 20% 이하일 때 경고한다면 19·20·21을 각각 확인해야 합니다.

**예제 코드 — [09_boundaries_and_parentheses.cpp](./examples/09_boundaries_and_parentheses.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int battery_percent{20};
    constexpr bool connected{true};
    constexpr double temperature_c{78.0};

    const bool valid_battery{battery_percent >= 0 && battery_percent <= 100};
    const bool warning{connected &&
                       (battery_percent <= 20 || temperature_c >= 75.0)};

    std::cout << std::boolalpha;
    std::cout << "Valid battery: " << valid_battery << '\n';
    std::cout << "Warning: " << warning << '\n';
}
```

**실행 결과**

```text
Valid battery: true
Warning: true
```

예제는 전원이 연결되어 있고, 배터리가 20%이거나 온도가 75°C 이상이면 경고합니다. 괄호 없이 `connected && battery_percent <= 20 || temperature_c >= 75.0`처럼 작성하면 온도가 높은 경우 `connected`의 참·거짓과 무관하게 경고가 발생할 수 있습니다. **조건을 어떤 묶음으로 판단할지** 명시하는 것이 중요합니다.

다음과 같은 경계값을 확인하면 조건식의 오류를 조기에 찾을 수 있습니다.

| 조건 | 검사할 값 |
|---|---|
| `distance_cm < 30` | 29, 30 |
| `battery_percent <= 20` | 19, 20, 21 |
| `temperature_c >= 75.0` | 74.9, 75.0, 75.1 |
| `flags` 허용 범위 0~7 | -1, 0, 7, 8 |

---

<a id="section-3-10"></a>
## 3.10. Coding Practice

`exercises/`에는 직접 작성할 시작 코드가, `solutions/`에는 모범답안이 있습니다. 각 문제는 정상 입력·경계값·잘못된 입력에 대한 기대 결과를 제시합니다.

| No. | Practice | Exercise | Solution |
|:---:|---|---|---|
| 01 | Box Counter | [문제 코드](./exercises/01_box_counter.cpp) | [정답 코드](./solutions/01_box_counter.cpp) |
| 02 | Distance Alert | [문제 코드](./exercises/02_distance_alert.cpp) | [정답 코드](./solutions/02_distance_alert.cpp) |
| 03 | Mode Selector | [문제 코드](./exercises/03_mode_selector.cpp) | [정답 코드](./solutions/03_mode_selector.cpp) |
| 04 | Status Flags | [문제 코드](./exercises/04_status_flags.cpp) | [정답 코드](./solutions/04_status_flags.cpp) |

### Exercise 01 — Box Counter

물품 수와 박스당 수용량을 정수로 입력받고, 가득 찬 박스 수와 남는 물품 수를 계산합니다.

**구현 조건**

- `items`는 0 이상, `capacity`는 1 이상이어야 합니다.
- 나눗셈(`/`)과 나머지 연산(`%`)을 각각 사용합니다.
- 수용량이 0일 때 나누기를 실행하지 않습니다.
- 숫자 읽기에 실패하거나 범위를 벗어나면 `std::cerr`에 `Error: invalid box input.`을 출력하고 종료 코드 1을 반환합니다.

**입력 및 출력 예시**

```text
Items: 17
Capacity: 5
Full boxes: 3
Remaining items: 2
```

**확인할 경계값:** `items=0`, `capacity=1`, `capacity=0`.

### Exercise 02 — Distance Alert

정수로 입력받은 거리(cm)에 따라 상태를 분류합니다.

| 거리 | 출력 |
|---|---|
| 0~29 | `STOP` |
| 30~100 | `SLOW DOWN` |
| 101~400 | `CLEAR` |
| 그 외 / 숫자 읽기 실패 | 표준 오류에 `Error: distance must be 0-400.` 및 종료 코드 1 |

**입력 및 출력 예시**

```text
Distance (0-400 cm): 30
SLOW DOWN
```

**확인할 경계값:** 0, 29, 30, 100, 101, 400, -1, 401.

### Exercise 03 — Mode Selector

정수 모드 번호를 `enum class DeviceMode`로 변환하여 `switch`로 상태를 출력합니다. `static_cast<DeviceMode>(selected)`는 Chapter 02에서 학습한 명시적 변환을 이용합니다.

| 입력 | 출력 |
|---|---|
| `0` | `OFF` |
| `1` | `STANDBY` |
| `2` | `ACTIVE` |
| 그 외 / 숫자 읽기 실패 | 표준 오류에 `Error: mode must be 0-2.` 및 종료 코드 1 |

**입력 및 출력 예시**

```text
Mode (0-2): 2
ACTIVE
```

### Exercise 04 — Status Flags

세 가지 상태 비트가 포함된 십진 정수(`0~7`)를 입력받아 장치 상태를 출력합니다.

- 비트 0(`1`): 전원 ON
- 비트 1(`2`): 센서 준비
- 비트 2(`4`): 오류
- 오류 플래그가 있으면 `FAULT`를 가장 먼저 적용합니다.
- 오류가 없고 전원·센서 비트가 모두 켜져 있으면 `READY`, 나머지는 `NOT READY`입니다.
- 숫자 읽기에 실패하거나 0~7 범위를 벗어나면 `Error: flags must be 0-7.`을 표준 오류로 출력하고 종료 코드 1을 반환합니다.

**입력 및 출력 예시**

```text
Flags (0-7): 3
READY
```

**추가 확인:** `0` → `NOT READY`, `4` → `FAULT`, `7` → `FAULT`.

### 컴파일 및 검증

`Chapter-03/` 디렉터리에서 아래 명령어를 실행합니다.

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/02_distance_alert.cpp -o distance_alert
./distance_alert
```

자동 테스트는 Python 표준 라이브러리를 사용하여 C++ 프로그램을 컴파일하고, 입력과 출력·종료 코드를 비교합니다. 별도의 Python 패키지는 필요하지 않습니다.

```bash
python3 tests/check.py
python3 tests/check.py --mode student --only exercise-04
```

**첫 번째 명령어**는 예제와 모범답안을 확인하는 용도입니다. **두 번째 명령어**는 직접 수정한 Exercise 04를 검사합니다. 아직 코드를 작성하지 않은 초기 상태에는 FAIL이 나오는 것이 정상입니다. Test Runner는 소스 코드를 C++20으로 컴파일한 뒤, 여러 입력값에 대한 출력 결과가 일치하는지 자동으로 검증합니다.

컴파일러가 Clang이라면 `--compiler clang++` 옵션을 추가할 수 있습니다. Windows 환경에서는 `python3` 대신 `python` 또는 `py` 명령어를 사용할 수도 있습니다.

---

<a id="section-3-11"></a>
## 3.11. Mini Project — Device Health Report

### 목표

배터리 잔량, 온도, 세 가지 상태 플래그를 입력받아 장치 정보와 최종 판정 결과를 표시하는 콘솔 프로그램을 작성합니다. 산술·비교·논리·비트 연산과 조건 분기를 종합적으로 사용합니다.

**프로젝트 파일**

- [device_health_report.cpp](./project/device_health_report.cpp) — 시작 코드
- [device_health_report.cpp](./solutions/device_health_report.cpp) — 모범답안
- [check.py](./tests/check.py) — 자동 검증

**입력 조건**

| 입력 | 자료형 | 허용 범위 |
|---|---|---|
| 배터리 잔량(%) | `int` | 0~100 |
| 온도(°C) | `double` | -40~125 |
| 상태 플래그 | 0~7 범위의 정수 입력 후 부호 없는 정수로 변환 | 0~7 |

상태 플래그의 의미는 Exercise 04와 같습니다. `001`은 전원 ON, `010`은 센서 준비, `100`은 오류를 나타냅니다. 세 비트가 모두 켜진 값은 십진수 `7`입니다.

**최종 상태 판정 우선순위**

| 우선순위 | 조건 | 결과 |
|:---:|---|---|
| 1 | 오류 비트가 켜짐 | `FAULT` |
| 2 | 전원 비트가 꺼짐 | `POWER OFF` |
| 3 | 센서 준비 비트가 꺼짐 | `SENSOR NOT READY` |
| 4 | 온도가 75°C 이상 | `OVERHEAT` |
| 5 | 배터리 잔량이 20% 이하 | `LOW BATTERY` |
| 6 | 위 조건에 해당하지 않음 | `READY` |

**실행 예시**

```text
Battery (0-100): 18
Temperature (-40 to 125 C): 78
Flags (0-7): 3

--- Device Health ---
Battery: 18%
Temperature: 78 C
Power: ON
Sensor: READY
Fault: NO
Status: OVERHEAT
```

배터리 잔량이 20% 이하이지만, 온도가 75°C 이상이므로 **우선순위가 더 높은 `OVERHEAT`** 가 출력됩니다.

### 완료 기준

- **입력 처리:** 배터리·온도·상태 플래그를 순서대로 읽고 지정된 범위를 확인해야 합니다.
- **비트 판정:** 전원·센서·오류 플래그를 각각 정확히 검사해야 합니다.
- **상태 우선순위:** 여러 경고 조건이 동시에 참일 때는 명세된 우선순위의 결과를 하나만 출력해야 합니다.
- **출력 정합성:** 입력값이 달라지면 다음 실행에서 해당 값과 판정 결과가 정확하게 반영되어야 합니다.
- **오류 처리:** 유효하지 않은 입력은 지정된 오류 메시지를 `std::cerr`로 출력하고 종료 코드 1을 반환해야 합니다.
- **빌드 정합성:** `g++ -std=c++20 -Wall -Wextra -Wpedantic` 옵션으로 컴파일되어야 합니다.

잘못된 입력의 오류 메시지는 배터리 `Error: battery must be 0-100.`, 온도 `Error: temperature must be -40 to 125.`, 상태 플래그 `Error: flags must be 0-7.`로 구분합니다. 입력 실패가 발생한 항목 이후의 처리는 수행하지 않습니다.

해당 프로젝트는 **공백이나 줄바꿈으로 구분된 숫자 세 개를 순서대로 입력하는 형식**을 기준으로 합니다. `12abc`처럼 숫자 뒤에 문자가 붙은 문자열 전체를 거부하는 엄격한 파싱은 여기서 요구하지 않습니다.

**컴파일 및 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/device_health_report.cpp -o device_health
./device_health
```

**자동 검증**

```bash
python3 tests/check.py --only project
python3 tests/check.py --mode student --only project
```

첫 번째 명령어는 모범답안의 여러 입력 사례를 검증하고, 두 번째 명령어는 직접 구현한 프로젝트를 검증합니다. 정상 입력 외에도 경계값·오류·판정 우선순위를 확인합니다.

---

<a id="section-3-12"></a>
## 3.12. Quiz & Summary

### Quiz

**Q1. `17 / 5`와 `17 % 5`의 결과로 올바른 조합은 무엇인가요?**

- A. `3`, `2`
- B. `3.4`, `2`
- C. `2`, `3`
- D. `3`, `0`

<details>
<summary>정답 및 해설</summary>

**정답: A**

두 피연산자가 정수이므로 `/`는 소수 부분을 버린 `3`을 반환하고, `%`는 나머지 `2`를 반환합니다. B는 정수 나눗셈을 실수 나눗셈으로 혼동한 결과입니다.

</details>

**Q2. `count = 10`과 `count == 10`은 무엇이 다른가요?**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** `count = 10`은 변수에 10을 대입하고, `count == 10`은 두 값이 같은지 비교하여 `true` 또는 `false`를 반환합니다.

단순히 기호 하나가 다른 것이 아니라 **값을 변경하는 연산**과 **조건을 검사하는 연산**이라는 목적이 다릅니다.

</details>

**Q3. 다음 조건에서 `count`가 0일 때 두 번째 피연산자 `100 / count > 5`는 실행되나요?**

```cpp
count != 0 && 100 / count > 5
```

<details>
<summary>정답 및 해설</summary>

**정답:** 실행되지 않습니다.

`&&`는 왼쪽이 거짓이면 오른쪽을 평가하지 않습니다. 이 단락 평가 덕분에 해당 표현식은 0으로 나누는 연산을 피할 수 있습니다. 조건의 순서를 반대로 쓰면 안전하지 않습니다.

</details>

**Q4. 거리 30cm를 `0~29cm → STOP`, `30~100cm → SLOW DOWN`으로 분류할 때 결과는 무엇인가요?**

- A. `STOP`
- B. `SLOW DOWN`
- C. `CLEAR`
- D. `INVALID`

<details>
<summary>정답 및 해설</summary>

**정답: B**

30은 `distance < 30`을 만족하지 않지만 `distance <= 100`을 만족합니다. A는 `<`와 `<=`를 혼동한 선택지이고, C는 100보다 큰 정상 거리의 결과입니다. D는 허용 범위 밖 입력에만 적용합니다.

</details>

**Q5. 가드 절(Guard Clause)을 사용하는 이유를 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** 처리할 수 없는 입력이나 상태를 먼저 검사하여 오류를 반환하고, 정상 처리 부분이 불필요한 조건문 안에 계속 중첩되지 않도록 하기 위해 사용합니다.

가드 절의 핵심은 조건식 자체가 아니라 **실패 경로를 먼저 종료하고 정상 흐름을 분리하는 구조**입니다.

</details>

**Q6. `switch` 문에서 `break`를 생략했을 때 발생할 수 있는 동작은 무엇인가요?**

- A. 다음 `case`에 해당하는 문장까지 실행될 수 있습니다.
- B. 무조건 컴파일 오류가 발생합니다.
- C. 다음 반복문의 처음으로 이동합니다.
- D. 프로그램이 자동으로 종료됩니다.

<details>
<summary>정답 및 해설</summary>

**정답: A**

`break`가 없다면 다음 `case`로 실행이 이어지는 Fallthrough가 발생할 수 있습니다. B는 올바르지 않습니다. `break` 생략 자체가 반드시 컴파일 오류는 아닙니다. C는 반복문의 `continue`와 혼동한 설명이며, D는 `main()`의 종료와 다릅니다.

</details>

**Q7. `response_ms > 200 ? "SLOW" : "NORMAL"`에서 `response_ms`가 180이면 선택되는 값은 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

**정답:** `NORMAL`입니다.

`180 > 200`은 거짓이므로 `:` 뒤의 표현식을 선택합니다. 조건 연산자 `?:`는 조건에 따라 두 표현식 중 하나의 값을 선택합니다.

</details>

**Q8. 다음 표현식의 결과는 무엇인가요?**

```cpp
5U & 3U
```

- A. `0`
- B. `1`
- C. `3`
- D. `7`

<details>
<summary>정답 및 해설</summary>

**정답: B**

`5`는 이진수 `0101`, `3`은 `0011`입니다. 비트 AND(`&`)는 두 비트가 모두 1일 때만 1을 남기므로 결과는 `0001`, 즉 1입니다. C는 한쪽의 값을 그대로 가져온 결과이고, D는 비트 OR(`|`)을 적용했을 때의 결과입니다.

</details>

**Q9. 논리 연산자 `&&`와 비트 연산자 `&`의 차이를 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** `&&`는 두 조건의 참·거짓을 결합하는 논리 연산자이며 왼쪽 조건에 따라 오른쪽 평가를 생략할 수 있습니다. `&`는 정수의 이진수 비트 위치마다 AND 연산을 적용합니다.

두 연산자는 입력과 계산 목적이 다르므로 서로 바꾸어 사용해서는 안 됩니다.

</details>

**Q10. 배터리 경고 기준이 20% 이하라면 19%, 20%, 21% 가운데 경고 상태인 값은 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

**정답:** 19%, 20%입니다.

`<= 20`은 경계값 20 자체를 포함합니다. 21은 정상 범위로 넘어가는 값이므로 경계 검사에 함께 사용하면 좋습니다.

</details>

**Q11. 다음 코드에서 `retries_left`를 `if` 문 밖에서 사용할 수 있나요?**

```cpp
if (const int retries_left{2}; retries_left > 0) {
    std::cout << retries_left;
}
```

- A. 언제나 사용할 수 있습니다.
- B. 해당 `if`와 연결된 `else` 내부에서 사용할 수 있지만, `if` 문 밖에서는 사용할 수 없습니다.
- C. 전역 변수로 자동 등록됩니다.
- D. C++20에서는 허용되지 않는 문법입니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

`if` 초기화 구문에서 선언된 변수의 범위는 해당 `if` 문과 연결된 `else`를 포함하는 범위까지입니다. 이 형식은 C++17에서 도입되어 C++20에서도 사용할 수 있습니다. C는 변수의 범위와 전역 변수 개념을 혼동한 설명입니다.

</details>

**Q12. Device Health Report에서 배터리가 18%, 온도가 78°C, 상태 플래그가 7이면 최종 상태는 무엇인가요? 이유도 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**정답:** `FAULT`입니다.

플래그 7(`111`)에는 오류 비트(4)가 포함되어 있습니다. 오류는 온도 경고와 배터리 경고보다 우선순위가 높으므로 `FAULT`를 출력합니다. 하나의 입력에서 여러 조건이 참일 수 있으므로 분기 순서가 중요합니다.

</details>

### Summary

- **연산자(Operator):** 계산·비교·판정을 수행하는 기호이며 피연산자에 적용합니다.
- **산술 연산:** 정수 나눗셈(`/`)은 소수 부분을 버리고 나머지 연산(`%`)은 남는 값을 구합니다.
- **비교 연산:** `==`, `!=`, `<`, `<=`, `>`, `>=`는 `bool` 결과를 만듭니다.
- **논리 연산:** `&&`, `||`, `!`로 조건을 조합하며 단락 평가를 활용할 수 있습니다.
- **조건 분기:** `if`, `else if`, `else`로 범위를, `switch`로 정해진 상태값을 구분합니다.
- **가드 절:** 입력 실패와 허용 범위 이탈을 앞에서 처리합니다.
- **조건 연산자:** `?:`로 간단한 두 값 중 하나를 선택할 수 있습니다.
- **C++17:** `if (초기화; 조건)`으로 임시 변수의 사용 범위를 한정할 수 있습니다.
- **비트 연산:** `&`, `|`, `^`, `~`, `<<`, `>>`로 상태 비트를 검사하거나 변경합니다.
- **경계값:** 조건이 달라지는 지점의 앞뒤 값을 함께 검사합니다.

### References

- [ISO C++ — The Standard](https://isocpp.org/std/the-standard)
- [cppreference — Arithmetic Operators](https://en.cppreference.com/w/cpp/language/operator_arithmetic)
- [cppreference — Logical Operators](https://en.cppreference.com/w/cpp/language/operator_logical)
- [cppreference — `if` Statement](https://en.cppreference.com/w/cpp/language/if)
- [cppreference — `switch` Statement](https://en.cppreference.com/w/cpp/language/switch)
- [cppreference — Conditional Operator](https://en.cppreference.com/w/cpp/language/operator_other)
- [cppreference — Operator Precedence](https://en.cppreference.com/w/cpp/language/operator_precedence)
- [cppreference — `std::basic_istream::operator>>`](https://en.cppreference.com/w/cpp/io/basic_istream/operator_gtgt)
- [C++ Core Guidelines — ES: Expressions and Statements](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-expr)

---

[← C++ 목차](../README.md#contents)

