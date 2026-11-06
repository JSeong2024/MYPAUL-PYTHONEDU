#include <print>
#include <string>

int main() {
    int retry_count{};
    bool connected{false};
    std::string device_name{"Lidar-01"};

    std::println("Device: {}", device_name);
    std::println("Retries: {}", retry_count);
    std::println("Connected: {}", connected);
}
