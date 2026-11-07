<p align="center">
  <img src="banner_Cpp.png" width="60%" alt="C++ Class Banner">
</p>

C++23을 기준으로 기본 문법부터 표준 라이브러리, 객체지향 프로그래밍까지 정리한 학습 자료입니다. 각 Chapter에서 개념 설명과 예제 코드를 확인하고, 연습문제를 직접 실행해 볼 수 있습니다.

- **기준 표준:** C++23 (ISO/IEC 14882:2024)
- **개발 환경:** GCC, Clang, MSVC
- **자료 구성:** 학습 문서, 실행 예제, 연습문제, 정답 코드

## Chapters

| Chapter | Topic |
|:---:|---|
| [01](./Chapter-01/) | Getting Started — 컴파일, 입출력, 문자열, `using`, 입력 검증 |
| [02](./Chapter-02/) | Variables & Data Types — 변수, 자료형, 상수, 형변환, 열거형 |
| [03](./Chapter-03/) | Operators & Conditions — 연산자, 조건문, 장치 상태 판단 |
| [04](./Chapter-04/) | Loops — 반복문, 센서 샘플링, 재시도 |
| [05](./Chapter-05/) | Functions — 함수 설계, 반환값, 람다, 파일 분리 |
| [06](./Chapter-06/) | Arrays & Strings — 배열, 문자열, 뷰, 입력 및 파싱 |
| [07](./Chapter-07/) | Pointers & References |
| [08](./Chapter-08/) | Structs & Classes |
| [09](./Chapter-09/) | Object-Oriented Programming |
| [10](./Chapter-10/) | Standard Library (STL) |
| [11](./Chapter-11/) | File I/O |


## Directory Structure

```text
C++/
├── README.md
├── Chapter-01/
│   ├── README.md
│   ├── examples/
│   ├── exercises/
│   └── solutions/
├── Chapter-02/
├── Chapter-03/
├── Chapter-04/
├── Chapter-05/
└── Chapter-06/
└── Chapter-07/
└── Chapter-08/
└── Chapter-09/
└── Chapter-10/
└── Chapter-11/
```

## Getting Started

[Chapter 01](./Chapter-01/)의 예제는 `Chapter-01/` 폴더를 기준으로 컴파일합니다.

**GCC**

```bash
cd Chapter-01
g++ -std=c++23 -Wall -Wextra -Wpedantic examples/01_hello_world.cpp -o hello
./hello
```

**Clang**

```bash
cd Chapter-01
clang++ -std=c++23 -Wall -Wextra -Wpedantic examples/01_hello_world.cpp -o hello
./hello
```

**MSVC** — Developer Command Prompt

```bat
cd Chapter-01
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 examples\01_hello_world.cpp /Fe:hello.exe
hello.exe
```

MSVC의 C++23 옵션은 설치된 도구 집합 버전에 따라 다를 수 있습니다. `/std:c++23`을 지원하는 버전에서는 해당 옵션을 사용하고, 그렇지 않으면 `/std:c++23preview`의 지원 여부를 확인하세요. 컴파일러의 C++23 모드와 표준 라이브러리의 개별 기능 지원 범위는 다를 수 있습니다.

Windows PowerShell에서 GCC 또는 Clang으로 생성한 실행 파일은 `.\hello.exe`로 실행할 수 있습니다. 개발 환경 설정과 Colab 실행 방법은 [Chapter 01](./Chapter-01/)에서 안내합니다.

## Code Guidelines

- 예제는 C++23을 기준으로 작성합니다.
- 기본적으로 `std::`를 명시하며, 반복되는 이름은 필요한 범위에서 `using std::이름;` 형태로 사용할 수 있습니다.
- 타입 별칭이 필요한 경우 `using 별칭 = 자료형;` 형태를 사용합니다.
- 전역 `using namespace std;`는 예제에서 사용하지 않습니다.
- 입력 실패, 범위 초과 등의 오류 처리를 포함하고 주요 컴파일러 경고를 활성화합니다.
- 예제와 정답 코드는 각각 `examples/`, `solutions/`에 별도 파일로 제공합니다.

## References

- [ISO/IEC 14882:2024 — C++](https://www.iso.org/standard/83626.html)
- [ISO C++ — The Standard](https://isocpp.org/std/the-standard)
- [C++23 Compiler Support — cppreference](https://en.cppreference.com/w/cpp/compiler_support/23)
- [MSVC `/std` 옵션 — Microsoft Learn](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version)

---

[← MoreStudy](../README.md)
