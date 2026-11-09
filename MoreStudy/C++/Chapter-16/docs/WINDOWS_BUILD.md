# Windows — CMake / MSVC 빌드 안내

Windows에서 Visual Studio의 **Developer PowerShell** 또는 Developer Command Prompt를 사용하면 MSVC의 빌드 도구가 PATH에 설정됩니다. 아래 명령은 저장소의 `MoreStudy/C++/Chapter-16/` 폴더에서 실행합니다.

## Visual Studio 생성기

```powershell
cmake -S examples/17_device_report -B build/basic -G "Visual Studio 17 2022" -A x64
cmake --build build/basic --config Release
ctest --test-dir build/basic -C Release --output-on-failure
```

Visual Studio 버전에 따라 생성기 이름을 변경합니다. Visual Studio 생성기는 다중 구성 생성기이므로 `--config Release`를 지정합니다.

## Ninja 생성기

Ninja가 설치되어 있고 컴파일러 환경이 설정되어 있다면:

```powershell
cmake -S examples/17_device_report -B build/ninja -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build/ninja
ctest --test-dir build/ninja --output-on-failure
```

Preset을 사용하려면 Ninja가 필요합니다.

```powershell
cd examples/17_device_report
cmake --preset debug
cmake --build --preset debug
ctest --preset debug
```

## Pro SDK 설치와 소비자 빌드

```powershell
cmake -S solutions/pro_sensor_sdk -B build/pro
cmake --build build/pro --config Release
ctest --test-dir build/pro -C Release --output-on-failure
cmake --install build/pro --config Release --prefix "$PWD/build/sdk-prefix"

cmake -S solutions/pro_sensor_sdk/consumer -B build/consumer -DCMAKE_PREFIX_PATH="$PWD/build/sdk-prefix"
cmake --build build/consumer --config Release
./build/consumer/Release/sensor_consumer.exe
```

일부 생성기에서는 실행 파일이 `build/consumer/sensor_consumer.exe`에 있으므로 실제 출력 경로를 확인합니다. Visual Studio 2022가 설치되어 있지 않으면 GCC·Clang 또는 설치된 다른 생성기를 사용합니다.

**참고:** MSVC는 예제 CMake 파일에 호환 경고 옵션을 넣었지만, Chapter 16의 자동 검증은 GCC 14와 Clang 17에서 수행했습니다.
