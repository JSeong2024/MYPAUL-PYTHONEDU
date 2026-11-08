# Chapter 11. File I/O

파일 읽기·쓰기부터 경로 처리, CSV와 바이너리 데이터, 스트림 오류와 파일 저장까지 다룹니다. 작은 텍스트 파일을 읽는 예제에서 시작해 센서 측정 기록을 파일로 집계하는 프로그램을 작성합니다.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다. C++17에서 도입된 파일 시스템 기능도 사용하며, C++23 관련 기능은 참고로만 소개합니다.

<details>
<summary>선행 학습</summary>

- [Chapter 05. Functions](../Chapter-05/) — 함수와 반환값
- [Chapter 06. Arrays & Strings](../Chapter-06/) — 문자열 분리와 숫자 변환
- [Chapter 10. Standard Library (STL)](../Chapter-10/) — 컨테이너와 집계

</details>

## Contents

| Section | Topic |
|:---:|---|
| [11.1](#section-11-1) | File I/O & Streams — 파일 입출력과 스트림 |
| [11.2](#section-11-2) | Reading Lines — 한 줄씩 읽기 |
| [11.3](#section-11-3) | Writing & Appending — 파일 덮어쓰기와 추가 |
| [11.4](#section-11-4) | Stream States — 스트림의 오류 상태 |
| [11.5](#section-11-5) | Filesystem Paths — 경로 구성 |
| [11.6](#section-11-6) | File Status & Errors — 파일 상태 확인 |
| [11.7](#section-11-7) | Parsing Text — 텍스트를 숫자로 변환 |
| [11.8](#section-11-8) | CSV Records — CSV 레코드 다루기 |
| [11.9](#section-11-9) | Binary I/O — 바이너리 데이터 |
| [11.10](#section-11-10) | Endianness — 바이트 순서 |
| [11.11](#section-11-11) | RAII & File Lifetime — 파일과 객체 수명 |
| [11.12](#section-11-12) | Optional Results — 실패할 수 있는 파일 읽기 |
| [11.13](#section-11-13) | Temporary Files & Rename — 임시 파일을 이용한 저장 |
| [11.14](#section-11-14) | Streaming — 대용량 파일 순차 처리 |
| [11.15](#section-11-15) | UTF-8 Text — 문자열과 인코딩 |
| [11.16](#section-11-16) | Path Safety & I/O Boundaries — 경로 처리의 주의사항 |
| [11.17](#section-11-17) | Coding Practice |
| [11.18](#section-11-18) | Mini Project — Sensor CSV Report |
| [11.19](#section-11-19) | Quiz & Summary |

## Getting Started

아래 명령어는 `Chapter-11/` 폴더에서 실행하는 경우를 기준으로 합니다. 입력 파일 경로는 현재 작업 디렉터리를 기준으로 해석합니다.

**GCC**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_read_text_file.cpp -o read_text
./read_text examples/17_sensor_report/data/readings.csv
```

**Clang**

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic examples/01_read_text_file.cpp -o read_text
./read_text examples/17_sensor_report/data/readings.csv
```

**MSVC — Developer Command Prompt**

```bat
cl /nologo /std:c++20 /W4 /EHsc /utf-8 examples\01_read_text_file.cpp /Fe:read_text.exe
read_text.exe examples\17_sensor_report\data\readings.csv
```

Windows PowerShell에서는 실행 파일을 `.\read_text.exe` 형태로 실행합니다. 파일을 생성하는 예제는 원본 자료를 덮어쓸 수 있으므로 별도의 실습 폴더에서 실행하는 편이 안전합니다.

**학습 목표**

1. 파일 스트림을 사용해 데이터를 읽고 쓰며 오류를 확인할 수 있습니다.
2. `std::filesystem`으로 경로를 조합하고 파일 상태를 검사할 수 있습니다.
3. CSV 및 바이너리 데이터 형식의 기본 규칙을 설명할 수 있습니다.
4. 파일의 입력값과 저장 결과를 검증하는 프로그램을 작성할 수 있습니다.

<a id="section-11-1"></a>

## 11.1. File I/O & Streams — 파일 입출력과 스트림

`std::ifstream`과 `std::ofstream`은 각각 파일을 읽고 쓰는 스트림입니다. `<fstream>`은 이 두 타입을 제공합니다. 스트림은 파일의 내용을 순서대로 처리하면서 읽기·쓰기 결과를 상태값으로 알려줍니다. 파일이 존재하는지뿐 아니라 **열기, 읽기, 쓰기, 닫기의 실패**를 구분해야 합니다.

**예제 코드 — [01_read_text_file.cpp](./examples/01_read_text_file.cpp)**

```cpp
#include <fstream>
#include <iostream>
#include <string>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: read_text_file <path>\n"; return 1; }
    std::ifstream input{argv[1], std::ios::binary};
    if (!input) { std::cerr << "Cannot open file\n"; return 1; }
    std::string content;
    char character{};
    while (input.get(character)) { content.push_back(character); }
    if (input.bad()) { std::cerr << "Read error\n"; return 1; }
    std::cout << "Bytes: " << content.size() << '\n';
}
```

**컴파일 후 실행**

```bash
./read_text examples/17_sensor_report/data/readings.csv
```

**실행 결과**

```text
Bytes: 48
```

<a id="section-11-2"></a>

## 11.2. Reading Lines — 한 줄씩 읽기

`std::getline(input, line)`은 줄바꿈을 제외한 한 줄을 읽습니다. 성공한 경우에만 본문을 처리할 수 있으므로 `while (std::getline(...))`이 자연스럽습니다. 반면 `while (!input.eof())`는 읽기 실패를 확인하기 전에 본문을 실행할 수 있어 적절하지 않습니다.

**예제 코드 — [02_read_lines.cpp](./examples/02_read_lines.cpp)**

```cpp
#include <fstream>
#include <iostream>
#include <string>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: read_lines <path>\n"; return 1; }
    std::ifstream input{argv[1]};
    if (!input) { std::cerr << "Cannot open file\n"; return 1; }
    std::string line;
    int count{};
    while (std::getline(input,line)) { ++count; std::cout << count << ": " << line << '\n'; }
    if (input.bad()) { std::cerr << "Read error\n"; return 1; }
}
```

**컴파일 후 실행**

```bash
./read_lines examples/17_sensor_report/data/readings.csv
```

**실행 결과**

```text
1: SENSOR-A,22
```

<a id="section-11-3"></a>

## 11.3. Writing & Appending — 파일 덮어쓰기와 추가

`std::ofstream`의 기본 열기 방식은 기존 내용을 지울 수 있습니다. 기존 기록을 유지하며 뒤에 추가하려면 `std::ios::app`을 사용합니다. `close()`를 명시적으로 호출하면 종료 시점의 오류까지 확인할 수 있습니다.

**예제 코드 — [03_write_text_file.cpp](./examples/03_write_text_file.cpp)**

```cpp
#include <fstream>
#include <iostream>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: write_text_file <path>\n"; return 1; }
    std::ofstream output{argv[1], std::ios::trunc};
    if (!output) { std::cerr << "Cannot create file\n"; return 1; }
    output << "device,temperature\n" << "SENSOR-A,23\n";
    output.close();
    if (!output) { std::cerr << "Write error\n"; return 1; }
    std::cout << "Saved 2 lines\n";
}
```

**컴파일 후 실행**

```bash
./write_text_file output.csv
```

**실행 결과**

```text
Saved 2 lines
```

기존 파일 내용을 유지해야 하는 상황에서는 [`04_append_log.cpp`](./examples/04_append_log.cpp)의 `std::ios::app`을 사용합니다.


<a id="section-11-4"></a>

## 11.4. Stream States — 스트림의 오류 상태

`fail()`은 형식 변환 실패 등을, `bad()`는 심각한 입출력 오류를 나타냅니다. `eof()`는 입력 끝을 읽으려 한 뒤 설정됩니다. 실패한 스트림은 오류 상태를 해제하기 전에는 다음 추출이 진행되지 않습니다. `std::istringstream`은 `<sstream>`에서 제공하며 파일을 만들지 않고 문자열로 실험할 수 있습니다.

**예제 코드 — [05_stream_state.cpp](./examples/05_stream_state.cpp)**

```cpp
#include <iostream>
#include <sstream>
#include <string>
int main() {
    std::istringstream source{"12 abc"};
    int number{};
    source >> number;
    std::cout << "First: " << number << '\n';
    source >> number;
    std::cout << std::boolalpha << "Failed: " << source.fail() << '\n';
    source.clear();
    std::string invalid;
    source >> invalid;
    std::cout << "Token: " << invalid << '\n';
}
```

**실행 결과**

```text
First: 12
Failed: true
Token: abc
```

<a id="section-11-5"></a>

## 11.5. Filesystem Paths — 경로 구성

`std::filesystem::path`는 경로의 구성 요소를 다루는 타입입니다. `<filesystem>`을 포함하며 `/` 연산자로 폴더와 파일 이름을 조합합니다. 현재 작업 디렉터리(Current Working Directory)는 실행 파일의 위치와 반드시 같지 않습니다.

**예제 코드 — [06_filesystem_paths.cpp](./examples/06_filesystem_paths.cpp)**

```cpp
#include <filesystem>
#include <iostream>
int main() {
    const std::filesystem::path path = std::filesystem::path{"reports"} / "daily" / "result.csv";
    std::cout << "Filename: " << path.filename().string() << '\n';
    std::cout << "Extension: " << path.extension().string() << '\n';
}
```

**실행 결과**

```text
Filename: result.csv
Extension: .csv
```

<a id="section-11-6"></a>

## 11.6. File Status & Errors — 파일 상태 확인

`std::filesystem::exists(path, ec)`는 경로 존재 여부와 오류를 분리합니다. `<system_error>`의 `std::error_code`는 예외 대신 오류 정보를 받는 방법입니다. 조회 직후 다른 프로그램이 파일을 수정할 수 있으므로 **사전 확인만으로 이후 열기 성공을 보장할 수 없습니다.**

**예제 코드 — [07_filesystem_status.cpp](./examples/07_filesystem_status.cpp)**

```cpp
#include <filesystem>
#include <iostream>
#include <system_error>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: filesystem_status <path>\n"; return 1; }
    std::error_code ec;
    const bool exists = std::filesystem::exists(argv[1],ec);
    if (ec) { std::cerr << "Status error: " << ec.message() << '\n'; return 1; }
    std::cout << std::boolalpha << "Exists: " << exists << '\n';
}
```

**컴파일 후 실행**

```bash
./filesystem_status examples/17_sensor_report/data/readings.csv
```

**실행 결과**

```text
Exists: true
```

<a id="section-11-7"></a>

## 11.7. Parsing Text — 텍스트를 숫자로 변환

`std::from_chars()`는 `<charconv>`에 정의된 변환 기능입니다. 정수 파싱에서는 오류 코드와 반환된 종료 위치를 모두 검사해야 `25ms`와 같은 일부 변환을 거부할 수 있습니다. 빈 문자열, 부호와 범위 등 허용 조건도 별도로 명시해야 합니다.

**예제 코드 — [08_parse_integer_lines.cpp](./examples/08_parse_integer_lines.cpp)**

```cpp
#include <charconv>
#include <iostream>
#include <string>
#include <system_error>
int main() {
    const std::string text{"42"};
    int value{};
    const auto result = std::from_chars(text.data(),text.data()+text.size(),value);
    if (result.ec != std::errc{} || result.ptr != text.data()+text.size()) { return 1; }
    std::cout << "Reading: " << value << '\n';
}
```

**실행 결과**

```text
Reading: 42
```

<a id="section-11-8"></a>

## 11.8. CSV Records — CSV 레코드 다루기

CSV는 쉼표로 구분된 필드를 사용하지만 인용부호 안에는 쉼표가 들어갈 수 있습니다. 인용부호를 `""`로 이스케이프하는 규칙도 있습니다. 아래 예제는 **한 줄의 단순한 CSV**만 다룹니다. 따옴표의 위치, 줄바꿈을 포함한 필드, 서로 다른 인코딩까지 처리하는 완전한 CSV 파서는 아닙니다.

**예제 코드 — [09_csv_quoted_fields.cpp](./examples/09_csv_quoted_fields.cpp)**

```cpp
#include <iostream>
#include <string>
#include <vector>
std::vector<std::string> split_csv(const std::string& line) {
    std::vector<std::string> fields;
    std::string field;
    bool quoted{};
    for (std::size_t i{}; i < line.size(); ++i) {
        const char c = line[i];
        if (c == '"') {
            if (quoted && i+1 < line.size() && line[i+1] == '"') { field += '"'; ++i; }
            else { quoted = !quoted; }
        } else if (c == ',' && !quoted) { fields.push_back(field); field.clear(); }
        else { field += c; }
    }
    if (quoted) { return {}; }
    fields.push_back(field);
    return fields;
}
int main() {
    const auto fields = split_csv("SENSOR-A,\"north, west\",23");
    if (fields.size() != 3) { return 1; }
    std::cout << "Location: " << fields[1] << '\n';
}
```

**실행 결과**

```text
Location: north, west
```

<a id="section-11-9"></a>

## 11.9. Binary I/O — 바이너리 데이터

바이너리 형식은 바이트 순서를 명시해야 다른 환경에서도 같은 값으로 읽을 수 있습니다. `struct` 객체의 메모리를 그대로 저장하면 패딩, 정렬, 타입 크기와 바이트 순서가 달라 호환성을 보장하기 어렵습니다. `<cstdint>`의 고정 폭 정수 타입을 활용해 바이트별로 인코딩하는 편이 명확합니다.

**예제 코드 — [10_binary_packet.cpp](./examples/10_binary_packet.cpp)**

```cpp
#include <cstdint>
#include <iostream>
#include <vector>
int main() {
    const std::uint32_t value{0x12345678u};
    const std::vector<std::uint8_t> bytes{
        static_cast<std::uint8_t>((value >> 24) & 0xffu),
        static_cast<std::uint8_t>((value >> 16) & 0xffu),
        static_cast<std::uint8_t>((value >> 8) & 0xffu),
        static_cast<std::uint8_t>(value & 0xffu)};
    std::uint32_t restored{};
    for (const auto byte : bytes) { restored = (restored << 8) | byte; }
    std::cout << std::boolalpha << "Round trip: " << (value == restored) << '\n';
}
```

**실행 결과**

```text
Round trip: true
```

<a id="section-11-10"></a>

## 11.10. Endianness — 바이트 순서

엔디언(Endianness)은 여러 바이트로 된 정수에서 낮은 자리 바이트와 높은 자리 바이트를 어떤 순서로 저장하는지 나타냅니다. `<bit>`의 `std::endian`(C++20)은 실행 환경의 기본 바이트 순서를 확인할 수 있게 합니다. **파일 형식에는 호스트 환경과 별개로 바이트 순서를 고정하는 방식**이 적합합니다.

**예제 코드 — [11_endianness.cpp](./examples/11_endianness.cpp)**

```cpp
#include <bit>
#include <iostream>
int main() {
    if (std::endian::native == std::endian::little) { std::cout << "Little endian\n"; }
    else if (std::endian::native == std::endian::big) { std::cout << "Big endian\n"; }
    else { std::cout << "Mixed endian\n"; }
}
```

**실행 결과(일반적인 x86-64 환경)**

```text
Little endian
```

CPU 아키텍처에 따라 다른 값이 출력될 수 있습니다.

<a id="section-11-11"></a>

## 11.11. RAII & File Lifetime — 파일과 객체 수명

RAII(Resource Acquisition Is Initialization)는 자원의 수명을 객체의 수명과 연결하는 방식입니다. 파일 스트림도 범위를 벗어나면 소멸자가 파일을 닫습니다. 단, **닫기 오류까지 확인해야 하는 쓰기 작업**에서는 명시적으로 `close()`를 호출한 뒤 스트림 상태를 검사하는 것이 좋습니다.

**예제 코드 — [12_raii_file_scope.cpp](./examples/12_raii_file_scope.cpp)**

```cpp
#include <fstream>
#include <iostream>
#include <string>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: raii_file_scope <path>\n"; return 1; }
    { std::ofstream output{argv[1]};
      if (!output) { return 1; }
      output << "status=ready\n";
      output.close();
      if (!output) { return 1; }
    }
    std::ifstream input{argv[1]};
    std::string line;
    if (!std::getline(input,line)) { return 1; }
    std::cout << line << '\n';
}
```

**컴파일 후 실행**

```bash
./raii_file_scope output.txt
```

**실행 결과**

```text
status=ready
```

<a id="section-11-12"></a>

## 11.12. Optional Results — 실패할 수 있는 파일 읽기

`std::optional<T>`는 결과가 존재하지 않을 수 있음을 나타냅니다. `<optional>`에서 제공하며 C++17부터 사용할 수 있습니다. 오류의 **원인**까지 반환하고 싶다면 오류 코드나 별도 결과 구조체를 사용할 수 있습니다. C++23에는 `std::expected<T,E>`가 있지만 기본 예제에서는 사용하지 않습니다.

**예제 코드 — [13_expected_file_read.cpp](./examples/13_expected_file_read.cpp)**

```cpp
#include <fstream>
#include <iostream>
#include <optional>
#include <string>
std::optional<std::string> first_line(const std::string& path) {
    std::ifstream input{path};
    std::string line;
    if (!input || !std::getline(input,line)) { return std::nullopt; }
    return line;
}
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: first_line <path>\n"; return 1; }
    const auto line = first_line(argv[1]);
    if (!line) { std::cerr << "No first line\n"; return 1; }
    std::cout << "First line: " << *line << '\n';
}
```

**컴파일 후 실행**

```bash
./expected_file_read examples/17_sensor_report/data/readings.csv
```

**실행 결과**

```text
First line: SENSOR-A,22
```

<a id="section-11-13"></a>

## 11.13. Temporary Files & Rename — 임시 파일을 이용한 저장

기존 파일에 직접 쓰는 대신 별도의 파일에 작성한 후 이름을 변경하는 방법을 사용할 수 있습니다. 다만 `std::filesystem::rename()`의 **기존 대상 처리 방식은 운영체제에 따라 차이가 있을 수 있고**, 충돌·저장장치 동기화·전원 장애에 대한 완전한 보호를 보장하지 않습니다. 아래 예제는 원리를 설명하는 간단한 버전입니다.

**예제 코드 — [14_write_new_via_rename.cpp](./examples/14_write_new_via_rename.cpp)**

```cpp
#include <filesystem>
#include <fstream>
#include <iostream>
#include <system_error>
int main(int argc,char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: rename_save <path>\n"; return 1; }
    const std::filesystem::path target{argv[1]};
    const std::filesystem::path temporary = target.string() + ".tmp";
    if (std::filesystem::exists(temporary)) { std::cerr << "Temporary file exists\n"; return 1; }
    { std::ofstream file{temporary};
      if (!file) { return 1; }
      file << "reading=24\n";
      file.close();
      if (!file) { std::filesystem::remove(temporary); return 1; }
    }
    std::error_code ec;
    std::filesystem::rename(temporary,target,ec);
    if (ec) { std::filesystem::remove(temporary); std::cerr << "Rename failed\n"; return 1; }
    std::cout << "Saved report\n";
}
```

**컴파일 후 실행**

```bash
./write_new_via_rename saved.txt
```

**실행 결과**

```text
Saved report
```

<a id="section-11-14"></a>

## 11.14. Streaming — 대용량 파일 순차 처리

파일 전체를 메모리에 올릴 필요가 없다면 `std::getline`으로 한 줄씩 처리할 수 있습니다. 이 방식은 메모리 사용을 줄이지만, 아주 긴 단일 줄은 여전히 큰 메모리를 사용할 수 있으므로 외부 파일 처리에는 행 길이 제한이 필요할 수 있습니다.

**예제 코드 — [15_streaming_large_file.cpp](./examples/15_streaming_large_file.cpp)**

```cpp
#include <fstream>
#include <iostream>
#include <string>
int main(int argc,char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: count_lines <path>\n"; return 1; }
    std::ifstream input{argv[1]};
    if (!input) { return 1; }
    std::size_t count{};
    std::string line;
    while (std::getline(input,line)) { ++count; }
    if (input.bad()) { return 1; }
    std::cout << "Lines: " << count << '\n';
}
```

**컴파일 후 실행**

```bash
./streaming_large_file examples/17_sensor_report/data/readings.csv
```

**실행 결과**

```text
Lines: 4
```

<a id="section-11-15"></a>

## 11.15. UTF-8 Text — 문자열과 인코딩

UTF-8에서는 한 글자가 여러 바이트로 저장될 수 있습니다. `std::string::size()`가 반환하는 값은 문자 수가 아닌 **바이트 수**입니다. 콘솔의 출력 인코딩은 환경에 영향을 받으며 Unicode의 화면 표시 글자 수까지 정확히 계산하려면 별도 텍스트 처리 기능이 필요합니다.

**예제 코드 — [16_utf8_text.cpp](./examples/16_utf8_text.cpp)**

```cpp
#include <iostream>
#include <string>
int main() {
    const std::string text{"한글"};
    std::cout << "UTF-8 bytes: " << text.size() << '\n';
}
```

**실행 결과**

```text
UTF-8 bytes: 6
```

<a id="section-11-16"></a>

## 11.16. Path Safety & I/O Boundaries — 경로 처리의 주의사항

경로 문자열을 정규화하는 작업만으로 외부 입력 경로가 안전해지지는 않습니다. 심볼릭 링크와 파일 교체 경쟁 상황을 고려해야 합니다. 외부 입력으로 파일을 선택하는 경우 허용 디렉터리, 파일 크기, 접근 권한과 동시 접근 정책을 별도로 정의합니다.

**예제 코드 — [04_append_log.cpp](./examples/04_append_log.cpp)**

```cpp
#include <fstream>
#include <iostream>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: append_log <path>\n"; return 1; }
    std::ofstream output{argv[1], std::ios::app};
    if (!output) { std::cerr << "Cannot open log\n"; return 1; }
    output << "INFO,started\n";
    output.close();
    if (!output) { std::cerr << "Write error\n"; return 1; }
    std::cout << "Appended event\n";
}
```

**컴파일 후 실행**

```bash
./append_log output.log
```

**실행 결과**

```text
Appended event
```

<a id="section-11-17"></a>

## 11.17. Coding Practice

각 `exercises/` 파일에는 학생이 직접 완성할 부분을 `TODO`로 남겼습니다. 정답은 `solutions/`에서 확인할 수 있습니다.

| Exercise | 학습 내용 | 시작 코드 | 모범답안 |
|:---:|---|---|---|
| 01 | Temperature Summary | [01_temperature_summary.cpp](./exercises/01_temperature_summary.cpp) | [정답](./solutions/01_temperature_summary.cpp) |
| 02 | Event Log Summary | [02_event_log_summary.cpp](./exercises/02_event_log_summary.cpp) | [정답](./solutions/02_event_log_summary.cpp) |
| 03 | Inventory CSV | [03_inventory_csv.cpp](./exercises/03_inventory_csv.cpp) | [정답](./solutions/03_inventory_csv.cpp) |
| 04 | Binary U32 Reader | [04_binary_u32_reader.cpp](./exercises/04_binary_u32_reader.cpp) | [정답](./solutions/04_binary_u32_reader.cpp) |

### Exercise 01 — Temperature Summary

공백으로 구분된 온도 데이터를 읽고 개수·최소·최대·평균을 계산합니다. 온도는 -100~100이며 빈 파일과 잘못된 숫자는 거부합니다.

**완료 기준:** 지정된 값의 계산 및 출력이 정확하고, 오류 입력에서는 비정상 종료 코드로 처리해야 합니다.

**출력 예시**

```text
Average: 20.00
```

### Exercise 02 — Event Log Summary

한 줄당 하나의 이벤트(`INFO`, `WARN`, `ERROR`)를 읽고 이벤트 이름 순서로 빈도를 출력합니다.

**완료 기준:** 지정된 값의 계산 및 출력이 정확하고, 오류 입력에서는 비정상 종료 코드로 처리해야 합니다.

**출력 예시**

```text
INFO: 2
```

### Exercise 03 — Inventory CSV

`이름,수량` 형식의 단순 CSV 레코드를 읽고 중복 이름·잘못된 정수·범위를 검증합니다. 복잡한 인용부호 CSV는 대상이 아닙니다.

**완료 기준:** 지정된 값의 계산 및 출력이 정확하고, 오류 입력에서는 비정상 종료 코드로 처리해야 합니다.

**출력 예시**

```text
battery: 5
```

### Exercise 04 — Binary U32 Reader

정확히 4바이트인 파일을 읽고 Big-Endian 부호 없는 32비트 정수로 해석합니다.

**완료 기준:** 지정된 값의 계산 및 출력이 정확하고, 오류 입력에서는 비정상 종료 코드로 처리해야 합니다.

**출력 예시**

```text
Value: 305419896
```

**실습 코드 컴파일**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic exercises/01_temperature_summary.cpp -o temperature_summary
./temperature_summary examples/17_sensor_report/data/temperatures.txt
```

**자동 검증**

```bash
python tests/check.py
python tests/check.py --mode student --only exercise-01
```

첫 번째 명령어는 예제와 모범답안을 검증합니다. 두 번째 명령어는 수정한 Exercise 01을 확인합니다. 시작 코드의 TODO를 완성하지 않았다면 실패하는 것이 정상입니다.

<a id="section-11-18"></a>

## 11.18. Mini Project — Sensor CSV Report

장치명과 온도가 기록된 CSV를 읽어 통계를 만든 뒤, 다른 텍스트 파일에 저장합니다. 데이터의 형식 검증과 파일 출력 실패 처리까지 함수로 나누어 구현합니다.

**입력 파일** — [`readings.csv`](./examples/17_sensor_report/data/readings.csv)

```text
SENSOR-A,22
SENSOR-B,18
SENSOR-A,24
SENSOR-C,20
```

**요구사항**

1. 각 행을 `장치명,온도` 형식으로 읽습니다.
2. 온도 범위는 -100~100이며, 잘못된 입력이 있으면 보고서를 생성하지 않습니다.
3. 측정 개수·장치 수·최솟값·최댓값·평균과 장치별 건수를 계산합니다.
4. 결과 파일은 입력 파일과 다른 경로에 저장합니다.
5. 저장 후 스트림의 오류 상태까지 검사합니다.

**완료 기준:** 정상 CSV에서 다음 보고서를 생성하고, 숫자 변환 오류·빈 파일·경로 오류에는 실패를 반환합니다.

**생성되는 보고서**

```text
Samples: 4
Devices: 3
Min: 18.00
Max: 24.00
Average: 21.00
SENSOR-A: 2
SENSOR-B: 1
SENSOR-C: 1
```

**프로젝트 파일**

- [학생용 시작 코드](./project/report.cpp) · [헤더](./project/report.hpp) · [실행 코드](./project/main.cpp)
- [전체 예제 및 정답 코드](./examples/17_sensor_report/report.cpp)
- [CMake 프로젝트](./examples/17_sensor_report/CMakeLists.txt)

**GCC — 다중 파일 컴파일**

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic project/main.cpp project/report.cpp -o sensor_report
./sensor_report project/readings.csv result.txt
```

**CMake — 완성 예제 검증**

```bash
cmake -S examples/17_sensor_report -B build/ch11
cmake --build build/ch11
ctest --test-dir build/ch11 --output-on-failure
```

`project/`는 학생용 시작 코드이며, `examples/17_sensor_report/`는 완성된 예제입니다. 파일 경로는 실행 위치를 기준으로 해석합니다.

<a id="section-11-19"></a>

## 11.19. Quiz & Summary

### Quiz

**1.** `std::getline(input, line)`을 `while`의 조건으로 사용하는 이유는?

- A. 파일을 항상 빠르게 읽기 위해
- B. 읽기가 성공한 행만 처리하기 위해
- C. 파일을 자동으로 삭제하기 위해

<details>
<summary>정답 및 해설</summary>

B. 조건식에서 읽기 성공 여부를 확인한 뒤 본문을 실행합니다. EOF나 읽기 실패 후 이전 데이터를 다시 처리하는 실수를 줄일 수 있습니다.

</details>

**2.** `std::ofstream output{path};`로 기존 파일을 열면 어떤 위험이 있나요?

<details>
<summary>정답 및 해설</summary>

기본 모드에서는 기존 내용이 비워질 수 있습니다. 기존 로그 뒤에 추가하려면 `std::ios::app`을 사용합니다.

</details>

**3.** 아래 중 `std::filesystem::path`가 제공하는 기능은?

- A. 경로 구성 요소 조합
- B. 모든 경로의 보안 검증
- C. 파일 데이터 자동 암호화

<details>
<summary>정답 및 해설</summary>

A. 파일 이름, 확장자 등을 다루며 `/`로 경로를 조합할 수 있습니다. 보안 검증이나 암호화까지 수행하지는 않습니다.

</details>

**4.** `std::from_chars()`에서 오류 코드 외에 반드시 확인할 것은?

<details>
<summary>정답 및 해설</summary>

변환 종료 포인터가 입력 끝을 가리키는지 확인해야 합니다. `23xyz`와 같은 부분 변환을 거부하려면 전체 입력 소비 여부를 검사합니다.

</details>

**5.** CSV 필드 안에 쉼표가 들어가면 어떻게 표현할 수 있나요?

<details>
<summary>정답 및 해설</summary>

일반적인 CSV에서는 인용부호로 필드를 감쌉니다. 예를 들어 `"north,west"`는 쉼표를 포함한 한 필드입니다. 실제 파서는 따옴표 이스케이프와 줄바꿈 규칙도 처리해야 합니다.

</details>

**6.** 바이너리 파일에 `struct`의 메모리를 그대로 기록하면 이식성이 떨어지는 이유는?

<details>
<summary>정답 및 해설</summary>

패딩, 정렬, 타입 크기, 바이트 순서가 환경에 따라 달라질 수 있습니다. 파일 형식의 바이트 순서를 정하고 각 필드를 명시적으로 인코딩하는 방법이 안전합니다.

</details>

**7.** `close()`에 성공했다면 전원 장애 후에도 기록은 반드시 남아 있나요?

- A. 예
- B. 아니요

<details>
<summary>정답 및 해설</summary>

B. `close()`가 성공해도 운영체제와 저장장치 수준의 내구성까지 보장하지는 않습니다.

</details>

**8.** `std::optional<std::string>`이 알려주지 못하는 정보는?

<details>
<summary>정답 및 해설</summary>

값의 존재 여부는 표현하지만 파일이 없었는지, 권한이 거부되었는지 같은 구체적인 실패 사유는 직접 담지 않습니다. 별도의 오류 구조체가 필요할 수 있습니다.

</details>

**9.** `std::ios::app`의 용도로 올바른 것은?

- A. 파일의 끝에 내용 추가
- B. 파일을 읽기 전용으로 열기
- C. 파일 이름 변경

<details>
<summary>정답 및 해설</summary>

A. 기존 데이터를 유지하고 파일 끝에 이어 쓰기 위한 모드입니다.

</details>

**10.** 대용량 파일을 한 줄씩 처리하면 언제나 메모리 사용이 일정할까요?

<details>
<summary>정답 및 해설</summary>

그렇지는 않습니다. 한 줄의 길이가 매우 길면 해당 줄의 문자열이 커질 수 있습니다. 입력 행 길이 제한이 필요한 이유입니다.

</details>

**11.** `std::filesystem::exists()`를 호출하면 바로 다음 파일 열기가 보장되나요?

<details>
<summary>정답 및 해설</summary>

보장되지 않습니다. 호출 사이에 다른 프로세스가 파일을 변경하거나 제거할 수 있습니다. 실제 열기 결과를 반드시 확인해야 합니다.

</details>

**12.** `std::string::size()`로 UTF-8의 글자 수를 알 수 있나요?

- A. 항상 가능합니다
- B. 바이트 수만 알 수 있습니다

<details>
<summary>정답 및 해설</summary>

B. UTF-8은 문자 하나가 여러 바이트일 수 있어 `size()`는 화면 글자 수가 아니라 바이트 수를 반환합니다.

</details>

### Summary

- **파일 스트림:** 읽기·쓰기 성공 여부를 확인하고 필요한 경우 `close()` 상태까지 검사합니다.
- **파일 경로:** `std::filesystem`으로 경로를 구성하지만 파일 접근 결과는 별도로 확인합니다.
- **텍스트 파싱:** 숫자 변환과 필드 형식을 구분해 검증합니다.
- **CSV와 바이너리:** 데이터 형식의 범위를 명시하고 파일 레이아웃에 의존하지 않습니다.
- **RAII:** 파일 스트림의 객체 수명으로 자원 정리를 관리합니다.
- **대용량 데이터:** 전체 파일 대신 순차적으로 읽어 처리할 수 있습니다.

### References

- [cppreference — File streams](https://en.cppreference.com/w/cpp/io/basic_ifstream)
- [cppreference — Filesystem](https://en.cppreference.com/w/cpp/filesystem)
- [cppreference — `std::from_chars`](https://en.cppreference.com/w/cpp/utility/from_chars)
- [cppreference — `std::endian`](https://en.cppreference.com/w/cpp/types/endian)

---

[← C++ 목차](../README.md#contents) · [이전 Chapter — Standard Library (STL)](../Chapter-10/)
