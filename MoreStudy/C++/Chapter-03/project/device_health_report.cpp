#include <cstdint>
#include <iostream>

int main() {
    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};

    int battery_percent{};
    double temperature_c{};
    int raw_flags{};

    std::cout << "Battery (0-100): " << std::flush;
    // TODO: 배터리 입력과 범위를 확인합니다.
    std::cout << "Temperature (-40 to 125 C): " << std::flush;
    // TODO: 온도 입력과 범위를 확인합니다.
    std::cout << "Flags (0-7): " << std::flush;
    // TODO: 상태 비트 입력과 범위를 확인합니다.
    // TODO: 세 입력값을 사용해 장치 상태 보고서를 출력합니다.
    // TODO: 결과 상태는 FAULT → POWER OFF → SENSOR NOT READY
    //       → OVERHEAT → LOW BATTERY → READY 순서로 판정합니다.
    return 0;
}
