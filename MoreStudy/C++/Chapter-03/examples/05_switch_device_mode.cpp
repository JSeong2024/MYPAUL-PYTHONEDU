#include <print>

enum class DeviceMode {
    off,
    standby,
    active
};

int main() {
    constexpr DeviceMode mode{DeviceMode::active};

    switch (mode) {
        case DeviceMode::off:
            std::println("Power off");
            break;
        case DeviceMode::standby:
            std::println("Waiting for command");
            break;
        case DeviceMode::active:
            std::println("Device running");
            break;
        default:
            std::println("Unknown device mode");
            return 1;
    }
}
