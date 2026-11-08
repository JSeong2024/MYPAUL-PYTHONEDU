#include <cstdint>
#include <iostream>

int main() {
    constexpr std::uint32_t power_on{1U << 0};
    constexpr std::uint32_t sensor_ready{1U << 1};
    constexpr std::uint32_t fault{1U << 2};
    int raw_flags{};

    std::cout << "Flags (0-7): " << std::flush;
    // TODO: 0~7 정수 입력을 검사합니다.
    // TODO: raw_flags를 std::uint32_t로 변환합니다.
    // TODO: 오류 비트가 있으면 FAULT를 출력합니다.
    // TODO: 전원과 센서 비트가 모두 있으면 READY, 그 외에는 NOT READY.
    return 0;
}
