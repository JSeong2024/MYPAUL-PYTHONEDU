# Chapter 11. File I/O

C++23에서 파일을 열고 데이터를 읽고 쓰는 방법을 다룹니다. Stream 상태 검증, 경로 처리, CSV·Binary 형식, 오류 전달, 임시 파일을 활용한 저장 방식 및 파일 입출력 테스트까지 살펴봅니다.

본 자료는 **C++23(ISO/IEC 14882:2024)** 을 기준으로 작성되었습니다. 예제는 GCC 14 이상 또는 필요한 C++23 표준 라이브러리를 지원하는 컴파일러 환경을 권장합니다. 파일의 인코딩과 경로 동작은 운영체제에 따라 달라질 수 있습니다.

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [11.1](#section-11-1) | File I/O와 Stream의 역할 |
| [11.2](#section-11-2) | 파일 열기와 텍스트 읽기 — `std::ifstream` |
| [11.3](#section-11-3) | 한 줄씩 읽기 — `std::getline` |
| [11.4](#section-11-4) | 파일 쓰기와 추가 — `std::ofstream` |
| [11.5](#section-11-5) | Stream 상태와 오류 구분 |
| [11.6](#section-11-6) | 경로 구성 — `std::filesystem::path` |
| [11.7](#section-11-7) | 파일 상태와 메타데이터 조회 |
| [11.8](#section-11-8) | 문자열과 숫자 변환 — `std::from_chars` |
| [11.9](#section-11-9) | CSV 형식과 필드 Parsing |
| [11.10](#section-11-10) | Binary I/O와 데이터 레이아웃 |
| [11.11](#section-11-11) | Byte Order와 이식 가능한 저장 형식 |
| [11.12](#section-11-12) | RAII, Flush 및 파일 닫기 |
| [11.13](#section-11-13) | 오류 반환 — `std::expected` |
| [11.14](#section-11-14) | 임시 파일과 이름 변경 — 안전한 저장 범위 |
| [11.15](#section-11-15) | UTF-8과 텍스트 인코딩 |
| [11.16](#section-11-16) | 경로 검증과 보안 고려 사항 |
| [11.17](#section-11-17) | 대용량 파일과 Streaming 처리 |
| [11.18](#section-11-18) | Mini Project — Sensor CSV Report |
| [11.19](#section-11-19) | Coding Practice |
| [11.20](#section-11-20) | Quiz & Summary |

---

<a id="section-11-1"></a>

## 11.1. File I/O와 Stream의 역할

파일 입출력(File Input/Output, File I/O)은 프로그램의 데이터를 파일에 보관하거나 저장된 데이터를 다시 읽는 작업입니다. C++에서는 **스트림(Stream)**을 통해 파일 및 콘솔 입출력을 같은 인터페이스로 다룰 수 있습니다.

| 기능 | 대표 형식 | 헤더 | 용도 |
|---|---|---|---|
| 파일 읽기 | `std::ifstream` | `<fstream>` | 입력 파일에서 데이터 읽기 |
| 파일 쓰기 | `std::ofstream` | `<fstream>` | 새로운 파일 생성 또는 기존 파일 수정 |
| 파일 읽기·쓰기 | `std::fstream` | `<fstream>` | 같은 Stream으로 읽기와 쓰기 수행 |
| 파일 경로 | `std::filesystem::path` | `<filesystem>` | 파일·폴더 경로 조합 및 분석 |
| 문자열 Stream | `std::istringstream`, `std::ostringstream` | `<sstream>` | 메모리 내 문자열을 Stream처럼 처리 |

**기본 흐름:** 파일 열기 → 데이터 처리 → 오류 확인 → 파일 닫기.

File I/O는 처리할 데이터의 **형식(Format)**과 **인코딩(Encoding)**을 구분해야 합니다. 텍스트 파일의 내용은 문자열로 해석하지만, Binary 파일은 정해진 바이트(Byte) 구조에 따라 읽고 써야 합니다.

- **텍스트 모드(Text Mode):** 구현 및 운영체제의 규칙에 따라 줄바꿈 등이 변환될 수 있는 방식
- **바이너리 모드(Binary Mode):** 텍스트 변환 없이 바이트 단위로 입출력하는 방식
- **동기화·내구성(Durability):** 파일을 닫는 것과 물리적 저장장치에 완전히 기록되는 것은 별개의 문제

C++ 표준 Stream은 하드웨어 동기화나 여러 프로세스의 동시 파일 수정까지 자동으로 보장하지 않습니다.

---

<a id="section-11-2"></a>

## 11.2. 파일 열기와 텍스트 읽기 — `std::ifstream`

`std::ifstream`은 파일을 입력 Stream으로 엽니다. 파일이 없거나 접근 권한이 없다면 생성 직후 `if (!input)` 등으로 열기 실패를 확인할 수 있습니다.

아래 코드는 경로를 명령줄 인수(Command-Line Argument)로 전달받습니다. 파일 전체를 메모리로 읽으므로 **크기를 제한할 수 있는 작은 텍스트 파일**에 적합합니다.

**예제 코드 — [01_read_text_file.cpp](./examples/01_read_text_file.cpp)**

```cpp
#include <fstream>
#include <iterator>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: read_text_file <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) {
        std::println(stderr, "Cannot open input file");
        return 1;
    }
    const std::string content{std::istreambuf_iterator<char>{input},
                              std::istreambuf_iterator<char>{}};
    if (input.bad()) {
        std::println(stderr, "File read failed");
        return 1;
    }
    std::println("Bytes read: {}", content.size());
}
```

**실행 결과**

```text
Bytes read: 17
```

**실행 방법** — `Chapter-11/` 경로 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic examples/01_read_text_file.cpp -o read_text
./read_text data/demo_lines.txt
```

기존 데이터 크기에 대한 제한 없이 전체 파일을 메모리에 올리는 방식은 대용량 파일에 적합하지 않습니다. 이런 경우 11.17의 Streaming 방식을 사용합니다. `input.bad()`는 저수준 읽기 실패를 확인하는 데 사용합니다.

---

<a id="section-11-3"></a>

## 11.3. 한 줄씩 읽기 — `std::getline`

텍스트 파일을 한 행씩 처리할 때 `std::getline()`을 사용합니다. 줄바꿈 문자를 소비하고 해당 줄의 내용을 `std::string`에 저장합니다.

**주의:** `while (!input.eof())`처럼 EOF(End of File)를 먼저 검사하는 반복문은 마지막 줄을 중복 처리할 수 있습니다. `while (std::getline(input, line))`처럼 **읽기 성공 여부를 조건으로** 사용하는 방식이 안전합니다.

**예제 코드 — [02_read_lines.cpp](./examples/02_read_lines.cpp)**

```cpp
#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: read_lines <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) {
        std::println(stderr, "Cannot open file");
        return 1;
    }
    std::string line;
    std::size_t count{};
    while (std::getline(input, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        ++count;
        std::println("{}: {}", count, line);
    }
    if (input.bad()) {
        std::println(stderr, "Read error");
        return 1;
    }
    std::println("Lines: {}", count);
}
```

**실행 결과**

```text
1: alpha
2: beta
3: gamma
Lines: 3
```

- **빈 줄:** 길이가 0인 문자열로 정상 처리
- **마지막 줄:** 끝에 개행 문자가 없어도 읽기 가능
- **CRLF:** Linux 등에서 `
`이 남는 경우를 고려하여 제거
- **오류:** 반복문 종료 후 `bad()`를 확인

파일 끝에 도달해 발생하는 `eofbit`/`failbit`는 통상적인 종료 상태일 수 있습니다. Stream이 끝났다는 사실만으로 물리적 오류라고 판단해서는 안 됩니다.

---

<a id="section-11-4"></a>

## 11.4. 파일 쓰기와 추가 — `std::ofstream`

`std::ofstream`은 파일을 저장할 때 사용합니다. 열기 모드(Open Mode)에 따라 기존 내용을 덮어쓰거나 파일 끝에 내용을 추가합니다.

| 옵션 | 의미 | 주의 |
|---|---|---|
| `std::ios::trunc` | 기존 파일 내용을 비우고 새로 쓰기 | 데이터 손실 가능 |
| `std::ios::app` | 모든 쓰기를 파일 끝에 추가 | 동시 쓰기 시 레코드 단위 원자성은 별도 보장 필요 |
| `std::ios::binary` | Binary 모드 | 바이트 형식을 직접 정의해야 함 |
| `std::ios::in` / `out` | 읽기 / 쓰기 | 필요한 조합에 맞춰 사용 |

**덮어쓰기 예제**

**예제 코드 — [03_write_text_file.cpp](./examples/03_write_text_file.cpp)**

```cpp
#include <fstream>
#include <print>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: write_text_file <output-path>");
        return 1;
    }
    std::ofstream output{argv[1], std::ios::out | std::ios::trunc};
    if (!output) {
        std::println(stderr, "Cannot create output file");
        return 1;
    }
    output << "device,temperature_c\n";
    output << "robot-01,23\n";
    output.close();
    if (!output) {
        std::println(stderr, "Write or close failed");
        return 1;
    }
    std::println("File written");
}
```

**실행 결과**

```text
File written
```

```bash
g++ -std=c++23 examples/03_write_text_file.cpp -o write_text
./write_text output.csv
```

`output.csv`가 이미 존재하면 내용이 교체됩니다. 테스트에서는 별도의 파일 이름을 사용합니다.

**추가 쓰기(Append) 예제**

**예제 코드 — [04_append_log.cpp](./examples/04_append_log.cpp)**

```cpp
#include <fstream>
#include <print>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: append_log <path>");
        return 1;
    }
    std::ofstream output{argv[1], std::ios::app};
    if (!output) {
        std::println(stderr, "Cannot open log file");
        return 1;
    }
    output << "INFO|robot-01|heartbeat\n";
    output.close();
    if (!output) {
        std::println(stderr, "Append failed");
        return 1;
    }
    std::println("Log appended");
}
```

**실행 결과**

```text
Log appended
```

```bash
g++ -std=c++23 examples/04_append_log.cpp -o append_log
./append_log events.log
```

위 프로그램을 두 번 실행하면 로그가 두 행 추가됩니다. 이미 존재하는 로그가 중요한 경우 파일 회전(Log Rotation), 동시 접근, 장애 복구 규칙을 함께 설계해야 합니다.

---

<a id="section-11-5"></a>

## 11.5. Stream 상태와 오류 구분

Stream은 읽기·쓰기 성공 상태를 여러 플래그로 관리합니다.

| 상태 | 설명 | 대표 검사 |
|---|---|---|
| `goodbit` | 오류 플래그 없음 | `good()` |
| `eofbit` | 입력 끝에 도달 | `eof()` |
| `failbit` | 요청된 입력 작업이 실패 | `fail()` |
| `badbit` | Stream 버퍼 등에서 심각한 오류 | `bad()` |

`operator bool()`은 `failbit` 또는 `badbit` 설정 여부로 Stream 사용 가능 상태를 판단합니다. `eofbit`가 설정되었다는 것만으로 `badbit`가 설정되는 것은 아닙니다.

읽기 반복문 종료 시 **정상적인 파일 끝**과 **입력 오류**를 구분해야 합니다.

**예제 코드 — [05_stream_state.cpp](./examples/05_stream_state.cpp)**

```cpp
#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: stream_state <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) {
        std::println(stderr, "Open failed");
        return 1;
    }
    std::string line;
    std::size_t lines{};
    while (std::getline(input, line)) {
        ++lines;
    }
    if (input.bad()) {
        std::println(stderr, "Physical read error");
        return 1;
    }
    std::println("Lines: {}, EOF reached: {}", lines, input.eof());
}
```

**실행 결과**

```text
Lines: 3, EOF reached: true
```

이 예제에서 마지막 `getline()`이 더 이상 읽을 행을 찾지 못하면 EOF 상태가 설정됩니다. 입력 도중 오류가 발생했다면 `bad()` 등을 통해 판단합니다.

`std::ifstream`을 열지 못한 경우, 데이터 형식이 틀린 경우, 디스크 오류가 발생한 경우는 서로 다른 문제입니다. 예외(Exception)를 사용하지 않는 코드에서도 상태 검사는 필수입니다.

---

<a id="section-11-6"></a>

## 11.6. 경로 구성 — `std::filesystem::path`

경로(Path)를 문자열로 연결하면 `/`, `\` 등 운영체제별 구분자를 직접 처리해야 할 수 있습니다. `std::filesystem::path`는 경로 요소를 조합하고 분석하는 표준 형식입니다.

**예제 코드 — [06_filesystem_paths.cpp](./examples/06_filesystem_paths.cpp)**

```cpp
#include <filesystem>
#include <print>

int main() {
    namespace fs = std::filesystem;
    const fs::path file = fs::path{"data"} / "logs" / "robot.csv";
    std::println("File name: {}", file.filename().string());
    std::println("Extension: {}", file.extension().string());
    std::println("Parent: {}", file.parent_path().generic_string());
}
```

**실행 결과**

```text
File name: robot.csv
Extension: .csv
Parent: data/logs
```

| 함수 | 역할 |
|---|---|
| `filename()` | 마지막 경로 요소 |
| `parent_path()` | 상위 경로 |
| `extension()` | 확장자 |
| `stem()` | 확장자를 제외한 이름 |
| `operator/` | 경로 구성 요소 결합 |
| `lexically_normal()` | 파일 시스템 접근 없이 경로 문자열 정규화 |

**상대 경로(Relative Path)**는 현재 작업 디렉터리(Current Working Directory)를 기준으로 해석됩니다. 실행 파일의 위치와 작업 디렉터리는 반드시 같지 않으므로, 예제 실행 경로를 문서에 명시합니다.

경로 출력에 사용하는 `path.string()`의 문자 인코딩은 플랫폼에 따라 다를 수 있습니다. 특히 Windows에서 비ASCII 경로를 다룰 때는 기본 문자열 인코딩을 무조건 UTF-8로 가정하지 않습니다.

---

<a id="section-11-7"></a>

## 11.7. 파일 상태와 메타데이터 조회

`std::filesystem`은 파일 존재 여부, 종류, 크기, 디렉터리 상태 등을 확인하는 기능을 제공합니다. 파일 시스템 작업은 권한 부족, 삭제, 경로 변경 등으로 실패할 수 있으므로 오류를 다뤄야 합니다.

동일한 기능에 **예외 발생 오버로드**와 `std::error_code`를 받는 **비예외 오버로드**가 제공되는 경우가 많습니다. 예측 가능한 실패가 일반적인 검사 루틴에는 후자가 유용합니다.

**예제 코드 — [07_filesystem_status.cpp](./examples/07_filesystem_status.cpp)**

```cpp
#include <filesystem>
#include <print>
#include <system_error>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: filesystem_status <path>");
        return 1;
    }
    namespace fs = std::filesystem;
    const fs::path path{argv[1]};
    std::error_code ec;
    const fs::file_status status = fs::status(path, ec);
    if (ec) {
        std::println(stderr, "Status failed: {}", ec.message());
        return 1;
    }
    if (!fs::is_regular_file(status)) {
        std::println(stderr, "Not a regular file");
        return 1;
    }
    const auto size = fs::file_size(path, ec);
    if (ec) {
        std::println(stderr, "Size failed: {}", ec.message());
        return 1;
    }
    std::println("Size: {} bytes", size);
}
```

**실행 결과**

```text
Size: 17 bytes
```

```bash
g++ -std=c++23 examples/07_filesystem_status.cpp -o fs_status
./fs_status data/demo_lines.txt
```

- `status(path, ec)`: 대상 파일의 상태 조회
- `is_regular_file(status)`: 일반 파일 여부 확인
- `file_size(path, ec)`: 크기 조회와 오류 코드 확인

파일이 존재한다는 검사를 통과한 후에도 사용 직전에 삭제될 수 있습니다. 이러한 시간차 검사(Time-of-Check to Time-of-Use, TOCTOU)는 경로 검증만으로 완전히 막을 수 없습니다.

---

<a id="section-11-8"></a>

## 11.8. 문자열과 숫자 변환 — `std::from_chars`

파일에서 읽은 값은 처음부터 숫자가 아니라 **문자열**입니다. 정수로 해석하려면 파싱(Parsing)이 필요합니다.

`std::from_chars`는 로캘(Locale)에 덜 의존하며, 반환된 종료 포인터와 오류 코드를 직접 검사할 수 있습니다. 성공해도 입력의 일부만 읽었을 수 있으므로 **전체 입력 소비 여부**를 확인해야 합니다.

| 입력 | 정수로 해석 | 설명 |
|---|---|---|
| `"42"` | 성공 | 전체 문자열 처리 |
| `"42ms"` | 실패 처리 권장 | 일부만 읽음 |
| `"99999999999999999999"` | 실패 | 범위 초과 |
| `""` | 실패 | 빈 문자열 |

**예제 코드 — [08_parse_integer_lines.cpp](./examples/08_parse_integer_lines.cpp)**

```cpp
#include <charconv>
#include <fstream>
#include <print>
#include <string>
#include <string_view>

[[nodiscard]] bool parse_int(std::string_view text, int& value) {
    if (text.empty()) return false;
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    return error == std::errc{} && end == text.data() + text.size();
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: parse_integer_lines <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::string line;
    int value{};
    std::size_t line_number{};
    while (std::getline(input, line)) {
        ++line_number;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (!parse_int(line, value)) {
            std::println(stderr, "Invalid integer at line {}", line_number);
            return 1;
        }
        std::println("Value: {}", value);
    }
    if (input.bad()) return 1;
}
```

**실행 결과**

```text
Value: 12
Value: -4
Value: 0
```

```bash
g++ -std=c++23 examples/08_parse_integer_lines.cpp -o parse_ints
./parse_ints data/demo_readings.txt
```

`std::from_chars`는 정수 변환에서 앞뒤 공백을 자동 제거하지 않습니다. 입력 형식에서 공백 허용 여부를 먼저 정하고, 허용한다면 별도 처리해야 합니다. 데이터를 단순히 `std::stoi()`로 변환하고 예외만 무시하는 방식은 입력 검증에 불충분할 수 있습니다.

---

<a id="section-11-9"></a>

## 11.9. CSV 형식과 필드 Parsing

CSV(Comma-Separated Values)는 쉼표로 필드를 구분하는 텍스트 형식입니다. 그러나 필드에 쉼표나 큰따옴표가 들어갈 수 있으므로 `find(',')` 한 번만으로 모든 CSV를 올바르게 분리할 수는 없습니다.

| 입력 행 | 필드 해석 |
|---|---|
| `sensor,23.5` | `sensor`, `23.5` |
| `"sensor, A",23.5` | `sensor, A`, `23.5` |
| `"say ""hello""",ok` | `say "hello"`, `ok` |

**예제 코드**는 큰따옴표로 둘러싼 필드와 `""` Escape를 처리합니다. 단, **필드 내부 줄바꿈, BOM, 다양한 CSV 확장 규칙은 지원하지 않는 축약형 Parser**입니다. 지원 범위를 명시하지 않은 단순 파서는 외부 CSV 파일을 처리할 때 문제가 될 수 있습니다.

**예제 코드 — [09_csv_quoted_fields.cpp](./examples/09_csv_quoted_fields.cpp)**

```cpp
#include <fstream>
#include <print>
#include <string>
#include <string_view>
#include <vector>
#include <utility>

// 한 행을 파싱하는 예제. 필드 내부 줄바꿈은 지원하지 않음.
[[nodiscard]] bool parse_csv_line(std::string_view line, std::vector<std::string>& fields) {
    fields.clear();
    std::size_t i{};
    while (true) {
        std::string field;
        if (i < line.size() && line[i] == '"') {
            ++i;
            bool closed = false;
            while (i < line.size()) {
                if (line[i] == '"') {
                    if (i + 1 < line.size() && line[i + 1] == '"') {
                        field.push_back('"');
                        i += 2;
                    } else {
                        ++i;
                        closed = true;
                        break;
                    }
                } else {
                    field.push_back(line[i++]);
                }
            }
            if (!closed || (i < line.size() && line[i] != ',')) return false;
        } else {
            while (i < line.size() && line[i] != ',') {
                if (line[i] == '"') return false;
                field.push_back(line[i++]);
            }
        }
        fields.push_back(std::move(field));
        if (i == line.size()) return true;
        ++i; // 쉼표 건너뛰기
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: csv_quoted_fields <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::string line;
    std::size_t line_number{};
    std::vector<std::string> fields;
    while (std::getline(input, line)) {
        ++line_number;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (!parse_csv_line(line, fields)) {
            std::println(stderr, "Invalid CSV at line {}", line_number);
            return 1;
        }
        std::println("Line {} has {} fields", line_number, fields.size());
    }
    if (input.bad()) return 1;
}
```

**실행 결과**

```text
Line 1 has 2 fields
Line 2 has 2 fields
```

```bash
g++ -std=c++23 examples/09_csv_quoted_fields.cpp -o csv_fields
./csv_fields data/demo_quoted.csv
```

다른 프로그램에서 제공받은 CSV를 일반적으로 처리해야 한다면 표준적인 CSV Parser 라이브러리를 검토합니다. 데이터에 필드 내부 줄바꿈이 허용되는 경우 한 줄씩만 읽는 구현으로는 완전한 처리가 불가능합니다.

---

<a id="section-11-10"></a>

## 11.10. Binary I/O와 데이터 레이아웃

Binary I/O는 바이트 단위로 저장하는 방식입니다. 텍스트 변환이 없다고 해서 C++ 객체를 메모리에 배치된 그대로 저장해도 안전하다는 뜻은 아닙니다.

- **Padding:** 구조체 멤버 사이에 생길 수 있는 빈 영역
- **Alignment:** 메모리 정렬 요구사항
- **Byte Order:** 여러 바이트로 이루어진 값의 저장 순서
- **Versioning:** 파일 포맷 변경을 구분하는 버전 정보

다음 예제는 8바이트로 고정된 파일 포맷을 명시적으로 구성합니다.

| Offset | 크기 | 값 | 의미 |
|---:|---:|---|---|
| 0 | 4 byte | `SNS1` | 파일 식별자(Magic Number) |
| 4 | 1 byte | `0x01` | 버전 |
| 5 | 3 byte | `00 01 2C` | 24-bit Big Endian 정수 300 |

**예제 코드 — [10_binary_packet.cpp](./examples/10_binary_packet.cpp)**

```cpp
#include <array>
#include <cstdint>
#include <fstream>
#include <print>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: binary_packet <path>");
        return 1;
    }
    // 명시적 8-byte 포맷: Magic(4) + Version(1) + Value(Big-Endian, 3)
    constexpr std::array<unsigned char, 8> packet{'S', 'N', 'S', '1', 1, 0, 1, 44};
    {
        std::ofstream output{argv[1], std::ios::binary | std::ios::trunc};
        if (!output) return 1;
        output.write(reinterpret_cast<const char*>(packet.data()),
                     static_cast<std::streamsize>(packet.size()));
        output.close();
        if (!output) return 1;
    }
    std::array<unsigned char, 8> restored{};
    std::ifstream input{argv[1], std::ios::binary};
    if (!input.read(reinterpret_cast<char*>(restored.data()),
                    static_cast<std::streamsize>(restored.size()))) return 1;
    if (input.peek() != std::char_traits<char>::eof()) return 1;
    if (!input.eof() && input.bad()) return 1;
    if (restored != packet) return 1;
    const std::uint32_t value = (std::uint32_t{restored[5]} << 16) |
                                (std::uint32_t{restored[6]} << 8) |
                                 std::uint32_t{restored[7]};
    std::println("Version: {}, Value: {}", restored[4], value);
}
```

**실행 결과**

```text
Version: 1, Value: 300
```

```bash
g++ -std=c++23 examples/10_binary_packet.cpp -o binary_packet
./binary_packet sample_packet.bin
```

출력 파일 크기가 정확히 8바이트인지 확인할 수 있습니다. 파일 버전이나 길이가 맞지 않으면 읽기를 중단하는 검증이 필요하며, `reinterpret_cast`를 사용하는 부분은 **원시 바이트 버퍼를 Stream에 전달**하기 위한 것이지 임의 구조체를 직렬화(Serialization)하기 위한 것이 아닙니다.

---

<a id="section-11-11"></a>

## 11.11. Byte Order와 이식 가능한 저장 형식

바이트 순서(Byte Order, Endianness)는 여러 바이트로 이루어진 정수의 저장 순서입니다. 메모리에서 리틀 엔디언(Little Endian)을 사용하는 CPU라도 파일 형식에서 빅 엔디언(Big Endian)을 지정할 수 있습니다.

네트워크 순서를 비롯한 Binary 규격에서는 바이트 순서를 문서에 명시합니다. `std::endian`은 현재 시스템의 기본 Byte Order를 확인할 때 사용할 수 있습니다.

**예제 코드 — [11_endianness.cpp](./examples/11_endianness.cpp)**

```cpp
#include <array>
#include <bit>
#include <cstdint>
#include <print>

int main() {
    constexpr std::uint32_t number{0x01020304};
    const std::array<std::uint8_t, 4> bytes{
        static_cast<std::uint8_t>(number >> 24),
        static_cast<std::uint8_t>(number >> 16),
        static_cast<std::uint8_t>(number >> 8),
        static_cast<std::uint8_t>(number)
    };
    std::println("Network bytes: {:02X} {:02X} {:02X} {:02X}",
                 bytes[0], bytes[1], bytes[2], bytes[3]);
    if constexpr (std::endian::native == std::endian::little) {
        std::println("Host: Little Endian");
    } else if constexpr (std::endian::native == std::endian::big) {
        std::println("Host: Big Endian");
    } else {
        std::println("Host: Mixed/Other Endian");
    }
}
```

**실행 결과**

```text
Network bytes: 01 02 03 04
Host: Little Endian
```

**참고:** 위 결과의 두 번째 줄은 Little Endian 시스템의 예시입니다. CPU 환경에 따라 `Big Endian` 또는 `Mixed/Other Endian`이 표시될 수 있습니다.

Binary 포맷은 헤더, 필드 크기, Byte Order, 데이터 개수, 버전, 오류 검증 규칙을 먼저 정의한 뒤 구현합니다. C++ 구조체의 메모리 레이아웃을 파일 형식으로 그대로 쓰는 방법은 플랫폼 의존성이 생길 수 있으므로 일반적으로 권장하지 않습니다.

---

<a id="section-11-12"></a>

## 11.12. RAII, Flush 및 파일 닫기

리소스 획득 즉 초기화(Resource Acquisition Is Initialization, RAII)는 객체 수명을 자원 관리와 연결하는 C++ 설계 원칙입니다. `std::ifstream`과 `std::ofstream`은 객체가 소멸할 때 소유한 파일을 닫습니다.

하지만 **소멸자에만 의존하면 쓰기 종료 시 발생한 오류를 호출자에게 보고하기 어렵습니다.** 쓰기 결과가 중요한 경우 `close()`를 명시적으로 호출하고 Stream 상태를 검사할 수 있습니다.

**예제 코드 — [12_raii_file_scope.cpp](./examples/12_raii_file_scope.cpp)**

```cpp
#include <fstream>
#include <print>
#include <string>

[[nodiscard]] bool save_message(const char* path, const std::string& message) {
    std::ofstream output{path, std::ios::trunc};
    if (!output) return false;
    output << message << '\n';
    output.close();
    return output.good();
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    if (!save_message(argv[1], "status=ready")) {
        std::println(stderr, "Save failed");
        return 1;
    }
    std::println("Saved");
}
```

**실행 결과**

```text
Saved
```

| 연산 | 설명 |
|---|---|
| `output << value` | 데이터를 Stream 버퍼에 기록 요청 |
| `output.flush()` | 버퍼의 데이터 쓰기 요청, 오류 상태 확인 가능 |
| `output.close()` | Stream이 관리하는 파일 닫기, 실패 확인 가능 |
| 객체 소멸 | 열려 있는 파일을 자동으로 정리 |

`flush()` 또는 `close()`가 성공해도 전원 장애 이후 데이터 보존까지 보장하지는 않습니다. 엄격한 내구성 요구사항에는 운영체제별 동기화 API와 저장장치 특성을 별도로 고려해야 합니다.

---

<a id="section-11-13"></a>

## 11.13. 오류 반환 — `std::expected`

파일 열기 실패나 읽기 오류를 단순한 `false`로만 반환하면 실패 원인을 전달하기 어렵습니다. C++23의 `std::expected<T, E>`는 성공 값과 오류 정보를 분리하여 반환합니다.

- **성공:** 파일 내용인 `std::string` 반환
- **실패:** 오류 메시지를 `std::unexpected`로 반환
- **사용:** 결과 확인 후 `*result`, 오류 발생 시 `result.error()` 조회

**예제 코드 — [13_expected_file_read.cpp](./examples/13_expected_file_read.cpp)**

```cpp
#include <expected>
#include <fstream>
#include <iterator>
#include <print>
#include <string>

[[nodiscard]] std::expected<std::string, std::string>
load_text(const std::string& path) {
    std::ifstream input{path};
    if (!input) return std::unexpected("Cannot open input file");
    std::string contents{std::istreambuf_iterator<char>{input},
                         std::istreambuf_iterator<char>{}};
    if (input.bad()) return std::unexpected("Read failed");
    return contents;
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    const auto text = load_text(argv[1]);
    if (!text) {
        std::println(stderr, "{}", text.error());
        return 1;
    }
    std::println("Loaded {} bytes", text->size());
}
```

**실행 결과**

```text
Loaded 17 bytes
```

위 코드는 작은 입력 파일을 전체 메모리로 읽습니다. 대규모 파일에 대해서는 처리 방식 자체를 Streaming으로 변경하는 것이 적절합니다.

오류 메시지에 경로·계정 정보 등을 그대로 노출하면 민감한 시스템 정보가 포함될 수 있으므로 사용자에게 출력하는 정보의 범위도 결정해야 합니다.

---

<a id="section-11-14"></a>

## 11.14. 임시 파일과 이름 변경 — 안전한 저장 범위

기존 설정 파일에 `std::ios::trunc`로 바로 쓰기 시작하면, 중간에 쓰기가 실패했을 때 원본 데이터가 일부 또는 전부 손실될 수 있습니다. 따라서 별도 파일에 작성한 뒤 이름 변경(Rename)을 시도하는 방식이 사용됩니다.

다음 예제는 **기존 파일을 덮어쓰지 않고 신규 파일만 생성**하는 단순한 절차입니다. 임시 파일(Temporary File)에 먼저 내용을 쓴 뒤 같은 디렉터리의 목적 이름으로 변경합니다.

**예제 코드 — [14_write_new_via_rename.cpp](./examples/14_write_new_via_rename.cpp)**

```cpp
#include <filesystem>
#include <fstream>
#include <print>
#include <string_view>
#include <system_error>

// 신규 파일 생성 예제. 동시 접근·신뢰할 수 없는 디렉터리에는 적합하지 않음.
[[nodiscard]] bool save_new(const std::filesystem::path& destination,
                            std::string_view content) {
    namespace fs = std::filesystem;
    std::error_code ec;
    if (fs::exists(destination, ec) || ec) return false; // 덮어쓰기 금지
    fs::path temporary = destination;
    temporary += ".tmp";
    if (fs::exists(temporary, ec) || ec) return false;
    {
        std::ofstream output{temporary, std::ios::binary | std::ios::trunc};
        if (!output) return false;
        output.write(content.data(), static_cast<std::streamsize>(content.size()));
        output.close();
        if (!output) {
            fs::remove(temporary, ec);
            return false;
        }
    }
    fs::rename(temporary, destination, ec);
    if (ec) {
        std::error_code cleanup_error;
        fs::remove(temporary, cleanup_error);
        return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    if (!save_new(argv[1], "mode=automatic\n")) {
        std::println(stderr, "Save failed (target or temporary file may exist)");
        return 1;
    }
    std::println("Created new file");
}
```

**실행 결과**

```text
Created new file
```

```bash
g++ -std=c++23 examples/14_write_new_via_rename.cpp -o save_new
./save_new new_settings.txt
```

**제약 및 주의사항**

- 대상 파일이 이미 존재하면 실패하도록 구현. 기존 파일 교체 기능 아님
- `.tmp` 이름은 교육용 고정 이름. 여러 프로세스가 동시에 접근하거나 외부에서 디렉터리를 조작할 수 있는 환경에 적합하지 않음
- 사전의 `exists()` 검사는 이후 상태가 변하지 않는다는 보장이 없음(TOCTOU)
- 같은 파일 시스템에서의 Rename이라도 기존 파일 교체·내구성·충돌 처리의 보장은 운영체제와 파일 시스템에 따라 검토 필요
- 실패 시 임시 파일 정리를 시도하지만 권한·장애 상황에 따라 파일이 남을 수 있음

**설정 파일을 안전하게 교체하는 완성형 프로그램**은 플랫폼별 원자적 교체(Atomic Replacement), 고유 임시 파일 생성, 파일·디렉터리 동기화, 실패 복구까지 검토해야 합니다.

---

<a id="section-11-15"></a>

## 11.15. UTF-8과 텍스트 인코딩

문자 인코딩(Character Encoding)은 텍스트를 바이트로 나타내는 규칙입니다. UTF-8은 가변 길이 인코딩이며, 문자열의 바이트 수와 화면에 보이는 문자 수가 일치하지 않을 수 있습니다.

Chapter 06에서 다룬 코드 포인트(Code Point), 문자소 클래스터(Grapheme Cluster)는 이 차이를 이해하는 데 필요한 개념입니다. UTF-8의 한글 음절은 일반적으로 여러 바이트로 인코딩됩니다.

**예제 코드 — [16_utf8_text.cpp](./examples/16_utf8_text.cpp)**

```cpp
#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    const std::string value = "센서"; // 소스 파일을 UTF-8로 저장
    std::ofstream output{argv[1], std::ios::binary | std::ios::trunc};
    if (!output) return 1;
    output.write(value.data(), static_cast<std::streamsize>(value.size()));
    output.close();
    if (!output) return 1;
    std::println("UTF-8 bytes: {}", value.size());
}
```

**실행 결과**

```text
UTF-8 bytes: 6
```

이 예제는 소스 파일이 UTF-8로 저장되고, 컴파일러가 좁은 문자열 리터럴을 UTF-8로 인코딩한다는 전제하에 `센서`를 6바이트로 기록합니다.

Windows의 파일 경로 인코딩과 **파일 내용의 인코딩**은 별개입니다. `std::filesystem::path`가 사용하는 운영체제별 경로 표현과 `std::string`에 저장한 UTF-8 내용은 구분해야 합니다. 다른 인코딩을 읽어야 한다면 변환 정책이 필요합니다.

---

<a id="section-11-16"></a>

## 11.16. 경로 검증과 보안 고려 사항

외부 입력으로 파일 경로를 전달받는 프로그램은 지정된 디렉터리 밖의 파일에 접근하지 않도록 설계해야 할 수 있습니다.

| 위험 | 예시 | 대응 방향 |
|---|---|---|
| 경로 탐색(Path Traversal) | `../../secret.txt` | 허용된 저장 위치와 파일 식별 규칙 적용 |
| 심볼릭 링크(Symbolic Link) | 검증 뒤 대상 변경 | 링크 정책 및 운영체제 파일 핸들 기반 검증 검토 |
| TOCTOU | `exists()` 검사 직후 파일 교체 | 검사와 사용을 분리하지 않는 API 활용 검토 |
| 과도한 메모리 사용 | 수 GB 파일을 한 번에 메모리로 읽기 | 최대 파일 크기 제한 또는 Streaming |
| 무제한 입력 | 매우 긴 CSV 행 | 행·필드 크기와 레코드 수 제한 |
| 정보 유출 | 원본 경로 포함 오류 메시지 | 사용자·로그 출력 구분 |

**중요:** `lexically_normal()`은 문자열 수준의 정리 기능이지 보안 경계를 보장하는 검증 함수가 아닙니다. 심볼릭 링크와 운영체제별 경로 해석까지 고려해야 합니다.

본 Chapter의 예제는 사용자가 통제하는 테스트 파일을 대상으로 합니다. 다중 사용자 서비스나 신뢰할 수 없는 경로를 받는 프로그램에는 별도 보안 설계가 필요합니다.

---

<a id="section-11-17"></a>

## 11.17. 대용량 파일과 Streaming 처리

대용량 파일에서는 모든 내용을 한 번에 복사하는 대신 일부씩 읽고 곧바로 처리하는 스트리밍(Streaming) 방식이 메모리 사용을 줄이는 데 유리합니다.

`std::getline()`은 각 행을 순서대로 처리할 수 있어 행별 집계에 적합합니다. 다만 한 행 자체의 길이가 무제한이면 `std::string`이 크게 증가할 수 있으므로 입력 크기 상한을 추가하는 것이 좋습니다.

**예제 코드 — [15_streaming_large_file.cpp](./examples/15_streaming_large_file.cpp)**

```cpp
#include <cstdint>
#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::uint64_t bytes{};
    std::uint64_t lines{};
    std::string line;
    while (std::getline(input, line)) {
        ++lines;
        bytes += line.size(); // 개행 바이트는 제외한 데이터 크기
    }
    if (input.bad()) return 1;
    std::println("Lines: {}, payload bytes: {}", lines, bytes);
}
```

**실행 결과**

```text
Lines: 3, payload bytes: 14
```

```bash
g++ -std=c++23 examples/15_streaming_large_file.cpp -o stream_lines
./stream_lines data/demo_lines.txt
```

이 예제의 `payload bytes`는 줄바꿈 바이트를 제외한 행 내용의 합계입니다. 실제 파일의 전체 바이트 수와 다를 수 있습니다.

**참고:** 텍스트 파일에서 무작위 위치 탐색(Seek)이나 전체 크기 추적이 필요하면 Stream의 `seekg`, `tellg` 또는 `std::filesystem::file_size`의 용도를 구분합니다. 줄바꿈 변환이 있는 Text Mode에서는 바이트 오프셋을 단순한 문자 인덱스로 해석해서는 안 됩니다.

---

<a id="section-11-18"></a>

## 11.18. Mini Project — Sensor CSV Report

### 목표

센서 측정값을 CSV로 읽어 장치별 기록 수와 온도 통계를 계산한 뒤 결과를 텍스트 파일로 저장합니다. 입력은 다음 형식으로 제한합니다.

```csv
device,temperature_c
robot-01,21.5
robot-02,24
robot-01,22.5
robot-03,17
robot-02,23
```

**입력 규칙**

- 첫 행은 반드시 `device,temperature_c`
- 장치 ID는 영문·숫자·`_`·`-`만 사용, 최대 32자
- 온도는 `-50.0` ~ `120.0` 범위의 유한한 실수
- 쉼표로 구분된 두 필드만 허용하며 인용부호가 포함된 CSV는 지원하지 않음
- 잘못된 행이 존재하면 결과 파일을 생성하기 전에 오류 반환

### 파일 구조

```text
examples/17_sensor_report/
├── CMakeLists.txt
├── report.hpp
├── report.cpp
├── main.cpp
└── data/
    └── sensor_readings.csv
```

- [report.hpp](./examples/17_sensor_report/report.hpp) — 자료형과 공개 함수 선언
- [report.cpp](./examples/17_sensor_report/report.cpp) — CSV 검증, 집계 및 파일 출력
- [main.cpp](./examples/17_sensor_report/main.cpp) — 명령줄 인수 처리 및 오류 출력
- [CMakeLists.txt](./examples/17_sensor_report/CMakeLists.txt) — C++23 빌드 설정
- [sensor_readings.csv](./examples/17_sensor_report/data/sensor_readings.csv) — 테스트 입력

### CMake 빌드 및 실행

**GCC 또는 Clang** — `Chapter-11/` 디렉터리 기준

```bash
cmake -S examples/17_sensor_report -B build/sensor_report
cmake --build build/sensor_report
./build/sensor_report/sensor_report examples/17_sensor_report/data/sensor_readings.csv build/sensor_report/report.txt
```

**Windows/MSVC** — Developer Command Prompt에서 구성

```bat
cmake -S examples\17_sensor_report -B build\sensor_report
cmake --build build\sensor_report --config Release
build\sensor_report\Release\sensor_report.exe examples\17_sensor_report\data\sensor_readings.csv build\sensor_report\report.txt
```

Visual Studio와 같은 다중 구성 Generator에서는 `--config Release`로 생성한 실행 파일이 `Release/`에 위치할 수 있습니다. Generator 설정에 따라 실제 경로는 다를 수 있습니다.

### 실행 결과

```text
Saved report: 5 readings from 3 devices
```

**생성된 `report.txt`**

```text
Readings: 5
Devices: 3
Average: 21.60 C
Minimum: 17.00 C
Maximum: 24.00 C
robot-01: 2
robot-02: 2
robot-03: 1
```

### 설계 확인

- CSV 전체 파싱이 성공한 후 출력 파일 생성
- `std::expected`를 통한 실패 사유 전달
- `std::map`을 이용한 장치별 집계와 정렬된 출력
- 입력 파일과 출력 파일이 이미 같은 파일인 경우 차단
- 쓰기 종료 후 Stream 상태 확인

출력 단계에서 디스크 오류가 발생하면 부분적으로 작성된 보고서가 남을 수 있습니다. **기존 파일의 원자적 교체까지 구현한 프로젝트는 아니므로**, 중요한 설정 파일을 갱신하는 경우 별도의 저장 절차가 필요합니다.

---

<a id="section-11-19"></a>

## 11.19. Coding Practice

각 문제는 `exercises/`에 시작 코드, `solutions/`에 모범답안을 제공합니다. 문제를 먼저 구현하고 정상 입력·비정상 입력을 모두 테스트합니다.

### ① Temperature Summary

- [문제 코드](./exercises/01_temperature_summary.cpp) · [정답 코드](./solutions/01_temperature_summary.cpp)
- **입력:** 한 행에 `-1000` ~ `1000` 범위의 정수 하나
- **출력:** 데이터 개수, 최솟값, 최댓값, 소수 둘째 자리까지 평균
- **검증:** 빈 파일, 공백 행, 숫자 뒤의 문자, 범위 초과 시 오류

```text
입력: data/temperatures.txt
Count: 3
Min: -2
Max: 8
Average: 4.00
```

### ② Event Log Summary

- [문제 코드](./exercises/02_event_log_summary.cpp) · [정답 코드](./solutions/02_event_log_summary.cpp)
- **입력:** `LEVEL|DEVICE|MESSAGE`, `LEVEL`은 `INFO`, `WARN`, `ERROR` 중 하나
- **조건:** `MESSAGE`에는 `|`를 포함할 수 있고 빈 필드는 허용하지 않음
- **출력:** 레벨별 발생 수. 정의되지 않은 레벨 또는 잘못된 행이면 오류

```text
입력: data/events.log
INFO: 1
WARN: 1
ERROR: 1
```

### ③ Inventory CSV

- [문제 코드](./exercises/03_inventory_csv.cpp) · [정답 코드](./solutions/03_inventory_csv.cpp)
- **입력:** 헤더 `id,quantity` 및 재고 데이터
- **조건:** ID는 영숫자·`_`·`-`, 길이 1~32. 수량은 `0` ~ `1000000`
- **출력:** ID 오름차순 재고와 총수량
- **검증:** 잘못된 행, 수량 범위 초과, 중복 ID

```text
입력: data/inventory.csv
battery: 5
sensor: 2
Total: 7
```

### ④ Binary Data Reader

- [문제 코드](./exercises/04_binary_u32_reader.cpp) · [정답 코드](./solutions/04_binary_u32_reader.cpp)
- **입력:** Magic `CNT1`(4 byte), Count(4 byte, Big Endian), Count개 `uint32` 값(Big Endian)
- **조건:** Count는 최대 `100000`, 데이터 길이와 Magic은 정확히 일치해야 함
- **출력:** Count와 `std::uint64_t`로 계산한 합계
- **검증:** 파일 길이 부족, 잉여 바이트, 잘못된 Magic, 과도한 Count

```text
입력: data/count_values.bin
Count: 3
Sum: 4294967596
```

### 컴파일 및 실행

**GCC** — `Chapter-11/` 기준

```bash
g++ -std=c++23 -Wall -Wextra -Wpedantic -O2 \
  solutions/01_temperature_summary.cpp -o temperature_summary
./temperature_summary data/temperatures.txt
```

**Clang** — C++23 표준 라이브러리 사용 가능 환경

```bash
clang++ -std=c++23 -Wall -Wextra -Wpedantic -O2 \
  solutions/01_temperature_summary.cpp -o temperature_summary
./temperature_summary data/temperatures.txt
```

**MSVC** — Developer Command Prompt

```bat
cl /nologo /std:c++23preview /W4 /EHsc /permissive- /utf-8 solutions\01_temperature_summary.cpp /Fe:temperature_summary.exe
temperature_summary.exe data\temperatures.txt
```

MSVC에서는 설치 버전에 따라 `/std:c++23` 또는 `/std:c++23preview`의 지원 범위를 확인합니다. `<print>`와 `<expected>` 등 개별 표준 라이브러리 기능도 지원 여부가 다를 수 있습니다.

---

<a id="section-11-20"></a>

## 11.20. Quiz & Summary

### Quiz

**1.** `std::ofstream`을 기본 모드로 열었을 때 기존 파일에 어떤 영향이 있을 수 있나요?

<details>
<summary>정답 확인</summary>

기존 파일을 비우는 Truncation이 발생할 수 있음.

</details>

**2.** `while (!input.eof())`보다 `while (std::getline(input, line))`을 권장하는 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

읽기 성공 여부가 확정된 뒤에만 행을 처리할 수 있기 때문.

</details>

**3.** `std::from_chars`가 `"25ms"`에서 `25`를 읽었을 때 추가로 무엇을 확인해야 하나요?

<details>
<summary>정답 확인</summary>

종료 포인터가 입력의 끝인지 검사하여 전체 입력 소비 여부를 검증.

</details>

**4.** Binary 파일에 `struct`를 그대로 기록하는 방법이 이식성에 문제가 될 수 있는 이유는 무엇인가요?

<details>
<summary>정답 확인</summary>

Padding, Alignment, Byte Order, 타입 크기 등이 환경별로 달라질 수 있음.

</details>

**5.** `flush()` 또는 `close()` 호출 성공만으로 전원 장애 이후 데이터 보존을 보장할 수 있나요?

<details>
<summary>정답 확인</summary>

불가능. 운영체제·파일 시스템·장치 차원의 동기화 요구사항을 별도 검토.

</details>

**6.** `std::filesystem::path::lexically_normal()`을 호출하면 경로 탐색 공격을 완전히 차단할 수 있나요?

<details>
<summary>정답 확인</summary>

불가능. 문자열 정규화는 실제 파일 시스템 상태와 Symbolic Link 등을 검증하지 않음.

</details>

### Summary

- **File I/O:** `std::ifstream`, `std::ofstream`을 통한 파일 읽기와 쓰기
- **Stream 상태:** `eofbit`, `failbit`, `badbit`의 의미 구분
- **Path:** `std::filesystem::path`를 이용한 경로 조합 및 분석
- **Error Code:** 파일 시스템 작업의 오류 정보 처리
- **Parsing:** `std::from_chars` 결과와 입력 전체 소비 여부 검증
- **CSV:** 인용부호, 구분자, 필드 규칙과 Parser의 지원 범위 확인
- **Binary Format:** Magic, Version, Byte Order 및 명시적 레이아웃 설계
- **RAII:** 객체 수명을 통한 파일 자원 관리
- **`std::expected`:** 성공 결과와 오류 사유를 구분하여 전달
- **Temporary File:** 신규 파일 작성 중 오류에 대비한 중간 파일 사용
- **UTF-8:** 바이트 수와 Grapheme Cluster 수를 구분
- **Streaming:** 파일 전체를 메모리에 올리지 않고 순차 처리
- **Validation:** 경로·크기·인코딩·입력 필드 및 출력 상태 검사

### References

- [cppreference — `std::basic_ifstream`](https://en.cppreference.com/w/cpp/io/basic_ifstream)
- [cppreference — `std::basic_ofstream`](https://en.cppreference.com/w/cpp/io/basic_ofstream)
- [cppreference — `std::getline`](https://en.cppreference.com/w/cpp/string/basic_string/getline)
- [cppreference — `std::filesystem::path`](https://en.cppreference.com/w/cpp/filesystem/path)
- [cppreference — `std::filesystem::rename`](https://en.cppreference.com/w/cpp/filesystem/rename)
- [cppreference — `std::from_chars`](https://en.cppreference.com/w/cpp/utility/from_chars)
- [cppreference — `std::expected`](https://en.cppreference.com/w/cpp/utility/expected)
- [ISO/IEC 14882:2024 — C++](https://www.iso.org/standard/83626.html)

---

[← C++ 목차](../README.md) · [Chapter 10 — Standard Library (STL)](../Chapter-10/)
