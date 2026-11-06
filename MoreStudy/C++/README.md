# C++

C++ 프로그래밍의 기본 문법부터 표준 라이브러리와 객체지향 프로그래밍까지 다루는 학습 자료.

- **기준 표준:** C++23 (ISO/IEC 14882:2024)
- **개발 환경:** GCC, Clang, MSVC
- **예제 구성:** 개념 설명, 실행 코드, 연습문제, 정답 코드

## Chapters

| Chapter | Topic | 상태 |
|:---:|---|:---:|
| [01](./Chapter-01/) | Getting Started — 컴파일, 기본 구조, 입출력, 문자열, 입력 검증 | 작성 완료 |
| 02 | Variables & Data Types | 예정 |
| 03 | Operators & Conditions | 예정 |
| 04 | Loops | 예정 |
| 05 | Functions | 예정 |
| 06 | Arrays & Strings | 예정 |
| 07 | Pointers & References | 예정 |
| 08 | Structs & Classes | 예정 |
| 09 | Object-Oriented Programming | 예정 |
| 10 | Standard Library (STL) | 예정 |
| 11 | File I/O | 예정 |


## Getting Started

[Chapter 01](./Chapter-01/)의 예제는 `Chapter-01/` 디렉터리를 기준으로 실행.

**GCC**

```bash
cd Chapter-01
g++ -std=c++23 -Wall -Wextra -Wpedantic examples/01_hello_world.cpp -o hello
./hello
```

Windows에서 GCC를 사용하는 경우 생성된 `hello.exe`를 `./hello.exe` 또는 PowerShell의 `.\hello.exe`로 실행.

**Clang**

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic examples/01_hello_world.cpp -o hello
./hello
```

**MSVC** — Visual Studio Developer Command Prompt

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 examples\01_hello_world.cpp /Fe:hello.exe
hello.exe
```

MSVC의 C++23 옵션은 설치 버전에 따라 다름. 최근 MSVC 14.52 시험판부터 `/std:c++23`을 지원하며, 이전 지원 버전에서는 `/std:c++23preview`를 사용함. 표준 라이브러리 기능의 지원 범위는 컴파일러 버전에 따라 달라질 수 있음.

## Code Guidelines

- C++23을 기준으로 예제 작성.
- 표준 라이브러리 이름은 `std::`를 명시하여 사용.
- 주요 컴파일러 경고를 활성화하고 입력 오류를 검사함.
- `std::println`, `std::string::contains` 등 C++23 기능은 지원 환경을 확인하여 사용.
- 짧은 개념 확인은 `examples/`, 직접 풀이할 문제는 `exercises/`, 정답은 `solutions/`에서 확인 가능.

## References

- [ISO/IEC 14882:2024 — C++](https://www.iso.org/standard/83626.html)
- [C++ Standard — ISO C++](https://isocpp.org/std/the-standard)
- [C++23 Compiler Support — cppreference](https://en.cppreference.com/w/cpp/compiler_support/23)
- [GCC C++ Status](https://gcc.gnu.org/projects/cxx-status.html)
- [Clang C++ Status](https://clang.llvm.org/cxx_status.html)
- [MSVC `/std` 옵션](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version)

---

[← MoreStudy](../README.md)
