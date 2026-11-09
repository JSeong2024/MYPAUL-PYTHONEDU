# Pro Project — QualityGate SDK

C++20 정산형 센서 검증 라이브러리의 **테스트 전략과 배포 품질 게이트**를 구축합니다.

- `summarize()`는 유효한 측정만 집계하고 기기 ID 오름차순으로 반환합니다.
- `valid=false` 측정은 검사하지 않고 건너뜁니다. `valid=true`인데 빈 ID 또는 0~100 범위 밖 값이면 `std::invalid_argument`를 던집니다.
- 단위 테스트와 고정 시드 Property 기반 테스트로 로직을 검증합니다.
- 로컬 성능 측정은 `quality_gate_bench`를 사용하며, 측정값은 정답 판정에 사용하지 않습니다.
- 설치·이동 후 소비자 프로젝트에서 `find_package(QualityGate 1 CONFIG REQUIRED)`로 다시 빌드합니다.

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j 2
ctest --test-dir build --output-on-failure
cmake --install build --prefix ./stage
cmake -S consumer -B build-consumer -DCMAKE_PREFIX_PATH="$PWD/stage"
cmake --build build-consumer
./build-consumer/quality_consumer
```

GCC·Clang이 지원하는 Linux/POSIX 환경에서 로컬 Sanitizer 실습:

```bash
cmake -S . -B build-asan -DCH17_ENABLE_SANITIZERS=ON -DCMAKE_BUILD_TYPE=Debug
cmake --build build-asan
ctest --test-dir build-asan --output-on-failure
```

`CH17_ENABLE_SANITIZERS=ON`은 ASan/UBSan 전용이며 TSan과 동시에 사용하지 않습니다. 플랫폼/환경에 따라 런타임 지원이 다릅니다.
