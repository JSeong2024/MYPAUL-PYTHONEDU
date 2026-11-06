# Chapter 01. Getting Started

C++23 개발 환경, 컴파일 과정, 프로그램 구조, 표준 입출력, 문자열, `using` 선언 및 입력값 검증을 다룹니다.

본 자료는 **C++23(ISO/IEC 14882:2024)**을 기준으로 작성되었습니다.

## Contents

| Section | Topic |
|:---:|---|
| 1.1 | C++23과 프로그램 실행 과정 |
| 1.2 | 개발 환경 및 컴파일 |
| 1.3 | 첫 번째 C++23 프로그램 |
| 1.4 | 표준 출력과 오류 출력 |
| 1.5 | 표준 입력과 기본 검증 |
| 1.6 | 문자열 입력 및 검색 |
| 1.7 | Namespace & Using Declarations |
| 1.8 | 정수 입력의 엄격한 검증 |
| 1.9 | Coding Practice |
| 1.10 | Summary |

---

## 1.1. C++23과 프로그램 실행 과정

C++은 일반적으로 소스 코드를 컴파일하고 링크하여 실행 파일을 생성하는 프로그래밍 언어입니다. 프로그램은 다음 과정을 거쳐 실행됩니다.

```text
소스 코드(.cpp) → 컴파일(.o/.obj) → 링크 → 실행 파일
```

- **컴파일:** 소스 코드를 목적 파일로 변환
- **링크:** 목적 파일과 필요한 라이브러리를 결합
- **실행:** 완성된 실행 파일을 운영체제에서 실행

`g++`, `clang++`을 이용하면 일반적으로 하나의 명령으로 컴파일과 링크를 수행할 수 있습니다.

C++23 모드를 지정하더라도 모든 기능을 사용할 수 있는 것은 아닙니다. 실제 지원 범위는 컴파일러와 표준 라이브러리의 버전에 따라 달라집니다.

## 1.2. 개발 환경 및 컴파일

C++ 프로그램을 빌드하려면 컴파일러가 필요합니다. 대표적인 컴파일러와 버전 확인 명령어는 다음과 같습니다.

| 컴파일러 | 주요 사용 환경 | 버전 확인 |
|---|---|---|
| GCC | Windows, Linux | `g++ --version` |
| Clang | macOS, Linux, Windows | `clang++ --version` |
| MSVC | Windows (Visual Studio) | `cl` |

아래 명령어는 `Chapter-01/` 폴더에서 실행하는 것을 기준으로 합니다.

### GCC

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -g examples/01_hello_world.cpp -o hello
./hello
```

### Clang

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic -g examples/01_hello_world.cpp -o hello
./hello
```

| 옵션 | 설명 |
|---|---|
| `-std=c++23` | C++23 표준 모드 지정 |
| `-Wall -Wextra` | 주요 컴파일 경고 활성화 |
| `-Wpedantic` | 표준 외 확장 기능에 대한 경고 활성화 |
| `-g` | 디버깅 정보 포함 |
| `-o hello` | 실행 파일 이름 지정 |

Windows PowerShell에서는 생성된 실행 파일을 `./hello` 대신 `.\hello.exe`로 실행합니다.

### MSVC (Visual Studio)

Visual Studio의 **Developer Command Prompt**에서 다음 명령을 실행합니다.

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 examples\01_hello_world.cpp /Fe:hello.exe
hello.exe
```

- `/std:c++23preview`: 지원되는 C++23 기능 활성화(미리 보기 모드)
- `/W4`: 경고 수준 4 설정
- `/EHsc`: C++ 예외 처리 방식 지정
- `/permissive-`: 표준 준수 검사 강화
- `/utf-8`: 소스 및 실행 문자 집합을 UTF-8로 지정

MSVC의 C++23 지원은 버전에 따라 달라집니다. 현재 공식 문서에서는 `/std:c++23preview`를 안내하며, 설치된 도구 집합에서 제공하는 옵션을 확인해야 합니다. `<print>` 등 개별 표준 라이브러리 기능의 지원 여부도 별도로 확인합니다.

### Google Colab (선택)

Google Colab에서도 셸 명령을 이용해 C++ 코드를 컴파일할 수 있습니다. 다음 과정은 각각 별도의 코드 셀에서 실행합니다.

**① 컴파일러 확인**

```python
!g++ --version
```

**② 소스 파일 작성**

```cpp
%%writefile hello.cpp
#include <print>

int main() {
    std::println("Hello, C++23!");
}
```

**③ 컴파일 및 실행**

```python
!g++ -std=c++23 -Wall -Wextra -Wpedantic hello.cpp -o hello
!./hello
```

`%%writefile`은 셀의 첫 줄에 작성해야 합니다. Colab 환경의 컴파일러나 표준 라이브러리에서 `<print>`를 지원하지 않는 경우에는 1.3의 `std::cout` 대체 예제를 사용합니다.

## 1.3. 첫 번째 C++23 프로그램

[예제 코드 — 01_hello_world.cpp](./examples/01_hello_world.cpp)

```cpp
#include <print>

int main() {
    std::println("Hello, C++23!");
    return 0;
}
```

**실행 결과**

```text
Hello, C++23!
```

이 프로그램은 C++23에서 도입된 `std::println()`을 사용하여 문자열을 출력합니다.

| 구성 요소 | 설명 |
|---|---|
| `#include <print>` | C++23 형식화 출력 기능을 제공하는 헤더 포함 |
| `int main()` | 프로그램의 시작 지점 |
| `std::println()` | 값을 출력하고 줄바꿈을 추가하는 함수 |
| `return 0;` | 정상 종료를 나타내는 반환값 (`main()`에서는 생략 가능) |
| `;` | 문장 종료 구분자 |

현재 컴파일 환경에서 `<print>`를 지원하지 않는다면 `std::cout`으로 동일한 결과를 출력할 수 있습니다.

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, C++23!\n";
}
```

## 1.4. 표준 출력과 오류 출력

C++은 일반적인 출력과 오류 메시지를 서로 다른 스트림으로 구분할 수 있습니다.

| 구문 | 출력 스트림 | 용도 |
|---|---|---|
| `std::cout` | stdout | 일반 메시지 및 처리 결과 출력 |
| `std::cerr` | stderr | 오류 메시지 출력 |
| `std::print()` | stdout | C++23 형식화 출력 |
| `std::println()` | stdout | C++23 형식화 출력 및 줄바꿈 |

[예제 코드 — 02_output_streams.cpp](./examples/02_output_streams.cpp)

```cpp
#include <iostream>

int main() {
    std::cout << "Application started.\n";
    std::cerr << "Error: configuration file not found.\n";
    return 1;
}
```

위 코드는 일반 메시지와 오류 메시지를 각각 `stdout`, `stderr`로 출력합니다. 두 스트림을 구분하면 명령행에서 출력 결과와 오류 로그를 별도로 저장하거나 처리할 수 있습니다.

`main()`에서 `0`을 반환하면 정상 종료, `0`이 아닌 값을 반환하면 비정상 종료를 나타냅니다. 이 예제는 오류 상황을 가정하므로 `1`을 반환합니다.

- `\n`: 줄바꿈 문자
- `std::endl`: 줄바꿈 후 출력 스트림 flush 수행
- `std::flush`: 줄바꿈 없이 출력 스트림 flush 수행

일반적인 줄바꿈에는 `\n`을 사용합니다. 입력을 기다리는 프롬프트처럼 출력을 즉시 표시해야 하는 상황에서는 `std::flush`를 명시할 수 있습니다.

## 1.5. 표준 입력과 기본 검증

`std::cin`은 표준 입력 스트림입니다. `>>` 연산자로 값을 읽을 수 있으며, 사용자 입력을 처리할 때는 **입력 성공 여부와 허용 범위**를 확인해야 합니다.

[예제 코드 — 03_number_input.cpp](./examples/03_number_input.cpp)

```cpp
#include <iostream>

int main() {
    int quantity{};

    std::cout << "Quantity (1-1000): " << std::flush;
    if (!(std::cin >> quantity) || quantity < 1 || quantity > 1000) {
        std::cerr << "Error: enter an integer from 1 to 1000.\n";
        return 1;
    }

    std::cout << "Quantity: " << quantity << '\n';
    return 0;
}
```

**실행 예시**

```text
Quantity (1-1000): 5
Quantity: 5
```

- `int quantity{}`: 정수 변수를 0으로 초기화
- `!(std::cin >> quantity)`: 입력 실패 또는 숫자 변환 실패 확인
- `quantity < 1 || quantity > 1000`: 허용 범위 이탈 여부 확인

단, `std::cin >> int`는 `12abc`를 입력받았을 때 앞부분인 `12`만 읽고 나머지 문자를 입력 스트림에 남길 수 있습니다. 입력한 문자열 전체를 검증해야 한다면 1.8의 방법을 사용합니다.

## 1.6. 문자열 입력 및 검색

`std::string`은 문자열을 관리하는 표준 라이브러리 타입입니다. 이름이나 문장처럼 공백이 포함된 입력을 처리할 때는 `std::getline()`을 사용할 수 있습니다.

| 입력 방식 | 특징 |
|---|---|
| `std::cin >> name` | 공백 전까지 입력 |
| `std::getline(std::cin, name)` | 공백을 포함한 한 줄 입력 |

[예제 코드 — 04_string_input.cpp](./examples/04_string_input.cpp)

```cpp
#include <iostream>
#include <print>
#include <string>

int main() {
    using std::println;
    using std::string;

    string name;
    std::cout << "Full name: " << std::flush;

    if (!std::getline(std::cin, name) ||
        name.find_first_not_of(" \t\r") == string::npos) {
        std::cerr << "Error: name is required.\n";
        return 1;
    }

    println("Welcome, {}!", name);
    return 0;
}
```

**실행 예시**

```text
Full name: Kim Min Su
Welcome, Kim Min Su!
```

이 예제는 `std::getline()`으로 전체 이름을 읽고, 공백만 입력한 경우를 거부합니다.

- `find_first_not_of(" \t\r")`: 공백·탭·캐리지 리턴 이외의 문자가 있는지 검색
- `string::npos`: 검색 대상 문자가 발견되지 않은 상태

`std::cin >>`으로 입력한 직후 `std::getline()`을 호출하면 입력 스트림에 남아 있는 개행 문자를 먼저 읽을 수 있으므로 주의해야 합니다.

### C++23: `std::string::contains()`

C++23부터는 `contains()`로 문자열에 특정 부분 문자열이 포함되어 있는지 직접 확인할 수 있습니다.

[예제 코드 — 06_string_contains.cpp](./examples/06_string_contains.cpp)

```cpp
#include <print>
#include <string>

int main() {
    using std::println;

    const std::string filename{"monthly_report.csv"};
    if (filename.contains("report")) {
        println("Report file: {}", filename);
    }

    return 0;
}
```

`contains()`는 부분 문자열의 포함 여부를 확인하는 함수입니다. 파일 확장자나 실제 파일 형식을 검증하는 용도로 사용해서는 안 됩니다.

## 1.7. Namespace & Using Declarations

`namespace`는 이름을 논리적으로 구분하는 기능입니다. 예를 들어 `std::string`의 `std`는 C++ 표준 라이브러리에서 사용하는 네임스페이스입니다.

### `using namespace`와 `using` 선언

`using namespace std;`는 `std` 네임스페이스의 이름들을 현재 범위의 이름 탐색에 포함합니다. 코드가 커질수록 이름 충돌이나 모호성이 발생할 수 있으므로, 특히 **헤더 파일과 전역 범위에서 사용하지 않는 것**이 좋습니다.

```cpp
using namespace std;  // 본 자료에서는 사용하지 않음
```

반면 `using std::string;`은 필요한 이름만 현재 범위에 도입합니다. 특정 이름을 반복해서 사용하는 경우에 활용할 수 있습니다.

```cpp
using std::string;
using std::println;
```

또한 `using`을 사용하여 기존 자료형에 별칭을 정의할 수 있습니다. 이는 위의 `using` 선언과는 다른 기능입니다.

```cpp
using UserId = std::uint64_t;
```

- **`using namespace std;`**: 네임스페이스 전체에 대한 using 지시문
- **`using std::string;`**: 지정한 이름을 도입하는 using 선언
- **`using UserId = ...;`**: 자료형에 이름을 부여하는 타입 별칭

### 예제: 주문 정보 출력

[예제 코드 — 07_using_declarations.cpp](./examples/07_using_declarations.cpp)

```cpp
#include <cstdint>
#include <print>
#include <string>

int main() {
    using std::println;
    using std::string;
    using OrderId = std::uint64_t;

    const OrderId order_id{1001};
    const string customer{"Kim Min Su"};

    println("Order #{}: {}", order_id, customer);
    return 0;
}
```

**실행 결과**

```text
Order #1001: Kim Min Su
```

이 예제에서는 `using` 선언으로 필요한 표준 라이브러리 이름만 가져오고, `OrderId`라는 타입 별칭으로 주문 번호의 의미를 표현합니다.

실무에서도 프로젝트 고유의 `namespace`는 이름 충돌을 방지하는 데 사용합니다. 피해야 할 대상은 `namespace` 자체가 아니라 **불필요하게 넓은 범위에서 사용하는 `using namespace` 지시문**입니다. 짧은 이름이 오히려 혼동을 일으킨다면 `std::`를 그대로 명시하는 편이 좋습니다.

## 1.8. 정수 입력의 엄격한 검증

1.5의 예제는 입력 앞부분이 올바른 정수라면 나머지 문자를 남길 수 있습니다. 전체 입력을 검증하려면 문자열 한 줄을 읽은 뒤 숫자로 변환하는 방식을 사용할 수 있습니다.

`std::from_chars()`는 문자열을 숫자로 변환하고, 변환이 끝난 위치와 오류 상태를 반환합니다. C++17에서 도입된 기능으로 C++23에서도 사용할 수 있습니다.

[예제 코드 — 05_strict_integer_input.cpp](./examples/05_strict_integer_input.cpp)

```cpp
#include <charconv>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    std::string input;
    std::cout << "Quantity (1-1000): " << std::flush;

    if (!std::getline(std::cin, input)) {
        std::cerr << "Error: unable to read input.\n";
        return 1;
    }

    int quantity{};
    const char* const end = input.data() + input.size();
    const auto [next, error] = std::from_chars(input.data(), end, quantity);

    if (error != std::errc{} || next != end ||
        quantity < 1 || quantity > 1000) {
        std::cerr << "Error: enter an integer from 1 to 1000.\n";
        return 1;
    }

    std::println("Quantity: {}", quantity);
    return 0;
}
```

**검증 조건**

1. 한 줄 입력 성공 여부 확인
2. `error == std::errc{}` — 정수 변환 성공 여부 확인
3. `next == end` — 입력 전체가 변환에 사용되었는지 확인
4. `quantity`의 `1~1000` 범위 확인

이 예제에서는 `12abc`, `0`, `1001`, 빈 문자열을 거부합니다. `std::from_chars()`는 앞뒤 공백을 자동으로 제거하지 않으므로 ` 12`, `12 `도 거부하며, 선행 `+` 부호도 허용하지 않습니다.

`const auto [next, error]`는 구조적 바인딩이고, `input.data()`는 문자열 내부 데이터의 시작 위치를 가리킵니다. 자세한 문법은 이후 Chapter에서 다룹니다.

## 1.9. Coding Practice

아래 연습문제는 `exercises/`의 미완성 코드를 직접 작성한 후, `solutions/`의 정답 코드와 비교할 수 있도록 구성했습니다.

| 번호 | 실습 | 문제 파일 | 정답 코드 |
|:---:|---|---|---|
| 01 | 이름 입력 및 환영 메시지 출력 | [01_greeting.cpp](./exercises/01_greeting.cpp) | [01_greeting.cpp](./solutions/01_greeting.cpp) |
| 02 | 주문 수량 입력 및 유효성 검증 | [02_order_quantity.cpp](./exercises/02_order_quantity.cpp) | [02_order_quantity.cpp](./solutions/02_order_quantity.cpp) |

### Exercise 01 — Greeting

공백을 포함할 수 있는 이름을 입력받고 환영 메시지를 출력하는 프로그램을 작성합니다.

**구현 조건**

- `std::getline()`으로 이름 한 줄 입력
- 빈 문자열 또는 공백만 있는 입력 거부
- 정상 입력 시 `Hello, <이름>!` 출력

**실행 예시**

```text
입력: Lee Ji Won
출력: Hello, Lee Ji Won!
```

### Exercise 02 — Order Quantity

주문 수량을 입력받고, 값이 유효한지 확인하는 프로그램을 작성합니다.

**구현 조건**

- 정수 수량 `1~1000`만 허용
- `12abc`, `0`, `1001`, `-5`, 빈 입력 거부
- 오류 시 `std::cerr`로 메시지 출력 및 비정상 종료
- 정상 입력 시 `Order quantity: <수량>` 출력

**실행 예시**

```text
입력: 15
출력: Order quantity: 15
```

## 1.10. Summary

- **C++23:** ISO/IEC 14882:2024를 기준으로 하는 C++ 표준
- **빌드 과정:** 소스 코드 → 컴파일 → 링크 → 실행 파일
- **컴파일 옵션:** GCC·Clang의 `-std=c++23` 지정
- **표준 출력:** `std::cout`, C++23의 `std::print()`, `std::println()`
- **오류 출력:** `std::cerr` 사용
- **문자열 입력:** 공백을 포함하는 경우 `std::getline()` 사용
- **`using` 선언:** 필요한 이름만 현재 범위에 도입
- **타입 별칭:** `using 별칭 = 자료형;` 형태로 선언
- **입력 검증:** 입력 성공, 전체 문자열 변환, 허용 범위 확인

## References

- [ISO C++ — The Standard](https://isocpp.org/std/the-standard)
- [C++23 Compiler Support — cppreference](https://en.cppreference.com/w/cpp/compiler_support/23)
- [Using-declaration — cppreference](https://en.cppreference.com/w/cpp/language/using_declaration)
- [MSVC `/std` 옵션 — Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version)

---

[← C++ 목차](../README.md)
