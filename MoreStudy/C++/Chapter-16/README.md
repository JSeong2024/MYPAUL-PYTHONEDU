# Chapter 16. CMake, Libraries & Project Structure

C++20 프로젝트를 여러 소스 파일과 라이브러리로 구성하고, **CMake 설정 → 빌드 → CTest 검증 → 설치 → 외부 프로젝트에서 재사용**까지 연결합니다. 간단한 실행 파일에서 시작해 설정 가능한 처리 파이프라인, 설치형 SDK 제작으로 확장합니다.

- **기준 표준:** C++20 (ISO/IEC 14882:2020)
- **개발 환경:** GCC, Clang, MSVC · CMake 3.23 이상
- **실습 기준:** 외부 다운로드 없는 오프라인 빌드, Target 중심 설정, 학생용과 모범답안 분리

**선행 학습:** [Chapter 05 — Functions](../Chapter-05/README.md) · [Chapter 11 — File I/O](../Chapter-11/README.md) · [Chapter 12 — Resource Management](../Chapter-12/README.md) · [Chapter 13 — Generic Programming](../Chapter-13/README.md) · [Chapter 15 — Performance Optimization](../Chapter-15/README.md)

## Contents

| Section | Topic |
|:---:|---|
| [16.1](#section-16-1) | Build Process — 컴파일부터 실행까지 |
| [16.2](#section-16-2) | `CMakeLists.txt`와 최소 프로젝트 |
| [16.3](#section-16-3) | Target 중심 설계와 의존 관계 |
| [16.4](#section-16-4) | Header, Translation Unit, Include 경로 |
| [16.5](#section-16-5) | C++20 표준 및 컴파일러 독립성 |
| [16.6](#section-16-6) | Static Library — 정적 라이브러리 |
| [16.7](#section-16-7) | Shared Library — 동적 라이브러리 |
| [16.8](#section-16-8) | `PUBLIC`, `PRIVATE`, `INTERFACE` |
| [16.9](#section-16-9) | 컴파일 옵션과 경고 관리 |
| [16.10](#section-16-10) | `option()`과 Compile Definition |
| [16.11](#section-16-11) | CMakePresets — Debug/Release 설정 공유 |
| [16.12](#section-16-12) | CTest와 Release에서도 동작하는 테스트 |
| [16.13](#section-16-13) | 설치 규칙과 공개 Header |
| [16.14](#section-16-14) | `find_package()`와 소비자 프로젝트 |
| [16.15](#section-16-15) | 외부 의존성 관리와 오프라인 빌드 |
| [16.16](#section-16-16) | 빌드 재현성, CI, 배포 점검 |
| [16.17](#section-16-17) | Basic Mini Project — Device Report |
| [16.18](#section-16-18) | Coding Practice — 4개 실습 |
| [16.19](#section-16-19) | Advanced Project — Configurable Pipeline |
| [16.20](#section-16-20) | Pro Project — Installable Sensor SDK |
| [16.21](#section-16-21) | Quiz & Summary |

## Getting Started

다음 명령어는 `Chapter-16/` 폴더를 기준으로 합니다. CMake는 버전 3.23 이상이 필요하고, **Ninja는 Preset 사용 시** 필요합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_build_pipeline.cpp -o demo
./demo
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_build_pipeline.cpp -o demo
./demo
```

**MSVC — Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /permissive- /utf-8 examples\01_build_pipeline.cpp /Fe:demo.exe
demo.exe
```

**CMake 예제 프로젝트**

```bash
cmake -S examples/17_device_report -B build/device -DCMAKE_BUILD_TYPE=Debug
cmake --build build/device
ctest --test-dir build/device --output-on-failure
```

[Windows / MSVC 빌드 안내](./docs/WINDOWS_BUILD.md)

**자동 검증**

```bash
python3 tests/check.py --compiler g++-14
python3 tests/check.py --compiler clang++
python3 tests/check.py --mode student --only exercises
```

`projects/`와 `exercises/`는 해결해야 할 TODO를 포함합니다. 기본 검사는 `solutions/`의 모범답안과 예제를 사용하며, 학생용 코드는 구현 완료 전 실패하는 것이 정상입니다.

---

<a id="section-16-1"></a>
## 16.1. Build Process — 컴파일부터 실행까지

C++ 소스 코드는 일반적으로 **전처리 → 컴파일 → 링크 → 실행** 단계를 거칩니다. `.cpp` 파일별로 만들어진 목적 파일(Object File)을 링커가 합쳐 최종 실행 파일이나 라이브러리를 구성합니다. CMake는 C++ 컴파일러 자체가 아니라 **어떤 파일을 어떤 옵션으로 빌드할지 기술하고 빌드 시스템을 생성하는 도구**입니다.

- **Configure:** `CMakeLists.txt`를 읽고 대상(Target), 컴파일러, 옵션과 의존성을 결정
- **Generate:** Ninja·Makefile 등의 빌드 시스템 생성
- **Build:** 컴파일 및 링크 실행. 필요한 대상만 다시 빌드하는 증분 빌드 지원
- **Test / Install:** CTest로 검증하고 설치 규칙이 있을 때 결과물을 배치

컴파일러를 바꾸거나 Debug/Release의 빌드 설정을 바꿀 때는 **별도 빌드 폴더**를 사용하는 편이 안전합니다. 기존 빌드 폴더의 캐시를 그대로 재사용하면 의도하지 않은 설정이 남을 수 있습니다.

**예제 코드 — [01_build_pipeline.cpp](./examples/01_build_pipeline.cpp)**

```cpp
#include <iostream>
int main() {
    std::cout << "Build pipeline: source -> object -> executable\n";
}
```

---

<a id="section-16-2"></a>
## 16.2. `CMakeLists.txt`와 최소 프로젝트

CMake는 소스와 빌드 결과를 분리하는 **Out-of-Source Build**를 권장합니다. 최상위 `CMakeLists.txt`에서 최소 버전, 프로젝트명, 언어, 실행 대상을 선언한 뒤 `cmake -S ... -B ...`로 빌드 디렉터리를 생성합니다.

```cmake
cmake_minimum_required(VERSION 3.23)
project(SensorExample LANGUAGES CXX)
add_executable(sensor_app main.cpp)
target_compile_features(sensor_app PRIVATE cxx_std_20)
```

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

`project()`에서 버전을 선택적으로 선언할 수 있으며, `add_executable()`은 **빌드 대상 이름과 소스 파일**을 정의합니다. 단일 `.cpp`에 구현한 코드를 여러 Translation Unit으로 분리하는 연습은 이후 Basic 프로젝트에서 수행합니다.

**예제 코드 — [02_translation_units.cpp](./examples/02_translation_units.cpp)**

```cpp
#include <iostream>
#include <string_view>

int count_tokens(std::string_view text) {
    int count = 0;
    bool inside = false;
    for (char ch : text) {
        if (ch == ' ') { inside = false; }
        else if (!inside) { inside = true; ++count; }
    }
    return count;
}
int main() {
    std::cout << "Tokens: " << count_tokens("CMake builds targets") << '\n';
}
```

---

<a id="section-16-3"></a>
## 16.3. Target 중심 설계와 의존 관계

CMake의 기본 구성 단위는 디렉터리가 아니라 **Target**입니다. 실행 파일은 `add_executable()`, 라이브러리는 `add_library()`로 만들고, `target_link_libraries()`로 실제 의존성을 연결합니다.

```cmake
add_library(device_core STATIC src/report.cpp)
add_executable(device_report app/main.cpp)
target_link_libraries(device_report PRIVATE device_core)
```

`device_report`는 `device_core`를 사용합니다. 빌드 시스템은 이 관계를 이용해 적절한 순서로 빌드하고, 재컴파일 범위를 판단합니다. `link_directories()`나 프로젝트 전체 `include_directories()`를 남용하기보다 대상별 속성을 설정하는 편이 관리하기 쉽습니다.

**핵심:** 하나의 라이브러리가 어디에서 어떤 컴파일 옵션과 헤더를 요구하는지 Target에 명시해야, 나중에 외부 소비자에게 전달할 수 있습니다.

**예제 코드 — [03_target_design.cpp](./examples/03_target_design.cpp)**

```cpp
#include <iostream>
#include <numeric>
#include <vector>
int main() {
    const std::vector<int> readings{12, 14, 16};
    std::cout << "Total: " << std::accumulate(readings.begin(), readings.end(), 0) << '\n';
}
```

---

<a id="section-16-4"></a>
## 16.4. Header, Translation Unit, Include 경로

헤더 파일은 외부에 공개할 **함수 선언·타입 계약**을 담고, `.cpp` 파일은 그 구현을 제공합니다. 헤더에서 필요한 타입을 사용한다면 해당 헤더에 필요한 `#include`를 직접 적어야 합니다. 다른 헤더의 우연한 포함 관계에 기대는 코드는 파일 분리 후 실패할 수 있습니다.

```text
include/device/report.hpp   ← 공개 API
src/report.cpp              ← 구현
app/main.cpp                ← 소비자
```

```cmake
target_include_directories(device_core PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
```

예제의 `std::span<const int>`는 연속 데이터를 **복사하지 않고** 받는 인터페이스입니다. `std::span`은 비소유 View이므로 원본 데이터의 수명이 충분히 길어야 합니다. 헤더의 정의를 변경하면 이를 사용하는 여러 소스 파일의 재컴파일이 필요할 수 있습니다.

**예제 코드 — [04_header_contracts.cpp](./examples/04_header_contracts.cpp)**

```cpp
#include <iostream>
#include <span>
#include <vector>
[[nodiscard]] int count(std::span<const int> items) {
    return static_cast<int>(items.size());
}
int main() {
    const std::vector<int> batch{7, 8, 9};
    std::cout << "Count: " << count(batch) << '\n';
}
```

---

<a id="section-16-5"></a>
## 16.5. C++20 표준 및 컴파일러 독립성

C++ 언어 버전은 Target 단위에서 선언합니다. `target_compile_features(target PUBLIC cxx_std_20)`는 해당 대상과 소비자에게 C++20 요구사항을 전달하는 방식이며, `CXX_EXTENSIONS OFF`는 GNU 확장 같은 비표준 언어 확장 사용을 제한합니다.

```cmake
target_compile_features(device_core PUBLIC cxx_std_20)
set_target_properties(device_core PROPERTIES CXX_EXTENSIONS OFF)
```

C++20 언어 모드가 켜졌다고 해서 모든 컴파일러·표준 라이브러리가 모든 기능을 동일하게 구현했다고 단정할 수는 없습니다. GCC, Clang, MSVC의 버전과 사용 중인 표준 라이브러리를 확인하세요. 이번 Chapter는 `<format>` 등 플랫폼별 지원 차이가 큰 기능을 필수 조건으로 두지 않습니다.

**예제 코드 — [05_cpp20_standard.cpp](./examples/05_cpp20_standard.cpp)**

```cpp
#include <iostream>
#include <map>
#include <string>
int main() {
    const std::map<std::string, int> devices{{"A", 12}, {"B", 21}};
    std::cout << "Has B: " << std::boolalpha << devices.contains("B") << '\n';
}
```

---

<a id="section-16-6"></a>
## 16.6. Static Library — 정적 라이브러리

정적 라이브러리(Static Library)는 보통 `.a` 또는 `.lib` 형태로 생성되며, 소비자 실행 파일을 링크할 때 필요한 코드를 포함시키는 방식입니다.

```cmake
add_library(device_core STATIC src/report.cpp)
add_executable(device_report app/main.cpp)
target_link_libraries(device_report PRIVATE device_core)
```

같은 라이브러리를 여러 실행 파일과 테스트에서 재사용할 때 유용합니다. 다만 정적 라이브러리라고 해서 **빌드 한 번으로 항상 동일한 바이너리**가 생성되거나, 모든 환경에서 종속성이 제거되는 것은 아닙니다. 플랫폼과 링크 설정을 구분해야 합니다.

**예제 코드 — [06_static_library_client.cpp](./examples/06_static_library_client.cpp)**

```cpp
#include <iostream>
#include <string>
[[nodiscard]] std::string format_device(const std::string& id, int count) {
    return id + ": " + std::to_string(count);
}
int main() {
    std::cout << format_device("sensor-A", 3) << '\n';
}
```

---

<a id="section-16-7"></a>
## 16.7. Shared Library — 동적 라이브러리

동적 라이브러리(Shared Library)는 실행 중 운영체제의 로더가 필요한 코드를 연결하는 방식입니다. Linux의 `.so`, Windows의 `.dll` 등이 대표적입니다.

```cmake
add_library(device_plugin SHARED src/plugin.cpp)
```

배포 시에는 실행 파일뿐 아니라 **동적 라이브러리를 찾아 로딩할 수 있는 경로**도 고려해야 합니다. Windows에서는 DLL 내보내기/가져오기, Linux에서는 RPATH나 라이브러리 검색 경로 등 플랫폼별 규칙이 다릅니다. 일반적으로 `SHARED`로 바꾸는 것만으로 모든 플랫폼에서 바로 배포 가능한 것은 아닙니다.

실제 기본 프로젝트는 배포 복잡도를 줄이기 위해 `STATIC`을 사용하며, 공유 라이브러리의 배포는 별도 확장 학습 주제로 남깁니다.

**예제 코드 — [07_shared_library_boundary.cpp](./examples/07_shared_library_boundary.cpp)**

```cpp
#include <iostream>
#include <string_view>
[[nodiscard]] bool needs_attention(std::string_view device, int reading) {
    return !device.empty() && reading >= 80;
}
int main() {
    std::cout << "Alert: " << std::boolalpha << needs_attention("motor", 85) << '\n';
}
```

---

<a id="section-16-8"></a>
## 16.8. `PUBLIC`, `PRIVATE`, `INTERFACE`

Target에 설정한 Include 경로, 컴파일 기능, 정의, 링크 의존성은 **자기 대상과 사용하는 대상 중 누구에게 전달할지** 정해야 합니다.

| 범위 | 대상 자신 | 소비자에게 전달 | 대표 용도 |
|---|:---:|:---:|---|
| `PRIVATE` | 적용 | 전달하지 않음 | 구현용 옵션, 내부 헤더 |
| `PUBLIC` | 적용 | 전달 | 공개 헤더가 요구하는 Include 경로·C++ 표준 |
| `INTERFACE` | 적용하지 않음 | 전달 | 사용 규칙만 제공하는 헤더 전용 라이브러리 |

```cmake
add_library(project_warnings INTERFACE)
target_compile_options(project_warnings INTERFACE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall>
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wextra>
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wpedantic>)
```

`INTERFACE` 라이브러리를 생성하고 다른 대상에 연결하면 컴파일 옵션을 재사용할 수 있습니다. 주의할 점은 예제의 구분자가 CMake List 문법을 따른다는 것이고, 컴파일러별 옵션은 조건부로 적용해야 합니다.

**예제 코드 — [08_interface_requirements.cpp](./examples/08_interface_requirements.cpp)**

```cpp
#include <iostream>
#include <span>
[[nodiscard]] int peak(std::span<const int> values) {
    int highest = 0;
    for (const int value : values) if (value > highest) highest = value;
    return highest;
}
int main() {
    const int samples[]{3, 9, 5};
    std::cout << "Peak: " << peak(samples) << '\n';
}
```

---

<a id="section-16-9"></a>
## 16.9. 컴파일 옵션과 경고 관리

경고 옵션은 버그를 조기에 발견하는 수단입니다. GCC·Clang에는 `-Wall -Wextra -Wpedantic`, MSVC에는 `/W4`를 출발점으로 사용할 수 있습니다. 옵션을 프로젝트 전체에 무조건 적용하면 타사 라이브러리까지 영향을 받을 수 있으므로 Target 단위로 관리하는 편이 안전합니다.

```cmake
if(MSVC)
    target_compile_options(device_core PRIVATE /W4 /EHsc /permissive- /utf-8)
else()
    target_compile_options(device_core PRIVATE -Wall -Wextra -Wpedantic)
endif()
```

`-Werror`는 경고를 오류로 취급하므로 CI에 유용할 수 있지만, 컴파일러 버전이 달라졌을 때 새 경고 때문에 빌드가 실패할 수 있습니다. 프로젝트 특성에 따라 도입을 결정해야 합니다. 예제의 `can_add()`는 정수 오버플로가 없음을 검사하고 그 판단 결과를 출력합니다.

**예제 코드 — [09_target_warnings.cpp](./examples/09_target_warnings.cpp)**

```cpp
#include <iostream>
#include <limits>
[[nodiscard]] bool can_add(int lhs, int rhs) {
    if (rhs > 0) return lhs <= std::numeric_limits<int>::max() - rhs;
    if (rhs < 0) return lhs >= std::numeric_limits<int>::min() - rhs;
    return true;
}
int main() {
    std::cout << "Can add: " << std::boolalpha << can_add(9, 8) << '\n';
}
```

---

<a id="section-16-10"></a>
## 16.10. `option()`과 Compile Definition

프로젝트 옵션을 이용하면 소스 코드를 수정하지 않고 기능을 켜고 끌 수 있습니다.

```cmake
option(SENSOR_TRACE "Enable sensor diagnostics" OFF)
target_compile_definitions(device_core PRIVATE
    $<$<BOOL:${SENSOR_TRACE}>:SENSOR_TRACE>)
```

```bash
cmake -S . -B build -DSENSOR_TRACE=ON
```

`#ifdef SENSOR_TRACE`는 해당 매크로의 정의 여부를 확인합니다. 값이 `0`으로 정의되어 있어도 `#ifdef`는 참이므로, 숫자 값으로 스위치를 만들려면 `#if SENSOR_TRACE`와 같은 표현을 사용해야 합니다. 옵션은 Target 인터페이스에 필요한 경우만 `PUBLIC`으로 전달합니다.

**예제 코드 — [10_compile_definitions.cpp](./examples/10_compile_definitions.cpp)**

```cpp
#include <iostream>
int main() {
#ifdef SENSOR_TRACE
    std::cout << "Trace: enabled\n";
#else
    std::cout << "Trace: disabled\n";
#endif
}
```

---

<a id="section-16-11"></a>
## 16.11. CMakePresets — Debug/Release 설정 공유

`CMakePresets.json`은 **팀에서 공유할 빌드 설정**을 기록하는 파일입니다. 반면 `CMakeUserPresets.json`은 개인 경로·로컬 도구 설정을 담는 용도로 사용하며 Git에 올리지 않는 편이 일반적입니다.

이번 Chapter의 Basic과 Pro 프로젝트에는 `debug`, `release` Configure/Build/Test Preset이 포함됩니다.

```bash
cd examples/17_device_report
cmake --preset debug
cmake --build --preset debug
ctest --preset debug
```

이 Preset은 **Ninja**를 생성기로 지정하므로 Ninja가 설치되어 있어야 합니다. Ninja가 없으면 `cmake -S . -B build` 방식으로 빌드할 수 있습니다. `CMAKE_BUILD_TYPE`은 단일 구성 생성기(Ninja·Makefile)에서 사용하며 Visual Studio 같은 다중 구성 생성기에서는 별도 구성 선택 방식이 필요합니다.

**예제 코드 — [11_presets_and_options.cpp](./examples/11_presets_and_options.cpp)**

```cpp
#include <iostream>
#include <string_view>
[[nodiscard]] constexpr std::string_view build_mode() {
#ifdef NDEBUG
    return "Release-like";
#else
    return "Debug-like";
#endif
}
int main() {
    std::cout << "Mode: " << build_mode() << '\n';
}
```

---

<a id="section-16-12"></a>
## 16.12. CTest와 Release에서도 동작하는 테스트

CMake의 `enable_testing()` 또는 `include(CTest)`로 테스트 기능을 활성화하고, `add_test()`로 실행할 프로그램을 등록합니다.

```cmake
include(CTest)
if(BUILD_TESTING)
    add_executable(device_report_tests tests/report_tests.cpp)
    target_link_libraries(device_report_tests PRIVATE device_core)
    add_test(NAME device_report_logic COMMAND device_report_tests)
endif()
```

```bash
ctest --test-dir build --output-on-failure --no-tests=error
```

중요한 점은 **`assert()`가 Release의 `NDEBUG` 설정에서 비활성화될 수 있다**는 사실입니다. 따라서 이번 프로젝트 테스트는 명시적인 조건 비교와 실패 반환 코드로 작성했습니다. CTest는 `0`이 아닌 종료 코드가 발생하면 실패로 처리합니다. `PASS_REGULAR_EXPRESSION`은 출력 검증에 쓸 수 있지만, 예외 처리나 경계값까지 검사할 때는 별도 테스트 프로그램이 더 적합합니다.

**예제 코드 — [12_ctest_behavior.cpp](./examples/12_ctest_behavior.cpp)**

```cpp
#include <iostream>
#include <stdexcept>
[[nodiscard]] int normalized(int reading) {
    if (reading < 0 || reading > 100) throw std::invalid_argument("reading out of range");
    return reading;
}
int main() {
    if (normalized(35) != 35) return 1; // Release에서도 검사 유지
    std::cout << "Test: PASS\n";
}
```

---

<a id="section-16-13"></a>
## 16.13. 설치 규칙과 공개 Header

내 컴퓨터의 빌드 폴더에서 동작하는 프로그램과 **다른 프로젝트가 설치된 라이브러리를 사용할 수 있는 패키지**는 구분해야 합니다. 설치형 라이브러리는 공개 Header, 바이너리, CMake 패키지 메타데이터가 함께 제공되어야 합니다.

```cmake
include(GNUInstallDirs)
install(TARGETS sensor_sdk_core EXPORT SensorSDKTargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
```

`BUILD_INTERFACE` 경로에는 소스 트리의 Include 경로를, `INSTALL_INTERFACE`에는 설치 기준 상대 경로를 사용합니다. 소비자에게 개발자 PC의 `/home/...` 절대 경로가 들어가지 않도록 해야 합니다. Pro 프로젝트가 이 구조를 실제로 구현합니다.

**예제 코드 — [13_install_public_api.cpp](./examples/13_install_public_api.cpp)**

```cpp
#include <iostream>
#include <span>
[[nodiscard]] int total(std::span<const int> readings) {
    int sum = 0;
    for (int n : readings) sum += n;
    return sum;
}
int main() {
    const int readings[]{5, 15};
    std::cout << "Public API total: " << total(readings) << '\n';
}
```

---

<a id="section-16-14"></a>
## 16.14. `find_package()`와 소비자 프로젝트

CMake의 소비자 프로젝트는 설치된 SDK를 직접 경로로 지정하지 않고 다음과 같이 사용할 수 있습니다.

```cmake
find_package(SensorSDK 1.2 CONFIG REQUIRED)
add_executable(sensor_consumer main.cpp)
target_link_libraries(sensor_consumer PRIVATE SensorSDK::core)
```

`SensorSDKConfig.cmake` 및 내보낸 `SensorSDKTargets.cmake`가 있으면 라이브러리 파일 위치와 공개 Header 경로를 일관되게 전달할 수 있습니다.

`find_package()`가 성공하는 것과 **소비자 빌드·실행이 성공하는 것**은 별개입니다. Pro 테스트는 설치 경로를 옮긴 뒤 새 빌드 폴더에서 소비자 프로그램을 다시 빌드하여 실제 재사용 가능성을 확인합니다. 설치 위치는 `CMAKE_PREFIX_PATH`로 알려줄 수 있습니다.

**예제 코드 — [14_package_consumer.cpp](./examples/14_package_consumer.cpp)**

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
int main() {
    std::vector<int> values{6, 2, 4};
    std::ranges::sort(values);
    std::cout << "First: " << values.front() << '\n';
}
```

---

<a id="section-16-15"></a>
## 16.15. 외부 의존성 관리와 오프라인 빌드

외부 라이브러리를 사용하는 대표 방식은 설치된 패키지를 찾는 `find_package()`, 소스를 프로젝트 내부에서 함께 빌드하는 `add_subdirectory()`, 설정 단계에서 가져오는 `FetchContent` 등입니다.

- **표준 라이브러리 우선:** 필요한 기능이 충분하면 외부 의존성을 추가하지 않음
- **버전 고정:** Git 브랜치명 같은 가변 참조보다 변경 불가능한 태그·커밋·해시 사용
- **출처 확인:** 라이선스, 유지보수 상태, 배포·업데이트 정책 검토
- **오프라인 빌드:** 네트워크가 없는 CI·교육 환경에서도 재현 가능한 구조 고려

`FetchContent`는 네트워크에서 코드를 불러올 수 있으므로 교육용 Chapter 16 프로젝트에서는 외부 다운로드를 의도적으로 사용하지 않습니다. 이 방식은 패키지 관리자(vcpkg, Conan 등)의 역할을 대체하거나 보안 검사를 자동으로 보장하지 않습니다. 예제는 `<charconv>`만으로 엄격한 숫자 파싱을 수행합니다.

**예제 코드 — [15_dependency_strategy.cpp](./examples/15_dependency_strategy.cpp)**

```cpp
#include <charconv>
#include <iostream>
#include <string_view>
[[nodiscard]] bool read_number(std::string_view input, int& output) {
    const char* first = input.data();
    const char* last = first + input.size();
    const auto [ptr, ec] = std::from_chars(first, last, output);
    return ec == std::errc{} && ptr == last;
}
int main() {
    int value{};
    std::cout << "Parsed: " << std::boolalpha << read_number("120", value)
              << ", value=" << value << '\n';
}
```

---

<a id="section-16-16"></a>
## 16.16. 빌드 재현성, CI, 배포 점검

**재현 가능한 빌드**는 같은 소스·의존성·도구·설정에서 검증 가능한 결과를 얻는 것을 목표로 합니다. 여러 환경에서 바이트까지 완전히 동일한 바이너리가 나오는 것은 별도의 설정과 도구 체인 고정이 필요하므로 단순히 CMake를 사용한다는 이유만으로 보장되지 않습니다.

- 최소 두 컴파일러에서 C++20 빌드 및 테스트
- Debug와 Release에서 동일한 기능 검증
- `CMakePresets.json`과 의존성 버전 관리
- 설치 후 **독립적인 소비자 프로젝트의 재빌드**
- 실패한 테스트가 CI의 실패 종료 코드로 이어지는지 확인

GitHub Actions에는 기존 Chapter와 동일하게 GCC 14·Clang 검사를 사용합니다. 패키징은 `cmake --install`로 실습하며, 배포 파일 서명·취약점 스캔 등 제품 배포 단계의 보안 절차를 자동으로 보장하지는 않습니다.

**예제 코드 — [16_reproducible_builds.cpp](./examples/16_reproducible_builds.cpp)**

```cpp
#include <iostream>
#include <string_view>
[[nodiscard]] bool valid_identifier(std::string_view id) {
    if (id.empty()) return false;
    for (unsigned char ch : id) {
        if (!((ch >= 'A' && ch <= 'Z') || (ch >= '0' && ch <= '9') || ch == '-')) return false;
    }
    return true;
}
int main() {
    std::cout << "Valid: " << std::boolalpha << valid_identifier("SENSOR-12") << '\n';
}
```

---

<a id="section-16-17"></a>
## 16.17. Basic Mini Project — Device Report

하나의 실행 파일에 작성되어 있던 장치 측정 집계 코드를 **라이브러리, CLI, 테스트 파일**로 분리합니다. 코드의 핵심 기능은 단순하지만, CMake의 대상과 의존성을 직접 구성해 보는 것이 목적입니다.

**실습 목표**

1. `device_core`를 정적 라이브러리로 구성하고, 공개 Header 위치를 `PUBLIC`으로 전달합니다.
2. `device_report`와 `device_report_tests`를 라이브러리에 연결합니다.
3. 장치 ID가 비어 있거나 측정값이 0~100 범위 밖이면 `std::invalid_argument`를 발생시킵니다.
4. `ctest --output-on-failure`로 성공·실패 조건을 검사하고, Release에서도 검증이 활성화되는지 확인합니다.

**프로젝트 구조**

```text
examples/17_device_report/
├── CMakeLists.txt
├── CMakePresets.json
├── include/device/report.hpp
├── src/report.cpp
├── app/main.cpp
└── tests/report_tests.cpp
```

**실행**

```bash
cmake -S examples/17_device_report -B build/basic -DCMAKE_BUILD_TYPE=Release
cmake --build build/basic
ctest --test-dir build/basic --output-on-failure --no-tests=error
./build/basic/device_report
```

**정상 출력**

```text
Records: 3, Alerts: 1, Total: 185
```

**코드 흐름:** `app/main.cpp` → `device::summarize()` → `src/report.cpp`. 테스트는 실제 `device_core` 라이브러리에 연결됩니다. `CMakeLists.txt`에서 `device_core`의 Include 경로를 `PRIVATE`로 바꾸고 클린 빌드를 해보면, 소비자 코드에서 헤더를 찾지 못하는 이유를 확인할 수 있습니다.

---

<a id="section-16-18"></a>
## 16.18. Coding Practice

| 실습 | 과제 | 학생용 코드 | 모범답안 |
|:---:|---|---|---|
| ① | 패키지 버전 이름 만들기 | [01_versioned_target.cpp](./exercises/01_versioned_target.cpp) | [정답](./solutions/01_versioned_target.cpp) |
| ② | `std::span`을 이용한 공개 함수 계약 | [02_include_contract.cpp](./exercises/02_include_contract.cpp) | [정답](./solutions/02_include_contract.cpp) |
| ③ | 컴파일 정의에 따른 기능 분기 | [03_configuration_flag.cpp](./exercises/03_configuration_flag.cpp) | [정답](./solutions/03_configuration_flag.cpp) |
| ④ | Release에서도 유지되는 문자열 검증 | [04_release_safe_tests.cpp](./exercises/04_release_safe_tests.cpp) | [정답](./solutions/04_release_safe_tests.cpp) |

### 실습 ① — Versioned Target

`versioned_name(name, major)`를 구현해 `sensor-v3` 같은 문자열을 반환합니다. 이름이 비었거나 버전이 1 미만이면 `std::invalid_argument`를 발생시킵니다. **경계값:** 빈 문자열, 0, 음수 버전.

### 실습 ② — Include Contract

`std::span<const int>`를 전달받아 양수인 원소만 합산합니다. 호출자의 `std::vector`·`std::array` 데이터를 복사하지 않고 사용합니다. **경계값:** 빈 Range, 음수만 존재하는 입력.

### 실습 ③ — Compile Definition

`CH16_DIAGNOSTICS` 매크로의 정의 여부에 따라 `diagnostics-on` 또는 `diagnostics-off`를 반환합니다. 두 빌드 모두 실행하여 조건부 컴파일의 결과를 비교합니다.

### 실습 ④ — Release-Safe Tests

패키지 이름은 영문 대·소문자, 숫자, `-`만 허용합니다. `assert()`로 결과를 확인하는 대신 실제 함수 반환값을 검사하여 Release에서도 테스트가 작동하도록 설계합니다.

**실습 검증**

```bash
python3 tests/check.py --only exercises                # 모범답안
python3 tests/check.py --mode student --only exercises # 학생용 TODO
```

<details>
<summary>검증 코드와 모범답안 확인</summary>

실습별 `tests/cases/`에 정상·경계값 검증 코드가 있습니다. 학생용 코드가 완성되면 `--mode student`의 결과를 확인하고, 필요한 경우 `solutions/`의 구현과 비교할 수 있습니다.

</details>

---

<a id="section-16-19"></a>
## 16.19. Advanced Project — Configurable Pipeline

### 상황 및 배경

센서 데이터가 여러 파일에서 들어오고 있으며, 일부 입력에는 잘못된 금액 대신 **비정상 측정값·상태 표기·형식 오류**가 섞여 있습니다. 운영 도구는 유효 데이터를 계속 처리해야 하고, 실패한 행은 집계에서 제외해야 합니다. 장치별 요약은 실행 순서와 관계없이 동일하게 출력되어야 합니다.

이 프로젝트에서는 코드를 **파서 라이브러리, CLI, 테스트**로 분리하고 CMake 옵션으로 테스트·진단 설정을 관리합니다.

### 구현 조건

1. 입력 파일은 헤더가 없는 `장치ID,측정값,상태`의 CSV입니다. 상태는 `ok` 또는 `bad`이며, 측정값은 0~100 정수만 허용합니다.
2. 필드 개수나 값이 잘못된 행은 `rejected` 건수를 증가시키고 계속 진행합니다. `bad` 상태의 유효한 행은 파싱되지만 집계에서는 제외합니다.
3. 집계는 **장치 ID 오름차순**으로 출력하며, 유효한 `ok` 상태의 측정값만 건수·합계·경보에 반영합니다. 경보 기준값은 80 이상입니다.
4. `pipeline_core`와 `pipeline_cli`를 별도 Target으로 만들고, `PIPELINE_BUILD_TESTS`와 `PIPELINE_VERBOSE` 옵션을 지원합니다.
5. 정상 CSV, 행 누락, 잘못된 정수, 범위 초과, CRLF 줄바꿈, 빈 입력에 대해 테스트합니다.

**입출력 예시**

```text
INPUT (data/measurements.csv)
A,20,ok
B,91,ok
A,40,bad
A,70,ok
BROKEN,abc,ok
B,8,ok

OUTPUT
accepted=4 rejected=1
A 2 90 0
B 2 99 1
```

**시작 코드:** [`projects/advanced_pipeline/`](./projects/advanced_pipeline/)  
**모범답안:** [`solutions/advanced_pipeline/`](./solutions/advanced_pipeline/)

```bash
cmake -S solutions/advanced_pipeline -B build/advanced -DPIPELINE_BUILD_TESTS=ON
cmake --build build/advanced
ctest --test-dir build/advanced --output-on-failure
./build/advanced/pipeline_cli solutions/advanced_pipeline/data/measurements.csv
```

<details>
<summary>구현 가이드</summary>

**STEP 01 — 파서 분리:** `std::getline`으로 각 행을 읽고 `std::from_chars`로 정수 변환 성공 여부와 문자열 전체 소비 여부를 검사합니다.

```cpp
int parsed{};
const auto [end, error] = std::from_chars(first, last, parsed);
const bool accepted = error == std::errc{} && end == last;
```

**STEP 02 — 집계:** `std::map<std::string, Summary>`을 사용하면 장치 ID 오름차순 결과를 별도 정렬 없이 만들 수 있습니다.

**STEP 03 — CMake 옵션:** `target_compile_definitions()`으로 진단용 매크로를 **구현 Target에만** 전달하고, 테스트 빌드는 `PIPELINE_BUILD_TESTS`에서 제어합니다.

</details>

**검증 사항:** 입력 순서를 바꾸었을 때 동일한 장치별 요약이 나오는지, 거부된 행이 합계에 영향을 주지 않는지, Debug·Release에서 결과가 일치하는지 확인합니다. 이 교육용 CSV 파서는 **인용부호로 감싼 쉼표 필드**를 지원하지 않습니다. 완전한 RFC 4180 파서가 필요한 실무에서는 별도 처리 규칙을 설계해야 합니다.

---

<a id="section-16-20"></a>
## 16.20. Pro Project — Installable Sensor SDK

### 의뢰 배경

내부 팀에서 제작한 센서 통계 함수가 여러 프로그램에서 중복 구현되고 있습니다. 각 팀은 서로 다른 Include 경로와 라이브러리 파일 이름을 수동으로 지정하고 있어, 저장소를 옮기거나 빌드 구성을 바꾸면 컴파일에 실패합니다.

C++20으로 작성한 센서 통계 기능을 **독립적으로 설치·이동·재사용할 수 있는 CMake 패키지**로 제공하세요. 다른 프로젝트는 원본 저장소 구조를 몰라도 `find_package()`와 내보낸 Target 이름만으로 사용해야 합니다.

### 요구사항 및 작업 범위

1. 공개 API `sensor_sdk::analyze(std::span<const int>)`를 제공하고, 빈 입력과 0~1000을 벗어난 값은 `std::invalid_argument`로 거부합니다.
2. 결과 구조체는 건수, 최솟값, 최댓값, 평균을 제공합니다. 평균은 `double`로 계산합니다.
3. `SensorSDK::core` 이름을 소비자가 사용하도록 **Target Export**와 Alias를 설정합니다.
4. `CMAKE_INSTALL_LIBDIR`, `CMAKE_INSTALL_INCLUDEDIR`를 사용해 공개 Header, 라이브러리, CMake 패키지 파일을 설치합니다.
5. `SensorSDKConfig.cmake`와 `SensorSDKConfigVersion.cmake`를 생성하고 프로젝트 버전 **1.2.0**, 같은 Major 버전 정책을 사용합니다.
6. 외부 라이브러리 다운로드 없이 독립적인 `consumer/` 프로젝트에서 `find_package(SensorSDK 1.2 CONFIG REQUIRED)`가 동작해야 합니다.
7. **설치 폴더를 이동한 뒤에도** 새 경로를 `CMAKE_PREFIX_PATH`로 전달하여 소비자 프로젝트가 빌드·실행되어야 합니다.
8. Debug·Release CMake Preset, CTest, 빌드 산출물 Git 제외 규칙을 마련합니다.

### 납품 항목

- 라이브러리 소스·공개 Header 및 프로젝트별 `CMakeLists.txt`
- CMake Package Config, Version 파일, Export 설정
- 독립 소비자 프로젝트, 실행 예제, 자동 테스트
- `CMakePresets.json` 및 빌드·설치·검증 설명

**학생용 시작 프로젝트:** [`projects/pro_sensor_sdk/`](./projects/pro_sensor_sdk/)  
**모범답안:** [`solutions/pro_sensor_sdk/`](./solutions/pro_sensor_sdk/)

**설치 후 독립 소비자 검증 (Linux / macOS 셸 예시)**

```bash
cmake -S solutions/pro_sensor_sdk -B build/pro -DCMAKE_BUILD_TYPE=Release
cmake --build build/pro
ctest --test-dir build/pro --output-on-failure
cmake --install build/pro --prefix "$(pwd)/build/sdk-prefix"

cmake -S solutions/pro_sensor_sdk/consumer -B build/consumer \
    -DCMAKE_PREFIX_PATH="$(pwd)/build/sdk-prefix"
cmake --build build/consumer
./build/consumer/sensor_consumer
```

**결과**

```text
Consumer avg: 8
```

<details>
<summary>Pro 설계 가이드</summary>

`target_include_directories()`에서 빌드 환경과 설치 환경을 분리합니다.

```cmake
target_include_directories(sensor_sdk_core PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
```

`install(EXPORT ...)`는 내보낸 Target을 `SensorSDK::core` 이름으로 참조할 수 있게 구성합니다. `configure_package_config_file()`과 `write_basic_package_version_file()`로 패키지 탐색과 버전 검증 파일을 생성합니다.

빌드가 성공해도 SDK가 재사용 가능하다고 단정하지 않고, **설치 경로를 옮긴 후 독립 소비자 프로젝트를 다시 Configure → Build → Run**해야 합니다.

</details>

### 검증 사항

- 정상 입력·빈 입력·범위 초과에서 API 반환 및 예외 계약 확인
- 설치한 라이브러리가 공개 Header와 함께 올바른 경로에 배치되는지 확인
- 내보낸 Target 이름과 C++20 요구사항이 외부 소비자에게 전달되는지 확인
- 설치 경로 이동 후에도 기존 절대 경로에 대한 의존이 없는지 확인
- Debug·Release 검증과 프로젝트 분리, 외부 다운로드 없는 오프라인 빌드 확인

이 Pro 프로젝트는 **정적 라이브러리** 배포를 기준으로 합니다. Shared Library의 ABI 안정성, 서명, 패키지 관리자 배포 및 Windows 설치 프로그램은 별도 확장 주제입니다.

---

<a id="section-16-21"></a>
## 16.21. Quiz & Summary

### Quiz

<details>
<summary>Q1. CMake는 C++ 소스 코드를 직접 기계어로 변환하는 컴파일러인가요?</summary>

아닙니다. CMake는 Target, 의존성, 옵션을 바탕으로 빌드 시스템을 생성하며 실제 컴파일은 설정된 컴파일러가 수행합니다.

</details>

<details>
<summary>Q2. 공개 Header가 필요로 하는 Include 경로에는 `PRIVATE`와 `PUBLIC` 중 어느 것이 적합한가요?</summary>

소비자도 사용해야 하므로 보통 `PUBLIC`을 사용합니다. 구현 파일 내부에만 필요한 경로라면 `PRIVATE`를 사용합니다.

</details>

<details>
<summary>Q3. `INTERFACE` 라이브러리는 반드시 정적 라이브러리 파일을 생성하나요?</summary>

아닙니다. 일반적인 `INTERFACE` 라이브러리는 사용 요구사항을 전달하며 라이브러리 바이너리를 생성하지 않습니다.

</details>

<details>
<summary>Q4. C++20 요구사항을 소비자 Target에 전달하려면 어떤 명령을 사용할 수 있나요?</summary>

`target_compile_features(library PUBLIC cxx_std_20)`처럼 설정합니다.

</details>

<details>
<summary>Q5. CMake의 Debug·Release 설정을 팀에서 공유하려면 어떤 파일을 사용하나요?</summary>

`CMakePresets.json`입니다. 개인의 로컬 설정은 `CMakeUserPresets.json`으로 분리할 수 있습니다.

</details>

<details>
<summary>Q6. `-DCMAKE_BUILD_TYPE=Release`가 모든 CMake 생성기에서 같은 방식으로 적용되나요?</summary>

아닙니다. 단일 구성 생성기는 `CMAKE_BUILD_TYPE`을 사용하고, Visual Studio 같은 다중 구성 생성기는 `--config Release` 등을 사용합니다.

</details>

<details>
<summary>Q7. Release에서도 중요한 테스트가 실행되도록 하려면 `assert()`에만 의존해도 되나요?</summary>

안 됩니다. `NDEBUG` 정의 시 `assert()` 검사는 비활성화될 수 있습니다. 명시적인 오류 반환·테스트 실패 처리를 사용합니다.

</details>

<details>
<summary>Q8. `ctest --test-dir build --output-on-failure`는 어떤 역할을 하나요?</summary>

CMake에 등록된 테스트를 실행하고 실패한 테스트의 출력 정보를 표시합니다.

</details>

<details>
<summary>Q9. 소비자 프로젝트가 원본 소스 폴더 없이 설치된 라이브러리를 사용할 수 있게 하려면 무엇이 필요한가요?</summary>

공개 Header, 설치 라이브러리, 패키지 설정 파일, 내보낸 Target, 설치 기준 Include 경로가 필요합니다.

</details>

<details>
<summary>Q10. `find_package(SensorSDK CONFIG REQUIRED)`가 성공하면 소비자 프로그램 실행까지 보장되나요?</summary>

아닙니다. 실제 링크·런타임 로딩·API 동작까지 소비자 프로젝트에서 검증해야 합니다.

</details>

<details>
<summary>Q11. `FetchContent`로 외부 Git 브랜치를 참조하면 완전히 재현 가능한 빌드가 보장되나요?</summary>

아닙니다. 가변 브랜치 참조는 내용이 바뀔 수 있어 커밋·해시 고정 등 버전 관리가 필요합니다.

</details>

<details>
<summary>Q12. 같은 소스와 CMakeLists만 있으면 모든 OS에서 바이트 단위로 동일한 바이너리가 만들어지나요?</summary>

아닙니다. 컴파일러, 툴체인, 플랫폼, 빌드 경로, 시간 정보 등에도 영향을 받을 수 있습니다.

</details>

### Summary

- CMake는 **Target과 의존성**을 중심으로 빌드 설정을 구성합니다.
- 공개 API를 제공하는 라이브러리는 `PUBLIC`·`PRIVATE`·`INTERFACE` 범위를 명확히 구분합니다.
- Debug·Release와 C++20 컴파일 요구사항을 일관되게 관리합니다.
- 테스트는 Release에서도 유지하고, CTest 실패가 CI 실패로 연결되도록 합니다.
- 라이브러리 배포는 **빌드 성공 → 설치 → 독립 소비자 빌드·실행**까지 검증해야 합니다.
- 패키지 의존성과 빌드 옵션을 고정하고, 플랫폼 간 차이를 문서화합니다.

### References

- [CMake Tutorial — Official Guide](https://cmake.org/cmake/help/latest/guide/tutorial/)
- [CMake Buildsystem — Target Usage Requirements](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html)
- [CMake Presets](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html)
- [CMake CTest](https://cmake.org/cmake/help/latest/manual/ctest.1.html)
- [CMakePackageConfigHelpers](https://cmake.org/cmake/help/latest/module/CMakePackageConfigHelpers.html)
- [GNUInstallDirs](https://cmake.org/cmake/help/latest/module/GNUInstallDirs.html)
- [CMake Dependencies — Using Dependencies Guide](https://cmake.org/cmake/help/latest/guide/using-dependencies/index.html)

---

[← Chapter 15](../Chapter-15/README.md) · [↑ C++ 목차](../README.md)
