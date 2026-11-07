#include <functional>
#include <map>
#include <print>
#include <string>
#include <string_view>

int main() {
    std::map<std::string, int, std::less<>> ports{{"camera", 8001}, {"lidar", 8002}};
    const std::string_view name{"lidar"};
    if (const auto it = ports.find(name); it != ports.end()) {
        std::println("{} port: {}", it->first, it->second);
    }
}
