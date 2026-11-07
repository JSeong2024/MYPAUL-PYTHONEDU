#include <print>
#include <string>

int main() {
    const std::string device_id{"SENSOR-ROOM-07"};

    std::println("Prefix: {}", device_id.starts_with("SENSOR-"));
    std::println("Contains ROOM: {}", device_id.contains("ROOM"));
    std::println("Suffix: {}", device_id.ends_with("-07"));

    const auto delimiter = device_id.find('-');
    if (delimiter != std::string::npos) {
        std::println("Category: {}", device_id.substr(0, delimiter));
    }
}
