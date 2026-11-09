# Chapter 18. Networking & Interprocess Communication

C++20으로 TCP·UDP Socket, 메시지 프레이밍, 프로세스 간 통신(IPC)을 구현하고 검증하는 방법을 다룹니다. Chapter 12의 RAII, Chapter 14의 동시성, Chapter 16의 CMake와 Chapter 17의 테스트를 연결하여 **실제 데이터를 주고받는 프로그램의 인터페이스와 오류 처리를 설계**하는 것이 목표입니다.

> **실행 범위:** 네트워크 소켓 API는 ISO C++20 표준 라이브러리에 포함되지 않습니다. 본 Chapter는 Linux/macOS의 POSIX API와 Windows의 Winsock을 사용합니다. 프로젝트는 외부 인터넷에 연결하지 않고 `127.0.0.1`의 임시 포트로만 통신하도록 구성되어 있습니다. TLS·사용자 인증 등을 제공하는 운영용 서버 구현이 아닙니다.

- **기준 표준:** C++20 (GCC 14, Clang 17에서 테스트)
- **선행 학습:** [Chapter 11 — File I/O](../Chapter-11/) · [Chapter 12 — Resource Management](../Chapter-12/) · [Chapter 14 — Concurrency](../Chapter-14/) · [Chapter 16 — CMake](../Chapter-16/) · [Chapter 17 — Testing](../Chapter-17/)
- **자료:** 예제 16개, 실습 4문제, Basic·Advanced·Pro 프로젝트, 자동 테스트, 플랫폼별 안내

<a id="contents"></a>
## Contents

| Section | Topic |
|:---:|---|
| [18.1](#section-18-1) | Network Programming의 범위와 통신 모델 |
| [18.2](#section-18-2) | IP 주소, Port와 Endpoint |
| [18.3](#section-18-3) | Byte Order와 바이너리 데이터 |
| [18.4](#section-18-4) | TCP Stream과 부분 송수신 |
| [18.5](#section-18-5) | Message Framing과 길이 헤더 |
| [18.6](#section-18-6) | Socket Lifetime과 RAII |
| [18.7](#section-18-7) | TCP Loopback 연결과 왕복 통신 |
| [18.8](#section-18-8) | UDP Datagram과 전송 보장 범위 |
| [18.9](#section-18-9) | Timeout, Deadline, Retry |
| [18.10](#section-18-10) | 오류 모델과 실패 처리 |
| [18.11](#section-18-11) | Request–Response Protocol |
| [18.12](#section-18-12) | 동시 접속과 공유 상태 |
| [18.13](#section-18-13) | 협력적 종료와 Shutdown |
| [18.14](#section-18-14) | Pipe와 부모·자식 프로세스 |
| [18.15](#section-18-15) | UNIX Domain Socket과 Local IPC |
| [18.16](#section-18-16) | Windows IPC와 플랫폼 차이 |
| [18.17](#section-18-17) | 신뢰할 수 없는 입력과 프로토콜 검증 |
| [18.18](#section-18-18) | 성능, 운영 및 테스트 설계 |
| [18.19](#section-18-19) | Coding Practice |
| [18.20](#section-18-20) | Basic Mini Project — Loopback Echo |
| [18.21](#section-18-21) | Advanced Project — Concurrent Telemetry Collector |
| [18.22](#section-18-22) | Pro Project — Installable ProLink SDK |
| [18.23](#section-18-23) | 설계 점검과 다음 학습 |
| [18.24](#section-18-24) | Quiz & Summary |

---

## 시작하기

`Chapter-18/` 폴더에서 실행합니다. Linux에서는 g++ 또는 clang++와 CMake가 필요합니다. Windows에서는 최신 MSVC와 CMake를 사용하며, Winsock을 쓰는 Target에 `ws2_32` 링크가 필요합니다.

```bash
# 전체 예제·정답·프로젝트 검증 (GCC 14)
python3 tests/check.py --compiler g++-14

# 다른 컴파일러로 검증
python3 tests/check.py --compiler clang++

# 단일 예제 직접 컴파일 (Linux)
g++-14 -std=c++20 -Wall -Wextra -Wpedantic -pthread examples/07_tcp_loopback.cpp -o loopback
./loopback
```

`tests/check.py`는 실습의 **모범답안**을 기본으로 확인합니다. 학생용 코드를 검증하려면 `--mode student --only exercise-01`처럼 실행하세요. 학습 중 미완성 코드가 테스트에 실패하는 것은 정상입니다.

**네트워크 환경 제약:** 샌드박스나 일부 온라인 실행 환경에서 Socket 생성이 차단될 수 있습니다. 이 경우 프로토콜·파싱 예제를 먼저 학습하고, TCP·UDP 프로젝트는 로컬 개발 PC에서 실행합니다. Windows와 POSIX 차이는 [플랫폼 안내](./docs/PLATFORM.md)를 확인하세요.

---

<a id="section-18-1" ></a>

## 18.1. Network Programming의 범위와 통신 모델


네트워크 프로그램은 서로 다른 프로세스가 **어떤 바이트를 어떤 규칙으로 보내고 해석하는지** 정한 뒤, 운영체제의 통신 API를 사용하여 전달합니다. C++20 자체에는 `std::socket` 같은 표준 네트워킹 객체가 없기 때문에 Socket API는 플랫폼별로 호출합니다.

| 층위 | 담당 | 예시 |
|---|---|---|
| 애플리케이션 프로토콜 | 메시지 의미·형식·오류 코드 | `READ A 20`, `OK` |
| 전송 계층 | 바이트/데이터그램 전달 | TCP, UDP |
| 주소·연결 | 목적지 식별 | `127.0.0.1:포트` |

Socket으로 데이터를 보냈다고 해서 바로 **명령 실행 성공**을 의미하지는 않습니다. 예를 들어 수신에 성공했더라도 명령이 잘못되었다면 `ERR`를 반환할 수 있습니다. 전송 오류와 애플리케이션 오류는 별도로 다룹니다.


**예제 코드 — [01_network_layers.cpp](./examples/01_network_layers.cpp)**

```cpp
#include <iostream>
int main() {
    std::cout << "Application: framing and validation\n"
              << "Transport: TCP stream / UDP datagram\n"
              << "Address: 127.0.0.1 (IPv4 loopback)\n";
}
```

**실행 결과**

```text
Application: framing and validation
Transport: TCP stream / UDP datagram
Address: 127.0.0.1 (IPv4 loopback)
```


---


<a id="section-18-2" ></a>

## 18.2. IP 주소, Port와 Endpoint


Endpoint는 IP 주소와 Port로 통신 상대를 구분하는 개념입니다. IPv4의 `127.0.0.1`은 현재 컴퓨터 안으로만 돌아오는 Loopback 주소입니다. 다른 컴퓨터가 접근할 수 있는 주소와 다르므로 로컬 실습에 적합합니다.

- 서버는 **bind → listen → accept** 순서로 TCP 연결을 기다립니다.
- 클라이언트는 **socket → connect** 순서로 접속합니다.
- Port `0`을 서버 바인딩에 지정하면 운영체제가 비어 있는 임시 Port를 배정합니다. 실제 Port는 `getsockname()`으로 읽습니다.
- IPv6의 Loopback 주소는 `::1`입니다. 본 예제는 IPv4만 구현합니다.

고정 Port는 다른 프로그램과 충돌할 수 있으므로 테스트에서는 임시 Port를 사용합니다.


**예제 코드 — [05_strict_command_parser.cpp](./examples/05_strict_command_parser.cpp)**

```cpp
#include <charconv>
#include <iostream>
#include <string_view>
#include <system_error>
[[nodiscard]] bool parse_port(std::string_view text, int& port) {
    if (text.empty()) return false;
    const char* first = text.data();
    const char* last = first + text.size();
    const auto [end, error] = std::from_chars(first, last, port);
    return error == std::errc{} && end == last && port >= 1 && port <= 65535;
}
int main() {
    int port = 0;
    std::cout << std::boolalpha
              << "valid: " << parse_port("8080", port) << " / " << port << '\n'
              << "invalid: " << parse_port("8080x", port) << '\n';
}
```

**실행 결과**

```text
valid: true / 8080
invalid: false
```


---


<a id="section-18-3" ></a>

## 18.3. Byte Order와 바이너리 데이터


컴퓨터마다 여러 바이트로 구성된 정수를 메모리에 배치하는 순서가 다를 수 있습니다. 네트워크 프로토콜에서는 바이트 순서를 명시해야 합니다. 일반적으로 **Network Byte Order는 Big-Endian**이며, 32비트 크기 `0x01020304`는 `01 02 03 04` 순서로 기록합니다.

```text
32-bit Length = 4  →  00 00 00 04
Payload "PING"     →  50 49 4E 47
Final frame         →  00 00 00 04 50 49 4E 47
```

숫자를 구조체 메모리째 전송하는 방식은 패딩과 바이트 순서로 인해 다른 시스템에서 깨질 수 있습니다. 필요한 필드를 정해진 크기와 바이트 순서로 인코딩해야 합니다.


**예제 코드 — [02_network_byte_order.cpp](./examples/02_network_byte_order.cpp)**

```cpp
#include <cstdint>
#include <iostream>
int main() {
    constexpr std::uint32_t size = 0x01020304;
    std::cout << std::hex << static_cast<unsigned>((size >> 24) & 0xff) << ' '
              << static_cast<unsigned>((size >> 16) & 0xff) << ' '
              << static_cast<unsigned>((size >> 8) & 0xff) << ' '
              << static_cast<unsigned>(size & 0xff) << '\n';
}
```

**실행 결과**

```text
1 2 3 4
```


---


<a id="section-18-4" ></a>

## 18.4. TCP Stream과 부분 송수신


**TCP는 메시지가 아니라 순서가 있는 바이트 스트림**을 전달합니다. `send()`가 한 번에 100바이트를 보냈다고 해서 상대의 `recv()`도 100바이트를 한 번에 반환한다는 보장이 없습니다. 하나의 메시지가 여러 번 나뉘어 도착하거나, 여러 메시지가 한 수신 버퍼에 붙어서 도착할 수 있습니다.

따라서 다음 계약이 중요합니다.

1. `send()`가 실제로 전달 요청한 바이트 수를 누적하여 남은 부분을 재시도함.
2. `recv()`에서 필요한 바이트를 채울 때까지 반복함.
3. `recv() == 0`이면 정상적인 스트림 종료(EOF)로 해석하되, **메시지 중간 EOF는 잘린 메시지**로 처리함.
4. 오류와 Timeout을 정상적인 메시지 종료와 혼동하지 않음.

이 예제는 `|` 구분자를 사용하는 단순 스트림 파서를 시뮬레이션합니다. 실제 TCP 통신에서는 길이 헤더 방식 등을 사용하는 편이 검증에 유리합니다.


**예제 코드 — [03_tcp_stream_chunking.cpp](./examples/03_tcp_stream_chunking.cpp)**

```cpp
#include <iostream>
#include <string>
#include <string_view>
int main() {
    const std::string_view chunks[]{"HEL", "LO|WOR", "LD|"};
    std::string pending;
    int messages = 0;
    for (const auto chunk : chunks) {
        pending.append(chunk);
        for (std::size_t split; (split = pending.find('|')) != std::string::npos;) {
            std::cout << "Message: " << pending.substr(0, split) << '\n';
            pending.erase(0, split + 1);
            ++messages;
        }
    }
    std::cout << "Count: " << messages << '\n';
}
```

**실행 결과**

```text
Message: HELLO
Message: WORLD
Count: 2
```


---


<a id="section-18-5" ></a>

## 18.5. Message Framing과 길이 헤더


메시지 경계가 없다면 수신자가 언제 하나의 요청이 끝나는지 알 수 없습니다. 이 Chapter는 **4바이트 Big-Endian 길이 헤더 + Payload** 형식을 사용합니다.

| 항목 | 형식 | 제약 |
|---|---|---|
| Length | Unsigned 32-bit, Big-Endian | 0~4096 |
| Payload | 원시 바이트 | UTF-8이라고 가정하지 않음 |
| 전체 Frame | 헤더 4바이트 + Payload | 최대 4100바이트 |

수신자는 헤더 4바이트를 먼저 읽고 길이가 4096을 넘으면 **할당 전에 거부**합니다. 길이가 허용 범위 안이면 해당 바이트 수만큼 추가로 수신합니다. 문자열에 ` `이 포함될 수 있으므로 `strlen()`으로 바이트 수를 계산하지 않습니다.

[상세 프로토콜 규칙](./docs/PROTOCOL.md)


**예제 코드 — [04_length_prefix_codec.cpp](./examples/04_length_prefix_codec.cpp)**

```cpp
#include "../common/socket.hpp"
#include <iostream>
int main() {
    const auto bytes = lesson_net::encode_frame("OK");
    std::cout << "Frame bytes: " << bytes.size() << '\n';
    std::cout << "Payload: " << bytes.substr(4) << '\n';
}
```

**실행 결과**

```text
Frame bytes: 6
Payload: OK
```


---


<a id="section-18-6" ></a>

## 18.6. Socket Lifetime과 RAII


Socket은 파일과 비슷하게 운영체제에서 부여받는 자원이며, 사용 후 반드시 반환해야 합니다. Chapter 12의 RAII를 사용하면 `Socket` 객체 소멸 시 `close()` 또는 `closesocket()`이 실행되도록 설계할 수 있습니다.

| 환경 | Native Handle | 해제 |
|---|---|---|
| POSIX | 정수 파일 디스크립터 | `close()` |
| Windows | `SOCKET` | `closesocket()` |

`Socket`은 **복사 금지·이동 허용**으로 구현했습니다. Move 이후 원래 객체는 무효 핸들을 보유하므로 중복 해제를 방지합니다. Windows에서는 Socket API 사용 전에 `WSAStartup()`이 필요해 별도 `Runtime` 객체가 초기화를 담당합니다. 공통 구현은 [`common/socket.hpp`](./common/socket.hpp)에 있습니다.


**예제 코드 — [06_socket_raii.cpp](./examples/06_socket_raii.cpp)**

```cpp
#include "../common/socket.hpp"
#include <iostream>
int main() {
    lesson_net::Runtime runtime;
    std::uint16_t port = 0;
    auto listener = lesson_net::listen_loopback(port);
    auto moved = std::move(listener);
    std::cout << "Owner moved: " << std::boolalpha
              << (!listener.valid() && moved.valid()) << '\n';
}
```

**실행 결과**

```text
Owner moved: true
```


---


<a id="section-18-7" ></a>

## 18.7. TCP Loopback 연결과 왕복 통신


서버가 `127.0.0.1`에 임시 Port로 대기하고, 클라이언트가 연결한 후 `hello`를 전송합니다. 서버는 Frame을 해석하고 `ECHO:hello`를 돌려줍니다.

```text
Server: bind(127.0.0.1:0) → listen → accept → receive_frame → send_frame
Client: connect(bound_port) → send_frame("hello") → receive_frame
```

한 연결에 무제한 요청을 처리하는 서버가 아니라 **한 번 왕복하고 끝나는 학습용 서버**입니다. 송수신에는 부분 전송 처리와 제한된 시간 대기를 포함합니다. 예외가 발생해도 Socket은 RAII로 정리합니다.


**예제 코드 — [07_tcp_loopback.cpp](./examples/07_tcp_loopback.cpp)**

```cpp
#include "../common/socket.hpp"
#include <iostream>
#include <thread>
#include <exception>
int main() {
    lesson_net::Runtime runtime;
    std::uint16_t port = 0;
    const auto listener = lesson_net::listen_loopback(port);
    std::exception_ptr server_error;
    std::thread server([&] {
        try {
            auto peer = lesson_net::accept_one(listener);
            std::string value;
            if (!lesson_net::receive_frame(peer, value)) throw std::runtime_error("no message");
            lesson_net::send_frame(peer, "ECHO:" + value);
        } catch (...) { server_error = std::current_exception(); }
    });
    try {
        auto client = lesson_net::connect_loopback(port);
        lesson_net::send_frame(client, "hello");
        std::string reply;
        if (!lesson_net::receive_frame(client, reply)) throw std::runtime_error("no reply");
        server.join();
        if (server_error) std::rethrow_exception(server_error);
        std::cout << "Reply: " << reply << '\n';
    } catch (...) {
        if (server.joinable()) server.join();
        throw;
    }
}
```

**실행 결과**

```text
Reply: ECHO:hello
```


---


<a id="section-18-8" ></a>

## 18.8. UDP Datagram과 전송 보장 범위


UDP는 **Datagram 단위**로 메시지를 송신하고 수신합니다. TCP처럼 연결된 바이트 스트림을 만들지 않으며, 패킷 순서·재전송·중복 제거가 자동으로 보장되지 않습니다.

| 비교 | TCP | UDP |
|---|---|---|
| 전달 단위 | Byte Stream | Datagram |
| 순서 | 연결 내 바이트 순서 보장 | 보장하지 않음 |
| 재전송 | 전송 계층에서 처리 | 응용 프로그램 정책에 따름 |
| 메시지 경계 | 별도 Framing 필요 | Datagram 경계 유지 |
| 대표 용도 | 파일·명령·상태 동기화 | 실시간 상태, 지연 민감한 전송 |

UDP는 수신 버퍼가 작으면 Datagram이 잘릴 수 있습니다. 구현할 때 최대 Datagram 크기, 타임아웃, 누락 처리까지 함께 설계합니다. 예제는 자기 자신에게 9바이트를 송신합니다.


**예제 코드 — [08_udp_loopback.cpp](./examples/08_udp_loopback.cpp)**

```cpp
#include "../common/socket.hpp"
#include <iostream>
int main() {
    lesson_net::Runtime runtime;
    lesson_net::Socket receiver{::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)};
    lesson_net::Socket sender{::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)};
    if (!receiver.valid() || !sender.valid()) throw std::runtime_error("UDP socket failed");
    const auto addr = lesson_net::loopback_address(0);
    if (::bind(receiver.get(), reinterpret_cast<const sockaddr*>(&addr), sizeof(addr)) != 0)
        throw std::runtime_error("UDP bind failed");
    lesson_net::set_timeout(receiver, 1000);
    sockaddr_in bound{};
#ifdef _WIN32
    int len = sizeof(bound);
#else
    socklen_t len = sizeof(bound);
#endif
    if (::getsockname(receiver.get(), reinterpret_cast<sockaddr*>(&bound), &len) != 0)
        throw std::runtime_error("getsockname failed");
    constexpr char message[] = "sensor=42";
    if (::sendto(sender.get(), message, 9, 0,
                 reinterpret_cast<const sockaddr*>(&bound), sizeof(bound)) != 9)
        throw std::runtime_error("sendto failed");
    char buffer[32]{};
    const int received = ::recvfrom(receiver.get(), buffer, sizeof(buffer), 0, nullptr, nullptr);
    if (received != 9) throw std::runtime_error("UDP receive failed");
    std::cout << "Datagram: " << std::string(buffer, static_cast<std::size_t>(received)) << '\n';
}
```

**실행 결과**

```text
Datagram: sensor=42
```


---


<a id="section-18-9" ></a>

## 18.9. Timeout, Deadline, Retry


Timeout은 **오랜 시간 기다리지 않고 실패를 반환하는 규칙**입니다. 일반적인 `SO_RCVTIMEO`·`SO_SNDTIMEO`는 개별 호출에 대한 대기 제한일 수 있으며, 여러 번 반복하는 `recv_exact()` 전체의 제한 시간과 다릅니다.

```text
연결 타임아웃 ≠ 한 번 수신 타임아웃 ≠ 전체 요청의 Deadline
```

서비스에서는 `steady_clock` 기준으로 절대 Deadline을 계산하고 남은 시간만 기다리는 방법을 검토합니다. 실패 재시도는 모든 오류에 적용하지 않습니다. Timeout·일시적인 서비스 불가와 잘못된 명령·권한 거부는 다른 정책이 필요합니다. **재시도 가능한 요청인지(멱등성)** 역시 확인해야 합니다.


**예제 코드 — [09_receive_timeout.cpp](./examples/09_receive_timeout.cpp)**

```cpp
#include "../common/socket.hpp"
#include <iostream>
int main() {
    lesson_net::Runtime runtime;
    auto socket = lesson_net::tcp_socket();
    lesson_net::set_timeout(socket, 100);
    std::cout << "Timeout configured (100 ms)\n";
    // A receive timeout is not an overall deadline for a multi-chunk transfer.
}
```

**실행 결과**

```text
Timeout configured (100 ms)
```


---


<a id="section-18-10" ></a>

## 18.10. 오류 모델과 실패 처리


통신 코드는 실패를 하나의 `false`로 뭉개기보다 **실패가 발생한 층위**를 구분하는 편이 좋습니다.

- 소켓 생성·연결 실패: OS 수준 문제
- 길이 헤더 손상·본문 누락: Protocol 오류
- `READ A 1001`: 데이터 검증 실패
- `READ A 30`의 처리 거부: 애플리케이션 정책 실패

예제는 `std::optional<int>`를 이용해 알 수 없는 상태 코드를 명시적으로 구분합니다. 실제 SDK는 `std::error_code`, 사용자 정의 오류 코드, 오류 정보 구조체 등을 사용할 수 있습니다. C++23의 `std::expected`는 참고할 수 있지만, 본 Chapter의 필수 기능은 아닙니다.


**예제 코드 — [10_error_result.cpp](./examples/10_error_result.cpp)**

```cpp
#include <iostream>
#include <optional>
#include <string_view>
[[nodiscard]] std::optional<int> parse_status(std::string_view text) {
    if (text == "OK") return 200;
    if (text == "BAD_REQUEST") return 400;
    return std::nullopt;
}
int main() {
    std::cout << "Known: " << parse_status("OK").value() << '\n';
    std::cout << "Unknown: " << std::boolalpha << !parse_status("?" ) << '\n';
}
```

**실행 결과**

```text
Known: 200
Unknown: true
```


---


<a id="section-18-11" ></a>

## 18.11. Request–Response Protocol


Request–Response는 클라이언트가 요청을 보내고 서버가 결과 또는 오류를 돌려주는 패턴입니다. 가장 작은 예로 `PING → PONG`, `STATUS → READY`를 구현했습니다.

실제 프로토콜은 단순히 요청 텍스트만 정의하면 충분하지 않습니다. **최대 길이, 버전, 인코딩, 오류 코드, 중복 요청 정책**도 함께 정의해야 합니다. TCP 연결이 끊겼을 때 서버가 요청을 이미 처리했는지 알 수 없으므로, 상태 변경 명령에는 요청 ID와 멱등성 정책이 필요할 수 있습니다.


**예제 코드 — [11_request_response.cpp](./examples/11_request_response.cpp)**

```cpp
#include <iostream>
#include <string>
#include <string_view>
[[nodiscard]] std::string process(std::string_view request) {
    if (request == "PING") return "PONG";
    if (request == "STATUS") return "READY";
    return "ERR unknown command";
}
int main() {
    std::cout << process("PING") << '\n' << process("STATUS") << '\n'
              << process("RESET") << '\n';
}
```

**실행 결과**

```text
PONG
READY
ERR unknown command
```


---


<a id="section-18-12" ></a>

## 18.12. 동시 접속과 공유 상태


여러 클라이언트가 동시에 접속하면 처리 순서는 일정하지 않습니다. 공유 카운터, 장치별 집계, 큐 상태 등에 보호 없이 접근하면 Data Race가 발생할 수 있습니다.

예제는 네 개의 작업자 스레드가 250번씩 카운터를 증가시키되 Mutex로 수정과 조회를 보호합니다.

```text
4 workers × 250 operations = 1000 (항상 동일한 결과)
```

Mutex의 목적은 모든 스레드가 같은 순서로 실행되게 하는 것이 아니라, **공유 상태의 변경을 안전하게 직렬화**하는 데 있습니다. 장시간 소켓 I/O를 Mutex 안에서 수행하면 전체 처리량이 줄거나 교착 상태 위험이 커질 수 있으므로, 임계 구역을 짧게 유지합니다.


**예제 코드 — [12_thread_safe_server_state.cpp](./examples/12_thread_safe_server_state.cpp)**

```cpp
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>
class Counter {
public:
    void record() { std::lock_guard guard{mutex_}; ++count_; }
    [[nodiscard]] int value() const { std::lock_guard guard{mutex_}; return count_; }
private:
    mutable std::mutex mutex_;
    int count_{};
};
int main() {
    Counter counter;
    std::vector<std::jthread> workers;
    for (int t = 0; t < 4; ++t) {
        workers.emplace_back([&] { for (int i = 0; i < 250; ++i) counter.record(); });
    }
    workers.clear(); // joins all workers
    std::cout << "Processed: " << counter.value() << '\n';
}
```

**실행 결과**

```text
Processed: 1000
```


---


<a id="section-18-13" ></a>

## 18.13. 협력적 종료와 Shutdown


서버를 종료할 때 작업이 진행 중일 수 있습니다. `std::jthread`와 `std::stop_token`은 **협력적 취소 요청**을 전달할 수 있습니다. 다만 `request_stop()` 자체가 임의의 블로킹 Socket 호출을 자동 중단시키지는 않습니다.

예제에서는 `condition_variable_any`의 Stop Token 지원 대기를 사용합니다. 실제 서버 종료에는 새 연결 수락 중단, 연결 닫기 또는 Wakeup 메커니즘, 작업 큐 종료, 남은 작업 완료 여부 결정이 필요합니다. 순서가 중요하기 때문에 Shutdown 절차는 문서로 정의해야 합니다.


**예제 코드 — [13_cooperative_shutdown.cpp](./examples/13_cooperative_shutdown.cpp)**

```cpp
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <stop_token>
#include <thread>
int main() {
    std::mutex mutex;
    std::condition_variable_any cv;
    bool work_ready = false;
    bool awakened = false;
    std::jthread worker([&](std::stop_token stop) {
        std::unique_lock lock{mutex};
        cv.wait(lock, stop, [&] { return work_ready; });
        awakened = stop.stop_requested();
    });
    worker.request_stop();
    worker.join();
    std::cout << "Stopped: " << std::boolalpha << awakened << '\n';
}
```

**실행 결과**

```text
Stopped: true
```


---


<a id="section-18-14" ></a>

## 18.14. Pipe와 부모·자식 프로세스


Pipe는 하나의 프로세스가 다른 프로세스로 바이트를 전달할 때 사용할 수 있는 단방향 통로입니다. POSIX에서는 `pipe()`로 읽기·쓰기 디스크립터를 만들고 `fork()`로 자식 프로세스를 생성하는 방식을 학습할 수 있습니다.

```text
Parent ----[ pipe write end ]----> Child 혹은 반대 방향
```

예제에서는 자식 프로세스가 `from child`를 쓰고 부모가 읽습니다. 부모와 자식은 사용하지 않는 디스크립터를 즉시 닫아야 합니다. 프로그램 종료 상태는 `waitpid()`로 확인합니다. Windows의 Pipe API는 다르므로 본 소스의 Windows 분기에서는 안내 문구만 출력합니다.


**예제 코드 — [14_posix_pipe.cpp](./examples/14_posix_pipe.cpp)**

```cpp
#include <iostream>
#ifndef _WIN32
#include <array>
#include <stdexcept>
#include <sys/wait.h>
#include <unistd.h>
#endif
int main() {
#ifdef _WIN32
    std::cout << "POSIX pipe requires a POSIX system\n";
#else
    int fds[2]{};
    if (::pipe(fds) == -1) throw std::runtime_error("pipe failed");
    const pid_t pid = ::fork();
    if (pid < 0) { ::close(fds[0]); ::close(fds[1]); throw std::runtime_error("fork failed"); }
    if (pid == 0) {
        ::close(fds[0]);
        constexpr char message[] = "from child";
        const auto n = ::write(fds[1], message, sizeof(message) - 1);
        ::close(fds[1]);
        _exit(n == static_cast<ssize_t>(sizeof(message) - 1) ? 0 : 1);
    }
    ::close(fds[1]);
    std::array<char, 32> buffer{};
    const auto n = ::read(fds[0], buffer.data(), buffer.size());
    ::close(fds[0]);
    int status = 0;
    if (::waitpid(pid, &status, 0) != pid || !WIFEXITED(status) || WEXITSTATUS(status) != 0 || n < 0)
        throw std::runtime_error("child IPC failed");
    std::cout << "IPC: " << std::string(buffer.data(), static_cast<std::size_t>(n)) << '\n';
#endif
}
```

**실행 결과**

```text
IPC: from child
```


---


<a id="section-18-15" ></a>

## 18.15. UNIX Domain Socket과 Local IPC


UNIX Domain Socket은 동일 컴퓨터의 프로세스가 네트워크 IP 없이 데이터를 주고받는 IPC 방식입니다. POSIX `socketpair(AF_UNIX, SOCK_STREAM, ...)`은 이미 연결된 두 소켓을 만들어 테스트하기 편리합니다.

일반적인 UNIX Domain Socket은 파일시스템 경로를 이용할 수도 있습니다. 이 경우 경로 길이·권한·기존 소켓 파일 정리 등의 문제를 고려합니다. 본 예제는 외부에 파일을 생성하지 않는 `socketpair()`를 사용합니다. Windows에서는 별도 API와 지원 환경을 확인해야 합니다.


**예제 코드 — [15_unix_domain_socket.cpp](./examples/15_unix_domain_socket.cpp)**

```cpp
#include <iostream>
#ifndef _WIN32
#include <stdexcept>
#include <sys/socket.h>
#include <unistd.h>
#endif
int main() {
#ifdef _WIN32
    std::cout << "socketpair demonstration requires POSIX\n";
#else
    int handles[2]{};
    if (::socketpair(AF_UNIX, SOCK_STREAM, 0, handles) != 0)
        throw std::runtime_error("socketpair failed");
    constexpr char message[] = "LOCAL";
    const auto sent = ::send(handles[0], message, 5, 0);
    char buffer[16]{};
    const auto received = sent == 5 ? ::recv(handles[1], buffer, sizeof(buffer), 0) : -1;
    ::close(handles[0]);
    ::close(handles[1]);
    if (received != 5) throw std::runtime_error("local IPC failed");
    std::cout << "Local socket: " << std::string(buffer, 5) << '\n';
#endif
}
```

**실행 결과**

```text
Local socket: LOCAL
```


---


<a id="section-18-16" ></a>

## 18.16. Windows IPC와 플랫폼 차이


Windows의 Winsock은 POSIX Socket과 기능이 비슷하지만 초기화, Handle 타입, 종료 함수, 타임아웃 값 형식이 다릅니다. `#ifdef _WIN32`로 플랫폼 차이를 작은 공통 계층에 모아두는 이유입니다.

- TCP/UDP는 Winsock 2의 `WSAStartup()` / `closesocket()` / `WSACleanup()` 사용
- Windows Named Pipe는 TCP Socket과 다른 `CreateNamedPipe()` 계열의 API 사용
- Linux/macOS의 `fork()`와 `socketpair()`는 플랫폼 특화 기능
- CMake는 Windows에서 `ws2_32`를 연결하고 POSIX에서 필요한 Threads 설정 사용

[플랫폼별 상세 안내](./docs/PLATFORM.md)에서 해당 코드를 확인합니다. Windows용 컴파일 분기를 포함했지만 **MSVC 실제 검증은 진행하지 않았습니다.**

---


<a id="section-18-17" ></a>

## 18.17. 신뢰할 수 없는 입력과 프로토콜 검증


통신 상대가 보낸 바이트는 **검증되지 않은 입력**입니다. 정상적인 클라이언트가 보내지 않을 값도 언제든 도착할 수 있다고 가정합니다.

1. **크기 제한:** Length Header를 읽자마자 4096바이트 초과 여부 검사
2. **전체 파싱:** `std::from_chars()` 뒤 `end == last` 확인
3. **타입·범위 확인:** 정수 오버플로·음수·허용되지 않은 명령 거부
4. **문자 인코딩:** ASCII 규칙과 UTF-8 규칙을 혼용하지 않음
5. **권한과 인증:** Loopback이라고 다른 프로세스의 접속까지 신뢰하지 않음
6. **전송 보호:** 실제 운영에서는 TLS, 접근 제어, Rate Limit 등을 별도로 도입

이 예제는 최대 크기를 넘기는 Payload를 인코딩 단계에서 거부합니다. 서버의 프레임 수신 단계도 길이를 검증합니다. 추가 위협 및 확장 조건은 [보안 점검](./docs/SECURITY.md)에 정리했습니다.


**예제 코드 — [16_defensive_protocol.cpp](./examples/16_defensive_protocol.cpp)**

```cpp
#include "../common/socket.hpp"
#include <iostream>
#include <string>
int main() {
    try {
        std::string oversize(lesson_net::max_payload + 1, 'a');
        (void)lesson_net::encode_frame(oversize);
    } catch (const std::length_error&) {
        std::cout << "Rejected: oversized payload\n";
    }
    const std::string data = lesson_net::encode_frame("PING");
    std::cout << "Accepted: " << data.size() << " bytes\n";
}
```

**실행 결과**

```text
Rejected: oversized payload
Accepted: 8 bytes
```


---


<a id="section-18-18" ></a>

## 18.18. 성능, 운영 및 테스트 설계


네트워크 코드의 성능은 평균 응답 시간 하나로 결정되지 않습니다. 연결 생성 비용, 동시 접속 수, Throughput, Tail Latency, 재시도 횟수, 큐 대기 시간을 구분해야 합니다.

테스트는 다음 순서가 유용합니다.

1. **단위 테스트:** 인코딩·파싱·상태 변경의 입력과 출력 검증
2. **Loopback 통합 테스트:** 실제 Socket을 열어 프레임 왕복 확인
3. **오류 테스트:** 길이 초과, 연결 종료, 잘못된 명령, 조기 EOF
4. **동시성 테스트:** 여러 클라이언트의 응답과 집계 불변식 검증
5. **패키지 테스트:** SDK를 설치 후 다른 프로젝트에서 독립 빌드

고정 시간 안에 끝난다는 가정으로 테스트를 작성하기보다, 완료 조건과 최대 허용 시간을 명시합니다. CI 환경의 스케줄링 지연과 실제 네트워크 지연은 구분합니다.

---


<a id="section-18-19" ></a>

## 18.19. Coding Practice


네 문제는 실제로 쓰이는 오류 조건을 중심으로 구성했습니다. **학생용 파일은 구현 전 상태**이며, 모범답안은 별도 폴더에 있습니다. 각 문제는 자동 검증 스크립트로 실행할 수 있습니다.

| 문제 | 학습 목표 | 학생용 | 정답 코드 |
|---|---|---|---|
| ① Frame Decoder | Big-Endian 길이·잘린 메시지·초과 길이 | [01_frame_decoder.cpp](./exercises/01_frame_decoder.cpp) | [모범답안](./solutions/01_frame_decoder.cpp) |
| ② Reading Parser | 명령 전체 파싱·기기 ID·수치 범위 | [02_reading_parser.cpp](./exercises/02_reading_parser.cpp) | [모범답안](./solutions/02_reading_parser.cpp) |
| ③ Retry Policy | 일시 오류와 영구 오류 구분 | [03_retry_policy.cpp](./exercises/03_retry_policy.cpp) | [모범답안](./solutions/03_retry_policy.cpp) |
| ④ Bounded Queue | 생산자·소비자 대기·종료 통지 | [04_bounded_queue.cpp](./exercises/04_bounded_queue.cpp) | [모범답안](./solutions/04_bounded_queue.cpp) |

**검증:**

```bash
python3 tests/check.py --mode student --only exercise-01 --compiler g++-14
python3 tests/check.py --mode solutions --only exercise-01 --compiler g++-14
```

**실습 ① 조건:** 4바이트 길이 헤더를 해석한 후 정확한 길이의 Payload만 반환함. 0바이트 메시지는 허용함. 남는 바이트와 잘린 바이트는 거부함. 4096바이트 초과는 무조건 거부함.

**실습 ② 조건:** `READ <device> <value>` 형식만 허용함. 장치 ID는 `[A-Za-z0-9_-]` 1~16글자, 값은 0~1000. 추가 토큰, 부분 파싱, 앞뒤 불필요한 공백은 거부함.

**실습 ③ 조건:** 실패한 시도 번호는 1부터 시작함. `timeout`·`unavailable`에서만 재시도를 허용하고, `attempt < max_attempts`일 때만 참을 반환함. 잘못된 시도 번호는 거부함.

**실습 ④ 조건:** 큐가 가득 차면 생산자가 대기함. 닫힌 큐에 새 항목을 넣을 수 없지만 기존 항목은 소비할 수 있음. `close()`는 대기 중인 생산자·소비자 모두를 깨워야 함. 0 용량은 예외 처리함.

---


<a id="section-18-20" ></a>

## 18.20. Basic Mini Project — Loopback Echo


### 요구사항

네트워크 프로그래밍을 처음 완성하는 단계입니다. 서버는 임시 Port에서 한 연결을 수락하고 길이 헤더를 확인한 뒤 Payload를 그대로 회신합니다. 클라이언트는 **보낸 바이트와 받은 바이트가 완전히 동일한지** 확인합니다.

| 항목 | 규칙 |
|---|---|
| IP | 127.0.0.1 전용 |
| Port | 운영체제가 배정하는 임시 Port |
| Frame | 4바이트 길이 + Payload 0~4096바이트 |
| 테스트 | 일반 텍스트·빈 Payload·바이너리·길이 초과 |

**프로젝트:** [examples/17_loopback_echo/](./examples/17_loopback_echo/) · [CMakeLists.txt](./examples/17_loopback_echo/CMakeLists.txt)

```bash
cmake -S examples/17_loopback_echo -B build-basic -DCMAKE_BUILD_TYPE=Release
cmake --build build-basic
ctest --test-dir build-basic --output-on-failure
```

<details><summary>구현 점검</summary>

- `Socket`의 복사를 금지하고 이동은 허용했는가?
- 수신 길이를 확인하고 필요한 바이트 수만큼 반복 수신하는가?
- 텍스트에 ` `이 들어 있어도 정확하게 처리하는가?
- 한쪽 연결이 종료되어도 Socket 리소스가 반환되는가?

</details>

---


<a id="section-18-21" ></a>

## 18.21. Advanced Project — Concurrent Telemetry Collector


### 시나리오

여러 장치가 중앙 수집 서버에 측정값을 동시에 제출합니다. 서버는 메시지를 해석해 **장치별 처리 건수와 합계**를 계산하고, 잘못된 기록은 건수에 반영하지 않습니다.

**프로토콜:** `READ <device> <value>`; `device`는 1~16글자, 값은 0~1000. 정상이면 `OK`, 오류면 `ERR invalid reading`을 응답합니다.

| 입력 | 결과 |
|---|---|
| `READ A 20` | A: count +1, sum +20 |
| `READ B 30` | B: count +1, sum +30 |
| `READ A 5` | A: count +1, sum +5 |
| `READ BAD x` | rejected +1 |

**기대 출력:**

```text
Accepted: 3, Rejected: 1
A: 2 / 25
B: 1 / 30
```

**학생용:** [projects/advanced_telemetry_server/](./projects/advanced_telemetry_server/)

**모범답안:** [solutions/advanced_telemetry_server/](./solutions/advanced_telemetry_server/)

```bash
cmake -S solutions/advanced_telemetry_server -B build-advanced
cmake --build build-advanced
ctest --test-dir build-advanced --output-on-failure
```

구현 목표는 단순한 집계 함수뿐 아니라 **동시에 도착한 요청의 처리·거부 정책·공유 상태 잠금**을 완성하는 것입니다. 작업 완료 순서는 달라져도 최종 합계는 같아야 합니다. 이 프로젝트는 최대 32개 클라이언트로 제한해 학습하며, 운영용 네트워크 서비스 수준의 인증·복구·부하 제어는 포함하지 않습니다.

---


<a id="section-18-22" ></a>

## 18.22. Pro Project — Installable ProLink SDK


### 시나리오

프로젝트에 종속된 네트워크 유틸리티를 다른 C++ 프로그램에서도 사용할 수 있도록 **설치 가능한 CMake 패키지**로 만듭니다. 공개 헤더·구현·테스트를 분리하고 `find_package()`와 Namespaced Target을 제공합니다.

| 구성 | 내용 |
|---|---|
| 공개 API | `prolink::process_command`, `decode_packet`, `round_trip` |
| 프로토콜 | `PING` → `PONG`, `UPPER hello` → `HELLO` |
| 오류 모델 | `Error::none`, `invalid_request`, `too_large`, `transport` |
| 패키지 | `ProLinkConfig.cmake`, `ProLinkTargets.cmake` |
| 사용 Target | `ProLink::prolink` |
| 검증 | 로컬 왕복·불완전 Frame·길이 초과·설치·경로 이동·외부 Consumer |

**학생용:** [projects/pro_loopback_sdk/](./projects/pro_loopback_sdk/)

**모범답안:** [solutions/pro_loopback_sdk/](./solutions/pro_loopback_sdk/)

```bash
cmake -S solutions/pro_loopback_sdk -B build-pro -DCMAKE_BUILD_TYPE=Release
cmake --build build-pro
ctest --test-dir build-pro --output-on-failure
cmake --install build-pro --prefix "$(pwd)/build-pro-install"
cmake -S solutions/pro_loopback_sdk/consumer -B build-consumer \
  -DCMAKE_PREFIX_PATH="$(pwd)/build-pro-install"
cmake --build build-consumer
ctest --test-dir build-consumer --output-on-failure
```

Pro의 핵심은 **외부 프로젝트에서 공개 API가 재사용 가능한지** 확인하는 것입니다. 패키지 설정에는 `find_dependency(Threads)`가 포함되며, 설치된 패키지를 별도 폴더로 옮겨도 사용할 수 있도록 상대 경로 기반 설정을 사용합니다. CMake 설치 검증 외에 실제 Linux 패키지·Windows DLL 배포까지 다루지는 않습니다.

---


<a id="section-18-23" ></a>

## 18.23. 설계 점검과 다음 학습


이 Chapter에서 완성한 것은 **로컬 통신과 메시지 검증의 기초**입니다. 외부 공개 서비스를 설계한다면 인증·TLS·비동기 I/O·접속 수 제한·로깅·관측 지표 등 더 많은 계층이 필요합니다.

**설계 점검:**

- Socket 수명과 Shutdown 순서가 명확한가?
- TCP를 메시지 단위로 가정하지 않고 길이·본문을 반복 수신하는가?
- 수신 바이트 수와 파싱 성공 여부를 분리해 확인하는가?
- 동시 처리 시 집계 값에 Data Race가 없는가?
- 재시도해도 안전한 요청만 재전송하는가?
- 설치한 라이브러리를 다른 프로젝트가 직접 빌드할 수 있는가?

추가 학습으로 TLS와 인증, IPv6, 비동기 이벤트 루프, 이벤트 기반 서버, IPC 권한 관리 등을 확장할 수 있습니다.

---


<a id="section-18-24" ></a>

## 18.24. Quiz & Summary



다음 문항은 각 Section의 코드와 실행 규칙을 확인하는 문제입니다. 정답은 문항 아래의 펼치기 영역에 분리했습니다.


**Q01. TCP에서 `send()` 1회와 `recv()` 1회가 일대일 대응하는가?**

<details><summary>정답 및 해설</summary>

아니다. TCP는 메시지가 아닌 바이트 스트림이므로 일부만 수신될 수 있다.

</details>


**Q02. 길이 헤더를 받은 뒤 가장 먼저 확인할 사항은?**

<details><summary>정답 및 해설</summary>

최대 허용 Payload 크기를 초과하는지 검사한다. 이후 필요한 길이만큼 읽는다.

</details>


**Q03. `recv()`의 반환값이 0이면 일반적으로 무엇을 뜻하는가?**

<details><summary>정답 및 해설</summary>

상대가 해당 스트림의 전송을 정상 종료했음을 뜻한다. 프레임 중간이라면 잘린 메시지다.

</details>


**Q04. UDP Datagram에서 전송 순서와 재전송이 자동 보장되는가?**

<details><summary>정답 및 해설</summary>

아니다. 필요한 경우 애플리케이션에서 별도 처리한다.

</details>


**Q05. `127.0.0.1`로 바인딩하는 이유는?**

<details><summary>정답 및 해설</summary>

현재 시스템 안에서만 연결하도록 제한해 외부 인터페이스 노출을 줄이기 위해서다.

</details>


**Q06. 네트워크 Byte Order는 어떤 순서인가?**

<details><summary>정답 및 해설</summary>

Big-Endian(상위 바이트 먼저)이다.

</details>


**Q07. RAII Socket에서 복사를 제한하는 이유는?**

<details><summary>정답 및 해설</summary>

중복 소유권과 중복 close를 막기 위해서다.

</details>


**Q08. `std::jthread::request_stop()`가 블로킹 Socket의 `recv()`를 자동 중단하는가?**

<details><summary>정답 및 해설</summary>

아니다. Socket 종료나 별도 Wakeup/Timeout 전략이 필요하다.

</details>


**Q09. Windows Winsock에서 Socket 사용 전 필요한 초기화는?**

<details><summary>정답 및 해설</summary>

`WSAStartup()`이다. Socket은 `closesocket()`으로 정리한다.

</details>


**Q10. 서로 다른 프로세스 사이에 쓰는 POSIX IPC 예시 두 가지는?**

<details><summary>정답 및 해설</summary>

Pipe와 UNIX Domain Socket이다. 이 Chapter에서 pipe/fork, socketpair를 실습한다.

</details>


**Q11. Timeout 이후 상태 변경 요청을 무조건 재시도하면 안 되는 이유는?**

<details><summary>정답 및 해설</summary>

이미 처리되었는지 불명확할 수 있어 중복 실행을 유발한다. 멱등성 정책이 필요하다.

</details>


**Q12. Pro SDK를 설치한 뒤 별도 Consumer에서 확인할 것은?**

<details><summary>정답 및 해설</summary>

`find_package(ProLink)`와 `ProLink::prolink` 연결, 공개 헤더, 동작 테스트, 설치 경로 이동 후 재빌드다.

</details>


### Summary

- Socket 통신은 운영체제 API를 사용하며 C++20 자체가 네트워크 Socket 표준 API를 제공하지는 않음.
- TCP는 Byte Stream, UDP는 Datagram. TCP의 메시지 경계는 직접 정의해야 함.
- 4바이트 Big-Endian 헤더와 크기 상한을 사용하여 Payload를 검증함.
- Socket Lifetime은 RAII, 공유 상태는 Mutex, 협력적 종료는 Stop Token 등으로 관리함.
- Pipe·UNIX Domain Socket은 POSIX 기반 IPC 예제이며 Windows는 다른 API를 사용함.
- 실제 공개 서비스에는 TLS·인증·Backpressure·Deadline·운영 수준의 로그가 추가로 필요함.

### References

- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/html/)
- [CMake Importing and Exporting Guide](https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html)
- [cppreference — Concurrency Support Library](https://en.cppreference.com/w/cpp/thread)
- [Microsoft — Winsock Programming](https://learn.microsoft.com/en-us/windows/win32/winsock/windows-sockets-start-page-2)
- [C++20 Compiler Support](https://en.cppreference.com/w/cpp/compiler_support/20)

---

[← C++ 목차](../README.md) · [↑ Contents](#contents)


---

