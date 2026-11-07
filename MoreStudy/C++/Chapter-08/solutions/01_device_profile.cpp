#include <print>
#include <string>

struct DeviceProfile {
    std::string name;
    int power_w{};
    bool online{};
};

[[nodiscard]] bool valid_profile(const DeviceProfile& profile) {
    return !profile.name.empty() && profile.power_w >= 0 &&
           profile.power_w <= 2'000;
}

int main() {
    const DeviceProfile device{"Vacuum-A", 850, true};
    std::println("Valid: {}", valid_profile(device));
}
