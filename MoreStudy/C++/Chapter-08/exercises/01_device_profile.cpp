#include <print>
#include <string>

struct DeviceProfile {
    std::string name;
    int power_w{};
    bool online{};
};

[[nodiscard]] bool valid_profile(const DeviceProfile& profile) {
    // TODO: 이름이 비어 있지 않고, 소비 전력이 0~2000W인 경우에만 true 반환
    (void)profile;
    return false;
}

int main() {
    const DeviceProfile device{"Vacuum-A", 850, true};
    std::println("Valid: {}", valid_profile(device));
}
