# Basic — Loopback Echo

[← Chapter 18](../../README.md)

**목표:** 소유권·메시지 프레이밍·TCP 왕복.

**버전:** C++20. 테스트는 127.0.0.1 임시 포트만 사용함. 실제 외부 네트워크에 서비스를 노출하지 않음.

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
```

**주요 구성:** `include/` 공개 API, `src/` 구현 및 데모, `tests/` 검증, `CMakeLists.txt` Target 구성.
