#include <iostream>

enum class DeviceState {
    idle = 0,
    running = 1,
    stopped = 2
};

int main() {
    const DeviceState state{DeviceState::running};

    std::cout << "State code: " << static_cast<int>(state) << '\n';
}
