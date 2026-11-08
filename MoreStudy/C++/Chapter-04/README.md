# Chapter 04. Loops

`for`, `while`, `do-while`을 이용해 작업을 반복하고, 반복 횟수·종료 조건·누적 결과를 제어하는 방법을 학습합니다. `break`, `continue`, 범위 기반 반복문과 중첩 반복문도 다룹니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서도 사용할 수 있는 반복 구문을 중심으로 학습하고, C++20의 Ranges 기능을 간단히 살펴봅니다.

<details>
<summary>선행 학습</summary>

- [Chapter 01. Getting Started with C++](../Chapter-01/) — `main()`, 표준 입출력, 컴파일과 실행
- [Chapter 02. Variables & Data Types](../Chapter-02/) — 변수, 상수, `bool`, 자료형, 형변환
- [Chapter 03. Operators & Conditions](../Chapter-03/) — 산술·비교·논리 연산, `if`, 입력값 검증

</details>

## Contents

| Section | Topic |
|:---:|---|
| [4.1](#section-4-1) | Introduction to Loops — 반복문의 목적과 종료 조건 |
| [4.2](#section-4-2) | `for` Loop — 횟수가 정해진 반복 |
| [4.3](#section-4-3) | Accumulation — 합계와 평균 |
| [4.4](#section-4-4) | `while` Loop — 조건에 따른 반복 |
| [4.5](#section-4-5) | `do-while` Loop — 최소 한 번 실행하는 반복 |
| [4.6](#section-4-6) | `break` & `continue` — 반복 흐름 변경 |
| [4.7](#section-4-7) | Range-Based `for` — 문자열 순회 |
| [4.8](#section-4-8) | Limited Retry — 반복 입력과 재시도 |
| [4.9](#section-4-9) | Nested Loops — 중첩 반복문 |
| [4.10](#section-4-10) | C++20 Ranges — `std::views::iota` |
| [4.11](#section-4-11) | Coding Practice |
| [4.12](#section-4-12) | Mini Project — Sampling Report |
| [4.13](#section-4-13) | Quiz & Summary |

## Getting Started

아래 명령어는 **`Chapter-04/` 디렉터리**에서 실행하는 경우를 기준으로 합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_for_and_counter.cpp -o loops
./loops
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_for_and_counter.cpp -o loops
./loops
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_for_and_counter.cpp /Fe:loops.exe
loops.exe
```

Windows PowerShell에서는 `./loops` 대신 `.\loops.exe`로 실행할 수 있습니다. 컴파일러 설정은 [Chapter 01](../Chapter-01/)에서 확인할 수 있습니다.

**학습 목표**

1. `for`, `while`, `do-while`의 실행 순서와 차이를 설명할 수 있습니다.
2. 반복 조건과 갱신식을 작성하여 원하는 시점에 반복을 종료할 수 있습니다.
3. 반복문으로 합계·평균·개수를 계산하고 0으로 나누는 상황을 피할 수 있습니다.
4. `break`, `continue`, 중첩 반복문으로 처리 흐름을 제어할 수 있습니다.
5. 정상 입력·잘못된 입력·반복 경계값을 검증할 수 있습니다.

---

<a id="section-4-1"></a>
## 4.1. Introduction to Loops — 반복문의 목적과 종료 조건

**반복문(Loop)** 은 같은 코드를 여러 번 실행하기 위한 제어 구문입니다. 예를 들어 측정값을 다섯 번 기록할 때 동일한 출력문을 다섯 줄 작성하는 대신 반복문으로 처리할 수 있습니다.

| 구문 | 조건 검사 시점 | 주로 사용하는 상황 |
|---|---|---|
| `for` | 각 반복을 시작하기 전 | 반복 횟수가 정해진 계산·출력 |
| `while` | 각 반복을 시작하기 전 | 종료 시점이 조건에 따라 달라지는 작업 |
| `do-while` | 본문을 실행한 뒤 | 메뉴 표시처럼 최소 한 번 실행해야 하는 작업 |
| 범위 기반 `for` | 범위의 각 요소에 대해 순회 | 문자열 등의 요소 처리 |

반복문에는 **종료 조건(Termination Condition)** 과 조건을 변화시키는 **갱신(Update)** 이 필요합니다. 조건이 영원히 참이면 반복이 끝나지 않는 **무한 반복(Infinite Loop)** 이 발생할 수 있습니다.

예를 들어 `count`가 `3`에서 시작하고 반복할 때마다 `1`씩 감소한다면, `count > 0`이라는 조건은 언젠가 거짓이 되어 반복이 종료됩니다. 반대로 감소시키는 코드가 없다면 같은 조건으로 계속 반복할 수 있습니다.

---

<a id="section-4-2"></a>
## 4.2. `for` Loop — 횟수가 정해진 반복

`for`는 초기화·조건·갱신을 한곳에 작성하는 반복 구문입니다.

```cpp
for (초기화; 조건; 갱신) {
    // 반복 실행할 코드
}
```

1. **초기화:** 반복문에 처음 진입할 때 한 번 실행합니다.
2. **조건:** 각 반복을 시작하기 전에 검사합니다. 거짓이면 종료합니다.
3. **본문:** 조건이 참일 때 실행합니다.
4. **갱신:** 본문이 정상적으로 끝나면 실행하고 조건을 다시 검사합니다.

여기서 **반복 변수(Loop Variable)** 는 몇 번째 반복인지를 추적하는 변수입니다. `++number`는 Chapter 03에서 배운 증가 연산자이며, `number`에 1을 더합니다.

**예제 코드 — [01_for_and_counter.cpp](./examples/01_for_and_counter.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int sample_count{5};

    for (int number{1}; number <= sample_count; ++number) {
        std::cout << "Sample " << number << '\n';
    }

    std::cout << "Completed: " << sample_count << '\n';
}
```

**실행 결과**

```text
Sample 1
Sample 2
Sample 3
Sample 4
Sample 5
Completed: 5
```

`number`는 1부터 5까지 변하고, 6이 되면 `number <= sample_count`가 거짓이 되어 종료합니다. `number < sample_count`로 작성하면 마지막 값인 5를 처리하지 못합니다.

또한 다음 예제처럼 반복 횟수가 0인 경우에는 본문이 한 번도 실행되지 않을 수 있습니다.

```cpp
for (int index{0}; index < 0; ++index) {
    std::cout << "Not executed\n";
}
```

---

<a id="section-4-3"></a>
## 4.3. Accumulation — 합계와 평균

**누적 계산(Accumulation)** 은 반복하는 동안 계산 결과를 변수에 계속 더하거나 갱신하는 방식입니다. 합계를 저장하는 변수를 **누적 변수(Accumulator)** 라고 합니다.

```cpp
int total{0};
total += 10;  // 10
total += 20;  // 30
```

합계를 구하는 변수는 일반적으로 0으로 초기화해야 합니다. 값을 초기화하지 않으면 의도하지 않은 결과가 발생할 수 있습니다. 평균은 합계를 항목 개수로 나누어 구하지만, 항목 개수가 0일 때는 나눗셈을 하지 않아야 합니다.

**예제 코드 — [02_accumulation.cpp](./examples/02_accumulation.cpp)**

```cpp
#include <iomanip>
#include <iostream>

int main() {
    constexpr int sample_count{4};
    int total{0};

    for (int number{1}; number <= sample_count; ++number) {
        const int reading{number * 10};
        total += reading;
    }

    const double average{
        static_cast<double>(total) / sample_count
    };

    std::cout << "Total: " << total << '\n';
    std::cout << "Average: " << std::fixed
              << std::setprecision(1) << average << '\n';
}
```

**실행 결과**

```text
Total: 100
Average: 25.0
```

각 반복에서 `10, 20, 30, 40`을 합산합니다. `static_cast<double>(total)`을 사용하여 정수끼리 나누면서 소수 부분이 사라지는 문제를 피합니다. `<iomanip>` 헤더의 `std::setprecision(1)`과 `std::fixed`는 Chapter 02에서 다룬 출력 자릿수 설정입니다.

**입력값이 늘어나도** `sample_count`와 반복 대상만 적절히 조정하면 동일한 계산 구조를 활용할 수 있습니다. 다만 큰 값을 계속 더하는 경우에는 누적 변수의 자료형이 결과를 담을 수 있는 범위인지 확인해야 합니다.

---

<a id="section-4-4"></a>
## 4.4. `while` Loop — 조건에 따른 반복

`while`은 **조건이 참인 동안 본문을 반복**합니다. 조건을 먼저 확인하므로 처음부터 거짓이면 본문을 실행하지 않습니다.

```cpp
while (조건) {
    // 반복 실행할 코드
}
```

**예제 코드 — [03_while_countdown.cpp](./examples/03_while_countdown.cpp)**

```cpp
#include <iostream>

int main() {
    int remaining{3};

    while (remaining > 0) {
        std::cout << remaining << '\n';
        --remaining;
    }

    std::cout << "Ready!\n";
}
```

**실행 결과**

```text
3
2
1
Ready!
```

`remaining`은 3에서 시작하여 `--remaining`에 따라 2, 1, 0으로 감소합니다. 0이 되면 `remaining > 0` 조건이 거짓이므로 본문을 더 이상 실행하지 않습니다.

`for`로도 같은 결과를 만들 수 있습니다. 다만 연결 상태나 입력 여부처럼 반복 횟수를 미리 알 수 없는 상황에서는 `while`이 더 자연스러울 수 있습니다.

---

<a id="section-4-5"></a>
## 4.5. `do-while` Loop — 최소 한 번 실행하는 반복

`do-while`은 먼저 본문을 실행한 다음 조건을 확인합니다. 그래서 조건이 처음부터 거짓이어도 **최소 한 번** 실행됩니다. 마지막 `while (조건);` 뒤에는 세미콜론(`;`)이 필요합니다.

```cpp
do {
    // 최소 한 번 실행할 코드
} while (조건);
```

메뉴에서 `0`을 입력할 때까지 선택지를 다시 보여주는 예제입니다.

**예제 코드 — [04_do_while_menu.cpp](./examples/04_do_while_menu.cpp)**

```cpp
#include <iostream>

int main() {
    int selection{};

    do {
        std::cout << "1. Show status\n"
                  << "0. Exit\n"
                  << "Select: " << std::flush;

        if (!(std::cin >> selection)) {
            std::cerr << "Error: integer input required.\n";
            return 1;
        }

        if (selection == 1) {
            std::cout << "Status: READY\n";
        } else if (selection != 0) {
            std::cout << "Unknown selection\n";
        }
    } while (selection != 0);

    std::cout << "Goodbye\n";
}
```

**실행 예시 (1, 0 순서로 입력)**

```text
1. Show status
0. Exit
Select: 1
Status: READY
1. Show status
0. Exit
Select: 0
Goodbye
```

- `1`을 선택하면 상태를 출력한 뒤 다시 메뉴를 표시합니다.
- `0`을 선택하면 조건이 거짓이 되어 반복을 종료합니다.
- 다른 정수는 `Unknown selection`을 출력한 뒤 다시 메뉴를 표시합니다.
- 정수가 아닌 입력이나 입력 종료(EOF)가 발생하면 오류 메시지를 출력하고 종료합니다.

`std::cin`의 입력 실패 상태를 복구하지 않은 상태에서 무조건 반복하면 같은 실패를 반복할 수 있습니다. 이 예제는 복잡한 입력 복구 대신 오류 발생 시 종료하도록 구성했습니다.

---

<a id="section-4-6"></a>
## 4.6. `break` & `continue` — 반복 흐름 변경

반복 도중 작업을 중단하거나 일부 처리를 건너뛸 때 사용합니다.

| 키워드 | 동작 | 대표적인 사용 사례 |
|---|---|---|
| `break` | 가장 가까운 반복문을 즉시 종료 | 목표값을 찾았을 때 탐색 중지 |
| `continue` | 현재 반복의 나머지를 건너뛰고 다음 반복 진행 | 조건에 맞지 않는 데이터 제외 |

`break`는 Chapter 03의 `switch`에서도 사용되지만, 반복문 안에서는 반복 자체를 끝냅니다. `continue`는 `for` 반복문에서 현재 본문을 건너뛴 뒤 **갱신식으로 이동**하고, 다시 조건을 검사합니다.

**예제 코드 — [05_break_and_continue.cpp](./examples/05_break_and_continue.cpp)**

```cpp
#include <iostream>

int main() {
    for (int reading{-2}; reading <= 6; reading += 2) {
        if (reading < 0) {
            continue;
        }
        if (reading > 4) {
            std::cout << "Limit reached\n";
            break;
        }
        std::cout << "Accepted: " << reading << '\n';
    }
}
```

**실행 결과**

```text
Accepted: 0
Accepted: 2
Accepted: 4
Limit reached
```

`-2`는 음수이므로 `continue`에 의해 제외됩니다. `0, 2, 4`는 정상 출력하며, `6`에서 `break`를 만나 반복이 종료됩니다. 중첩 반복문에서 `break`는 **가장 안쪽 반복문만 종료**한다는 점에 주의해야 합니다.

---

<a id="section-4-7"></a>
## 4.7. Range-Based `for` — 문자열 순회

**범위 기반 반복문(Range-Based `for` Loop)** 은 범위 안에 있는 요소를 하나씩 꺼내는 형태입니다. 요소의 개수만큼 반복하므로 직접 반복 인덱스를 작성하지 않아도 됩니다.

```cpp
for (요소를 받을 변수 : 범위) {
    // 요소를 사용하는 코드
}
```

Chapter 01에서 사용한 `std::string`도 범위 기반 `for`로 순회할 수 있습니다. 다음 예제에서는 영문자와 숫자로만 구성된 코드의 숫자 개수를 셉니다.

**예제 코드 — [06_range_for_string.cpp](./examples/06_range_for_string.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    const std::string code{"A1B2C"};
    int digit_count{};

    for (const char character : code) {
        if (character >= '0' && character <= '9') {
            ++digit_count;
        }
    }

    std::cout << "Code: " << code << '\n';
    std::cout << "Digits: " << digit_count << '\n';
}
```

**실행 결과**

```text
Code: A1B2C
Digits: 2
```

문자 `1`, `2`만 `'0'`~`'9'` 범위에 들어가므로 결과는 2입니다. `char` 타입은 단일 바이트 문자 코드를 다룰 수 있지만, UTF-8로 인코딩한 한글 등의 문자를 `char` 하나가 반드시 표현하지는 않습니다. 위 예제는 **ASCII 영문자·숫자 데이터**를 전제로 합니다.

배열과 컨테이너의 다양한 순회 방법은 이후 관련 Chapter에서 확장합니다.

---

<a id="section-4-8"></a>
## 4.8. Limited Retry — 반복 입력과 재시도

잘못된 입력을 다시 받는 프로그램은 **최대 재시도 횟수(Retry Limit)** 와 입력 실패 시의 처리 방법을 함께 정해야 합니다. 종료 조건이 없는 반복은 사용자가 계속 잘못된 값을 입력할 때 끝나지 않을 수 있습니다.

**예제 코드 — [07_limited_retry.cpp](./examples/07_limited_retry.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int max_attempts{3};

    for (int attempt{1}; attempt <= max_attempts; ++attempt) {
        std::cout << "Reading (0-100): " << std::flush;

        int reading{};
        if (!(std::cin >> reading)) {
            std::cerr << "Error: integer input required.\n";
            return 1;
        }

        if (reading < 0 || reading > 100) {
            std::cout << "Invalid reading\n";
            continue;
        }

        std::cout << "Accepted: " << reading << '\n';
        return 0;
    }

    std::cerr << "Error: retry limit exceeded.\n";
    return 1;
}
```

**실행 예시 (120, 25 순서로 입력)**

```text
Reading (0-100): 120
Invalid reading
Reading (0-100): 25
Accepted: 25
```

- **범위 오류:** `0~100`을 벗어난 정수를 입력하면 재시도합니다.
- **정상 입력:** 값을 출력하고 즉시 종료합니다.
- **세 번 모두 범위 오류:** 한도 초과 메시지를 `std::cerr`로 출력하고 실패로 종료합니다.
- **정수 입력 실패:** `std::cin`이 실패한 상태에서는 반복하지 않고 즉시 종료합니다.

`std::cin >> int`는 `12abc`처럼 숫자 뒤에 다른 문자가 붙은 입력을 일부 읽을 수 있습니다. 입력 한 줄 전체를 엄격하게 검사해야 하는 경우에는 별도의 문자열 파싱이 필요합니다. 여기서는 재시도 구조와 종료 조건에 집중합니다.

---

<a id="section-4-9"></a>
## 4.9. Nested Loops — 중첩 반복문

**중첩 반복문(Nested Loop)** 은 반복문 안에 다른 반복문을 배치하는 방식입니다. 격자처럼 행(Row)과 열(Column)을 반복할 때 사용할 수 있습니다.

바깥 반복문이 한 번 실행될 때마다 안쪽 반복문이 처음부터 끝까지 실행됩니다. 아래 예제는 3행 5열 격자를 출력합니다.

**예제 코드 — [08_nested_loops.cpp](./examples/08_nested_loops.cpp)**

```cpp
#include <iostream>

int main() {
    constexpr int rows{3};
    constexpr int columns{5};

    for (int row{0}; row < rows; ++row) {
        for (int column{0}; column < columns; ++column) {
            const char symbol{
                (row + column) % 2 == 0 ? '#' : '.'
            };
            std::cout << symbol;
        }
        std::cout << '\n';
    }
}
```

**실행 결과**

```text
#.#.#
.#.#.
#.#.#
```

`row`는 0부터 2까지, `column`은 각 행에서 0부터 4까지 변합니다. `(row + column) % 2 == 0`이면 `#`, 아니면 `.`을 출력합니다. 안쪽 반복문이 끝날 때마다 줄바꿈을 추가합니다.

행이 `R`개, 열이 `C`개인 격자의 모든 위치를 한 번씩 방문하면 **총 `R × C`회**의 내부 작업을 수행합니다. 중첩이 깊어질수록 반복 횟수가 빠르게 늘어날 수 있으므로 주의해야 합니다.

---

<a id="section-4-10"></a>
## 4.10. C++20 Ranges — `std::views::iota`

C++20에서 도입된 **Ranges** 기능을 이용하면 순차적인 숫자를 하나의 범위로 표현할 수 있습니다. `<ranges>`는 이러한 범위와 뷰(View) 기능을 제공하는 표준 헤더입니다.

**새로운 헤더 — `<ranges>`:** 아래 예제의 `std::views::iota()`를 사용하기 위해 포함합니다. `iota`는 시작값부터 끝값 **직전까지**의 연속된 값을 생성하는 뷰입니다. 모든 값을 별도 컨테이너에 저장하는 방식은 아닙니다.

**예제 코드 — [09_cxx20_iota.cpp](./examples/09_cxx20_iota.cpp)**

```cpp
#include <iostream>
#include <ranges>

int main() {
    for (const int number : std::views::iota(1, 5)) {
        std::cout << "Step " << number << '\n';
    }
}
```

**실행 결과**

```text
Step 1
Step 2
Step 3
Step 4
```

`std::views::iota(1, 5)`는 `1, 2, 3, 4`를 순회하며 끝값 `5`를 포함하지 않습니다. 기본적인 횟수 반복에서는 일반 `for`도 충분하며, Ranges의 다양한 조합 방법은 표준 라이브러리 학습에서 자세히 다룹니다.

---

<a id="section-4-11"></a>
## 4.11. Coding Practice

각 문제는 `exercises/`에 시작 코드가 있고, `solutions/`에서 모범답안을 확인할 수 있습니다. 문제에서 지정한 출력 형식과 오류 조건을 확인한 뒤 구현합니다.

| No. | Practice | Exercise | Solution |
|:---:|---|---|---|
| 01 | Sum from One | [문제 코드](./exercises/01_sum_from_one.cpp) | [정답 코드](./solutions/01_sum_from_one.cpp) |
| 02 | Countdown | [문제 코드](./exercises/02_countdown.cpp) | [정답 코드](./solutions/02_countdown.cpp) |
| 03 | Filter Readings | [문제 코드](./exercises/03_filter_readings.cpp) | [정답 코드](./solutions/03_filter_readings.cpp) |
| 04 | Checkerboard | [문제 코드](./exercises/04_checkerboard.cpp) | [정답 코드](./solutions/04_checkerboard.cpp) |

### Exercise 01 — Sum from One

입력받은 정수 `N`에 대해 1부터 `N`까지 모든 정수의 합계를 구합니다.

**구현 조건**

- `N`은 `1~100` 범위의 정수입니다.
- `for` 반복문을 사용해 합계를 계산합니다.
- 오류 입력은 `std::cerr`에 메시지를 출력하고 실패로 종료합니다.

**입력 예시**

```text
5
```

**기대 출력**

```text
Sum: 15
```

경계값 `1`과 `100`에서도 각각 `1`, `5050`이 출력되어야 합니다.

### Exercise 02 — Countdown

입력받은 `N`부터 1까지 숫자를 한 줄씩 출력한 뒤 마지막에 `Launch!`를 출력합니다.

**구현 조건**

- `N`은 `1~20` 범위의 정수입니다.
- `while` 반복문을 사용합니다.
- `N`이 0이 되면 반복이 끝나야 합니다.

**입력 예시**

```text
3
```

**기대 출력**

```text
3
2
1
Launch!
```

### Exercise 03 — Filter Readings

측정값 중 **0 이상의 정수만** 평균 계산에 포함합니다.

**구현 조건**

- 처음에 측정값 개수 `N`을 입력하며, `1~8`만 허용합니다.
- 이어서 `N`개의 정수를 입력하며 각 값은 `-100~100` 범위여야 합니다.
- 음수는 `continue`로 건너뛰고, `0`은 정상 측정값으로 포함합니다.
- 포함한 값의 개수와 평균을 소수 첫째 자리까지 출력합니다.
- 포함한 측정값이 하나도 없거나 입력 형식·범위에 오류가 있으면 실패로 종료합니다.

**입력 예시**

```text
5
10
-1
20
30
-5
```

**기대 출력**

```text
Accepted: 3
Average: 20.0
```

### Exercise 04 — Checkerboard

중첩 반복문을 활용해 `#`과 `.`이 교대로 나타나는 격자를 출력합니다.

**구현 조건**

- `rows`와 `columns` 두 정수를 입력합니다. 각각 `1~8`을 허용합니다.
- 좌측 상단 좌표 `(0, 0)`은 `#`입니다.
- 행과 열의 인덱스 합이 짝수이면 `#`, 홀수이면 `.`을 출력합니다.
- 행이 끝나면 줄바꿈합니다.

**입력 예시**

```text
3 4
```

**기대 출력**

```text
#.#.
.#.#
#.#.
```

### 실행 및 검증

예를 들어 Exercise 01을 직접 컴파일하려면 아래 명령어를 사용합니다.

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/01_sum_from_one.cpp -o sum_from_one
./sum_from_one
```

자동 검증에는 Python 3과 GCC 또는 Clang이 필요합니다. `python3` 명령어가 없는 Windows 환경에서는 `py` 또는 `python`을 사용할 수 있습니다.

```bash
python3 tests/check.py
python3 tests/check.py --exercise 04
```

**첫 번째 명령어**는 예제와 모범답안을 확인하는 용도입니다. **두 번째 명령어**는 직접 수정한 Exercise 04를 검사합니다. 아직 코드가 작성되지 않아 초기 상태에서는 FAIL이 나오는 것이 정상입니다. 테스트 코드는 C++20으로 컴파일한 뒤 다양한 입력값을 전달하여 종료 코드와 출력 결과를 비교합니다.

---

<a id="section-4-12"></a>
## 4.12. Mini Project — Sampling Report

여러 번 입력받은 측정값으로 보고서를 만드는 콘솔 프로그램입니다. 반복문으로 값을 수집하면서 합계, 평균, 최솟값, 최댓값, 높은 측정값의 개수를 계산합니다.

**파일**

- [sampling_report.cpp](./project/sampling_report.cpp) — 직접 구현할 시작 코드
- [sampling_report.cpp](./solutions/sampling_report.cpp) — 모범답안

**프로그램 흐름**

```text
측정 횟수 입력(1~6)
       ↓
측정값 입력(0~100)
       ↓
범위 오류 시 최대 2회 시도
       ↓
정상값을 누적하고 최솟값·최댓값 갱신
       ↓
합계 / 평균 / 최솟값 / 최댓값 / 80 이상인 측정값 개수 출력
```

입력값의 단위는 별도로 정의하지 않은 **0~100의 예시 측정값**입니다. `80` 이상이면 높은 값으로 분류합니다.

**구현 조건**

- 측정 횟수는 `1~6`의 정수만 허용합니다.
- 각 측정값은 `0~100`의 정수여야 합니다.
- 범위를 벗어난 정수는 `Invalid reading`을 출력하고 같은 순번에서 재시도합니다.
- 한 측정값당 최대 두 번 시도하며, 모두 실패하면 오류 메시지를 출력하고 종료합니다.
- 정수가 아닌 입력이나 입력 종료 시 즉시 오류 종료합니다.
- 정상 측정값만 합계·최솟값·최댓값에 반영합니다.
- 평균은 소수 둘째 자리까지 출력합니다.
- 80 이상인 측정값의 개수를 계산하며, 오류 시에는 보고서를 출력하지 않습니다.

**실행 예시 (입력: 4, 80, 15, 95, 45)**

```text
Samples (1-6): 4
Reading 1 (0-100): 80
Reading 2 (0-100): 15
Reading 3 (0-100): 95
Reading 4 (0-100): 45

--- Sampling Report ---
Samples: 4
Total: 235
Average: 58.75
Minimum: 15
Maximum: 95
High readings (>=80): 2
```

**재시도 예시 (입력: 2, 150, 95, 80)**

```text
Samples (1-6): 2
Reading 1 (0-100): 150
Invalid reading
Reading 1 (0-100): 95
Reading 2 (0-100): 80

--- Sampling Report ---
Samples: 2
Total: 175
Average: 87.50
Minimum: 80
Maximum: 95
High readings (>=80): 2
```

**완료 기준**

- **반복 횟수:** 지정한 수만큼 정상 측정값을 받고 종료해야 합니다.
- **재시도:** 범위를 벗어난 정수는 결과에 포함하지 않고 최대 두 번까지 시도해야 합니다.
- **집계:** 평균·최솟값·최댓값·80 이상 개수가 실제 정상 입력값과 일치해야 합니다.
- **오류 처리:** 정수가 아닌 입력, 입력 종료, 재시도 한도 초과 시 비정상 종료해야 합니다.
- **컴파일:** `g++ -std=c++20`으로 컴파일할 수 있어야 합니다.

**직접 작성한 파일 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/sampling_report.cpp -o sampling
./sampling
```

시작 코드에는 구현해야 할 부분이 남아 있습니다. 완성된 실행 결과는 `solutions/sampling_report.cpp`를 컴파일하여 비교할 수 있습니다.

**자동 검증**

```bash
python3 tests/check.py --project
```

이 명령어는 직접 작성한 `project/sampling_report.cpp`를 대상으로 실행됩니다. 아직 구현하지 않은 초기 파일에서는 FAIL이 발생합니다.

---

<a id="section-4-13"></a>
## 4.13. Quiz & Summary

### Quiz

**Q1. `for` 반복문의 초기화·조건·갱신은 각각 언제 실행되나요?**

<details>
<summary>정답 및 해설</summary>

초기화는 반복 시작 시 한 번 실행합니다. 조건은 매 반복의 시작 전에 평가합니다. 조건이 참이면 본문을 실행하고, 본문이 정상 종료되면 갱신식을 실행한 뒤 조건을 다시 검사합니다.

</details>

**Q2. 다음 코드의 출력 결과는 무엇인가요?**

```cpp
for (int number{1}; number < 4; ++number) {
    std::cout << number;
}
```

A. `123`  
B. `1234`  
C. `0123`  
D. `4`

<details>
<summary>정답 및 해설</summary>

**정답: A. `123`**

`number`는 1에서 시작해 1, 2, 3일 때 본문을 실행합니다. 4가 되면 `< 4` 조건이 거짓이므로 종료합니다. **B**는 끝값 4를 포함한다고 착각한 경우이고, **C**는 초기값 1 대신 0에서 시작한다고 착각한 경우입니다.

</details>

**Q3. 처음부터 반복 조건이 거짓이어도 본문을 최소 한 번 실행하는 반복문은 무엇인가요?**

A. `for`  
B. `while`  
C. `do-while`  
D. 범위 기반 `for`

<details>
<summary>정답 및 해설</summary>

**정답: C. `do-while`**

`do-while`은 본문을 실행한 뒤 조건을 확인합니다. 반면 일반 `for`와 `while`은 본문 실행 전에 조건을 검사합니다.

</details>

**Q4. `break`와 `continue`의 차이를 설명해 보세요.**

<details>
<summary>정답 및 해설</summary>

`break`는 가장 가까운 반복문을 즉시 끝냅니다. `continue`는 현재 반복의 나머지를 건너뛰고 다음 반복으로 넘어갑니다. `for`에서는 `continue` 이후 갱신식이 실행됩니다.

</details>

**Q5. 아래 코드의 최종 합계는 얼마인가요?**

```cpp
int total{};
for (int value{1}; value <= 5; ++value) {
    if (value % 2 == 0) {
        continue;
    }
    total += value;
}
```

A. `6`  
B. `9`  
C. `10`  
D. `15`

<details>
<summary>정답 및 해설</summary>

**정답: B. `9`**

짝수 2와 4는 `continue`로 건너뛰므로 합계에는 홀수 1, 3, 5만 포함됩니다. 따라서 `1 + 3 + 5 = 9`입니다. **D**는 짝수도 포함해 모두 더한 경우입니다.

</details>

**Q6. 평균을 계산하는 반복 프로그램에서 나눗셈 전에 확인해야 하는 조건은 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

**평균을 구할 항목 수가 0이 아닌지** 확인해야 합니다. 항목 수가 0이면 나눗셈을 수행해서는 안 됩니다. 정수 나눗셈으로 소수 부분이 손실되는 문제도 고려해야 합니다.

</details>

**Q7. 중첩 반복문에서 안쪽 반복문에 `break`를 사용하면 어떤 일이 발생하나요?**

A. 프로그램 전체가 즉시 종료됩니다.  
B. 모든 반복문이 한 번에 종료됩니다.  
C. 가장 안쪽 반복문만 종료됩니다.  
D. 현재 반복만 건너뛰고 다음 반복으로 이동합니다.

<details>
<summary>정답 및 해설</summary>

**정답: C. 가장 안쪽 반복문만 종료됩니다.**

`break`는 자신이 속한 가장 가까운 반복문을 종료합니다. 바깥쪽 반복문은 자신의 조건과 갱신에 따라 계속 진행할 수 있습니다. **D**는 `continue`의 동작에 가깝습니다.

</details>

**Q8. `std::cin >> reading`이 실패했는데 오류 상태를 처리하지 않고 같은 입력 구문을 반복하면 어떤 문제가 생길 수 있나요?**

<details>
<summary>정답 및 해설</summary>

입력 스트림에 오류 상태가 유지되어 다음 입력도 계속 실패할 수 있습니다. 따라서 재입력을 허용하려면 스트림 오류 상태 및 남아 있는 입력을 적절히 처리해야 합니다. 이번 예제에서는 입력 실패 시 즉시 종료하도록 구성했습니다.

</details>

**Q9. `std::views::iota(2, 6)`으로 순회할 때 얻는 값은 무엇인가요?**

A. `2, 3, 4, 5`  
B. `2, 3, 4, 5, 6`  
C. `3, 4, 5, 6`  
D. `2, 4, 6`

<details>
<summary>정답 및 해설</summary>

**정답: A. `2, 3, 4, 5`**

시작값 2는 포함하고 끝값 6은 포함하지 않습니다. 범위는 연속된 값으로 구성되므로 2씩 증가하는 것도 아닙니다.

</details>

**Q10. 다음 반복문은 본문을 총 몇 번 실행하나요?**

```cpp
for (int row{0}; row < 3; ++row) {
    for (int column{0}; column < 4; ++column) {
        std::cout << '*';
    }
}
```

<details>
<summary>정답 및 해설</summary>

**정답: 12번**

바깥 반복문은 3번, 안쪽 반복문은 바깥 반복 한 번마다 4번 실행합니다. 총 반복 횟수는 `3 × 4 = 12`입니다.

</details>

**Q11. 아래 반복문이 종료되지 않는 이유는 무엇인가요?**

```cpp
int count{3};
while (count > 0) {
    std::cout << count << '\n';
}
```

<details>
<summary>정답 및 해설</summary>

`count`가 변하지 않아 `count > 0`이 계속 참이기 때문입니다. 반복 본문에서 `--count;`처럼 값을 변화시키는 구문이 필요합니다.

</details>

**Q12. Sampling Report에서 범위를 벗어난 측정값을 합계에 더하지 않아야 하는 이유를 설명해 보세요.**

<details>
<summary>정답 및 해설</summary>

오류 입력까지 합산하면 실제로 인정된 측정값의 합계·평균·최솟값·최댓값이 왜곡됩니다. 따라서 범위를 확인한 뒤 정상값만 통계에 반영해야 합니다.

</details>

### Summary

- **반복문(Loop):** 같은 코드를 조건에 따라 반복 실행하는 구문
- **`for`:** 초기화·조건·갱신을 함께 작성하는 반복
- **누적 변수(Accumulator):** 반복하며 합계나 개수를 저장하는 변수
- **`while`:** 반복 시작 전에 종료 조건을 검사
- **`do-while`:** 본문을 먼저 실행하므로 최소 한 번 실행
- **`break`:** 가장 가까운 반복문 종료
- **`continue`:** 현재 반복의 나머지를 건너뛰고 다음 반복 진행
- **범위 기반 `for`:** 요소를 하나씩 순서대로 처리
- **재시도 횟수:** 제한과 입력 실패 처리를 함께 고려
- **중첩 반복문:** 행·열처럼 여러 차원의 반복을 조합
- **`std::views::iota`:** C++20에서 연속된 값의 범위를 생성하는 기능

### References

- [cppreference — `for` Statement](https://en.cppreference.com/w/cpp/language/for)
- [cppreference — `while` Statement](https://en.cppreference.com/w/cpp/language/while)
- [cppreference — `do-while` Statement](https://en.cppreference.com/w/cpp/language/do)
- [cppreference — Range-Based `for`](https://en.cppreference.com/w/cpp/language/range-for)
- [cppreference — `break`](https://en.cppreference.com/w/cpp/language/break)
- [cppreference — `continue`](https://en.cppreference.com/w/cpp/language/continue)
- [cppreference — `std::ranges::iota_view`](https://en.cppreference.com/w/cpp/ranges/iota_view)

---

[← C++ 목차](../README.md#contents)
