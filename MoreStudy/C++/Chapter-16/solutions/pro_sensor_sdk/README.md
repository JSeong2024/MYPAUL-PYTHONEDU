# Pro Project — 모범답안

`SensorSDK::core` 정적 라이브러리를 설치 및 내보내며, `SensorSDKConfig.cmake`, `SensorSDKConfigVersion.cmake`, `SensorSDKTargets.cmake`를 생성합니다. 소비자는 `find_package(SensorSDK 1.2 CONFIG REQUIRED)`로 패키지를 찾습니다.

```bash
cmake -S solutions/pro_sensor_sdk -B build/pro -DCMAKE_BUILD_TYPE=Release
cmake --build build/pro
ctest --test-dir build/pro --output-on-failure
cmake --install build/pro --prefix "$(pwd)/build/sdk-prefix"
```

다른 설치 경로에서도 패키지를 사용할 수 있도록 `BUILD_INTERFACE`/`INSTALL_INTERFACE`를 나누고 있습니다. [Chapter 16으로 돌아가기](../../README.md#section-16-20)
