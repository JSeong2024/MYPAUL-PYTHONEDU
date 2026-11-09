# Sanitizers — 런타임 오류 찾기

이 문서의 `buglab/` 파일에는 **일부러 결함을 심은 코드**가 들어 있습니다. 자동 테스트와 배포 코드에 포함하지 않으며, 격리된 로컬 실습에서만 사용합니다. 검출되지 않았다고 안전하다는 뜻은 아닙니다.

## AddressSanitizer (ASan)

Linux + Clang 또는 GCC에서:

```bash
clang++ -std=c++20 -O1 -g -fno-omit-frame-pointer \
  -fsanitize=address buglab/01_out_of_bounds.cpp -o /tmp/ch17_asan
/tmp/ch17_asan
```

`heap-buffer-overflow` 등이 보고되면 입력 범위 검사를 추가해 수정합니다. 안전한 예제 `examples/11_address_sanitizer_fix.cpp`와 비교해 봅니다. ASan은 메모리 접근 오류를 탐지하지만 **모든 메모리 문제**를 발견하지는 못합니다.

## UndefinedBehaviorSanitizer (UBSan)

```bash
clang++ -std=c++20 -O1 -g -fsanitize=undefined \
  -fno-sanitize-recover=undefined buglab/02_signed_overflow.cpp -o /tmp/ch17_ubsan
/tmp/ch17_ubsan
```

부호 있는 정수 오버플로는 정의되지 않은 동작입니다. 안전한 예제 `examples/12_undefined_behavior_fix.cpp`에서 덧셈 전에 범위를 검사하는 방법을 확인합니다.

## ThreadSanitizer (TSan)

```bash
clang++ -std=c++20 -O1 -g -pthread -fsanitize=thread \
  buglab/03_data_race.cpp -o /tmp/ch17_tsan
/tmp/ch17_tsan
```

Data Race를 검출할 수 있지만 실행 환경에 따라 TSan 런타임을 사용하지 못하거나 환경 제약으로 종료될 수 있습니다. ASan과 TSan을 동시에 켜지 않습니다. 안전한 예제 `examples/13_thread_sanitizer_fix.cpp`에서는 Mutex를 사용합니다.

## Pro 프로젝트에서 검증

```bash
cmake -S solutions/pro_quality_gate -B build-asan \
  -DCMAKE_BUILD_TYPE=Debug -DCH17_ENABLE_SANITIZERS=ON
cmake --build build-asan
ctest --test-dir build-asan --output-on-failure
```

해당 옵션은 Linux/POSIX의 GCC·Clang에서 ASan/UBSan을 켭니다. 검증 실행과 성능 측정은 분리합니다. Windows의 MSVC는 지원하는 개별 옵션을 별도 확인합니다.

## 참고 자료

- https://clang.llvm.org/docs/AddressSanitizer.html
- https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html
- https://clang.llvm.org/docs/ThreadSanitizer.html
