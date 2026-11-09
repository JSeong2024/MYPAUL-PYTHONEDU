# 환경별 네트워크·IPC 차이

[← Chapter 18](../README.md)

## Linux / macOS (POSIX)

* TCP/UDP: `<sys/socket.h>`, `<arpa/inet.h>`, `<unistd.h>` 등 사용
* 소켓 핸들 타입은 정수 파일 디스크립터, 해제는 `close()`
* `pipe()` + `fork()`는 부모·자식 간 바이트 전달 예제로 사용
* `socketpair(AF_UNIX, SOCK_STREAM, ...)`은 로컬 바이트 스트림 IPC 예제임
* Linux에서는 `send(..., MSG_NOSIGNAL)`로 끊긴 소켓에 보낼 때 발생할 수 있는 `SIGPIPE`를 억제할 수 있음
* 일부 POSIX 플랫폼은 별도로 `SO_NOSIGPIPE` 등의 설정이 필요할 수 있음

## Windows (Winsock)

* TCP/UDP: `<winsock2.h>`, `<ws2tcpip.h>`와 `ws2_32` 라이브러리 사용
* **`WSAStartup()` 호출 후에 소켓 API 사용**, 사용 종료 시 `WSACleanup()`
* 핸들 타입은 `SOCKET`, 무효 값은 `INVALID_SOCKET`, 해제는 `closesocket()`
* `SO_RCVTIMEO` 등의 값 형식은 POSIX와 다름
* 본 Chapter의 POSIX `pipe()/fork()/socketpair()` 예제는 Windows에서 개념 안내 문구만 출력함
* Windows의 Named Pipe는 `CreateNamedPipe()` / `ConnectNamedPipe()` / `CreateFile()` 계열의 별도 API를 사용함

## CMake

* 프로젝트는 `find_package(Threads REQUIRED)`로 스레드 지원을 지정함
* Windows에서는 소켓을 사용하는 Target에 `ws2_32`를 연결함
* Linux에서는 일반적으로 `-pthread`가 스레드 작업에 필요함
* Windows/MSVC 소켓 빌드는 **구성했으나 실제 Windows 빌드를 테스트하지 않았음**

## 포트·경로

* 테스트 서버는 `127.0.0.1`과 **임시 포트(0으로 bind 후 getsockname)** 만 사용함
* 예제에서 공개 IP, 고정 포트, 인터넷 접속이나 방화벽 설정 변경을 요구하지 않음
* 실행이 차단되면 로컬 보안 정책·컨테이너 네트워크 권한부터 점검함
* POSIX 파일 경로 기반 UNIX Domain Socket은 별도의 파일 권한·정리 정책이 필요함
