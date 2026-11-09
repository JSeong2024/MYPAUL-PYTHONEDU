# Advanced Project — Configurable Pipeline

## 문제

`data/measurements.csv`를 순서대로 읽어 파싱 오류 행을 거부하고, 유효한 `ok` 행만 장치 ID 오름차순으로 집계합니다. `src/pipeline.cpp`의 TODO를 구현합니다.

- 정상 상태: `ok`, 무효 상태: `bad`
- 측정값: 0~100 범위 정수
- 잘못된 행: `Parsed::rejected` 증가, 다음 행 계속 처리
- 경보: 측정값 80 이상

## 빌드

```bash
cmake -S projects/advanced_pipeline -B build/advanced-student -DPIPELINE_BUILD_TESTS=ON
cmake --build build/advanced-student
ctest --test-dir build/advanced-student --output-on-failure
```

`Chapter-16/`에서 실행합니다. TODO가 완료되기 전에는 테스트 실패가 정상입니다. 모범답안은 [`../../solutions/advanced_pipeline/`](../../solutions/advanced_pipeline/)에 있습니다.
