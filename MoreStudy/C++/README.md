<p align="center">
  <img src="banner_Cpp.png" width="60%" alt="C++ Class Banner">
</p>

C++20을 기준으로 기본 문법부터 객체지향 프로그래밍, 표준 라이브러리, 자원 관리 및 제네릭 프로그래밍까지 학습하는 자료입니다. 각 Chapter에서 개념 설명과 실행 예제, 연습문제 및 모범답안을 확인할 수 있습니다. 이후 동시성, 성능 최적화, 빌드 시스템, 테스트, 네트워크 프로그래밍으로 학습 범위를 확장합니다.

- **기준 표준:** C++20 (ISO/IEC 14882:2020)
- **개발 환경:** GCC, Clang, MSVC
- **자료 구성:** 학습 문서, 실행 예제, 연습문제, 정답 코드, 검증 자료

## Contents

### Part 1 — C++ Fundamentals

C++의 기본 문법과 주요 언어 기능을 학습하는 과정입니다.

| Chapter | Topic |
|:---:|---|
| [01](./Chapter-01/) | Getting Started — 컴파일, 입출력, 문자열, 네임스페이스, 입력 검증 |
| [02](./Chapter-02/) | Variables & Data Types — 변수, 자료형, 상수, 형변환, 열거형 |
| [03](./Chapter-03/) | Operators & Conditions — 연산자, 조건문, 장치 상태 판단 |
| [04](./Chapter-04/) | Loops — 반복문, 센서 샘플링, 재시도 |
| [05](./Chapter-05/) | Functions — 함수 설계, 반환값, 람다, 파일 분리 |
| [06](./Chapter-06/) | Arrays & Strings — 배열, 문자열, View, 입력 및 Parsing |
| [07](./Chapter-07/) | Pointers & References — 포인터, 참조, Ownership, 객체 수명 |
| [08](./Chapter-08/) | Structs & Classes — 구조체, 클래스, 생성자, Composition |
| [09](./Chapter-09/) | Object-Oriented Programming — 상속, 다형성, Interface 설계 |
| [10](./Chapter-10/) | Standard Library (STL) — Container, Iterator, Algorithm, Ranges |
| [11](./Chapter-11/) | File I/O — 파일 입출력, 경로 관리, CSV·Binary 데이터 |

**Part 1 종합 복습:** [Summary — Part 01](./Summary-Part-01/) — Quiz 및 코드 문제

### Part 2 — Advanced C++ & Systems Programming

고급 C++ 기능과 시스템 프로그래밍을 학습하는 과정입니다.

| Chapter | Topic |
|:---:|---|
| [12](./Chapter-12/) | Modern C++ & Resource Management — Move Semantics, RAII, Exception Safety |
| [13](./Chapter-13/) | Templates & Generic Programming — Template, Concepts, Generic Design |
| 14 | Concurrency & Multithreading — Thread, Synchronization, Atomic Operation |
| 15 | Memory & Performance Optimization — 메모리 구조, 프로파일링, 최적화 |
| 16 | CMake, Libraries & Project Structure — 빌드 구성, 라이브러리, 프로젝트 관리 |
| 17 | Testing, Debugging & Profiling — 자동화 테스트, 디버깅, 성능 측정 |
| 18 | Networking & Interprocess Communication — Socket, IPC, 데이터 통신 |

## Getting Started

다음 명령어는 `C++/` 폴더를 기준으로 작성되었습니다. GCC, Clang, MSVC 중 설치된 컴파일러에 해당하는 명령어를 사용합니다.

**GCC**

```bash
cd Chapter-01
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_hello_world.cpp -o hello
./hello
```

**Clang**

```bash
cd Chapter-01
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_hello_world.cpp -o hello
./hello
```

**MSVC — Developer Command Prompt**

```bat
cd Chapter-01
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_hello_world.cpp /Fe:hello.exe
hello.exe
```

각 명령어 블록은 `C++/` 폴더에서 별도로 시작하는 기준입니다. Windows PowerShell에서는 생성된 실행 파일을 `./hello.exe` 또는 `.\hello.exe`로 실행할 수 있습니다. VS Code에서 빌드·실행 환경을 설정하는 방법은 [Chapter 01](./Chapter-01/)에서 안내합니다.

## Code Guidelines

- 예제와 연습문제는 **C++20**을 기준으로 작성합니다.
- 표준 라이브러리의 이름은 기본적으로 `std::`를 명시합니다. `using namespace ...;` 지시문은 사용하지 않습니다.
- 타입 별칭이 필요할 때는 `using Alias = Type;` 형태를 사용할 수 있습니다.
- 입력 실패와 범위 초과 등 주요 오류 상황을 처리하고, 컴파일러 경고 옵션을 활성화합니다.
- 실행 예제는 `examples/`, 학생용 실습은 `exercises/`, 모범답안은 `solutions/`에 구분하여 제공합니다.
- 해당 Chapter에 검증 스크립트가 있는 경우 `tests/`에서 테스트할 수 있습니다.

## References

- [ISO/IEC 14882:2020 — Programming languages — C++](https://webstore.iec.ch/en/publication/68285)
- [ISO C++ — The Standard](https://isocpp.org/std/the-standard)
- [C++20 Compiler Support — cppreference](https://en.cppreference.com/cpp/compiler_support/20)
- [MSVC `/std` 옵션 — Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version)

---

[← MoreStudy](../README.md)
