#include <cstdint>
#include <print>
#include <string>

int main() {
    using std::println;

    const std::string device_name{"Sensor-A1"};
    const std::uint32_t device_id{1'024};
    const bool active{true};

    println("Device: {} (ID: {})", device_name, device_id);
    println("Active: {}", active);
}
