# Profiling — 측정 설계와 결과 해석

## 비교 순서

1. Release와 Debug를 혼동하지 않고 빌드 종류를 고정한다.
2. 입력 크기, 데이터 분포, CPU·OS·컴파일러·옵션을 기록한다.
3. 먼저 **결과 정확성**을 검사한다.
4. 워밍업 뒤 여러 차례 측정하고 중앙값·분포를 확인한다.
5. 실행 시간을 단정적으로 설명하지 말고 실제 병목 위치를 도구로 확인한다.
6. 개선 전후에 같은 테스트를 다시 실행한다.

## 실행 가능한 벤치마크

```bash
cmake -S solutions/pro_quality_gate -B build-release -DCMAKE_BUILD_TYPE=Release
cmake --build build-release --parallel 2
./build-release/quality_gate_bench 100000
./build-release/quality_gate_bench 1000000
```

출력 `rows`, `groups`, `checksum`은 정합성을 확인하기 위한 값이고, `ms`는 해당 실행에서 측정된 시간입니다. 시간이 적게 나왔다고 무조건 더 나은 알고리즘이라고 결론 내리지 않습니다.

## Linux perf (설치된 경우)

```bash
perf stat ./build-release/quality_gate_bench 1000000
perf record -g -- ./build-release/quality_gate_bench 1000000
perf report
```

`perf`는 Linux 전용이고, 권한 또는 커널 보안 설정으로 사용이 제한될 수 있습니다. 별도 설치가 필요할 수 있습니다.

## 벤치마크 함정

- `-O0` 결과로 Release 최적화 결정을 내리지 않습니다.
- 첫 실행만 측정하지 않습니다(파일 캐시·메모리 할당·CPU 주파수 영향).
- 입력 크기를 바꾸면 동작 경향이 달라질 수 있습니다.
- 계산 결과를 전혀 사용하지 않으면 컴파일러가 계산 자체를 제거할 수 있습니다.
- `volatile`만으로 최적화 방지가 완벽해지는 것은 아닙니다.
- Sanitizer를 켠 바이너리의 시간은 일반 배포 성능으로 해석하지 않습니다.
- CI 러너의 공유 자원에서 절대 시간 제한을 무리하게 적용하지 않습니다. CI에는 정확성 검사를 우선 배치합니다.
