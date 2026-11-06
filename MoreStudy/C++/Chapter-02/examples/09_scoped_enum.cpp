#include <cstdint>
#include <print>
#include <utility>

enum class DeviceState : std::uint32_t {
    idle = 0,
    running = 1,
    fault = 2
};

int main() {
    const DeviceState state{DeviceState::running};
    std::println("Device state code: {}", std::to_underlying(state));
}
