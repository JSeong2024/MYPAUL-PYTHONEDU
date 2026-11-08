#include <optional>
#include <string>
#include <utility>
#ifndef CH12_LIBRARY_ONLY
#include <iostream>
#endif

struct Device {
    std::string name;
    int limit{};
};

[[nodiscard]] std::optional<Device> make_device(std::string name, int limit) {
    // TODO 1: 이름 1~16자, 영문/숫자/하이픈만 허용합니다.
    // TODO 2: limit는 0~100 범위여야 합니다.
    // TODO 3: 실패하면 std::nullopt, 성공하면 Device를 반환합니다.
    (void)name;
    (void)limit;
    return std::nullopt;
}

#ifndef CH12_LIBRARY_ONLY
int main() {
    auto device = make_device("sensor-A", 80);
    if (device) std::cout << "Created: " << device->name << " / " << device->limit << '\n';
    if (!make_device("", 20)) std::cout << "Rejected empty name\n";
}
#endif
