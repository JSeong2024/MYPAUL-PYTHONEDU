# Pro Project — Installable Sensor SDK

## 문제

서로 다른 프로그램에서 `SensorSDK::core`를 재사용할 수 있는 **설치형 CMake 패키지**를 완성합니다. `src/statistics.cpp`의 TODO 구현과 함께, 설치 결과를 독립 소비자 프로젝트에서 확인하세요.

- API: `sensor_sdk::analyze(std::span<const int>)`
- 측정값: 0~1000, 비어 있거나 범위 밖이면 `std::invalid_argument`
- 반환: count / minimum / maximum / average
- CMake 프로젝트 버전: 1.2.0

## 빌드 및 테스트

```bash
cmake -S projects/pro_sensor_sdk -B build/pro-student
cmake --build build/pro-student
ctest --test-dir build/pro-student --output-on-failure
```

테스트는 TODO 완료 전 실패합니다. 모범답안은 [`../../solutions/pro_sensor_sdk/`](../../solutions/pro_sensor_sdk/)에 있습니다.

## 패키지 검증

설치한 후 `consumer/` 폴더를 독립 빌드하고, 소비자가 빌드 폴더의 내부 Include 경로나 라이브러리 경로에 의존하지 않는지 확인합니다. 자세한 명령은 [Chapter 16 README 16.20](../../README.md#section-16-20)을 참고합니다.
