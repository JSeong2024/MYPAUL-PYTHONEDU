#include <iostream>

enum class DeviceMode { off = 0, standby = 1, active = 2 };

int main() {
    int selected{};
    std::cout << "Mode (0-2): " << std::flush;
    // TODO: 정수 입력을 검사합니다.
    // TODO: static_cast<DeviceMode>(selected)로 변환합니다.
    // TODO: switch로 OFF / STANDBY / ACTIVE를 출력합니다.
    // TODO: 0~2 이외의 값은 오류 처리합니다.
    return 0;
}
