# Chapter 01. Getting Started with C++

C++ 프로그램의 기본 구조를 이해하고, 소스 코드를 직접 컴파일하여 실행하는 방법을 학습합니다. 표준 출력과 입력, 문자열 한 줄 읽기, 오류 출력 등 **첫 번째 콘솔 프로그램을 작성하는 데 필요한 내용**을 다룹니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서도 사용할 수 있는 기본 문법을 중심으로 시작하며, C++23에서 추가된 출력 기능도 간략히 살펴봅니다.

## Contents

| Section | Topic |
|:---:|---|
| [1.1](#section-1-1) | Introduction to C++ — C++와 표준 버전 |
| [1.2](#section-1-2) | Source to Executable — 컴파일과 실행 과정 |
| [1.3](#section-1-3) | Development Environment — 개발 환경 구성 |
| [1.4](#section-1-4) | Hello, C++20! — 첫 번째 프로그램 |
| [1.5](#section-1-5) | Program Structure — 문법과 주석 |
| [1.6](#section-1-6) | Standard Output & Error — 출력 스트림 |
| [1.7](#section-1-7) | Standard Input — 단어 입력 |
| [1.8](#section-1-8) | Line Input — 공백을 포함한 문자열 입력 |
| [1.9](#section-1-9) | Namespaces & Common Errors — 이름 표기와 오류 구분 |
| [1.10](#section-1-10) | Coding Practice |
| [1.11](#section-1-11) | Mini Project — Console Registration Card |
| [1.12](#section-1-12) | Quiz & Summary |

## Getting Started

**준비물:** C++20을 지원하는 컴파일러(GCC, Clang, MSVC 중 하나)와 코드 편집기입니다. VS Code를 사용할 수 있지만, VS Code만 설치해서는 C++ 프로그램을 컴파일할 수 없습니다.

```text
C++ 소스 코드 작성 → 컴파일러로 빌드 → 실행 파일 실행
```

아래 명령어는 **`Chapter-01/` 폴더에서 실행하는 경우**를 기준으로 합니다.

**GCC — Linux, macOS의 GCC 환경, Windows의 GCC 환경**

```bash
g++ --version
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_hello_world.cpp -o hello
./hello
```

Windows PowerShell에서는 `./hello` 대신 `.\hello.exe`로 실행합니다. `g++` 명령어가 인식되지 않는다면 GCC 도구 모음을 설치하고 실행 경로를 설정해야 합니다.

**Clang**

```bash
clang++ --version
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_hello_world.cpp -o hello
./hello
```

**MSVC — Visual Studio Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /utf-8 examples\01_hello_world.cpp /Fe:hello.exe
hello.exe
```

**학습 목표**

1. 소스 코드, 컴파일, 링크, 실행 파일의 관계를 설명할 수 있습니다.
2. `main()`을 포함한 최소 C++ 프로그램을 작성하고 실행할 수 있습니다.
3. `std::cout`과 `std::cerr`의 용도를 구분할 수 있습니다.
4. `std::cin >>`과 `std::getline()`의 입력 범위 차이를 설명할 수 있습니다.
5. 배운 입출력 기능을 이용해 간단한 콘솔 프로그램을 직접 작성할 수 있습니다.

---

<a id="section-1-1"></a>
## 1.1. Introduction to C++ — C++와 표준 버전

C++은 **소스 코드를 컴파일하여 실행하는 방식**으로 널리 사용하는 프로그래밍 언어입니다. 운영체제용 프로그램, 게임 엔진, 임베디드 장치, 성능이 중요한 소프트웨어 등 다양한 분야에서 사용합니다.

C++ 문법과 표준 라이브러리는 지속적으로 개정됩니다. 기본 예제와 실습은 C++20을 기준으로 작성했습니다.

| 표준 | 적용 범위 |
|---|---|
| C++17 | 기존 코드와 호환되는 기본 문법 및 주요 기능 이해 |
| **C++20** | **기본 예제·연습문제·프로젝트의 컴파일 기준** |
| C++23 | 새로운 기능 중 관련성이 높은 내용을 간략히 소개 |

새 표준을 지정한다고 해서 프로그램이 자동으로 더 빨라지는 것은 아닙니다. 표준 옵션은 **어떤 언어 규칙과 기능을 사용할 수 있는지** 결정합니다. 실제 지원 범위는 설치된 컴파일러와 표준 라이브러리에 따라 달라집니다.

---

<a id="section-1-2"></a>
## 1.2. Source to Executable — 컴파일과 실행 과정

텍스트 편집기로 작성한 `.cpp` 파일은 C++ 소스 코드입니다. 실행하려면 보통 다음 과정을 거칩니다.

```text
소스 코드(.cpp)
    ↓
전처리(헤더 포함 등)
    ↓
컴파일(목적 파일 생성)
    ↓
링크(필요한 코드 연결)
    ↓
실행 파일
    ↓
프로그램 실행
```

| 단계 | 역할 |
|---|---|
| 전처리(Preprocessing) | `#include` 등의 지시문을 처리합니다. |
| 컴파일(Compilation) | C++ 코드를 검사하고 목적 파일로 변환합니다. |
| 링크(Linking) | 목적 파일과 필요한 라이브러리 코드를 연결합니다. |
| 실행(Execution) | 운영체제가 실행 파일을 실행합니다. |

`g++` 또는 `clang++`의 빌드 명령어는 일반적으로 **컴파일과 링크를 함께 수행**합니다.

```bash
g++ -std=c++20 examples/01_hello_world.cpp -o hello
```

이 명령어를 실행하면 Linux/macOS에서는 일반적으로 `hello`, Windows에서는 `hello.exe`가 생성됩니다. 빌드가 성공해도 **프로그램이 자동 실행되지는 않으므로** 실행 명령어를 별도로 입력해야 합니다.

**세 가지 실패 상황**

| 종류 | 예시 | 의미 |
|---|---|---|
| 컴파일 오류 | 세미콜론 누락, 이름 오타 | 소스 코드를 올바르게 번역하지 못한 상태 |
| 링크 오류 | 필요한 함수의 정의를 연결하지 못함 | 실행 파일을 완성하지 못한 상태 |
| 실행 중 오류 | 프로그램이 실행 도중 비정상 종료 | 실행 파일은 생성되었지만 실행 과정에서 문제 발생 |

실행 결과가 예상과 다른 **논리 오류**도 있습니다. 논리 오류는 컴파일이 성공하더라도 발생할 수 있습니다.

---

<a id="section-1-3"></a>
## 1.3. Development Environment — 개발 환경 구성

C++ 프로그래밍 환경은 **편집기, 컴파일러, 터미널**로 나누어 이해하면 쉽습니다.

| 도구 | 역할 |
|---|---|
| VS Code 등 코드 편집기 | `.cpp` 파일 작성 및 수정 |
| GCC, Clang, MSVC | 소스 코드를 컴파일하고 링크 |
| 터미널 | 컴파일 명령어 입력 및 실행 파일 실행 |

VS Code에서는 `Chapter-01/` 폴더를 열고 **Terminal → New Terminal**을 선택하면 됩니다. Windows에서는 설치한 컴파일러에 맞는 터미널을 사용해야 합니다. MSVC는 보통 Developer Command Prompt 환경에서 실행합니다.

**GCC/Clang 컴파일 옵션**

| 옵션 | 의미 |
|---|---|
| `-std=c++20` | C++20 표준 모드를 지정합니다. |
| `-Wall` | 주요 경고를 표시합니다. |
| `-Wextra` | 추가 경고를 표시합니다. |
| `-Wpedantic` | 비표준 확장 관련 경고를 표시합니다. |
| `-o hello` | 생성할 실행 파일 이름을 지정합니다. |

처음에는 한 파일씩 빌드하고, 여러 파일을 함께 빌드하는 방법은 후속 Chapter에서 다룹니다.

**컴파일 확인**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/02_program_structure.cpp -o structure
./structure
```

**실행 결과**

```text
Source code
Executable program
```

---

<a id="section-1-4"></a>
## 1.4. Hello, C++20! — 첫 번째 프로그램

**예제 코드 — [01_hello_world.cpp](./examples/01_hello_world.cpp)**

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, C++20!\n";
    return 0;
}
```

**실행 결과**

```text
Hello, C++20!
```

| 코드 | 설명 |
|---|---|
| `#include <iostream>` | 화면 출력 등 기본 입출력 기능을 사용하기 위한 헤더를 포함합니다. |
| `int main()` | 프로그램 실행이 시작되는 진입 함수입니다. |
| `{`와 `}` | 함수에 속한 코드의 범위를 표시합니다. |
| `std::cout` | 표준 출력(stdout)에 데이터를 보냅니다. |
| `<<` | 오른쪽의 값을 출력 스트림에 전달하는 연산자입니다. |
| `"Hello, C++20!\n"` | 출력할 문자열과 줄바꿈(`\n`)입니다. |
| `return 0;` | 프로그램이 정상적으로 종료되었음을 알립니다. |

`main()`의 `int`는 종료 상태를 정수로 전달한다는 의미입니다. `main()` 끝의 `return 0;`은 생략할 수 있지만, 여기서는 정상 종료를 명확하게 나타내기 위해 작성했습니다.

`#include` 줄에는 세미콜론을 붙이지 않습니다. 반면 `std::cout ...;`과 `return 0;`처럼 이번 예제의 실행 문장에는 세미콜론이 필요합니다.

---

<a id="section-1-5"></a>
## 1.5. Program Structure — 문법과 주석

C++ 코드는 **대문자와 소문자를 구별**합니다. 예를 들어 `main`과 `Main`은 서로 다른 이름입니다.

**문자열과 줄바꿈**

```cpp
std::cout << "First line\n";
std::cout << "Second line\n";
```

위 코드는 다음 두 줄을 출력합니다.

```text
First line
Second line
```

`\n`은 줄바꿈을 나타내는 특수 문자입니다. `"\n"`처럼 큰따옴표로 둘러싼 값은 문자열 리터럴(string literal)이고, `'\n'`처럼 작은따옴표로 둘러싼 값은 문자 리터럴(character literal, `char`)입니다.

**주석(Comment)**은 소스 코드에 설명을 남기는 문법이며 프로그램의 출력에는 표시되지 않습니다.

**예제 코드 — [02_program_structure.cpp](./examples/02_program_structure.cpp)**

```cpp
#include <iostream>

int main() {
    // 한 줄 주석: 화면에 표시되지 않습니다.
    std::cout << "Source code\n";

    /* 여러 줄 주석도
       작성할 수 있습니다. */
    std::cout << "Executable program\n";
    return 0;
}
```

**실행 결과**

```text
Source code
Executable program
```

소스 코드를 읽기 쉽게 들여쓰기하고, 한 줄에는 한 가지 작업을 작성하는 습관을 권장합니다.

---

<a id="section-1-6"></a>
## 1.6. Standard Output & Error — 출력 스트림

콘솔 프로그램은 일반 결과와 오류·진단 메시지를 서로 다른 통로로 출력할 수 있습니다. 이 통로를 **스트림(Stream)**이라고 부릅니다.

| 코드 | 통로 | 주로 사용하는 목적 |
|---|---|---|
| `std::cout` | 표준 출력(stdout) | 정상 결과, 일반 안내 |
| `std::cerr` | 표준 오류(stderr) | 오류, 경고, 진단 메시지 |

**예제 코드 — [03_output_streams.cpp](./examples/03_output_streams.cpp)**

```cpp
#include <iostream>

int main() {
    std::cout << "Result: success\n";
    std::cerr << "Notice: demonstration message\n";
    return 0;
}
```

**출력 내용**

| 통로 | 출력 내용 |
|---|---|
| stdout | `Result: success` |
| stderr | `Notice: demonstration message` |

터미널에서는 두 메시지가 함께 보일 수 있습니다. **서로 다른 스트림의 메시지가 화면에 섞여 표시되는 순서는 환경에 따라 달라질 수 있습니다.** 따라서 순서에 의존하지 않고 통로 자체를 구분해야 합니다.

`<<`를 이어 쓰면 여러 값을 한 문장으로 출력할 수 있습니다.

```cpp
std::cout << "Language: " << "C++" << '\n';
```

**실행 결과**

```text
Language: C++
```

`std::endl`도 줄바꿈을 수행하지만 출력 버퍼를 비우는 동작(flush)을 추가로 수행합니다. 일반적인 줄바꿈에는 `\n`을 사용하면 됩니다.

---

<a id="section-1-7"></a>
## 1.7. Standard Input — 단어 입력

`std::cin`은 사용자 입력을 읽는 표준 입력 스트림입니다. `>>` 연산자를 이용하면 **공백으로 구분되는 값**을 읽을 수 있습니다.

입력한 글자는 `std::string`에 저장할 수 있습니다. `std::string keyword;`는 `keyword`라는 이름의 문자열 변수를 선언하는 코드입니다.

**예제 코드 — [04_token_input.cpp](./examples/04_token_input.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    std::string keyword;

    std::cout << "Keyword: ";
    std::cin >> keyword;
    std::cout << "First token: " << keyword << '\n';
    return 0;
}
```

**실행 예시**

```text
Keyword: robotics basics
First token: robotics
```

- `#include <string>`: `std::string` 타입을 사용하기 위한 헤더입니다.
- `std::cin >> keyword;`: 입력에서 공백 전까지 한 단어를 읽습니다.
- `std::cout << keyword;`: 읽은 값을 출력합니다.

`robotics basics`를 입력하면 **`robotics`까지만** 읽습니다. 공백까지 포함한 문장을 읽으려면 다음 Section의 `std::getline()`을 사용합니다.

여기서는 정상적인 문자열 입력을 가정합니다.

---

<a id="section-1-8"></a>
## 1.8. Line Input — 공백을 포함한 문자열 입력

이름이나 문장처럼 공백이 있는 입력은 `std::getline()`이 적합합니다. `std::getline(std::cin, 변수)`는 **줄바꿈을 만날 때까지 한 줄을 읽고**, 줄바꿈 문자 자체는 문자열에 저장하지 않습니다.

**예제 코드 — [05_line_input.cpp](./examples/05_line_input.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    std::string full_name;

    std::cout << "Full name: ";
    std::getline(std::cin, full_name);
    std::cout << "Hello, " << full_name << "!\n";
    return 0;
}
```

**실행 예시**

```text
Full name: Kim Min Su
Hello, Kim Min Su!
```

| 방식 | 입력값 `Kim Min Su` 처리 |
|---|---|
| `std::cin >> name` | `Kim`만 읽습니다. |
| `std::getline(std::cin, name)` | `Kim Min Su` 전체를 읽습니다. |

**예제 코드 — [06_two_lines.cpp](./examples/06_two_lines.cpp)**

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name;
    std::string interest;

    std::cout << "Name: ";
    std::getline(std::cin, name);
    std::cout << "Interest: ";
    std::getline(std::cin, interest);

    std::cout << "Profile: " << name << " | " << interest << '\n';
    return 0;
}
```

**실행 예시**

```text
Name: Kim Min Su
Interest: Robotics Club
Profile: Kim Min Su | Robotics Club
```

`std::cin >>`으로 값을 읽은 **직후** `std::getline()`을 호출하면, 입력 스트림에 남아 있는 줄바꿈 문자 때문에 빈 줄을 읽을 수 있습니다. 두 입력 방식을 함께 사용할 때는 이 차이를 고려해야 합니다.

---

<a id="section-1-9"></a>
## 1.9. Namespaces & Common Errors — 이름 표기와 오류 구분

`std::cout`, `std::cin`, `std::string` 앞의 `std::`는 이름이 **C++ 표준 라이브러리의 `std` 네임스페이스에 속한다**는 의미입니다.

```cpp
std::cout << "Ready\n";
```

권장하는 코딩 스타일은 **`std::`를 명시하는 방식**입니다. 필요한 이름만 가져오는 `using std::cout;`과 같은 개별 선언은 사용할 수 있지만, 이름 충돌 가능성을 높이는 `using namespace std;` 지시문은 사용하지 않습니다.

**입문자가 자주 만나는 문제**

| 상황 | 원인 또는 확인할 사항 |
|---|---|
| `g++` 명령어를 찾지 못함 | 컴파일러가 설치되지 않았거나 실행 경로가 설정되지 않음 |
| `iostream`을 찾지 못함 | C++ 개발 도구 또는 헤더 검색 경로 문제 |
| `expected ';'` 오류 | 문장 끝의 세미콜론 누락 가능성 |
| `'cout' is not a member of 'std'` | `<iostream>` 포함 여부, 이름의 철자 확인 |
| 실행 파일이 만들어지지 않음 | 컴파일·링크 오류가 먼저 발생했는지 확인 |
| 코드 변경이 실행 결과에 반영되지 않음 | 소스를 수정한 뒤 다시 빌드했는지 확인 |

오류 메시지는 **첫 번째 오류부터** 확인하는 것이 좋습니다. 앞부분의 문법 오류 하나로 뒤에 여러 오류가 연쇄적으로 표시될 수 있습니다.

**기존 코드와 C++23 간단 비교**

| 표준 | 출력 예시 | 비고 |
|---|---|---|
| C++17·20 | `std::cout << "Hello\n";` | `<iostream>` 헤더 사용 |
| C++23 | `std::println("Hello");` | `<print>` 헤더 및 지원 환경 필요 |

C++23의 `std::println()`은 `<print>` 헤더에서 제공하는 출력 기능입니다. 사용 가능 여부는 컴파일러와 표준 라이브러리의 지원 수준에 따라 달라집니다.

---

<a id="section-1-10"></a>
## 1.10. Coding Practice

`exercises/`에는 미완성 코드가, `solutions/`에는 모범답안이 제공됩니다. 먼저 문제를 읽고 직접 구현한 다음 결과를 비교합니다.

| No. | 문제 | 미완성 코드 | 모범답안 |
|:---:|---|---|---|
| 01 | Console Banner — 여러 줄 출력 | [문제](./exercises/01_console_banner.cpp) | [정답](./solutions/01_console_banner.cpp) |
| 02 | Output Channels — 출력 스트림 구분 | [문제](./exercises/02_output_channels.cpp) | [정답](./solutions/02_output_channels.cpp) |
| 03 | Keyword Echo — 한 단어 입력 | [문제](./exercises/03_keyword_echo.cpp) | [정답](./solutions/03_keyword_echo.cpp) |
| 04 | Full Name — 한 줄 입력 | [문제](./exercises/04_full_name.cpp) | [정답](./solutions/04_full_name.cpp) |

### Exercise 01 — Console Banner

**목표:** `std::cout`으로 여러 줄의 안내 문구를 출력합니다.

**요구사항:** 다음 문장을 **두 줄로**, 줄 끝에 개행을 포함해 출력합니다.

```text
Hello, C++20!
Ready to learn.
```

별도의 사용자 입력은 없습니다.

### Exercise 02 — Output Channels

**목표:** 일반 출력과 진단 메시지를 구분합니다.

**요구사항:** 아래 두 메시지를 각각 지정한 스트림에 출력합니다.

| 스트림 | 메시지 |
|---|---|
| stdout | `Status: running` |
| stderr | `Notice: check log` |

각 메시지 끝에는 개행을 추가합니다. 프로그램은 정상 종료합니다.

### Exercise 03 — Keyword Echo

**목표:** `std::cin >>`을 사용해 첫 번째 단어를 읽습니다.

**요구사항:** `Keyword: `를 출력하고 한 단어를 입력받아 `You typed: <단어>` 형식으로 출력합니다.

**입력·출력 예시**

```text
Keyword: network security
You typed: network
```

공백 이후의 입력은 처리하지 않습니다. 정상적인 문자열 입력이 주어진다고 가정합니다.

### Exercise 04 — Full Name

**목표:** `std::getline()`으로 공백을 포함한 이름을 입력받습니다.

**요구사항:** `Full name: `을 출력하고 이름 한 줄을 읽어 `Welcome, <이름>!` 형식으로 출력합니다.

**입력·출력 예시**

```text
Full name: Park Ji Min
Welcome, Park Ji Min!
```

공백을 포함한 이름이 잘리지 않아야 합니다. 정상적인 문자열 입력이 주어진다고 가정합니다.

### 실행과 확인

**예: Exercise 04 컴파일·실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/04_full_name.cpp -o greeting
./greeting
```

실습 코드의 TODO를 채워 직접 완성합니다. 모범답안을 확인하려면 `solutions/`의 동일한 번호 파일을 열어 비교합니다.

**선택: 자동 검증**

Python 3과 GCC가 설치되어 있다면 다음 명령어로 자동 검증을 실행할 수 있습니다.

```bash
python tests/check.py
python tests/check.py --mode student --only exercise-04
```

**첫 번째 명령어**는 예제와 모범답안을 확인하는 용도입니다. **두 번째 명령어**는 직접 수정한 Exercise 04를 검사합니다. 아직 코드가 작성되지 않은 초기 상태에는 FAIL이 나오는 것이 정상입니다. 테스트 실행기(Test Runner)는 소스 코드를 C++20으로 컴파일한 뒤 다양한 입력값을 전달하여 출력 결과와 종료 상태가 예상과 일치하는지 자동으로 검증합니다.

---

<a id="section-1-11"></a>
## 1.11. Mini Project — Console Registration Card

### 프로젝트 목표

한 명의 학생에게 **이름, 수강 과정, 학습 목표**를 차례로 입력받고, 입력한 내용을 등록 카드 형식으로 출력하는 콘솔 프로그램을 작성합니다.

입력 안내에는 `std::cout`을, 문자열 입력에는 `std::getline()`을 사용합니다.

**제공 파일**

- [프로젝트 시작 코드 — registration_card.cpp](./project/registration_card.cpp)
- [프로젝트 모범답안 — registration_card.cpp](./solutions/registration_card.cpp)

### 구현 요구사항

1. 문자열 3개에 각각 학생 이름(`name`), 과정명(`course`), 학습 목표(`goal`)를 저장합니다.
2. `Name: `, `Course: `, `Goal: `을 순서대로 출력하고 **각각 한 줄씩** 입력받습니다.
3. 세 입력값에는 공백이 포함될 수 있으므로 `std::getline()`을 사용합니다.
4. 빈 줄을 하나 출력한 다음 `--- Registration Card ---`를 출력합니다.
5. 이름·과정·목표를 다음 예시와 같은 순서로 출력합니다. 마지막 줄에도 개행을 포함합니다.

**입력·출력 예시**

```text
Name: Kim Min Su
Course: C++ Basics
Goal: Read source code

--- Registration Card ---
Name: Kim Min Su
Course: C++ Basics
Goal: Read source code
```

**완료 기준**

- **공백 데이터 처리:** 이름이나 과정명에 공백(띄어쓰기)이 포함되어도 전체 문자열이 잘리지 않고 입력되어야 합니다.
- **입출력 순서 보존:** 이름·과정·학습 목표를 요구된 순서대로 입력받고, 등록 카드의 각 항목도 지정된 순서대로 출력해야 합니다.
- **입력값 변경 반영:** 입력값을 변경하여 다시 실행하면 등록 카드에 새로운 값이 정확히 반영되어야 합니다.
- **빌드 정합성:** `g++ -std=c++20` 옵션으로 오류 없이 컴파일되어야 합니다.

해당 프로젝트는 **정상 형식의 세 줄 입력**을 전제로 합니다. 빈 값 예외 처리나 복잡한 유효성 검증(Validation)은 구현 대상에 포함하지 않습니다.

**프로젝트 실행**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/registration_card.cpp -o registration
./registration
```

**선택: 자동 검증**

```bash
python tests/check.py --mode student --only project
```

---

<a id="section-1-12"></a>
## 1.12. Quiz & Summary

### Quiz

각 문제의 답을 먼저 생각한 뒤 **정답 및 해설**을 펼쳐 확인하세요.

**Q1. C++ 소스 코드를 실행 파일로 만드는 과정에서 링크(Linking)의 역할로 가장 적절한 것은 무엇인가요?**

- A. 소스 코드의 들여쓰기를 자동으로 수정합니다.
- B. 목적 파일과 필요한 코드를 연결합니다.
- C. 실행 중인 프로그램의 입력을 받습니다.
- D. 화면에 문자열을 출력합니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

컴파일 과정에서 생성된 목적 파일과 필요한 코드의 정의를 연결하여 실행 파일을 구성하는 작업이 링크입니다. 문법 검사와 코드 번역은 컴파일 단계에서 수행하며, 입력과 출력은 프로그램 실행 단계의 동작입니다.

</details>

**Q2. C++20 표준 모드를 명시하는 GCC 옵션은 무엇인가요?**

- A. `-std=c++17`
- B. `-std=c++20`
- C. `-std=c++23`
- D. `-o c++20`

<details>
<summary>정답 및 해설</summary>

**정답: B**

`-std=c++20`은 C++20 표준 모드를 지정합니다. `-o`는 언어 표준이 아니라 출력 파일 이름을 지정하는 옵션입니다.

</details>

**Q3. C++ 프로그램에서 `int main()`은 어떤 역할을 하나요?**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** 프로그램 실행이 시작되는 진입 함수입니다.

`main()`은 프로그램의 진입점입니다. `int`는 종료 상태를 정수로 전달한다는 의미이며, `return 0;`은 정상 종료를 나타냅니다.

</details>

**Q4. 다음 중 일반적인 오류·진단 메시지를 보내는 출력 스트림은 무엇인가요?**

- A. `std::cout`
- B. `std::cin`
- C. `std::cerr`
- D. `std::string`

<details>
<summary>정답 및 해설</summary>

**정답: C**

`std::cerr`는 표준 오류(stderr) 스트림입니다. `std::cout`은 일반 출력, `std::cin`은 표준 입력에 사용합니다. `std::string`은 문자열을 저장하는 타입입니다.

</details>

**Q5. 아래 코드의 출력 결과를 작성하세요.**

```cpp
std::cout << "A\n";
std::cout << "B\n";
```

<details>
<summary>정답 및 해설</summary>

**정답:**

```text
A
B
```

`\n`은 줄바꿈을 의미합니다. 따라서 `A`를 출력한 뒤 줄을 바꾸고 다음 줄에 `B`를 출력합니다.

</details>

**Q6. 입력 `Kim Min Su`를 공백까지 포함해 한 줄로 읽는 방법은 무엇인가요?**

- A. `std::cin >> name;`
- B. `std::getline(std::cin, name);`
- C. `std::cout << name;`
- D. `return 0;`

<details>
<summary>정답 및 해설</summary>

**정답: B**

`std::getline()`은 줄바꿈 전까지의 글자를 한 줄로 읽습니다. `std::cin >> name`은 기본적으로 공백 전까지 읽으므로 `Kim`만 저장합니다. 반면 `std::cout << name;`은 입력이 아니라 출력에 사용하며, `return 0;`은 `main()`에서 정상 종료 상태를 반환할 때 사용합니다.

</details>

**Q7. `#include <string>`이 필요한 이유를 설명하세요.**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** `std::string`과 같은 문자열 관련 표준 라이브러리 기능을 사용하기 위해 필요한 헤더를 포함합니다.

헤더는 필요한 기능의 선언을 제공합니다. `#include`는 전처리 지시문이므로 끝에 세미콜론을 붙이지 않습니다.

</details>

**Q8. 다음 코드에서 `std::`의 의미로 가장 적절한 것은 무엇인가요?**

```cpp
std::cout << "Ready\n";
```

- A. 프로그램을 종료하는 명령어입니다.
- B. 출력 내용을 저장하는 파일 이름입니다.
- C. `cout`이 `std` 네임스페이스에 속한다는 표시입니다.
- D. 새로운 자료형을 정의하는 문법입니다.

<details>
<summary>정답 및 해설</summary>

**정답: C**

`std::`는 이름의 소속을 명시합니다. 표준 라이브러리 이름 앞에 `std::`를 작성하면 해당 이름이 어디에서 정의되었는지 분명하게 나타낼 수 있습니다.

**오답 해설**

- **A:** 프로그램을 종료하려면 `main()`에서 `return 0;`과 같이 종료 상태를 반환할 수 있습니다. `std::`는 프로그램을 종료하는 명령어가 아닙니다.
- **B:** `g++` 컴파일 명령어의 `-o hello`처럼 `-o` 옵션으로 출력 실행 파일의 이름을 지정할 수 있습니다. `std::`는 파일 이름이 아닙니다.
- **D:** `struct`나 `class` 등으로 새로운 자료형을 정의할 수 있습니다. `std::`는 자료형을 정의하는 문법이 아닙니다.

</details>

**Q9. `std::cin >> name` 다음에 바로 `std::getline(std::cin, sentence)`을 사용했을 때 빈 줄이 읽힐 수 있는 이유는 무엇인가요?**

<details>
<summary>정답 및 해설</summary>

**예시 답안:** `std::cin >>`이 입력 뒤의 줄바꿈 문자를 남길 수 있고, 이어서 실행된 `std::getline()`이 그 줄바꿈을 먼저 읽기 때문입니다.

두 입력 방식은 공백과 줄바꿈을 처리하는 규칙이 다르므로 함께 사용할 때 주의해야 합니다.

</details>

**Q10. C++20 환경의 기본 예제로 가장 적절한 것은 무엇인가요?**

- A. `<print>`의 `std::println()`을 필수로 사용합니다.
- B. `<iostream>`의 `std::cout`을 사용합니다.
- C. C++23 전용 문법만 사용합니다.
- D. 표준 옵션은 항상 `-std=c++23`으로 지정합니다.

<details>
<summary>정답 및 해설</summary>

**정답: B**

`std::cout`은 C++20에서 사용할 수 있는 표준 출력 기능입니다. `std::println()`은 C++23에서 추가되었으므로 C++20 기본 예제의 필수 기능으로 사용하지 않습니다.

</details>

### Summary

- **C++20:** 기본 예제·실습의 컴파일 기준
- **소스 코드:** 개발자가 작성하는 `.cpp` 텍스트 파일
- **컴파일·링크:** 소스 코드를 목적 파일로 만들고 필요한 코드를 연결해 실행 파일 생성
- **`main()`:** C++ 프로그램의 실행 시작점
- **`#include`:** 필요한 헤더를 포함하는 전처리 지시문
- **`std::cout`:** 표준 출력(stdout)
- **`std::cerr`:** 표준 오류(stderr)
- **`std::cin >>`:** 공백으로 구분되는 입력 읽기
- **`std::getline()`:** 공백을 포함해 한 줄 읽기
- **`std::string`:** 문자열을 보관하는 표준 라이브러리 타입
- **`std::`:** 표준 라이브러리 이름의 네임스페이스를 명시

### References

- [ISO C++ — The Standard](https://isocpp.org/std/the-standard)
- [C++ Compiler Support — cppreference](https://en.cppreference.com/w/cpp/compiler_support)
- [GCC — C++ Dialect Options](https://gcc.gnu.org/onlinedocs/gcc/C-Dialect-Options.html)
- [Microsoft Learn — `/std` option](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version)
- [cppreference — `std::getline`](https://en.cppreference.com/w/cpp/string/basic_string/getline)
- [Visual Studio Code — C++](https://code.visualstudio.com/docs/languages/cpp)

---

[← C++ 목차](../README.md)
