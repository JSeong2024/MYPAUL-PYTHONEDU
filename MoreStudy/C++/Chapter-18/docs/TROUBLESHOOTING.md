# 실행 및 테스트 문제 해결

[← Chapter 18](../README.md)

| 현상 | 확인할 항목 |
|---|---|
| `socket failed` | OS 소켓 사용 권한, Winsock 초기화 여부 |
| `bind/listen failed` | OS 네트워크 정책, IPv4 Loopback 사용 가능 여부 |
| `accept failed or timed out` | 클라이언트 연결 여부, 타임아웃과 스케줄링 지연 |
| `recv failed/truncated frame` | 길이 헤더와 Payload 길이 일치, 조기 종료 여부 |
| `frame length exceeds 4096` | 네트워크 길이 헤더와 크기 상한 확인 |
| `Threads::Threads` CMake 오류 | 설치형 Pro SDK의 `find_dependency(Threads)` 확인 |
| Windows 링크 오류 | 사용 Target에 `ws2_32` 연결 여부 |
| 예제 14·15가 POSIX 안내만 표시 | Windows 빌드의 의도된 동작 |
| 테스트가 느리거나 실패 | 로컬 호스트 방화벽·보안 소프트웨어·CI 샌드박스 제한 여부 |

전체 테스트는 `python3 tests/check.py --compiler g++-14`로 실행함. `--only examples`, `--only project`, `--only exercise-02` 같은 제한 실행도 가능함 (프로젝트는 `--only projects`로 실행).
