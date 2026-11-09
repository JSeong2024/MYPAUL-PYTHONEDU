# Pro — Installable ProLink SDK

[← Chapter 18](../../README.md)

**목표:** 재배치 가능한 CMake 라이브러리 패키지와 외부 소비자 검증.

**버전:** C++20. 테스트는 127.0.0.1 임시 포트만 사용함. 실제 외부 네트워크에 서비스를 노출하지 않음.

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
```

**주요 구성:** `include/` 공개 API, `src/` 구현 및 데모, `tests/` 검증, `CMakeLists.txt` Target 구성.

**설치 후 외부 소비자 예시:**

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
cmake --install build --prefix install
cmake -S consumer -B consumer-build -DCMAKE_PREFIX_PATH="$(pwd)/install"
cmake --build consumer-build
ctest --test-dir consumer-build --output-on-failure
```

공개 헤더는 `include/prolink/api.hpp`이며 CMake Target은 `ProLink::prolink`임.
