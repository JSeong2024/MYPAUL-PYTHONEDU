# Advanced Project — 모범답안

`src/pipeline.cpp`에서 문자열 전체 소비를 검사하는 `std::from_chars`를 사용하며, 잘못된 입력 행은 거부하고 정상 처리 흐름을 이어갑니다. 입력 줄의 순서는 유지하고, `std::map`으로 결과를 장치 ID 순서대로 출력합니다.

```bash
cmake -S solutions/advanced_pipeline -B build/advanced -DPIPELINE_BUILD_TESTS=ON
cmake --build build/advanced
ctest --test-dir build/advanced --output-on-failure
```

[Chapter 16으로 돌아가기](../../README.md#section-16-19)
