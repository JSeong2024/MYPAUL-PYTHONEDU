# Debugging — 재현에서 수정까지

## 1. 재현 가능한 최소 사례

1. 사용 중이던 입력과 실행 명령을 기록한다.
2. 예상 결과와 실제 결과를 정확하게 구분한다.
3. 불필요한 모듈을 줄여 동일한 결함이 재현되는 최소 사례를 만든다.
4. 실패하는 테스트를 **먼저** 작성한 뒤 코드를 수정한다.
5. 기존 테스트와 새 회귀 테스트를 함께 실행한다.

## 2. GCC / GDB (Linux)

```bash
g++-14 -std=c++20 -Wall -Wextra -Wpedantic -g -O0 \
  examples/10_debugger_repro.cpp -o /tmp/ch17_debug
gdb --args /tmp/ch17_debug
```

GDB 프롬프트에서:

```text
break sum_positive
run
next
print total
print value
backtrace
continue
quit
```

`break`는 함수 진입점에 중단점을 두고, `next`는 현재 프레임에서 한 줄씩 진행합니다. 특정 줄의 지역 변수는 실행 전/후 시점에 따라 아직 초기화되지 않을 수 있습니다.

## 3. Clang / LLDB

```bash
clang++ -std=c++20 -Wall -Wextra -Wpedantic -g -O0 \
  examples/10_debugger_repro.cpp -o ch17_debug
lldb ./ch17_debug
```

```text
breakpoint set --name sum_positive
run
next
frame variable
bt
continue
quit
```

디버거 자체 설치 여부는 환경마다 다릅니다. VS Code에서는 C++ 확장 기능과 해당 디버거의 설치 경로를 확인합니다.

## 4. 디버깅 중 주의

- 최적화가 활성화되면 변수나 실행 흐름이 소스와 다르게 보일 수 있습니다.
- `-O0 -g`는 원인 추적에 유리하지만 Release 성능을 대변하지 않습니다.
- 멀티스레드 버그는 중단점으로 스케줄이 바뀌어 재현되지 않을 수 있습니다.
- `std::cout` 출력 순서만으로 스레드의 올바른 동기화를 검증할 수 없습니다.
