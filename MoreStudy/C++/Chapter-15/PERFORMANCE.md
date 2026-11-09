# Chapter 15 — Performance Measurement

## 목표

`Sensor Batch Analyzer`의 **기준 구현(선형 검색)** 과 **최적화 구현(Hash Index + 정렬)** 을 동일한 입력으로 비교합니다. 정확성 검증 없이 성능만 비교하지 않습니다.

## 빌드

프로젝트 폴더 `examples/17_sensor_batch_analyzer/`에서 실행합니다.

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_STANDARD=20
cmake --build build --parallel 2
ctest --test-dir build --output-on-failure
./build/sensor_batch_analyzer --benchmark 100000
```

Windows의 Visual Studio 다중 구성 생성기는 `cmake --build build --config Release`로 빌드하고, 실행 파일은 보통 `build/Release/` 아래에 있습니다.

## 측정 절차

1. Release 빌드, 컴파일러·CPU·OS를 기록합니다. Debug와 Release를 혼합하지 않습니다.
2. 첫 측정은 워밍업으로 구분하고, 같은 입력으로 5회 이상 반복하여 중앙값 및 최솟값/최댓값을 기록합니다.
3. 두 구현의 결과가 같은지 `Matches: true`로 확인합니다. 출력 파일이 있다면 파일 내용도 비교합니다.
4. 총 소요 시간과 피크 메모리, 데이터 크기(10,000 / 100,000 / 1,000,000행)를 각각 기록합니다.
5. Hash Table과 정렬의 메모리 비용도 함께 평가합니다. 측정에서 이득이 작거나 메모리가 과도하게 늘면 최적화를 재검토합니다.

## 결과 기록 표

| 환경 | 행 수 | 기준(ms, 중앙값) | 최적화(ms, 중앙값) | 피크 메모리 | 일치 |
|---|---:|---:|---:|---:|:---:|
| 컴파일러 / CPU / OS 기입 | 10,000 | 직접 측정 | 직접 측정 | 직접 측정 | 확인 |
| 컴파일러 / CPU / OS 기입 | 100,000 | 직접 측정 | 직접 측정 | 직접 측정 | 확인 |

이 표는 **측정용 템플릿**입니다. 예시 수치를 실제 측정 결과처럼 기재하지 않습니다.

## 유의 사항

- 프로그램 출력 시간은 단일 실행의 관측값입니다. 캐시, CPU 부하, 발열, 클럭에 따라 달라집니다.
- **기준 구현:** 입력 n개와 서로 다른 장치 d개에 대해 최대 O(n·d), 결과 정렬 O(d log d).
- **최적화 구현:** 해시 삽입은 평균 O(n), 최종 정렬 O(d log d). 최악의 해시 충돌 비용은 더 클 수 있습니다.
- `std::unordered_map`은 노드/버킷 메모리 오버헤드가 있으므로 언제나 `std::vector`보다 빠르지는 않습니다.
- 측정 결과는 C++ 언어 차원의 성능 보장이나 플랫폼 전체에 대한 결론이 아닙니다.
