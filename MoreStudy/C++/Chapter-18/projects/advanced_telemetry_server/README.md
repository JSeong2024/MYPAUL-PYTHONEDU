# Advanced — Concurrent Telemetry Collector

[← Chapter 18](../../README.md)

**목표:** 복수 클라이언트의 동시 처리와 집계의 일관성.

**버전:** C++20. 테스트는 127.0.0.1 임시 포트만 사용함. 실제 외부 네트워크에 서비스를 노출하지 않음.

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
```

**주요 구성:** `include/` 공개 API, `src/` 구현 및 데모, `tests/` 검증, `CMakeLists.txt` Target 구성.

**입력 규칙:** `READ <device> <0~1000>`; 장치별 합계, 정상·거부 건수. 스레드별 응답 순서는 고정하지 않음. 각 요청은 독립된 TCP 연결을 사용함.

**학생용 TODO:** 핵심 처리 함수 일부가 비어 있어 기본 테스트 실패가 정상임. 완성본은 `../../solutions/` 아래 동일한 프로젝트에 있음.
